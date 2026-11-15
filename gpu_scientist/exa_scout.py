"""Exa scout: outside evidence for the research loop (Exa challenge + Track 2 direction B).

Each iteration of autoresearch.py (with --exa) asks Exa two questions built from the champion's
diagnosis, before the proposer writes its hypothesis:

  method  how others forecast or calibrate intervals for the problem the diagnosis shows
          (e.g. truths above q90 too often), so the proposer can borrow a method;
  market  what was published about GPU rental prices, supply and demand up to the data cutoff
          of this run (direction B: market signals), so hypotheses can use market context.

No look-ahead: market results must carry a publication date on or before the run's cutoff
(the last gate origin), and the request itself asks Exa only for pages published by then.
Everything found is kept in <experiments>/evidence.jsonl, a dated evidence memory: later
iterations see what earlier ones found (deduplicated by URL), so the loop builds up a picture of
the market instead of starting from zero each time. The key comes from EXA_API_KEY only.

    EXA_API_KEY=... python exa_scout.py --dry-run     # print the queries this ledger would send
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.request

import config as C

EXA_URL = "https://api.exa.ai/search"
N_RESULTS = 5
MEMORY_IN_PROMPT = 12


def cutoff_date() -> str:
    """Last date whose information a decision in this run may use: the end of the gate window."""
    return str(C.HOLDOUT_ORIGINS[1])[:10]


def _post(body: dict) -> dict:
    key = os.environ.get("EXA_API_KEY")
    if not key:
        raise RuntimeError("set EXA_API_KEY in the environment (never paste keys into chat or code)")
    req = urllib.request.Request(EXA_URL, json.dumps(body).encode(),
                                 {"x-api-key": key, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def search(query: str, end_date: str | None, require_date: bool, n: int = N_RESULTS) -> list[dict]:
    body = {"query": query, "type": "auto", "numResults": n, "contents": {"highlights": True}}
    if end_date:
        body["endPublishedDate"] = f"{end_date}T23:59:59.999Z"
    out = []
    for r in _post(body).get("results", []):
        pub = (r.get("publishedDate") or "")[:10]
        if end_date and pub and pub > end_date:
            continue                      # belt and braces: never use a page dated after the cutoff
        if require_date and not pub:
            continue                      # undated market news cannot be placed in time
        hl = r.get("highlights") or []
        out.append({"title": (r.get("title") or "")[:200], "url": r.get("url"), "published": pub or None,
                    "highlights": [h[:400] for h in hl[:3]]})
    return out


def queries(ctx: dict) -> dict:
    """Two queries from the champion's DEV diagnosis (the numbers the proposer also sees)."""
    d = ctx["champion"]["dev"]
    above, below, cov = d["coverage_above_q90"], d["coverage_below_q10"], d["coverage_in"]
    if above > 0.12 and above >= below:
        issue = "prices rising above the upper forecast quantile more often than expected"
    elif below > 0.12:
        issue = "prices falling below the lower forecast quantile more often than expected"
    elif cov > 0.85:
        issue = "prediction intervals that are too wide"
    else:
        issue = "small improvements to quantile forecasts of sticky, step-like posted prices"
    month = dt.date.fromisoformat(cutoff_date()).strftime("%B %Y")
    return {
        "method": f"forecasting method for {issue}: quantile forecasts of posted prices that change in "
                  f"steps, online conformal or adaptive interval calibration, pinball loss",
        "market": f"H100 A100 H200 B200 cloud GPU rental prices news {month}: price changes, supply, "
                  f"demand, new capacity, neocloud pricing",
    }


def _memory_path():
    return C.EXPERIMENTS / "evidence.jsonl"


def load_memory(end_date: str | None = None) -> list[dict]:
    p = _memory_path()
    if not p.exists():
        return []
    rows = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    if end_date:
        rows = [r for r in rows if r["kind"] == "method" or (r.get("published") or "9999") <= end_date]
    return rows


def remember(rows: list[dict]) -> int:
    seen = {r["url"] for r in load_memory()}
    new = [r for r in rows if r["url"] not in seen]
    if new:
        C.EXPERIMENTS.mkdir(parents=True, exist_ok=True)
        with open(_memory_path(), "a") as f:
            for r in new:
                f.write(json.dumps(r) + "\n")
    return len(new)


def scout(ctx: dict, iteration: int) -> dict:
    """Run both queries, store new evidence, return what the proposer should see this turn."""
    end = cutoff_date()
    qs = queries(ctx)
    found, errors = [], []
    for kind, q in qs.items():
        try:
            res = search(q, end_date=end, require_date=(kind == "market"))
        except Exception as e:                       # Exa down must not stop the research loop
            errors.append(f"{kind}: {e}")
            continue
        now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        found += [{**r, "kind": kind, "query": q, "iteration": iteration, "retrieved_utc": now} for r in res]
    n_new = remember(found)
    memory = load_memory(end)
    return {"cutoff": end, "queries": qs, "found_this_turn": found, "new_in_memory": n_new,
            "errors": errors,
            "memory_for_prompt": [{k: r.get(k) for k in ("kind", "title", "url", "published", "highlights")}
                                  for r in memory[-MEMORY_IN_PROMPT:]]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the queries for the current champion")
    a = ap.parse_args()
    champ = json.loads((C.EXPERIMENTS / "champion.json").read_text())
    ctx = {"champion": {"dev": champ["dev"]}}
    if a.dry_run:
        print(json.dumps({"cutoff": cutoff_date(), "queries": queries(ctx)}, indent=1))
    else:
        print(json.dumps(scout(ctx, iteration=0), indent=1))
