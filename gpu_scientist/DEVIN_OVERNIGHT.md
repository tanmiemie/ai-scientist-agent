# Devin: overnight queue (work through in order, keep going until done)

You can run all night; the user is asleep. Work through these tasks in order. Each task gets its own
branch `devin/<task-slug>` and its own PR into `devin/gpu-scientist-handoff`; do not wait for review
between tasks (branch each new task from `devin/gpu-scientist-handoff`, not from the previous task).

Global rules (from HANDOFF_DEVIN.md, still binding):
- Never change `submission_final/` or `experiments_final/`. Never push to `devin/gpu-scientist-handoff` directly.
- Never choose a spec or parameter from HOLDOUT or TEST numbers. Do not edit `config.py`, `data.py`,
  `evaluate.py`, `run_experiment.py`, `online.py` or `ledger.py`; if a task seems to need it, write
  down why in the PR and skip that part.
- API keys only from the environment; never write one to a file, log, commit or message.
- If a task fails twice for the same reason, write what happened in its PR description and move on.
- At the end, append a short "Overnight summary" to `FINDINGS_devin.md` on the last branch, listing
  every PR with one line of result.

## 1. LLM proposer walk-forward, three repeats  (branch `devin/llm-walkforward`)
Do `DEVIN_LLM_RUN.md`, then repeat the full walk-forward twice more (`--run llm_openai_r2`, `_r3`).
LLM replies vary, so report mean and spread of the per-slice TEST gain over the three runs next to the
heuristic run. Count API calls and refused proposals.

## 2. Wider walk-forward evidence  (branch `devin/walkforward-wide`)
Write `walkforward_wide.py` (a copy of `walkforward.py`, do not edit the original) with six slices whose
TEST weeks start on Sep 29, Oct 3, Oct 10, Oct 14, Oct 17 and Oct 24 (DEV always starts 2026-09-15,
GATE = the 7 days before TEST, TEST = 7 days; overlapping TEST weeks are fine, say so).
Run it with the heuristic proposer, 12 iterations per slice. Report: per-slice seed vs final TEST,
mean gain, number of slices improved, and a sign test p-value. Plot like `walkforward.png`.

## 3. Leakage and determinism tests  (branch `devin/tests`)
Add `tests/` with pytest:
- `test_no_lookahead`: for a few series and origins, multiply every raw value dated after the origin
  by 3 (and separately delete those rows), rebuild the Panel, and assert that `online.run` forecasts
  for that origin are bit-identical, for every registered non-heavy model and for spec 04.
- `test_determinism`: run spec 04 twice over a short window; forecasts identical.
- `test_edge_ties`: feedback with y exactly equal to q10/q90 counts as inside (the tie fix).
- `test_submission_valid`: `submission_final/forecast_2026-11-06.csv` passes the starter `scorer.py`
  in `--frozen-cutoff 2026-11-06` mode with 0 validation problems and has 111 rows.
Add a `Makefile` target or `run_tests.sh`; put the passing output in the PR description.

## 4. Provider-mix hypothesis  (branch `devin/provider-mix`)
DEV EDA (`scratch/dev_provider_eda.py`): when providers join during a 7-day fall, the price rises
afterwards 63% of the time (n=127). Implement `models/m_provider_mix.py` (new file; uses
`ctx.raw().n_providers`, data up to the origin only): a momentum-style model that shifts the median and
upper edge up after a fall that coincided with more providers. Choose its parameters on DEV only in
a scratch sweep. Then let the loop judge it: run `autoresearch.py --proposer heuristic` and, if the key
works, `--proposer llm`, each in its own `GPU_EXPERIMENTS` ledger seeded with `specs/04_momentum.json`,
6 iterations. Report whether any proposal using it passed the gate, and its TEST effect via a
walk-forward run. A clear negative result is fine.

## 5. Long-horizon value view, 2-3 years  (branch `devin/long-horizon`)
Write `LONG_HORIZON.md` (2-3 pages, with 2-3 charts in `long_horizon/`) answering: what will an H100 and
an A100 rent for, and resell for, in 2028-2029, with ranges and the reasoning. Use the pack's
`capability/` (e.g. the capability ladder; H100 vs A100 relative throughput), `hardware_fundamentals/`,
`index_prints.csv`, `aggregator_medians.csv` and the trend in our rental series; use web sources for
resale and new-generation prices (B200/B300, Rubin) and cite every source with a link and date. Keep
instrument classes separate. State assumptions, give low/base/high cases, and say what would change
the view. Never present an estimate as data. Respect the pack's `ATTRIBUTION.md`.

## 6. Live demo script  (branch `devin/demo`)
`demo.sh`: from a clean clone with the pack beside it, in under ~90 seconds, rebuild the series, seed a
fresh ledger with `specs/02_trend_tail_cal.json`, run 2 iterations of `autoresearch.py` (heuristic
proposer, so it needs no key), print each hypothesis, decision and lesson, and open/print the path of
`progress.png`. Add a `--llm` flag that uses the LLM proposer instead when a key is present. Time it and
put the timing in the PR.
