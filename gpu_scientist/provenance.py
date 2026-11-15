"""Provenance for immutable records: what data and code produced a forecast."""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import shutil
import subprocess
from pathlib import Path

import config as C


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def code_commit() -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=C.ROOT, capture_output=True, text=True, timeout=10)
        dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=C.ROOT,
                               capture_output=True, text=True, timeout=10).stdout.strip()
        return (out.stdout.strip() + ("+dirty" if dirty else "")) or None
    except Exception:
        return None


def record(series_csv, forecast_csv=None) -> dict:
    v = C.PACK / "VERSION"
    rec = {"created_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "pack_version": v.read_text().strip().splitlines()[0] if v.exists() else None,
           "series_sha256": sha256(series_csv), "code_commit": code_commit()}
    if forecast_csv is not None:
        rec["forecast_sha256"] = sha256(forecast_csv)
    return rec


def archive(csv_path) -> Path:
    """Keep a compressed, committed copy of a forecast file (CSVs themselves are git-ignored)."""
    gz = Path(str(csv_path) + ".gz")
    with open(csv_path, "rb") as src, gzip.GzipFile(gz, "wb", mtime=0) as dst:
        shutil.copyfileobj(src, dst)
    return gz
