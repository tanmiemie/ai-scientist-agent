# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1922; truth above q50 in 45% of cells (50% if unbiased); above q90 15% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.142 |         0.217 |       0.05  |       0.05  |             -0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.053 |         0.37  |       0.159 |       0.203 |              0.009 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.176 |         0.476 |       0.162 |       0.142 |              0.002 |
| fastgpu_daily|neocloud_spot        | 483 |   0.266 |         0.385 |       0.168 |       0.147 |              0.01  |
| gpurentalprices|marketplace_ask    |  74 |  -0.008 |         0.378 |       0.014 |       0.027 |             -0.012 |
| gpurentalprices|neocloud_rate_card | 888 |   0.237 |         0.565 |       0.172 |       0.057 |              0.019 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.084 |         0.315 |       0.121 |       0.099 |              0.002 |
|              3 | 885 |   0.117 |         0.463 |       0.127 |       0.111 |              0.007 |
|              7 | 872 |   0.252 |         0.578 |       0.202 |       0.102 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.231 |         0.583 |       0.15  |       0.093 |              0.011 |
| 2-3          |  376 |   0.122 |         0.41  |       0.122 |       0.09  |              0.01  |
| 4-7          |  284 |   0.17  |         0.437 |       0.173 |       0.12  |              0.01  |
| 8-30         |  489 |   0.077 |         0.202 |       0.166 |       0.168 |              0.001 |
| >30          |  150 |   0.149 |         0.22  |       0.12  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.041 |         0.481 |       0.081 |       0.185 |              0.009 |
| more          |  394 |   0.187 |         0.513 |       0.091 |       0.069 |              0.012 |
| same          | 2113 |   0.208 |         0.438 |       0.165 |       0.106 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -1.008 |         0     |       0     |       0.053 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.17  |         0.23  |       0.014 |       0.189 |             -0.003 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |   -0.132 |         0.478 |       0.174 |       0.174 |              0.023 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -0.118 |         0.261 |       0.043 |       0.072 |              0.002 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  69 |   -0.024 |         0.116 |       0.072 |       0.116 |             -0     |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median           |  74 |   -0.008 |         0.378 |       0.014 |       0.027 |             -0.012 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |   -0.001 |         0.554 |       0.297 |       0     |              0.068 |

## Each base model alone: skill by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |         0.193 |
| fastgpu_daily|hyperscaler_spot     |         0.012 |
| fastgpu_daily|neocloud_rate_card   |         0.128 |
| fastgpu_daily|neocloud_spot        |         0.165 |
| gpurentalprices|marketplace_ask    |        -0.012 |
| gpurentalprices|neocloud_rate_card |         0.114 |

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
