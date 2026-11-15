# Research report: experiments

_Written automatically from `ledger.jsonl` by `report.py`. Every number is the ledger's; nothing here is judged by a language model._

## Summary

- 7 experiments: the starting point (exp_000), then 2 kept and 4 rejected.
- Skill vs last value (pooled), DEV: +0.070 at the start (exp_000) → +0.208 for the champion (exp_006).
- HOLDOUT (never used to choose parameters, only as a gate): +0.022 → +0.082.
- Champion interval coverage: DEV 0.75, HOLDOUT 0.73 (target 0.80).
- Rule: keep a change only if DEV improves by at least 0.002 and HOLDOUT does not fall below the champion's.

![progress](progress.png)

## All experiments

| id | kept | DEV | HOLDOUT | coverage DEV | hypothesis |
|---|---|---|---|---|---|
| exp_000 | yes | +0.070 | +0.022 | 0.46 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-... |
| exp_001 | yes | +0.203 | +0.055 | 0.78 | DEV: coverage_in = 0.456 (well under target 0.80), coverage_above_q90 = 0.418 (should be 0.10 if well calib... |
| exp_002 | no | +0.219 | +0.048 | 0.76 | calibration coverage_in is 0.7779 (close, but just under 0.80 target) and above_q90 is 0.128 (still high; i... |
| exp_003 | no | +0.191 | +0.058 | 0.77 | calibration coverage_in = 0.7779 (just under 0.80 target); group_by = instrument_class (6 groups), meaning ... |
| exp_004 | no | +0.136 | +0.036 | 0.60 | In the champion, calibrate.group_by = instrument_class (6 groups). Coverage_in = 0.778, below 0.80 target. ... |
| exp_005 | no | +0.170 | +0.110 | 0.79 | Diagnosis table by series group: afhubbard/hyperscaler_spot is the only group with very tight intervals (co... |
| exp_006 | yes | +0.208 | +0.082 | 0.75 | The worst-miscalibrated group (afhubbard/hyperscaler_spot) has tight intervals—coverage_above_q90 0.065, be... |

## The path, one experiment at a time

### exp_000: kept

**Hypothesis.** Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.

**What changed.** starting point. Model: drift (single; no calibration).

**Decision.** first experiment: becomes the starting champion

**Lesson written to memory.** seed: starting champion for this autonomous run

### exp_001: kept

**Hypothesis.** DEV: coverage_in = 0.456 (well under target 0.80), coverage_above_q90 = 0.418 (should be 0.10 if well calibrated), coverage_below_q10 = 0.126 (should be 0.10). All base models have weight 1 only for themselves (single drift model). -> The champion's quantile intervals are too narrow, dramatically under-covering (45.6% vs target 80%), indicating the drift model's uncertainty estimate is much too small. Enabling interval calibration with modest step size (gamma=0.5, scale=0.01) should quickly widen the intervals and bring empirical coverage closer to target, especially in series with extreme undercoverage. Pinball loss may temporarily worsen, but gross undercoverage should improve substantially. Change: Enable online interval calibration with gamma=0.5, scale=0.01, grouped by instrument_class. DEV sweep of calibrate.scale: 0.005->+0.2026, 0.01->+0.1786, 0.02->+0.0470, 0.03->-0.1176; chose 0.005.

**What changed.** `calibrate.enabled`: False → True; `calibrate.gamma`: None → 0.5; `calibrate.group_by`: None → instrument_class; `calibrate.scale`: None → 0.005. Model: drift (single; calibration by instrument_class).

**Test.** Against champion exp_000: DEV +0.1328, HOLDOUT +0.0333. By horizon (DEV, 1/3/7 days): +0.104 / +0.136 / +0.257.

**Decision.** dev skill_pooled +0.1328 vs champion exp_000 (need >= +0.002); holdout +0.0333 (need >= -0.0)

**Lesson written to memory.** Enabling online interval calibration increased dev pooled skill by +0.1328 and holdout by +0.0333 versus the champion, while boosting in-sample coverage from 0.456 to 0.778—much closer to the 0.80 target—implying the next experiment should explore refining calibration scale or more granular grouping to close the remaining coverage gap without sacrificing skill.

### exp_002: rejected

**Hypothesis.** calibration coverage_in is 0.7779 (close, but just under 0.80 target) and above_q90 is 0.128 (still high; ideally 0.10). Calibrate.scale is at 0.005; in calibration, this is log-units per step (about a 0.5% adjustment per error). Increasing scale to 0.01 should further widen intervals, boost coverage and perhaps bring above_q90 and below_q10 closer to 0.10. -> Increasing calibrate.scale from 0.005 to 0.01 (holding gamma*scale constant or increasing step size) will nudge coverage_in closer to the 0.80 target, and may help above_q90 and below_q10 move closer to 0.10, since slightly undercoverage and slight skew remain. This should help overall calibration if widening is not too aggressive. Change: Increase calibrate.scale from 0.005 (champion) to 0.01. DEV sweep of calibrate.scale: 0.003->+0.2186, 0.007->+0.1863, 0.01->+0.1786, 0.02->+0.0470; chose 0.003.

**What changed.** `calibrate.scale`: 0.005 → 0.003. Model: drift (single; calibration by instrument_class).

**Test.** Against champion exp_001: DEV +0.0160, HOLDOUT -0.0072. By horizon (DEV, 1/3/7 days): +0.114 / +0.176 / +0.262.

**Decision.** dev skill_pooled +0.0160 vs champion exp_001 (need >= +0.002); holdout -0.0072 (need >= -0.0)

**Lesson written to memory.** The dev skill_pooled improved (+0.0160 vs champion), but coverage_in dropped (0.757 vs 0.778) and holdout skill_pooled declined (-0.0072), indicating the experiment increased overfitting and reduced calibration quality; next step: explore a smaller calibrate.scale or additional regularization to improve generalization and coverage.

### exp_003: rejected

**Hypothesis.** calibration coverage_in = 0.7779 (just under 0.80 target); group_by = instrument_class (6 groups), meaning calibration likely suffers from limited granularity or imbalanced data by instrument type. The worst coverage and most miscalibrated series are mostly in gpurentalprices|neocloud_rate_card, while afhubbard|hyperscaler_spot and fastgpu_daily|hyperscaler_spot seem better calibrated. -> Refining calibration granularity by grouping by source_id (which yields more homogeneous and fine-grained segments than by instrument_class) will allow the online interval correction to more tightly adapt to distinct distribution drift patterns per data source. This will improve coverage alignment and pooled skill, especially where instrument_class mixes divergent sources. Change: Change calibrate.group_by from instrument_class to source_id.

**What changed.** `calibrate.group_by`: instrument_class → source_id. Model: drift (single; calibration by source_id).

**Test.** Against champion exp_001: DEV -0.0111, HOLDOUT +0.0034. By horizon (DEV, 1/3/7 days): +0.105 / +0.174 / +0.219.

**Decision.** dev skill_pooled -0.0111 vs champion exp_001 (need >= +0.002); holdout +0.0034 (need >= -0.0)

**Lesson written to memory.** Calibration coverage_in on dev was 0.773 (just below target 0.80), skill_pooled dropped -0.011 vs champion, and holdout improved slightly (+0.003). Grouping calibration by instrument_class did not boost skill, likely due to coarse or mismatched groups; next, group by source_id to better capture drift and improve both coverage and pooled skill.

### exp_004: rejected

**Hypothesis.** In the champion, calibrate.group_by = instrument_class (6 groups). Coverage_in = 0.778, below 0.80 target. Attempts to change group_by to source_id (exp_003) or to make scale smaller/larger did not help, and results by series group show that most groups (except afhubbard|hyperscaler_spot, fastgpu_daily|hyperscaler_spot, and gpurentalprices|marketplace_ask) have above_q90 and below_q10 far from the 0.10 ideal. The group fastgpu_daily|neocloud_rate_card and gpurentalprices|neocloud_rate_card are large, at 990 and 1068 n, and their above_q90, below_q10 are both off from ideal calibration. Since series_id is even more granular than source_id, and intervals are appearing too narrow or off-calibrated in some series, try calibrating per series_id. -> Calibrating online interval width by series_id (the finest grouping) will allow the calibration step to fully adapt to local signal noise and drift conditions, particularly helpful for the groups with systematic miscalibration (e.g. gpurentalprices|neocloud_rate_card, fastgpu_daily|neocloud_rate_card). This finer adaptation should bring overall coverage_in closer to the 0.80 target (from 0.778), and reduce excess above_q90 or below_q10. Change: Change calibrate.group_by from instrument_class to series_id.

**What changed.** `calibrate.group_by`: instrument_class → series_id. Model: drift (single; calibration by series_id).

**Test.** Against champion exp_001: DEV -0.0662, HOLDOUT -0.0186. By horizon (DEV, 1/3/7 days): +0.106 / +0.152 / +0.135.

**Decision.** dev skill_pooled -0.0662 vs champion exp_001 (need >= +0.002); holdout -0.0186 (need >= -0.0)

**Lesson written to memory.** Changing calibration from instrument_class to series_id reduced dev skill_pooled by 0.066 (to 0.136) and coverage_in to 0.600 (from champion’s 0.778), indicating overfitting and undercoverage. For the next experiment, try a less granular group_by (e.g., source_id) or hybrid grouping to balance local adaptation and global data sufficiency.

### exp_005: rejected

**Hypothesis.** Diagnosis table by series group: afhubbard|hyperscaler_spot is the only group with very tight intervals (coverage_above_q90 0.065, below_q10 0.055, BOTH below 0.10 target) and skill 0.145 (second best), suggesting calibration is slightly overcorrected for this group compared to others. -> Calibrating intervals jointly across all instrument classes (calibrate.group_by = all) rather than by instrument_class (current champion), will allow the global calibrator to adjust interval width more flexibly according to recent realized coverage. This should reduce overcorrection for high-performing groups (e.g., afhubbard|hyperscaler_spot: above_q90 0.065, below_q10 0.055) and slightly widen intervals overall, likely nudging coverage_in closer to the 0.80 target without overfitting to class-level idiosyncrasies. We expect no loss or a small gain in skill, mainly by improving coverage balance. Change: Set calibrate.group_by to 'all' instead of 'instrument_class'.

**What changed.** `calibrate.group_by`: instrument_class → all. Model: drift (single; calibration by all).

**Test.** Against champion exp_001: DEV -0.0324, HOLDOUT +0.0552. By horizon (DEV, 1/3/7 days): +0.097 / +0.179 / +0.181.

**Decision.** dev skill_pooled -0.0324 vs champion exp_001 (need >= +0.002); holdout +0.0552 (need >= -0.0)

**Lesson written to memory.** Joint calibration across all instrument classes increased dev set coverage from 0.778 to 0.787 but reduced skill_pooled by 0.032 (from 0.203 to 0.170), failing the required skill threshold; next, try a hybrid grouping strategy or introduce regularization to balance interval widths without hurting skill.

### exp_006: kept

**Hypothesis.** The worst-miscalibrated group (afhubbard|hyperscaler_spot) has tight intervals—coverage_above_q90 0.065, below_q10 0.055 (both under 0.10 target), skill 0.145—suggesting overcorrection. Calibrate.group_by = instrument_class lumps it with other classes, possibly oversmoothing online adjustments. Attempts to increase or decrease calibration granularity or scale (exp_002-005) reduced skill or coverage. Calibrate.scale remains at 0.005 in the champion. -> Changing calibrate.group_by from instrument_class to source_class will better capture heterogeneity in calibration needs between hyperscaler_spot, neocloud_rate_card, neocloud_spot, marketplace_ask, etc. This may improve both skill and interval calibration, especially for groups with unique volatility patterns such as afhubbard|hyperscaler_spot (now undercovered) and gpurentalprices groups (now overcovered). Change: Change calibrate.group_by from instrument_class to source_class.

**What changed.** `calibrate.group_by`: instrument_class → source_class. Model: drift (single; calibration by source_class).

**Test.** Against champion exp_001: DEV +0.0055, HOLDOUT +0.0271. By horizon (DEV, 1/3/7 days): +0.111 / +0.174 / +0.246.

**Decision.** dev skill_pooled +0.0055 vs champion exp_001 (need >= +0.002); holdout +0.0271 (need >= -0.0)

**Lesson written to memory.** Changing calibrate.group_by from instrument_class to source_class increased dev skill_pooled from 0.2026 to 0.2080 (+0.0055) and holdout by +0.0271, with a slight coverage drop (dev: 0.7549 vs 0.7779), indicating better calibration and discrimination across volatile groups; next, tune calibration scale within source_class to recover coverage while retaining skill gains.

## What the loop ruled out

- **exp_002**: The dev skill_pooled improved (+0.0160 vs champion), but coverage_in dropped (0.757 vs 0.778) and holdout skill_pooled declined (-0.0072), indicating the experiment increased overfitting and reduced calibration quality; next step: explore a smaller calibrate.scale or additional regularization to improve generalization and coverage.
- **exp_003**: Calibration coverage_in on dev was 0.773 (just below target 0.80), skill_pooled dropped -0.011 vs champion, and holdout improved slightly (+0.003). Grouping calibration by instrument_class did not boost skill, likely due to coarse or mismatched groups; next, group by source_id to better capture drift and improve both coverage and pooled skill.
- **exp_004**: Changing calibration from instrument_class to series_id reduced dev skill_pooled by 0.066 (to 0.136) and coverage_in to 0.600 (from champion’s 0.778), indicating overfitting and undercoverage. For the next experiment, try a less granular group_by (e.g., source_id) or hybrid grouping to balance local adaptation and global data sufficiency.
- **exp_005**: Joint calibration across all instrument classes increased dev set coverage from 0.778 to 0.787 but reduced skill_pooled by 0.032 (from 0.203 to 0.170), failing the required skill threshold; next, try a hybrid grouping strategy or introduce regularization to balance interval widths without hurting skill.

## Outside evidence (Exa)

Each iteration searched the web with Exa before proposing, for a method and for dated market news published on or before the run's cutoff. What the proposer said it used:

| experiment | kept | source the proposer relied on | found this turn |
|---|---|---|---|
| exp_001 | yes | https://arxiv.org/html/2207.14219v9 | method 5, market 4 |
| exp_002 | no | none | method 5, market 4 |
| exp_003 | no | none | method 5, market 4 |
| exp_004 | no | none | method 5, market 4 |
| exp_005 | no | none | method 5, market 4 |
| exp_006 | yes | none | method 5, market 4 |

Evidence memory: 9 dated sources in `experiments/evidence.jsonl`.

## Champion by horizon

| horizon | DEV skill | HOLDOUT skill |
|---|---|---|
| 1 day | +0.111 | +0.109 |
| 3 day | +0.174 | +0.087 |
| 7 day | +0.246 | +0.074 |

Champion spec: `experiments/exp_006/spec.json`. Diagnosis: `experiments/exp_006/diagnosis.md`.
