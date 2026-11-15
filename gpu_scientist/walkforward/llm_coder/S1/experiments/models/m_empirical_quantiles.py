import numpy as np
from data import log_changes
from .base import Model, from_log

class EmpiricalQuantilesModel(Model):
    name = "empirical_quantiles"
    defaults = {"window": 60}

    def predict(self, ctx, horizons):
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, self.p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
