#!/usr/bin/env bash
# One command reproduces everything from the pack: rebuild the series, replay every spec in
# specs/ in order into a fresh ledger (replay/experiments, so the live research ledger is never
# touched), plot progress and write the Sunday submission from the replayed champion.
# Usage: bash run_all.sh            (pack next to this folder, or GPU_PACK=/path/to/pack)
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
export GPU_EXPERIMENTS="$PWD/replay/experiments" GPU_SUBMISSION="$PWD/replay/submission"
rm -rf replay
python3 -c "import data; data.build(force=True); data.build(force=True, cutoff=__import__('config').CUTOFF)"
prev=""
for spec in specs/*.json; do
  hyp=$(python3 -c "import json; print(json.load(open('$spec')).get('_hypothesis', 'replay of $spec'))")
  python3 run_experiment.py --spec "$spec" --hypothesis "$hyp" ${prev:+--parent $prev} | sed -n '2,4p'
  prev=$(basename "$(ls -d "$GPU_EXPERIMENTS"/exp_* | tail -1)")
done
python3 ledger.py plot
python3 submit.py
