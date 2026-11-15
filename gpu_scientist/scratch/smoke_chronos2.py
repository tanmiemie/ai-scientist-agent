import time, pandas as pd, config as C, data, models as M
s, c = data.build(); P = data.Panel.load(s, c); ids = P.series_ids()
o = pd.Timestamp(C.DEV_ORIGINS[0])
import sys
for g in sys.argv[1:]:
    m = M.make(g, {}); t = time.time(); n = 0
    for sid in ids:
        h = P.upto(sid, o)
        if len(h) < 10: continue
        ctx = data.Ctx(sid, o, P.meta(sid), h, P); r = m.predict(ctx, (1, 3, 7)); n += 1
    print(g, n, "series", round(time.time() - t, 1), "s", sid, r)
