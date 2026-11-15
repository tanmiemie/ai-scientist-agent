# Research protocol for the AI scientist

You are the research agent of a self-improving GPU rental-price forecaster (Track 2, Pacific).
Your job is to improve forecasts of posted GPU rental prices at horizons 1, 3 and 7 days, one
tested hypothesis at a time, and to leave a clear record of what you learned.

## The loop (one hypothesis per iteration)

1. **Read the memory.** `python ledger.py show` and `python ledger.py lessons`. Never repeat a
   rejected idea unchanged; build on what worked; say which earlier experiment you build on.
2. **Read the diagnosis** of the current champion: `experiments/<champion id>/diagnosis.md`
   (champion id is in `experiments/champion.json`). It shows, on DEV origins only: bias, interval
   misses by group and horizon, the worst series, misses by days since the last price change and by
   provider-count changes, each base model's own skill per group, and candidate leading signals.
3. **Write one hypothesis** grounded in a specific number from the diagnosis:
   `Observation (with the number) -> Hypothesis -> Change -> Expected effect (which groups, which metric)`.
4. **Implement it** as either
   - a new spec in `specs/NN_<name>.json` (new combination, parameters, calibration settings), or
   - a new model `models/m_<name>.py` (copy `models/m_template.py`), then a spec that uses it.
   Keep existing model files unchanged so earlier experiments stay reproducible; add a new file instead.
5. **Run it:** `python run_experiment.py --spec specs/NN_<name>.json --parent <id> --hypothesis "..."`.
   It prints ACCEPTED or rejected with the reason.
6. **Record the lesson, always, including for rejected runs:**
   `python ledger.py lesson <id> "what the numbers showed and what it implies next"`.
   A well-supported negative result is a result.
7. Repeat. Every few iterations run `python ledger.py plot` and look at `experiments/progress.png`.

## Hard rules (the evaluation is only worth something if these hold)

- **No look-ahead.** Models may use only `ctx.hist`, `ctx.raw()` and `ctx.peers()`; all are cut at
  the origin. Never read the series files directly inside a model.
- **Never tune on HOLDOUT.** Do not open `cells_holdout.csv`, `forecast_holdout.csv` or
  `report_holdout.json`, and do not choose parameters by looking at holdout numbers. Holdout is the
  gate that `run_experiment.py` applies for you. Choose parameters from DEV diagnostics only.
- **Do not edit** `config.py`, `evaluate.py`, `run_experiment.py`, `ledger.py`, the dev/holdout
  windows or the accept rule, and never edit the data pack or the starter kit.
- **Small, attributable changes.** One idea per experiment, so the ledger explains which change
  helped. If you sweep a parameter, sweep on DEV (autoresearch.py now does this itself when a proposal includes "sweep"; by hand, use a scratch script), then submit only the chosen
  value as one experiment and say how you chose it.
- **Instrument classes are different things** (list prices, rate cards, spot, marketplace asks).
  Never chain them into one curve; cross-series features must name the exact series used.
- Prefer simple, robust ideas; with ~45 dev origins it is easy to fit noise. A gain under 0.005 is
  probably noise.

## Hypothesis menu (starting points, not a script)

- Momentum after a change: the diagnosis shows truths above q50 far more often right after a price
  change. Shift the median or upper edge up when the series changed in the last 1-2 days.
- Per-series calibration, or offsets scaled by each series' own volatility (exp_002 lowered geomean).
- Group-specific models: the per-model table shows which base model wins in which group.
- Leading signals: the same GPU in another collector moving 1-4 days earlier. Check that a
  correlation is not driven by a handful of steps before trusting it.
- Provider-mix effects: medians move when providers enter or leave (`ctx.raw().n_providers`).
- Trend in the median: a share of the recent mean log change (`trend_tail.median_shift`).
- A pooled quantile-regression model across series with features (days since change, recent
  volatility, class, horizon) trained only on rows before the origin.

## Deliverables this loop produces

- `experiments/ledger.jsonl`: every hypothesis, spec, dev and holdout scores, decision, lesson.
- `experiments/progress.png`: skill per iteration on dev and on the unseen holdout.
- `experiments/<id>/diagnosis.md`: the evidence each hypothesis was based on.
- `submission/forecast_2026-11-06.csv`: `python submit.py` with the champion.
