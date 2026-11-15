# DEV-only sweep, round 2 for models/m_aggregator.py: move only the interval edge on the signal's side,
# and/or act only on large gaps. Scores DEV origins only, never HOLDOUT/TEST.
# Run from gpu_scientist/: PYTHONPATH=. python scratch/dev_sweep_aggregator_tail.py
import itertools, json, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, ".")
import config as C, data, online, evaluate

sc, cc = data.build(); panel = data.Panel.load(sc, cc); sids = panel.series_ids()
origins = pd.date_range(C.WARMUP_START, C.DEV_ORIGINS[1])
base = json.load(open("specs/07_composition.json"))
comp = base["models"][0]["params"]
out = Path("/tmp/sweep_agg2")

def run(params, tag):
    spec = json.loads(json.dumps(base)); spec["models"] = [{"name": "aggregator", "params": {**comp, **params}}]
    fc, _, _ = online.run(spec, panel, origins, sids, C.HORIZONS)
    m = evaluate.score(fc, C.DEV_ORIGINS, out, tag, sc, cc)
    r = (tag, round(m["skill_pooled"], 4), round(m["skill_geomean"], 4), round(m["skill_median_of_series"], 4), round(m["coverage_in"], 3))
    print(*r, flush=True); return r

res = []
for sig, b, cap in itertools.product(["gap", "dgap"], [0.1, 0.25, 0.5], [0.1, 0.3]):
    res.append(run({"signal": sig, "apply": "tail", "beta_agg": b, "cap": cap}, f"tail_{sig}_b{b}_c{cap}"))
for sig, mg, b in itertools.product(["gap", "dgap"], [0.1, 0.2], [0.05, 0.1]):
    res.append(run({"signal": sig, "apply": "all", "min_gap": mg, "beta_agg": b, "cap": 1.0}, f"all_{sig}_min{mg}_b{b}"))
print("\nbest by DEV pooled (exp_007 = 0.1908):")
for r in sorted(res, key=lambda x: -x[1])[:8]: print(*r)
