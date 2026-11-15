import numpy as np
from data import log_changes
from .base import Model, from_log

class LogEmpiricalWideWindowModel(Model):
    name = "log_empirical_wide_window"
    defaults = {"window": 60}

    def predict(self, ctx, horizons):
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, self.p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            # Estimate q05, q50, q95
            lo_wide, mid, hi_wide = np.quantile(ch, [0.05, 0.5, 0.95])
            # Contract q05–q95 range linearly to q10–q90 (assume normality for scale)
            # For normal: (q90 - median)/(q95 - median) = (0.90 - 0.5)/(0.95 - 0.5) = 0.4/0.45 = 8/9
            shrink = 0.8
            lo = mid + shrink * (lo_wide - mid)
            hi = mid + shrink * (hi_wide - mid)
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
