"""Read-only access to what the AI scientist writes: ledgers, experiments, walk-forward runs, LLM logs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config as C  # noqa: E402

LAB = ROOT / "experiments_app"
K = C.PRIMARY_METRIC


def pack_ready() -> bool:
    return (C.STARTER / "scorer.py").exists() and (C.STARTER / "build_series.py").exists()


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _read_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def ledger_label(d: Path) -> str:
    parts = d.relative_to(ROOT).parts
    if parts[0] == "walkforward":
        return f"walk-forward / {parts[1]} / {parts[2]}"
    if parts[0] == LAB.name:
        return f"lab / {parts[1]}"
    return parts[0]


def _ledger_order(d: Path) -> tuple:
    rel = d.relative_to(ROOT).as_posix()
    rank = 0 if rel == "experiments_final" else 1 if rel.startswith("experiments") else 3 if rel.startswith(LAB.name) else 2
    return rank, rel


def ledgers() -> dict[str, Path]:
    """Every folder with a ledger.jsonl, labelled; the main research ledger first."""
    dirs = {p.parent for p in ROOT.rglob("ledger.jsonl") if "replay" not in p.parts or p.parent.name == "experiments"}
    return {ledger_label(d): d for d in sorted(dirs, key=_ledger_order)}


@st.cache_data(show_spinner=False)
def ledger_df(exp_dir: str, mtime: float = 0.0) -> pd.DataFrame:
    recs = _read_jsonl(Path(exp_dir) / "ledger.jsonl")
    rows, champ, champ_hold = [], None, None
    for i, r in enumerate(recs):
        if r["accepted"]:
            champ, champ_hold = r["id"], r["holdout"][K]
        rows.append({
            "i": i, "id": r["id"], "accepted": bool(r["accepted"]), "parent": r.get("parent"),
            "champion_before": r.get("champion_before"), "champion_after": champ,
            "dev": r["dev"][K], "holdout": r["holdout"][K], "champion_holdout": champ_hold,
            "dev_geomean": r["dev"].get("skill_geomean"), "holdout_geomean": r["holdout"].get("skill_geomean"),
            "dev_coverage": r["dev"].get("coverage_in"), "holdout_coverage": r["holdout"].get("coverage_in"),
            "above_q90": r["dev"].get("coverage_above_q90"), "below_q10": r["dev"].get("coverage_below_q10"),
            "dev_by_h": r["dev"].get("by_horizon", {}), "hypothesis": r.get("hypothesis", ""),
            "lesson": r.get("lesson") or "", "reason": r.get("reason", ""), "time_utc": r.get("time_utc"),
            "runtime_s": r.get("runtime_s"), "spec": r.get("spec", {}),
        })
    return pd.DataFrame(rows)


def load_ledger(exp_dir: Path) -> pd.DataFrame:
    p = exp_dir / "ledger.jsonl"
    return ledger_df(str(exp_dir), p.stat().st_mtime if p.exists() else 0.0)


def champion(exp_dir: Path) -> dict | None:
    return _read_json(exp_dir / "champion.json")


def exp_json(exp_dir: Path, eid: str, name: str):
    return _read_json(exp_dir / eid / name)


def exp_text(exp_dir: Path, eid: str, name: str) -> str | None:
    p = exp_dir / eid / name
    return p.read_text() if p.exists() else None


@st.cache_data(show_spinner=False)
def _cells(path: str, mtime: float) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["origin_date", "target_date"])


def cells(exp_dir: Path, eid: str) -> pd.DataFrame | None:
    """Per-cell forecasts with truth for DEV and HOLDOUT origins (not in git; rebuilt by run_all.sh)."""
    out = []
    for tag in ("dev", "holdout"):
        p = exp_dir / eid / f"cells_{tag}.csv"
        if p.exists():
            out.append(_cells(str(p), p.stat().st_mtime).assign(window=tag))
    return pd.concat(out, ignore_index=True) if out else None


def per_series(exp_dir: Path, eid: str, tag: str) -> pd.DataFrame | None:
    r = exp_json(exp_dir, eid, f"report_{tag}.json")
    if not r or "per_series" not in r:
        return None
    return pd.DataFrame([{k: v for k, v in s.items() if not isinstance(v, dict)} for s in r["per_series"]])


def walkforward_runs() -> dict[str, Path]:
    return {p.parent.name: p.parent for p in sorted((ROOT / "walkforward").glob("*/summary.json"))}


@st.cache_data(show_spinner=False)
def walkforward_df(run_dir: str, mtime: float = 0.0) -> pd.DataFrame:
    return pd.DataFrame(json.loads((Path(run_dir) / "summary.json").read_text()))


def load_walkforward(run_dir: Path) -> pd.DataFrame:
    p = run_dir / "summary.json"
    return walkforward_df(str(run_dir), p.stat().st_mtime)


def autoresearch_log(exp_dir: Path) -> list[dict]:
    return _read_jsonl(exp_dir / "autoresearch_log.jsonl")


def submissions() -> dict[str, Path]:
    return {f"{p.parent.name}/{p.name}": p for p in sorted(ROOT.glob("submission*/forecast_*.csv"))}
