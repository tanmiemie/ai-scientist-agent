# Walk-forward check (llm, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |    gain | final champion   |   iterations |
|:--------|------------:|-------------:|--------:|:-----------------|-------------:|
| S1      |      0.1449 |       0.2304 |  0.0855 | exp_001          |            7 |
| S2      |      0.0217 |       0.0877 |  0.066  | exp_001          |            6 |
| S3      |      0.0774 |       0.0574 | -0.0201 | exp_001          |            6 |

Mean TEST gain seed -> final champion: +0.0438 (2/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1449 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | coverage_in is only 0.46256 (target 0.80), above_q90=0.414251 and below_q10=0.123188 both too high; champion has no calibration. Over-quantile hits most in fast |
| S1      |           2 | exp_002 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Overall skill 0.1778, coverage_in 0.758454 (target 0.80), skill for afhubbard|hyperscaler_spot is only 0.066 but base drift model achieves 0.186 for this group. |
| S1      |           3 | exp_003 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | coverage_in is only 0.758, below the 0.80 target, with above_q90 at 0.151 and below_q10 at 0.090. Calibration uses gamma=0.5 and scale=0.01 grouped by instrumen |
| S1      |           4 | exp_004 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Coverage is low across the board (overall 0.758, above_q90 0.1516, below_q10 0.09), especially in fastgpu_daily groups (high above_q90 and below_q10). Calibrati |
| S1      |           5 | exp_005 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | The champion shows notably poor skill (-inf to -0.45) and near-zero coverage in multiple 'neocloud_rate_card' and 'neocloud_spot' series, e.g., fastgpu_daily.ne |
| S1      |           6 | exp_006 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Coverage is low (0.758454 < target 0.8) and the most problematic series and series groups have very poor skill—the worst have zero or negative skill and no cove |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1449 | 0.0217 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | coverage_in is 0.454958 (well below target 0.80), above_q90 0.420515 and below_q10 0.124527 (both too high—should be ~0.10); intervals are too narrow everywhere |
| S2      |           2 | exp_002 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | By group, 'fastgpu_daily|neocloud_rate_card' (n=759) has skill 0.169, but 'drift' alone provides only 0.023 here. Skill is much higher in the champion with cali |
| S2      |           3 | exp_003 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | Worst series have negative skill (e.g., fastgpu_daily.neocloud_spot.A100_80GB.spot.median with -inf skill, fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_dem |
| S2      |           4 | exp_004 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | drift has poor or even negative skill in fastgpu_daily|hyperscaler_spot (−0.03), fastgpu_daily|neocloud_rate_card (0.023), fastgpu_daily|neocloud_spot (−0), but |
| S2      |           5 | exp_005 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | The champion uses calibration group_by=instrument_class, with overall skill 0.1631, coverage_in 0.7896; worst skill is in gpurentalprices|neocloud_rate_card (-0 |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | Overall coverage_in is 0.456 (target 0.80), q90 coverage is 0.418, q10 is 0.126. All show undercoverage. -> Enabling post-hoc interval calibration should increa |
| S3      |           2 | exp_002 | False      | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | By horizon: skill for 7d is 0.237 (much worse than 1d: 0.082, 3d: 0.104). By series: 'afhubbard|hyperscaler_spot' is much better (0.049) than others; its covera |
| S3      |           3 | exp_003 | False      | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | coverage_in = 0.8016 (good), but skill for some groups is poor, especially fastgpu_daily|hyperscaler_spot (0.182), fastgpu_daily|neocloud_rate_card (0.19), and  |
| S3      |           4 | exp_004 | False      | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | coverage for fastgpu_daily|neocloud_rate_card is 0.095 above q90, 0.112 below q10 (target 0.10 each); mean_log_err_q50 is 0.004; skill is 0.19 (worst among all  |
| S3      |           5 | exp_005 | False      | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | Calibration coverage is 0.8016 (target 0.80), but 0.0904 below q10 and 0.108 above q90: slightly more misses high than low. Some groups (e.g., fastgpu_daily|neo |