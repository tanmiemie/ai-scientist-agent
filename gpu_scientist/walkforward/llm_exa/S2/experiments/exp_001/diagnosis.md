# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1314; truth above q50 in 46% of cells (50% if unbiased); above q90 33% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.192 |         0.227 |       0.083 |       0.133 |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.068 |         0.261 |       0.159 |       0.225 |             -0.001 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.129 |         0.544 |       0.373 |       0.132 |              0.004 |
| fastgpu_daily|neocloud_spot        | 483 |   0.143 |         0.387 |       0.335 |       0.124 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.109 |         0.243 |       0.041 |       0.027 |             -0.014 |
| gpurentalprices|neocloud_rate_card | 888 |   0.133 |         0.564 |       0.423 |       0.059 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.09  |         0.32  |       0.242 |       0.078 |              0.003 |
|              3 | 885 |   0.136 |         0.473 |       0.318 |       0.11  |              0.008 |
|              7 | 872 |   0.138 |         0.597 |       0.431 |       0.136 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.158 |         0.608 |       0.429 |       0.1   |              0.012 |
| 2-3          |  376 |   0.106 |         0.404 |       0.266 |       0.072 |              0.01  |
| 4-7          |  284 |   0.13  |         0.43  |       0.232 |       0.12  |              0.009 |
| 8-30         |  489 |   0.017 |         0.202 |       0.196 |       0.184 |              0.001 |
| >30          |  150 |   0     |         0.22  |       0.22  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.026 |         0.43  |       0.348 |       0.141 |              0.009 |
| more          |  394 |   0.194 |         0.566 |       0.282 |       0.074 |              0.015 |
| same          | 2113 |   0.12  |         0.446 |       0.337 |       0.112 |              0.009 |

## Worst series
| series_id                                                       |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |  -0.696 |         0     |       0     |       0.147 |             -0.003 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |  -0.041 |         0.261 |       0.174 |       0.188 |              0.005 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |   0     |         0.554 |       0.459 |       0     |              0.069 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  69 |   0.031 |         0.116 |       0.101 |       0.116 |             -0     |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median     |  69 |   0.041 |         0.696 |       0.522 |       0.159 |             -0.009 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   0.048 |         0.284 |       0.284 |       0     |              0.006 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median   |  74 |   0.049 |         0.405 |       0.23  |       0.108 |              0.015 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   0.057 |         0.261 |       0.246 |       0.072 |              0.003 |

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
