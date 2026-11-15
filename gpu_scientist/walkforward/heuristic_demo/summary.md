# Walk-forward check (heuristic, 6 iterations per slice, seed 00_drift.json)

Every TEST week lies after all the data its slice's decisions used.

| slice   |   seed TEST |   final TEST |    gain | final champion   |   iterations |
|:--------|------------:|-------------:|--------:|:-----------------|-------------:|
| S1      |      0.1452 |       0.1938 |  0.0486 | exp_003          |            7 |
| S2      |      0.0216 |       0.1072 |  0.0857 | exp_001          |            7 |
| S3      |      0.0774 |       0.0437 | -0.0336 | exp_002          |            7 |

Mean TEST gain seed -> final champion: +0.0335 (2/3 slices improved)

## Every iteration

| slice   |   iteration | exp     | accepted   | champion   |    dev |   gate |   test |   test_coverage | hypothesis                                                                                                                                                       |
|:--------|------------:|:--------|:-----------|:-----------|-------:|-------:|-------:|----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S1      |           0 | exp_000 | True       | exp_000    | 0.0459 | 0.0493 | 0.1452 |          0.4692 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S1      |           1 | exp_001 | True       | exp_001    | 0.198  | 0.1487 | 0.2023 |          0.8541 | no calibration; truth above q90 in 41% and below q10 in 12% of dev cells (10% each if calibrated), coverage 0.46 -> Learning an upper and lower offset per colle |
| S1      |           2 | exp_002 | False      | exp_001    | 0.198  | 0.1487 | 0.2023 |          0.8541 | champion model drift has dev skill 0.198, coverage 0.72 -> Replacing drift by trend_tail (recent-window, step-aware) should fit posted prices better. Change: pr |
| S1      |           3 | exp_003 | True       | exp_003    | 0.2027 | 0.1526 | 0.1938 |          0.8369 | champion model drift has dev skill 0.198, coverage 0.72 -> Replacing drift by momentum (recent-window, step-aware) should fit posted prices better. Change: prim |
| S1      |           4 | exp_004 | False      | exp_003    | 0.2027 | 0.1526 | 0.1938 |          0.8369 | champion model momentum has dev skill 0.203, coverage 0.71 -> Replacing momentum by step_hazard (recent-window, step-aware) should fit posted prices better. Cha |
| S1      |           5 | exp_005 | False      | exp_003    | 0.2027 | 0.1526 | 0.1938 |          0.8369 | champion model momentum has dev skill 0.203, coverage 0.71 -> Replacing momentum by vol_tail (recent-window, step-aware) should fit posted prices better. Change |
| S1      |           6 | exp_006 | False      | exp_003    | 0.2027 | 0.1526 | 0.1938 |          0.8369 | dev coverage 0.71 (above q90 0.16, below q10 0.12; target 0.80 / 0.10 / 0.10) -> Calibration reacts too slowly to misses; a larger step should pull coverage to  |
| S2      |           0 | exp_000 | True       | exp_000    | 0.0474 | 0.1452 | 0.0216 |          0.5365 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S2      |           1 | exp_001 | True       | exp_001    | 0.1765 | 0.2023 | 0.1072 |          0.7196 | no calibration; truth above q90 in 42% and below q10 in 12% of dev cells (10% each if calibrated), coverage 0.46 -> Learning an upper and lower offset per colle |
| S2      |           2 | exp_002 | False      | exp_001    | 0.1765 | 0.2023 | 0.1072 |          0.7196 | champion model drift has dev skill 0.176, coverage 0.76 -> Replacing drift by trend_tail (recent-window, step-aware) should fit posted prices better. Change: pr |
| S2      |           3 | exp_003 | False      | exp_001    | 0.1765 | 0.2023 | 0.1072 |          0.7196 | champion model drift has dev skill 0.176, coverage 0.76 -> Replacing drift by momentum (recent-window, step-aware) should fit posted prices better. Change: prim |
| S2      |           4 | exp_004 | False      | exp_001    | 0.1765 | 0.2023 | 0.1072 |          0.7196 | champion model drift has dev skill 0.176, coverage 0.76 -> Replacing drift by step_hazard (recent-window, step-aware) should fit posted prices better. Change: p |
| S2      |           5 | exp_005 | False      | exp_001    | 0.1765 | 0.2023 | 0.1072 |          0.7196 | champion model drift has dev skill 0.176, coverage 0.76 -> Replacing drift by vol_tail (recent-window, step-aware) should fit posted prices better. Change: prim |
| S2      |           6 | exp_006 | False      | exp_001    | 0.1765 | 0.2023 | 0.1072 |          0.7196 | dev coverage 0.76 (above q90 0.14, below q10 0.09; target 0.80 / 0.10 / 0.10) -> Calibration reacts too slowly to misses; a larger step should pull coverage to  |
| S3      |           0 | exp_000 | True       | exp_000    | 0.0698 | 0.0216 | 0.0774 |          0.6386 | Reference: the starter kit's drift baseline (whole-history empirical random walk), re-run through our walk-forward pipeline on daily origins.                    |
| S3      |           1 | exp_001 | True       | exp_001    | 0.1824 | 0.1072 | 0.0217 |          0.7752 | no calibration; truth above q90 in 41% and below q10 in 13% of dev cells (10% each if calibrated), coverage 0.46 -> Learning an upper and lower offset per colle |
| S3      |           2 | exp_002 | True       | exp_002    | 0.1844 | 0.1236 | 0.0437 |          0.7959 | champion model drift has dev skill 0.182, coverage 0.78 -> Replacing drift by trend_tail (recent-window, step-aware) should fit posted prices better. Change: pr |
| S3      |           3 | exp_003 | False      | exp_002    | 0.1844 | 0.1236 | 0.0437 |          0.7959 | champion model trend_tail has dev skill 0.184, coverage 0.79 -> Replacing trend_tail by momentum (recent-window, step-aware) should fit posted prices better. Ch |
| S3      |           4 | exp_004 | False      | exp_002    | 0.1844 | 0.1236 | 0.0437 |          0.7959 | champion model trend_tail has dev skill 0.184, coverage 0.79 -> Replacing trend_tail by step_hazard (recent-window, step-aware) should fit posted prices better. |
| S3      |           5 | exp_005 | False      | exp_002    | 0.1844 | 0.1236 | 0.0437 |          0.7959 | champion model trend_tail has dev skill 0.184, coverage 0.79 -> Replacing trend_tail by vol_tail (recent-window, step-aware) should fit posted prices better. Ch |
| S3      |           6 | exp_006 | False      | exp_002    | 0.1844 | 0.1236 | 0.0437 |          0.7959 | pooled 0.184 vs geomean 0.120: quiet series score much worse -> One calibration offset per group over-widens low-volatility series; a smaller step per update sh |