"""Walk-forward proof that the self-improvement is real.

Each slice pretends it is an earlier date. The autonomous loop (autoresearch.py) iterates using only
DEV and GATE origins up to that date. Then every champion it produced is scored on the TEST week right
after the gate, which no decision in that slice ever saw. If self-improvement is real, the champion
gets better on TEST as iterations go on, in every slice.

  python walkforward.py --proposer heuristic --iters 6
  python walkforward.py --proposer llm --provider openai --iters 6

Outputs walkforward/<run>/summary.md, summary.json and walkforward.png.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

import pandas as pd

import config as C
import data
import evaluate
import online

SLICES = [
    {"name": "S1", "dev": ("2026-09-15", "2026-09-30"), "gate": ("2026-10-01", "2026-10-09"), "test": ("2026-10-10", "2026-10-16")},
    {"name": "S2", "dev": ("2026-09-15", "2026-10-09"), "gate": ("2026-10-10", "2026-10-16"), "test": ("2026-10-17", "2026-10-23")},
    {"name": "S3", "dev": ("2026-09-15", "2026-10-16"), "gate": ("2026-10-17", "2026-10-23"), "test": ("2026-10-24", "2026-10-30")},
]


def champions_by_iteration(ledger_path):
    recs = [json.loads(l) for l in open(ledger_path) if l.strip()]
    out, cur = [], None
    for i, r in enumerate(recs):
        if r["accepted"]:
            cur = r
        out.append({"iteration": i, "exp": r["id"], "accepted": r["accepted"], "champion": cur["id"],
                    "spec": cur["spec"], "dev": cur["dev"][C.PRIMARY_METRIC], "gate": cur["holdout"][C.PRIMARY_METRIC],
                    "hypothesis": r["hypothesis"][:160], "lesson": r.get("lesson")})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=6)
    ap.add_argument("--proposer", default="heuristic", choices=["heuristic", "llm"])
    ap.add_argument("--provider", default="openai")
    ap.add_argument("--model", default=None)
    ap.add_argument("--seed", default=str(C.ROOT / "specs" / "00_drift.json"),
                    help="starting spec; default is the starter kit's drift so every improvement is found by the loop")
    ap.add_argument("--run", default=None)
    ap.add_argument("--no-memory", action="store_true", help="ablation: proposer sees no past lessons")
    ap.add_argument("--exa", action="store_true", help="outside evidence from Exa each iteration")
    ap.add_argument("--ideas", choices=["single", "batch"], default="single",
                    help="llm proposer: one idea per turn, or a scored batch of 5 (idea_batch.py)")
    a = ap.parse_args()

    run = a.run or f"{a.proposer}_{dt.datetime.now():%Y%m%d_%H%M}"
    base = C.ROOT / "walkforward" / run
    series_csv, catalog_csv = data.build()
    panel = data.Panel.load(series_csv, catalog_csv)
    sids = panel.series_ids()
    results = []
    for sl in SLICES:
        exp_dir = base / sl["name"] / "experiments"
        env = {**os.environ, "GPU_EXPERIMENTS": str(exp_dir), "GPU_DEV": ",".join(sl["dev"]),
               "GPU_HOLDOUT": ",".join(sl["gate"])}
        cmd = [sys.executable, "-B", "autoresearch.py", "--iters", str(a.iters), "--proposer", a.proposer,
               "--provider", a.provider, "--seed", a.seed, "--max-rejects", str(a.iters)]
        if a.model:
            cmd += ["--model", a.model]
        if a.no_memory:
            cmd += ["--no-memory"]
        if a.exa:
            cmd += ["--exa"]
        if a.ideas != "single":
            cmd += ["--ideas", a.ideas]
        print(f"\n### {sl['name']}: dev {sl['dev']} gate {sl['gate']} test {sl['test']}")
        subprocess.run(cmd, check=True, env=env, cwd=C.ROOT)
        cache = {}
        for row in champions_by_iteration(exp_dir / "ledger.jsonl"):
            if row["champion"] not in cache:
                fc, _, _ = online.run(row["spec"], panel, pd.date_range(C.WARMUP_START, sl["test"][1]), sids, C.HORIZONS)
                cache[row["champion"]] = evaluate.score(fc, sl["test"], base / sl["name"] / "test", row["champion"],
                                                        series_csv, catalog_csv)
            t = cache[row["champion"]]
            row.update(slice=sl["name"], test=t[C.PRIMARY_METRIC], test_geomean=t["skill_geomean"], test_coverage=t["coverage_in"])
            row.pop("spec")
            results.append(row)
            print(f"  iter {row['iteration']}  {row['exp']} {'ACC' if row['accepted'] else 'rej'}  champion {row['champion']}  "
                  f"dev {row['dev']:+.4f}  gate {row['gate']:+.4f}  TEST {row['test']:+.4f}  cov {row['test_coverage']:.2f}")

    df = pd.DataFrame(results)
    (base / "summary.json").write_text(json.dumps(results, indent=1, default=str))
    first = df.groupby("slice").first()
    last = df.groupby("slice").last()
    summ = pd.DataFrame({"seed TEST": first.test, "final TEST": last.test, "gain": last.test - first.test,
                         "final champion": last.champion, "iterations": df.groupby("slice").size()})
    md = [f"# Walk-forward check ({a.proposer}{', ' + a.ideas + ' ideas' if a.ideas != 'single' else ''}, {a.iters} iterations per slice, seed {os.path.basename(a.seed)})", "",
          "Every TEST week lies after all the data its slice's decisions used.", "", summ.round(4).to_markdown(), "",
          f"Mean TEST gain seed -> final champion: {summ.gain.mean():+.4f} ({(summ.gain > 0).sum()}/{len(summ)} slices improved)",
          "", "## Every iteration", "",
          df[["slice", "iteration", "exp", "accepted", "champion", "dev", "gate", "test", "test_coverage", "hypothesis"]]
          .round(4).to_markdown(index=False)]
    (base / "summary.md").write_text("\n".join(md))
    print("\n" + "\n".join(md[:7]))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for name, g in df.groupby("slice"):
        ax.plot(g.iteration, g.test, marker="o", label=f"{name}: test week {dict((s['name'], s['test'][0]) for s in SLICES)[name]}")
    ax.set_xlabel("iteration of the autonomous loop"); ax.set_ylabel(f"champion {C.PRIMARY_METRIC} on unseen TEST week")
    ax.set_title("Self-improvement measured on data no decision saw"); ax.axhline(0, color="#999", lw=0.8)
    ax.legend(frameon=False, fontsize=8); fig.tight_layout(); fig.savefig(base / "walkforward.png", dpi=150)
    print(base / "walkforward.png")


if __name__ == "__main__":
    main()
