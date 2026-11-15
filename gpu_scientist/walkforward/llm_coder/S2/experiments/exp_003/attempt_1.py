import numpy as np
from data import log_changes
from .base import Model, from_log

class VolWeightedDriftBroaderModel(Model):
    name = "vol_weighted_drift_broader"
    defaults = {"window": 60, "min_changes": 20, "vol_window": 30, "width": 1.3}

    def predict(self, ctx, horizons):
        out = {}
        last = ctx.last
        hist = ctx.hist
        window = self.p["window"]
        min_changes = self.p["min_changes"]
        vol_window = self.p["vol_window"]
        width = self.p["width"]
        for h in horizons:
            changes = log_changes(hist, h, window)
            if changes is None or len(changes) < min_changes:
                out[h] = None
                continue
            drift = np.median(changes)
            end = len(changes)
            start = max(0, end - vol_window)
            recent_changes = changes[start:end]
            vol = np.std(recent_changes) if len(recent_changes) > 1 else 0.0
            q10 = drift - width * vol
            q50 = drift
            q90 = drift + width * vol
            out[h] = from_log(last, q10, q50, q90)
        return out
