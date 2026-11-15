"""2-3 year value view for H100 and A100 (rental and resale kept separate).

Not a fitted model: three explicit scenarios (low / base / high), each a constant
annual rate applied to a dated anchor. Every anchor and rate is written below with
its source so the numbers can be argued with. Run:

    python -m gpu_scientist.long_horizon        # writes long_horizon.json + long_horizon.png

Pack inputs (if present) are read only to print the cross-checks in LONG_HORIZON.md;
the scenario table itself depends only on the constants below.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "long_horizon.json"
OUT_PNG = HERE / "long_horizon.png"

# Anchor date for everything: the forecast origin of the short-horizon task.
ANCHOR = "2026-11"
YEARS = {"2027-11": 1, "2028-11": 2, "2029-11": 3}

# ---------- Rental: USD per GPU-hour, "market midpoint" ----------
# Midpoint = between spot and on-demand, close to 1-month / 12-month reserved.
# H100: GetDeploying medians week of 2026-11-02 (pack aggregator_medians.csv):
#       spot 2.52, reserved_1m 3.36, reserved_12m 3.21, on_demand 4.02;
#       Ornn OCPI-H100 2.92 on 2026-10-01; SemiAnalysis 1-yr contract ~2.80 (Oct 2026).
# A100: GetDeploying spot 1.51, reserved_1m 1.70, reserved_12m 1.68, on_demand 1.99;
#       Akash 80GB average 1.54 (Aug 2026).
RENTAL_ANCHOR = {"H100": 3.00, "A100": 1.65}
# Annual change. Reasons in LONG_HORIZON.md sections 3 and 4.
RENTAL_RATE = {
    "H100": {"low": -0.35, "base": -0.12, "high": +0.03},
    "A100": {"low": -0.40, "base": -0.15, "high": 0.00},
}
# Cash operating cost per GPU-hour (power at PUE 1.3, $0.08/kWh, colocation ~$150/kW-month,
# share of network/ops). Below this an owner idles the GPU instead of renting it.
CASH_FLOOR = {"H100": 0.35, "A100": 0.25}

# ---------- Resale: USD per used SXM module, typical realized sale ----------
# American Compute October 2026 Rack Report (data through Aug 2026):
#   H100 SXM 80GB realized 14,250 (p25 13,200; dealer ask 16,576 = 1.16x);
#   HGX 8xH100 node 195,000 (24,400/GPU).
#   A100 SXM4 80GB realized ~5,400 (range 4,700-5,400, down ~35% y/y);
#   HGX 8xA100 80GB node 95,200 (11,900/GPU).
RESALE_ANCHOR = {"H100": 14250, "A100": 5400}
RESALE_RATE = {
    "H100": {"low": -0.50, "base": -0.25, "high": -0.08},
    "A100": {"low": -0.55, "base": -0.30, "high": -0.10},
}
NODE_PER_GPU = {"H100": 24400, "A100": 11900}  # whole-node resale per GPU, same report
UTIL = 0.70  # assumed sold utilisation for the cash-flow cross-check

# ---------- Capability (pack capability_units.csv, inference, A100 SXM 80GB = 1.0) ----------
CAPABILITY = {"A100": 1.0, "H100": 2.465, "H200": 2.716, "B200": 7.915}
# GetDeploying reserved_1m medians, week of 2026-11-02 (pack)
RES1M = {"A100": 1.6962, "H100": 3.36, "H200": 3.9536, "B200": 8.0925}


# ---------- Market-implied path (Silicon Data 36-month forwards vs spot, 2026-09-03,
# as reported by the Compute-and-LLM dashboard): A100 -24.9%, H100 -12.3% over 36 months.
FORWARD_36M = {"H100": -0.123, "A100": -0.249}

# ---------- Ages used for the cross-sectional age curve (CCIR, 2026-09-28, +0.1y to Nov) ----------
AGE = {"NVIDIA A100": 5.9, "NVIDIA H100": 3.9, "NVIDIA H200": 2.3, "NVIDIA B200": 1.6}
# Performance parity of A100 vs H100: compute (pack MLPerf units) and memory bandwidth (datasheet, pack)
PARITY_A100_H100 = {"compute_mlperf": round(1 / 2.465, 2), "memory_bandwidth": round(1 / 1.643, 2)}


def pack_tests() -> dict | None:
    """H1 (cross-section = cohort decline?) and H3 (A100 converging to parity?) on the pack's
    GetDeploying weekly medians, Nov 2025 -> Nov 2026 (first and last 4 weeks averaged)."""
    import numpy as np
    import pandas as pd
    try:
        from .config import PACK
    except Exception:
        return None
    f = PACK / "aggregator_medians.csv"
    if not f.exists():
        return None
    a = pd.read_csv(f)
    out = {}
    for m in ("on_demand", "reserved_1m", "reserved_12m", "spot"):
        s = a[(a.pricing_mode == m) & a.gpu_model.isin(AGE)]
        p = s.pivot_table(index="week_start", columns="gpu_model",
                          values="median_usd_per_gpu_hour").sort_index()
        start, end = p.iloc[:4].mean(), p.iloc[-4:].mean()
        e = end.dropna()
        slope = np.polyfit([AGE[g] for g in e.index], np.log(e.values), 1)[0]
        out[m] = {
            "cross_section_change_per_year_of_age": round(float(np.exp(slope) - 1), 3),
            "cohort_change_over_year": {g.split()[-1]: round(float(end[g] / start[g] - 1), 3)
                                        for g in ("NVIDIA A100", "NVIDIA H100")},
            "a100_over_h100": [round(float(start["NVIDIA A100"] / start["NVIDIA H100"]), 2),
                               round(float(end["NVIDIA A100"] / end["NVIDIA H100"]), 2)],
            "n_providers_last_week": {g.split()[-1]: int(s[(s.gpu_model == g)].sort_values("week_start")
                                                         .n_providers.iloc[-1])
                                      for g in ("NVIDIA A100", "NVIDIA H100")},
        }
    return out


# ---------- CCIR daily print 2026-11-14, posted asks, guaranteed on-demand, US & Europe, panel median ----------
CCIR = {"A100": {"hyperscaler": 4.45, "neocloud": 2.12, "marketplace": 1.08, "neocloud_interruptible": 1.20},
        "H100": {"hyperscaler": 11.25, "neocloud": 3.37, "marketplace": 2.60, "neocloud_interruptible": 2.15}}

# ---------- Electricity (BLS CPI electricity index, +4.4% in the 12 months to Sep 2026,
# +5.1% in the 12 months to Sep 2025). Household index; data centres buy at commercial or industrial rates.
POWER = {"kw": {"H100": 0.70, "A100": 0.40}, "pue": 1.3, "usd_per_kwh": 0.08}


def electricity_sensitivity() -> dict:
    """How much of the cash floor is electricity, and what 3 years of +5%/yr or a doubling would add."""
    out = {}
    for g in ("H100", "A100"):
        e = POWER["kw"][g] * POWER["pue"] * POWER["usd_per_kwh"]
        out[g] = {"electricity_usd_per_hr": round(e, 3),
                  "share_of_floor": round(e / CASH_FLOOR[g], 2),
                  "floor_after_3y_at_+5pct": round(CASH_FLOOR[g] + e * (1.05 ** 3 - 1), 3),
                  "floor_if_power_doubles": round(CASH_FLOOR[g] + e, 3)}
    return out


def ccir_check() -> dict:
    """Where our posted-price anchor sits among CCIR's provider tiers, and A100/H100 by tier."""
    out = {}
    for g in ("H100", "A100"):
        t = CCIR[g]
        out[g] = {"anchor": RENTAL_ANCHOR[g],
                  "between_marketplace_and_neocloud": t["marketplace"] <= RENTAL_ANCHOR[g] <= t["neocloud"]}
    out["a100_over_h100_by_tier"] = {k: round(CCIR["A100"][k] / CCIR["H100"][k], 2) for k in CCIR["A100"]}
    return out


