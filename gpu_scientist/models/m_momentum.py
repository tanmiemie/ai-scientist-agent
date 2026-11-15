"""trend_tail plus momentum after a recent price rise.

DEV evidence (exp_000 of experiments_devin): when the series rose in the last 0-1 days, 68.5% of
truths ended above the last value (n=1281); after a recent fall only 31% ended below it. So the
shift is one-sided: after a rise within `k` days, the median moves up by `beta` typical non-zero
daily moves (and the upper edge with it). The trend_tail part is unchanged.
"""
import numpy as np

from data import days_since_change, log_changes
from .base import Model, from_log


class Momentum(Model):
    name = "momentum"
    defaults = {"window": 60, "k_up": 1.0, "k_dn": 1.0, "floor": 1.0, "k": 1, "beta": 0.5}

    def predict(self, ctx, horizons):
        p = self.p
        ch1 = log_changes(ctx.hist, 1, p["window"])
        nz = np.abs(ch1[ch1 != 0])
        step = float(np.median(nz)) if len(nz) else 0.0
        v = np.log(ctx.hist.values.astype(float))
        moves = np.nonzero(np.diff(v))[0]
        rose = len(moves) > 0 and v[moves[-1] + 1] > v[moves[-1]]
        shift = p["beta"] * step if rose and days_since_change(ctx.hist) <= p["k"] else 0.0
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            lo, hi = np.quantile(ch, [0.1, 0.9])
            up = max(max(hi, 0) * p["k_up"], p["floor"] * step) + shift
            dn = min(lo, 0) * p["k_dn"]
            out[h] = from_log(ctx.last, dn, shift, max(up, shift))
        return out
