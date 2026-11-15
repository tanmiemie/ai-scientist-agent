import numpy as np
from data import log_changes
from .base import Model, from_log

class LogEmpiricalScaledWindowModel(Model):
    name = "log_empirical_scaled_window"
    defaults = {"window": 60, "scale": 1.0}

    def predict(self, ctx, horizons):
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, self.p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            s = self.p["scale"]
            # Move lo, hi farther from mid by the scale factor
            mid_orig = mid
            lo = mid_orig + (lo - mid_orig)*s
            hi = mid_orig + (hi - mid_orig)*s
            out[h] = from_log(ctx.last, lo, mid_orig, hi)
        return out