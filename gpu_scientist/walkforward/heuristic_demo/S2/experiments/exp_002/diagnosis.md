# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1832; truth above q50 in 45% of cells (50% if unbiased); above q90 13% and below q10 9% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.028 |         0.24  |       0.093 |       0.047 |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.167 |         0.239 |       0.145 |       0.181 |             -0     |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.204 |         0.526 |       0.132 |       0.116 |              0.005 |
| fastgpu_daily|neocloud_spot        | 483 |   0.186 |         0.387 |       0.147 |       0.124 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.113 |         0.216 |       0.041 |       0.027 |             -0.012 |
| gpurentalprices|neocloud_rate_card | 888 |   0.183 |         0.553 |       0.148 |       0.053 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.039 |         0.318 |       0.115 |       0.088 |              0.003 |
|              3 | 885 |   0.109 |         0.461 |       0.119 |       0.089 |              0.008 |
|              7 | 872 |   0.25  |         0.584 |       0.167 |       0.091 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.215 |         0.602 |       0.137 |       0.076 |              0.012 |
| 2-3          |  376 |   0.129 |         0.388 |       0.12  |       0.069 |              0.01  |
| 4-7          |  284 |   0.185 |         0.394 |       0.134 |       0.088 |              0.009 |
| 8-30         |  489 |   0.074 |         0.202 |       0.149 |       0.17  |              0.001 |
| >30          |  150 |   0.039 |         0.22  |       0.087 |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.056 |         0.407 |       0.089 |       0.119 |              0.009 |
| more          |  394 |   0.152 |         0.505 |       0.071 |       0.061 |              0.016 |
| same          | 2113 |   0.206 |         0.447 |       0.148 |       0.093 |              0.009 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -1.755 |         0     |       0     |       0.053 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.439 |         0.176 |       0.027 |       0.23  |             -0.004 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -0.311 |         0.261 |       0.029 |       0.072 |              0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.137 |         0.676 |       0.176 |       0.027 |              0.008 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   -0.056 |         0.284 |       0     |       0     |              0.006 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  74 |   -0.005 |         0.473 |       0.135 |       0     |              0.009 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |    0.009 |         0.203 |       0.159 |       0.145 |              0.003 |

## Each base model alone: skill by group
| group                              |   trend_tail |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |        0.127 |
| fastgpu_daily|hyperscaler_spot     |        0.107 |
| fastgpu_daily|neocloud_rate_card   |        0.169 |
| fastgpu_daily|neocloud_spot        |        0.205 |
| gpurentalprices|marketplace_ask    |        0.113 |
| gpurentalprices|neocloud_rate_card |        0.142 |

## Mean ensemble weight by group
| group                              |   trend_tail |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |            1 |
| fastgpu_daily|hyperscaler_spot     |            1 |
| fastgpu_daily|neocloud_rate_card   |            1 |
| fastgpu_daily|neocloud_spot        |            1 |
| gpurentalprices|marketplace_ask    |            1 |
| gpurentalprices|neocloud_rate_card |            1 |

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
