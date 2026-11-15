"""The automatic DEV sweep must (1) pick the value with the best DEV score and (2) never forecast a
HOLDOUT origin, so the gate sees exactly one candidate per idea."""
import pandas as pd

import autoresearch
import config as C
import online


def test_set_path():
    s = {"models": [{"name": "trend_tail", "params": {"window": 60}}], "calibrate": {"enabled": True}}
    assert autoresearch._set(s, "models.0.params.window", 30)["models"][0]["params"]["window"] == 30
    assert autoresearch._set(s, "calibrate.gamma", 0.7)["calibrate"]["gamma"] == 0.7
    assert s["models"][0]["params"]["window"] == 60  # original untouched


def test_sweep_dev_only_and_best(built, monkeypatch):
    seen = []
    real = online.run

    def spy(spec, panel, origins, *a, **k):
        seen.append(pd.DatetimeIndex(origins).max())
        return real(spec, panel, origins, *a, **k)

    monkeypatch.setattr(online, "run", spy)
    spec = {"models": [{"name": "trend_tail", "params": {"window": 60}}]}
    best, rows = autoresearch.dev_sweep(spec, {"param": "models.0.params.window", "values": [20, 90]},
                                        heavy=False, tried=set())
    scored = [r for r in rows if "dev" in r]
    assert len(scored) == 2
    assert best["models"][0]["params"]["window"] == max(scored, key=lambda r: r["dev"])["value"]
    assert seen and max(seen) <= pd.Timestamp(C.DEV_ORIGINS[1]) < pd.Timestamp(C.HOLDOUT_ORIGINS[0])
