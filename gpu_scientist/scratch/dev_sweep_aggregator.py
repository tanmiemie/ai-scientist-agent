# DEV-only sweep for models/m_aggregator.py. Scores DEV origins only, never HOLDOUT/TEST.
# Run from gpu_scientist/: PYTHONPATH=. python scratch/dev_sweep_aggregator.py
import itertools, json, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, ".")
import config as C, data, online, evaluate

sc, cc = data.build(); panel = data.Panel.load(sc, cc); sids = panel.series_ids()
origins = pd.date_range(C.WARMUP_START, C.DEV_ORIGINS[1])
base = json.load(open("specs/07_composition.json"))
comp = base["models"][0]["params"]
out = Path("/tmp/sweep_agg")

def run(params, tag):
    spec = json.loads(json.dumps(base)); spec["models"] = [{"name": "aggregator", "params": {**comp, **params}}]
    fc, _, _ = online.run(spec, panel, origins, sids, C.HORIZONS)
    m = evaluate.score(fc, C.DEV_ORIGINS, out, tag, sc, cc)
    r = (tag, round(m["skill_pooled"], 4), round(m["skill_geomean"], 4), round(m["skill_median_of_series"], 4), round(m["coverage_in"], 3))
    print(*r, flush=True); return r

res = [run({"beta_agg": 0.0}, "beta0_equals_exp007")]
for sig, col, b, cap in itertools.product(["gap", "dgap"], ["median_usd_per_gpu_hour", "provider_median_usd_per_gpu_hour"],
                                          [0.05, 0.1, 0.2, 0.3], [0.1, 0.3]):
    res.append(run({"signal": sig, "col": col, "beta_agg": b, "cap": cap}, f"{sig}_{col[:3]}_b{b}_c{cap}"))
print("\nbest by DEV pooled:")
for r in sorted(res, key=lambda x: -x[1])[:8]: print(*r)
