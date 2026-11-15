import numpy as np
from data import log_changes, days_since_change
from .base import Model, from_log

class LogEmpiricalAdjvolWindowModel(Model):
    name = "log_empirical_adjvol_window"
    defaults = {"window": 60, "vol_scale": 1.4, "vol_days": 1, "stable_scale": 1.0, "stable_days": 7}

    def predict(self, ctx, horizons):
        out = {}
        window = self.p["window"]
        vol_scale = self.p["vol_scale"]
        vol_days = self.p["vol_days"]
        stable_scale = self.p["stable_scale"]
        stable_days = self.p["stable_days"]
        dsc = days_since_change(ctx.hist)
        # Linear interpolation of scale: most wide for min days, taper to stable for stable_days or above
        def scale(dsc):
            if dsc <= vol_days:
                return vol_scale
            elif dsc >= stable_days:
                return stable_scale
            else:
                return vol_scale + (stable_scale - vol_scale) * (dsc - vol_days) / (stable_days - vol_days)
        width_scale = scale(dsc)
        for h in horizons:
            ch = log_changes(ctx.hist, h, window)
            if len(ch) < 5:
                out[h] = None
                continue
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            mid_offset = mid
            lo_offset = mid + (lo - mid) * width_scale
            hi_offset = mid + (hi - mid) * width_scale
            lo_offset, mid_offset, hi_offset = sorted((lo_offset, mid_offset, hi_offset))
            out[h] = from_log(ctx.last, lo_offset, mid_offset, hi_offset)
        return out
