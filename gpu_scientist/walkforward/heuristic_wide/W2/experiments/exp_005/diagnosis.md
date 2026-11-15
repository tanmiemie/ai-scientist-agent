# Diagnosis (dev origins only)

Cells: 1101. Overall skill 0.1203; truth above q50 in 42% of cells (50% if unbiased); above q90 18% and below q10 7% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 132 |   0.067 |         0.25  |       0.076 |       0.015 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  54 |   0.24  |         0.222 |       0.222 |       0.259 |             -0.014 |
| fastgpu_daily|neocloud_rate_card   | 297 |   0.16  |         0.522 |       0.178 |       0.051 |              0.005 |
| fastgpu_daily|neocloud_spot        | 189 |   0.031 |         0.249 |       0.249 |       0.153 |              0.006 |
| gpurentalprices|marketplace_ask    |  33 |   0.131 |         0.364 |       0.061 |       0.091 |             -0.013 |
| gpurentalprices|neocloud_rate_card | 396 |   0.1   |         0.525 |       0.187 |       0.028 |              0.007 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 367 |   0.094 |         0.278 |       0.144 |       0.074 |              0.001 |
|              3 | 367 |   0.165 |         0.439 |       0.109 |       0.044 |              0.003 |
|              7 | 367 |   0.108 |         0.556 |       0.286 |       0.084 |              0.01  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 492 |   0.131 |         0.581 |       0.181 |       0.059 |              0.005 |
| 2-3          | 123 |   0.172 |         0.553 |       0.195 |       0.033 |              0.008 |
| 4-7          |  90 |   0.305 |         0.433 |       0.2   |       0.089 |             -0     |
| 8-30         | 303 |  -0.038 |         0.208 |       0.205 |       0.109 |              0.004 |
| >30          |  93 |  -0.341 |         0.118 |       0.054 |       0     |              0.003 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |    6 |  -0.053 |         0     |       0     |       0.833 |             -0.005 |
| more          |   15 |  -0.442 |         0.267 |       0.2   |       0.133 |              0     |
| same          | 1080 |   0.125 |         0.429 |       0.181 |       0.062 |              0.005 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  33 | -inf     |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  27 | -inf     |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  27 | -inf     |         0     |       0     |       1     |             -0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  33 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median   |  33 | -inf     |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  27 |   -3.462 |         0     |       0     |       0.037 |             -0     |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  27 |   -0.487 |         0.037 |       0     |       0.185 |             -0.001 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  33 |   -0.481 |         0.152 |       0.061 |       0.121 |             -0.004 |

## Each base model alone: skill by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.243 |
| fastgpu_daily|hyperscaler_spot     |      0.243 |
| fastgpu_daily|neocloud_rate_card   |      0.138 |
| fastgpu_daily|neocloud_spot        |     -0.008 |
| gpurentalprices|marketplace_ask    |      0.14  |
| gpurentalprices|neocloud_rate_card |      0.234 |

## Mean ensemble weight by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |          1 |
| fastgpu_daily|hyperscaler_spot     |          1 |
| fastgpu_daily|neocloud_rate_card   |          1 |
| fastgpu_daily|neocloud_spot        |          1 |
| gpurentalprices|marketplace_ask    |          1 |
| gpurentalprices|neocloud_rate_card |          1 |

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
