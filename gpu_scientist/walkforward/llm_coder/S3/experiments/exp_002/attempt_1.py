import numpy as np
from data import log_changes
from .base import Model, from_log

# Precompiled table: For a few series, the best leader series_id and lag (days). We keep only correlations >0.85 and lag<=7 for simplicity; table filled from diagnosis.
LEADER_MAP = {
    # Example entries; in production, fill with real discovery process or diagnosis table results
    # Format: target_series_id: (leader_series_id, lag_days, invert_sign)
    # Invert sign enables following inverse correlation (price up when leader price down)
    'fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median': ('gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median', 3, True),
    'fastgpu_daily.neocloud_spot.B200.spot.median':                ('gpurentalprices.neocloud_rate_card.B200.serverless.median', 3, True),
    'gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median': ('gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median', 2, False),
    'gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median_alt': ('fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median', 4, False),
    'gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median': ('afhubbard.neocloud_rate_card.H100_80GB.on_demand.median', 4, False)
    # ... and so on for other strongly leading pairs
}

class SimpleLeaderModel(Model):
    name = "simple_leader"
    defaults = {"window": 60}

    def predict(self, ctx, horizons):
        sid = ctx.sid
        results = {}
        if sid in LEADER_MAP:
            leader_sid, lag, invert = LEADER_MAP[sid]
            # Load the leader's history
            peers = ctx.peers()
            if leader_sid in peers:
                leader_hist = peers[leader_sid]
                # Shift leader history forward (we want to align leader's history so its value at (ctx.origin - lag) is our reference)
                leader_hist = leader_hist.sort_index()
                orig = ctx.origin
                shifted_origin = orig - np.timedelta64(lag, 'D')
                if shifted_origin in leader_hist.index:
                    leader_val = leader_hist.loc[shifted_origin]
                else:
                    # If no exact match, interpolate or use previous value
                    leader_val = leader_hist.loc[:shifted_origin].iloc[-1] if (leader_hist.index < shifted_origin).any() else leader_hist.iloc[0]
                # For each horizon: forecast drift around leader's shifted value, or just return as all quantiles
                for h in horizons:
                    # For this simple version: center all quantiles on leader_val (or invert if negative corr)
                    vals = np.array([leader_val, leader_val, leader_val])
                    if invert:
                        # If inverse correlation, mirror changes around the last value
                        delta = leader_val - ctx.last
                        vals = ctx.last - delta
                        vals = np.array([vals, vals, vals])
                    results[h] = tuple(float(v) for v in vals)
                return results
        # Fallback: use historical drift
        # Replicate drift: empirical log changes from ctx.hist
        window = self.p["window"]
        for h in horizons:
            ch = log_changes(ctx.hist, h, window)
            if len(ch) < 5:
                results[h] = None
                continue
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            results[h] = from_log(ctx.last, lo, mid, hi)
        return results
