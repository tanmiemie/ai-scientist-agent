"""First prototype (iteration 0 finding): median = last value; lower edge = recent 0.1 quantile
of h-day changes; upper edge = recent 0.9 quantile, scaled by `k_up`, and at least `floor`
typical non-zero daily moves. Motivation: posted prices have been creeping up, and the
starter's drift left ~29% of truths above q90.
"""
import numpy as np

from data import log_changes
from .base import Model, from_log


class TrendTail(Model):
    name = "trend_tail"
    defaults = {"window": 60, "k_up": 1.0, "k_dn": 1.0, "floor": 1.0, "median_shift": 0.0}

    def predict(self, ctx, horizons):
        p = self.p
        ch1 = log_changes(ctx.hist, 1, p["window"])
        nz = np.abs(ch1[ch1 != 0])
        step = float(np.median(nz)) if len(nz) else 0.0
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            lo, hi = np.quantile(ch, [0.1, 0.9])
            mid = p["median_shift"] * ch.mean()
            up = max(max(hi, 0) * p["k_up"], p["floor"] * step)
            dn = min(lo, 0) * p["k_dn"]
            out[h] = from_log(ctx.last, dn, mid, max(up, mid))
        return out
