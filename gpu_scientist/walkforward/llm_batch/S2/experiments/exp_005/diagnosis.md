# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.174; truth above q50 in 45% of cells (50% if unbiased); above q90 21% and below q10 13% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.154 |         0.257 |       0.03  |       0.103 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.102 |         0.225 |       0.159 |       0.239 |             -0.002 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.178 |         0.51  |       0.209 |       0.162 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.22  |         0.385 |       0.224 |       0.182 |              0.01  |
| gpurentalprices|marketplace_ask    |  74 |   0.077 |         0.203 |       0.041 |       0.027 |             -0.018 |
| gpurentalprices|neocloud_rate_card | 888 |   0.179 |         0.544 |       0.294 |       0.088 |              0.018 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.081 |         0.312 |       0.132 |       0.146 |              0.001 |
|              3 | 885 |   0.174 |         0.45  |       0.193 |       0.134 |              0.006 |
|              7 | 872 |   0.193 |         0.579 |       0.314 |       0.123 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.207 |         0.573 |       0.229 |       0.15  |              0.009 |
| 2-3          |  376 |   0.13  |         0.41  |       0.186 |       0.061 |              0.01  |
| 4-7          |  284 |   0.185 |         0.401 |       0.169 |       0.109 |              0.009 |
| 8-30         |  489 |   0.036 |         0.211 |       0.198 |       0.2   |              0.001 |
| >30          |  150 |  -0     |         0.26  |       0.26  |       0.013 |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.084 |         0.407 |       0.222 |       0.141 |              0.007 |
| more          |  394 |   0.206 |         0.51  |       0.18  |       0.14  |              0.013 |
| same          | 2113 |   0.171 |         0.437 |       0.218 |       0.133 |              0.007 |

## Worst series
| series_id                                                       |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |  -0.966 |         0.093 |       0.027 |       0.173 |             -0.004 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |  -0.001 |         0.174 |       0.174 |       0.188 |              0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |   0.006 |         0.527 |       0.365 |       0.095 |              0.067 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   0.027 |         0.29  |       0.188 |       0.087 |              0.002 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median   |  74 |   0.031 |         0.392 |       0.351 |       0.122 |              0.025 |
| fastgpu_daily.neocloud_spot.H200.spot.median                    |  69 |   0.046 |         0.348 |       0.174 |       0.087 |              0.005 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median     |  69 |   0.054 |         0.667 |       0.232 |       0.188 |             -0.01  |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median   |  74 |   0.055 |         0.27  |       0.23  |       0.041 |              0.014 |

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
