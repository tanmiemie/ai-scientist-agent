"""LLM-written models (DEVIN_NEXT.md task E): gates and sandbox.

The proposer may return {"new_model": {"name": ..., "code": ...}} written against models/m_template.py.
Before the experiment counts, the code must pass, in order:
  1. static   AST check: imports only numpy/pandas/scipy, `from data import <helper>` and `.base`;
              no os/sys/subprocess/socket/open/eval/exec/__import__ and friends, no file I/O
              helpers (np.load, pd.read_csv, to_csv, ...), no private or dunder attributes and no
              `ctx.panel` (the panel holds data after the origin); exactly one Model subclass whose
              `name` is the requested name and whose `defaults` is a literal dict.
  2. smoke    `predict` on 20 random (series, origin) pairs, at most 5 s in total, returns
              {h: None or (q10, q50, q90)} with finite positive values.
  3. lookahead tests/test_no_lookahead.py with the new model as the spec it checks: data after the
              origin multiplied by 3 or deleted must give bit-identical forecasts.
Every attempt is kept as <experiments>/coder/iter_<n>/attempt_<i>.py (and copied into the experiment
folder if it runs). A model that passes is saved as <experiments>/models/m_<name>.py, local to the run,
so one run's generated code never enters another run's or the canonical model registry.

Generated code only ever executes in a child process (sandbox_child.py) with no network
(`unshare -rn`, plus socket functions disabled), a memory limit and a timeout. In the research loop
itself the model is a stub carrying its name and defaults, enough to validate and hash specs.
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys

import config as C
import ledger
import models as M

ALLOWED_MODULES = {"numpy", "pandas", "scipy", "__future__"}
DATA_HELPERS = {"log_changes", "days_since_change"}
BASE_NAMES = {"Model", "from_log"}
BANNED_NAMES = {"os", "sys", "subprocess", "socket", "shutil", "pathlib", "importlib", "builtins", "io",
                "open", "eval", "exec", "compile", "__import__", "globals", "locals", "vars", "getattr",
                "setattr", "delattr", "input", "breakpoint", "exit", "quit", "memoryview", "help"}
BANNED_ATTRS = {"load", "save", "savez", "savez_compressed", "fromfile", "tofile", "loadtxt", "savetxt",
                "genfromtxt", "memmap", "DataSource", "ctypeslib", "panel", "system", "popen"}
BANNED_ATTR_RE = re.compile(r"^(read_\w+|to_(csv|json|pickle|parquet|excel|hdf|sql|feather|html|xml|stata|"
                            r"clipboard|latex|markdown|orc))$")
NAME_RE = re.compile(r"^[a-z][a-z0-9_]{1,30}$")
SMOKE_PAIRS, SMOKE_BUDGET_S = 20, 5.0
ERR_CHARS = 1500
GATE_TIMEOUT_S, RUN_TIMEOUT_S = 300, 900
ROOT = C.ROOT


_ITER_BASE: dict = {}


def iter_dir(iteration: int):
    """<experiments>/coder/iter_<n>; numbering continues after a previous run in the same folder."""
    root = C.EXPERIMENTS / "coder"
    if root not in _ITER_BASE:
        _ITER_BASE[root] = max((int(p.name[5:]) for p in root.glob("iter_*") if p.name[5:].isdigit()), default=0)
    return root / f"iter_{_ITER_BASE[root] + iteration:02d}"


def gen_dir():
    return C.EXPERIMENTS / "models"


def generated_names() -> set[str]:
    return {static_info(f.read_text())[0] for f in sorted(gen_dir().glob("m_*.py"))} if gen_dir().exists() else set()


def uses_generated(spec: dict) -> bool:
    g = generated_names()
    return any(m.get("name") in g for m in spec.get("models", []))


# ---------------------------------------------------------------- gate 1: static check
def static_info(code: str) -> tuple[str, dict]:
    """(name, defaults) of the single Model subclass, read from the AST without running the code."""
    tree = ast.parse(code)
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)
               and any(isinstance(b, ast.Name) and b.id == "Model" for b in n.bases)]
    if len(classes) != 1:
        raise ValueError(f"need exactly one class that subclasses Model, found {len(classes)}")
    name, defaults = None, None
    for st in classes[0].body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            if st.targets[0].id == "name":
                name = ast.literal_eval(st.value)
            elif st.targets[0].id == "defaults":
                defaults = ast.literal_eval(st.value)
    if not isinstance(name, str) or not isinstance(defaults, dict):
        raise ValueError("the class must set `name = \"...\"` and `defaults = {...}` as literals")
    for k, v in defaults.items():
        if not isinstance(k, str) or not (isinstance(v, (int, float)) and not isinstance(v, bool)):
            raise ValueError(f"defaults must map parameter names to numbers; got {k!r}: {v!r}")
    return name, defaults


def static_check(code: str, want_name: str) -> list[str]:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"SyntaxError: {e}"]
    errs = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                if a.name.split(".")[0] not in ALLOWED_MODULES:
                    errs.append(f"line {n.lineno}: import {a.name} is not allowed (numpy, pandas, scipy only)")
        elif isinstance(n, ast.ImportFrom):
            mod = n.module or ""
            names = {a.name for a in n.names}
            if n.level == 1 and mod == "base":
                bad = names - BASE_NAMES
            elif n.level == 0 and mod == "data":
                bad = names - DATA_HELPERS
            elif n.level == 0 and mod.split(".")[0] in ALLOWED_MODULES:
                bad = set()
            else:
                errs.append(f"line {n.lineno}: from {'.' * n.level}{mod} import ... is not allowed")
                continue
            if bad or "*" in names:
                errs.append(f"line {n.lineno}: cannot import {sorted(bad or {'*'})} from {'.' * n.level}{mod}")
        elif isinstance(n, ast.Name) and (n.id in BANNED_NAMES or n.id.startswith("__")):
            errs.append(f"line {n.lineno}: name {n.id!r} is not allowed")
        elif isinstance(n, ast.Attribute) and (n.attr.startswith("_") or n.attr in BANNED_ATTRS
                                               or BANNED_ATTR_RE.match(n.attr)):
            errs.append(f"line {n.lineno}: attribute .{n.attr} is not allowed (no private attributes, "
                        "no ctx.panel, no file I/O)")
        elif isinstance(n, (ast.Global, ast.Nonlocal)):
            errs.append(f"line {n.lineno}: global/nonlocal is not allowed")
    if errs:
        return errs
    try:
        name, _ = static_info(code)
    except Exception as e:
        return [str(e)]
    if name != want_name:
        return [f"class name attribute is {name!r} but new_model.name is {want_name!r}"]
    return []


def check_name(name) -> list[str]:
    if not isinstance(name, str) or not NAME_RE.match(name):
        return ["new_model.name must match [a-z][a-z0-9_]{1,30}"]
    if name in M.REGISTRY:
        return [f"a model named {name!r} already exists; pick a new name"]
    for r in ledger.load():
        if name in {m.get("name") for m in (r.get("spec") or {}).get("models", [])}:
            return [f"a model named {name!r} was already tried in {r.get('id')}; pick a new name"]
    return []


# ---------------------------------------------------------------- stubs for the research loop
def register_stubs() -> list[str]:
    """Put every generated model of this run into M.REGISTRY as a stub (name + defaults only)."""
    out = []
    if not gen_dir().exists():
        return out
    for f in sorted(gen_dir().glob("m_*.py")):
        name, defaults = static_info(f.read_text())
        if name not in M.REGISTRY:
            M.REGISTRY[name] = _stub(name, defaults)
        out.append(name)
    return out


def _stub(name: str, defaults: dict) -> type:
    def predict(self, ctx, horizons):
        raise RuntimeError("generated models only run inside the sandbox (coder.sandbox)")
    return type(f"Generated_{name}", (M.Model,), {"name": name, "defaults": dict(defaults), "predict": predict,
                                                   "generated": True})


# ---------------------------------------------------------------- sandbox
_UNSHARE = None


def _prefix() -> list[str]:
    global _UNSHARE
    if _UNSHARE is None:
        try:
            _UNSHARE = subprocess.run(["unshare", "-rn", "true"], capture_output=True, timeout=10).returncode == 0
        except Exception:
            _UNSHARE = False
    if _UNSHARE:
        return ["unshare", "-rn"]
    if os.environ.get("GPU_CODER_ALLOW_NETNS_FALLBACK") == "1":   # explicit opt-in: runtime guard only
        return []
    raise RuntimeError("no network namespace (`unshare -rn` failed); refusing to run generated code. "
                       "Set GPU_CODER_ALLOW_NETNS_FALLBACK=1 to rely on the in-process guard alone.")


def _env(extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items()
           if not any(s in k for s in ("KEY", "TOKEN", "SECRET", "PASSWORD"))}   # no credentials in the sandbox
    tmp = C.EXPERIMENTS / "coder" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    env.update({"TMPDIR": str(tmp), "MPLCONFIGDIR": str(tmp)})
    env.update({"GPU_LOAD_GENERATED": "1", "GPU_EXPERIMENTS": str(C.EXPERIMENTS), "PYTHONDONTWRITEBYTECODE": "1",
                "GPU_DEV": ",".join(C.DEV_ORIGINS), "GPU_HOLDOUT": ",".join(C.HOLDOUT_ORIGINS)})
    env.update(extra or {})
    return env


def sandbox(job: dict, timeout: int = RUN_TIMEOUT_S, extra_env: dict | None = None) -> dict:
    """Run one job of sandbox_child.py with no network; return its JSON result or {"error": ...}."""
    try:
        cmd = _prefix() + [sys.executable, "-B", str(ROOT / "sandbox_child.py")]
        p = subprocess.run(cmd, input=json.dumps(job), capture_output=True, text=True, timeout=timeout,
                           cwd=ROOT, env=_env(extra_env))
    except subprocess.TimeoutExpired:
        return {"error": f"timeout: the job did not finish within {timeout} s"}
    except RuntimeError as e:
        return {"error": str(e)}
    lines = [l for l in p.stdout.splitlines() if l.startswith("@@RESULT ")]
    if p.returncode == 0 and lines:
        return json.loads(lines[-1][len("@@RESULT "):])
    return {"error": (p.stdout + "\n" + p.stderr).strip()[-ERR_CHARS:] or f"exit code {p.returncode}"}


def lookahead_test(name: str) -> dict:
    try:
        cmd = _prefix() + [sys.executable, "-B", "-m", "pytest", "tests/test_no_lookahead.py", "-q", "-x",
                           "-p", "no:cacheprovider", "-k", "test_no_lookahead"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=GATE_TIMEOUT_S, cwd=ROOT,
                           env=_env({"GPU_LOOKAHEAD_MODELS": name}))
    except subprocess.TimeoutExpired:
        return {"error": f"timeout: test_no_lookahead did not finish within {GATE_TIMEOUT_S} s"}
    except RuntimeError as e:
        return {"error": str(e)}
    if p.returncode == 0:
        return {"ok": True, "summary": p.stdout.strip().splitlines()[-1]}
    return {"error": (p.stdout + "\n" + p.stderr).strip()[-ERR_CHARS:]}


# ---------------------------------------------------------------- the gates, in order
def gate(new_model: dict, iteration: int, attempt: int) -> dict:
    """Snapshot the attempt, then run static -> smoke -> lookahead. Returns
    {"name", "attempt", "passed": [...gates passed], "failed": gate or None, "error": text or None}."""
    name, code = new_model.get("name"), new_model.get("code")
    d = iter_dir(iteration)
    d.mkdir(parents=True, exist_ok=True)
    (d / f"attempt_{attempt}.py").write_text(code if isinstance(code, str) else json.dumps(code))
    res = {"name": name, "attempt": attempt, "file": str((d / f"attempt_{attempt}.py").relative_to(C.EXPERIMENTS)),
           "passed": [], "failed": None, "error": None}

    def fail(stage, err):
        res.update(failed=stage, error=err[-ERR_CHARS:])
        return res

    if not isinstance(code, str) or not code.strip():
        return fail("static", "new_model.code must be the full Python source as a string")
    errs = check_name(name) or static_check(code, name)
    if errs:
        return fail("static", "\n".join(errs))
    res["passed"].append("static")
    import data
    data.build()
    staging = C.EXPERIMENTS / "coder" / "staging"          # the only generated file the children load
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    (staging / f"m_{name}.py").write_text(code)
    try:
        out = sandbox({"job": "smoke", "file": str(staging / f"m_{name}.py"), "name": name,
                       "pairs": SMOKE_PAIRS, "budget_s": SMOKE_BUDGET_S, "seed": iteration * 100 + attempt},
                      timeout=GATE_TIMEOUT_S)
        if "error" in out:
            return fail("smoke", out["error"])
        res["smoke"] = out
        res["passed"].append("smoke")
        gen = gen_dir()
        gen.mkdir(parents=True, exist_ok=True)
        target = gen / f"m_{name}.py"
        target.write_text(code)                               # visible to the lookahead test's registry
        out = lookahead_test(name)
        if "error" in out:
            target.unlink()
            return fail("lookahead", out["error"])
        res["passed"].append("lookahead")
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return res


def copy_attempts(iteration: int, exp_id: str):
    src = iter_dir(iteration)
    for f in sorted(src.glob("attempt_*.py")):
        shutil.copy(f, C.EXPERIMENTS / exp_id / f.name)


def discard(name: str):
    """Remove a generated model that passed the gates but whose spec was then refused."""
    f = gen_dir() / f"m_{name}.py"
    if f.exists():
        f.unlink()
    M.REGISTRY.pop(name, None)


PROMPT = """
WRITING A NEW MODEL. Besides tuning, you may write a new forecaster in Python. Add to your JSON:
  "new_model": {"name": "<snake_case, new>", "code": "<full source of models/m_<name>.py>"}
