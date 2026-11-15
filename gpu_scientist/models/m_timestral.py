"""Timestral (Mistral AI, Oct 2026; Modified MIT), zero-shot.

Hypothesis it tests: Timestral-209M tops GIFT-Eval CRPS and fev-bench SQL among open pretrained
models (model card, Oct 2026), ahead of Chronos-2; if pretrained quantiles help here at all, the
current leader should help most. Only ctx.hist is used (cut at the origin).

Params
  model_id      "mistralai/Timestral-209M" | "-123M" | "-28M" | "-5M"
  context_days  most recent daily values fed to the model
  median_mode   "model" or "last" (keep the last value as q50, use Timestral only for the spread)
  width         multiplier on the log spread around q50
"""
import numpy as np

from .base import Model, from_log

_M = {}


def _model(model_id):
    if model_id not in _M:
        from timestral import TimestralForecaster
        _M[model_id] = TimestralForecaster.from_pretrained(model_id, device="cpu")
    return _M[model_id]


class Timestral(Model):
    name = "timestral"
    defaults = {"model_id": "mistralai/Timestral-209M", "context_days": 90,
                "median_mode": "last", "width": 1.0}

    def predict(self, ctx, horizons):
        p = self.p
        own = ctx.hist.values[-p["context_days"]:].astype(float)
        if len(own) < 14:
            return {h: None for h in horizons}
        H = max(horizons)
        f = _model(p["model_id"]).forecast(np.log(own), prediction_length=H, clip_nonnegative=False)
        lo_s, mid_s, hi_s = (np.asarray(f.quantile(q)).reshape(-1)[-H:] for q in (0.1, 0.5, 0.9))
        last_log = np.log(ctx.last)
        out = {}
        for h in horizons:
            lo, mid, hi = lo_s[h - 1] - last_log, mid_s[h - 1] - last_log, hi_s[h - 1] - last_log
            if p["median_mode"] == "last":
                lo, hi, mid = lo - mid, hi - mid, 0.0
            lo, hi = mid + p["width"] * (lo - mid), mid + p["width"] * (hi - mid)
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
