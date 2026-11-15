# Handoff to Devin: run the research loop on `gpu_scientist`

## 1. Context in one paragraph

Hackathon Track 2 (Pacific, "An AI Scientist for GPU Value"). We forecast **posted GPU rental
prices** 1, 3 and 7 days ahead as 0.1/0.5/0.9 quantiles. The data pack ends on **2026-11-06**;
on **Sunday 15 Nov** organisers score our forecasts from origin 2026-11-06 (targets 7, 9 and 13 Nov)
with the starter kit's `scorer.py` (pinball loss; skill = 1 - loss / last-value loss; interval
coverage target 0.8). Judges care less about the leaderboard and more about **a system that improves
itself across iterations, with leak-free evaluation and a clear record of what it learned**.
Well-supported negative results count.

## 2. What already exists

`gpu_scientist/` is a working framework (read `README.md`, then `RESEARCH_PROTOCOL.md`):

- `online.py`: walk-forward fast loop over daily origins; learns per-group interval calibration and
  ensemble weights from realised errors.
- `run_experiment.py`: one hypothesis -> official scorer on DEV (origins 2026-09-15..10-15) and
  HOLDOUT (10-16..10-30) -> automatic diagnosis -> accept only if DEV skill_pooled >= champion + 0.002
  and HOLDOUT >= champion -> appended to the ledger.
- `diagnose.py` writes `experiments/<id>/diagnosis.md` (bias, misses by group/horizon/state,
  per-model skill, candidate leading signals). **Every hypothesis must start from a number in it.**
- `models/`: `last_value`, `drift`, `trend_tail`, `step_hazard`, `chronos` (optional, needs
  `chronos-forecasting`). New model = new file from `models/m_template.py`.
- `submit.py`: writes `submission/forecast_2026-11-06.csv` from the champion.

Scored universe: the 37 `headline` rental series of the catalog built at as_of 2026-11-06 (AWS spot
is excluded: it has no November truth).

Results so far (skill_pooled vs last value):

| exp | idea | dev | holdout | dev coverage | decision |
|---|---|---|---|---|---|
| 000 | starter drift | +0.0714 | +0.0437 | 0.46 | start |
| 001 | 60-day window + one-step upper floor (`trend_tail`) | +0.1677 | +0.0903 | 0.64 | accepted |
| 002 | + online per-group calibration | +0.1742 | +0.0975 | 0.80 | **champion** |
| 003 | hedge ensemble (trend_tail, step_hazard, drift_30) | +0.1731 | +0.1067 | 0.80 | rejected (dev) |

## 3. Setup

1. Layout: the data pack folder `gpu-price-pack-v0.1.1-handover/` must sit **next to**
   `gpu_scientist/` (or `export GPU_PACK=/abs/path/to/gpu-price-pack-v0.1.1-handover`).
   The pack is ~285 MB zipped; it is provided separately (not in git). Do not modify it.
2. `pip install duckdb pandas numpy pyarrow matplotlib tabulate`
3. **Check reproduction first:** `bash run_all.sh` (about 1 minute). It replays `specs/*.json` into
   `replay/` and must print the four rows of the table above (to 4 decimals). If it does not, stop
   and report the difference before doing anything else.
4. Use your **own ledger** so you never collide with the other agent working in parallel:
   `export GPU_EXPERIMENTS=$PWD/experiments_devin GPU_SUBMISSION=$PWD/submission_devin`
   (set these in every shell). Seed it with the current champion:
   `python run_experiment.py --spec specs/02_trend_tail_cal.json --hypothesis "seed: current champion (exp_002 of the main ledger)"`

## 4. Your task: 6 research iterations

Follow `RESEARCH_PROTOCOL.md` exactly: one hypothesis per experiment, grounded in a number from the
latest champion's `diagnosis.md`; implement as a new spec in `specs/` or a new `models/m_*.py`; run
`run_experiment.py --parent <id> --hypothesis "..."`; then **always** `python ledger.py lesson <id> "..."`,
including for rejected runs.

Suggested order (adapt if the diagnosis points elsewhere, and say why):

1. **Momentum after a change.** In exp_001's diagnosis, cells whose series changed price in the last
   0-1 days had truth above q50 in 62% of cases (50% if unbiased) and above q90 in 32%. Test shifting
   the median and/or upper edge up when the last change was recent (new model, e.g. `m_momentum.py`,
   or a parameter on a copy of trend_tail).
2. **Volatility-aware calibration.** exp_002's calibration raised coverage to 0.80 but dropped
   skill_geomean from 0.166 to 0.105, i.e. it over-widens quiet series. Test scaling the learned offsets
   by each series' own recent volatility, or calibrating per series with a group prior.
3. **Chronos-Bolt (optional, time-box ~1 hour).** `pip install chronos-forecasting`, then run
   `specs/optional/10_chronos_alone.json`, `11_chronos_last_median.json`, `12_ensemble_trend_chronos.json`
   in that order (hypotheses are inside the files). A clear negative result is fine.
4. **Leading signals across collectors.** The diagnosis lists same-GPU pairs with |corr| up to 0.93 at
   lags 1-4 days, several negative. Before using any, check how many non-zero moves drive each
   correlation; record pairs you reject and why.
5. **Provider-mix effect.** Medians move when providers enter or leave (`ctx.raw().n_providers`).
6. Your own idea from the diagnosis.

Stop early if three consecutive experiments are rejected; write up why.

## 5. Hard rules

- Never open `*_holdout.*` files or choose parameters from holdout numbers; the accept rule does that.
- Do not edit `config.py`, `data.py`, `evaluate.py`, `run_experiment.py`, `ledger.py`, the data pack
  or the starter kit. Do not edit existing model files; add new ones.
- Models may only use `ctx.hist`, `ctx.raw()`, `ctx.peers()` (all cut at the origin).
- Never chain different instrument classes (list, rate card, spot, marketplace ask) into one curve.
- Parameter sweeps: do them on DEV in a scratch script, then run only the chosen value as one
  experiment and state how it was chosen. Gains under ~0.005 are likely noise; say so.
- If a run errors, fix your own new file; do not loosen the rules or the accept gate.

## 6. Deliverables (commit to branch `devin-research`)

1. `experiments_devin/` (ledger.jsonl with a lesson on every row, each experiment's spec.json and
   diagnosis.md; large forecast/cell CSVs may be left out if the repo gets heavy).
2. New files in `models/` and `specs/` you created. If you change the champion, also copy its spec into
   `specs/` with the next number so `run_all.sh` reproduces it.
3. `python ledger.py plot` -> `experiments_devin/progress.png`.
4. `python submit.py` -> `submission_devin/forecast_2026-11-06.csv` (111 rows: 37 series x 3 horizons).
5. `FINDINGS_devin.md`, one page: a table of every experiment (id, hypothesis, dev, holdout, coverage,
   decision), the lessons, what the system learned about GPU rental prices, which champion you
   recommend for Sunday and why, and anything that looked suspicious.

## 7. Open questions (do not block on them; note assumptions)

- Which aggregate ranks teams (pooled, median, geomean)? We optimise pooled and report all three.
- Will Sunday score exactly these 37 series? Unknown; `submit.py --scope all` covers every rental
  series still being collected, but extra series also carry risk, so keep `headline` unless told otherwise.

Data: gpu-price-pack v0.1.1-handover, CC BY 4.0; keep its `ATTRIBUTION.md` with any shared work.
