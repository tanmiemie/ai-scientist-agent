# Research report: experiments_review

_Written automatically from `ledger.jsonl` by `report.py`. Every number is the ledger's; nothing here is judged by a language model._

## Summary

- 8 experiments: the starting point (exp_000), then 4 kept and 3 rejected.
- Skill vs last value (pooled), DEV: +0.071 at the start (exp_000) → +0.191 for the champion (exp_007).
- HOLDOUT (never used to choose parameters, only as a gate): +0.044 → +0.101.
- Champion interval coverage: DEV 0.79, HOLDOUT 0.76 (target 0.80).
- Rule: keep a change only if DEV improves by at least 0.002 and HOLDOUT does not fall below the champion's.

![progress](progress.png)

## All experiments

| id | kept | DEV | HOLDOUT | coverage DEV | hypothesis |
|---|---|---|---|---|---|
| exp_000 | yes | +0.071 | +0.044 | 0.45 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-... |
| exp_001 | yes | +0.168 | +0.090 | 0.64 | exp_000 diagnosis: truth above q90 in 41% of dev cells, so the upper edge is far too narrow while prices cr... |
| exp_002 | yes | +0.183 | +0.097 | 0.79 | exp_001 still has 25% of truths above q90, unevenly by group. Learn an upper/lower offset per collector x c... |
| exp_003 | no | +0.177 | +0.104 | 0.75 | Different groups behave differently (rare steps vs frequent small moves). Run trend_tail, a jump/hazard mod... |
| exp_004 | yes | +0.187 | +0.100 | 0.78 | Iter 1 (momentum). exp_000 diagnosis: cells with last change 0-1 days ago have truth above q50 in 63% (n=16... |
| exp_005 | no | +0.191 | +0.022 | 0.74 | Iter 2 (volatility-aware calibration). exp_000 diagnosis: calibration groups by collector x class, so quiet... |
| exp_006 | no | +0.136 | +0.188 | 0.80 | Iter 3 (Chronos-Bolt, time-boxed). exp_000 diagnosis: 47% of truths above q50 and +0.063 skill at h=1 show ... |
| exp_007 | yes | +0.191 | +0.101 | 0.79 | EDA.md: 45% of 10%+ moves fall on a day the provider count changed, and such moves are 7x larger. Momentum ... |

## The path, one experiment at a time

### exp_000: kept

**Hypothesis.** Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.

**What changed.** starting point. Model: drift (single; no calibration).

**Decision.** first experiment: becomes the starting champion

**Lesson written to memory.** Drift baseline: median near the last value is fine, but intervals are far too narrow (dev coverage 0.45, 42% of truths above q90). Unchanged by the tie fix.

### exp_001: kept

**Hypothesis.** exp_000 diagnosis: truth above q90 in 41% of dev cells, so the upper edge is far too narrow while prices creep up. Use only the last 60 days of changes and keep at least one typical daily move of room above the last value.

**What changed.** adds model `trend_tail`; drops model `drift`. Model: trend_tail (single; no calibration).

**Test.** Against champion exp_000: DEV +0.0964, HOLDOUT +0.0466. By horizon (DEV, 1/3/7 days): +0.099 / +0.168 / +0.182.

**Decision.** dev skill_pooled +0.0964 vs champion exp_000 (need >= +0.002); holdout +0.0466 (need >= -0.0)

**Lesson written to memory.** Empirical trend tails over a 60-day window: largest single gain (+0.096 dev). Still 25% of truths above q90, so the interval, not the median, is the bottleneck. Unchanged by the tie fix.

**Reviewer flags** (kept if ≥3 of 5 reviews; they do not change the decision):
- `interval_widened_not_centred` (5/5, severity 2): Mean log interval width increased from 0.02497 to 0.04567 (dev), and coverage_in rose from 0.454853 to 0.643735, suggesting much of the skill gain is from wider intervals.

### exp_002: kept

**Hypothesis.** exp_001 still has 25% of truths above q90, unevenly by group. Learn an upper/lower offset per collector x class online from realised misses (adaptive calibration, target 10% each side).

**What changed.** `calibrate.enabled`: False → True; `calibrate.gamma`: None → 0.5; `calibrate.group_by`: None → source_class; `calibrate.scale`: None → 0.01. Model: trend_tail (single; calibration by source_class).

**Test.** Against champion exp_001: DEV +0.0155, HOLDOUT +0.0068. By horizon (DEV, 1/3/7 days): +0.063 / +0.134 / +0.235.

**Decision.** dev skill_pooled +0.0155 vs champion exp_001 (need >= +0.002); holdout +0.0068 (need >= -0.0)

**Lesson written to memory.** Online source_class calibration brings dev coverage to 0.79 (+0.0155 dev). After the tie fix dev +0.1833 / holdout +0.0970; before it the same spec gave +0.1742 (Mac) and +0.1831 (VM) because exact y<q10 comparisons on prices sitting on the edge were decided by exp/log rounding.

**Reviewer flags** (kept if ≥3 of 5 reviews; they do not change the decision):
- `gain_from_few_series` (5/5, severity 2): The largest 3 series account for 40.3% of the absolute skill change (1.238512, -1.162656, 0.732801), and only 19/37 series improved.
- `interval_widened_not_centred` (5/5, severity 2): Mean log interval width q90/q10 increased from 0.04567 to 0.08949 (dev) and 0.06735 to 0.1112 (holdout), while coverage_in rose from 0.643735 to 0.792998 (dev), suggesting improvement is largely from wider intervals.
- `other` (5/5, severity 2): DEV/HOLDOUT divergence: skill_pooled drops from 0.183275 (dev) to 0.097039 (holdout), and skill_geomean from 0.118615 to 0.054054, indicating possible overfitting or instability.

### exp_003: rejected

**Hypothesis.** Different groups behave differently (rare steps vs frequent small moves). Run trend_tail, a jump/hazard model and a 30-day drift side by side and let each group's weights follow recent pinball loss.

**What changed.** adds model `step_hazard`; adds model `drift`; `combine.eta`: None → 0.5; `combine.group_by`: None → source_class; `combine.method`: single → hedge. Model: trend_tail, step_hazard, drift (hedge; calibration by source_class).

**Test.** Against champion exp_002: DEV -0.0065, HOLDOUT +0.0070. By horizon (DEV, 1/3/7 days): +0.088 / +0.117 / +0.227.

**Decision.** dev skill_pooled -0.0065 vs champion exp_002 (need >= +0.002); holdout +0.0070 (need >= -0.0)

**Lesson written to memory.** Hedging trend_tail with step_hazard and drift loses on dev (-0.0065); extra models add spread the calibration already handles. Holdout +0.0070 is not a reason to accept. Unchanged decision after the tie fix.

**Reviewer flags** (kept if ≥3 of 5 reviews; they do not change the decision):
- `gain_from_few_series` (3/5, severity 2): The largest 3 series account for 37.4% of the absolute change in loss, and all three have large negative changes (e.g., -0.319116, -0.237423, -0.186472), suggesting the overall DEV result is heavily influenced by a few series.
- `interval_widened_not_centred` (3/5, severity 2): Mean log interval width increased on dev (0.09247 vs 0.08949) and holdout (0.11543 vs 0.1112), while coverage_in decreased (dev: 0.752457 vs 0.792998; holdout: 0.734261 vs 0.776673), suggesting intervals widened but did not improve calibration or centering.
- `other` (5/5, severity 2): DEV skill_pooled dropped from 0.183275 (champion) to 0.176792 (this), and skill_median_of_series from 0.185248 to 0.163772; holdout skill_pooled is only slightly higher (0.104 vs 0.097039), indicating the new method does not generalize or improve overall performance.

### exp_004: kept

**Hypothesis.** Iter 1 (momentum). exp_000 diagnosis: cells with last change 0-1 days ago have truth above q50 in 63% (n=1685); DEV EDA: after a recent RISE 68.5% end above the last value (n=1281), after a recent fall only 31% end below. Shift median and upper edge up by beta typical daily moves after a rise in the last day. beta=0.25 chosen by a DEV-only sweep over {0,0.25,0.5,0.75,1} (dev pooled +0.1831/+0.1858/+0.1847/+0.1812/+0.1747).

**What changed.** adds model `momentum`; drops model `trend_tail`; drops model `step_hazard`; drops model `drift`; `combine.eta`: 0.5 → None; `combine.group_by`: source_class → None; `combine.method`: hedge → single. Model: momentum (single; calibration by source_class).

**Test.** Against champion exp_002: DEV +0.0039, HOLDOUT +0.0032. By horizon (DEV, 1/3/7 days): +0.035 / +0.145 / +0.242.

**Decision.** dev skill_pooled +0.0039 vs champion exp_002 (need >= +0.002); holdout +0.0032 (need >= -0.0)

**Lesson written to memory.** Momentum (median/upper edge up after a recent rise, beta=0.25). Before the tie fix it was rejected on the VM (dev +0.0027, holdout -0.0018); after the fix it passes (dev +0.0039, holdout +0.0032) and becomes champion. Both gains are below the ~0.005 noise line, so it is a marginal champion.

**Reviewer flags** (kept if ≥3 of 5 reviews; they do not change the decision):
- `other` (5/5, severity 2): DEV skill_pooled (0.1871) is much higher than HOLDOUT (0.1002); DEV/HOLDOUT divergence suggests possible overfitting or non-stationarity.

### exp_005: rejected

**Hypothesis.** Iter 2 (volatility-aware calibration). exp_000 diagnosis: calibration groups by collector x class, so quiet and volatile GPUs share one additive offset; geomean skill +0.115 vs pooled +0.183, and by-group skill ranges +0.033 (afhubbard spot) to +0.200. Volatility tracks the GPU (B200/H100 vs older cards) more than the collector, so learn the offsets per gpu_model. Chosen by a DEV-only scratch comparison of calibration keys (source_class +0.1831, gpu_model +0.1960, instrument_class +0.1443, source_id +0.1441, pricing_tier +0.1243, series_id/all +0.0090) and of a per-series self-rescaling model vol_tail (m=5/10/30: +0.150/+0.149/+0.152, discarded). Offsets only widen/narrow intervals; no price curve is chained across classes.

**What changed.** adds model `trend_tail`; drops model `momentum`; `calibrate.group_by`: source_class → gpu_model. Model: trend_tail (single; calibration by gpu_model).

**Test.** Against champion exp_004: DEV +0.0038, HOLDOUT -0.0786. By horizon (DEV, 1/3/7 days): +0.093 / +0.181 / +0.217.

**Decision.** dev skill_pooled +0.0038 vs champion exp_004 (need >= +0.002); holdout -0.0786 (need >= -0.0)

**Lesson written to memory.** Calibration offsets per gpu_model: dev +0.0038 but holdout -0.0786. The offsets learned the October rise and fail when prices fall back; overfitting, same conclusion before and after the tie fix.

**Reviewer flags** (kept if ≥3 of 5 reviews; they do not change the decision):
- `gain_from_few_series` (5/5, severity 2): The largest 3 series account for 27.4% of the absolute change in loss, with one series improving by 0.587 and two others worsening by -0.494 and -0.411, indicating outsized influence from a few series.
- `repeats_rejected_idea` (5/5, severity 2): The experiment adds 'trend_tail', which was previously rejected in exp_003 for similar reasons (group-specific modeling with trend_tail and calibration).
- `other` (5/5, severity 3): There is a large DEV/HOLDOUT divergence: skill_pooled is 0.191 on DEV but only 0.022 on HOLDOUT, and holdout skill is much worse than the champion (0.022 vs 0.100), suggesting overfitting or poor generalization.

### exp_006: rejected

**Hypothesis.** Iter 3 (Chronos-Bolt, time-boxed). exp_000 diagnosis: 47% of truths above q50 and +0.063 skill at h=1 show the median is near-optimal at the last value, so the open question is the interval: does a pretrained foundation model give better q10/q90 widths than trend_tail? Chronos-Bolt-small zero-shot on 90 days of log prices, median kept at the last value, same source_class calibration. Variant chosen by a DEV-only scratch run: median_mode=model +0.0337, median_mode=last +0.1430 (champion +0.1831), so only the stronger variant is submitted; expected to be rejected.

**What changed.** adds model `chronos`; drops model `trend_tail`; `calibrate.group_by`: gpu_model → source_class. Model: chronos (single; calibration by source_class).

**Test.** Against champion exp_004: DEV -0.0513, HOLDOUT +0.0879. By horizon (DEV, 1/3/7 days): +0.048 / +0.071 / +0.188.

**Decision.** dev skill_pooled -0.0513 vs champion exp_004 (need >= +0.002); holdout +0.0879 (need >= -0.0)

**Lesson written to memory.** Chronos-Bolt-small for the interval, median at last value: dev -0.0513, holdout +0.0879, the largest dev/holdout divergence in the ledger. Better on spot/ask series, worse on step-like rate cards (regime-dependent). Not selectable on holdout.

**Reviewer flags** (kept if ≥3 of 5 reviews; they do not change the decision):
- `interval_widened_not_centred` (5/5, severity 2): Mean log interval width increased on DEV (0.09982 vs 0.09208 for champion), but coverage is only slightly up (0.799 vs 0.782), and skill dropped (0.1358 vs 0.1871), suggesting wider intervals did not improve centering or sharpness.
- `other` (5/5, severity 2): DEV/HOLDOUT divergence: DEV skill_pooled dropped -0.0513 vs champion, but HOLDOUT improved +0.0879, suggesting possible overfitting or instability; also, some series have -inf or strongly negative skill (e.g., fastgpu_daily.neocloud_spot.A100_80GB.spot.median: -inf, afhubbard.hyperscaler_spot.A100_40GB.spot.median: -1.339), indicating the method fails badly for some cases.

### exp_007: kept

**Hypothesis.** EDA.md: 45% of 10%+ moves fall on a day the provider count changed, and such moves are 7x larger. Momentum should react only to repricing, not to a change in who is listed: apply the momentum shift only when the provider count did not change on the day of the last rise. DEV-only sweep (scratch): this alone gives +0.1908 vs +0.1871 for spec 04; adding partial reversion after composition moves (rho 0.2-0.6) lowered DEV in all 18 settings, so rho = 0.

**What changed.** adds model `composition`; drops model `momentum`. Model: composition (single; calibration by source_class).

**Test.** Against champion exp_004: DEV +0.0036, HOLDOUT +0.0008. By horizon (DEV, 1/3/7 days): +0.039 / +0.152 / +0.243.

**Decision.** dev skill_pooled +0.0036 vs champion exp_004 (need >= +0.002); holdout +0.0008 (need >= -0.0)

**Lesson written to memory.** Momentum should follow repricing, not changes in who is listed: skipping the shift when the provider count changed on the day of the last rise gives DEV +0.0036 and HOLDOUT +0.0008 over exp_004, and was better in 6 of 6 weeks (Sep 15-Oct 26, overlapping the selection windows). Partial reversion after composition moves lowered DEV in all 18 settings tried: rejected before the gate. Gain is within noise; adopted because the pre-registered rule chose it. Sunday file changes only in q10 of 19 rows (at most 0.5%).

**Reviewer flags** (kept if ≥3 of 5 reviews; they do not change the decision):
- `gain_from_few_series` (5/5, severity 2): The largest 3 series account for 58.5% of the total absolute loss reduction (0.0968, 0.0606, 0.0586 out of 0.3455), suggesting the DEV gain is concentrated in a few series.
- `other` (5/5, severity 2): DEV/holdout skill_pooled diverges: DEV +0.0036, but holdout only +0.0008; skill_median_of_series drops from 0.1793 (champion) to 0.1658 (holdout), and geomean is nearly unchanged (0.0606 vs 0.0603), suggesting DEV gain may not generalize.

## What the loop ruled out

- **exp_003**: Hedging trend_tail with step_hazard and drift loses on dev (-0.0065); extra models add spread the calibration already handles. Holdout +0.0070 is not a reason to accept. Unchanged decision after the tie fix.
- **exp_005**: Calibration offsets per gpu_model: dev +0.0038 but holdout -0.0786. The offsets learned the October rise and fail when prices fall back; overfitting, same conclusion before and after the tie fix.
- **exp_006**: Chronos-Bolt-small for the interval, median at last value: dev -0.0513, holdout +0.0879, the largest dev/holdout divergence in the ledger. Better on spot/ask series, worse on step-like rate cards (regime-dependent). Not selectable on holdout.

## Champion by horizon

| horizon | DEV skill | HOLDOUT skill |
|---|---|---|
| 1 day | +0.039 | +0.066 |
| 3 day | +0.152 | +0.096 |
| 7 day | +0.243 | +0.111 |

Champion spec: `experiments_review/exp_007/spec.json`. Diagnosis: `experiments_review/exp_007/diagnosis.md`.
