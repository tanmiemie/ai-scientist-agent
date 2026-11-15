# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1734; truth above q50 in 45% of cells (50% if unbiased); above q90 21% and below q10 13% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.149 |         0.247 |       0.04  |       0.1   |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.106 |         0.225 |       0.159 |       0.239 |             -0.002 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.177 |         0.516 |       0.207 |       0.167 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.222 |         0.385 |       0.211 |       0.174 |              0.01  |
| gpurentalprices|marketplace_ask    |  74 |   0.078 |         0.203 |       0.027 |       0.027 |             -0.018 |
| gpurentalprices|neocloud_rate_card | 888 |   0.177 |         0.547 |       0.286 |       0.089 |              0.018 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.077 |         0.325 |       0.131 |       0.142 |              0.001 |
|              3 | 885 |   0.172 |         0.444 |       0.189 |       0.133 |              0.006 |
|              7 | 872 |   0.193 |         0.577 |       0.305 |       0.127 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.207 |         0.572 |       0.22  |       0.152 |              0.009 |
| 2-3          |  376 |   0.128 |         0.42  |       0.184 |       0.061 |              0.01  |
| 4-7          |  284 |   0.183 |         0.412 |       0.173 |       0.106 |              0.009 |
| 8-30         |  489 |   0.036 |         0.215 |       0.204 |       0.194 |              0.001 |
| >30          |  150 |  -0     |         0.24  |       0.24  |       0.02  |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.081 |         0.407 |       0.222 |       0.141 |              0.007 |
| more          |  394 |   0.201 |         0.523 |       0.173 |       0.142 |              0.013 |
| same          | 2113 |   0.172 |         0.437 |       0.213 |       0.133 |              0.007 |

## Worst series
| series_id                                                       |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |  -0.942 |         0.08  |       0.067 |       0.16  |             -0.004 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |  -0.018 |         0.319 |       0.203 |       0.145 |              0.002 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |  -0.005 |         0.174 |       0.174 |       0.188 |              0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |   0.006 |         0.527 |       0.378 |       0.095 |              0.067 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median   |  74 |   0.022 |         0.351 |       0.311 |       0.135 |              0.025 |
| fastgpu_daily.neocloud_spot.H200.spot.median                    |  69 |   0.03  |         0.348 |       0.174 |       0.058 |              0.005 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median   |  74 |   0.052 |         0.27  |       0.257 |       0.041 |              0.014 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median     |  69 |   0.055 |         0.667 |       0.217 |       0.188 |             -0.01  |

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
