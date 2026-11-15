"""Lab workspaces and background jobs. The app never writes to the tracked ledgers: every run goes into
experiments_app/<workspace>, either fresh (seeded by a spec) or forked from an existing ledger."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import uuid
from pathlib import Path

from store import LAB, ROOT

JOBS = LAB / "_jobs"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "run"


def workspaces() -> list[Path]:
    return sorted(p for p in LAB.glob("*") if p.is_dir() and not p.name.startswith("_"))


def fork(src: Path, name: str) -> Path:
    """Copy a ledger with its small per-experiment files (spec, reports, diagnosis), not the CSVs."""
    dst = LAB / slug(name)
    if dst.exists():
        raise FileExistsError(f"workspace {dst.name} already exists")
    dst.mkdir(parents=True)
    for f in ("ledger.jsonl", "champion.json", "autoresearch_log.jsonl"):
        if (src / f).exists():
            shutil.copy2(src / f, dst / f)
    for e in sorted(src.glob("exp_*")):
        (dst / e.name).mkdir()
        for f in e.glob("*"):
            if f.suffix in (".json", ".md"):
                shutil.copy2(f, dst / e.name / f.name)
    return dst


def new_workspace(name: str) -> Path:
    dst = LAB / slug(name)
    if dst.exists():
        raise FileExistsError(f"workspace {dst.name} already exists")
    dst.mkdir(parents=True)
    return dst


def busy(workspace: Path) -> bool:
    """A workspace's ledger and experiment ids are not safe for concurrent writers."""
    return any(j["running"] and j.get("workspace") == str(workspace) for j in jobs())


def start(kind: str, args: list[str], workspace: Path | None, title: str, extra_env: dict | None = None) -> str:
    if workspace is not None and busy(workspace):
        raise RuntimeError(f"a job is already running in {workspace.name}")
    JOBS.mkdir(parents=True, exist_ok=True)
    jid = f"{dt.datetime.now():%Y%m%d-%H%M%S}-{slug(kind)}-{uuid.uuid4().hex[:6]}"
    log = JOBS / f"{jid}.log"
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1", **(extra_env or {})}
    if workspace is not None:
        env["GPU_EXPERIMENTS"] = str(workspace)
        env["GPU_SUBMISSION"] = str(workspace / "submission")
    with open(log, "w") as fh:
        proc = subprocess.Popen([sys.executable, "-u", *args], cwd=ROOT, env=env, stdout=fh,
                                stderr=subprocess.STDOUT, start_new_session=True)
    meta = {"id": jid, "kind": kind, "title": title, "args": args, "pid": proc.pid,
            "workspace": str(workspace) if workspace else None, "started": dt.datetime.now().isoformat(timespec="seconds")}
    (JOBS / f"{jid}.json").write_text(json.dumps(meta, indent=1))
    return jid


def _alive(pid: int) -> bool:
    try:
        wpid, _ = os.waitpid(pid, os.WNOHANG)
        if wpid == pid:
            return False
    except ChildProcessError:
        pass
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    status = Path(f"/proc/{pid}/status")
    return not status.exists() or "zombie" not in status.read_text().lower()


def jobs() -> list[dict]:
    out = []
    if not JOBS.exists():
        return out
    for m in sorted(JOBS.glob("*.json"), reverse=True):
        meta = json.loads(m.read_text())
        meta["running"] = _alive(meta["pid"]) if "ended" not in meta else False
        if not meta["running"] and "ended" not in meta:
            meta["ended"] = dt.datetime.now().isoformat(timespec="seconds")
            m.write_text(json.dumps({k: v for k, v in meta.items() if k != "running"}, indent=1))
        out.append(meta)
    return out


def log_text(jid: str, tail: int = 400) -> str:
    p = JOBS / f"{jid}.log"
    lines = p.read_text(errors="replace").splitlines() if p.exists() else []
    return "\n".join(lines[-tail:])


def stop(jid: str) -> None:
    meta = json.loads((JOBS / f"{jid}.json").read_text())
    try:
        os.killpg(meta["pid"], signal.SIGTERM)
    except ProcessLookupError:
        pass
