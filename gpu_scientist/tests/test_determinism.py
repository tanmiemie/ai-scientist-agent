"""Spec 04 run twice over the same window gives identical forecasts, also in a fresh process with a
different hash seed (set/dict ordering must not leak into the numbers)."""
import json
import os
import subprocess
import sys

import pandas as pd

import config as C
import online

SPEC04 = json.loads((C.ROOT / "specs" / "04_momentum.json").read_text())
WINDOW = ("2026-10-01", "2026-10-20")


def run(panel):
    fc, per_model, state = online.run(SPEC04, panel, pd.date_range(*WINDOW), panel.series_ids(), C.HORIZONS)
    return fc, state


def test_determinism(panel):
    (a, sa), (b, sb) = run(panel), run(panel)
    assert len(a) > 0
    pd.testing.assert_frame_equal(a, b, check_exact=True)
    assert json.dumps(sa, sort_keys=True) == json.dumps(sb, sort_keys=True)


def test_determinism_fresh_process(panel, built, tmp_path):
    a, _ = run(panel)
    out = tmp_path / "fc.pkl"
    code = (f"import json,data,online,config as C,pandas as pd\n"
            f"p=data.Panel.load(*data.build())\n"
            f"fc,_,_=online.run(json.load(open({str(C.ROOT / 'specs' / '04_momentum.json')!r})),p,"
            f"pd.date_range(*{WINDOW!r}),p.series_ids(),C.HORIZONS)\n"
            f"fc.to_pickle({str(out)!r})\n")
    subprocess.run([sys.executable, "-B", "-c", code], check=True, cwd=C.ROOT,
                   env={**os.environ, "PYTHONHASHSEED": "12345"})
    pd.testing.assert_frame_equal(a, pd.read_pickle(out), check_exact=True)
