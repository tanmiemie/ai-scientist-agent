# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1517; truth above q50 in 46% of cells (50% if unbiased); above q90 25% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.195 |         0.227 |       0.053 |       0.117 |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.081 |         0.261 |       0.159 |       0.217 |             -0.001 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.138 |         0.544 |       0.273 |       0.132 |              0.004 |
| fastgpu_daily|neocloud_spot        | 483 |   0.192 |         0.387 |       0.271 |       0.124 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.105 |         0.243 |       0.041 |       0.027 |             -0.014 |
| gpurentalprices|neocloud_rate_card | 888 |   0.166 |         0.564 |       0.324 |       0.035 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.097 |         0.32  |       0.148 |       0.072 |              0.003 |
|              3 | 885 |   0.157 |         0.473 |       0.245 |       0.096 |              0.008 |
|              7 | 872 |   0.16  |         0.597 |       0.366 |       0.125 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.185 |         0.608 |       0.3   |       0.081 |              0.012 |
| 2-3          |  376 |   0.118 |         0.404 |       0.202 |       0.069 |              0.01  |
| 4-7          |  284 |   0.142 |         0.43  |       0.208 |       0.116 |              0.009 |
| 8-30         |  489 |   0.017 |         0.202 |       0.196 |       0.184 |              0.001 |
| >30          |  150 |   0     |         0.22  |       0.22  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.051 |         0.43  |       0.259 |       0.141 |              0.009 |
| more          |  394 |   0.19  |         0.566 |       0.223 |       0.074 |              0.015 |
| same          | 2113 |   0.148 |         0.446 |       0.257 |       0.099 |              0.009 |

## Worst series
| series_id                                                       |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |  -0.572 |         0     |       0     |       0.147 |             -0.003 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |  -0.052 |         0.261 |       0.174 |       0.188 |              0.005 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |  -0.025 |         0.261 |       0.246 |       0.072 |              0.003 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |  -0.003 |         0.554 |       0.473 |       0     |              0.069 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   0.01  |         0.284 |       0.284 |       0     |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  69 |   0.024 |         0.116 |       0.101 |       0.116 |             -0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  69 |   0.043 |         0.217 |       0.188 |       0.783 |             -0.001 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median   |  74 |   0.044 |         0.405 |       0.216 |       0.027 |              0.015 |

## Each base model alone: skill by group
| group                              |   drift |   vol_tail |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |   0.169 |      0.168 |
| fastgpu_daily|hyperscaler_spot     |  -0.03  |      0.105 |
| fastgpu_daily|neocloud_rate_card   |   0.023 |      0.137 |
| fastgpu_daily|neocloud_spot        |  -0     |      0.2   |
| gpurentalprices|marketplace_ask    |   0.097 |      0.095 |
| gpurentalprices|neocloud_rate_card |   0.073 |      0.16  |

## Mean ensemble weight by group
| group                              |   drift |   vol_tail |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |     0.5 |        0.5 |
| fastgpu_daily|hyperscaler_spot     |     0.5 |        0.5 |
| fastgpu_daily|neocloud_rate_card   |     0.5 |        0.5 |
| fastgpu_daily|neocloud_spot        |     0.5 |        0.5 |
| gpurentalprices|marketplace_ask    |     0.5 |        0.5 |
| gpurentalprices|neocloud_rate_card |     0.5 |        0.5 |

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
