# Findings: an AI scientist for GPU rental prices

Track 2 (Pacific), direction A with parts of B. Built during the SF AI Research Hackathon, 14–15 Nov 2026.

## Question

1. **Short horizon (scored):** what will posted GPU rental prices be 1, 3 and 7 days after 6 November 2026, as 0.1 / 0.5 / 0.9 quantiles, for the 37 headline series of the Pacific data pack?
2. **Can a system improve its own forecasts** by forming hypotheses from its errors, testing them, and keeping only what survives data it has not seen?
3. **2–3 years (argued, not scored):** what will H100 and A100 rent and resell for in 2028–2029?

## Method

- **Forecaster.** Quantile models (recent-window empirical tails, momentum, step hazard, leader–follower, ensembles) run walk-forward one day at a time, as if live. A fast online loop updates interval calibration and ensemble weights from each realised error (`online.py`).
- **Research loop (`autoresearch.py`).** Each iteration: read the champion's automatic error diagnosis and the ledger of past hypotheses and lessons → (optionally) search the web with **Exa** for a method and for dated market news → propose one hypothesis as a JSON spec, with an optional parameter sweep scored on DEV only → run it through the official `scorer.py` → keep it only if DEV improves by ≥ 0.002 and HOLDOUT does not fall → write the lesson into the ledger → write `REPORT.md`. The proposer is rule-based or an LLM (GPT-4.1); it never runs its own code.
- **Guards.** Data after an origin is invisible (a test multiplies or deletes it and requires identical forecasts); DEV = origins 15 Sep–15 Oct, HOLDOUT = 16–30 Oct, never used to tune; immutable forecasts with SHA-256 provenance; an LLM reviewer ensemble flags weak results but cannot overrule the gate.

## Evaluation

Official `scorer.py`: pinball loss at 0.1/0.5/0.9, skill vs the last value, pooled over series. We also report per-series tests (Wilcoxon), scale-free aggregates (median, geomean), coverage, cluster-bootstrap intervals (`uncertainty.py`, 2,000 resamples of whole series or whole origin days), and walk-forward slices whose TEST week no decision ever saw (`walkforward.py`).

## Results, with uncertainty

| | DEV (selection) | HOLDOUT (gate only) |
|---|---|---|
| Champion (exp_007) pooled skill vs last value | +0.191, 95% CI +0.13 to +0.23 | **+0.101, 95% CI +0.02 to +0.17** (by series); +0.06 to +0.13 (by day) |
| Gain over the starter drift baseline | +0.119, CI +0.07 to +0.16 | +0.057, CI −0.05 to +0.13 (not significant) |
| Interval coverage (target 0.80) | 0.79 | 0.76 |
| Series where champion beats last value (Wilcoxon) | 30 / 6, p = 0.0003 | **27 / 7, p = 0.006** |
| Skill by horizon 1 / 3 / 7 days | +0.04 / +0.15 / +0.24 | +0.07 / +0.10 / +0.11 |

- **Self-improvement on unseen weeks.** Starting from the drift baseline each time: rule-based scientist +0.053 mean TEST gain over 6 weekly slices (5 of 6 improved, sign test p = 0.11); LLM scientist +0.042 over 3 slices (3 of 3).
- **Memory ablation** (same budget, 2 runs per arm): with the lesson ledger +0.044 mean TEST gain, without it +0.035; the runs overlap, so the score difference is not significant. The mechanism is clear: without memory the LLM re-proposed already-rejected ideas 17 times and lost 4 iterations; with memory, once.
- **Honest negatives.** The champion's gain over the starter drift is not significant per series on HOLDOUT (p = 0.52); online calibration lifted pooled skill but cut HOLDOUT geomean from 0.14 to 0.06 (it favours expensive GPUs); on series selectable before HOLDOUT, plain trend tails beat the champion. Foundation models (Chronos-Bolt, Chronos-2, Timestral) lost on DEV. A published market index (GIX) does not lead our series' direction (466 pairs, Spearman 0.09). The GetDeploying weekly median as a signal (exp_008, `experiments_aggregator/`) passes the gate (DEV +0.196, HOLDOUT +0.102) but the gain is within noise (HOLDOUT 20/17 series, p = 0.14), was the best of 64 DEV settings, and comes mostly from providers joining or leaving the aggregator; not submitted.

Submitted file: `gpu_scientist/submission_final/forecast_2026-11-06.csv` (exp_007, 111 rows, valid under the scorer's frozen-cutoff check; SHA-256 in `MANIFEST.json`).

## What the system learned across iterations

1. **The last price is the best median; the value is in the interval.** The biggest single gain (+0.096 DEV) came from a recent 60-day window with room above the last value; 1-day skill stays near +0.04.
2. **Calibrate by collector × instrument class, not by GPU model.** Per-GPU calibration led on DEV (+0.191) and collapsed on HOLDOUT (+0.022): caught by the gate and by the reviewer.
3. **Rises continue, if they are real repricing.** After a rise, 68.5% of series end higher (n = 1,281), but 45% of 10%+ moves happen on days a provider joined or left, and those are 7× larger. Momentum only on days the provider count is unchanged (exp_007) is the economic distinction between *repricing* and *composition change*.
4. **Memory changes the search, not yet the score.** The ledger stops the loop from repeating rejected ideas.

## Economic insight: the 2–3 year view (`gpu_scientist/LONG_HORIZON.md`)

| Nov 2028 (base, range) | rent $/GPU-hr | used module resale |
|---|---|---|
| H100 | 2.32 (1.27–3.18) | $8,000 ($3,600–12,100) |
| A100 | 1.19 (0.59–1.65) | $2,600 ($1,100–4,400) |

- **Rent and resale are different markets and are forecast separately.** Over the past year, posted A100 rent rose 23% while A100 resale fell about 35%.
- **The gap between generations is not a depreciation rate.** Across generations rent is 25–26% lower per year of age, yet over the same year A100 and H100 rents moved between −32% and +33% by pricing mode.
- **Posted is not transacted.** Transacted A100 is about a third below posted; H100 matches.
- **Resale buyers are more cautious than rent markets.** Discounting the base rent path at 15% gives $33,200 per H100 in a node against $24,400 realised; matching it takes a 34% discount rate.
- **Power availability, not power price, protects old GPUs.** Doubling electricity prices lifts the H100 cash floor by only 7 cents an hour; what keeps A100s and H100s rented is that their halls cannot host liquid-cooled racks.
- Direction-B sources used: NVIDIA roadmap, Epoch AI hardware and MLPerf capability units, BLS electricity index, provider-tier prints, forward curves.

## Reproduce

```
git clone https://github.com/tanmiemie/ai-scientist-agent && cd ai-scientist-agent/gpu_scientist
python3 -m pip install duckdb pandas numpy pyarrow matplotlib tabulate
GPU_PACK=/path/to/gpu-price-pack-v0.1.1-handover bash run_all.sh   # about 2 minutes: rebuilds series, replays every experiment, writes the submission
sha256sum replay/submission/forecast_2026-11-06.csv submission_final/forecast_2026-11-06.csv   # identical
```

Live demo of the autonomous loop: `bash demo.sh` (rule-based) or `bash demo.sh --llm`; with Exa: `python3 autoresearch.py --proposer llm --exa --iters 3` (needs `OPENAI_API_KEY`, `EXA_API_KEY`).

Data: Pacific gpu-price-pack v0.1.1 (CC BY 4.0), see `gpu_scientist/ATTRIBUTION.md`. Built with Claude (research lead), Devin (runs and reviews) and GPT-4.1 (proposer in the loop).