and use that name in "spec" (alone, or with existing models under mean/hedge). The code must follow
this template and interface:
--- models/m_template.py ---
TEMPLATE
--- models/base.py: Model, from_log ---
BASE
--- what ctx gives you (data.Ctx; everything is cut at the origin) ---
  ctx.hist   pd.Series of daily as-of prices (USD/GPU-hour), DatetimeIndex, last entry = origin's value
  ctx.last   float, the last price
  ctx.origin pd.Timestamp; ctx.sid str; ctx.meta dict of the series' catalog row (source_id,
             source_class, instrument_class, gpu_model, ...)
  ctx.raw()  DataFrame of the collected rows up to the origin (columns include value, n_providers)
  ctx.peers(same="gpu_model") {series_id: pd.Series} of other series sharing that catalog field
  from data import log_changes, days_since_change
      log_changes(hist, h, window) -> np.ndarray of h-day log changes over the last `window` days
      days_since_change(hist) -> int
Gates the code must pass before it counts (on failure you get the error and may fix it, 3 times):
  imports only numpy, pandas, scipy, `from data import log_changes, days_since_change` and
  `from .base import Model, from_log`; no os/sys/subprocess/socket/open/eval/exec/__import__, no
  file I/O, no attributes starting with "_", never touch ctx.panel; exactly one Model subclass with
  name == new_model.name and literal numeric `defaults`; predict() must run on 20 random
  (series, origin) pairs in under 5 s in total and return {h: None or (q10, q50, q90)} with
  positive finite numbers; and forecasts must not change when data after the origin is changed.
Prefer a small, deterministic, vectorised model built around one idea from the diagnosis."""


def prompt(always: bool) -> str:
    txt = PROMPT.replace("TEMPLATE", (ROOT / "models" / "m_template.py").read_text().strip())
    base = (ROOT / "models" / "base.py").read_text()
    txt = txt.replace("BASE", base[base.index("class Model"):].strip())
    if always:
        txt += ("\nTHIS RUN TESTS MODEL WRITING: every proposal MUST include new_model, and spec must use it."
                " A sweep may tune one of its parameters (models.<i>.params.<p>).")
    return txt
