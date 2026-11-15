# Diagnosis (dev origins only)

Cells: 1101. Overall skill 0.0983; truth above q50 in 43% of cells (50% if unbiased); above q90 20% and below q10 8% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 132 |   0.102 |         0.273 |       0.023 |       0.038 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  54 |  -0.006 |         0.222 |       0.222 |       0.407 |             -0.014 |
| fastgpu_daily|neocloud_rate_card   | 297 |   0.038 |         0.522 |       0.269 |       0.051 |              0.005 |
| fastgpu_daily|neocloud_spot        | 189 |   0.037 |         0.249 |       0.249 |       0.153 |              0.006 |
| gpurentalprices|marketplace_ask    |  33 |   0.224 |         0.303 |       0.061 |       0.091 |             -0.038 |
| gpurentalprices|neocloud_rate_card | 396 |   0.109 |         0.538 |       0.205 |       0.025 |              0.008 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 367 |   0.144 |         0.286 |       0.144 |       0.079 |              0.001 |
|              3 | 367 |   0.043 |         0.447 |       0.153 |       0.063 |              0.003 |
|              7 | 367 |   0.111 |         0.556 |       0.316 |       0.087 |              0.008 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 492 |   0.144 |         0.593 |       0.236 |       0.069 |              0.003 |
| 2-3          | 123 |   0.108 |         0.553 |       0.22  |       0.033 |              0.008 |
| 4-7          |  90 |   0.126 |         0.433 |       0.233 |       0.144 |             -0     |
| 8-30         | 303 |  -0.053 |         0.208 |       0.195 |       0.109 |              0.004 |
| >30          |  93 |  -0.36  |         0.118 |       0.022 |       0     |              0.003 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |    6 |  -0.009 |         0     |       0     |       0.833 |             -0.005 |
| more          |   15 |  -0.382 |         0.267 |       0.2   |       0.133 |              0     |
| same          | 1080 |   0.102 |         0.434 |       0.206 |       0.071 |              0.004 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  33 | -inf     |         0     |           0 |       0     |              0     |
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  27 | -inf     |         0     |           0 |       0     |              0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  27 | -inf     |         0     |           0 |       1     |             -0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  33 | -inf     |         0     |           0 |       0     |              0     |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median   |  33 | -inf     |         0     |           0 |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  27 |   -8.666 |         0     |           0 |       0.037 |             -0     |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  27 |   -0.744 |         0.037 |           0 |       0.185 |             -0.001 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  27 |   -0.625 |         0     |           0 |       0.037 |             -0.002 |

## Each base model alone: skill by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |   0.29  |
| fastgpu_daily|hyperscaler_spot     |  -0     |
| fastgpu_daily|neocloud_rate_card   |  -0     |
| fastgpu_daily|neocloud_spot        |  -0     |
| gpurentalprices|marketplace_ask    |   0.237 |
| gpurentalprices|neocloud_rate_card |   0.052 |

## Mean ensemble weight by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |       1 |
| fastgpu_daily|hyperscaler_spot     |       1 |
| fastgpu_daily|neocloud_rate_card   |       1 |
| fastgpu_daily|neocloud_spot        |       1 |
| gpurentalprices|marketplace_ask    |       1 |
| gpurentalprices|neocloud_rate_card |       1 |

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
