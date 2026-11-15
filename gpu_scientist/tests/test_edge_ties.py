"""A truth exactly on q10 or q90 counts as inside the interval (the EDGE_TOL tie fix in online.py).

A flat series forecast by last_value has q10 = q50 = q90 = exp(log(y)), which differs from y in the
last bit for many y. Every feedback must count as inside, so each calibration offset moves by
exactly -0.1 * gamma * scale per realised target."""
import math

import numpy as np
import pandas as pd
import pytest

import data
import online

GAMMA, SCALE = 0.5, 0.01


def flat_panel(tmp_path, value, days=40):
    dates = pd.date_range("2026-09-01", periods=days)
    raw = pd.DataFrame({"series_id": "t.flat", "date": dates.strftime("%Y-%m-%d"), "value": value,
                        "n_providers": 3, "source_id": "t", "instrument_class": "flat"})
    cat = pd.DataFrame([{"series_id": "t.flat", "tier": "headline", "source_id": "t",
                         "instrument_class": "flat", "gpu_model": "X"}])
    raw.to_csv(tmp_path / "s.csv", index=False)
    cat.to_csv(tmp_path / "c.csv", index=False)
    return data.Panel.load(tmp_path / "s.csv", tmp_path / "c.csv"), dates


def roundoff_values():
    """Prices where exp(log(y)) != y, the case that used to flip with the machine."""
    vals = [v for v in np.round(np.arange(0.5, 6.0, 0.0137), 4) if math.exp(math.log(v)) != v]
    assert vals, "no round-off example found"
    return [vals[0], vals[len(vals) // 2], 1.9891]


@pytest.mark.parametrize("value", roundoff_values())
def test_edge_ties(tmp_path, value):
    panel, dates = flat_panel(tmp_path, value)
    spec = {"models": [{"name": "last_value"}],
            "calibrate": {"enabled": True, "gamma": GAMMA, "scale": SCALE, "group_by": "all"}}
    origins = dates[10:]
    fc, _, state = online.run(spec, panel, origins, ["t.flat"], (1, 3, 7))
    assert np.allclose(fc[["q10", "q50", "q90"]].values, value, rtol=1e-12)
    for h in (1, 3, 7):
        n_fb = sum(1 for o in origins if o + pd.Timedelta(days=h) <= origins[-1])
        expect = -0.1 * GAMMA * SCALE * n_fb
        assert state["calibration_up"][f"all|h{h}"] == pytest.approx(expect, abs=1e-12)
        assert state["calibration_dn"][f"all|h{h}"] == pytest.approx(expect, abs=1e-12)


def test_real_miss_still_counts(tmp_path):
    """Beyond the tolerance a truth outside the interval is still a miss."""
    panel, dates = flat_panel(tmp_path, 2.0)
    raw = panel.raw.copy()
    raw.loc[raw.date >= dates[20], "value"] = 2.0 * (1 + 1e-6)
    raw["date"] = raw.date.dt.strftime("%Y-%m-%d")
    raw.to_csv(tmp_path / "s2.csv", index=False)
    p2 = data.Panel.load(tmp_path / "s2.csv", tmp_path / "c.csv")
    spec = {"models": [{"name": "last_value"}],
            "calibrate": {"enabled": True, "gamma": GAMMA, "scale": SCALE, "group_by": "all"}}
    _, _, s_flat = online.run(spec, panel, dates[10:21], ["t.flat"], (1,))
    _, _, s_step = online.run(spec, p2, dates[10:21], ["t.flat"], (1,))
    assert s_step["calibration_up"]["all|h1"] > s_flat["calibration_up"]["all|h1"]
