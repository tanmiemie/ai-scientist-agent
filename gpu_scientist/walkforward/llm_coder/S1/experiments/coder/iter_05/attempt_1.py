import numpy as np
from data import log_changes, days_since_change
from .base import Model, from_log

class GentleStaleAwareQuantiles(Model):
    name = "gentle_stale_aware_quantiles"
    defaults = {"window": 30, "stale_thresh": 7, "max_scale": 1.25}

    def predict(self, ctx, horizons):
        out = {}
        dsc = days_since_change(ctx.hist)
        for h in horizons:
            ch = log_changes(ctx.hist, h, self.p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            qlo, qmed, qhi = np.quantile(ch, [0.1,0.5,0.9])
            width = qhi - qlo
            # Smooth, modest nonlinear ramp for stale data
            scale = 1.0
            if dsc > self.p["stale_thresh"]:
                ramp = min(dsc - self.p["stale_thresh"], 20)
                # sigmoid-based ramp, starts slow, maxes at max_scale
                scale = 1 + (self.p["max_scale"] - 1) * (1 - np.exp(-ramp/7.0))
            # widen interval only, median unchanged
            c = (qhi+qlo)/2
            qlo_new = qmed - scale*(qmed-qlo)
            qhi_new = qmed + scale*(qhi-qmed)
            out[h] = from_log(ctx.last, qlo_new, qmed, qhi_new)
        return out
