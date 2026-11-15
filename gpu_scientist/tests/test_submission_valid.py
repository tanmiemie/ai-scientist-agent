"""The Sunday submission passes the starter scorer in frozen-cutoff mode with no validation problems."""
import json
import subprocess
import sys

import pandas as pd

import config as C
import data

SUB = C.ROOT / "submission_final" / f"forecast_{C.CUTOFF}.csv"


def test_submission_valid(built, tmp_path):
    series_csv, catalog_csv = built
    hist_csv, hist_cat = data.build(cutoff=C.CUTOFF)
    sub = pd.read_csv(SUB)
    assert len(sub) == 111
    assert sub.series_id.nunique() == 37 and set(sub.horizon_days) == set(C.HORIZONS)
    assert (sub.origin_date == C.CUTOFF).all()
    assert ((sub.q10 <= sub.q50) & (sub.q50 <= sub.q90)).all()
    out = tmp_path / "report.json"
    r = subprocess.run([sys.executable, "-B", str(C.STARTER / "scorer.py"), "--forecast", str(SUB),
                        "--truth", str(series_csv), "--history", str(hist_csv), "--catalog", str(hist_cat),
                        "--tier", C.TIER, "--horizons", ",".join(map(str, C.HORIZONS)),
                        "--frozen-cutoff", C.CUTOFF, "--out", str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    rep = json.loads(out.read_text())
    assert rep["mode"] == "frozen_cutoff"
    assert rep["forecast_validation"]["n_problems"] == 0, rep["forecast_validation"]
