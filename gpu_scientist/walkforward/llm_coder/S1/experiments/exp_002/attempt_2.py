import numpy as np
from data import log_changes
from .base import Model, from_log

class VolAdaptModel(Model):
    name = "vol_adapt"
    defaults = {"window": 60, "lookback": 30, "m": 10.0, "lo_clip": 0.5, "hi_clip": 2.0, "floor": 1.0}

    def predict(self, ctx, horizons):
        out = {}
        hist = ctx.hist
        w = self.p["window"]
        lb = self.p["lookback"]
        m = self.p["m"]
        lo_clip = self.p["lo_clip"]
        hi_clip = self.p["hi_clip"]
        floor = self.p["floor"]
        for h in horizons:
            ch = log_changes(hist, h, w)
            if len(ch) < 5:
                out[h] = None
                continue
            median = np.median(ch)
            recent = ch[-lb:] if len(ch) > lb else ch
            spread = np.median(np.abs(recent - np.median(recent)))
            mad = np.clip(spread, lo_clip, hi_clip)
            lo = median - m * mad
            hi = median + m * mad
            # Lower bound by log(floor)
            out[h] = from_log(ctx.last, max(lo, -np.log(floor)), median, hi)
        return out
