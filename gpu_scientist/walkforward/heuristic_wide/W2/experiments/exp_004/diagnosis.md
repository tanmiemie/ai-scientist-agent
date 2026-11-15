# Diagnosis (dev origins only)

Cells: 1101. Overall skill 0.0848; truth above q50 in 41% of cells (50% if unbiased); above q90 17% and below q10 8% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 132 |   0.137 |         0.242 |       0.045 |       0.023 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  54 |   0.011 |         0.278 |       0.222 |       0.296 |             -0.004 |
| fastgpu_daily|neocloud_rate_card   | 297 |   0.014 |         0.461 |       0.209 |       0.088 |              0.004 |
| fastgpu_daily|neocloud_spot        | 189 |   0.037 |         0.249 |       0.249 |       0.153 |              0.006 |
| gpurentalprices|marketplace_ask    |  33 |   0.15  |         0.364 |       0.03  |       0.03  |             -0.014 |
| gpurentalprices|neocloud_rate_card | 396 |   0.116 |         0.525 |       0.159 |       0.028 |              0.007 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 367 |   0.134 |         0.278 |       0.134 |       0.076 |              0.001 |
|              3 | 367 |   0.007 |         0.422 |       0.125 |       0.068 |              0.003 |
|              7 | 367 |   0.106 |         0.529 |       0.262 |       0.09  |              0.01  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 492 |   0.127 |         0.555 |       0.171 |       0.073 |              0.005 |
| 2-3          | 123 |   0.047 |         0.528 |       0.22  |       0.049 |              0.007 |
| 4-7          |  90 |   0.166 |         0.433 |       0.222 |       0.122 |             -0.001 |
| 8-30         | 303 |  -0.049 |         0.208 |       0.198 |       0.109 |              0.004 |
| >30          |  93 |  -0.38  |         0.118 |       0     |       0     |              0.003 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |    6 |  -0.009 |         0     |       0     |       0.833 |             -0.005 |
| more          |   15 |  -0.304 |         0.267 |       0.2   |       0.133 |              0     |
| same          | 1080 |   0.088 |         0.414 |       0.174 |       0.073 |              0.004 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  33 | -inf     |         0     |           0 |       0     |              0     |
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  27 | -inf     |         0     |           0 |       0     |              0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  27 | -inf     |         0     |           0 |       1     |             -0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  33 | -inf     |         0     |           0 |       0     |              0     |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median   |  33 | -inf     |         0     |           0 |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  27 |   -7.218 |         0     |           0 |       0.037 |             -0     |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  27 |   -0.602 |         0.037 |           0 |       0.185 |             -0.001 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  27 |   -0.52  |         0     |           0 |       0.037 |             -0.002 |

## Each base model alone: skill by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |         0.261 |
| fastgpu_daily|hyperscaler_spot     |         0.014 |
| fastgpu_daily|neocloud_rate_card   |         0.006 |
| fastgpu_daily|neocloud_spot        |        -0     |
| gpurentalprices|marketplace_ask    |         0.148 |
| gpurentalprices|neocloud_rate_card |         0.165 |

## Mean ensemble weight by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |             1 |
| fastgpu_daily|hyperscaler_spot     |             1 |
| fastgpu_daily|neocloud_rate_card   |             1 |
| fastgpu_daily|neocloud_spot        |             1 |
| gpurentalprices|marketplace_ask    |             1 |
| gpurentalprices|neocloud_rate_card |             1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                            | leader                                                         |   lag_days |   corr |
|:------------------------------------------------------------------|:---------------------------------------------------------------|-----------:|-------:|
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median     |          1 |  0.896 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median |          1 | -0.515 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median          | afhubbard.hyperscaler_spot.B200.spot.median                    |          5 | -0.513 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | afhubbard.hyperscaler_spot.H100_SXM_80GB.spot.median           |          1 | -0.464 |
| gpurentalprices.neocloud_rate_card.A100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.A100_SXM_80GB.spot.median     |          5 |  0.418 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  | afhubbard.neocloud_rate_card.RTX_PRO_6000.on_demand.median     |          1 |  0.398 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_spot.H200.spot.median              |          5 |  0.338 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | afhubbard.neocloud_rate_card.H200.on_demand.median             |          4 |  0.326 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median         |          5 |  0.312 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_spot.H100_80GB.spot.median            |          3 | -0.308 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median     | gpurentalprices.marketplace_ask.H100_80GB.spot.median          |          1 |  0.308 |
