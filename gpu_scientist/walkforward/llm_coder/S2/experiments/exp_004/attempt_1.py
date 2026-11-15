import numpy as np
import pandas as pd
from data import log_changes
from .base import Model, from_log

class PeerLeaderLagModel(Model):
    name = "peer_leader_lag"
    defaults = {"window": 60, "max_lag": 5}  # days

    def predict(self, ctx, horizons):
        # Find eligible peers: same GPU model, different series
        peers = ctx.peers("gpu_model")
        if len(peers) <= 1:
            return {h: None for h in horizons}
        target_hist = ctx.hist
        best_peer = None
        best_lag = 0
        best_corr = -np.inf
        # Only consider peers that are not the current series
        for sid, peer_s in peers.items():
            if sid == ctx.sid:
                continue
            # Use inner join to ensure common history
            df = pd.DataFrame({"target": target_hist, "peer": peer_s.dropna()}).dropna()
            if len(df) < 10:
                continue
            # Try all lags within allowed max_lag, seeking positive lag (peer leads target)
            for lag in range(1, self.p["max_lag"] + 1):
                target_aligned = df['target'].iloc[lag:].values
                peer_aligned = df['peer'].iloc[:-lag].values
                if len(target_aligned) < 5:
                    continue
                corr = np.corrcoef(target_aligned, peer_aligned)[0, 1]
                if np.abs(corr) > abs(best_corr):
                    best_peer = peer_s
                    best_lag = lag
                    best_corr = corr
        if best_peer is None or best_lag == 0:
            return {h: None for h in horizons}
        # Now, for prediction, use the best peer's last h-day log changes and empirical quantiles
        out = {}
        peer_hist = best_peer.copy()
        peer_hist = peer_hist.loc[:ctx.origin]
        for h in horizons:
            # To forecast h days ahead, use peer's log changes h days ahead of target's origin
            # Find a window of prior dates (ending before origin+0), shift forward by lag
            target_dates = target_hist.index
            peer_dates = peer_hist.index
            # select peer_window pre-cut to origin - best_lag days
            latest_peer_date = ctx.origin - pd.Timedelta(days=best_lag)
            peer_hist_cut = peer_hist.loc[:latest_peer_date]
            chg = log_changes(peer_hist_cut, h, self.p["window"])
            # If not enough for quantile, fallback
            if len(chg) < 5:
                out[h] = None
                continue
            q_lo, q_mid, q_hi = np.quantile(chg, [0.1, 0.5, 0.9])
            out[h] = from_log(ctx.last, q_lo, q_mid, q_hi)
        return out
