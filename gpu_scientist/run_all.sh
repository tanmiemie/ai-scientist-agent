#!/usr/bin/env bash
# One command reproduces everything from the pack: rebuild the series, replay every spec in
# specs/ in order into a fresh ledger (replay/experiments, so the live research ledger is never
# touched), plot progress and write the Sunday submission from the replayed champion.
# Usage: bash run_all.sh            (pack next to this folder, or GPU_PACK=/path/to/pack)
# Takes about 5 minutes on a laptop. Check: sha256sum replay/submission/*.csv submission_final/*.csv
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
export GPU_EXPERIMENTS="$PWD/replay/experiments" GPU_SUBMISSION="$PWD/replay/submission"
rm -rf replay
python3 -c "import data; data.build(force=True); data.build(force=True, cutoff=__import__('config').CUTOFF)"
prev=""
for spec in specs/*.json; do
  if [[ "$spec" == *chronos* && "${RUN_HEAVY:-0}" != "1" ]]; then
    # Chronos needs extra packages and a weight download; it was rejected, so skipping it leaves the
    # champion and the submission unchanged. RUN_HEAVY=1 bash run_all.sh includes it.
    echo "== skipped $spec (set RUN_HEAVY=1 to include; rejected in the official ledger)"; continue
  fi
  hyp=$(python3 -c "import json; print(json.load(open('$spec')).get('_hypothesis', 'replay of $spec'))")
  eid="exp_$(basename "$spec" | cut -c1-2 | sed 's/^/0/')"   # specs/07_x.json -> exp_007, as in the official ledger
  python3 run_experiment.py --spec "$spec" --hypothesis "$hyp" --id "$eid" ${prev:+--parent $prev} | sed -n '2,4p'
  prev="$eid"
done
python3 ledger.py plot
python3 submit.py
