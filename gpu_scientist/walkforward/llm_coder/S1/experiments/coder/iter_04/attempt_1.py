import numpy as np
from data import log_changes, days_since_change
from .base import Model, from_log

class StaleAwareQuantilesModel(Model):
    name = "stale_aware_quantiles"
    defaults = {"window": 30, "stale_thresh": 7, "max_scale": 2.0}

    def predict(self, ctx, horizons):
        out = {}
        dsc = days_since_change(ctx.hist)
        # scaling: 1.0 for dsc <= stale_thresh, then linear to max_scale at dsc>=30
        if dsc <= self.p["stale_thresh"]:
            scale = 1.0
        elif dsc >= 30:
            scale = self.p["max_scale"]
        else:
            scale = 1.0 + (self.p["max_scale"] - 1.0) * (dsc - self.p["stale_thresh"]) / (30 - self.p["stale_thresh"])
        ch = log_changes(ctx.hist, 1, self.p["window"])
        if len(ch) < 5:
            # fall back to last value for all horizons
            for h in horizons:
                out[h] = None
            return out
        # get log-change quantiles
        lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
        mid = float(mid)
        lo = float(mid + (lo - mid) * scale)
        hi = float(mid + (hi - mid) * scale)
        for h in horizons:
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
