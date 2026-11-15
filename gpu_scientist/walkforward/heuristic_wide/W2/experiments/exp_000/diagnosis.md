# Diagnosis (dev origins only)

Cells: 1101. Overall skill 0.0739; truth above q50 in 42% of cells (50% if unbiased); above q90 40% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 132 |   0.2   |         0.25  |       0.159 |       0.114 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  54 |   0     |         0.222 |       0.222 |       0.407 |             -0.014 |
| fastgpu_daily|neocloud_rate_card   | 297 |  -0     |         0.522 |       0.522 |       0.051 |              0.005 |
| fastgpu_daily|neocloud_spot        | 189 |  -0     |         0.249 |       0.249 |       0.153 |              0.006 |
| gpurentalprices|marketplace_ask    |  33 |   0.238 |         0.303 |       0.091 |       0.03  |             -0.02  |
| gpurentalprices|neocloud_rate_card | 396 |   0.056 |         0.525 |       0.508 |       0.091 |              0.008 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 367 |   0.096 |         0.278 |       0.267 |       0.09  |              0.001 |
|              3 | 367 |   0.1   |         0.439 |       0.414 |       0.095 |              0.003 |
|              7 | 367 |   0.061 |         0.55  |       0.515 |       0.136 |              0.009 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 492 |   0.103 |         0.577 |       0.537 |       0.128 |              0.004 |
| 2-3          | 123 |   0.067 |         0.553 |       0.504 |       0.049 |              0.008 |
| 4-7          |  90 |   0.054 |         0.433 |       0.433 |       0.178 |             -0     |
| 8-30         | 303 |  -0.007 |         0.208 |       0.208 |       0.109 |              0.004 |
| >30          |  93 |   0     |         0.118 |       0.118 |       0     |              0.003 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |    6 |   0     |         0     |       0     |       0.833 |             -0.005 |
| more          |   15 |   0     |         0.267 |       0.267 |       0.133 |              0     |
| same          | 1080 |   0.075 |         0.427 |       0.403 |       0.103 |              0.004 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  33 |    -inf |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  27 |    -inf |         0     |       0     |       1     |             -0     |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                    |  27 |       0 |         0.111 |       0.111 |       0.667 |             -0.041 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median      |  27 |       0 |         0.741 |       0.741 |       0.037 |             -0.005 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median      |  27 |       0 |         0     |       0     |       0.037 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  27 |       0 |         0     |       0     |       0.111 |             -0.011 |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           |  27 |      -0 |         0.889 |       0.889 |       0.111 |              0.005 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  27 |       0 |         0.333 |       0.333 |       0.148 |              0.013 |

## Each base model alone: skill by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |   0.2   |
| fastgpu_daily|hyperscaler_spot     |  -0     |
| fastgpu_daily|neocloud_rate_card   |  -0     |
| fastgpu_daily|neocloud_spot        |  -0     |
| gpurentalprices|marketplace_ask    |   0.238 |
| gpurentalprices|neocloud_rate_card |   0.056 |

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
