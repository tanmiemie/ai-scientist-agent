import numpy as np
from data import log_changes
from .base import Model, from_log

class VolTailModel(Model):
    name = "vol_tail"
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
            # Use the last 'lookback' log changes for volatility
            recent = ch[-lb:] if len(ch) > lb else ch
            spread = np.median(np.abs(recent - np.median(recent)))
            # Scale spread (MAD) up for tail, clipped
            lo = median - m * np.clip(spread, lo_clip, hi_clip)
            hi = median + m * np.clip(spread, lo_clip, hi_clip)
            out[h] = from_log(ctx.last, max(lo, -np.log(floor)), median, hi)
        return out
