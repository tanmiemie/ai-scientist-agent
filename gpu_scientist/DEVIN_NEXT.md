# Devin: next two tasks (one branch and PR each, into devin/gpu-scientist-handoff)

Rules from HANDOFF_DEVIN.md still apply. Read EDA.md, SIGNIFICANCE.md (if merged) and HONEST_EVAL.md first.
New since last time: run_experiment.py records provenance and commits forecast_all.csv.gz per experiment.

## A. One new signal: GetDeploying weekly medians  (branch `devin/signal-aggregator`)
`aggregator_medians.csv` (weekly medians from an independent aggregator) is in the pack and unused.
Hypothesis to test: when the aggregator's latest weekly median for the same GPU (and a matching
instrument class, never mixing classes) sits above our series' last value, our series tends to move up
within 7 days, and vice versa.
1. DEV-only EDA in `scratch/`: align each headline series with the aggregator series it can be matched
   to (state the mapping and how many series match), using only weeks published on or before each origin
   (check the file's date semantics and any publication lag, and say what you assumed).
2. If DEV shows a signal, implement `models/m_aggregator.py` (new file, data up to the origin only; read
   the CSV once and cache it), choose parameters on DEV in a scratch sweep, then run ONE experiment through
   `run_experiment.py` in a copy of `experiments_final` (GPU_EXPERIMENTS), parent exp_007.
3. Report DEV and HOLDOUT, per-series Wilcoxon vs exp_007 (see significance.py), and the per-collector
   HOLDOUT split (see honest_eval.py). Do not change experiments_final/ or submission_final/.
A clear negative result is fine.

## B. Long-horizon value view: CANCELLED, Claude is writing LONG_HORIZON.md. Skip this task.

(Original text kept for reference.)
DEVIN_OVERNIGHT.md task 5, unchanged. Keep rental and resale strictly separate: rental prices and
utilisation inform the economics behind resale value but are different markets. Cite every web source
with link and date; low/base/high cases; say what would change the view.
