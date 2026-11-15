"""DEV-only: how many non-zero daily moves sit behind the top leading-signal correlations in
experiments_devin/exp_000/diagnosis.md (window = first DEV origin - 60d .. last DEV origin)."""
import json
import numpy as np, pandas as pd
import config as C, data
s, c = data.build(); P = data.Panel.load(s, c)
lo, hi = pd.Timestamp(C.DEV_ORIGINS[0]) - pd.Timedelta(days=60), pd.Timestamp(C.DEV_ORIGINS[1])
diag = json.load(open(C.EXPERIMENTS / "exp_000/diagnosis.json"))
for d in diag["candidate_leading_signals"][:10]:
    a = np.log(P.daily[d["series"]].loc[lo:hi]).diff(); b = np.log(P.daily[d["leader"]].loc[lo:hi]).diff().shift(d["lag_days"])
    x = pd.concat([a, b], axis=1).dropna()
    both = int(((x.iloc[:, 0] != 0) & (x.iloc[:, 1] != 0)).sum())
    print(f"{d['corr']:+.3f} lag{d['lag_days']} n={len(x)} moves follower={int((x.iloc[:,0]!=0).sum())} leader={int((x.iloc[:,1]!=0).sum())} coincident={both} | {d['leader']} -> {d['series']}")
