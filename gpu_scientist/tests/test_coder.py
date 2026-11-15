"""coder.py static gate: what an LLM-written model may and may not do (no data or network needed)."""
import pytest

import coder

GOOD = '''import numpy as np
from data import log_changes
from .base import Model, from_log


class Wide(Model):
    name = "wide_test"
    defaults = {"window": 60, "k": 1.5}

    def predict(self, ctx, horizons):
        out = {}
        for h in horizons:
            ch = log_changes(ctx.hist, h, int(self.p["window"]))
            if len(ch) < 5:
                out[h] = None
                continue
            lo, mid, hi = np.quantile(ch, [0.1, 0.5, 0.9])
            out[h] = from_log(ctx.last, self.p["k"] * lo, mid, self.p["k"] * hi)
        return out
'''


def test_good_model_passes():
    assert coder.static_check(GOOD, "wide_test") == []
    assert coder.static_info(GOOD) == ("wide_test", {"window": 60, "k": 1.5})


@pytest.mark.parametrize("bad", [
    "import os",
    "import subprocess",
    "import socket",
    "from data import build",
    "import data",
    "import config",
    "from evaluate import score",
    "x = open('f')",
    "x = eval('1')",
    "exec('1')",
    "m = __import__('os')",
    "x = getattr(np, 'load')",
    "x = np.load('f.npy')",
    "import pandas as pd\nx = pd.read_csv('f.csv')",
    "x = ctx.panel",
    "x = ctx._raw_by",
    "x = ().__class__.__subclasses__()",
])
def test_banned_code_is_refused(bad):
    assert coder.static_check(GOOD + "\n\ndef f(ctx, np=None):\n    " + bad.replace("\n", "\n    ") + "\n",
                              "wide_test")


def test_name_must_match_and_be_new():
    assert coder.static_check(GOOD, "other")
    assert coder.check_name("momentum")            # registered already
    assert coder.check_name("Bad-Name")
    assert coder.check_name("fresh_idea") == []


def test_defaults_must_be_literal_numbers():
    assert coder.static_check(GOOD.replace('"k": 1.5', '"k": "x"'), "wide_test")
    assert coder.static_check(GOOD.replace('{"window": 60, "k": 1.5}', 'dict(window=60)'), "wide_test")
