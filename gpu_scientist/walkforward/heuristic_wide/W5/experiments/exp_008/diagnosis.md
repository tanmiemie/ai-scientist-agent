# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.2058; truth above q50 in 46% of cells (50% if unbiased); above q90 15% and below q10 9% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.129 |         0.227 |       0.063 |       0.047 |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.142 |         0.239 |       0.145 |       0.188 |             -0     |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.202 |         0.545 |       0.145 |       0.123 |              0.005 |
| fastgpu_daily|neocloud_spot        | 483 |   0.23  |         0.387 |       0.17  |       0.124 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.112 |         0.216 |       0.054 |       0.027 |             -0.012 |
| gpurentalprices|neocloud_rate_card | 888 |   0.229 |         0.553 |       0.182 |       0.056 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.072 |         0.32  |       0.112 |       0.092 |              0.003 |
|              3 | 885 |   0.157 |         0.467 |       0.128 |       0.092 |              0.008 |
|              7 | 872 |   0.257 |         0.588 |       0.212 |       0.095 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.24  |         0.608 |       0.153 |       0.083 |              0.012 |
| 2-3          |  376 |   0.16  |         0.396 |       0.122 |       0.061 |              0.01  |
| 4-7          |  284 |   0.196 |         0.394 |       0.155 |       0.102 |              0.009 |
| 8-30         |  489 |   0.075 |         0.202 |       0.166 |       0.168 |              0.001 |
| >30          |  150 |   0.124 |         0.22  |       0.14  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.084 |         0.407 |       0.089 |       0.126 |              0.009 |
| more          |  394 |   0.2   |         0.543 |       0.081 |       0.074 |              0.016 |
| same          | 2113 |   0.219 |         0.445 |       0.167 |       0.094 |              0.009 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -1.261 |         0     |       0     |       0.04  |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.136 |         0.176 |       0.014 |       0.189 |             -0.004 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.029 |         0.676 |       0.203 |       0.027 |              0.008 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |    0.013 |         0.203 |       0.159 |       0.145 |              0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |    0.02  |         0.261 |       0.043 |       0.072 |              0.003 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  69 |    0.051 |         0.116 |       0.072 |       0.116 |             -0     |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |    0.061 |         0.554 |       0.203 |       0     |              0.069 |

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
