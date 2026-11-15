"""coder.py static gate: what an LLM-written model may and may not do (no data or network needed)."""
import pytest

import coder
import config as C

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


GUARD_PROBE = r'''
import os, socket, sys
sys.path.insert(0, os.getcwd())
import sandbox_guard
sandbox_guard.install(write_dirs=[sys.argv[1]])
out = []
for name, f in [("read_home", lambda: open(os.path.expanduser("~/.bashrc")).read()),
                ("write_outside", lambda: open(os.path.join(os.path.dirname(sys.argv[1]), "x.txt"), "w")),
                ("socket", lambda: socket.socket()),
                ("subprocess", lambda: __import__("subprocess").run(["true"])),
                ("pandas_handle", lambda: __import__("pandas.io.common", fromlist=["x"]).get_handle("/etc/hostname", "r"))]:
    try:
        f(); out.append(name + ":allowed")
    except PermissionError:
        out.append(name + ":blocked")
open(os.path.join(sys.argv[1], "ok.txt"), "w").write("fine")
print(" ".join(out))
'''


def test_runtime_guard_blocks_files_network_processes(tmp_path):
    import subprocess
    import sys
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    p = subprocess.run([sys.executable, "-c", GUARD_PROBE, str(allowed)], cwd=C.ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert p.stdout.split() == ["read_home:blocked", "write_outside:blocked", "socket:blocked",
                                "subprocess:blocked", "pandas_handle:blocked"]
    assert (allowed / "ok.txt").read_text() == "fine"


def test_name_of_a_tried_model_cannot_be_reused(monkeypatch):
    monkeypatch.setattr(coder.ledger, "load", lambda: [{"id": "exp_003", "spec": {"models": [{"name": "my_try"}]}}])
    assert "already tried in exp_003" in coder.check_name("my_try")[0]
    assert coder.check_name("my_other") == []


def test_guard_allows_only_the_official_scorer_call(tmp_path):
    import subprocess
    import sys
    probe = r'''
import os, sys
sys.path.insert(0, os.getcwd())
import config as C, sandbox_guard
sandbox_guard.install(write_dirs=[sys.argv[1]])
import subprocess
ok = [sys.executable, "-B", str(C.STARTER / "scorer.py"), "--tier", "x"]
bad = [sys.executable, "-B", str(C.STARTER / "scorer.py"), "--out", "/etc/x"]
for name, cmd in [("scorer", ok), ("scorer_out_elsewhere", bad), ("python", [sys.executable, "-c", "1"])]:
    try:
        subprocess.run(cmd, capture_output=True); print(name + ":allowed")
    except PermissionError:
        print(name + ":blocked")
'''
    p = subprocess.run([sys.executable, "-c", probe, str(tmp_path)], cwd=C.ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert p.stdout.split() == ["scorer:allowed", "scorer_out_elsewhere:blocked", "python:blocked"]


def test_sandbox_refuses_without_network_namespace(monkeypatch):
    monkeypatch.setattr(coder, "_UNSHARE", False)
    monkeypatch.delenv("GPU_CODER_ALLOW_NETNS_FALLBACK", raising=False)
    assert "refusing to run generated code" in coder.sandbox({"job": "smoke"})["error"]
    assert "refusing to run generated code" in coder.lookahead_test("x")["error"]



def test_guard_scorer_exception_needs_the_real_interpreter(tmp_path):
    import subprocess
    import sys
    probe = r"""
import os, sys
sys.path.insert(0, os.getcwd())
import config as C, sandbox_guard
sandbox_guard.install(write_dirs=[sys.argv[1]])
import subprocess
argv = [sys.executable, "-B", str(C.STARTER / "scorer.py"), "--tier", "x"]
for name, kw in [("other_executable", {"executable": "/bin/sh"}), ("cwd", {"cwd": "/"}), ("env", {"env": {}})]:
    try:
        subprocess.run(argv, capture_output=True, **kw); print(name + ":allowed")
    except PermissionError:
        print(name + ":blocked")
os.environ["PYTHONPATH"] = sys.argv[1]
try:
    subprocess.run(argv, capture_output=True); print("changed_env:allowed")
except PermissionError:
    print("changed_env:blocked")
"""
    p = subprocess.run([sys.executable, "-c", probe, str(tmp_path)], cwd=C.ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert p.stdout.split() == ["other_executable:blocked", "cwd:blocked", "env:blocked", "changed_env:blocked"]
