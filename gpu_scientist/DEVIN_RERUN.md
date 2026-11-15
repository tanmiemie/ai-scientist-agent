# Devin: re-run after the calibration tie fix

Branch `devin/gpu-scientist-handoff` now contains commit 9c456b2, "Make calibration feedback robust to
ties at the interval edges" (`online.py`, `EDGE_TOL`; see the Changelog in README.md). That explains
the Mac-vs-VM discrepancy you reported: the data is identical, and exact `y < q10` / `y > q90`
comparisons on prices that equal the edge were decided by exp/log last-bit rounding.

## Do this, in order

1. `git pull` on `devin/gpu-scientist-handoff`. Make sure `online.py` contains `EDGE_TOL`.
2. Make sure `chronos-forecasting` is installed and the Chronos-Bolt weights load (spec 06 needs them).
3. `bash run_all.sh` (writes to `replay/`, never touches `experiments/` or `experiments_devin/`).
4. Check determinism: run `bash run_all.sh` a second time and confirm
   `replay/submission/forecast_2026-11-06.csv` is byte-identical to the first run.
5. Compare against the numbers measured on the Claude side after the fix (no Chronos there):

   | exp | spec | dev pooled | holdout pooled | decision |
   |---|---|---|---|---|
   | 000 | 00_drift | +0.0714 | +0.0437 | start |
   | 001 | 01_trend_tail | +0.1677 | +0.0903 | accepted |
   | 002 | 02_trend_tail_cal | +0.1833 | +0.0970 | accepted |
   | 003 | 03_ensemble_cal | +0.1768 | +0.1040 | rejected |
   | 004 | 04_momentum | +0.1871 | +0.1002 | accepted -> champion |
   | 005 | 05_cal_by_gpu | +0.1909 | +0.0216 | rejected |
   | 006 | 06_chronos_last_median | (not run on Claude side) | | |

   If 000-005 do not match to 4 decimals, stop and report the first row that differs.
6. Promote the replay to the official record:
   - copy `replay/experiments/` to `experiments_final/`, then add a lesson to each row with
     `GPU_EXPERIMENTS=$PWD/experiments_final python ledger.py lesson <id> "..."`
     (reuse the lessons from both earlier ledgers where they still hold; note what changed for 004)
   - copy `replay/submission/forecast_2026-11-06.csv` to `submission_final/forecast_2026-11-06.csv`
   - `GPU_EXPERIMENTS=$PWD/experiments_final python ledger.py plot`
7. Update `FINDINGS_devin.md` with a short section "After the tie fix": the new table, the new
   champion and whether you still recommend it for Sunday. Mention that momentum's gain (+0.0039 dev,
   +0.0032 holdout) is close to noise.
8. Commit to a new branch `devin/rerun-after-tie-fix` and open a PR into `devin/gpu-scientist-handoff`.
   Do not push to `devin/gpu-scientist-handoff` directly.

Rules from HANDOFF_DEVIN.md still apply (no holdout-driven choices, no edits to core files).
