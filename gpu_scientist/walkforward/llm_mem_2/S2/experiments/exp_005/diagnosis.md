# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1626; truth above q50 in 46% of cells (50% if unbiased); above q90 11% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |  -0.042 |         0.223 |       0.077 |       0.043 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.149 |         0.239 |       0.123 |       0.123 |             -0.002 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.164 |         0.522 |       0.09  |       0.137 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.172 |         0.427 |       0.145 |       0.145 |              0.012 |
| gpurentalprices|marketplace_ask    |  74 |   0.05  |         0.203 |       0.041 |       0.027 |             -0.024 |
| gpurentalprices|neocloud_rate_card | 888 |   0.195 |         0.565 |       0.135 |       0.059 |              0.019 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |  -0.071 |         0.322 |       0.114 |       0.11  |              0.002 |
|              3 | 885 |   0.134 |         0.472 |       0.103 |       0.087 |              0.007 |
|              7 | 872 |   0.224 |         0.592 |       0.125 |       0.096 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.197 |         0.602 |       0.114 |       0.108 |              0.01  |
| 2-3          |  376 |   0.08  |         0.441 |       0.106 |       0.048 |              0.009 |
| 4-7          |  284 |   0.204 |         0.394 |       0.12  |       0.063 |              0.009 |
| 8-30         |  489 |   0.026 |         0.202 |       0.131 |       0.157 |              0.001 |
| >30          |  150 |   0.056 |         0.22  |       0.067 |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |  -0.01  |         0.459 |       0.059 |       0.081 |              0.003 |
| more          |  394 |   0.158 |         0.591 |       0.051 |       0.071 |              0.015 |
| same          | 2113 |   0.18  |         0.437 |       0.129 |       0.104 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -1.845 |         0     |       0     |       0.053 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -1.106 |         0.261 |       0     |       0.014 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.759 |         0.176 |       0.041 |       0.203 |             -0.004 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  69 |   -0.414 |         0.812 |       0.101 |       0.072 |              0.006 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   -0.281 |         0.284 |       0.014 |       0     |              0.006 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.263 |         0.676 |       0.162 |       0.027 |              0.007 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  74 |   -0.165 |         0.473 |       0.108 |       0.054 |              0.008 |

## Each base model alone: skill by group
| group                              |   composition |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |         0.089 |
| fastgpu_daily|hyperscaler_spot     |         0.073 |
| fastgpu_daily|neocloud_rate_card   |         0.165 |
| fastgpu_daily|neocloud_spot        |         0.195 |
| gpurentalprices|marketplace_ask    |         0.049 |
| gpurentalprices|neocloud_rate_card |         0.16  |

## Mean ensemble weight by group
| group                              |   composition |
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
