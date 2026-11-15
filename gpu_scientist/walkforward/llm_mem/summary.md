# Walk-forward check (llm, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |   gain | final champion   |   iterations |
|:--------|------------:|-------------:|-------:|:-----------------|-------------:|
| S1      |      0.1449 |       0.2021 | 0.0572 | exp_004          |            7 |
| S2      |      0.0217 |       0.0877 | 0.066  | exp_001          |            7 |
| S3      |      0.0774 |       0.0787 | 0.0012 | exp_005          |            7 |

Mean TEST gain seed -> final champion: +0.0415 (3/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1449 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Coverage is much too low: overall in (0.46), above_q90 0.41 and below_q10 0.12. Ideal is 0.80. Some groups overshoot, but overall intervals are too narrow: e.g. |
| S1      |           2 | exp_002 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Calibration coverage is still low at 0.758, especially for 'fastgpu_daily|neocloud_rate_card' and 'gpurentalprices|neocloud_rate_card' (0.071-0.076 below q10, 0 |
| S1      |           3 | exp_003 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Increasing calibrate.scale from 0.01 to 0.02 caused a drastic skill_pooled drop (-0.143), even though dev coverage increased from 0.758 to 0.768. Therefore, tun |
| S1      |           4 | exp_004 | True       | exp_004    | 0.198  | 0.1487 | 0.2021 |          0.8541 | DEV group fastgpu_daily|neocloud_spot shows below_q10 = 0.163 and above_q90 = 0.228, both much higher than ideal 0.10; overall coverage is 0.758. Increasing cal |
| S1      |           5 | exp_005 | False      | exp_004    | 0.198  | 0.1487 | 0.2021 |          0.8541 | In the champion, fastgpu_daily|hyperscaler_spot group has skill 0.09 and very high overcoverage (above_q90 = 0.262, below_q10 = 0.31). This group exhibits much  |
| S1      |           6 | exp_006 | False      | exp_004    | 0.198  | 0.1487 | 0.2021 |          0.8541 | Coverage for the fastgpu_daily|hyperscaler_spot group is too high: above_q90=0.262 and below_q10=0.31 (should be ~0.10 for each). This suggests that the interva |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1449 | 0.0217 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | Overall coverage is only 0.455; skill is 0.0474. Coverage above q90 is 0.42 (vs. 0.10 target), below q10 is 0.12 (target 0.10). Coverage by group and horizon sh |
| S2      |           2 | exp_002 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | calibration coverage 0.7896 (target 0.80), calibration gamma=0.5, scale=0.01, group_by=instrument_class. Small remaining undercoverage especially at q10 for som |
| S2      |           3 | exp_003 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | The champion achieves 0.1631 pooled skill with 0.79 coverage, via empirical-drift and calibration by instrument_class. But among base model skills by group, dri |
| S2      |           4 | exp_004 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | champion coverage_in 0.7896; above_q90 0.1188; below_q10 0.0916; overall skill 0.1631; diagnosis shows overall skill and coverage are very close to targets, but |
| S2      |           5 | exp_005 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | calibration coverage_in is 0.7896 (target 0.80), and above_q90/ below_q10 are slightly off: 0.1188 and 0.0916. Drift model is the only base, with the strongest  |
| S2      |           6 | exp_006 | False      | exp_001    | 0.1632 | 0.2304 | 0.0877 |          0.7396 | Calibration coverage_in is 0.7896 (target 0.80). Some series show persistent undercoverage or overcoverage, but step size is fixed at scale=0.01 (1%). Gamma=0.5 |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | Coverage is low at 0.456 (target 0.80); truth is above q90 in 42% and below q10 in 13% (should be 10% each if calibrated). Skill: dev 0.0697, geomean 0.0606. Be |
| S3      |           2 | exp_002 | False      | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | The champion's coverage is very close to target (0.8016 vs 0.80) with nearly perfect quantile calibration (above_q90: 0.1081, below_q10: 0.0904) and most groups |
| S3      |           3 | exp_003 | False      | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | Skill worsens with horizon: 0.082 (1d), 0.104 (3d), 0.237 (7d). Horizon 7 has especially high y_above_q50 (0.597), suggesting underconfidence. -> Increasing cal |
| S3      |           4 | exp_004 | False      | exp_001    | 0.1786 | 0.0877 | 0.0574 |          0.7821 | skill_pooled=0.1786, skill_worsens_with_horizon (1d=0.082, 7d=0.237), y_above_q50 increases with horizon and days since change (e.g., y_above_q50 at 7d=0.597),  |
| S3      |           5 | exp_005 | True       | exp_005    | 0.1839 | 0.1287 | 0.0787 |          0.7848 | skill on fastgpu_daily|neocloud_spot and fastgpu_daily|hyperscaler_spot is dramatically worse vs other groups (0.239 and 0.182 vs 0.049 elsewhere); drift base s |
| S3      |           6 | exp_006 | False      | exp_005    | 0.1839 | 0.1287 | 0.0787 |          0.7848 | Skill is especially poor in fastgpu_daily|neocloud_spot (0.235) and fastgpu_daily|hyperscaler_spot (0.179), where leader (0.25/0.105) strongly outperforms drift |