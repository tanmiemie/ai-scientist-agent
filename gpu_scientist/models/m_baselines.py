"""Reference models: the flat last value and an empirical random walk like the starter's drift."""
import numpy as np

from data import log_changes
from .base import Model, from_log


class LastValue(Model):
    name = "last_value"

    def predict(self, ctx, horizons):
        return {h: (ctx.last,) * 3 for h in horizons}


class Drift(Model):
    """Empirical 0.1/0.5/0.9 quantiles of past h-day log changes (window=None: whole history)."""
    name = "drift"
    defaults = {"window": None, "min_changes": 20}

    def predict(self, ctx, horizons):
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, self.p["window"])
            if np.count_nonzero(ch) < self.p["min_changes"]:
                out[h] = (ctx.last,) * 3
                continue
            out[h] = from_log(ctx.last, *np.quantile(ch, [0.1, 0.5, 0.9]))
        return out
