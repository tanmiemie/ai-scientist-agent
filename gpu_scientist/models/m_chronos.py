"""Chronos-Bolt (Amazon's pretrained time-series model), zero-shot.

Hypothesis it tests: a foundation time-series model forecasts posted GPU rental prices at
least as well as our hand-built models, with no training. Expectation is cautious: these
series are short (60-90 days) and move in steps or small upward ticks, which such models tend
to smooth.

Install (not needed by the rest of the framework):
    pip install chronos-forecasting        # pulls in torch
The first run downloads the weights from Hugging Face (amazon/chronos-bolt-small, ~200 MB).

Only data up to the origin is passed in. Chronos-Bolt was trained before these 2026 series
existed, so the pretrained weights cannot have seen them.

Params
  model_id      Hugging Face id ("amazon/chronos-bolt-small"; "amazon/chronos-bolt-base" is slower)
  context_days  how many most recent daily values to feed the model
  median_mode   "model": use Chronos' own median; "last": keep the last value as the median and
                use Chronos only for the width of the interval (tests whether its median hurts)
  log_input     feed log prices (scale-free) instead of raw prices
  model_id "__fake__" swaps in a trivial stand-in so the plumbing can be smoke-tested offline.
"""
import numpy as np

from .base import Model, from_log

_PIPELINES = {}


def _pipeline(model_id):
    if model_id not in _PIPELINES:
        if model_id == "__fake__":
            _PIPELINES[model_id] = _FakePipeline()
        else:
            import torch
            from chronos import BaseChronosPipeline
            torch.set_num_threads(max(1, torch.get_num_threads()))
            _PIPELINES[model_id] = BaseChronosPipeline.from_pretrained(model_id, device_map="cpu",
                                                                        torch_dtype=torch.float32)
    return _PIPELINES[model_id]


class _FakePipeline:
    """Offline stand-in with the same predict_quantiles signature (random walk on the context)."""
    def predict_quantiles(self, inputs, prediction_length, quantile_levels):
        x = np.asarray(inputs[0], dtype=float)
        d = np.diff(x[-60:]) if len(x) > 2 else np.zeros(1)
        steps = np.arange(1, prediction_length + 1)[:, None]
        q = x[-1] + np.quantile(d, quantile_levels)[None, :] * np.sqrt(steps)
        return q[None, ...], None


class Chronos(Model):
    name = "chronos"
    defaults = {"model_id": "amazon/chronos-bolt-small", "context_days": 90,
                "median_mode": "model", "log_input": True}

    def predict(self, ctx, horizons):
        p = self.p
        vals = ctx.hist.values[-p["context_days"]:].astype(float)
        if len(vals) < 14:
            return {h: None for h in horizons}
        series = np.log(vals) if p["log_input"] else vals
        pipe = _pipeline(p["model_id"])
        H = max(horizons)
        if p["model_id"] == "__fake__":
            q, _ = pipe.predict_quantiles([series], prediction_length=H, quantile_levels=[0.1, 0.5, 0.9])
        else:
            import torch
            q, _ = pipe.predict_quantiles(torch.tensor(series, dtype=torch.float32)[None, :],
                                          prediction_length=H, quantile_levels=[0.1, 0.5, 0.9])
            q = q.detach().cpu().numpy()
        q = np.asarray(q)[0]                      # (H, 3)
        last_log = np.log(ctx.last)
        out = {}
        for h in horizons:
            row = q[h - 1]
            lo, mid, hi = (row - last_log) if p["log_input"] else np.log(np.maximum(row, 1e-9) / ctx.last)
            if p["median_mode"] == "last":
                lo, hi, mid = lo - mid, hi - mid, 0.0   # keep Chronos' spread, centre on the last value
            out[h] = from_log(ctx.last, lo, mid, hi)
        return out
