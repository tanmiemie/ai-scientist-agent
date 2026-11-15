"""LLM reviewer ensemble for one experiment: it FLAGS concerns, it never overrules the numeric gate.

    GPU_EXPERIMENTS=experiments_review python review.py exp_005          # one experiment
    GPU_EXPERIMENTS=experiments_review python review.py --all            # every non-seed experiment

After Sakana's AI Scientist (perform_review: several reviewers at low temperature): the same evidence
pack is sent N_REVIEWS=5 times at temperature 0.1 and a checklist item is kept only if at least
KEEP_VOTES=3 of the 5 reviews flag it. The evidence is computed here from files the loop already wrote
(ledger.jsonl, report_dev/holdout.json, forecast_all.csv[.gz], diagnosis.md); the reviewer sees DEV and
HOLDOUT reports of this experiment and of the champion it was compared with, never TEST. Writes
<exp>/review.json; report.py prints the kept flags. API key from OPENAI_API_KEY / ANTHROPIC_API_KEY only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

import config as C
from report import _diff

N_REVIEWS, KEEP_VOTES, TEMPERATURE = 5, 3, 0.1
MAX_ATTEMPTS = 3  # per review: invalid replies are retried, never counted as votes
ITEMS = {
    "leakage_risk": "the experiment could use information not available at the forecast origin "
                    "(future truth, later data vintages, HOLDOUT used for choices, look-ahead in features)",
    "gain_from_few_series": "the DEV gain over the champion is carried by a few (large, expensive) series "
                            "while most series are flat or worse",
    "interval_widened_not_centred": "the score improved mainly because the q10-q90 interval got wider "
                                    "(coverage up), not because the median or the interval got better placed",
    "repeats_rejected_idea": "the hypothesis overlaps an idea the ledger already rejected (same mechanism, "
                             "possibly different parameters)",
    "other": "any other concern a careful reviewer would raise (overfitting DEV, DEV/HOLDOUT divergence, "
             "hypothesis not tested by the change, ...)",
}
SYSTEM = """You review one experiment of an autonomous forecasting research loop (GPU rental prices,
q10/q50/q90 forecasts, pinball-loss skill vs the last value; positive is better). A numeric gate already
decided accept/reject; you do NOT change that decision. Your job is to flag concerns a careful scientist
would raise, using only the evidence given. Be specific and cite numbers from the evidence.
Answer with JSON only:
{"items": {"<item>": {"flag": true|false, "evidence": "<one or two sentences with numbers>", "severity": 1|2|3}},
 "summary": "<one sentence>"}
