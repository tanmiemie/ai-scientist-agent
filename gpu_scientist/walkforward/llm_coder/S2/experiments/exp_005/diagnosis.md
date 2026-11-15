# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1851; truth above q50 in 45% of cells (50% if unbiased); above q90 17% and below q10 5% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.212 |         0.227 |       0.08  |       0.063 |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.228 |         0.239 |       0.152 |       0.13  |             -0     |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.186 |         0.536 |       0.138 |       0.094 |              0.004 |
| fastgpu_daily|neocloud_spot        | 483 |   0.237 |         0.387 |       0.213 |       0.023 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.135 |         0.176 |       0.041 |       0.068 |             -0.025 |
| gpurentalprices|neocloud_rate_card | 888 |   0.175 |         0.553 |       0.209 |       0.009 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.052 |         0.316 |       0.07  |       0.032 |              0.002 |
|              3 | 885 |   0.165 |         0.462 |       0.149 |       0.051 |              0.007 |
|              7 | 872 |   0.222 |         0.585 |       0.284 |       0.068 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.212 |         0.6   |       0.194 |       0.048 |              0.011 |
| 2-3          |  376 |   0.128 |         0.396 |       0.144 |       0.045 |              0.01  |
| 4-7          |  284 |   0.154 |         0.394 |       0.194 |       0.081 |              0.009 |
| 8-30         |  489 |   0.151 |         0.202 |       0.104 |       0.055 |              0.001 |
| >30          |  150 |   0.034 |         0.22  |       0.14  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.159 |         0.407 |       0.178 |       0.104 |              0.009 |
| more          |  394 |   0.21  |         0.543 |       0.165 |       0.025 |              0.015 |
| same          | 2113 |   0.179 |         0.44  |       0.167 |       0.051 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -0.466 |         0     |       0     |       0.013 |             -0.003 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |   -0.054 |         0.554 |       0.162 |       0     |              0.069 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |    0.006 |         0.261 |       0.014 |       0     |              0.003 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  69 |    0.015 |         0.116 |       0.101 |       0.116 |             -0     |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median   |  74 |    0.082 |         0.27  |       0.189 |       0     |              0.014 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |    0.088 |         0.203 |       0.159 |       0.174 |              0.003 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |    0.089 |         0.284 |       0.149 |       0     |              0.006 |

## Each base model alone: skill by group
| group                              |   vol_weighted_drift_floor |
|:-----------------------------------|---------------------------:|
| afhubbard|hyperscaler_spot         |                      0.212 |
| fastgpu_daily|hyperscaler_spot     |                      0.228 |
| fastgpu_daily|neocloud_rate_card   |                      0.186 |
| fastgpu_daily|neocloud_spot        |                      0.237 |
| gpurentalprices|marketplace_ask    |                      0.135 |
| gpurentalprices|neocloud_rate_card |                      0.175 |

## Mean ensemble weight by group
| group                              |   vol_weighted_drift_floor |
|:-----------------------------------|---------------------------:|
| afhubbard|hyperscaler_spot         |                          1 |
| fastgpu_daily|hyperscaler_spot     |                          1 |
| fastgpu_daily|neocloud_rate_card   |                          1 |
| fastgpu_daily|neocloud_spot        |                          1 |
| gpurentalprices|marketplace_ask    |                          1 |
| gpurentalprices|neocloud_rate_card |                          1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                           | leader                                                                  |   lag_days |   corr |
|:-----------------------------------------------------------------|:------------------------------------------------------------------------|-----------:|-------:|
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_rate_card.B200.serverless.median               |          3 | -0.974 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_spot.B200.spot.median                          |          1 |  0.974 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      | gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median           |          3 | -0.956 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median       |          2 |  0.933 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median                 |          4 |  0.868 |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median              |          1 |  0.86  |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | afhubbard.hyperscaler_list.B300.on_demand.median                        |          1 | -0.856 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median        |          1 |  0.787 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 | fastgpu_daily.neocloud_spot.A100_40GB.spot.median                       |          1 | -0.764 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median       |          3 |  0.761 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    | fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median             |          1 | -0.724 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median         | afhubbard.neocloud_rate_card.B300.on_demand.median                      |          1 |  0.713 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median    | gpurentalprices_cheapest.aggregator_cheapest.RTX_A6000.on_demand.median |          2 | -0.712 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median             |          5 |  0.711 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      | gpurentalprices_cheapest.aggregator_cheapest.RTX_A6000.on_demand.median |          5 |  0.705 |
