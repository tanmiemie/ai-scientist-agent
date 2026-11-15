# FINDINGS_devin — six-iteration run, stopped after 3 (stop rule)

Ledger `experiments_devin/ledger.jsonl` · plot `experiments_devin/progress.png` · submission `submission_devin/forecast_2026-11-06.csv` (111 rows, champion exp_000). Data: gpu-price-pack v0.1.1-handover, CC BY 4.0 (see the pack's `ATTRIBUTION.md`).

## Experiments (skill_pooled vs last value; coverage = share in [q10,q90] on DEV)

| id | hypothesis (diagnosis number it rests on) | DEV | HOLDOUT | cov | decision |
|---|---|---|---|---|---|
| 000 | seed: main-ledger champion (trend_tail w60 + source_class calibration) | +0.1831 | +0.1039 | 0.80 | champion |
| 001 | momentum: last change 0-1 d ago -> 63% of truths above q50 (n=1685); shift median +0.25 step after a rise | +0.1858 | +0.1021 | 0.79 | rejected (+0.0027 dev, holdout worse) |
| 002 | volatility-aware calibration: geomean +0.115 vs pooled +0.183 -> calibrate per gpu_model | +0.1960 | +0.0283 | 0.75 | rejected (holdout -0.076) |
| 003 | Chronos-Bolt-small widths, median = last value (h=1 skill only +0.063 -> test interval only) | +0.1430 | +0.1860 | 0.81 | rejected (dev -0.040) |

Three rejections in a row -> **stopped per the stop rule**; iterations 4-6 were not run as experiments. Parameter choices were made on DEV only with `scratch/sweep_dev.py` (official scorer, DEV origins, holdout never computed): momentum beta {0, .25, .5, .75, 1} -> +.1831/.1858/.1847/.1812/.1747; calibration key source_class/gpu_model/instrument_class/source_id/pricing_tier/series_id -> +.1831/.1960/.1443/.1441/.1243/.0090; vol_tail (per-series self-rescaling, `models/m_vol_tail.py`) m=5/10/30 -> +.150/.149/.152 (discarded); Chronos median model/last -> +.034/+.143.

## Lessons
- **001** Continuation after a rise is real on DEV (68.5% end higher, n=1281; after a fall only 31% end lower), but online upper-edge calibration already captures it. Moving the median hurts the many series that rose and then stayed flat (median-of-series 0.186 -> 0.176).
- **002** Clear overfit: the DEV gain came from narrower bands (cov 0.80 -> 0.75, above_q90 0.12 -> 0.17). Collector x class is the right calibration unit because rate cards step and asks drift. A DEV win that comes with a coverage drop is a warning sign.
- **003** Regime-dependent. On DEV, Chronos wins on afhubbard hyperscaler spot (+0.162 vs +0.033) and ties on marketplace asks, but loses on step-like rate cards (+0.103 vs +0.173) and collapses in the week of 10-05 (+0.001 vs +0.102). On HOLDOUT it is +0.082 better.

## What we learned about GPU rental prices
Posted prices are step processes. The last value is close to the best median (47% of truths above q50; h=1 skill only +0.06), and almost all skill comes from the interval and grows with horizon (h=7 +0.23). Moves are asymmetric: rises cluster and continue, falls partly revert. A rise in provider count during a 7-day fall is followed by a rise 63% of the time (n=127, scratch/dev_provider_eda.py). That looks like a composition effect in the median and is a candidate for iteration 5. Interval width has to follow instrument class (step vs. drift), not GPU model.

## Recommended Sunday champion: exp_000 (unchanged)
It is the only spec that passed the gate, and its coverage is on target (0.80 DEV / 0.79 HOLDOUT). Chronos's holdout score is tempting, but choosing it would mean selecting on HOLDOUT, which the protocol forbids. Its DEV record is also unstable. The submission is byte-for-byte deterministic on re-run and numerically identical to `run_all.sh`'s replay submission.

## Suspicious / caveats
- **Replay discrepancy (baseline choice by user).** `run_all.sh` reproduces 000/001 of the main ledger exactly, but 002 gives +0.1831/+0.1039 (ledger +0.1742/+0.0975) and 003 gives +0.1689/+0.0906 (ledger +0.1731/+0.1067). Decisions are unchanged. The effect also shows up at submission level: the Mac `submission/forecast_2026-11-06.csv` (same spec) differs from Devin's in 43/111 rows by up to 0.5%, all gpurentalprices or fastgpu. Only the online-feedback path (truth -> calibration/hedge) is affected, so the likely cause is different truth values for those two collectors in the Mac build. That would come from a different pack, starter or pandas version, and is unverified. Devin's replay numbers are used as the baseline, per the user.
- **Leading signals are mostly spurious.** Of the top 10 in diagnosis.md, 8 rest on 1-3 coincident moves; the +/-0.928 B200 pairs each have a single leader move (scratch/dev_lead_eda.py). Two same-class pairs are real: afhubbard -> gpurentalprices RTX 6000 Ada rate card, lag 1, 25/25 moves coincide; afhubbard -> fastgpu L40S spot, lag 1, 11/12. These look like shared upstream providers scraped a day apart. `models/m_leader.py` uses only these two and gains just +0.0006 on DEV in scratch, so it was not run (stop rule). Those pairs were also found in the DEV window itself.
- **Chronos** HOLDOUT +0.186 vs DEV +0.143: the largest DEV/HOLDOUT disagreement in the ledger. It should be re-checked on more origins before anyone trusts or dismisses it.
- **Big DEV gaps between aggregates** (pooled +0.18 vs geomean +0.12) mean the ranking aggregate matters. Worst DEV series: fastgpu A100 80GB spot (-inf skill, flat last-value baseline) and afhubbard A100 40GB spot (-2.18).

## Next (if the stop rule is lifted)
1. Leader pairs: expect noise-level gains.
2. Provider-composition reversal.
3. A class-gated Chronos width model used only for spot/ask series.

These are pre-registered here; each needs its own DEV-justified experiment.

## Model research: newer foundation models (DEV-only scratch, no HOLDOUT used)
Question: does a 2025–26 pretrained forecaster beat the champion inside this loop? Candidates were picked from the GIFT-Eval / fev-bench leaders with permissive licenses: Chronos-2 (Amazon, Apache-2.0; `models/m_chronos2.py`, optional same-instrument-class peer group via `cross_learning`) and Timestral (Mistral, Modified MIT; `models/m_timestral.py`). TimesFM-3 was skipped because its open checkpoint is non-commercial. All runs below use `scratch/sweep_dev.py`, DEV origins only, median kept at the last value, the same source_class online calibration as exp_000, and are NOT formal experiments.

| variant | DEV pooled | cov |
|---|---|---|
| champion exp_000 (trend_tail) | +0.1831 | 0.80 |
| Chronos-2-small, own series, width 1.0 / 1.5 / 2.0 | +0.066 / −0.314 / −2.308 | 0.81 |
| Chronos-2-small, gpu_model peer group, width 1.0 / 0.75 / 0.5 / 0.4 / 0.25 | +0.115 / +0.150 / +0.182 / +0.185 / +0.189 | 0.81→0.78 |
| Chronos-2 (120M), own series, width 1.0 / 1.5 | −0.130 / −3.593 | 0.81 |
| Timestral-28M, width 1.0 | +0.037 | 0.81 |
| trend_tail + Chronos-2 group, mean / hedge η=0.5 / η=2 | +0.169 / +0.169 / +0.170 | 0.80 |
| Chronos-2 group, width 0 (= last value, no model spread) | **+0.1927** | 0.77 |
| `last_value` + source_class calibration (control) | **+0.1927** | 0.77 |

Findings
- Every pretrained model, used for interval width, loses to the champion; the skill rises monotonically as its spread is shrunk to zero. At width 0 the model contributes nothing and the result equals the control `last_value` + online calibration exactly.
- So the newest models do not help on these step-like posted prices; their wide continuous intervals are punished most on high-price series (pooled skill down to −3.6). Benchmark rank on GIFT-Eval does not transfer.
- Unexpected: the zero-width control beats the champion on DEV by +0.0096 (above the 0.005 noise line), with coverage 0.77 vs 0.80. The online calibration alone learns a better interval than trend_tail's empirical tails. This is a candidate hypothesis, not a result: it has not been run through `run_experiment.py`, and the ledger is past the 3-rejection stop rule.
