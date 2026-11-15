"""Write the Sunday submission with the current champion.

  python submit.py [--scope headline|all] [--spec specs/x.json]

Uses the history truncated at the cutoff (built by the starter kit with --cutoff), runs the
champion's walk-forward loop up to the cutoff so its weights and calibration have learned from
every realised error, and keeps only the rows with origin_date = cutoff.
"""
from __future__ import annotations

import argparse
import json
import sys

import pandas as pd

import config as C
import data
import online


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", default="headline", choices=["headline", "all"])
    ap.add_argument("--spec", default=None, help="default: experiments/champion.json")
    ap.add_argument("--team-id", default="")
    a = ap.parse_args()

    if a.spec:
        spec, src = json.loads(open(a.spec).read()), a.spec
    else:
        champ = json.loads((C.EXPERIMENTS / "champion.json").read_text())
        spec, src = champ["spec"], champ["id"]

    series_csv, catalog_csv = data.build(cutoff=C.CUTOFF)
    panel = data.Panel.load(series_csv, catalog_csv)
    assert panel.raw.date.max() <= pd.Timestamp(C.CUTOFF), "history holds a row after the cutoff"
    sids = panel.series_ids(None if a.scope == "all" else C.TIER)
    if a.scope == "all":   # only series that are still being collected
        sids = [s for s in sids if panel.daily[s].index.max() >= pd.Timestamp(C.CUTOFF) - pd.Timedelta(days=3)]

    fc, _, state = online.run(spec, panel, pd.date_range(C.WARMUP_START, C.CUTOFF), sids, C.HORIZONS)
    fc = fc[fc.origin_date == C.CUTOFF].copy()
    fc["team_id"] = a.team_id
    fc["method_note"] = f"gpu_scientist champion {src}"

    sys.path.insert(0, str(C.STARTER))
    from _common import validate_forecast  # the scorer's own validation
    valid, problems = validate_forecast(fc, list(C.HORIZONS))
    if problems:
        print(f"[warn] {len(problems)} invalid rows: {problems[:5]}")

    C.SUBMISSION.mkdir(parents=True, exist_ok=True)
    path = C.SUBMISSION / f"forecast_{C.CUTOFF}.csv"
    cols = ["series_id", "origin_date", "horizon_days", "q10", "q50", "q90", "target_date", "team_id", "method_note"]
    valid = fc.loc[fc.index.isin(valid.index), cols] if "_row" in valid.columns else valid[cols]
    valid.to_csv(path, index=False)
    (C.SUBMISSION / "submission_state.json").write_text(json.dumps({"spec_from": src, "spec": spec, "state": state}, indent=1))
    print(f"wrote {path}: {len(valid)} rows, {valid.series_id.nunique()} series, origin {C.CUTOFF}, spec from {src}")


if __name__ == "__main__":
    main()
