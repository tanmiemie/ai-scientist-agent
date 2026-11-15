"""trend_tail plus a same-instrument-class leading signal from a named series in another collector.

DEV evidence (scratch/dev_lead_eda.py on exp_000 of experiments_devin): of the top-10 candidate
leading signals in diagnosis.md, 8 rest on 1-3 coincident moves (e.g. the +/-0.928 B200 pairs have
a single leader move) and are discarded. Two pairs have many coincident moves and the same
instrument class on both sides, so they are the only ones used (exact source series below):
  gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median
      <- afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median, lag 1 (25 of 25 follower moves coincide)
  fastgpu_daily.neocloud_spot.L40S.spot.median
      <- afhubbard.neocloud_spot.L40S.spot.median, lag 1 (11 of 12 follower moves coincide)
If the leader moved within the last `lag` days and the follower has not moved since, the follower's
median is shifted by `beta` x the leader's move and the band edge on that side is widened to it.
The leader is read from ctx.peers() (cut at the origin); no curve is chained across classes.
"""
import numpy as np

from data import days_since_change, log_changes
from .base import Model, from_log

PAIRS = {
    "gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median":
        ("afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median", 1),
    "fastgpu_daily.neocloud_spot.L40S.spot.median":
        ("afhubbard.neocloud_spot.L40S.spot.median", 1),
}


class Leader(Model):
    name = "leader"
    defaults = {"window": 60, "floor": 1.0, "beta": 1.0}

    def _signal(self, ctx):
        pair = PAIRS.get(ctx.sid)
        if pair is None:
            return 0.0
        leader, lag = pair
        lh = ctx.peers().get(leader)
        if lh is None or len(lh) <= lag or lh.index[-1] < ctx.origin:
            return 0.0
        move = float(np.log(lh.iloc[-1] / lh.iloc[-1 - lag]))
        if move == 0 or days_since_change(ctx.hist) < lag:
            return 0.0                      # leader quiet, or follower already moved
        return self.p["beta"] * move

    def predict(self, ctx, horizons):
        p = self.p
        ch1 = log_changes(ctx.hist, 1, p["window"])
        nz = np.abs(ch1[ch1 != 0])
        step = float(np.median(nz)) if len(nz) else 0.0
        s = self._signal(ctx)
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            lo, hi = np.quantile(ch, [0.1, 0.9])
            up = max(max(hi, 0), p["floor"] * step)
            dn = min(lo, 0)
            out[h] = from_log(ctx.last, min(dn, s), s, max(up, s))
        return out
