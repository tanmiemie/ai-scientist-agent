"""Shared settings. Override the pack location with the GPU_PACK environment variable."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACK = Path(os.environ.get("GPU_PACK", ROOT.parent / "gpu-price-pack-v0.1.1-handover")).resolve()
STARTER = PACK / "starter"
WORK = ROOT / "work"                 # built series, caches
EXPERIMENTS = Path(os.environ.get("GPU_EXPERIMENTS", ROOT / "experiments")).resolve()   # one folder per experiment + ledger.jsonl + champion.json
SUBMISSION = Path(os.environ.get("GPU_SUBMISSION", ROOT / "submission")).resolve()

CUTOFF = "2026-11-06"                # the pack's last day = the frozen origin for Sunday
HORIZONS = (1, 3, 7)                 # scored on Sunday (30 is not)
TIER = "headline"                    # which catalog tier the dev/holdout scores use

# Daily origins. The research loop may look at DEV results as often as it likes.
# HOLDOUT is only ever scored by run_experiment.py and is the gate for accepting a change.
WARMUP_START = "2026-08-15"          # online loop starts here so calibration/weights have feedback
# Both can be overridden (e.g. by walkforward.py) with GPU_DEV / GPU_HOLDOUT="start,end".
DEV_ORIGINS = tuple(os.environ.get("GPU_DEV", "2026-09-15,2026-10-15").split(","))
HOLDOUT_ORIGINS = tuple(os.environ.get("GPU_HOLDOUT", "2026-10-16,2026-10-30").split(","))  # 10-30 + 7 days = 11-06

# Accept rule (see RESEARCH_PROTOCOL.md)
PRIMARY_METRIC = "skill_pooled"
MIN_DEV_GAIN = 0.002                 # candidate must beat the champion on dev by at least this
HOLDOUT_TOLERANCE = 0.0              # ...and must not be worse than the champion on holdout
