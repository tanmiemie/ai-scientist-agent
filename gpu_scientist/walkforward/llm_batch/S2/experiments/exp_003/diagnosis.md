# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1745; truth above q50 in 44% of cells (50% if unbiased); above q90 22% and below q10 13% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.152 |         0.237 |       0.027 |       0.097 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.097 |         0.225 |       0.159 |       0.225 |             -0.002 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.178 |         0.507 |       0.217 |       0.163 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.216 |         0.383 |       0.238 |       0.174 |              0.01  |
| gpurentalprices|marketplace_ask    |  74 |   0.077 |         0.203 |       0.041 |       0.027 |             -0.018 |
| gpurentalprices|neocloud_rate_card | 888 |   0.181 |         0.538 |       0.301 |       0.087 |              0.018 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.085 |         0.306 |       0.138 |       0.138 |              0.001 |
|              3 | 885 |   0.177 |         0.444 |       0.199 |       0.13  |              0.006 |
|              7 | 872 |   0.191 |         0.575 |       0.323 |       0.126 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.207 |         0.57  |       0.245 |       0.147 |              0.009 |
| 2-3          |  376 |   0.133 |         0.402 |       0.191 |       0.059 |              0.01  |
| 4-7          |  284 |   0.187 |         0.394 |       0.169 |       0.109 |              0.009 |
| 8-30         |  489 |   0.038 |         0.207 |       0.196 |       0.192 |              0.001 |
| >30          |  150 |  -0     |         0.233 |       0.233 |       0.02  |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.087 |         0.407 |       0.215 |       0.148 |              0.007 |
| more          |  394 |   0.214 |         0.508 |       0.183 |       0.132 |              0.013 |
| same          | 2113 |   0.169 |         0.431 |       0.227 |       0.13  |              0.007 |

## Worst series
| series_id                                                     |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median              |  75 |  -1.028 |         0.04  |       0     |       0.147 |             -0.004 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                 |  69 |   0.003 |         0.174 |       0.174 |       0.188 |              0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median |  74 |   0.01  |         0.527 |       0.351 |       0.095 |              0.067 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median |  74 |   0.038 |         0.338 |       0.297 |       0.108 |              0.025 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median   |  69 |   0.049 |         0.667 |       0.246 |       0.188 |             -0.01  |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median |  74 |   0.057 |         0.27  |       0.216 |       0.054 |              0.014 |
| fastgpu_daily.neocloud_spot.H200.spot.median                  |  69 |   0.064 |         0.348 |       0.174 |       0.072 |              0.005 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median   |  69 |   0.066 |         0.116 |       0.101 |       0.116 |             -0.003 |

## Each base model alone: skill by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |   0.169 |      0.05  |
| fastgpu_daily|hyperscaler_spot     |  -0.03  |      0.039 |
| fastgpu_daily|neocloud_rate_card   |   0.023 |      0.18  |
| fastgpu_daily|neocloud_spot        |  -0     |      0.221 |
| gpurentalprices|marketplace_ask    |   0.097 |      0.067 |
| gpurentalprices|neocloud_rate_card |   0.073 |      0.163 |

## Mean ensemble weight by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |    0.33 |       0.67 |
| fastgpu_daily|hyperscaler_spot     |    0.33 |       0.67 |
| fastgpu_daily|neocloud_rate_card   |    0.07 |       0.93 |
| fastgpu_daily|neocloud_spot        |    0.41 |       0.59 |
| gpurentalprices|marketplace_ask    |    0.34 |       0.66 |
| gpurentalprices|neocloud_rate_card |    0.1  |       0.9  |

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
