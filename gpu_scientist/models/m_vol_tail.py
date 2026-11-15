"""trend_tail with a per-series, volatility-aware band rescaling learned from the series' own past.

DEV evidence (exp_000 of experiments_devin): online calibration adds one additive log offset per
collector x class, which brings coverage to 0.80 but drops the geomean skill from +0.166
(uncalibrated trend_tail) to +0.115: quiet series in a group are widened as much as volatile ones.
Here each series first replays trend_tail on its own last `lookback` origins (targets <= origin,
so only ctx.hist is used), measures how far realised moves landed relative to each band edge, and
rescales the edges by the 90th percentile of that ratio, shrunk toward 1 with `m` pseudo-cells.
"""
import numpy as np

from data import log_changes
from .base import Model, from_log


def _edges(v, h, window, floor):
    """trend_tail's (dn, up) log offsets from a log-price array ending at the origin."""
    c1 = np.diff(v[-(window + 1):])
    nz = np.abs(c1[c1 != 0])
    step = float(np.median(nz)) if len(nz) else 0.0
    w = v[-(window + h):]
    ch = w[h:] - w[:-h]
    if len(ch) < 5:
        return None
    lo, hi = np.quantile(ch, [0.1, 0.9])
    return min(lo, 0.0), max(max(hi, 0.0), floor * step)


class VolTail(Model):
    name = "vol_tail"
    defaults = {"window": 60, "floor": 1.0, "lookback": 30, "m": 10.0, "lo_clip": 0.5, "hi_clip": 2.0}

    def predict(self, ctx, horizons):
        p = self.p
        v = np.log(ctx.hist.values.astype(float))
        out = {}
        for h in horizons:
            if len(log_changes(ctx.hist, h, p["window"])) < 5:
                out[h] = None
                continue
            dn, up = _edges(v, h, p["window"], p["floor"])
            ru, rd = [], []
            for t in range(len(v) - h - p["lookback"], len(v) - h):
                if t < 10:
                    continue
                e = _edges(v[:t + 1], h, p["window"], p["floor"])
                if e is None:
                    continue
                y = v[t + h] - v[t]
                if e[1] > 0:
                    ru.append(max(y, 0.0) / e[1])
                if e[0] < 0:
                    rd.append(max(-y, 0.0) / -e[0])
            fu = self._factor(ru)
            fd = self._factor(rd)
            out[h] = from_log(ctx.last, dn * fd, 0.0, up * fu)
        return out

    def _factor(self, r):
        p = self.p
        if not r:
            return 1.0
        q = float(np.quantile(r, 0.9))
        f = (len(r) * q + p["m"]) / (len(r) + p["m"])
        return float(np.clip(f, p["lo_clip"], p["hi_clip"]))
