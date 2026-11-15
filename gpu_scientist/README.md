# gpu_scientist: a self-improving forecaster of posted GPU rental prices

Track 2 (Pacific, "An AI Scientist for GPU Value"). Forecasts the 0.1/0.5/0.9 quantiles of posted
rental prices 1, 3 and 7 days ahead, and improves itself in two loops:

- **Fast loop (`online.py`, no AI).** Walks forward one day at a time as if live. When a target date
  arrives it compares the forecast with the truth and updates (a) per-group interval calibration
  toward 10% misses on each side and (b) ensemble weights from recent pinball loss.
- **Research loop (an AI agent following `RESEARCH_PROTOCOL.md`).** Reads an automatic error
  diagnosis, proposes one hypothesis, implements it as a model or spec, runs it, and keeps it only
  if it beats the champion on DEV and does not lose on the unseen HOLDOUT. Every run and its lesson
  goes into `experiments/ledger.jsonl`.

## Layout

| file | role |
|---|---|
| `config.py` | paths, horizons, DEV (Sep 15 to Oct 15) and HOLDOUT (Oct 16 to Oct 30) origin windows, accept rule |
| `data.py` | builds series with the starter kit; leak-free `Ctx` (history cut at the origin) |
| `models/` | model library, one file per model, auto-registered (`m_template.py` to start a new one) |
| `online.py` | the walk-forward fast loop: forecast, combine, calibrate, learn from realised errors |
| `evaluate.py` | scores with the starter kit's own `scorer.py` |
| `diagnose.py` | error health check on DEV: bias, misses by group/horizon/state, per-model skill, leading signals |
| `run_experiment.py` | one hypothesis end to end + accept/reject + ledger |
| `ledger.py` | memory: show, lessons, plot |
| `submit.py` | Sunday file: champion, origin 2026-11-06, horizons 1/3/7 |
| `specs/` | experiment specs (JSON) |
| `run_all.sh` | one command: rebuild series, replay every spec in order, write the submission |

## Quickstart

Put this folder next to `gpu-price-pack-v0.1.1-handover/` (or set `GPU_PACK=/path/to/pack`).

```
python3 -m pip install duckdb pandas numpy pyarrow matplotlib tabulate
bash run_all.sh                      # rebuild everything from the pack and write the submission
python3 ledger.py show               # what has been tried
```

## Interactive app

```
python3 -m pip install -r app/requirements.txt
GPU_PACK=/path/to/pack OPENAI_API_KEY=... streamlit run app/main.py
```

Browse every ledger (overview, research timeline, diagnosis, forecast explorer, walk-forward, proposer log,
submission) and, in **Lab**, design an experiment by hand, launch `autoresearch.py` or `walkforward.py`, and watch
the log live. Lab runs go to `experiments_app/` and `walkforward/app_*/` (git-ignored), never the tracked ledgers.
The results pages work without the data pack; Lab needs it.

## Autonomous loop (no human in it)

`autoresearch.py` closes the research loop. Each iteration it reads the ledger (with lessons) and the
champion's diagnosis, a proposer writes one hypothesis plus the spec that tests it, the spec is
validated (registered models and parameters only, never a repeat), `run_experiment.run()` scores it
with the official scorer and applies the fixed accept rule, and the proposer writes the lesson.

```
python3 autoresearch.py --iters 6 --proposer heuristic                    # offline, rule-based scientist
OPENAI_API_KEY=... python3 autoresearch.py --iters 6 --proposer llm --provider openai
ANTHROPIC_API_KEY=... python3 autoresearch.py --iters 6 --proposer llm --provider anthropic
```
Set `GPU_EXPERIMENTS` to keep an autonomous run in its own ledger. Prompts and replies are logged in
`autoresearch_log.jsonl`. The proposer recombines and retunes registered models; it does not write code.

`walkforward.py` checks that the improvement is real. Three slices each pretend to be an earlier date:
the loop starts from the starter drift and iterates on DEV and GATE origins up to that date, and every
champion it produces is scored on the following TEST week, which no decision saw.

Heuristic proposer, 6 iterations per slice (`walkforward/heuristic_demo/`):

| slice | test week | seed (drift) TEST | final champion TEST | gain |
|---|---|---|---|---|
| S1 | Oct 10-16 | +0.145 | +0.194 | +0.049 |
| S2 | Oct 17-23 | +0.022 | +0.107 | +0.086 |
| S3 | Oct 24-30 | +0.077 | +0.044 | -0.034 |

Mean +0.034, 2 of 3 slices improved. In S3 the loop's first accepted change (online calibration)
helped on DEV and GATE but not in the following week; that is reported as is.

## Changelog

- **Calibration tie fix (`online.py`, EDGE_TOL).** Posted prices often equal the last value, which is
  also q10 (or q90). The calibration step compared `y < q10` exactly, so the last-bit rounding of
  exp/log decided about 1,500 of 6,300 feedback events, and two machines with the same data learned
  different offsets (Mac vs Devin: 43/111 submission rows differed, dev +0.1742 vs +0.1831 for the
  same spec). Ties now count as inside the interval. Replay after the fix: exp_002 dev +0.1833 /
  holdout +0.0970; exp_004 (momentum) now passes the gate (dev +0.0039, holdout +0.0032) and becomes
  champion; exp_005 is still rejected (holdout -0.0786). Ledgers in `experiments/` and
  `experiments_devin/` predate the fix; `run_all.sh` regenerates the corrected one.

## Optional: Chronos-Bolt (pretrained time-series model)

`models/m_chronos.py` wraps Amazon's Chronos-Bolt, zero-shot. It needs extra packages and a
one-time weight download from Hugging Face, so its specs live in `specs/optional/` (not replayed
by `run_all.sh`). Run them in this order, one experiment each:

```
pip install chronos-forecasting
python3 run_experiment.py --spec specs/optional/10_chronos_alone.json --parent <champion id> \
  --hypothesis "$(python3 -c "import json;print(json.load(open('specs/optional/10_chronos_alone.json'))['_hypothesis'])")"
# then 11_chronos_last_median.json and 12_ensemble_trend_chronos.json the same way
```

The plumbing was smoke-tested offline with `"model_id": "__fake__"`; the real weights have not been
run yet. If a Chronos spec is accepted, copy it into `specs/` so `run_all.sh` reproduces it.

## Results so far (scorer.py, 37 headline rental series, daily origins)

| exp | idea | dev pooled | holdout pooled | coverage (dev) | decision |
|---|---|---|---|---|---|
| 000 | starter drift (reference) | +0.071 | +0.044 | 0.46 | start |
| 001 | recent 60-day window + one-step upper floor | +0.168 | +0.090 | 0.64 | accepted |
| 002 | + online per-group calibration | +0.174 | +0.098 | 0.80 | accepted (champion) |
| 003 | hedge ensemble with step-hazard and 30-day drift | +0.173 | +0.107 | 0.80 | rejected on dev |

Skill is versus the flat last value. Data: gpu-price-pack v0.1.1-handover (CC BY 4.0); keep its
`ATTRIBUTION.md` with this work.
