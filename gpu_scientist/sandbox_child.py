"""Child process for coder.py: runs generated model code with no network, a memory cap and no
credentials. Reads one JSON job on stdin, prints '@@RESULT <json>' on success."""
import json
import os
import resource
import socket
import sys
import time


def _no_net(*a, **k):
    raise OSError("network access is disabled in the sandbox")


for _f in ("socket", "create_connection", "getaddrinfo", "socketpair", "fromfd"):
    setattr(socket, _f, _no_net)
resource.setrlimit(resource.RLIMIT_AS, (8 << 30, 8 << 30))
sys.excepthook = sys.__excepthook__   # plain tracebacks (distro hooks such as apport fail without network)


def smoke(job):
    import numpy as np
    import pandas as pd
    import config as C
    import data
    import models as M
    from data import Ctx
    names = M.load_generated(os.path.dirname(job["file"]))
    if job["name"] not in names:
        raise RuntimeError(f"model {job['name']!r} did not register (found {names})")
    model = M.make(job["name"])
    panel = data.Panel.load(*data.build())
    rng = np.random.default_rng(job["seed"])
    sids = panel.series_ids()
    days = pd.date_range(C.WARMUP_START, C.DEV_ORIGINS[1])
    spent, done, n_none = 0.0, 0, 0
    while done < job["pairs"]:
        sid, o = sids[rng.integers(len(sids))], days[rng.integers(len(days))]
        hist = panel.upto(sid, o)
        if len(hist) < 10:
            continue
        ctx = Ctx(sid=sid, origin=o, meta=panel.meta(sid), hist=hist, panel=panel)
        t0 = time.perf_counter()
        out = model.predict(ctx, C.HORIZONS)
        spent += time.perf_counter() - t0
        if spent > job["budget_s"]:
            raise RuntimeError(f"too slow: {spent:.2f} s after {done + 1} of {job['pairs']} pairs "
                               f"(budget {job['budget_s']} s in total)")
        if not isinstance(out, dict):
            raise TypeError(f"predict must return a dict, got {type(out).__name__}")
        for h in C.HORIZONS:
            q = out.get(h)
            if q is None:
                n_none += 1
                continue
            q = tuple(float(x) for x in q)
            if len(q) != 3 or not all(np.isfinite(q)) or min(q) <= 0:
                raise ValueError(f"{sid} @ {o.date()} h={h}: need 3 positive finite quantiles, got {q}")
            if not q[0] <= q[1] <= q[2]:
                raise ValueError(f"{sid} @ {o.date()} h={h}: quantiles not ordered q10<=q50<=q90: {q}")
        done += 1
    return {"pairs": done, "seconds": round(spent, 3), "none_horizons": n_none}


def run(job):
    import run_experiment
    rec = run_experiment.run(job["spec"], job["hypothesis"], parent=job.get("parent"), verbose=False)
    return rec


def dev_score(job):
    from pathlib import Path
    import run_experiment
    return run_experiment.dev_score(job["spec"], Path(job["out_dir"]))


def test_score(job):
    import pandas as pd
    import config as C
    import data
    import evaluate
    import online
    from pathlib import Path
    series_csv, catalog_csv = data.build()
    panel = data.Panel.load(series_csv, catalog_csv)
    fc, _, _ = online.run(job["spec"], panel, pd.date_range(C.WARMUP_START, job["test"][1]), panel.series_ids(),
                          C.HORIZONS)
    return evaluate.score(fc, tuple(job["test"]), Path(job["out_dir"]), job["label"], series_csv, catalog_csv)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    job = json.loads(sys.stdin.read())
    res = {"smoke": smoke, "run": run, "dev_score": dev_score, "test_score": test_score}[job["job"]](job)
    print("@@RESULT " + json.dumps(res, default=str))
