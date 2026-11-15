import numpy as np
from data import log_changes
from .base import Model, from_log

class TrendAwareEmpiricalModel(Model):
    name = "trend_aware_empirical"
    defaults = {"window": 30, "trend_weight": 1.0}

    def predict(self, ctx, horizons):
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, self.p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            # Calculate mean trend over window (if possible)
            trend = np.mean(ch) if len(ch) > 0 else 0.0
            # Shift quantiles by trend_weight * trend
            w = float(self.p["trend_weight"])
            lo += w * trend
            mid += w * trend
            hi += w * trend
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
