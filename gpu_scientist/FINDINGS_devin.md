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

## Recommended Sunday champion: exp_000 (superseded by exp_004, see "After the tie fix")
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
- Before the tie fix, the zero-width control looked +0.0096 better than the champion on DEV. That was mostly the tie artifact: with zero width nearly every truth sits exactly on q10/q90. After the fix (below) the control scores dev +0.1890 vs the new champion exp_004 +0.1871, i.e. +0.0019, under both MIN_DEV_GAIN (0.002) and the ~0.005 noise line. Chronos-2 grouped width 0.5 drops to +0.1644 after the fix. Verdict: no newer model improves this loop; the interval quality comes from the online calibration.

## After the tie fix (commit 9c456b2, `online.py` EDGE_TOL)
`bash run_all.sh` replayed on the VM twice; the two `replay/submission/forecast_2026-11-06.csv` are byte-identical, and exp_000–005 match the Claude-side table to 4 decimals. The Mac-vs-VM discrepancy above is resolved: it came from exact `y < q10` / `y > q90` comparisons on prices sitting on the edge, not from the data.

| exp | spec | dev pooled | holdout pooled | dev cov | decision |
|---|---|---|---|---|---|
| 000 | 00_drift | +0.0714 | +0.0437 | 0.45 | start |
| 001 | 01_trend_tail | +0.1677 | +0.0903 | 0.64 | accepted |
| 002 | 02_trend_tail_cal | +0.1833 | +0.0970 | 0.79 | accepted |
| 003 | 03_ensemble_cal | +0.1768 | +0.1040 | 0.75 | rejected |
| 004 | 04_momentum | +0.1871 | +0.1002 | 0.78 | accepted → champion |
| 005 | 05_cal_by_gpu | +0.1909 | +0.0216 | 0.74 | rejected (holdout −0.0786) |
| 006 | 06_chronos_last_median | +0.1358 | +0.1881 | 0.80 | rejected (dev −0.0513) |

- New champion: exp_004 (momentum). It was rejected before the fix; after it, it passes the gate with dev +0.0039 and holdout +0.0032. Both gains are below the ~0.005 noise line, so it is a marginal champion: practically tied with exp_002.
- Sunday recommendation: still submit exp_004 (`submission_final/forecast_2026-11-06.csv`), because it is what the pre-registered rule selects and its holdout is not worse. Expect its score to be indistinguishable from exp_002's.
- Chronos-Bolt (exp_006) keeps the largest dev/holdout divergence (+0.188 holdout); it stays rejected because selection never uses holdout.
- Official record: `experiments_final/` (ledger with a lesson per row, progress.png) and `submission_final/`. `experiments/` and `experiments_devin/` predate the fix and are kept only for history.

## LLM vs heuristic proposer (walk-forward, `DEVIN_LLM_RUN.md`)
Same `walkforward.py` check as `walkforward/heuristic_demo/`: seed = starter drift, 6 iterations per slice, decisions on DEV + GATE only, every champion scored afterwards on the following TEST week. TEST is used here only to compare the two proposers, never to pick a spec. LLM: OpenAI `gpt-4.1` (the default model name was accepted, so `GPU_LLM_MODEL` was not set). Run: `walkforward/llm_openai/`; smoke test: `experiments_llm_smoke/`.

| slice | test week | seed TEST | heuristic final TEST | heuristic gain | LLM final TEST | LLM gain |
|---|---|---|---|---|---|---|
| S1 | Oct 10-16 | +0.1452 | +0.1938 | +0.0486 | +0.2305 | **+0.0853** |
| S2 | Oct 17-23 | +0.0216 | +0.1072 | **+0.0857** | +0.0216 | 0 (no valid proposal, see below) |
| S3 | Oct 24-30 | +0.0774 | +0.0437 | −0.0336 | +0.1059 | **+0.0286** |
| mean | | | | +0.0335 (2/3) | | +0.0380 (2/3) |

What each proposer tried
- Heuristic: per-collector calibration (`source_class`, gamma 0.5 / scale 0.01), then swapping the base model (trend_tail, momentum, step_hazard, vol_tail), then a calibration-step tweak. Accepted: calibration in all slices, momentum in S1, trend_tail in S3.
- LLM: global calibration (`group_by=all`, gamma 0.05, scale 0.05) first in S1 and S3, then calibration tweaks (gamma 0.10 / 0.075, `group_by=series_id`), then ensembles: drift + last_value (mean, accepted in S1), drift + leader (mean, accepted in S3), hedge instead of mean (rejected in both), adding leader as a third model (rejected). It never swapped the base model to the step-aware models the heuristic favoured.
- The LLM's S3 champion (drift + leader, mean, global calibration) improved on TEST where the heuristic's (trend_tail + source_class calibration) got worse than the seed. The S1/S3 advantage is three slices of one run of a non-deterministic proposer; treat it as suggestive, not significant.

