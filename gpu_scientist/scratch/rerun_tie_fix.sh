#!/bin/bash
cd /home/ubuntu/repos/ai-scientist-agent/gpu_scientist
export PATH=/home/ubuntu/gpu/.venv/bin:$PATH GPU_PACK=/home/ubuntu/gpu/gpu-price-pack-v0.1.1-handover
echo "== run1 $(date)"; bash run_all.sh || exit 1
cp replay/submission/forecast_2026-11-06.csv scratch/logs/run1_forecast.csv
python3 ledger.py show > scratch/logs/run1_ledger.txt 2>&1
echo "== run2 $(date)"; bash run_all.sh || exit 1
cmp scratch/logs/run1_forecast.csv replay/submission/forecast_2026-11-06.csv && echo "BYTE-IDENTICAL"
echo "== sweeps $(date)"
export PYTHONPATH=. OMP_NUM_THREADS=2 MKL_NUM_THREADS=2
python3 scratch/sweep_dev.py scratch/lastval_cal.json '{"calibrate.gamma":[0.5]}' > scratch/logs/fix_lastval.log 2>&1 &
python3 scratch/sweep_dev.py scratch/chronos2_grp.json '{"models.0.params.width":[0.5]}' > scratch/logs/fix_c2grp05.log 2>&1 &
wait; echo "== done $(date)"
