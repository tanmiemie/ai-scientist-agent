import numpy as np
from data import log_changes
from .base import Model, from_log

class VolWeightedDriftModel(Model):
    name = "vol_weighted_drift"
    defaults = {
        "window": 60,
        "min_changes": 20,
        "vol_window": 10,
        "width": 1.0
    }

    def predict(self, ctx, horizons):
        hist = ctx.hist
        out = {}
        window = self.p["window"]
        min_changes = self.p["min_changes"]
        vol_window = self.p["vol_window"]
        width = self.p["width"]

        for h in horizons:
            ch = log_changes(hist, h, window)
            if len(ch) < min_changes:
                out[h] = None
                continue
            # Use last vol_window log changes to estimate recent volatility
            recent_ch = ch[-vol_window:] if len(ch) >= vol_window else ch
            std = np.std(recent_ch)
            # Basic drift assumption: mean is 0 under random walk, so q50 stays unchanged
            lo = -width * std * 1.28           # 10th percentile (for N(0,std^2))
            hi = width * std * 1.28            # 90th percentile
            mid = 0.0                          # median
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
