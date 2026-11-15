# Walk-forward check (llm, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |   gain | final champion   |   iterations |
|:--------|------------:|-------------:|-------:|:-----------------|-------------:|
| S1      |      0.1449 |       0.2165 | 0.0716 | exp_004          |            7 |
| S2      |      0.0217 |       0.0877 | 0.066  | exp_001          |            7 |
| S3      |      0.0774 |       0.0787 | 0.0012 | exp_002          |            7 |

Mean TEST gain seed -> final champion: +0.0463 (3/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1449 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Overall coverage on dev is 0.4626 (well below target 0.80), with truth above q90 in 0.414 and below q10 in 0.123 (both too high); this strongly indicates underc |
| S1      |           2 | exp_002 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | DEV coverage_in is 0.758 (target 0.80); coverage_above_q90 is 0.151 (should be 0.10), and coverage_below_q10 is 0.08998 (slightly low), so intervals are slightl |
| S1      |           3 | exp_003 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | By series group: fastgpu_daily|hyperscaler_spot and fastgpu_daily|neocloud_spot have high above_q90 (0.214; 0.228) and below_q10 (0.179; 0.163), and have among  |
| S1      |           4 | exp_004 | True       | exp_004    | 0.2264 | 0.157  | 0.2165 |          0.8484 | DEV overall coverage is 0.758 (vs target 0.80). Above q90 is 0.151 (should be 0.10), below q10 is 0.08998 (nearly right), and coverage is particularly too high  |
| S1      |           5 | exp_005 | False      | exp_004    | 0.2264 | 0.157  | 0.2165 |          0.8484 | Coverage in champion is 0.733 (target 0.80); above_q90 (0.18 overall) is high, especially in fastgpu_daily|hyperscaler_spot (0.262) and fastgpu_daily|neocloud_s |
| S1      |           6 | exp_006 | False      | exp_004    | 0.2264 | 0.157  | 0.2165 |          0.8484 | Calibration coverage is systematically too high in fastgpu_daily|hyperscaler_spot (above_q90 0.262, below_q10 0.202) and fastgpu_daily|neocloud_spot (above_q90  |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1449 | 0.0217 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | Overall skill 0.0474; coverage_in 0.454958; coverage_above_q90 0.420515; coverage_below_q10 0.124527. The interval coverage is far too low (should target 0.80), |
| S2      |           2 | exp_002 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | Coverage is now at 0.7896 (up from 0.45) using calibrate (gamma=0.5, scale=0.01, group_by=instrument_class) on drift, with skill_pooled up to 0.1631 from 0.0474 |
| S2      |           3 | exp_003 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | Calibration is by instrument_class (champion), but gpu_model grouping (exp_002) overfit: skill_pooled rose 0.021 to 0.1841 but coverage_in fell by 0.087 to 0.70 |
| S2      |           4 | exp_004 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | Coverage by horizon is low at 1d (0.32), 3d (0.475), and 7d (0.601); overall coverage_in improved from 0.45 to 0.79 with instrument_class calibration. Previous  |
| S2      |           5 | exp_005 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | champion calibrate.group_by=instrument_class obtains coverage_in 0.790 (dev). Exp_002 (gpu_model) and exp_003 (source_class) overfit: both raised skill but drop |
| S2      |           6 | exp_006 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | By horizon: skill at 1d is 0.057, at 3d is 0.051, at 7d is 0.241; interval coverage: 1d-0.32, 3d-0.475, 7d-0.601 (all under target 0.80). Calibration params are |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | Coverage is too low (overall 0.456; q90=0.418, q10=0.126), far from the target 0.80. All series use drift only, and over-confident tails are evident across near |
| S3      |           2 | exp_002 | True       | exp_002    | 0.1839 | 0.1287 | 0.0787 |          0.7848 | Skill and coverage are much lower in fastgpu_daily|hyperscaler_spot (skill 0.182; coverage below_q10 0.228, above_q90 0.111), versus afhubbard|hyperscaler_spot  |
| S3      |           3 | exp_003 | False      | exp_002    | 0.1839 | 0.1287 | 0.0787 |          0.7848 | By group, drift underperforms leader in all but gpurentalprices|marketplace_ask (drift=0.179, leader=0.194) and afhubbard|hyperscaler_spot (drift=0.174, leader= |
| S3      |           4 | exp_004 | False      | exp_002    | 0.1839 | 0.1287 | 0.0787 |          0.7848 | Coverage is slightly high on q10 (below_q10 0.0909; target 0.10) and slightly low on q90 (above_q90 0.1051; target 0.10), but pooled in-interval is well calibra |
| S3      |           5 | exp_005 | False      | exp_002    | 0.1839 | 0.1287 | 0.0787 |          0.7848 | dev skill for fastgpu_daily|neocloud_spot (0.235) and fastgpu_daily|neocloud_rate_card (0.196) is much worse than afhubbard|hyperscaler_spot (0.024); in both, d |
| S3      |           6 | exp_006 | False      | exp_002    | 0.1839 | 0.1287 | 0.0787 |          0.7848 | The mean ensemble gives equal weights to drift and leader in all groups, yet the leader model strongly outperforms drift in fastgpu_daily|neocloud_spot (leader= |