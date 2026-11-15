"""Error diagnosis ("health check") on DEV origins only. This is what the research agent reads
to decide the next hypothesis. Everything is computed by code, not guessed.

Sections:
  1. bias and interval misses by series group and horizon
  2. worst and best series
  3. misses by state at the origin (days since last price change, provider count change)
  4. each base model's own skill per group (which model works where)
  5. co-movement of the same GPU across collectors (candidate leading signals)
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from data import Panel, days_since_change
from online import cell_loss


def _group_table(df, by):
    g = df.groupby(by)
    return pd.DataFrame({
        "n": g.size(),
        "skill": 1 - g.loss.sum() / g.baseline_loss.sum(),
        "y_above_q50": g.apply(lambda x: (x.y > x.q50).mean(), include_groups=False),
        "above_q90": g.apply(lambda x: (x.y > x.q90).mean(), include_groups=False),
        "below_q10": g.apply(lambda x: (x.y < x.q10).mean(), include_groups=False),
        "mean_log_err_q50": g.apply(lambda x: np.log(x.y / x.q50).mean(), include_groups=False),
    }).round(3)


def run(cells_csv, model_rows: pd.DataFrame, panel: Panel, dev_window) -> tuple[dict, str]:
    cells = pd.read_csv(cells_csv)
    cells = cells[cells.status == "scored"].copy()
    meta = panel.catalog.set_index("series_id")
    cells["group"] = cells.series_id.map(lambda s: f"{meta.at[s, 'source_id']}|{meta.at[s, 'instrument_class']}")
    cells["origin"] = pd.to_datetime(cells.origin_date)

    # state at origin
    def state(r):
        hist = panel.upto(r.series_id, r.origin)
        raw = panel.raw_upto(r.series_id, r.origin)
        prov = raw.n_providers.values
        return pd.Series({"days_since_change": days_since_change(hist),
                          "provider_change_7d": float(prov[-1] - prov[-8]) if len(prov) > 8 else 0.0})
    cells = pd.concat([cells, cells.apply(state, axis=1)], axis=1)
    cells["dsc_bucket"] = pd.cut(cells.days_since_change, [-1, 1, 3, 7, 30, 10_000],
                                 labels=["0-1", "2-3", "4-7", "8-30", ">30"])
    cells["prov_bucket"] = np.sign(cells.provider_change_7d).map({-1: "fewer", 0: "same", 1: "more"})

    by_group = _group_table(cells, ["group"])
    by_h = _group_table(cells, ["horizon_days"])
    by_dsc = _group_table(cells, ["dsc_bucket"])
    by_prov = _group_table(cells, ["prov_bucket"])
    per_series = _group_table(cells, ["series_id"]).sort_values("skill")

    # per-model skill (each base model scored alone on the same cells)
    mr = model_rows.copy()
    mr = mr[(mr.origin_date >= dev_window[0]) & (mr.origin_date <= dev_window[1])]
    mr = mr.merge(cells[["series_id", "origin_date", "horizon_days", "y", "baseline_loss", "group"]],
                  on=["series_id", "origin_date", "horizon_days"])
    if len(mr):
        mr["loss"] = [cell_loss(y, (a, b, c)) for y, a, b, c in zip(mr.y, mr.q10, mr.q50, mr.q90)]
        g = mr.groupby(["group", "model"])
        per_model = (1 - g.loss.sum() / g.baseline_loss.sum()).unstack().round(3)
        mean_w = mr.groupby(["group", "model"]).weight.mean().unstack().round(2)
    else:
        per_model = mean_w = pd.DataFrame()

    # co-movement of the same GPU across collectors (daily log changes, dev period)
    lo, hi = pd.Timestamp(dev_window[0]) - pd.Timedelta(days=60), pd.Timestamp(dev_window[1])
    scored = set(cells.series_id)
    lead = []
    for sid in sorted(scored):
        m = panel.meta(sid)
        a = np.log(panel.daily[sid].loc[lo:hi]).diff()
        for other, om in panel._meta.items():
            if other == sid or om.get("gpu_model") != m.get("gpu_model") or other not in panel.daily:
                continue
            b = np.log(panel.daily[other].loc[lo:hi]).diff()
            best = None
            for lag in range(1, 6):          # does `other` move `lag` days before `sid`?
                x = pd.concat([a, b.shift(lag)], axis=1).dropna()
                if len(x) < 30 or x.iloc[:, 0].std() == 0 or x.iloc[:, 1].std() == 0:
                    continue
                cor = x.corr().iloc[0, 1]
                if best is None or abs(cor) > abs(best[1]):
                    best = (lag, cor)
            if best and abs(best[1]) >= 0.3:
                lead.append({"series": sid, "leader": other, "lag_days": best[0], "corr": round(best[1], 3)})
    lead = sorted(lead, key=lambda d: -abs(d["corr"]))[:15]

    diag = {
        "n_cells": int(len(cells)),
        "overall": {"skill": round(1 - cells.loss.sum() / cells.baseline_loss.sum(), 4),
                    "y_above_q50": round((cells.y > cells.q50).mean(), 3),
                    "above_q90": round((cells.y > cells.q90).mean(), 3),
                    "below_q10": round((cells.y < cells.q10).mean(), 3)},
        "by_group": by_group.reset_index().to_dict("records"),
        "by_horizon": by_h.reset_index().to_dict("records"),
        "by_days_since_change": by_dsc.reset_index().astype({"dsc_bucket": str}).to_dict("records"),
        "by_provider_change_7d": by_prov.reset_index().to_dict("records"),
        "worst_series": per_series.head(8).reset_index().to_dict("records"),
        "best_series": per_series.tail(5).reset_index().to_dict("records"),
        "per_model_skill_by_group": per_model.reset_index().to_dict("records") if len(per_model) else [],
        "mean_weight_by_group": mean_w.reset_index().to_dict("records") if len(mean_w) else [],
        "candidate_leading_signals": lead,
    }
    md = ["# Diagnosis (dev origins only)", "",
          f"Cells: {diag['n_cells']}. Overall skill {diag['overall']['skill']}; truth above q50 in "
          f"{diag['overall']['y_above_q50']:.0%} of cells (50% if unbiased); above q90 {diag['overall']['above_q90']:.0%} "
          f"and below q10 {diag['overall']['below_q10']:.0%} (10% each if calibrated).", "",
          "## By series group", by_group.to_markdown(), "",
          "## By horizon", by_h.to_markdown(), "",
          "## By days since the last price change at the origin", by_dsc.to_markdown(), "",
          "## By change in provider count over the 7 days before the origin", by_prov.to_markdown(), "",
          "## Worst series", per_series.head(8).to_markdown(), "",
          "## Each base model alone: skill by group", per_model.to_markdown() if len(per_model) else "(single model)", "",
          "## Mean ensemble weight by group", mean_w.to_markdown() if len(mean_w) else "(n/a)", "",
          "## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)",
          pd.DataFrame(lead).to_markdown(index=False) if lead else "(none with |corr| >= 0.3)", ""]
    return diag, "\n".join(md)


def save(diag, md, out_dir):
    (out_dir / "diagnosis.json").write_text(json.dumps(diag, indent=1, default=str))
    (out_dir / "diagnosis.md").write_text(md)
