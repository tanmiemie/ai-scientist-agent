"""Model library. Every file models/m_*.py defines one class that subclasses Model.

To add a model: copy models/m_template.py to models/m_<name>.py, set `name`, implement
`predict`. It is picked up automatically (registry below) and can be used in a spec by name.
"""
import importlib
import pkgutil
from pathlib import Path

from .base import Model

REGISTRY: dict[str, type] = {}

for mod in pkgutil.iter_modules([str(Path(__file__).parent)]):
    if mod.name.startswith("m_") and mod.name != "m_template":
        m = importlib.import_module(f"{__name__}.{mod.name}")
        for obj in vars(m).values():
            if isinstance(obj, type) and issubclass(obj, Model) and obj is not Model and getattr(obj, "name", None):
                REGISTRY[obj.name] = obj


def make(name: str, params: dict | None = None) -> Model:
    if name not in REGISTRY:
        raise KeyError(f"unknown model {name!r}; known: {sorted(REGISTRY)}")
    return REGISTRY[name](**(params or {}))
