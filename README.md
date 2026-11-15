# An AI scientist for GPU rental prices

**SF AI Research Hackathon, Track 2 (Pacific): Recursive Self-Improvement.** Also entered: Exa challenge.

A system that forecasts posted GPU rental prices (0.1/0.5/0.9 quantiles, 1, 3 and 7 days ahead) and improves itself the way a researcher would: it reads a diagnosis of its own errors, searches the web with Exa for methods and dated market news, proposes one hypothesis, tests it with the official scorer, and keeps it only if it also holds on weeks it never tuned on. Every decision and lesson is in a ledger, and the system writes its own research report. On top, an argued 2–3 year view of H100 and A100 rent and resale value.

- **Findings (question, method, evaluation, results with uncertainty, what it learned):** [FINDINGS.md](FINDINGS.md)
- **Submission:** [`gpu_scientist/submission_final/forecast_2026-11-06.csv`](gpu_scientist/submission_final/forecast_2026-11-06.csv) (starter-kit format, 111 rows, [MANIFEST](gpu_scientist/submission_final/MANIFEST.json))
- **One command to reproduce it:** `cd gpu_scientist && GPU_PACK=/path/to/pack bash run_all.sh`
- **The system's own research report:** [`gpu_scientist/experiments_final/REPORT.md`](gpu_scientist/experiments_final/REPORT.md)
- **2–3 year view:** [`gpu_scientist/LONG_HORIZON.md`](gpu_scientist/LONG_HORIZON.md)
- **Rigour:** [SIGNIFICANCE.md](gpu_scientist/SIGNIFICANCE.md), [HONEST_EVAL.md](gpu_scientist/HONEST_EVAL.md), [MEMORY_ABLATION.md](gpu_scientist/walkforward/MEMORY_ABLATION.md), [REVIEWER.md](gpu_scientist/REVIEWER.md), `gpu_scientist/uncertainty.json`
- **Code guide:** [`gpu_scientist/README.md`](gpu_scientist/README.md)

**Where Exa is called:** [`gpu_scientist/exa_scout.py`](gpu_scientist/exa_scout.py) (`search`, `scout`), invoked every iteration of the main research loop in [`autoresearch.py`](gpu_scientist/autoresearch.py) (`--exa`). What it found and what the proposer used is logged in `autoresearch_log.jsonl`, kept in a dated evidence memory (`evidence.jsonl`) and listed in each run's `REPORT.md`.

Data: Pacific gpu-price-pack v0.1.1 (CC BY 4.0). Built during the event with Claude, Devin and GPT-4.1.