Representative LLM hypotheses (observation quoted from the log)
1. S1 exp_001, accepted: "dev coverage_in is very low at 0.46256 (should target 0.80); overestimation of q10 and q90 is evident (q90: 0.414251, q10: 0.123188)" → enable calibration. DEV +0.046 → +0.205, TEST +0.145 → +0.185.
2. S1 exp_004, accepted: "Increasing calibrate.gamma to 0.10 caused overfitting and a sharp skill decline … All failures thus far have involved calibration, not the base predictive model" → add last_value to drift in a mean ensemble. DEV +0.205 → +0.249, GATE +0.116 → +0.183, TEST → +0.2305 (best TEST of either proposer).
3. S3 exp_003, accepted: "groups fastgpu_daily|neocloud_rate_card and gpurentalprices|neocloud_rate_card show much worse tail calibration (above_q90 0.123/0.149 …) … candidate leaders table: e.g. fastgpu_daily.neocloud_rate_card.RTX_A6000 correl ~ -0.92 …" → drift + leader mean ensemble. DEV +0.170 → +0.176, GATE +0.110 → +0.138.
4. S1 exp_005, rejected: "the leader model's signals … are highly correlated with targets, particularly for neocloud_rate_card series (e.g., corr 0.87 for RTX_6000_Ada at lag 1)" → add leader as a third model. DEV −0.033, coverage 0.74.
5. S3 exp_005, rejected: "Leader … outperforms drift notably in fastgpu_daily|neocloud_spot (leader: 0.25, drift: 0.008) … Mean ensemble (fixed 0.5/0.5) may underweight leader" → hedge η=2. DEV −0.038.

Refused and wasted proposals
- Validation refused 8 proposals, all for the same reason: `calibrate.scale must be in (0, 0.05]` (S1 ×4, S3 ×1, S2 ×3). The system prompt lists the calibrate keys but not their ranges or defaults, and the LLM kept proposing larger scales; it also described "default gamma = 0.05, scale = 0.05" when the code defaults are 0.5 / 0.01. In S2 all three attempts of iteration 1 were refused, so the loop stopped at the seed and S2 has no LLM iterations (TEST gain 0). These 3 calls are not in `autoresearch_log.jsonl` because the loop logs only iterations that ran.
- No exact repeats were proposed (the repeat check never fired).
- 3 accepted-by-validation specs were no-ops (identical DEV and GATE to 4 decimals): S1 exp_002 `calibrate.group_by=series_id` (the catalog meta has no `series_id` key, so `online.group_key` maps every series to `"None"`, i.e. one global group) and S3 exp_004 / exp_006 `combine.group_by` = source_class / source_id with `method=mean` (mean weights do not depend on the group). Suggested follow-ups, not done here (core files): put the parameter ranges/defaults in the prompt, make `series_id` a real group key, and reject `combine.group_by` changes under `mean`.

API calls: 32 in the walk-forward (S1 16, S2 3, S3 13; each iteration = 1 proposal + 1 lesson, plus 1 per refused proposal) and 2 in the smoke test, 34 in total. The smoke test (1 iteration from the exp_004 champion) proposed `calibrate.group_by` source_class → gpu_model, citing "afhubbard|hyperscaler_spot (n=372), skill is only 0.008"; it was rejected (DEV +0.0015, holdout −0.0711), the same overfit as exp_005. `submission_final/` is unchanged.

## LLM proposer v2 (after PR #4: ranges in the prompt, no-op refusal)
Same check as above, rerun with `python walkforward.py --proposer llm --provider openai --iters 6 --run llm_openai_v2` (OpenAI `gpt-4.1`). Selection used DEV + GATE only; TEST was scored afterwards. Run: `walkforward/llm_openai_v2/`.

| slice | seed TEST | heuristic gain | LLM v1 gain | LLM v2 final TEST | LLM v2 gain | v2 champion |
|---|---|---|---|---|---|---|
| S1 | +0.1452 | +0.0486 | +0.0853 | +0.2023 | +0.0571 | exp_003: drift + calibration by `source_class` |
| S2 | +0.0216 | +0.0857 | 0 | +0.0875 | +0.0660 | exp_001: drift + default calibration |
| S3 | +0.0774 | −0.0336 | +0.0286 | +0.0789 | +0.0015 | exp_006: drift + leader (mean) + calibration |
| mean | | +0.0335 (2/3) | +0.0380 (2/3) | | **+0.0415 (3/3)** | |

