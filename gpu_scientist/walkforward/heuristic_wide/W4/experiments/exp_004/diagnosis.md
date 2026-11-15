# Diagnosis (dev origins only)

Cells: 2322. Overall skill 0.1729; truth above q50 in 45% of cells (50% if unbiased); above q90 14% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 264 |   0.167 |         0.227 |       0.064 |       0.08  |              0     |
| fastgpu_daily|hyperscaler_spot     | 120 |   0.037 |         0.4   |       0.183 |       0.192 |              0.014 |
| fastgpu_daily|neocloud_rate_card   | 660 |   0.183 |         0.468 |       0.152 |       0.158 |              0.001 |
| fastgpu_daily|neocloud_spot        | 420 |   0.209 |         0.369 |       0.167 |       0.162 |              0.01  |
| gpurentalprices|marketplace_ask    |  66 |  -0.007 |         0.394 |       0.015 |       0.03  |             -0.018 |
| gpurentalprices|neocloud_rate_card | 792 |   0.186 |         0.558 |       0.157 |       0.058 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 774 |   0.066 |         0.3   |       0.127 |       0.107 |              0.002 |
|              3 | 774 |   0.075 |         0.461 |       0.133 |       0.118 |              0.007 |
|              7 | 774 |   0.246 |         0.583 |       0.172 |       0.116 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1185 |   0.192 |         0.559 |       0.142 |       0.102 |              0.011 |
| 2-3          |  294 |   0.128 |         0.483 |       0.146 |       0.095 |              0.013 |
| 4-7          |  216 |   0.232 |         0.477 |       0.199 |       0.13  |              0.012 |
| 8-30         |  483 |   0.075 |         0.205 |       0.143 |       0.18  |              0.001 |
| >30          |  144 |   0.049 |         0.229 |       0.076 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   90 |  -0.006 |         0.478 |       0.111 |       0.222 |              0.01  |
| more          |  273 |   0.163 |         0.535 |       0.088 |       0.084 |              0.016 |
| same          | 1959 |   0.19  |         0.434 |       0.153 |       0.113 |              0.009 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  60 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  66 |   -0.808 |         0     |       0     |       0.152 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  66 |   -0.504 |         0.197 |       0     |       0     |              0.004 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  66 |   -0.402 |         0.167 |       0.015 |       0.212 |             -0.004 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  60 |   -0.287 |         0.283 |       0.017 |       0.083 |              0.003 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  60 |   -0.175 |         0.517 |       0.167 |       0.15  |              0.002 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  60 |   -0.119 |         0.1   |       0     |       0.9   |             -0.003 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  60 |   -0.112 |         0.5   |       0.2   |       0.2   |              0.026 |

## Each base model alone: skill by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |         0.193 |
| fastgpu_daily|hyperscaler_spot     |         0.01  |
| fastgpu_daily|neocloud_rate_card   |         0.107 |
| fastgpu_daily|neocloud_spot        |         0.141 |
| gpurentalprices|marketplace_ask    |        -0.013 |
| gpurentalprices|neocloud_rate_card |         0.104 |

## Mean ensemble weight by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |             1 |
| fastgpu_daily|hyperscaler_spot     |             1 |
| fastgpu_daily|neocloud_rate_card   |             1 |
| fastgpu_daily|neocloud_spot        |             1 |
| gpurentalprices|marketplace_ask    |             1 |
| gpurentalprices|neocloud_rate_card |             1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                            | leader                                                                  |   lag_days |   corr |
|:------------------------------------------------------------------|:------------------------------------------------------------------------|-----------:|-------:|
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median             |          5 |  0.997 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median                  |          5 |  0.994 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median       |          2 |  0.933 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_list.H100_SXM_80GB.on_demand.median         |          5 |  0.913 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.H100_SXM_80GB.spot.median              |          5 |  0.913 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median     | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median                 |          4 |  0.868 |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median              |          1 |  0.86  |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.neocloud_rate_card.B300.on_demand.median                      |          1 |  0.712 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median     | gpurentalprices_cheapest.aggregator_cheapest.RTX_A6000.on_demand.median |          2 | -0.712 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | gpurentalprices.neocloud_rate_card.B300.serverless.median               |          1 |  0.703 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.hyperscaler_list.B300.on_demand.median                        |          2 | -0.648 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.neocloud_rate_card.H200.serverless.median               |          2 |  0.586 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | afhubbard.neocloud_rate_card.H200.on_demand.median                      |          2 |  0.57  |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_list.H200.on_demand.median                  |          1 | -0.538 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median          |          1 | -0.504 |
