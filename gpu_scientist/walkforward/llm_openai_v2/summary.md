# Walk-forward check (llm, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |   gain | final champion   |   iterations |
|:--------|------------:|-------------:|-------:|:-----------------|-------------:|
| S1      |      0.1452 |       0.2023 | 0.0571 | exp_003          |            7 |
| S2      |      0.0216 |       0.0875 | 0.066  | exp_001          |            7 |
| S3      |      0.0774 |       0.0789 | 0.0015 | exp_006          |            7 |

Mean TEST gain seed -> final champion: +0.0415 (3/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1452 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.1778 | 0.1442 | 0.2308 |          0.8469 | Overall coverage is 0.46 (should be ~0.80), with above_q90 at 0.41 and below_q10 at 0.12; all quantiles are sharply underdispersed. mean_log_err_q50 is near zer |
| S1      |           2 | exp_002 | False      | exp_001    | 0.1778 | 0.1442 | 0.2308 |          0.8469 | Calibration coverage is now 0.76 (up from 0.46), with much improved skill, but truth is above q50 only 44% of the time (should be 50%), and above q90 and below  |
| S1      |           3 | exp_003 | True       | exp_003    | 0.198  | 0.1487 | 0.2023 |          0.8541 | Coverage overall is 0.76 (vs 0.80 target). By series group, afhubbard|hyperscaler_spot is worst (coverage above q90: 8.3%, below q10: 3.6%, truth above q50: 26% |
| S1      |           4 | exp_004 | False      | exp_003    | 0.198  | 0.1487 | 0.2023 |          0.8541 | champion coverage_in is 0.7186 (below target 0.80); 'instrument_class' grouping gave higher coverage (0.758) in exp_001 than the champion's 'source_class' (0.71 |
| S1      |           5 | exp_005 | False      | exp_003    | 0.198  | 0.1487 | 0.2023 |          0.8541 | champion calibration uses group_by=source_class (skill_pooled=0.198, coverage_in=0.719), but group_by=instrument_class (exp_001) gave higher coverage (0.758) bu |
| S1      |           6 | exp_006 | False      | exp_003    | 0.198  | 0.1487 | 0.2023 |          0.8541 | champion has coverage_in 0.719 (target 0.80), above_q90 0.184 (target 0.10), below_q10 0.097 (target 0.10), all using calibrate.group_by=source_class. Historica |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1452 | 0.0216 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1632 | 0.2308 | 0.0875 |          0.7396 | Overall coverage is just 0.45 (target 0.8); above q90 much too high across groups (e.g. 0.54 in neocloud_rate_card). For group gpurentalprices|neocloud_rate_car |
| S2      |           2 | exp_002 | False      | exp_001    | 0.1632 | 0.2308 | 0.0875 |          0.7396 | By group, 'afhubbard|hyperscaler_spot' achieves low skill (0.053) yet has excellent coverage (above_q90 0.06, below_q10 0.04), even after calibration. However,  |
| S2      |           3 | exp_003 | False      | exp_001    | 0.1632 | 0.2308 | 0.0875 |          0.7396 | Calibration improved overall dev skill (0.1631 vs 0.0474 uncalibrated) and coverage (0.79 vs 0.45), but diagnosis shows above_q90 is still consistently high in  |
| S2      |           4 | exp_004 | False      | exp_001    | 0.1632 | 0.2308 | 0.0875 |          0.7396 | Coverage still slightly below target (0.7896 vs 0.80), but skill suffered when gamma was increased to 1.0 (exp_003), and sharply dropped coverage when calibrati |
| S2      |           5 | exp_005 | False      | exp_001    | 0.1632 | 0.2308 | 0.0875 |          0.7396 | Base drift skill on 'fastgpu_daily|hyperscaler_spot' is quite poor (-0.03), and worse for 'fastgpu_daily|neocloud_spot' (0.0). Calibration by instrument_class c |
| S2      |           6 | exp_006 | False      | exp_001    | 0.1632 | 0.2308 | 0.0875 |          0.7396 | In the champion, coverage_in is 0.7896 (target 0.8). Reducing scale from 0.01 to 0.005 (exp_004) increased skill a little (+0.0368) but made coverage worse (0.7 |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0698 | 0.0216 | 0.0774 |          0.629  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.1787 | 0.0875 | 0.0578 |          0.7821 | Calibration coverage is low overall: only 45.6% in, vs desired ~80%. Bias is visible: e.g. above q90 is 41.8% overall, 52.6% in fastgpu_daily|neocloud_rate_card |
| S3      |           2 | exp_002 | False      | exp_001    | 0.1787 | 0.0875 | 0.0578 |          0.7821 | Enabling calibration with gamma=0.5, scale=0.01, group_by=instrument_class took dev coverage_in from 45.6% to 80.2% and improved skill_pooled. However, skill is |
| S3      |           3 | exp_003 | False      | exp_001    | 0.1787 | 0.0875 | 0.0578 |          0.7821 | Calibration with gamma=0.5, scale=0.01, group_by=instrument_class yields coverage close to target (0.80), but shows persistent bias for fastgpu_daily|neocloud_s |
| S3      |           4 | exp_004 | False      | exp_001    | 0.1787 | 0.0875 | 0.0578 |          0.7821 | Coverage_in is close to target (0.802), but y_above_q50 is persistently high in fastgpu_daily|neocloud_rate_card (0.545) and gpurentalprices|neocloud_rate_card  |
| S3      |           5 | exp_005 | False      | exp_001    | 0.1787 | 0.0875 | 0.0578 |          0.7821 | Coverage_in is close to target (0.802), but skill is higher (worse) for 7-day horizon (0.237) and for dsc_bucket=0-1 (0.222). y_above_q50 is persistently high f |
| S3      |           6 | exp_006 | True       | exp_006    | 0.184  | 0.1288 | 0.0789 |          0.7848 | The calibration group fastgpu_daily|neocloud_spot still shows relatively poor skill (0.239), persistent undercoverage (y_above_q50=0.425, ideal 0.5), and above- |