- **PR #4 fixed the failure that cost S2 its whole run in v1.** All 18 iterations ran and no proposal failed the range check. The only refusals were 2 repeats in S1 (iteration 4): the LLM re-proposed the exp_001 spec and the new no-op check caught it.
- The search was narrower than in v1. 14 of the 18 experiments are calibration tweaks: `gamma`, `scale`, or `group_by` among instrument_class / source_class / gpu_model / series_id / all. Only 3 try a second model (momentum ×2, leader ×1), and the base model was never swapped. S3 exp_006, drift + leader, was accepted in both v1 and v2.
- **New no-op class.** S3 exp_003 (`gamma=0.25`) and exp_004 (`scale=0.005`) gave identical DEV and GATE. The calibration step in `online.py` uses only the product `gamma*scale`, so the two specs are the same model. The no-op check compares normalized settings, not this product, so it missed them. Suggested follow-up in `autoresearch.normalize`: canonicalize to `gamma*scale`, or expose just one step-size parameter.
- S2 exp_005 put the momentum parameters at the top level of the model entry instead of under `params`. The validator accepted it, and it ran with momentum defaults (the values happened to be the defaults).
- The 3/3 improvement and +0.0415 mean come from one run of a non-deterministic proposer over 3 overlapping-in-time slices. v1 → v2 is +0.0035 in mean gain, which is noise-level. The real change is that no slice was lost to invalid proposals.
- API calls: 38. That is 18 proposals + 18 lessons + 2 refused repeats (S1 14, S2 12, S3 12). The key came only from the environment. `submission_final/` and `experiments_final/` are unchanged.

## Wider walk-forward (6 TEST weeks, heuristic proposer, 12 iterations; `DEVIN_OVERNIGHT.md` task 2)
`walkforward_wide.py` (a copy of `walkforward.py`; the original is unchanged). DEV always starts 2026-09-15, GATE is the 7 days before TEST, TEST is 7 days. Selection used DEV + GATE only, and TEST was scored after selection. Run: `walkforward/heuristic_wide/`.

| slice | TEST week | seed TEST | final TEST | gain |
|---|---|---|---|---|
| W1 | 09-29..10-05 | +0.0120 | +0.1330 | +0.1209 |
| W2 | 10-03..10-09 | +0.0715 | +0.0765 | +0.0050 |
| W3 | 10-10..10-16 | +0.1452 | +0.2186 | +0.0734 |
| W4 | 10-14..10-20 | +0.0336 | +0.1076 | +0.0740 |
| W5 | 10-17..10-23 | +0.0216 | +0.0819 | +0.0604 |
| W6 | 10-24..10-30 | +0.0774 | +0.0632 | −0.0141 |

Mean gain +0.0533. 5 of 6 slices improved. Exact one-sided sign test p = 7/64 = 0.109.
- **TEST weeks overlap** (W1/W2 share 3 days; W3/W4/W5 share 3–4 days each), so the six slices are not independent. The sign-test p-value assumes they are, so it is optimistic. Even so, it does not reach 0.05.
- Almost all of the gain comes from the first one or two acceptances: online calibration, and in W1 trend_tail. The later acceptances (iterations 7–9 in W2, W4, W5, W6) passed DEV and GATE but lowered TEST in W2, W4 and W5. This is the same small-gain overfitting seen in the earlier ledger. A larger `MIN_DEV_GAIN`, or a rule requiring the gain on more than one DEV sub-window, would likely help, but choosing either from these TEST numbers would be TEST selection, so it is not done here.
- W1 has only 7 DEV days (09-15..09-21), so its large gain rests on a thin DEV window.

## Overnight summary
- PR #5 (task 3): pytest suite for no-lookahead, determinism, edge ties and submission validity, plus `run_tests.sh`. Result: 13 passed, 1 strict xfail, which records a `data.Panel` trailing forward-fill look-ahead (fix belongs in `data.py`).
- PR #6 (run requested before task 2): LLM proposer v2 walk-forward after PR #4. Mean TEST gain +0.0415, 3/3 slices improved, no invalid proposals, 38 API calls. New no-op class: only `gamma*scale` matters.
- PR #7 (task 6): `demo.sh`, the 2-iteration live demo. Clean clone runs in 23 s with the heuristic proposer and 31 s with `--llm`; it checks the Python prerequisites first.
- This PR (task 2): `walkforward_wide.py` over 6 TEST weeks. Mean gain +0.0533, 5/6 slices improved, sign test p = 0.109 (overlapping weeks).
