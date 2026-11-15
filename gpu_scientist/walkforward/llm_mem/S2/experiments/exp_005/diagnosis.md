# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1595; truth above q50 in 47% of cells (50% if unbiased); above q90 12% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.009 |         0.223 |       0.07  |       0.04  |             -0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.136 |         0.261 |       0.13  |       0.123 |             -0.002 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.17  |         0.528 |       0.092 |       0.142 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.195 |         0.427 |       0.153 |       0.145 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.073 |         0.243 |       0.041 |       0.027 |             -0.02  |
| gpurentalprices|neocloud_rate_card | 888 |   0.166 |         0.573 |       0.139 |       0.068 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |  -0.029 |         0.325 |       0.113 |       0.111 |              0.002 |
|              3 | 885 |   0.129 |         0.481 |       0.108 |       0.093 |              0.007 |
|              7 | 872 |   0.213 |         0.6   |       0.13  |       0.102 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.196 |         0.608 |       0.117 |       0.111 |              0.011 |
| 2-3          |  376 |   0.099 |         0.444 |       0.117 |       0.064 |              0.009 |
| 4-7          |  284 |   0.181 |         0.43  |       0.123 |       0.074 |              0.009 |
| 8-30         |  489 |   0.007 |         0.202 |       0.131 |       0.153 |              0.001 |
| >30          |  150 |   0.041 |         0.22  |       0.06  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.026 |         0.481 |       0.059 |       0.111 |              0.006 |
| more          |  394 |   0.143 |         0.604 |       0.053 |       0.069 |              0.015 |
| same          | 2113 |   0.177 |         0.442 |       0.133 |       0.107 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -1.619 |         0     |       0     |       0.013 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -1.327 |         0.261 |       0     |       0.014 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.954 |         0.176 |       0.027 |       0.243 |             -0.004 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  69 |   -0.525 |         0.797 |       0.116 |       0.087 |              0.006 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   -0.438 |         0.284 |       0.014 |       0     |              0.006 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.37  |         0.676 |       0.176 |       0.027 |              0.007 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  74 |   -0.259 |         0.473 |       0.122 |       0.054 |              0.009 |

## Each base model alone: skill by group
| group                              |   composition |   drift |
|:-----------------------------------|--------------:|--------:|
| afhubbard|hyperscaler_spot         |         0.089 |   0.169 |
| fastgpu_daily|hyperscaler_spot     |         0.073 |  -0.03  |
| fastgpu_daily|neocloud_rate_card   |         0.165 |   0.023 |
| fastgpu_daily|neocloud_spot        |         0.195 |  -0     |
| gpurentalprices|marketplace_ask    |         0.049 |   0.097 |
| gpurentalprices|neocloud_rate_card |         0.16  |   0.073 |

## Mean ensemble weight by group
| group                              |   composition |   drift |
|:-----------------------------------|--------------:|--------:|
| afhubbard|hyperscaler_spot         |           0.5 |     0.5 |
| fastgpu_daily|hyperscaler_spot     |           0.5 |     0.5 |
| fastgpu_daily|neocloud_rate_card   |           0.5 |     0.5 |
| fastgpu_daily|neocloud_spot        |           0.5 |     0.5 |
| gpurentalprices|marketplace_ask    |           0.5 |     0.5 |
| gpurentalprices|neocloud_rate_card |           0.5 |     0.5 |

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
