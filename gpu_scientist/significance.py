"""Are the gains real across series, not just in the pooled number?  python significance.py

Following Hewamalage, Ackermann & Bergmeir (2023), "Forecast evaluation for data scientists":
- pooled skill is dominated by expensive GPUs (B300 ~$10/h vs T4 ~$0.09/h), so we also compare
  scale-free, per-series numbers;
- differences against benchmarks get a statistical test: Wilcoxon signed-rank on the per-series
  log loss ratio (each series counts once, whatever its price).

Compares, on DEV and HOLDOUT origins together and separately: the champion (spec 07) against the
previous champion (spec 04), the starter drift (spec 00) and the last value (the skill baseline).
Writes significance.json.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

import config as C
import data
import evaluate
import online

SPECS = {"00_drift": "specs/00_drift.json", "04_momentum": "specs/04_momentum.json", "07_composition": "specs/07_composition.json"}


def per_series_loss(cells: pd.DataFrame) -> pd.DataFrame:
    c = cells[cells.status == "scored"]
    return c.groupby("series_id")[["loss", "baseline_loss"]].sum()


def compare(a: pd.Series, b: pd.Series) -> dict:
    """a, b: per-series total pinball loss. Negative log ratio = a is better."""
    j = pd.concat([a, b], axis=1, keys=["a", "b"]).dropna()
    j = j[(j.a > 0) & (j.b > 0)]
    r = np.log(j.a / j.b)
    nz = r[r != 0]
    p = float(wilcoxon(nz, alternative="less").pvalue) if len(nz) >= 6 else None
    return {"n_series": int(len(r)), "better": int((r < 0).sum()), "worse": int((r > 0).sum()), "ties": int((r == 0).sum()),
            "median_loss_ratio": round(float(np.exp(r.median())), 4), "geomean_loss_ratio": round(float(np.exp(r.mean())), 4),
            "wilcoxon_p_one_sided": None if p is None else round(p, 5)}


def main():
    sc, cc = data.build()
    panel = data.Panel.load(sc, cc)
    sids = panel.series_ids()
    origins = pd.date_range(C.WARMUP_START, C.HOLDOUT_ORIGINS[1])
    out = C.WORK / "significance"
    losses = {}
    for name, path in SPECS.items():
        fc, _, _ = online.run(json.load(open(C.ROOT / path)), panel, origins, sids, C.HORIZONS)
        for tag, win in (("dev", C.DEV_ORIGINS), ("holdout", C.HOLDOUT_ORIGINS)):
            evaluate.score(fc, win, out, f"{name}_{tag}", sc, cc)
            losses[(name, tag)] = per_series_loss(pd.read_csv(out / f"cells_{name}_{tag}.csv"))
    res = {}
    for tag in ("dev", "holdout", "both"):
        L = {n: (losses[(n, "dev")] + losses[(n, "holdout")]) if tag == "both" else losses[(n, tag)] for n in SPECS}
        ch = L["07_composition"]
        res[tag] = {"07 vs last value": compare(ch.loss, ch.baseline_loss),
                    "07 vs 00 drift": compare(ch.loss, L["00_drift"].loss),
                    "07 vs 04 momentum": compare(ch.loss, L["04_momentum"].loss),
                    "04 vs last value": compare(L["04_momentum"].loss, L["04_momentum"].baseline_loss)}
    (C.ROOT / "significance.json").write_text(json.dumps(res, indent=1))
    for tag, d in res.items():
        print(f"== {tag}")
        for k, v in d.items():
            print(f"  {k:20s} better {v['better']:2d} / worse {v['worse']:2d} / ties {v['ties']:2d}   median ratio {v['median_loss_ratio']}"
                  f"   geomean ratio {v['geomean_loss_ratio']}   Wilcoxon p {v['wilcoxon_p_one_sided']}")


if __name__ == "__main__":
    main()
