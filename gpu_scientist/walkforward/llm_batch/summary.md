# Walk-forward check (llm, batch ideas, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |    gain | final champion   |   iterations |
|:--------|------------:|-------------:|--------:|:-----------------|-------------:|
| S1      |      0.1449 |       0.2304 |  0.0855 | exp_001          |            7 |
| S2      |      0.0217 |       0.0739 |  0.0522 | exp_003          |            7 |
| S3      |      0.0774 |       0.0649 | -0.0125 | exp_003          |            7 |

Mean TEST gain seed -> final champion: +0.0417 (2/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1449 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Coverage_in is 0.463 (well below 0.80), and afhubbard|hyperscaler_spot has y_above_q50 0.26 and coverage_above_q90 = 0.151. Coverage far too low, with uneven mi |
| S1      |           2 | exp_002 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Diagnosis: after price change, y_above_q50=0.596 (truth above median far too often). -> Combining drift and momentum with mean will upweight forecasts after cha |
| S1      |           3 | exp_003 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Series with large-magnitude or anti-correlated leader signals (e.g., corr=-0.952 lag 2 for H100) may benefit from including the leader. -> Using a leader model  |
| S1      |           4 | exp_004 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Skill collapses and y_above_q50 goes to extreme (0.056) for provider-loss cases (prov_bucket='fewer', n=18). -> Provider-count shifts are poorly captured by dri |
| S1      |           5 | exp_005 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Coverage_in at 0.758 overall, but serious series-by-series miscoverage (see worst series table) suggests that calibrate.group_by=series_id has not been tried an |
| S1      |           6 | exp_006 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | Worst series see infinite or huge negative skill and y_above_q50 near zero (e.g., neocloud_spot/B200, various A100/L40S); but exp_005 with series_id-wide calibr |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1449 | 0.0217 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1342 | 0.2013 | 0.061  |          0.6509 | For 1343 dev cells with 0-1 days since last price change: skill is 0.06 (much higher loss), y_above_q50 is 0.611 (strong under-prediction), and above_q90 is 0.5 |
| S2      |           2 | exp_002 | True       | exp_002    | 0.1642 | 0.2096 | 0.0734 |          0.7353 | In afhubbard|hyperscaler_spot, drift skill = 0.169, momentum = 0.050, and static 0.5/0.5 weights under-serve drift, contributing to large negative skill in key  |
| S2      |           3 | exp_003 | True       | exp_003    | 0.1745 | 0.2156 | 0.0739 |          0.7454 | At 7-day horizon: y_above_q50 is 0.577 (truth above median too often), above_q90 is 0.364 (should be ~0.10 if calibrated); group coverage (in) is only 0.63 (tar |
| S2      |           4 | exp_004 | False      | exp_003    | 0.1745 | 0.2156 | 0.0739 |          0.7454 | The group 'gpurentalprices|neocloud_rate_card' has both severe over-coverage (above_q90 = 0.301) and y_above_q50 = 0.538, indicating intervals are too low and t |
| S2      |           5 | exp_005 | False      | exp_003    | 0.1745 | 0.2156 | 0.0739 |          0.7454 | Calibration coverage_in is 0.648 (well below 0.80 target); gpurentalprices|neocloud_rate_card above_q90 is 0.301, intervals are too narrow/too low. Previous cal |
| S2      |           6 | exp_006 | False      | exp_003    | 0.1745 | 0.2156 | 0.0739 |          0.7454 | Previous highest calibrate.scale tested was 0.0075 (exp_005). More aggressive expansion, up to 0.05, has not been tested and is permitted. Coverage remains far  |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.1503 | 0.0369 | 0.0463 |          0.731  | Coverage well below 0.80 for all groups, worst for afhubbard|hyperscaler_spot (0.229) and fastgpu_daily|hyperscaler_spot (0.211). -> Turning on per-series calib |
| S3      |           2 | exp_002 | True       | exp_002    | 0.1781 | 0.0655 | 0.0649 |          0.7145 | y_above_q50 is 0.628 and above_q90 is 0.296 for dsc_bucket=0-1 (0/1 days since last price change), indicating frequent underprediction just after a price change |
| S3      |           3 | exp_003 | True       | exp_003    | 0.1807 | 0.0731 | 0.0649 |          0.7269 | afhubbard|hyperscaler_spot has worst skill (-1.096) and momentum underperforms drift (0.041 vs 0.174), so single shared weights likely penalize this group. -> G |
| S3      |           4 | exp_004 | False      | exp_003    | 0.1807 | 0.0731 | 0.0649 |          0.7269 | afhubbard|hyperscaler_spot and fastgpu_daily|hyperscaler_spot show very different model wins—momentum deeply underperforms for afhubbard but is overweighted by  |
| S3      |           5 | exp_005 | False      | exp_003    | 0.1807 | 0.0731 | 0.0649 |          0.7269 | In fastgpu_daily|hyperscaler_spot, y_above_q50 is only 0.228 and below_q10 is 0.289—far too many low quantile misses, especially just after price changes (dsc_b |
| S3      |           6 | exp_006 | False      | exp_003    | 0.1807 | 0.0731 | 0.0649 |          0.7269 | In fastgpu_daily|hyperscaler_spot, y_above_q50=0.228 and below_q10=0.289: systematic underprediction, worst 0-1 days after price change (y_above_q50=0.596, belo |