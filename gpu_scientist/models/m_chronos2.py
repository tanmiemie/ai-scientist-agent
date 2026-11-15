"""Chronos-2 (Amazon, Oct 2025; Apache-2.0), zero-shot, optionally with group attention over peers.

Hypothesis it tests: Chronos-2 leads fev-bench/GIFT-Eval among open pretrained models and, unlike
Chronos-Bolt, can forecast a group of related series jointly ("cross_learning"). Our strongest
hand-built gain came from pooling change distributions across related series, so a pretrained
model that pools in context may give better q10/q90 than trend_tail.

Only ctx.hist and ctx.peers() are used, both cut at the origin. Peers are restricted to the same
instrument_class so different instrument classes are never mixed.

Params
  model_id      "autogluon/chronos-2-small" (28M) or "amazon/chronos-2" (120M)
  context_days  most recent daily values fed to the model
  median_mode   "model" or "last" (keep the last value as q50, use Chronos-2 only for the spread)
  group         "none" or a catalog column (e.g. "gpu_model"): forecast the series jointly with
                its same-class peers sharing that column, via cross_learning
  max_peers     cap on peers in the group (longest histories first)
  width         multiplier on the log spread around q50
"""
import numpy as np

from .base import Model, from_log

_PIPES = {}


def _pipe(model_id):
    if model_id not in _PIPES:
        import torch
        from chronos import BaseChronosPipeline
        _PIPES[model_id] = BaseChronosPipeline.from_pretrained(model_id, device_map="cpu",
                                                               torch_dtype=torch.float32)
    return _PIPES[model_id]


class Chronos2(Model):
    name = "chronos2"
    defaults = {"model_id": "autogluon/chronos-2-small", "context_days": 90,
                "median_mode": "last", "group": "none", "max_peers": 15, "width": 1.0}

    def predict(self, ctx, horizons):
        p = self.p
        own = ctx.hist.values[-p["context_days"]:].astype(float)
        if len(own) < 14:
            return {h: None for h in horizons}
        inputs = [np.log(own)]
        cross = False
        if p["group"] != "none":
            same_cls = set(ctx.peers("instrument_class"))
            peers = [h for sid, h in ctx.peers(p["group"]).items() if sid in same_cls and len(h) >= 14]
            peers = sorted(peers, key=len, reverse=True)[:p["max_peers"]]
            inputs += [np.log(h.values[-p["context_days"]:].astype(float)) for h in peers]
            cross = len(inputs) > 1
        H = max(horizons)
        q, _ = _pipe(p["model_id"]).predict_quantiles(inputs, prediction_length=H,
                                                      quantile_levels=[0.1, 0.5, 0.9],
                                                      cross_learning=cross)
        q = q[0].detach().cpu().numpy()[0]        # (H, 3) for the target series
        last_log = np.log(ctx.last)
        out = {}
        for h in horizons:
            lo, mid, hi = q[h - 1] - last_log
            if p["median_mode"] == "last":
                lo, hi, mid = lo - mid, hi - mid, 0.0
            lo, hi = mid + p["width"] * (lo - mid), mid + p["width"] * (hi - mid)
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
