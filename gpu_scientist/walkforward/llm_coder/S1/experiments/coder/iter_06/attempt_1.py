import numpy as np
from data import log_changes
from .base import Model, from_log

class LeaderQuantilesModel(Model):
    name = "leader_quantiles"
    defaults = {"window": 30, "leader_weight": 0.5, "lag_days": 2}

    def predict(self, ctx, horizons):
        # Standard quantiles from rolling log changes
        out = {}
        self_id = ctx.meta.get("source_id", None)
        gpu_model = ctx.meta.get("gpu_model", None)
        series_candidates = ctx.peers(same="gpu_model") if gpu_model else {}
        # Pick a leader: any series with DIFFERENT source_id
        leader_sid = None
        for sid, s in series_candidates.items():
            if sid == ctx.sid: continue
            meta = s.attrs.get("meta") or {}
            if meta.get("source_id") != self_id:
                leader_sid = sid
                break
        # Try to get the leader series
        leader_hist = None
        if leader_sid:
            leader_hist = series_candidates[leader_sid]
            # Apply lag: shift leader forward by lag_days
            leader_hist = leader_hist.shift(self.p["lag_days"])
            # Drop any nans (aligned with index)
            leader_hist = leader_hist.dropna()
        for h in horizons:
            # Empirical quantiles as baseline
            ch = log_changes(ctx.hist, h, self.p["window"])
            if len(ch) < 5:
                out[h] = None
                continue
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            # Compute leader log-change if available
            if leader_hist is not None and len(leader_hist) >= 2:
                # Log change over minimum window
                lch = log_changes(leader_hist, h, self.p["window"])
                if len(lch) < 5:
                    # Not enough points in leader: just use empirical
                    out[h] = from_log(ctx.last, lo, mid, hi)
                    continue
                llo, lmid, lhi = np.quantile(lch, [0.1, 0.5, 0.9])
                # Blend the quantiles
                w = self.p["leader_weight"]
                blo = (1-w)*lo + w*llo
                bmid = (1-w)*mid + w*lmid
                bhi = (1-w)*hi + w*lhi
                out[h] = from_log(ctx.last, blo, bmid, bhi)
            else:
                out[h] = from_log(ctx.last, lo, mid, hi)
        return out