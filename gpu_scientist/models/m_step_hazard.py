"""Step (jump) model: posted prices mostly stay flat and sometimes jump.

Each day a change happens with probability p (estimated over the recent window); a change
size is drawn from the recent non-zero daily log changes. The h-day distribution is the
sum of Binomial(h, p) jumps, simulated; its 0.1/0.5/0.9 quantiles are the forecast.
"""
import numpy as np

from data import log_changes
from .base import Model, from_log


class StepHazard(Model):
    name = "step_hazard"
    defaults = {"window": 60, "n_sims": 4000, "min_jumps": 3, "seed": 0}

    def predict(self, ctx, horizons):
        p = self.p
        ch1 = log_changes(ctx.hist, 1, p["window"])
        if len(ch1) < 10:
            return {h: None for h in horizons}
        jumps = ch1[ch1 != 0]
        if len(jumps) < p["min_jumps"]:
            return {h: (ctx.last,) * 3 for h in horizons}
        rate = len(jumps) / len(ch1)
        rng = np.random.default_rng(p["seed"])
        out = {}
        for h in horizons:
            n = rng.binomial(h, rate, size=p["n_sims"])
            draws = rng.choice(jumps, size=(p["n_sims"], h))
            mask = np.arange(h)[None, :] < n[:, None]
            total = (draws * mask).sum(axis=1)
            out[h] = from_log(ctx.last, *np.quantile(total, [0.1, 0.5, 0.9]))
        return out
