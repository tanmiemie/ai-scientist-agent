# Report for exp_008 (aggregator) vs exp_007: per-series Wilcoxon (significance.py) and the per-collector /
# early-set HOLDOUT split (honest_eval.py). Run from gpu_scientist/: PYTHONPATH=. python scratch/aggregator_report.py
import json, sys
import pandas as pd
sys.path.insert(0, ".")
import config as C, data, evaluate, online
from significance import compare, per_series_loss

SPECS = {"07": "specs/07_composition.json", "08": "specs/08_aggregator.json"}
sc, cc = data.build(); data.build(cutoff="2026-10-15")
cat_oct = C.WORK / "series_catalog_cut2026-10-15.csv"
early = sorted(pd.read_csv(cat_oct).query("tier == 'headline'").series_id)
panel = data.Panel.load(sc, cc); sids = panel.series_ids()
origins = pd.date_range(C.WARMUP_START, C.HOLDOUT_ORIGINS[1])
out = C.WORK / "aggregator_report"
L, res = {}, {"wilcoxon_08_vs_07": {}, "by_collector_holdout": [], "early_set_holdout": {}, "metrics": {}}
for n, p in SPECS.items():
    fc, _, _ = online.run(json.load(open(p)), panel, origins, sids, C.HORIZONS)
    for tag, win in (("dev", C.DEV_ORIGINS), ("holdout", C.HOLDOUT_ORIGINS)):
        res["metrics"][f"{n}_{tag}"] = {k: v for k, v in evaluate.score(fc, win, out, f"{n}_{tag}", sc, cc).items()
                                        if k in ("skill_pooled", "skill_median_of_series", "skill_geomean", "coverage_in")}
        L[(n, tag)] = per_series_loss(pd.read_csv(out / f"cells_{n}_{tag}.csv"))
    c = pd.read_csv(out / f"cells_{n}_holdout.csv").query("status == 'scored'")
    for src, g in c.groupby(c.series_id.str.split(".").str[0]):
        res["by_collector_holdout"].append({"spec": n, "collector": src, "n_series": int(g.series_id.nunique()),
                                            "pooled": round(1 - g.loss.sum() / g.baseline_loss.sum(), 4)})
    m = evaluate.score(fc[fc.series_id.isin(early)], C.HOLDOUT_ORIGINS, out, f"early_{n}", sc, cat_oct)
    res["early_set_holdout"][n] = {k: m[k] for k in ("skill_pooled", "skill_median_of_series", "skill_geomean", "coverage_in")}
for tag in ("dev", "holdout", "both"):
    get = lambda n: (L[(n, "dev")] + L[(n, "holdout")]) if tag == "both" else L[(n, tag)]
    res["wilcoxon_08_vs_07"][tag] = compare(get("08").loss, get("07").loss)
res["early_set_size"] = len(early)
json.dump(res, open(C.EXPERIMENTS / "exp_008" / "aggregator_report.json", "w"), indent=1)
print(json.dumps(res, indent=1))
