"""DEV-only look at what happens after a recent price change (champion exp_000 cells)."""
import numpy as np, pandas as pd
import config as C, data
from data import days_since_change
s, c = data.build(); P = data.Panel.load(s, c)
cells = pd.read_csv(C.EXPERIMENTS / "exp_000/cells_dev.csv"); cells = cells[cells.status == "scored"].copy()
rows = []
for r in cells.itertuples():
    o = pd.Timestamp(r.origin_date); h = P.upto(r.series_id, o); v = np.log(h.values)
    d = days_since_change(h); nz = np.nonzero(np.diff(v))[0]
    jump = v[nz[-1] + 1] - v[nz[-1]] if len(nz) else 0.0
    rows.append((d, jump, np.log(r.y / h.values[-1]), r.horizon_days))
d = pd.DataFrame(rows, columns=["dsc", "jump", "ret", "h"])
d["recent"] = d.dsc <= 1; d["dir"] = np.sign(d.jump)
print(d.groupby(["recent", "dir"]).agg(n=("ret", "size"), up=("ret", lambda x: (x > 0).mean()), dn=("ret", lambda x: (x < 0).mean()), mean=("ret", "mean")).round(3))
r = d[d.recent & (d.jump != 0)]
for h, g in r.groupby("h"):
    b = np.polyfit(g.jump, g.ret, 1)[0]; print("h", h, "slope ret~last_jump", round(b, 3), "n", len(g))
