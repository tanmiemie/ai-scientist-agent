"""Run one experiment = one hypothesis, end to end, and decide whether it is accepted.

  python run_experiment.py --spec specs/my_idea.json --hypothesis "why I expect this to help" [--parent exp_003]

Steps: walk-forward pipeline over all origins -> official scorer on DEV and HOLDOUT ->
diagnosis on DEV -> compare with the champion -> append to experiments/ledger.jsonl.
Accepted if: DEV primary metric >= champion + MIN_DEV_GAIN  and  HOLDOUT >= champion - HOLDOUT_TOLERANCE.
The first experiment (no champion yet) is accepted as the starting point.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json

import pandas as pd

import config as C
import data
import diagnose
import evaluate
import online
import provenance


def next_id() -> str:
    C.EXPERIMENTS.mkdir(parents=True, exist_ok=True)
    n = len(list(C.EXPERIMENTS.glob("exp_*")))
    return f"exp_{n:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--hypothesis", required=True, help="what you expect and why (from the diagnosis)")
    ap.add_argument("--parent", default=None, help="experiment this one builds on")
    ap.add_argument("--id", default=None)
    a = ap.parse_args()
    run(json.loads(open(a.spec).read()), a.hypothesis, a.parent, a.id)


def run(spec: dict, hypothesis: str, parent: str | None = None, eid: str | None = None, verbose: bool = True) -> dict:
    """Run one experiment end to end and return its ledger record (also used by autoresearch.py)."""
    a = argparse.Namespace(hypothesis=hypothesis, parent=parent)
    eid = eid or next_id()
    out = C.EXPERIMENTS / eid
    out.mkdir(parents=True, exist_ok=True)
    (out / "spec.json").write_text(json.dumps(spec, indent=1))

    series_csv, catalog_csv = data.build()
    panel = data.Panel.load(series_csv, catalog_csv)
    sids = panel.series_ids()
    origins = pd.date_range(C.WARMUP_START, C.HOLDOUT_ORIGINS[1])

    t0 = dt.datetime.now()
    fc, per_model, state = online.run(spec, panel, origins, sids, C.HORIZONS)
    fc.to_csv(out / "forecast_all.csv", index=False)
    prov = provenance.record(series_csv, out / "forecast_all.csv")
    provenance.archive(out / "forecast_all.csv")   # immutable, committed copy of every forecast
    per_model.to_csv(out / "per_model.csv.gz", index=False)
    (out / "state.json").write_text(json.dumps(state, indent=1))

    dev = evaluate.score(fc, C.DEV_ORIGINS, out, "dev", series_csv, catalog_csv)
    hold = evaluate.score(fc, C.HOLDOUT_ORIGINS, out, "holdout", series_csv, catalog_csv)
    diag, md = diagnose.run(out / "cells_dev.csv", per_model, panel, C.DEV_ORIGINS)
    diagnose.save(diag, md, out)

    champ_path = C.EXPERIMENTS / "champion.json"
    champ = json.loads(champ_path.read_text()) if champ_path.exists() else None
    k = C.PRIMARY_METRIC
    if champ is None:
        accepted, reason = True, "first experiment: becomes the starting champion"
    else:
        dgain = dev[k] - champ["dev"][k]
        hgain = hold[k] - champ["holdout"][k]
        accepted = dgain >= C.MIN_DEV_GAIN and hgain >= -C.HOLDOUT_TOLERANCE
        reason = (f"dev {k} {dgain:+.4f} vs champion {champ['id']} (need >= +{C.MIN_DEV_GAIN}); "
                  f"holdout {hgain:+.4f} (need >= -{C.HOLDOUT_TOLERANCE})")

    rec = {"id": eid, "time_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "parent": a.parent,
           "hypothesis": a.hypothesis, "spec": spec, "dev": dev, "holdout": hold,
           "champion_before": champ["id"] if champ else None, "accepted": accepted, "reason": reason,
           "lesson": None, "provenance": prov, "runtime_s": round((dt.datetime.now() - t0).total_seconds(), 1)}
    with open(C.EXPERIMENTS / "ledger.jsonl", "a") as f:
        f.write(json.dumps(rec, default=str) + "\n")
    if accepted:
        champ_path.write_text(json.dumps({"id": eid, "spec": spec, "dev": dev, "holdout": hold}, indent=1))

    if not verbose:
        return rec

    def line(name, m):
        return (f"{name:8s} pooled {m['skill_pooled']:+.4f}  median {m['skill_median_of_series']:+.4f}  "
                f"geomean {m['skill_geomean']:+.4f}  in[q10,q90] {m['coverage_in']:.2f}  above_q90 {m['coverage_above_q90']:.2f}")
    print(f"\n== {eid}: {'ACCEPTED' if accepted else 'rejected'} ({reason})")
    print(line("dev", dev))
    print(line("holdout", hold))
    print(f"diagnosis: {out / 'diagnosis.md'}")
    print(f"next: python ledger.py lesson {eid} \"what this taught us\"")
    return rec


if __name__ == "__main__":
    main()
