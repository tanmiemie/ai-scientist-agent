# LLM-written models: gate results (llm_coder)

22 generated models (attempts, including fixes after a failed gate).

| gate | passed | failed here |
|---|---|---|
| static | 18 | 4 |
| smoke | 18 | 0 |
| lookahead | 18 | 0 |
| spec check after the gates | 18 | 0 |

Ran on DEV and met the HOLDOUT gate: 18; sandboxed run failed: 0; accepted: 6.

| slice | iter | attempt | model | passed | failed | experiment | accepted |
|---|---|---|---|---|---|---|---|
| S1 | 1 | 1 | `empirical_quantiles` | static, smoke, lookahead | - | exp_001 | yes |
| S1 | 2 | 1 | `vol_tail` | - | static | - | - |
| S1 | 2 | 2 | `vol_adapt` | static, smoke, lookahead | - | exp_002 | no |
| S1 | 3 | 1 | `trend_aware_empirical` | static, smoke, lookahead | - | exp_003 | no |
| S1 | 4 | 1 | `stale_aware_quantiles` | static, smoke, lookahead | - | exp_004 | no |
| S1 | 5 | 1 | `gentle_stale_aware_quantiles` | static, smoke, lookahead | - | exp_005 | no |
| S1 | 6 | 1 | `leader_quantiles` | static, smoke, lookahead | - | exp_006 | no |
| S2 | 1 | 1 | `wide_drift` | - | static | - | - |
| S2 | 1 | 2 | `wide_drift` | static, smoke, lookahead | - | exp_001 | yes |
| S2 | 2 | 1 | `vol_weighted_drift` | static, smoke, lookahead | - | exp_002 | yes |
| S2 | 3 | 1 | `vol_weighted_drift_broader` | static, smoke, lookahead | - | exp_003 | no |
| S2 | 4 | 1 | `peer_leader_lag` | static, smoke, lookahead | - | exp_004 | no |
| S2 | 5 | 1 | `vol_weighted_drift_floor` | static, smoke, lookahead | - | exp_005 | yes |
| S2 | 6 | 1 | `vol_weighted_drift_floor` | - | static | - | - |
| S2 | 6 | 2 | `vol_weighted_drift_floor2` | static, smoke, lookahead | - | exp_006 | no |
| S3 | 1 | 1 | `log_empirical_window` | static, smoke, lookahead | - | exp_001 | no |
| S3 | 2 | 1 | `simple_leader` | static, smoke, lookahead | - | exp_002 | no |
| S3 | 3 | 1 | `log_empirical_window` | static, smoke, lookahead | - | exp_003 | yes |
| S3 | 4 | 1 | `log_empirical_window` | - | static | - | - |
| S3 | 4 | 2 | `log_empirical_wide_window` | static, smoke, lookahead | - | exp_004 | yes |
| S3 | 5 | 1 | `log_empirical_scaled_window` | static, smoke, lookahead | - | exp_005 | no |
| S3 | 6 | 1 | `log_empirical_adjvol_window` | static, smoke, lookahead | - | exp_006 | no |

## Gate failures (last 300 characters of the error fed back)

- S1 iter 2 attempt 1 `vol_tail`, static:
  ```
  a model named 'vol_tail' already exists; pick a new name
  ```
- S2 iter 1 attempt 1 `wide_drift`, static:
  ```
  defaults must map parameter names to numbers; got 'window': None
  ```
- S2 iter 6 attempt 1 `vol_weighted_drift_floor`, static:
  ```
  a model named 'vol_weighted_drift_floor' already exists; pick a new name
  ```
- S3 iter 4 attempt 1 `log_empirical_window`, static:
  ```
  a model named 'log_empirical_window' already exists; pick a new name
  ```
