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
   Data rules for this file (added): weeks are Monday-dated and each value is the median of that week's
   daily captures, so a week is usable only at origins on or after week_start + 7 days. The whole file
   was retrieved on 2026-11-07, so past weeks may be a later vintage than what was public at the origin:
   say so in the report. Never interpolate weekly values to daily. The median counts every listing, so
   it moves when providers join or leave (`n_providers`, `n_offerings`): test the signal both with and
   without weeks where `n_providers` changed.
3. Report DEV and HOLDOUT, per-series Wilcoxon vs exp_007 (see significance.py), and the per-collector
   HOLDOUT split (see honest_eval.py). Do not change experiments_final/ or submission_final/.
A clear negative result is fine.

## C. Memory ablation  (branch `devin/memory-ablation`, after A or in parallel)
Question: does the ledger of past hypotheses and lessons make the LLM research loop better, at the same
budget? `autoresearch.py` and `walkforward.py` now take `--no-memory` (the proposer then sees only the
champion and its diagnosis; exact duplicate specs are still refused).
1. Run the 3-slice walk-forward twice with the LLM proposer, same model, seed and `--iters 6`:
   `python walkforward.py --proposer llm --provider openai --iters 6 --run llm_mem`
   `python walkforward.py --proposer llm --provider openai --iters 6 --run llm_nomem --no-memory`
   If the budget allows, repeat each once more (LLM runs are not deterministic) and report both.
2. Report per slice: TEST skill of the final champion, number of accepted / rejected / refused
   iterations, and how many proposals repeated an idea already rejected in that slice (judge from the
   hypotheses; list them). Write `walkforward/MEMORY_ABLATION.md`. A null result is fine; say so plainly.
   Do not change experiments_final/ or submission_final/.

## D. Reviewer ensemble  (branch `devin/reviewer`, after C)
Borrowed from Sakana's AI Scientist (perform_review: 5 reviewers, reflection, low temperature), but
the reviewer FLAGS and never overrules the numeric gate.
1. New `review.py`: for one experiment, give an LLM the hypothesis, spec diff, DEV/HOLDOUT reports,
   per-horizon and per-group skill, coverage, and the diagnosis. Ask for JSON on a fixed checklist:
   leakage risk, gain carried by a few large series, interval widened rather than better centred,
   gain below 0.005 (noise), coverage fell, passed on HOLDOUT by a hair (within 0.002), overlap with an
   idea already rejected in the ledger, other. Each item: yes/no, evidence, severity 1–3.
   Use a sceptical system prompt ("if unsure, flag it"); add one area-chair call that reads the 5
   reviews and writes the meta-review.
2. Ask 5 times at temperature 0.1 (API key from the environment only) and keep an item if at least 3
   of 5 flag it. Write `<exp>/review.json`; `report.py` should print the kept flags if the file exists.
3. Run it on experiments_final exp_001 to exp_007 in a COPY of the folder and report whether the flags
   agree with what we know (exp_005 overfit per-GPU calibration; exp_006 Chronos lost on DEV).
   Do not change experiments_final/ or submission_final/.

## E. Let the LLM write a model, not only tune one  (branch `devin/llm-coder`, after D)
Today the proposer can only edit a JSON spec. Add a code path, following Sakana's coder loop:
1. The proposer may return {"new_model": {"name": ..., "code": ...}} written against
   `models/m_template.py`. Save it as `models/m_<name>.py`; keep every attempt as
   `<exp>/attempt_<i>.py` (snapshot before each run).
2. Hard gates, in order, before the experiment counts: imports only numpy/pandas/scipy and our
   modules (AST check: no os, subprocess, socket, open, eval, exec, __import__); the model's
   `predict` runs on 20 random (series, origin) pairs within 5 s; `tests/test_no_lookahead.py`
   passes with the new model added to the specs it checks (data after the origin multiplied by 3 or
   deleted must give identical forecasts). On failure, feed the last 1,500 characters of the error
   back and retry, at most 3 times.
3. Run it in a sandbox: Devin's VM is fine, no network for the generated code, timeout per run.
4. Then it goes through the normal DEV sweep and HOLDOUT gate. Report how many generated models
   passed each gate and whether any was accepted. Do not change experiments_final/ or submission_final/.

## F. Ideas in batches  (branch `devin/idea-batch`, after E)
1. Turn the hypothesis menu in RESEARCH_PROTOCOL.md into machine-readable `seed_ideas.json`.
2. Each iteration the LLM proposes 5 ideas, scores each 1–10 on expected gain (from the diagnosis'
   biggest miss), feasibility and novelty vs the ledger, reflects once, and the loop runs only the
   top one. Keep all ideas, run or not, in `<experiments>/ideas.json`.
3. Compare with the current one-idea loop on the 3-slice walk-forward at equal number of runs.

## B. Long-horizon value view: CANCELLED, Claude is writing LONG_HORIZON.md. Skip this task.

(Original text kept for reference.)
DEVIN_OVERNIGHT.md task 5, unchanged. Keep rental and resale strictly separate: rental prices and
utilisation inform the economics behind resale value but are different markets. Cite every web source
with link and date; low/base/high cases; say what would change the view.
