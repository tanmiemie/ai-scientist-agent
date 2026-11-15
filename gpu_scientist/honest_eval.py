"""Hindsight-free check: score on the series that could have been chosen before HOLDOUT.

The 37 scored series were selected with data up to 2026-11-06. Here the headline set is rebuilt with
data up to 2026-10-15 (the day before HOLDOUT) and HOLDOUT is scored on that set only; then HOLDOUT on
the full set is split by collector.   python honest_eval.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

import config as C
import data
import evaluate
import online

SPECS = ["00_drift", "01_trend_tail", "02_trend_tail_cal", "04_momentum", "07_composition"]


def main():
    sc, cc = data.build()
    data.build(cutoff="2026-10-15")
    cat_oct = C.WORK / "series_catalog_cut2026-10-15.csv"
    panel = data.Panel.load(sc, cc)
    early = sorted(pd.read_csv(cat_oct).query("tier == 'headline'").series_id)
    out, origins, res = C.WORK / "honest", pd.date_range(C.WARMUP_START, C.HOLDOUT_ORIGINS[1]), {"early_set": {}, "by_collector": []}
    per = {}
    for f in SPECS:
        spec = json.load(open(C.ROOT / "specs" / f"{f}.json"))
        fc, _, _ = online.run(spec, panel, origins, panel.series_ids(), C.HORIZONS)
        m = evaluate.score(fc[fc.series_id.isin(early)], C.HOLDOUT_ORIGINS, out, f"early_{f}", sc, cat_oct)
        res["early_set"][f] = {k: m[k] for k in ("skill_pooled", "skill_median_of_series", "skill_geomean", "coverage_in")}
        cells = pd.read_csv(out / f"cells_early_{f}.csv").query("status == 'scored'")
        per[f] = cells.groupby("series_id")[["loss", "baseline_loss"]].sum()
        evaluate.score(fc, C.HOLDOUT_ORIGINS, out, f"full_{f}", sc, cc)
        c = pd.read_csv(out / f"cells_full_{f}.csv").query("status == 'scored'")
        for src, g in c.groupby(c.series_id.str.split(".").str[0]):
            res["by_collector"].append({"spec": f, "collector": src, "pooled": round(1 - g.loss.sum() / g.baseline_loss.sum(), 4)})

    def test(a, b):
        r = np.log(a / b)
        r = r[np.isfinite(r)]
        return {"better": int((r < 0).sum()), "n": int(len(r)), "p": round(float(wilcoxon(r[r != 0], alternative="less").pvalue), 4)}
    ch = per["07_composition"]
    res["early_set_tests"] = {"07 vs last value": test(ch.loss, ch.baseline_loss), "07 vs drift": test(ch.loss, per["00_drift"].loss),
                              "07 vs 01": test(ch.loss, per["01_trend_tail"].loss)}
    res["early_set_size"] = len(early)
    (C.ROOT / "honest_eval.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
