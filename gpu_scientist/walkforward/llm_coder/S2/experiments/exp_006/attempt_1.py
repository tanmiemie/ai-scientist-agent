import numpy as np
from data import log_changes
from .base import Model, from_log

class VolWeightedDriftFloorModel(Model):
    name = "vol_weighted_drift_floor"
    defaults = {"window": 60, "min_changes": 20, "vol_window": 30, "width": 1.0, "min_vol": 0.01}

    def predict(self, ctx, horizons):
        out = {}
        hist = ctx.hist
        for h in horizons:
            ch = log_changes(hist, h, self.p["window"])
            if len(ch) < self.p["min_changes"]:
                out[h] = None
                continue
            vol_hist = log_changes(hist, 1, self.p["vol_window"])
            if len(vol_hist) == 0:
                realized_vol = self.p["min_vol"]
            else:
                realized_vol = max(np.std(vol_hist), self.p["min_vol"])
            width = self.p["width"]
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            # Widen quantile offsets by realized_log_vol
            lo = mid + (lo - mid) * realized_vol / np.std(ch) * width
            hi = mid + (hi - mid) * realized_vol / np.std(ch) * width
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
