"""Uncertainty of the headline numbers: cluster bootstrap over series and over origin days.

    python uncertainty.py        # writes uncertainty.json

Skill = 1 - sum(pinball loss) / sum(last-value pinball loss), pooled as in the official scorer.
Resampling whole series (or whole origin days) keeps each cluster's correlated cells together, so the
intervals reflect how much the result depends on which series and which days happened to be scored."""
import json

import numpy as np
import pandas as pd

import config as C

B = 2000
RNG = np.random.default_rng(20261115)
EXP = C.ROOT / "experiments_final"


def cells(eid, part):
    d = pd.read_csv(EXP / eid / f"cells_{part}.csv")
    return d[d.status == "scored"]


def skill(d):
    return 1 - d.loss.sum() / d.baseline_loss.sum()


def boot(d, by, other=None):
    """Percentile CI of pooled skill (or of the skill difference vs `other`) resampling clusters `by`."""
    keys = d[by].unique()
    g = d.groupby(by)[["loss", "baseline_loss"]].sum()
    go = other.groupby(by)[["loss"]].sum().reindex(g.index) if other is not None else None
    out = []
    for _ in range(B):
        k = RNG.choice(len(keys), len(keys), replace=True)
        s = g.iloc[k].sum()
        v = 1 - s.loss / s.baseline_loss
        if go is not None:
            v -= 1 - go.iloc[k].loss.sum() / s.baseline_loss
        out.append(v)
    return [round(float(np.percentile(out, 2.5)), 3), round(float(np.percentile(out, 97.5)), 3)]


res = {}
for part in ("dev", "holdout"):
    ch, dr = cells("exp_007", part), cells("exp_000", part)
    r = {"champion_skill": round(skill(ch), 3),
         "ci95_by_series": boot(ch, "series_id"), "ci95_by_origin_day": boot(ch, "origin_date"),
         "gain_vs_drift": round(skill(ch) - skill(dr), 3),
         "gain_vs_drift_ci95_by_series": boot(ch, "series_id", dr),
         "by_horizon": {}}
    for h, dh in ch.groupby("horizon_days"):
        r["by_horizon"][int(h)] = {"skill": round(skill(dh), 3), "ci95_by_series": boot(dh, "series_id"),
                                   "coverage": round(float(((dh.y >= dh.q10) & (dh.y <= dh.q90)).mean()), 3)}
    r["n_cells"], r["n_series"] = int(len(ch)), int(ch.series_id.nunique())
    res[part] = r
json.dump(res, open(C.ROOT / "uncertainty.json", "w"), indent=1)
print(json.dumps(res, indent=1))
