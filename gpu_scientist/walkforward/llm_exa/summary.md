# Walk-forward check (llm, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |    gain | final champion   |   iterations |
|:--------|------------:|-------------:|--------:|:-----------------|-------------:|
| S1      |      0.1449 |       0.2237 |  0.0788 | exp_005          |            7 |
| S2      |      0.0217 |       0.0347 |  0.013  | exp_004          |            7 |
| S3      |      0.0774 |       0.0357 | -0.0417 | exp_006          |            7 |

Mean TEST gain seed -> final champion: +0.0167 (2/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1449 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | The DEV coverage is very poor: overall coverage_in 0.463 (well below the 0.8 target), with coverage_above_q90 0.414 and coverage_below_q10 0.123—most notably, o |
| S1      |           2 | exp_002 | False      | exp_001    | 0.1778 | 0.1442 | 0.2304 |          0.8469 | DEV diagnosis: coverage_in 0.758 (target 0.8), with all series using only drift as a model and calibration grouped by instrument_class (champion). 'fastgpu_dail |
| S1      |           3 | exp_003 | True       | exp_003    | 0.236  | 0.1532 | 0.2115 |          0.8526 | Champion has coverage_in 0.758 (target 0.8) and good pooled skill (0.1778), but some groups show notable undercoverage, especially fastgpu_daily|hyperscaler_spo |
| S1      |           4 | exp_004 | False      | exp_003    | 0.236  | 0.1532 | 0.2115 |          0.8526 | Fastgpu_daily|hyperscaler_spot and fastgpu_daily|neocloud_spot have above_q90 at 0.262 and 0.262 and below_q10 at 0.202 and 0.163, respectively, showing consist |
| S1      |           5 | exp_005 | True       | exp_005    | 0.243  | 0.1835 | 0.2237 |          0.8383 | The champion achieves dev skill_pooled 0.236 and coverage_in 0.723, but notable undercoverage remains in fastgpu_daily|hyperscaler_spot (above_q90: 0.262, below |
| S1      |           6 | exp_006 | False      | exp_005    | 0.243  | 0.1835 | 0.2237 |          0.8383 | The champion's coverage_in is 0.697 (target 0.8), with consistent undercoverage in fastgpu_daily|hyperscaler_spot (above_q90 0.274, below_q10 0.226) and fastgpu |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1449 | 0.0217 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1314 | 0.186  | 0.0457 |          0.6838 | Coverage in is very low at 0.455 (target is 0.80). Skill is higher for longer horizons, and severe undercoverage is seen for fastgpu_daily|neocloud_rate_card (a |
| S2      |           2 | exp_002 | False      | exp_001    | 0.1314 | 0.186  | 0.0457 |          0.6838 | coverage_in = 0.562 (target = 0.80), above_q90 = 0.33, below_q10 = 0.11 (too narrow intervals). vol_tail is allowed m=10.0 (default 10.0, champion 15) and lo_cl |
| S2      |           3 | exp_003 | False      | exp_001    | 0.1314 | 0.186  | 0.0457 |          0.6838 | coverage_in = 0.562 (target = 0.80), coverage above_q90 = 0.33, below_q10 = 0.11: intervals are too narrow across almost all groups. vol_tail.hi_clip is at the  |
| S2      |           4 | exp_004 | True       | exp_004    | 0.1517 | 0.1955 | 0.0347 |          0.7382 | Enabling calibration with gamma=0.25, scale=0.01, group_by=instrument_class raised dev coverage_in to 0.772 (+0.21 vs champion) and dev skill_pooled to 0.207 (+ |
| S2      |           5 | exp_005 | False      | exp_004    | 0.1517 | 0.1955 | 0.0347 |          0.7382 | Dev coverage_in is 0.6499 (target 0.80), with 0.25 above q90 and 0.10 below q10 (intervals too narrow, skewed above). Series-level calibration was an improvemen |
| S2      |           6 | exp_006 | False      | exp_004    | 0.1517 | 0.1955 | 0.0347 |          0.7382 | champion calibrate.gamma=0.25, scale=0.01, group_by=series_id; coverage_in 0.650, above_q90 0.252, below_q10 0.098, skill_pooled 0.1517. Tuning gamma*scale upwa |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.2026 | 0.0549 | 0.0747 |          0.7766 | DEV: coverage_in = 0.456 (well under target 0.80), coverage_above_q90 = 0.418 (should be 0.10 if well calibrated), coverage_below_q10 = 0.126 (should be 0.10).  |
| S3      |           2 | exp_002 | False      | exp_001    | 0.2026 | 0.0549 | 0.0747 |          0.7766 | calibration coverage_in is 0.7779 (close, but just under 0.80 target) and above_q90 is 0.128 (still high; ideally 0.10). Calibrate.scale is at 0.005; in calibra |
| S3      |           3 | exp_003 | False      | exp_001    | 0.2026 | 0.0549 | 0.0747 |          0.7766 | calibration coverage_in = 0.7779 (just under 0.80 target); group_by = instrument_class (6 groups), meaning calibration likely suffers from limited granularity o |
| S3      |           4 | exp_004 | False      | exp_001    | 0.2026 | 0.0549 | 0.0747 |          0.7766 | In the champion, calibrate.group_by = instrument_class (6 groups). Coverage_in = 0.778, below 0.80 target. Attempts to change group_by to source_id (exp_003) or |
| S3      |           5 | exp_005 | False      | exp_001    | 0.2026 | 0.0549 | 0.0747 |          0.7766 | Diagnosis table by series group: afhubbard|hyperscaler_spot is the only group with very tight intervals (coverage_above_q90 0.065, below_q10 0.055, BOTH below 0 |
| S3      |           6 | exp_006 | True       | exp_006    | 0.208  | 0.0821 | 0.0357 |          0.7503 | The worst-miscalibrated group (afhubbard|hyperscaler_spot) has tight intervals—coverage_above_q90 0.065, below_q10 0.055 (both under 0.10 target), skill 0.145—s |