"""Direction B, DEV-only test: does a published market index lead our posted-price series?

For every headline series whose GPU has a GIX daily index (A100, H100, H200, B200, MI300X), at each DEV
origin t we take the index change over the last 7 days, using only prints dated on or before t, and the
series' change from t to t+7. Hypothesis: when the index has risen (fallen) by more than 1%, our series
is more likely to rise (fall) over the next 7 days than when the index is flat."""
import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
import config as C  # noqa: E402
import data  # noqa: E402

idx = pd.read_csv(C.PACK / "index_prints.csv", parse_dates=["print_date"])
idx = idx[idx.index_id.str.startswith("GIX_") & idx.status.isin(["final", "restated"])]
idx = idx.sort_values("print_date").drop_duplicates(["index_id", "print_date"], keep="last")
gix = {g: s.set_index("print_date").value_usd_per_gpu_hour for g, s in idx.groupby("gpu_model")}

panel = data.Panel.load(*data.build())
rows = []
origins = pd.date_range(*C.DEV_ORIGINS)
for sid in panel.series_ids():
    g = str(panel.meta(sid).get("gpu_model", ""))
    key = next((k for k in gix if k in g.replace("NVIDIA ", "").replace("AMD ", "")), None)
    if key is None:
        continue
    s = gix[key]
    for t in origins:
        past = s[s.index <= t]
        past7 = s[s.index <= t - pd.Timedelta(days=7)]
        if len(past) == 0 or len(past7) == 0:
            continue
        sig = np.log(past.iloc[-1] / past7.iloc[-1])
        h = panel.upto(sid, t)
        y = panel.truth(sid, t + pd.Timedelta(days=7))
        if len(h) == 0 or y is None or not np.isfinite(y):
            continue
        rows.append({"series": sid, "gpu": key, "origin": t, "index_7d": sig, "fwd_7d": np.log(y / h.iloc[-1])})

df = pd.DataFrame(rows)
df["index_state"] = np.select([df.index_7d > 0.01, df.index_7d < -0.01], ["up", "down"], "flat")
df["moved"] = np.select([df.fwd_7d > 1e-9, df.fwd_7d < -1e-9], ["up", "down"], "flat")
tab = pd.crosstab(df.index_state, df.moved, normalize="index").round(3)
cnt = df.index_state.value_counts()
corr = df[["index_7d", "fwd_7d"]].corr(method="spearman").iloc[0, 1]
out = {"n_pairs": int(len(df)), "n_series": int(df.series.nunique()), "gpus": sorted(df.gpu.unique()),
       "share_by_index_state": tab.to_dict("index"), "count_by_index_state": cnt.to_dict(),
       "spearman_index7d_vs_fwd7d": round(float(corr), 3)}
print(json.dumps(out, indent=1, default=str))
json.dump(out, open("scratch/index_signal.json", "w"), indent=1, default=str)
