"""Data layer: builds the official series with the starter kit, and gives leak-free slices.

Every model sees only `Ctx.hist` (values dated on or before the origin) and
`Ctx.peer(...)` (other series, also cut at the origin). Nothing here can return a
value dated after the origin.
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

import config as C


def build(force: bool = False, cutoff: str | None = None) -> tuple:
    """Run the starter kit's build_series.py (rental series only; AWS spot is not scored on Sunday).

    Without cutoff: the full file (truth for dev/holdout backtests).
    With cutoff: the truncated history used for the frozen submission.
    """
    C.WORK.mkdir(parents=True, exist_ok=True)
    tag = f"_cut{cutoff}" if cutoff else ""
    series = C.WORK / f"series_daily{tag}.csv"
    catalog = C.WORK / f"series_catalog{tag}.csv"
    if force or not series.exists():
        cmd = [sys.executable, "-B", str(C.STARTER / "build_series.py"), "--pack", str(C.PACK), "--no-aws",
               "--out", str(series), "--catalog", str(catalog), "--report", str(C.WORK / f"build{tag}.json")]
        cmd += ["--cutoff", cutoff] if cutoff else ["--as-of", C.CUTOFF]
        subprocess.run(cmd, check=True)
    return series, catalog


@dataclass
class Panel:
    raw: pd.DataFrame                      # official rows: series_id, date, value, n_providers, ...
    catalog: pd.DataFrame
    daily: dict = field(default_factory=dict)  # series_id -> daily as-of (forward-filled) pd.Series

    @classmethod
    def load(cls, series_csv, catalog_csv) -> "Panel":
        raw = pd.read_csv(series_csv, parse_dates=["date"]).sort_values(["series_id", "date"])
        cat = pd.read_csv(catalog_csv)
        p = cls(raw=raw, catalog=cat)
        for sid, g in raw.groupby("series_id"):
            s = g.set_index("date")["value"]
            p.daily[sid] = s.reindex(pd.date_range(s.index.min(), s.index.max())).ffill()
        p._raw_by = {sid: g.set_index("date") for sid, g in raw.groupby("series_id")}
        p._meta = {sid: {**m, "series_id": sid} for sid, m in cat.set_index("series_id").to_dict("index").items()}
        return p

    def series_ids(self, tier: str | None = C.TIER) -> list[str]:
        c = self.catalog if tier is None else self.catalog[self.catalog.tier == tier]
        return sorted(c.series_id)

    def meta(self, sid: str) -> dict:
        return self._meta[sid]

    def upto(self, sid: str, origin: pd.Timestamp) -> pd.Series:
        """Daily as-of history up to the last day actually collected on or before the origin.
        It never forward-fills past that day: whether a later row exists must not change the
        history (that leaked; see tests/test_no_lookahead.py), and live, at the cutoff, there is
        no later row either."""
        s = self.daily.get(sid)
        if s is None:
            return pd.Series(dtype=float)
        idx = self._raw_by[sid].index
        seen = idx[idx <= origin]
        return s.loc[:seen.max()] if len(seen) else s.iloc[:0]

    def raw_upto(self, sid: str, origin: pd.Timestamp) -> pd.DataFrame:
        return self._raw_by[sid].loc[:origin]

    def truth(self, sid: str, date: pd.Timestamp):
        """Observed value exactly on `date` (None if that day was not collected). Same rule as the scorer."""
        g = self._raw_by.get(sid)
        if g is None or date not in g.index:
            return None
        return float(g.at[date, "value"])


@dataclass
class Ctx:
    """What a model is allowed to see when forecasting `sid` from `origin`."""
    sid: str
    origin: pd.Timestamp
    meta: dict
    hist: pd.Series            # daily as-of values, index <= origin
    panel: Panel

    @property
    def last(self) -> float:
        return float(self.hist.iloc[-1])

    def raw(self) -> pd.DataFrame:
        return self.panel.raw_upto(self.sid, self.origin)

    def peers(self, same: str = "gpu_model") -> dict:
        """Other series sharing `same` (e.g. the same GPU in other collectors), cut at the origin."""
        key = self.meta.get(same)
        out = {}
        for sid, m in self.panel._meta.items():
            if sid != self.sid and m.get(same) == key:
                h = self.panel.upto(sid, self.origin)
                if len(h):
                    out[sid] = h
        return out


def log_changes(hist: pd.Series, h: int, window: int | None = None) -> np.ndarray:
    """h-day log changes of a daily as-of series, using anchor days in the last `window` days."""
    v = np.log(hist.values.astype(float))
    if window is not None:
        v = v[-(window + h):]
    if len(v) <= h:
        return np.array([])
    return v[h:] - v[:-h]


def days_since_change(hist: pd.Series) -> int:
    v = hist.values
    idx = np.nonzero(v[1:] != v[:-1])[0]
    return len(v) - 1 - (idx[-1] + 1) if len(idx) else len(v)
