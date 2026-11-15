# Walk-forward check (llm, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |    gain | final champion   |   iterations |
|:--------|------------:|-------------:|--------:|:-----------------|-------------:|
| S1      |      0.1449 |       0.185  |  0.0401 | exp_001          |            7 |
| S2      |      0.0217 |       0.2252 |  0.2036 | exp_005          |            7 |
| S3      |      0.0774 |       0.0658 | -0.0116 | exp_004          |            7 |

Mean TEST gain seed -> final champion: +0.0773 (2/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1449 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.1177 | 0.1781 | 0.185  |          0.6438 | Skill is 0.0459 with very poor coverage (0.46 in); highest skill (0.186, 0.196) is on afhubbard|hyperscaler_spot and gpurentalprices|marketplace_ask. There is u |
| S1      |           2 | exp_002 | False      | exp_001    | 0.1177 | 0.1781 | 0.185  |          0.6438 | Coverage in the current champion is only 0.61 (target 0.80), with 0.29 of outcomes above q90 (should be 0.10 if calibrated), and weak skill especially for fastg |
| S1      |           3 | exp_003 | False      | exp_001    | 0.1177 | 0.1781 | 0.185  |          0.6438 | The main finding is that the current champion (empirical_quantiles, window=30) has skill_pooled=0.1177 (dev), but poor coverage: only 0.61 in, with 0.29 above q |
| S1      |           4 | exp_004 | False      | exp_001    | 0.1177 | 0.1781 | 0.185  |          0.6438 | The champion's dev skill_pooled is 0.118, but coverage_in is 0.61 (well under the 0.80 target). The q90 tail especially is much too high: coverage_above_q90 is  |
| S1      |           5 | exp_005 | False      | exp_001    | 0.1177 | 0.1781 | 0.185  |          0.6438 | By days since last price change, the champion's skill drops sharply (from 0.139 at 0-1d to 0.036 at 8-30d, and 0 for >30d), and coverage above q90 also drops (f |
| S1      |           6 | exp_006 | False      | exp_001    | 0.1177 | 0.1781 | 0.185  |          0.6438 | Coverage in interval is 0.61 (vs target 0.80), with skill_pooled 0.118; group fastgpu_daily|hyperscaler_spot skill -0.208, above_q90 0.274, below_q10 0.274; ski |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1449 | 0.0217 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1009 | 0.1913 | 0.0488 |          0.6853 | Coverage is severely low (0.45), with the q90 and q10 bounds hit too often (q90: 42%, q10: 12%), especially for the most volatile horizons and for series with f |
| S2      |           2 | exp_002 | True       | exp_002    | 0.1135 | 0.2035 | 0.2096 |          0.7439 | By horizon, coverage is poor and interval coverage in the champion is ~0.54 (want 0.8), with q90 hit much too often, especially at 7 days (0.46 above q90, with  |
| S2      |           3 | exp_003 | False      | exp_002    | 0.1135 | 0.2035 | 0.2096 |          0.7439 | Coverage is too low across nearly all groups (overall 0.60 vs target 0.80; q90 hit too often, especially at 7d: 0.46 vs 0.10 ideal). Recent gain came from using |
| S2      |           4 | exp_004 | False      | exp_002    | 0.1135 | 0.2035 | 0.2096 |          0.7439 | The DEV coverage is low across nearly all groups and horizons (overall 0.60, far below target 0.80; e.g. at 7d, above_q90 is 0.455). All current models operate  |
| S2      |           5 | exp_005 | True       | exp_005    | 0.1851 | 0.2346 | 0.2252 |          0.7654 | DEV coverage is 0.60 (target 0.80); skill is adequate (0.1135). Coverage is especially low at longer horizons (7d above_q90: 0.455) and for highly volatile/spot |
| S2      |           6 | exp_006 | False      | exp_005    | 0.1851 | 0.2346 | 0.2252 |          0.7654 | Coverage for the champion (vol_weighted_drift_floor, vol_window=30) is 0.783 overall, but above_q90 is too high at 7 days (0.284), especially for neocloud_spot  |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | False      | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Coverage is 0.456 (well below 0.8). Undercoverage is most acute at long horizons and following recent price changes (above_q90=0.494 at h=7, above_q90=0.557 for |
| S3      |           2 | exp_002 | False      | exp_000    | 0.0697 | 0.0217 | 0.0774 |          0.6303 | Coverage is very low (0.46 overall); major undercoverage in q10/q90; skill by group is mediocre; clear evidence (table: 'Candidate leading signals') that some s |
| S3      |           3 | exp_003 | True       | exp_003    | 0.1506 | 0.0389 | 0.0685 |          0.7172 | Skill is mediocre (0.0697 pooled); coverage is extremely poor (0.456 in, 0.418 above q90, 0.126 below q10). Drift gives only one interval (whole-history empiric |
| S3      |           4 | exp_004 | True       | exp_004    | 0.1548 | 0.062  | 0.0658 |          0.7076 | Coverage is 0.61 (well below target 0.80), with undercoverage at horizon=7 (above_q90=0.382, below_q10=0.129). Increasing the window in the log_empirical_window |
| S3      |           5 | exp_005 | False      | exp_004    | 0.1548 | 0.062  | 0.0658 |          0.7076 | Overall skill_pooled: 0.1548; coverage_in: 0.6037 (well below 0.8 target); above_q90: 0.2802, below_q10: 0.1161. Coverage is notably too low, especially for hor |
| S3      |           6 | exp_006 | False      | exp_004    | 0.1548 | 0.062  | 0.0658 |          0.7076 | Coverage on DEV for the champion is 0.6037 (far below 0.8), and interval width increases (exp_005, scaled intervals) slightly improved coverage (to 0.64) but at |