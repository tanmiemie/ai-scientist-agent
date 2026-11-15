# Walk-forward check (llm, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |   gain | final champion   |   iterations |
|:--------|------------:|-------------:|-------:|:-----------------|-------------:|
| S1      |      0.1452 |       0.2305 | 0.0853 | exp_004          |            7 |
| S2      |      0.0216 |       0.0216 | 0      | exp_000          |            1 |
| S3      |      0.0774 |       0.1059 | 0.0286 | exp_003          |            7 |

Mean TEST gain seed -> final champion: +0.0380 (2/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1452 |          0.4607 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.2048 | 0.1155 | 0.185  |          0.8441 | dev coverage_in is very low at 0.46256 (should target 0.80); overestimation of q10 and q90 is evident (q90: 0.414251, q10: 0.123188). -> Enabling a simple conti |
| S1      |           2 | exp_002 | False      | exp_001    | 0.2048 | 0.1155 | 0.185  |          0.8441 | dev coverage_in is 0.7506 vs target 0.80; skill_median_of_series is much lower (0.073) than pooled (0.205), series like fastgpu_daily.neocloud_spot and afhubbar |
| S1      |           3 | exp_003 | False      | exp_001    | 0.2048 | 0.1155 | 0.185  |          0.8441 | Champion coverage_in is 0.7506 vs target 0.80; worst groups (e.g., afhubbard|hyperscaler_spot skill 0.01) and some coverage buckets remain undercovered; previou |
| S1      |           4 | exp_004 | True       | exp_004    | 0.249  | 0.1833 | 0.2305 |          0.8212 | dev coverage_in is 0.7506 vs target 0.80; some series (e.g., neocloud_rate_card, neocloud_spot) have exceptionally low or negative skill, but group-based recali |
| S1      |           5 | exp_005 | False      | exp_004    | 0.249  | 0.1833 | 0.2305 |          0.8212 | The diagnosis shows that the leader model's signals (from other collectors, lagged 1-3 days) are highly correlated with targets, particularly for neocloud_rate_ |
| S1      |           6 | exp_006 | False      | exp_004    | 0.249  | 0.1833 | 0.2305 |          0.8212 | By horizon, skill increases from 0.059 (1d) → 0.306 (7d); q10 and q90 coverage are too high at 3d (below_q10=0.136, above_q90=0.156), especially for 7d. Calibra |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1452 | 0.0216 |          0.535  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0698 | 0.0216 | 0.0774 |          0.629  | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.1703 | 0.11   | 0.0999 |          0.7834 | Overall coverage_in is 0.456 (target 0.8), with above_q90 at 0.418 and below_q10 at 0.126, indicating underconfident intervals with too-narrow quantiles. Covera |
| S3      |           2 | exp_002 | False      | exp_001    | 0.1703 | 0.11   | 0.0999 |          0.7834 | calibration gamma=0.05 yields coverage_in=0.78689 (target=0.8), but q90 and q10 coverages are 0.1098 and 0.1033. The main skill gain in exp_001 came from enabli |
| S3      |           3 | exp_003 | True       | exp_003    | 0.1761 | 0.1384 | 0.1059 |          0.7945 | champion overall skill 0.1703; groups fastgpu_daily|neocloud_rate_card and gpurentalprices|neocloud_rate_card show much worse tail calibration (above_q90 0.123/ |
| S3      |           4 | exp_004 | False      | exp_003    | 0.1761 | 0.1384 | 0.1059 |          0.7945 | By group skill: leader improves dev skill notably over drift in fastgpu_daily|neocloud_spot (+0.242) and fastgpu_daily|hyperscaler_spot (+0.104), but is inferio |
| S3      |           5 | exp_005 | False      | exp_003    | 0.1761 | 0.1384 | 0.1059 |          0.7945 | Leader (window=60, floor=1.0, beta=1.0) outperforms drift notably in fastgpu_daily|neocloud_spot (leader: 0.25, drift: 0.008) and fastgpu_daily|hyperscaler_spot |
| S3      |           6 | exp_006 | False      | exp_003    | 0.1761 | 0.1384 | 0.1059 |          0.7945 | Skill by group for fastgpu_daily|neocloud_spot (drift: 0.008, leader: 0.25) and fastgpu_daily|hyperscaler_spot (drift: 0.001, leader: 0.105) shows leader heavil |