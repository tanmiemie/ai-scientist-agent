import numpy as np
from data import log_changes
from .base import Model, from_log

class WideDriftModel(Model):
    name = "wide_drift"
    defaults = {"width": 1.0, "window": None, "min_changes": 20}

    def predict(self, ctx, horizons):
        hist = ctx.hist
        window = self.p["window"]
        min_changes = self.p["min_changes"]
        out = {}
        for h in horizons:
            ch = log_changes(hist, h, window)
            if ch is None or len(ch) < min_changes:
                out[h] = None
                continue
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            # center stays, widen quantiles around center
            mid_ = mid
            width = float(self.p["width"])
            lo_ = mid_ + (lo - mid_) * width
            hi_ = mid_ + (hi - mid_) * width
            out[h] = from_log(ctx.last, lo_, mid_, hi_)
        return out
