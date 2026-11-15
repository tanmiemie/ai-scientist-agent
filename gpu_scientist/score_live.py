"""Score the frozen Sunday forecast once newer data exists, and record it immutably.

  python score_live.py --new-pack /path/to/a/newer/gpu-price-pack

1. Checks that submission_final/forecast_2026-11-06.csv still has the sha256 recorded in
   submission_final/MANIFEST.json (the forecast must not have changed since it was made).
2. Builds the series from the newer pack (truth) with the starter kit.
3. Scores with the starter kit's scorer.py in --frozen-cutoff mode: history = the original pack cut at
   the cutoff, truth = the newer pack, so only days after the cutoff count.
4. Appends one line to experiments_final/live_ledger.jsonl: forecast hash, truth fingerprint, scores.
   Every live forecast is scored, misses included; nothing is overwritten.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import config as C
import data
import evaluate
import provenance


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new-pack", required=True, help="a newer gpu-price-pack folder with data after the cutoff")
    a = ap.parse_args()

    sub = C.ROOT / "submission_final" / f"forecast_{C.CUTOFF}.csv"
    man = json.loads((C.ROOT / "submission_final" / "MANIFEST.json").read_text())
    got = provenance.sha256(sub)
    if got != man["forecast_sha256"]:
        sys.exit(f"submission changed since it was frozen: {got} != {man['forecast_sha256']}")

    hist_csv, cat_csv = data.build(cutoff=C.CUTOFF)
    live = C.WORK / "live"
    live.mkdir(parents=True, exist_ok=True)
    truth_csv = live / "series_daily_truth.csv"
    subprocess.run([sys.executable, "-B", str(C.STARTER / "build_series.py"), "--pack", str(Path(a.new_pack).resolve()),
                    "--no-aws", "--out", str(truth_csv), "--catalog", str(live / "series_catalog_truth.csv"),
                    "--report", str(live / "build_truth.json")], check=True)
    rep = live / "report_live.json"
    subprocess.run([sys.executable, "-B", str(C.STARTER / "scorer.py"), "--forecast", str(sub), "--truth", str(truth_csv),
                    "--history", str(hist_csv), "--catalog", str(cat_csv), "--tier", C.TIER, "--frozen-cutoff", C.CUTOFF,
                    "--horizons", ",".join(map(str, C.HORIZONS)), "--out", str(rep), "--per-cell", str(live / "cells_live.csv")],
                   check=True)
    r = json.loads(rep.read_text())
    o = r["overall"]
    rec = {"forecast": sub.name, "forecast_sha256": got, "champion": man["champion"],
           "truth_pack": str(Path(a.new_pack).name), "truth_series_sha256": provenance.sha256(truth_csv),
           "scored_utc": provenance.record(truth_csv)["created_utc"], "cells_scored": o.get("n_cells"),
           "summary": evaluate.summarize(r) if o.get("n_cells") else None}
    with open(C.ROOT / "experiments_final" / "live_ledger.jsonl", "a") as f:
        f.write(json.dumps(rec, default=str) + "\n")
    print(json.dumps(rec, indent=1, default=str))


if __name__ == "__main__":
    main()
