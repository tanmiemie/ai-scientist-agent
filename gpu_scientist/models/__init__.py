"""Model library. Every file models/m_*.py defines one class that subclasses Model.

To add a model: copy models/m_template.py to models/m_<name>.py, set `name`, implement
`predict`. It is picked up automatically (registry below) and can be used in a spec by name.
"""
import importlib
import importlib.util
import os
import pkgutil
import sys
from pathlib import Path

from .base import Model

REGISTRY: dict[str, type] = {}

for mod in pkgutil.iter_modules([str(Path(__file__).parent)]):
    if mod.name.startswith("m_") and mod.name != "m_template":
        m = importlib.import_module(f"{__name__}.{mod.name}")
        for obj in vars(m).values():
            if isinstance(obj, type) and issubclass(obj, Model) and obj is not Model and getattr(obj, "name", None):
                REGISTRY[obj.name] = obj


def load_generated(directory) -> list[str]:
    """Register LLM-written models (<experiments>/models/m_*.py, see coder.py). Only sandboxed
    processes call this (GPU_LOAD_GENERATED=1), so generated code never runs in the research loop."""
    names = []
    for f in sorted(Path(directory).glob("m_*.py")):
        modname = f"{__name__}.{f.stem}"
        spec = importlib.util.spec_from_file_location(modname, f)
        m = importlib.util.module_from_spec(spec)
        sys.modules[modname] = m
        spec.loader.exec_module(m)
        for obj in vars(m).values():
            if isinstance(obj, type) and issubclass(obj, Model) and obj is not Model and getattr(obj, "name", None):
                REGISTRY[obj.name] = obj
                names.append(obj.name)
    return names


if os.environ.get("GPU_LOAD_GENERATED") == "1":
    import config as _C
    import sandbox_guard
    sandbox_guard.install(write_dirs=[_C.EXPERIMENTS, _C.WORK, os.environ.get("TMPDIR"), os.environ.get("MPLCONFIGDIR")])
    load_generated(_C.EXPERIMENTS / "models")


def make(name: str, params: dict | None = None) -> Model:
    if name not in REGISTRY:
        raise KeyError(f"unknown model {name!r}; known: {sorted(REGISTRY)}")
    return REGISTRY[name](**(params or {}))
