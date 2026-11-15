"""No forecast may depend on data dated after its origin.

For each origin, every raw value dated after it (in every series, so peers are covered too) is
multiplied by 3, or those rows are deleted; the Panel is rebuilt and online.run must give
bit-identical forecasts for the run that ends at that origin.

Known issue (test_trailing_fill_depends_on_future_rows, xfail): data.Panel forward-fills each series
up to its last raw row. If a series has no row on the origin but has one later, the history gains
forward-filled days up to the origin; deleting the later rows removes them. Values are unchanged
but the history is one or more days longer, which moves drift quantiles and days-since-change.
This affects about 4% of (headline series, DEV/HOLDOUT origin) pairs, all gpurentalprices. The fix
belongs in data.py, which the overnight rules do not allow editing."""
import json

import pandas as pd
import pytest

import autoresearch
import config as C
import data
import online

ORIGINS = ["2026-09-20", "2026-10-15", "2026-10-30"]
WINDOW_DAYS = 21          # origins walked before the tested origin, so the feedback path is exercised
SPEC04 = json.loads((C.ROOT / "specs" / "04_momentum.json").read_text())
SPECS = {f"single:{n}": {"models": [{"name": n}]} for n in sorted(autoresearch.allowed_models(heavy=False))}
SPECS["spec04"] = {k: v for k, v in SPEC04.items() if not k.startswith("_")}


@pytest.fixture(scope="module")
def series(panel):
    """A few headline series from different sources and classes."""
    cat = panel.catalog[panel.catalog.tier == C.TIER].drop_duplicates(["source_id", "instrument_class"])
    return sorted(cat.series_id)[:6]


def tampered_panel(built, tmp_path, origin, mode):
    series_csv, catalog_csv = built
    raw = pd.read_csv(series_csv)
    after = pd.to_datetime(raw.date) > pd.Timestamp(origin)
    assert after.any(), "nothing to tamper with"
    if mode == "x3":
        raw.loc[after, "value"] = raw.loc[after, "value"] * 3
    else:
        raw = raw[~after]
    path = tmp_path / f"series_{mode}.csv"
    raw.to_csv(path, index=False)
    return data.Panel.load(path, catalog_csv)


def forecast(spec, panel, origin, sids):
    o = pd.Timestamp(origin)
    fc, _, _ = online.run(spec, panel, pd.date_range(o - pd.Timedelta(days=WINDOW_DAYS), o), sids, C.HORIZONS)
    return fc.reset_index(drop=True)


def gap_series(panel, origin, sids):
    """Series with no row on any origin of the window but a row after it (the known issue)."""
    o = pd.Timestamp(origin)
    days = pd.date_range(o - pd.Timedelta(days=WINDOW_DAYS), o)
    return {s for s in sids for d in days
            if d not in panel._raw_by[s].index and panel._raw_by[s].index.max() > d >= panel._raw_by[s].index.min()}


@pytest.mark.parametrize("mode", ["x3", "delete"])
@pytest.mark.parametrize("origin", ORIGINS)
def test_no_lookahead(panel, built, series, tmp_path, origin, mode):
    bad = tampered_panel(built, tmp_path, origin, mode)
    sids = series if mode == "x3" else sorted(set(series) - gap_series(panel, origin, series))
    assert len(sids) >= 4
    for name, spec in SPECS.items():
        a, b = forecast(spec, panel, origin, sids), forecast(spec, bad, origin, sids)
        assert len(a) and (a.origin_date == origin).any(), name
        pd.testing.assert_frame_equal(a, b, check_exact=True, obj=f"{name} @ {origin} ({mode})")


@pytest.mark.xfail(strict=True, reason="data.Panel forward-fills to the last raw row, so the existence of a "
                   "row after the origin lengthens the history; fix belongs in data.py (not editable overnight)")
def test_trailing_fill_depends_on_future_rows(panel, built, tmp_path):
    origin = "2026-10-30"
    sids = sorted(gap_series(panel, origin, panel.series_ids()))
    assert sids, "no series with a gap in the window"
    bad = tampered_panel(built, tmp_path, origin, "delete")
    a = forecast({"models": [{"name": "drift"}]}, panel, origin, sids)
    b = forecast({"models": [{"name": "drift"}]}, bad, origin, sids)
    pd.testing.assert_frame_equal(a, b, check_exact=True)
