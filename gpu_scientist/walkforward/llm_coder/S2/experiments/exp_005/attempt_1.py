import numpy as np
from data import log_changes
from .base import Model, from_log

class VolWeightedDriftFloorModel(Model):
    name = "vol_weighted_drift_floor"
    defaults = {"window": 60, "min_changes": 20, "vol_window": 30, "width": 1.0, "min_vol": 0.01}

    def predict(self, ctx, horizons):
        out = {}
        x = ctx.hist
        last = ctx.last
        log_x = np.log(x)
        
        # Compute realized volatility (stddev) over vol_window days, in log space
        recent = log_x[-self.p["vol_window"]:]
        log_ch = np.diff(recent)
        if len(log_ch) < 2:
            vol = self.p["min_vol"]
        else:
            vol = max(np.std(log_ch, ddof=1), self.p["min_vol"])
        
        # Empirical drift model for median
        all_log_ch = log_changes(x, 1, self.p["window"])
        if len(all_log_ch) < self.p["min_changes"]:
            med = 0.0 # fallback to flat
        else:
            med = np.median(all_log_ch)
        
        # Predictive interval width
        width = self.p["width"] * vol
        for h in horizons:
            # Scale by sqrt(h): random walk
            lo = med * h - width * np.sqrt(h) # drift minus volatility
            mid = med * h                    # drift only
            hi = med * h + width * np.sqrt(h)
            out[h] = from_log(last, lo, mid, hi)
        return out
