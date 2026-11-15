# DEV-only sweep for models/m_composition.py (spec 07). Run from gpu_scientist/: python scratch/dev_sweep_composition.py
# DEV-only sweep: scores DEV origins only, never HOLDOUT/TEST
import json, itertools, pandas as pd, sys
sys.path.insert(0,".")
import config as C, data, online, evaluate
sc, cc = data.build(); panel = data.Panel.load(sc, cc); sids = panel.series_ids()
origins = pd.date_range(C.WARMUP_START, C.DEV_ORIGINS[1])
base = json.load(open("specs/04_momentum.json"))
from pathlib import Path
out = Path("/tmp/sweep"); res=[]
def run(params, tag):
    spec = json.loads(json.dumps(base)); spec["models"] = [{"name": "composition", "params": params}]
    fc, _, _ = online.run(spec, panel, origins, sids, C.HORIZONS)
    m = evaluate.score(fc, C.DEV_ORIGINS, out, tag, sc, cc); return m
m = run({"window":60,"floor":1.0,"k":1,"beta":0.25,"rho":0.0,"thresh":9.0}, "momentum_equiv")
print("momentum-equivalent (comp moves get no momentum, no reversion):", round(m["skill_pooled"],4), round(m["coverage_in"],3))
for rho, th, kr in itertools.product([0.0,0.2,0.4,0.6],[0.03,0.05,0.10],[1,3]):
    m = run({"window":60,"floor":1.0,"k":1,"beta":0.25,"rho":rho,"thresh":th,"k_rev":kr}, f"r{rho}_t{th}_k{kr}")
    res.append((rho,th,kr,round(m["skill_pooled"],4),round(m["skill_geomean"],4),round(m["coverage_in"],3)))
for r in sorted(res,key=lambda x:-x[3]): print(r)
