# An AI scientist for GPU rental prices

**SF AI Research Hackathon · Track 2 (Pacific): Recursive Self-Improvement · also entered: Exa challenge**

## The problem

GPUs are now financed, leased and traded like long-lived assets, yet nobody has a reliable price for them. Rental prices are posted by dozens of providers, change in jumps, and differ by 10–40% between data sources; real transaction prices are private. Lenders, data-centre builders and compute buyers need two numbers:

- **Next week:** what will an hour of H100 or A100 time cost, and how sure can we be?
- **In 2–3 years:** what will these GPUs rent and resell for, which decides whether a loan or a data centre pays back?

Forecasting this by hand does not keep up: the market changes every week, and a model that worked last month quietly stops working.

## Our solution

An **AI scientist** that forecasts posted GPU rental prices and keeps improving its own forecasts the way a research team would, without a human in the loop.

- It forecasts a range, not a single number: a low, a middle and a high price (10th, 50th, 90th percentile) for 1, 3 and 7 days ahead, across 37 price series.
- It checks its own mistakes every day and widens or narrows its ranges to stay honest: about 8 in 10 real prices land inside the range, as intended.
- It explains itself: every idea it tried, why it was kept or rejected, and what it learned is written down in a ledger and a report the system writes itself.

## How it improves itself

Each research round runs on its own:

1. **Diagnose:** find where its forecasts miss most (by GPU, provider type, horizon).
2. **Look outside:** search the web with **Exa** for forecasting methods and for GPU market news published before the data cutoff, and cite the sources it uses.
3. **Propose:** an LLM (or a rule-based scientist) turns the diagnosis and evidence into one testable idea.
4. **Test fairly:** score the idea with the organisers' scorer on past weeks; tune it on one period only.
5. **Keep or reject:** adopt it only if it also holds on weeks it never tuned on. This gate rejected an idea that looked best but would have failed in practice.
6. **Remember:** write the lesson down so it does not repeat failed ideas. Without this memory it re-proposed rejected ideas 17 times; with it, once.

## How it scales up

- **More GPUs and markets:** new price series plug in through the same data pipeline; the system learns separate adjustments per provider type and collector.
- **More research per day:** each round is a short, self-contained run with a hard pass/fail gate, so many can run in parallel on cloud machines without a person checking each one.
- **New sources of evidence:** web search (Exa), market indices and hardware data enter as evidence the loop must test before it trusts them; two such signals were tested, and neither earned a place in the submission.
- **Safe autonomy:** the AI proposes settings, never runs its own code, and cannot touch the evaluation; an AI reviewer panel flags weak results for a human.
- **Longer horizons:** the same evidence base feeds the 2–3 year value model (rent, resale and their drivers), which can be updated as new data arrives.

## Results

| | Result |
|---|---|
| Forecast accuracy vs "price stays the same" on weeks never used for tuning | **10% lower error** (95% range 2% to 17%) |
| Price series where it beats "price stays the same" | **27 of 34** (statistically significant, p = 0.006) |
| Share of real prices inside its forecast range (target 80%) | 79% on tuning weeks, 76% on unseen weeks |
| Does it really improve itself? Restarted from scratch on 6 past weeks | improved on **5 of 6** unseen weeks |
| Reproducible | one command rebuilds the submitted forecast byte for byte in about 2 minutes |

**What it learned about the market:** the last posted price is the best middle guess, the value is in getting the range right, and a price rise usually continues only when it is a real repricing, not a provider joining or leaving the listings.

**2–3 year view:** in the base case an H100 still rents for about **$2.30 an hour in late 2028** and about $2 in 2029, but its used resale value falls faster, to about **$8,000** in 2028 from $14,250 today. Rent and resale are different markets: last year A100 posted rent rose 23% while A100 resale fell about 35%. Full argument with ranges and sources: [LONG_HORIZON.md](gpu_scientist/LONG_HORIZON.md).

**Honest limits:** the gain over the organisers' simple trend baseline is not statistically significant on unseen weeks; the adjustments favour expensive GPUs; posted prices are not transaction prices.

## For judges and engineers

- Findings (question, method, evaluation, results with uncertainty, what it learned): [FINDINGS.md](FINDINGS.md)
- Submission: [`gpu_scientist/submission_final/forecast_2026-11-06.csv`](gpu_scientist/submission_final/forecast_2026-11-06.csv) ([MANIFEST](gpu_scientist/submission_final/MANIFEST.json))
- Reproduce: `cd gpu_scientist && GPU_PACK=/path/to/gpu-price-pack bash run_all.sh`
- Live demo of the loop: `cd gpu_scientist && bash demo.sh` (about 1 minute, no API key needed)
- The system's own research report: [`gpu_scientist/experiments_final/REPORT.md`](gpu_scientist/experiments_final/REPORT.md)
- Where Exa is called: [`gpu_scientist/exa_scout.py`](gpu_scientist/exa_scout.py), every iteration of [`autoresearch.py`](gpu_scientist/autoresearch.py) with `--exa`; sources are logged in `autoresearch_log.jsonl`, a dated `evidence.jsonl` memory and each run's `REPORT.md`
- Rigour: [SIGNIFICANCE.md](gpu_scientist/SIGNIFICANCE.md), [HONEST_EVAL.md](gpu_scientist/HONEST_EVAL.md), [MEMORY_ABLATION.md](gpu_scientist/walkforward/MEMORY_ABLATION.md), [REVIEWER.md](gpu_scientist/REVIEWER.md)
- Code guide: [`gpu_scientist/README.md`](gpu_scientist/README.md)

Data: Pacific gpu-price-pack v0.1.1 (CC BY 4.0). Built during the event by Tania Lin with Claude, Devin and GPT-4.1 as research agents.