Use exactly these items: """ + ", ".join(ITEMS) + """.
severity: 1 = minor, 2 = would change how the result is reported, 3 = result should not be trusted.
Use severity 1 with flag false when there is no concern."""


def _ledger(exp_dir: Path) -> list[dict]:
    return [json.loads(l) for l in (exp_dir / "ledger.jsonl").read_text().splitlines() if l.strip()]


def _report(exp_dir: Path, eid: str, win: str) -> dict:
    return json.loads((exp_dir / eid / f"report_{win}.json").read_text())


def _forecast(exp_dir: Path, eid: str) -> pd.DataFrame | None:
    for name in ("forecast_all.csv.gz", "forecast_all.csv"):
        p = exp_dir / eid / name
        if p.exists():
            return pd.read_csv(p, parse_dates=["origin_date"])
    return None


def _width(fc: pd.DataFrame | None, origins) -> float | None:
    """Mean log(q90/q10) over the origins the archived report was scored on (its own scope, not the current env)."""
    if fc is None or not origins:
        return None
    f = fc[fc.origin_date.isin(pd.to_datetime(list(origins)))]
    f = f[(f.q10 > 0) & (f.q90 > 0)]
    return round(float(np.log(f.q90 / f.q10).mean()), 5) if len(f) else None


def _per_series(rep: dict) -> pd.DataFrame:
    d = pd.DataFrame(rep["per_series"]).set_index("series_id")
    d["total"] = d.pinball * d.n_cells
    d["group"] = [".".join(s.split(".")[:2]) for s in d.index]
    return d


def evidence(exp_dir: Path, eid: str) -> dict:
    recs = _ledger(exp_dir)
    by_id = {r["id"]: r for r in recs}
    r = by_id[eid]
    champ = by_id.get(r.get("champion_before"))
    keys = ("skill_pooled", "skill_median_of_series", "skill_geomean", "coverage_in", "by_horizon")
    ev = {"experiment": eid, "hypothesis": r["hypothesis"],
          "gate_decision": {"accepted": r["accepted"], "reason": r.get("reason")},
          "this": {w: {k: r[w].get(k) for k in keys} for w in ("dev", "holdout")}}
    if champ is None:
        return ev
    ev["compared_with_champion"] = champ["id"]
    ev["spec_change_vs_champion"] = _diff(champ["spec"], r["spec"])
    ev["champion"] = {w: {k: champ[w].get(k) for k in keys} for w in ("dev", "holdout")}

    a, b = _per_series(_report(exp_dir, eid, "dev")), _per_series(_report(exp_dir, champ["id"], "dev"))
    j = a[["total", "group"]].join(b[["total"]], rsuffix="_champ", how="inner")
    j["gain"] = j.total_champ - j.total             # positive = this experiment has lower loss
    tot = float(j.gain.sum())
    top = j.gain.abs().sort_values(ascending=False).index[:3]
    ev["dev_per_series_vs_champion"] = {
        "n_series": int(len(j)), "better": int((j.gain > 0).sum()), "worse": int((j.gain < 0).sum()),
        "total_loss_reduction": round(tot, 6),
        "largest_3_series_by_abs_change": {s: round(float(j.gain[s]), 6) for s in top},
        "share_of_absolute_change_from_largest_3": round(float(j.gain[top].abs().sum() / j.gain.abs().sum()), 3)
        if j.gain.abs().sum() else None,
    }
    grp = j.groupby("group")[["total", "total_champ"]].sum()
    base = (a.baseline_pinball * a.n_cells).groupby(a.group).sum()
    ev["dev_skill_by_group"] = {g: {"this": round(1 - grp.total[g] / base[g], 4),
                                    "champion": round(1 - grp.total_champ[g] / base[g], 4)} for g in grp.index}
    fc_this, fc_champ = _forecast(exp_dir, eid), _forecast(exp_dir, champ["id"])
    ev["mean_log_interval_width_q90_over_q10"] = {
        w: {"this": _width(fc_this, _report(exp_dir, eid, w)["scope"]["origins"]),
            "champion": _width(fc_champ, _report(exp_dir, champ["id"], w)["scope"]["origins"])}
        for w in ("dev", "holdout")}
    ev["rejected_earlier_in_ledger"] = [
        {"id": x["id"], "hypothesis": x["hypothesis"][:300], "lesson": (x.get("lesson") or x.get("reason") or "")[:300]}
        for x in recs[:recs.index(r)] if not x["accepted"]]
    diag = exp_dir / eid / "diagnosis.md"
    if diag.exists():
        ev["diagnosis_dev"] = diag.read_text()[:6000]
    return ev


def _chat(provider: str, model: str, system: str, user: str) -> str:
    if provider == "openai":
        body = {"model": model, "temperature": TEMPERATURE, "response_format": {"type": "json_object"},
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions", json.dumps(body).encode(),
                                     {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                                      "Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=180).read())["choices"][0]["message"]["content"]
    body = {"model": model, "max_tokens": 2000, "temperature": TEMPERATURE, "system": system,
            "messages": [{"role": "user", "content": user}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", json.dumps(body).encode(),
                                 {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
                                  "content-type": "application/json"})
    return "".join(b.get("text", "") for b in json.loads(urllib.request.urlopen(req, timeout=180).read())["content"])


def _parse(txt: str) -> dict:
    """Strict checklist parse; raises ValueError unless every item has a bool flag, str evidence, int severity 1-3."""
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        raise ValueError("no JSON object in reply")
    items = json.loads(m.group(0)).get("items")
    if not isinstance(items, dict):
        raise ValueError("missing 'items'")
    out = {}
    for k in ITEMS:
        it = items.get(k)
        if not isinstance(it, dict):
            raise ValueError(f"missing item {k}")
        flag, ev, sev = it.get("flag"), it.get("evidence"), it.get("severity")
        if not isinstance(flag, bool) or not isinstance(ev, str) or isinstance(sev, bool) \
                or not isinstance(sev, int) or not 1 <= sev <= 3:
            raise ValueError(f"invalid item {k}: {it!r}"[:200])
        out[k] = {"flag": flag, "evidence": ev, "severity": sev}
    return out


def _one_review(provider: str, model: str, user: str) -> dict:
    err = None
    for _ in range(MAX_ATTEMPTS):
        try:
            return _parse(_chat(provider, model, SYSTEM, user))
        except (ValueError, json.JSONDecodeError) as e:
            err = e
    raise RuntimeError(f"no valid checklist after {MAX_ATTEMPTS} attempts: {err}")


def review(exp_dir: Path, eid: str, provider: str, model: str) -> dict:
    ev = evidence(exp_dir, eid)
    user = "CHECKLIST:\n" + json.dumps(ITEMS, indent=1) + "\n\nEVIDENCE:\n" + json.dumps(ev, indent=1, default=str)
    runs = [_one_review(provider, model, user) for _ in range(N_REVIEWS)]  # all 5 valid, or no review.json
    agg = {}
    for k in ITEMS:
        votes = [x[k] for x in runs if x[k]["flag"]]
        agg[k] = {"votes": len(votes), "kept": len(votes) >= KEEP_VOTES,
                  "severity": int(statistics.median_low([v["severity"] for v in votes])) if votes else None,
                  "evidence": [v["evidence"] for v in votes]}
    out = {"experiment": eid, "provider": provider, "model": model, "n_reviews": N_REVIEWS,
           "keep_if_votes_at_least": KEEP_VOTES, "temperature": TEMPERATURE,
           "kept_flags": [k for k in ITEMS if agg[k]["kept"]], "items": agg, "reviews": runs,
           "note": "Flags only; the numeric gate's accept/reject decision is unchanged."}
    (exp_dir / eid / "review.json").write_text(json.dumps(out, indent=1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exp", nargs="*")
    ap.add_argument("--all", action="store_true", help="every experiment with a champion to compare against")
    ap.add_argument("--provider", default="openai", choices=["openai", "anthropic"])
    ap.add_argument("--model", default=None)
    a = ap.parse_args()
    model = a.model or os.environ.get("GPU_LLM_MODEL") or ("gpt-4.1" if a.provider == "openai" else "claude-sonnet-5-5")
    exp_dir = C.EXPERIMENTS
    ids = [r["id"] for r in _ledger(exp_dir) if r.get("champion_before")] if a.all else a.exp
    for eid in ids:
        out = review(exp_dir, eid, a.provider, model)
        print(f"{eid}: " + (", ".join(f"{k} ({out['items'][k]['votes']}/{N_REVIEWS}, sev {out['items'][k]['severity']})"
                                      for k in out["kept_flags"]) or "no flags kept"))


if __name__ == "__main__":
    main()
