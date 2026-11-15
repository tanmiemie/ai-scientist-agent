"""The fast loop: walk forward one day at a time, as if live.

At each origin the pipeline
  1. learns from every earlier forecast whose target date has now arrived
     (ensemble weights and interval calibration are updated from the realised errors),
  2. asks every model in the spec for a forecast using data up to the origin only,
  3. combines them (weighted in log space) and applies the learned calibration.

A spec (JSON) looks like:
{
  "models":    [{"name": "trend_tail", "params": {"window": 60}}, {"name": "step_hazard"}],
  "combine":   {"method": "hedge", "eta": 2.0, "group_by": "instrument_class"},
  "calibrate": {"enabled": true, "gamma": 0.5, "scale": 0.01, "group_by": "instrument_class"}
}
combine.method: "single" (first model only), "mean" (equal weights) or "hedge" (weights follow
recent pinball loss). group_by: "all", "source_class" or any catalog column.
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np
import pandas as pd

import models as M
from data import Ctx, Panel

QS = (0.1, 0.5, 0.9)


def cell_loss(y, q):
    return float(np.mean([max(t * (y - f), (t - 1) * (y - f)) for t, f in zip(QS, q)]))


def group_key(meta: dict, how: str) -> str:
    if how == "all":
        return "all"
    if how == "source_class":
        return f"{meta['source_id']}|{meta['instrument_class']}"
    return str(meta.get(how))


def run(spec: dict, panel: Panel, origins, series_ids, horizons=(1, 3, 7)):
    mods = [M.make(m["name"], m.get("params")) for m in spec["models"]]
    labels = [m.get("label", m["name"]) for m in spec["models"]]
    comb = {"method": "single", "eta": 2.0, "group_by": "instrument_class", **spec.get("combine", {})}
    cal = {"enabled": False, "gamma": 0.5, "scale": 0.01, "group_by": "instrument_class", **spec.get("calibrate", {})}
    n = len(mods)

    weights = defaultdict(lambda: np.ones(n) / n)
    d_up = defaultdict(float)   # learned widening of the upper edge, in log units
    d_dn = defaultdict(float)
    pending = []                # forecasts waiting for their target date
    rows, model_rows = [], []

    for o in pd.DatetimeIndex(origins):
        # 1. feedback from targets that are now in the past
        still = []
        for it in pending:
            if it["target"] > o:
                still.append(it)
                continue
            y = panel.truth(it["sid"], it["target"])
            if y is None:
                continue
            gk, ck, h = it["gk"], it["ck"], it["h"]
            if comb["method"] == "hedge" and n > 1:
                losses = np.array([cell_loss(y, q) / y for q in it["per_model"]])
                w = weights[(gk, h)] * np.exp(-comb["eta"] * losses / max(cal["scale"], 1e-9))
                weights[(gk, h)] = w / w.sum() if w.sum() > 0 else np.ones(n) / n
            if cal["enabled"]:
                q10, _, q90 = it["final"]
                d_up[(ck, h)] += cal["gamma"] * cal["scale"] * ((y > q90) - 0.1)
                d_dn[(ck, h)] += cal["gamma"] * cal["scale"] * ((y < q10) - 0.1)
        pending = still

        # 2-3. forecast every series from this origin
        for sid in series_ids:
            hist = panel.upto(sid, o)
            if len(hist) < 10:
                continue
            meta = panel.meta(sid)
            ctx = Ctx(sid=sid, origin=o, meta=meta, hist=hist, panel=panel)
            per = []
            for m in mods:
                try:
                    per.append(m.predict(ctx, horizons))
                except Exception as e:  # a broken model must not stop the loop
                    per.append({})
                    print(f"[warn] {m.name} failed on {sid} @ {o.date()}: {e}")
            gk, ck = group_key(meta, comb["group_by"]), group_key(meta, cal["group_by"])
            for h in horizons:
                qs = [p.get(h) or (ctx.last,) * 3 for p in per]
                if comb["method"] == "single":
                    w = np.eye(n)[0]
                elif comb["method"] == "mean":
                    w = np.ones(n) / n
                else:
                    w = weights[(gk, h)]
                logq = np.log(np.array(qs)).T @ w            # weighted average of each quantile in log space
                c = logq[1]
                lo, hi = logq[0], logq[2]
                if cal["enabled"]:
                    hi, lo = hi + d_up[(ck, h)], lo - d_dn[(ck, h)]
                lo, hi = min(lo, c), max(hi, c)
                final = (float(np.exp(lo)), float(np.exp(c)), float(np.exp(hi)))
                target = o + pd.Timedelta(days=h)
                rows.append(dict(series_id=sid, origin_date=o.date().isoformat(), horizon_days=h,
                                 q10=final[0], q50=final[1], q90=final[2], target_date=target.date().isoformat()))
                for lab, q, wi in zip(labels, qs, w):
                    model_rows.append(dict(series_id=sid, origin_date=o.date().isoformat(), horizon_days=h,
                                           model=lab, q10=q[0], q50=q[1], q90=q[2], weight=float(wi)))
                pending.append(dict(sid=sid, target=target, h=h, gk=gk, ck=ck, per_model=qs, final=final))

    state = {"weights": {f"{k[0]}|h{k[1]}": dict(zip(labels, map(float, v))) for k, v in weights.items()},
             "calibration_up": {f"{k[0]}|h{k[1]}": v for k, v in d_up.items()},
             "calibration_dn": {f"{k[0]}|h{k[1]}": v for k, v in d_dn.items()}}
    return pd.DataFrame(rows), pd.DataFrame(model_rows), state
