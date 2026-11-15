"""DEV-only check (DEVIN_NEXT.md task A data rules): is the GetDeploying signal carried by weeks where
n_providers changed from the week before? EDA with and without those cells, then the exp_008 spec scored
on DEV with skip_provider_change=0/1. DEV origins only, never HOLDOUT/TEST.
Run from gpu_scientist/: PYTHONPATH=. python3 scratch/dev_aggregator_nprov.py
"""
import json, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import config as C, data, online, evaluate
from dev_aggregator_eda import rows, summarise

d = rows()
print(f"DEV cells {len(d)}; latest usable week had an n_providers change in {d.npch.mean():.1%} "
      f"({d[d.npch].sid.nunique()} series)")
for name, g in (("all", d), ("n_providers unchanged", d[~d.npch]), ("n_providers changed", d[d.npch])):
    print(f"\n== gap, {name}"); print(summarise(g, "gap"))
    print("   h=7", summarise(g[g.h == 7], "gap"))

sc, cc = data.build(); panel = data.Panel.load(sc, cc); sids = panel.series_ids()
origins = pd.date_range(C.WARMUP_START, C.DEV_ORIGINS[1])
spec08 = json.load(open("specs/optional/08_aggregator.json"))
for skip in (0, 1):
    spec = json.loads(json.dumps(spec08)); spec["models"][0]["params"]["skip_provider_change"] = skip
    fc, _, _ = online.run(spec, panel, origins, sids, C.HORIZONS)
    m = evaluate.score(fc, C.DEV_ORIGINS, Path("/tmp/agg_nprov"), f"skip{skip}", sc, cc)
    print(f"exp_008 spec, skip_provider_change={skip}: DEV pooled {m['skill_pooled']:+.4f} median "
          f"{m['skill_median_of_series']:+.4f} geomean {m['skill_geomean']:+.4f} cov {m['coverage_in']:.3f}")
