"""DEV-only EDA: does the GetDeploying weekly median predict the direction of our series' next move?
Run from gpu_scientist/: PYTHONPATH=. python scratch/dev_aggregator_eda.py   (DEV origins only; never HOLDOUT/TEST)

Mapping (stated in FINDINGS_devin.md): same GPU (GetDeploying does not split SXM/PCIe or 40/80GB, so all
A100 and H100 variants map to its single A100 / H100 line) and pricing mode = our pricing_tier
(on_demand rate cards <-> on_demand; neocloud_spot, hyperscaler_spot and marketplace_ask spot <-> spot).
Availability: a Monday-dated week is the median of that week's daily captures and is provisional until
Sunday, so it is used from the following Monday (week_start + 7 days) on; LAG adds extra days of
publication lag as a sensitivity check.
"""
import sys
import numpy as np, pandas as pd
from scipy.stats import spearmanr
sys.path.insert(0, ".")
import config as C, data
from models.m_aggregator import agg_series, agg_key, provider_change

s, c = data.build(); P = data.Panel.load(s, c)
sids = P.series_ids()
dev = pd.date_range(*C.DEV_ORIGINS)
fc = pd.read_csv(C.ROOT / "experiments_final/exp_007/forecast_all.csv.gz", parse_dates=["origin_date"])
fc = fc.set_index(["series_id", "origin_date", "horizon_days"])

def rows(lag=0, col="median_usd_per_gpu_hour"):
    out = []
    for sid in sids:
        m = P.meta(sid); key = agg_key(m)
        if key is None:
            continue
        a = agg_series(*key, col=col, lag=lag)
        pch = provider_change(*key, lag=lag)
        full = P.daily[sid]
        # gap at every day up to the last DEV origin, for a trailing-median "normal gap"
        days = pd.date_range("2026-07-01", dev[-1])
        av = a.reindex(days, method="ffill")
        g = np.log(av / full.reindex(days)).dropna()
        for o in dev:
            if o not in g.index or P.truth(sid, o) is None and len(P.upto(sid, o)) == 0:
                continue
            h = P.upto(sid, o)
            if not len(h) or h.index[-1] != o:
                continue                                  # origin not collected
            last = float(h.iloc[-1]); gap = g.loc[o]
            past = g.loc[o - pd.Timedelta(days=56):o - pd.Timedelta(days=1)]
            dgap = gap - past.median() if len(past) >= 28 else np.nan
            wk = a.loc[:o]
            dagg = np.log(wk.iloc[-1] / wk.iloc[-2]) if len(wk) >= 2 else np.nan
            npch = bool(pch.get(wk.index[-1], False))
            for hz in C.HORIZONS:
                y = P.truth(sid, o + pd.Timedelta(days=hz))
                if y is None:
                    continue
                q50 = fc.q50.get((sid, o, hz), np.nan)
                out.append(dict(sid=sid, cls=m["instrument_class"], src=m["source_id"], h=hz, gap=gap, dgap=dgap,
                                dagg=dagg, npch=npch, o=o, r=np.log(y / last), res=np.log(y / q50)))
    return pd.DataFrame(out)

def summarise(d, sig):
    d = d.dropna(subset=[sig])
    mv = d[d.r != 0]
    hit = (np.sign(mv[sig]) == np.sign(mv.r)).mean()
    up = d[d[sig] > 0.02]; dn = d[d[sig] < -0.02]
    rho_r = spearmanr(d[sig], d.r).statistic
    rho_res = spearmanr(d[sig], d.res, nan_policy="omit").statistic
    per = d.groupby("sid").apply(lambda g: spearmanr(g[sig], g.res, nan_policy="omit").statistic if g[sig].nunique() > 1 and g.res.nunique() > 1 else np.nan)
    return dict(n=len(d), n_series=d.sid.nunique(), moves=len(mv), hit_rate=round(hit, 3),
                p_up_if_above=round((up.r > 0).mean(), 3), p_dn_if_above=round((up.r < 0).mean(), 3), n_above=len(up),
                p_dn_if_below=round((dn.r < 0).mean(), 3), p_up_if_below=round((dn.r > 0).mean(), 3), n_below=len(dn),
                spearman_r=round(rho_r, 3), spearman_resid_vs_exp007=round(rho_res, 3),
                series_resid_corr_pos=f"{int((per > 0).sum())}/{int(per.notna().sum())}")

if __name__ == "__main__":
    d = rows()
    print("matched series:", d.sid.nunique(), "of", len(sids))
    print(d.groupby(["src", "cls"]).sid.nunique().to_string())
    for sig in ("gap", "dgap", "dagg"):
        print(f"\n== signal {sig} (all horizons)"); print(summarise(d, sig))
        for hz in C.HORIZONS:
            print(f"  h={hz}", summarise(d[d.h == hz], sig))
        for cls, g in d.groupby("cls"):
            print(f"  {cls:20s}", summarise(g, sig))
    for lag, col in ((7, "median_usd_per_gpu_hour"), (0, "provider_median_usd_per_gpu_hour")):
        print(f"\n== sensitivity lag={lag} col={col}")
        e = rows(lag, col)
        for sig in ("gap", "dgap"):
            print(" ", sig, summarise(e, sig))
