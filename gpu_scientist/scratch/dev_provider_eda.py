"""DEV-only: does a change in n_providers over the last 7 days predict the next move? (exp_000 cells)"""
import numpy as np, pandas as pd
import config as C, data
s, c = data.build(); P = data.Panel.load(s, c)
cells = pd.read_csv(C.EXPERIMENTS / "exp_000/cells_dev.csv"); cells = cells[cells.status == "scored"]
rows = []
for r in cells.itertuples():
    o = pd.Timestamp(r.origin_date); raw = P.raw_upto(r.series_id, o)
    if "n_providers" not in raw or len(raw) < 8:
        continue
    n = raw.n_providers.values
    dn = n[-1] - n[-8]  # same definition as diagnose.py
    h = P.upto(r.series_id, o); w7 = np.log(h.values[-1] / h.values[-8]) if len(h) > 8 else 0.0
    rows.append((np.sign(dn), np.sign(w7), np.log(r.y / h.values[-1]), r.horizon_days, (r.y > r.q90), (r.y < r.q10)))
d = pd.DataFrame(rows, columns=["prov", "move7", "ret", "h", "above", "below"])
print(d.groupby(["prov", "move7"]).agg(n=("ret", "size"), up=("ret", lambda x: (x > 0).mean()), dn=("ret", lambda x: (x < 0).mean()),
      mean=("ret", "mean"), above_q90=("above", "mean"), below_q10=("below", "mean")).round(3))