def path(anchor: float, rate: float, floor: float | None = None) -> dict:
    out = {ANCHOR: round(anchor, 2)}
    for label, n in YEARS.items():
        v = anchor * (1 + rate) ** n
        if floor is not None:
            v = max(v, floor)
        out[label] = round(v, 2)
    return out


def build() -> dict:
    res = {"anchor": ANCHOR, "rental_usd_per_gpu_hour": {}, "resale_usd_per_module": {},
           "cross_checks": {}}
    for g in ("H100", "A100"):
        res["rental_usd_per_gpu_hour"][g] = {
            s: path(RENTAL_ANCHOR[g], r, CASH_FLOOR[g]) for s, r in RENTAL_RATE[g].items()}
        res["resale_usd_per_module"][g] = {
            s: {k: int(round(v, -2)) for k, v in path(RESALE_ANCHOR[g], r).items()}
            for s, r in RESALE_RATE[g].items()}
    # 1) price per unit of capability today: older generations pay a premium
    res["cross_checks"]["usd_per_capability_unit_res1m"] = {
        g: round(RES1M[g] / CAPABILITY[g], 3) for g in CAPABILITY}
    # 2) resale as a multiple of one year of net rental cash (node basis)
    mult = {}
    for g in ("H100", "A100"):
        net = (RENTAL_ANCHOR[g] * UTIL - CASH_FLOOR[g]) * 8760
        mult[g] = {"net_cash_per_gpu_year": int(round(net, -2)),
                   "node_resale_per_gpu": NODE_PER_GPU[g],
                   "years_of_net_cash": round(NODE_PER_GPU[g] / net, 2)}
        # same multiple in the base case at +2y
        r2 = res["rental_usd_per_gpu_hour"][g]["base"]["2028-11"]
        m2 = res["resale_usd_per_module"][g]["base"]["2028-11"]
        net2 = (r2 * UTIL - CASH_FLOOR[g]) * 8760
        node2 = m2 * NODE_PER_GPU[g] / RESALE_ANCHOR[g]
        mult[g]["base_2028_years_of_net_cash"] = round(node2 / net2, 2)
    res["cross_checks"]["resale_vs_rent"] = mult
    res["market_forward_2029"] = {g: round(RENTAL_ANCHOR[g] * (1 + FORWARD_36M[g]), 2) for g in FORWARD_36M}
    res["parity_a100_over_h100"] = PARITY_A100_H100
    res["pack_tests"] = pack_tests()
    res["ccir_check"] = ccir_check()
    res["electricity_sensitivity"] = electricity_sensitivity()
    return res


