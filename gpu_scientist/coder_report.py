"""Count how many LLM-written models passed each coder gate, and which were accepted (DEVIN_NEXT task E).

    python coder_report.py walkforward/llm_coder      # writes CODER_REPORT.md there
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GATES = ("static", "smoke", "lookahead")


def rows(run: Path):
    for log in sorted(run.glob("*/experiments/autoresearch_log.jsonl")):
        sl = log.parent.parent.name
        for i, line in enumerate(log.read_text().splitlines()):
            r = json.loads(line)
            for g in r.get("gates") or []:
                yield {"slice": sl, "iteration": r.get("iteration") or i + 1, "exp": r.get("id"), **g,
                       "ran": g is (r.get("gates") or [None])[-1] and r.get("id") is not None and not g["failed"],
                       "accepted": bool(r.get("accepted")) and g is r["gates"][-1] and not g["failed"],
                       "run_error": r.get("run_error") if g is r["gates"][-1] else None}


def build(run: Path) -> str:
    rs = list(rows(run))
    n = len(rs)
    md = [f"# LLM-written models: gate results ({run.name})", "",
          f"{n} generated models (attempts, including fixes after a failed gate).", "",
          "| gate | passed | failed here |", "|---|---|---|"]
    for g in GATES:
        md.append(f"| {g} | {sum(g in r['passed'] for r in rs)} | {sum(r['failed'] == g for r in rs)} |")
    md.append(f"| spec check after the gates | {sum(not r['failed'] for r in rs)} | {sum(r['failed'] == 'spec' for r in rs)} |")
    ran = [r for r in rs if r["ran"]]
    md += ["", f"Ran on DEV and met the HOLDOUT gate: {len(ran)}; sandboxed run failed: "
           f"{sum(bool(r['run_error']) for r in rs)}; accepted: {sum(r['accepted'] for r in rs)}.", "",
           "| slice | iter | attempt | model | passed | failed | experiment | accepted |", "|---|---|---|---|---|---|---|---|"]
    for r in rs:
        md.append(f"| {r['slice']} | {r['iteration']} | {r['attempt']} | `{r['name']}` | {', '.join(r['passed']) or '-'} | "
                  f"{r['failed'] or '-'} | {r['exp'] if r['ran'] else '-'} | {'yes' if r['accepted'] else ('no' if r['ran'] else '-')} |")
    fails = [r for r in rs if r["failed"]]
    if fails:
        md += ["", "## Gate failures (last 300 characters of the error fed back)", ""]
        for r in fails:
            err = (r.get("error") or "").strip().replace("```", "'''")[-300:]
            md += [f"- {r['slice']} iter {r['iteration']} attempt {r['attempt']} `{r['name']}`, {r['failed']}:",
                   "  ```", *["  " + x for x in err.splitlines()], "  ```"]
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    run = Path(sys.argv[1])
    out = build(run)
    (run / "CODER_REPORT.md").write_text(out)
    print(out)
