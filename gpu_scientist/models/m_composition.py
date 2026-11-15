"""momentum, but tells repricing apart from a change in who is listed.

EDA.md: 45% of 10%+ moves happen on a day the provider count changed, and such moves are 7x larger
than other moves; 31% of 10%+ moves are half undone within 7 days. A median over 2-3 providers jumps
when one joins or leaves, without anyone repricing.

So, at the origin, look at the most recent price move and whether the provider count changed that day:
- a rise WITHOUT a provider-count change: momentum shift up by `beta` typical moves (as `momentum`);
- a move WITH a provider-count change: no momentum; if it is at least `thresh` in size and at most
  `k_rev` days old, shift the median back by `rho` of the move (partial reversion) and widen the edge
  on that side so the last value stays inside the interval.
Uses only ctx.hist and ctx.raw() (both cut at the origin).
"""
import numpy as np

from data import days_since_change, log_changes
from .base import Model, from_log


class Composition(Model):
    name = "composition"
    defaults = {"window": 60, "k_up": 1.0, "k_dn": 1.0, "floor": 1.0, "k": 1, "beta": 0.25,
                "rho": 0.3, "thresh": 0.05, "k_rev": 3}

    def predict(self, ctx, horizons):
        p = self.p
        ch1 = log_changes(ctx.hist, 1, p["window"])
        nz = np.abs(ch1[ch1 != 0])
        step = float(np.median(nz)) if len(nz) else 0.0
        v = np.log(ctx.hist.values.astype(float))
        moves = np.nonzero(np.diff(v))[0]
        shift = 0.0
        if len(moves):
            i = moves[-1]
            move = v[i + 1] - v[i]
            day = ctx.hist.index[i + 1]
            raw = ctx.raw()
            prov = raw.n_providers
            comp = False
            if day in prov.index:
                before = prov.loc[:day - np.timedelta64(1, "D")]
                comp = len(before) > 0 and prov.loc[day] != before.iloc[-1]
            age = days_since_change(ctx.hist)
            if not comp and move > 0 and age <= p["k"]:
                shift = p["beta"] * step
            elif comp and abs(move) >= p["thresh"] and age <= p["k_rev"]:
                shift = -p["rho"] * move
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            lo, hi = np.quantile(ch, [0.1, 0.9])
            up = max(max(hi, 0) * p["k_up"], p["floor"] * step) + max(shift, 0)
            dn = min(lo, 0) * p["k_dn"] + min(shift, 0)
            out[h] = from_log(ctx.last, min(dn, shift), shift, max(up, shift))
        return out
