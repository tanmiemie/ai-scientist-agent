import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

import config as C  # noqa: E402
import data  # noqa: E402


@pytest.fixture(scope="session")
def built():
    if not (C.STARTER / "build_series.py").exists():
        pytest.skip(f"data pack not found at {C.PACK}; set GPU_PACK")
    return data.build()


@pytest.fixture(scope="session")
def panel(built):
    return data.Panel.load(*built)
