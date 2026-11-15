# Walk-forward check (llm, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |    gain | final champion   |   iterations |
|:--------|------------:|-------------:|--------:|:-----------------|-------------:|
| S1      |      0.1449 |       0.2115 |  0.0666 | exp_004          |            6 |
| S2      |      0.0217 |       0.0877 |  0.066  | exp_001          |            7 |
| S3      |      0.0774 |       0.0211 | -0.0563 | exp_002          |            6 |

Mean TEST gain seed -> final champion: +0.0254 (2/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1449 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | coverage_in is low at 0.46256 (target 0.80), with above_q90 at 0.414251 and below_q10 at 0.123188, indicating severe undercoverage (too-narrow intervals); mean  |
| S1      |           2 | exp_002 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Coverage is low: overall 0.76 in vs 0.80 target; above q90 is 15.2% and below q10 is 9.0%. Coverage is low in almost every group (esp. gpurentalprices|marketpla |
| S1      |           3 | exp_003 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Calibration coverage is low at 0.758 (target 0.80); intervals are too narrow across series. Increasing the calibration scale slightly may help widen intervals a |
| S1      |           4 | exp_004 | True       | exp_004    | 0.236  | 0.1532 | 0.2115 |          0.8526 | Champion coverage_in = 0.758 (target 0.80). Coverage_above_q90 at 0.1516 and below_q10 at 0.09 indicate mild miscalibration, slightly underconfident in the uppe |
| S1      |           5 | exp_005 | False      | exp_004    | 0.236  | 0.1532 | 0.2115 |          0.8526 | DEV skill is especially poor for gpurentalprices|neocloud_rate_card (0.056 drift skill, 0.303 overall skill), and overall coverage is low at 0.72. Calibration i |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1449 | 0.0217 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | The overall coverage under champion is very low: coverage_in=0.45 (should be near 0.8), with above_q90 at 0.42 and below_q10 at 0.12. This means the predicted i |
| S2      |           2 | exp_002 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | The champion is strongest on afhubbard|hyperscaler_spot (skill 0.053) but weakest (negative or near zero skill) on fastgpu_daily|hyperscaler_spot and fastgpu_da |
| S2      |           3 | exp_003 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | By 'series group': skill in 'afhubbard|hyperscaler_spot' is 0.053 (best), but 'fastgpu_daily|neocloud_spot' is 0.211 (worst) and 'gpurentalprices|neocloud_rate_ |
| S2      |           4 | exp_004 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | champion skill_pooled 0.16315; drift base model skill by group includes near-zero or negative (e.g., fastgpu_daily|neocloud_spot: -0, fastgpu_daily|hyperscaler_ |
| S2      |           5 | exp_005 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | The group fastgpu_daily|neocloud_spot has particularly bad skill (0.211), elevated coverage above q90 (0.161), and a candidate leading signal pair to gpurentalp |
| S2      |           6 | exp_006 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | coverage_in is low at 0.7896 (target is 0.80); skill_geomean is 0.0662; calibration uses group_by instrument_class -> Calibration may better correct for systema |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | Overall coverage_in is 0.456 (much too low; target is 0.80), with extreme quantile coverage also far off (q90: 0.418, q10: 0.126). -> Adding calibration with a  |
| S3      |           2 | exp_002 | True       | exp_002    | 0.1824 | 0.1073 | 0.0211 |          0.7738 | Coverage in afhubbard|hyperscaler_spot is 0.06 above q90 and 0.049 below q10 (too narrow), while coverage in fastgpu_daily|neocloud_rate_card is 0.095 above q90 |
| S3      |           3 | exp_003 | False      | exp_002    | 0.1824 | 0.1073 | 0.0211 |          0.7738 | In the champion, calibration is grouped by source_class. For groups like afhubbard|hyperscaler_spot (n=384, skill=0.117, above_q90=0.06, below_q10=0.06), both c |
| S3      |           4 | exp_004 | False      | exp_002    | 0.1824 | 0.1073 | 0.0211 |          0.7738 | Coverage for fastgpu_daily|hyperscaler_spot is poor: above_q90=0.133, below_q10=0.294 (should be ≈0.10 each). Mean_log_err_q50 is slightly negative (-0.018), su |
| S3      |           5 | exp_005 | False      | exp_002    | 0.1824 | 0.1073 | 0.0211 |          0.7738 | Coverage for fastgpu_daily|hyperscaler_spot is too wide (above_q90=13.3%, below_q10=29.4%), skill is weak (0.147), and mean_log_err shows mild down-bias (-0.018 |