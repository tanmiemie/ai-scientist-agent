"""Scratch: score spec variants on DEV origins only (official scorer); holdout is never run.
usage: PYTHONPATH=. python scratch/sweep_dev.py base_spec.json '{"path.to.param": [v1, v2]}' """
import copy, json, sys, tempfile
from pathlib import Path
import pandas as pd
import config as C, data, evaluate, online
spec0 = json.load(open(sys.argv[1])); grid = json.loads(sys.argv[2])
s, c = data.build(); P = data.Panel.load(s, c); ids = P.series_ids()
origins = pd.date_range(C.WARMUP_START, C.DEV_ORIGINS[1])
def setp(sp, path, v):
    keys = path.split("."); d = sp
    for k in keys[:-1]:
        d = d[int(k)] if isinstance(d, list) else d[k]
    d[keys[-1]] = v
(path, vals), = grid.items()
for v in vals:
    sp = copy.deepcopy(spec0); setp(sp, path, v)
    fc, _, _ = online.run(sp, P, origins, ids, C.HORIZONS)
    m = evaluate.score(fc, C.DEV_ORIGINS, Path(tempfile.mkdtemp()), "dev", s, c)
    print(f"{path}={v}: dev pooled {m['skill_pooled']:+.4f} median {m['skill_median_of_series']:+.4f} geomean {m['skill_geomean']:+.4f} cov {m['coverage_in']:.3f} above {m['coverage_above_q90']:.3f}", flush=True)
