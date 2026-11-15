"""Scores forecasts with the starter kit's own scorer.py (the same code that scores Sunday)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

import config as C


def score(forecast: pd.DataFrame, window: tuple, out_dir: Path, tag: str, series_csv, catalog_csv) -> dict:
    """Score the rows whose origin is inside `window` (inclusive). Returns the headline numbers."""
    out_dir.mkdir(parents=True, exist_ok=True)
    f = forecast[(forecast.origin_date >= window[0]) & (forecast.origin_date <= window[1])]
    fpath, rpath, cpath = out_dir / f"forecast_{tag}.csv", out_dir / f"report_{tag}.json", out_dir / f"cells_{tag}.csv"
    f.to_csv(fpath, index=False)
    cmd = [sys.executable, "-B", str(C.STARTER / "scorer.py"), "--forecast", str(fpath), "--truth", str(series_csv),
           "--history", str(series_csv), "--catalog", str(catalog_csv), "--tier", C.TIER,
           "--horizons", ",".join(map(str, C.HORIZONS)), "--out", str(rpath), "--per-cell", str(cpath)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    return summarize(json.loads(rpath.read_text()))


def summarize(r: dict) -> dict:
    o = r["overall"]
    return {
        "skill_pooled": o["skill_pooled"],
        "skill_median_of_series": o["skill_median_of_series"],
        "skill_geomean": o["skill_geomean"],
        "coverage_in": o["coverage"]["within_q10_q90"],
        "coverage_above_q90": o["coverage"]["above_q90"],
        "coverage_below_q10": o["coverage"]["below_q10"],
        "share_series_positive": o.get("share_series_positive_skill"),
        "by_horizon": {h: v["skill_pooled"] for h, v in r["by_horizon"].items()},
        "n_cells": o["n_cells"],
        "n_problems": r["forecast_validation"]["n_problems"],
    }
