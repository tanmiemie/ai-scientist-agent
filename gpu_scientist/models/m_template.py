"""Template for a new model. Copy to models/m_<name>.py, rename the class and `name`.

Rules: use only ctx.hist / ctx.raw() / ctx.peers() (all cut at the origin). No file or
network access. Keep it deterministic (seed any randomness).
"""
import numpy as np

from data import log_changes
from .base import Model, from_log


class TemplateModel(Model):
    name = ""                      # set a unique name, e.g. "my_idea"
    defaults = {"window": 60}      # every tunable parameter, with its default

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
