from __future__ import annotations

import numpy as np


class Model:
    """Interface every forecaster implements.

    predict(ctx, horizons) -> {h: (q10, q50, q90)} in USD per GPU-hour.
    `ctx` (data.Ctx) only holds data dated on or before ctx.origin. Return None for a
    horizon you cannot forecast; the pipeline then falls back to the last value.
    """
    name: str = ""
    defaults: dict = {}

    def __init__(self, **params):
        unknown = set(params) - set(self.defaults)
        if unknown:
            raise ValueError(f"{self.name}: unknown params {unknown}")
        self.p = {**self.defaults, **params}

    def predict(self, ctx, horizons) -> dict:
        raise NotImplementedError


def from_log(last: float, lo: float, mid: float, hi: float) -> tuple:
    """Quantiles from log offsets around the last value, made monotone and positive."""
    lo, mid, hi = sorted((lo, mid, hi))
    return (last * np.exp(lo), last * np.exp(mid), last * np.exp(hi))
