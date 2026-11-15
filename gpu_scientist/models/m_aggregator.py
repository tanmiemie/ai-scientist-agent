"""composition (exp_007) plus a nudge towards the GetDeploying weekly median of the same GPU.

Hypothesis (DEVIN_NEXT.md task A): when the aggregator's latest weekly median for the same GPU and pricing
mode sits above our series' last value, our series tends to move up within 7 days, and vice versa.

aggregator_medians.csv is a different instrument (aggregator_median); it is never chained with our series,
only used as a signal. Matching: same GPU (GetDeploying has one line per GPU family, e.g. all H100
variants -> NVIDIA H100) and pricing mode = our pricing_tier. A Monday-dated week is the median of that
week's daily captures and stays provisional until Sunday, so it is used from week_start + 7 + lag days on.
The CSV is read once and cached; every lookup is cut at the origin.
apply="all" shifts all three quantiles by beta_agg * clip(signal, +-cap); apply="tail" moves only the
interval edge on the signal's side. Signals: "gap" = log(aggregator / last value); "dgap" = gap minus
its median over the previous norm_days (removes the persistent level difference between collectors).
"""
from functools import lru_cache

import numpy as np
import pandas as pd

import config as C
from .base import from_log
from .m_composition import Composition

AGG_GPU = {"A100 40GB": "NVIDIA A100", "A100 80GB": "NVIDIA A100", "A100 SXM 80GB": "NVIDIA A100",
           "H100 80GB": "NVIDIA H100", "H100 PCIe 80GB": "NVIDIA H100", "H100 SXM 80GB": "NVIDIA H100",
           "RTX A6000": "NVIDIA A6000"}
AGG_MODES = {"on_demand", "spot"}


def agg_key(meta: dict):
    """(GetDeploying gpu_model, pricing_mode) for a catalog row, or None if it cannot be matched."""
    mode = meta.get("pricing_tier")
    gpu = meta.get("gpu_model")
    if mode not in AGG_MODES or not isinstance(gpu, str):
        return None
    name = AGG_GPU.get(gpu, f"NVIDIA {gpu}")
    return (name, mode) if (name, mode) in _table().index else None


@lru_cache(maxsize=1)
def _table() -> pd.DataFrame:
    a = pd.read_csv(C.PACK / "aggregator_medians.csv", parse_dates=["week_start"])
    a = a[a.pricing_mode.isin(AGG_MODES)]
    return a.set_index(["gpu_model", "pricing_mode"]).sort_index()


@lru_cache(maxsize=None)
def agg_series(gpu: str, mode: str, col: str = "median_usd_per_gpu_hour", lag: int = 0) -> pd.Series:
    """Weekly values indexed by the first day they may be used (week_start + 7 + lag days, lag >= 0)."""
    g = _table().loc[(gpu, mode)].sort_values("week_start")
    s = g.set_index(g.week_start + pd.Timedelta(days=7 + max(int(lag), 0)))[col].dropna()
    return s[s > 0]


class Aggregator(Composition):
    name = "aggregator"
    defaults = {**Composition.defaults, "signal": "gap", "beta_agg": 0.1, "cap": 0.2, "lag": 0,
                "col": "median_usd_per_gpu_hour", "norm_days": 56, "apply": "all", "min_gap": 0.0}

    def _signal(self, ctx):
        key = agg_key(ctx.meta)
        if key is None:
            return 0.0
        a = agg_series(*key, col=self.p["col"], lag=self.p["lag"]).loc[:ctx.origin]
        if not len(a):
            return 0.0
        gap = float(np.log(a.iloc[-1] / ctx.last))
        if self.p["signal"] == "gap":
            return gap
        days = pd.date_range(ctx.origin - pd.Timedelta(days=self.p["norm_days"]), ctx.origin - pd.Timedelta(days=1))
        hist = ctx.hist.reindex(days).dropna()
        av = a.reindex(days, method="ffill").reindex(hist.index).dropna()
        if len(av) < self.p["norm_days"] // 2:
            return 0.0
        return gap - float(np.median(np.log(av / hist.loc[av.index])))

    def predict(self, ctx, horizons):
        out = super().predict(ctx, horizons)
        g = self._signal(ctx)
        if abs(g) <= self.p["min_gap"]:
            return out
        s = self.p["beta_agg"] * float(np.clip(g, -self.p["cap"], self.p["cap"]))
        if s == 0.0:
            return out
        for h, q in out.items():
            if q is None:
                continue
            lo, mid, hi = (np.log(x / ctx.last) for x in q)
            if self.p["apply"] == "all":           # shift the whole forecast
                lo, mid, hi = lo + s, mid + s, hi + s
            elif s > 0:                            # "tail": only the edge on the signal's side moves out
                hi += s
            else:
                lo += s
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
