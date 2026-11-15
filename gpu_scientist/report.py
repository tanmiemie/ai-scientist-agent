"""Write the research report for one experiments folder, from its ledger alone (no LLM).

    python report.py                      # experiments folder from config (GPU_EXPERIMENTS)
    GPU_EXPERIMENTS=experiments_final python report.py

Writes REPORT.md next to ledger.jsonl: what was tried, in order, what each test showed, what was kept
and why, what was rejected and the lesson the loop wrote down. autoresearch.py calls it after each run.
"""
from __future__ import annotations

import json
from pathlib import Path

import config as C

METRIC = "skill_pooled"


def _f(x, nd=3):
    return "n/a" if x is None else f"{x:+.{nd}f}" if isinstance(x, float) and abs(x) < 10 else f"{x}"


def _models(spec: dict) -> str:
    ms = spec.get("models", [])
    names = ", ".join(m.get("name", "?") for m in ms) or "?"
    comb = spec.get("combine", {}).get("method", "single")
    cal = spec.get("calibrate", {})
    cal_s = f"calibration by {cal.get('group_by') or 'group'}" if cal.get("enabled") else "no calibration"
    return f"{names} ({comb}; {cal_s})"


def _diff(parent: dict | None, spec: dict) -> str:
    """Plain list of top-level parameters that differ from the parent spec."""
    if not parent:
        return "starting point"
    out = []
    pm = {m.get("name"): m for m in parent.get("models", [])}
    for m in spec.get("models", []):
        p = pm.get(m.get("name"))
        if p is None:
            out.append(f"adds model `{m.get('name')}`")
            continue
        for k, v in m.items():
            if p.get(k) != v and k != "name":
                out.append(f"`{m['name']}.{k}`: {p.get(k)} → {v}")
    for name in pm:
        if name not in {m.get("name") for m in spec.get("models", [])}:
            out.append(f"drops model `{name}`")
    for sect in ("combine", "calibrate"):
        a, b = parent.get(sect, {}), spec.get(sect, {})
        for k in sorted(set(a) | set(b)):
            if a.get(k) != b.get(k):
                out.append(f"`{sect}.{k}`: {a.get(k)} → {b.get(k)}")
    return "; ".join(out) or "no parameter change (re-run)"


def build(exp_dir: Path | None = None) -> Path:
    exp_dir = Path(exp_dir or C.EXPERIMENTS)
    recs = [json.loads(l) for l in (exp_dir / "ledger.jsonl").read_text().splitlines() if l.strip()]
    if not recs:
        raise SystemExit(f"empty ledger in {exp_dir}")
    by_id = {r["id"]: r for r in recs}
    champ_path = exp_dir / "champion.json"
    champ_id = json.loads(champ_path.read_text())["id"] if champ_path.exists() else \
        [r for r in recs if r["accepted"]][-1]["id"]
    first, champ = recs[0], by_id[champ_id]
    kept = [r for r in recs if r["accepted"]]
    rejected = [r for r in recs if not r["accepted"]]

    L = [f"# Research report: {exp_dir.name}", "",
         "_Written automatically from `ledger.jsonl` by `report.py`. Every number is the ledger's; nothing "
         "here is judged by a language model._", "",
         "## Summary", "",
         f"- {len(recs)} experiments: the starting point ({first['id']}), then {len(kept) - 1} kept and "
         f"{len(rejected)} rejected.",
         f"- Skill vs last value (pooled), DEV: {_f(first['dev'][METRIC])} at the start ({first['id']}) → "
         f"{_f(champ['dev'][METRIC])} for the champion ({champ_id}).",
         f"- HOLDOUT (never used to choose parameters, only as a gate): {_f(first['holdout'][METRIC])} → "
         f"{_f(champ['holdout'][METRIC])}.",
         f"- Champion interval coverage: DEV {champ['dev']['coverage_in']:.2f}, HOLDOUT "
         f"{champ['holdout']['coverage_in']:.2f} (target 0.80).",
         f"- Rule: keep a change only if DEV improves by at least {C.MIN_DEV_GAIN} and HOLDOUT does not fall "
         f"below the champion's.", ""]
    if (exp_dir / "progress.png").exists():
        L += ["![progress](progress.png)", ""]

    L += ["## All experiments", "",
          "| id | kept | DEV | HOLDOUT | coverage DEV | hypothesis |", "|---|---|---|---|---|---|"]
    for r in recs:
        h = r["hypothesis"].replace("|", "/").replace("\n", " ")
        h = h if len(h) <= 110 else h[:107] + "..."
        L.append(f"| {r['id']} | {'yes' if r['accepted'] else 'no'} | {_f(r['dev'][METRIC])} | "
                 f"{_f(r['holdout'][METRIC])} | {r['dev']['coverage_in']:.2f} | {h} |")
    L.append("")

    L += ["## The path, one experiment at a time", ""]
    for r in recs:
        parent = by_id.get(r.get("parent")) if r.get("parent") else None
        before = by_id.get(r.get("champion_before")) if r.get("champion_before") else None
        L += [f"### {r['id']}: {'kept' if r['accepted'] else 'rejected'}", "",
              f"**Hypothesis.** {r['hypothesis'].strip()}", "",
              f"**What changed.** {_diff(parent['spec'] if parent else None, r['spec'])}. "
              f"Model: {_models(r['spec'])}.", ""]
        if before:
            dd = r["dev"][METRIC] - before["dev"][METRIC]
            dh = r["holdout"][METRIC] - before["holdout"][METRIC]
            L.append(f"**Test.** Against champion {before['id']}: DEV {dd:+.4f}, HOLDOUT {dh:+.4f}. "
                     f"By horizon (DEV, 1/3/7 days): " +
                     " / ".join(_f(r["dev"]["by_horizon"].get(k)) for k in ("1", "3", "7")) + ".")
            L.append("")
        L += [f"**Decision.** {r.get('reason', '')}", ""]
        if r.get("lesson"):
            L += [f"**Lesson written to memory.** {r['lesson'].strip()}", ""]

    if rejected:
        L += ["## What the loop ruled out", ""]
        for r in rejected:
            L.append(f"- **{r['id']}**: {(r.get('lesson') or r.get('reason') or '').strip()}")
        L.append("")
    L += ["## Champion by horizon", "", "| horizon | DEV skill | HOLDOUT skill |", "|---|---|---|"]
    for k in ("1", "3", "7"):
        L.append(f"| {k} day | {_f(champ['dev']['by_horizon'].get(k))} | {_f(champ['holdout']['by_horizon'].get(k))} |")
    L += ["", f"Champion spec: `{exp_dir.name}/{champ_id}/spec.json`. Diagnosis: "
          f"`{exp_dir.name}/{champ_id}/diagnosis.md`.", ""]
    out = exp_dir / "REPORT.md"
    out.write_text("\n".join(L))
    return out


if __name__ == "__main__":
    print(build())
