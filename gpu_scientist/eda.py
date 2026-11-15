"""Data-quality check of the scored series: python eda.py  ->  eda/EDA_tables.json + eda/*.png

Six checks on the 37 headline rental series (built by the starter kit as of 2026-11-06):
  1 missing days        2 spikes and reversals   3 provider counts
  4 rows dropped by the pack's build              5 stale series
  6 the same GPU across collectors (levels and units)
Uses only the pack. The write-up with conclusions is EDA.md.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

import config as C
import data

OUT = C.ROOT / "eda"
INK, PAPER, MUTED, AMBER, BLUE, GRID = "#14213D", "#F7F5EF", "#4A5568", "#D9822B", "#2F6FCC", "#D9D4C7"


def main():
    OUT.mkdir(exist_ok=True)
    series_csv, catalog_csv = data.build()
    s = pd.read_csv(series_csv, parse_dates=["date"]).sort_values(["series_id", "date"])
    cat = pd.read_csv(catalog_csv)
    head = cat[cat.tier == C.TIER].set_index("series_id")
    h = s[s.series_id.isin(head.index)].copy()
    cutoff = pd.Timestamp(C.CUTOFF)
    T = {}

    # 1 missing days ---------------------------------------------------------------
    rows = []
    for sid, g in h.groupby("series_id"):
        d = g.date
        span = pd.date_range(d.min(), d.max())
        missing = span.difference(d)
        gaps = np.diff(d.values).astype("timedelta64[D]").astype(int) - 1
        rows.append({"series_id": sid, "source": sid.split(".")[0], "first": d.min().date(), "last": d.max().date(),
                     "days_observed": len(d), "days_missing": len(missing), "longest_gap": int(gaps.max()) if len(gaps) else 0,
                     "missing_in_last_60d": int(sum(m >= cutoff - pd.Timedelta(days=60) for m in missing))})
    miss = pd.DataFrame(rows)
    T["missing_by_source"] = miss.groupby("source").agg(series=("series_id", "size"), first=("first", "min"),
        median_days=("days_observed", "median"), missing_days_total=("days_missing", "sum"),
        longest_gap=("longest_gap", "max"), missing_last_60d=("missing_in_last_60d", "sum")).reset_index().astype(str).to_dict("records")
    T["missing_dates_gpurentalprices_last60d"] = sorted({str(m.date()) for sid, g in h[h.series_id.str.startswith("gpurentalprices")].groupby("series_id")
        for m in pd.date_range(g.date.min(), g.date.max()).difference(g.date) if m >= cutoff - pd.Timedelta(days=60)})

    # 2 spikes and reversals ----------------------------------------------------------
    h["lr"] = h.groupby("series_id").value.transform(lambda v: np.log(v).diff())
    h["dprov"] = h.groupby("series_id").n_providers.diff()
    ch = h[h.lr.notna() & (h.lr != 0)].copy()
    big = ch[ch.lr.abs() >= 0.10]
    rev = 0
    for _, r in big.iterrows():   # a big move undone by at least half within 7 days
        after = h[(h.series_id == r.series_id) & (h.date > r.date) & (h.date <= r.date + pd.Timedelta(days=7))]
        if len(after) and np.sign(after.lr.sum()) == -np.sign(r.lr) and abs(after.lr.sum()) >= 0.5 * abs(r.lr):
            rev += 1
    T["price_changes"] = {"days_with_a_change": int(len(ch)), "share_of_days_with_a_change": round(len(ch) / h.lr.notna().sum(), 3),
                          "abs_change_p50": round(ch.lr.abs().median(), 4), "abs_change_p90": round(ch.lr.abs().quantile(0.9), 4),
                          "abs_change_p99": round(ch.lr.abs().quantile(0.99), 4), "moves_10pct_or_more": int(len(big)),
                          "of_which_reversed_half_within_7d": rev,
                          "largest_moves": big.reindex(big.lr.abs().sort_values(ascending=False).index).head(8)
                          .assign(pct=lambda x: (np.exp(x.lr) - 1).round(3), date=lambda x: x.date.dt.date.astype(str))
                          [["series_id", "date", "pct", "n_providers", "dprov"]].to_dict("records")}

    # 3 provider counts --------------------------------------------------------------
    pv = h.groupby("series_id").n_providers.agg(["median", "min"])
    T["providers"] = {"series_median_providers_le3": int((pv["median"] <= 3).sum()),
                      "series_median_providers_le5": int((pv["median"] <= 5).sum()),
                      "series_min_providers_1": int((pv["min"] <= 1).sum()), "n_series": int(len(pv)),
                      "share_of_changes_on_a_provider_count_change": round((ch.dprov.fillna(0) != 0).mean(), 3),
                      "share_of_10pct_moves_on_a_provider_count_change": round((big.dprov.fillna(0) != 0).mean(), 3),
                      "median_abs_change_when_providers_change": round(ch[ch.dprov.fillna(0) != 0].lr.abs().median(), 4),
                      "median_abs_change_when_providers_same": round(ch[ch.dprov.fillna(0) == 0].lr.abs().median(), 4)}

    # 4 rows dropped by the build ---------------------------------------------------------
    dp = C.PACK / "rental_observations_dropped_rows_by_source_date.csv"
    if dp.exists():
        d = pd.read_csv(dp)
        T["dropped_rows"] = {"by_reason": d.groupby("reason").rows.sum().sort_values(ascending=False).to_dict(),
                             "by_source": d.groupby("source_id").rows.sum().to_dict(),
                             "max_day": d.groupby(["source_id", "dt"]).rows.sum().sort_values(ascending=False).head(5).reset_index().to_dict("records")}

    # 5 stale series --------------------------------------------------------------------
    last = h.groupby("series_id").date.max()
    lastchg = ch.groupby("series_id").date.max().reindex(last.index)
    T["staleness"] = {"series_not_observed_on_cutoff": sorted(last[last < cutoff].index.tolist()),
                      "days_since_last_change_at_cutoff": (cutoff - lastchg).dt.days.describe().round(1).to_dict(),
                      "series_unchanged_30d_plus": int(((cutoff - lastchg).dt.days >= 30).sum())}

    # 6 same GPU across collectors -------------------------------------------------------
    lv = h[h.date == cutoff].set_index("series_id").value
    m = head.loc[lv.index, ["source_id", "instrument_class", "gpu_model", "pricing_tier"]].assign(price=lv)
    m["gpu"] = m.gpu_model.str.replace("_", " ")
    T["levels_at_cutoff"] = m.sort_values(["gpu", "instrument_class", "source_id"])[["gpu", "instrument_class", "source_id", "price"]].round(3).to_dict("records")
    T["price_range_usd_per_gpu_hour"] = [round(float(lv.min()), 3), round(float(lv.max()), 3)]

    (OUT / "EDA_tables.json").write_text(json.dumps(T, indent=1, default=str))

    # figures ----------------------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 20, "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                         "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": PAPER, "axes.facecolor": PAPER})
    # coverage strip: one row per headline series, a mark per observed day since Aug 1
    order = miss.sort_values(["source", "series_id"]).series_id.tolist()
    fig, ax = plt.subplots(figsize=(14, 7.5))
    for i, sid in enumerate(order):
        g = h[(h.series_id == sid) & (h.date >= "2026-08-01")]
        col = {"afhubbard": INK, "fastgpu_daily": BLUE, "gpurentalprices": AMBER}.get(sid.split(".")[0], MUTED)
        ax.scatter(g.date, [i] * len(g), s=9, marker="s", color=col, linewidths=0)
    ax.set_yticks([]); ax.set_ylabel("37 scored series (by collector)")
    import matplotlib.dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([], [], marker="s", ls="", color=c, ms=12, label=l) for c, l in
                       [(INK, "afhubbard"), (BLUE, "fastgpu"), (AMBER, "gpurentalprices")]], frameon=False, loc="center left", fontsize=18)
    ax.set_title("A square = a collected day; white = no data that day", fontsize=20, color=INK)
    fig.tight_layout(); fig.savefig(OUT / "coverage.png", dpi=110); plt.close(fig)
    # change sizes, split by whether the provider count moved the same day
    fig, ax = plt.subplots(figsize=(11, 7.5))
    bins = np.linspace(0, 0.3, 31)
    ax.hist(ch[ch.dprov.fillna(0) == 0].lr.abs().clip(upper=0.3), bins=bins, color=BLUE, alpha=0.85, label="provider count unchanged")
    ax.hist(ch[ch.dprov.fillna(0) != 0].lr.abs().clip(upper=0.3), bins=bins, color=AMBER, alpha=0.85, label="provider count changed")
    ax.set_xlabel("size of a daily price change (|log change|, capped at 0.3)"); ax.set_ylabel("number of changes")
    ax.legend(frameon=False, fontsize=18); fig.tight_layout(); fig.savefig(OUT / "change_sizes.png", dpi=110); plt.close(fig)
    print(json.dumps({k: v for k, v in T.items() if k not in ("levels_at_cutoff",)}, indent=1, default=str))


if __name__ == "__main__":
    main()
