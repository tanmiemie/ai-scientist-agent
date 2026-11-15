"""Tabulate the memory ablation (task C) from walkforward/<run>/S*/experiments and summary.json.

Repeats of rejected ideas are judged by hand from the -v listing and the refused proposals in
autoresearch_log.jsonl (see walkforward/MEMORY_ABLATION.md)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report import _diff

WF = Path(__file__).resolve().parents[1] / "walkforward"
RUNS = ["llm_mem", "llm_mem_2", "llm_nomem", "llm_nomem_2"]


rows, detail = [], []
for run in RUNS:
    summ = json.loads((WF / run / "summary.json").read_text()) if (WF / run / "summary.json").exists() else []
    for s in ("S1", "S2", "S3"):
        ed = WF / run / s / "experiments"
        if not (ed / "ledger.jsonl").exists():
            continue
        led = [json.loads(l) for l in (ed / "ledger.jsonl").read_text().splitlines() if l.strip()]
        log = [json.loads(l) for l in (ed / "autoresearch_log.jsonl").read_text().splitlines() if l.strip()]
        by = {r["id"]: r for r in led}
        exps = [r for r in led if r.get("champion_before")]
        refused_iters = sum(1 for x in log if x.get("id") is None)
        refused_props = sum(len(x.get("refused") or x.get("refused_before") or []) for x in log)
        for r in exps:
            detail.append(dict(run=run, slice=s, id=r["id"], acc=r["accepted"],
                               diff=_diff(by[r["champion_before"]]["spec"], r["spec"]),
                               hyp=r["hypothesis"][:160]))
        sl = [x for x in summ if x["slice"] == s]
        rows.append(dict(run=run, slice=s, seed_test=sl[0]["test"] if sl else None,
                         final_test=sl[-1]["test"] if sl else None, final_champ=sl[-1]["champion"] if sl else None,
                         accepted=sum(r["accepted"] for r in exps), rejected=sum(not r["accepted"] for r in exps),
                         refused_iterations=refused_iters, refused_proposals=refused_props))
print(json.dumps(rows, indent=1, default=str))
if "-v" in sys.argv:
    for d in detail:
        print(f"{d['run']:12s} {d['slice']} {d['id']} {'ACC' if d['acc'] else 'rej'} | {d['diff']} | {d['hyp']}")