def plot(res: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, grid = "#14213D", "#5A6275", "#E3DFD4"
    col = {"H100": "#2F6FCC", "A100": "#D9822B"}
    xs = [ANCHOR] + list(YEARS)
    xl = ["Nov 2026", "Nov 2027", "Nov 2028", "Nov 2029"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), facecolor="#F7F5EF")
    panels = [("rental_usd_per_gpu_hour", "Rental, USD per GPU-hour (market midpoint)", "${:.2f}"),
              ("resale_usd_per_module", "Resale, USD per used SXM module (realized)", "${:,.0f}")]
    for ax, (key, title, fmt) in zip(axes, panels):
        ax.set_facecolor("#F7F5EF")
        for g in ("H100", "A100"):
            d = res[key][g]
            lo = [d["low"][x] for x in xs]; hi = [d["high"][x] for x in xs]; b = [d["base"][x] for x in xs]
            ax.fill_between(range(4), lo, hi, color=col[g], alpha=0.15, linewidth=0)
            ax.plot(range(4), b, color=col[g], lw=2, marker="o", ms=5)
            below = key.startswith("rental") and g == "A100"
            ax.annotate(f"{g} base {fmt.format(b[2])} (2028)", (2, b[2]), xytext=(-8, -24) if below else (6, 8), ha="right" if below else "left",
                        textcoords="offset points", color=ink, fontsize=9)
            if key.startswith("rental"):
                fv = res["market_forward_2029"][g]
                ax.plot([3], [fv], marker="D", ms=7, mfc="none", mec=col[g], mew=1.6)
                ax.annotate("forward", (3, fv), xytext=(8, 2), textcoords="offset points",
                            color=muted, fontsize=8.5)
            ax.annotate(f"{g}", (3, b[3]), xytext=(8, -3), textcoords="offset points",
                        color=ink, fontsize=10, weight="bold")
        ax.set_xticks(range(4), xl, color=muted, fontsize=9)
        ax.tick_params(axis="y", colors=muted, labelsize=9)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _, f=fmt: f.format(v)))
        ax.set_ylim(bottom=0)
        ax.set_xlim(-0.2, 3.6)
        ax.grid(axis="y", color=grid, lw=0.8)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(grid)
        ax.set_title(title, loc="left", color=ink, fontsize=11)
    fig.text(0.01, 0.01, "Line = base case; band = low to high scenario; hollow diamond = market forward "
             "(Silicon Data 36-month, Sep 2026). Rental and resale are separate markets.", color=muted, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT_PNG, dpi=160)


if __name__ == "__main__":
    r = build()
    OUT_JSON.write_text(json.dumps(r, indent=2))
    if os.environ.get("NO_PLOT") != "1":
        plot(r)
    print(json.dumps(r, indent=2))
