# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1579; truth above q50 in 46% of cells (50% if unbiased); above q90 13% and below q10 9% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.093 |         0.227 |       0.063 |       0.043 |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.164 |         0.239 |       0.145 |       0.181 |             -0     |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.17  |         0.545 |       0.126 |       0.116 |              0.005 |
| fastgpu_daily|neocloud_spot        | 483 |   0.173 |         0.387 |       0.147 |       0.124 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.096 |         0.216 |       0.041 |       0.068 |             -0.012 |
| gpurentalprices|neocloud_rate_card | 888 |   0.154 |         0.553 |       0.142 |       0.053 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.058 |         0.32  |       0.111 |       0.09  |              0.003 |
|              3 | 885 |   0.081 |         0.467 |       0.113 |       0.09  |              0.008 |
|              7 | 872 |   0.216 |         0.588 |       0.157 |       0.089 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.177 |         0.608 |       0.127 |       0.078 |              0.012 |
| 2-3          |  376 |   0.126 |         0.396 |       0.104 |       0.066 |              0.01  |
| 4-7          |  284 |   0.17  |         0.394 |       0.127 |       0.088 |              0.009 |
| 8-30         |  489 |   0.078 |         0.202 |       0.153 |       0.17  |              0.001 |
| >30          |  150 |   0.076 |         0.22  |       0.093 |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.082 |         0.407 |       0.089 |       0.119 |              0.009 |
| more          |  394 |   0.078 |         0.543 |       0.066 |       0.061 |              0.016 |
| same          | 2113 |   0.192 |         0.445 |       0.141 |       0.094 |              0.009 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -1.026 |         0     |       0     |       0.053 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.548 |         0.176 |       0.027 |       0.216 |             -0.004 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -0.322 |         0.261 |       0.072 |       0.072 |              0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.235 |         0.676 |       0.189 |       0.027 |              0.008 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  74 |   -0.14  |         0.473 |       0.162 |       0     |              0.009 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   -0.126 |         0.284 |       0     |       0     |              0.006 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |   -0.095 |         0.203 |       0.159 |       0.145 |              0.003 |

## Each base model alone: skill by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.171 |
| fastgpu_daily|hyperscaler_spot     |      0.103 |
| fastgpu_daily|neocloud_rate_card   |      0.134 |
| fastgpu_daily|neocloud_spot        |      0.2   |
| gpurentalprices|marketplace_ask    |      0.102 |
| gpurentalprices|neocloud_rate_card |      0.16  |

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
