# Diagnosis (dev origins only)

Cells: 2322. Overall skill 0.1905; truth above q50 in 46% of cells (50% if unbiased); above q90 15% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 264 |   0.025 |         0.239 |       0.095 |       0.053 |              0.001 |
| fastgpu_daily|hyperscaler_spot     | 120 |   0.156 |         0.275 |       0.167 |       0.175 |              0.004 |
| fastgpu_daily|neocloud_rate_card   | 660 |   0.211 |         0.539 |       0.15  |       0.126 |              0.004 |
| fastgpu_daily|neocloud_spot        | 420 |   0.18  |         0.371 |       0.164 |       0.143 |              0.011 |
| gpurentalprices|marketplace_ask    |  66 |   0.114 |         0.227 |       0.03  |       0.03  |             -0.019 |
| gpurentalprices|neocloud_rate_card | 792 |   0.197 |         0.548 |       0.164 |       0.057 |              0.021 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 774 |   0.036 |         0.305 |       0.123 |       0.098 |              0.003 |
|              3 | 774 |   0.122 |         0.468 |       0.136 |       0.098 |              0.008 |
|              7 | 774 |   0.259 |         0.593 |       0.187 |       0.094 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1185 |   0.212 |         0.586 |       0.151 |       0.083 |              0.012 |
| 2-3          |  294 |   0.155 |         0.459 |       0.143 |       0.071 |              0.012 |
| 4-7          |  216 |   0.245 |         0.444 |       0.176 |       0.106 |              0.011 |
| 8-30         |  483 |   0.075 |         0.205 |       0.151 |       0.172 |              0.001 |
| >30          |  144 |   0.051 |         0.229 |       0.09  |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   90 |   0.028 |         0.367 |       0.122 |       0.178 |              0.009 |
| more          |  273 |   0.177 |         0.568 |       0.099 |       0.066 |              0.019 |
| same          | 1959 |   0.207 |         0.444 |       0.157 |       0.097 |              0.009 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  60 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  66 |   -1.524 |         0     |       0     |       0.061 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  66 |   -0.379 |         0.197 |       0     |       0     |              0.004 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  66 |   -0.357 |         0.106 |       0.03  |       0.242 |             -0.004 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  60 |   -0.135 |         0.1   |       0     |       0.9   |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  60 |   -0.098 |         0.283 |       0.033 |       0.083 |              0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  66 |   -0.055 |         0.742 |       0.197 |       0.03  |              0.009 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  66 |   -0.019 |         0.515 |       0.152 |       0     |              0.009 |

## Each base model alone: skill by group
| group                              |   trend_tail |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |        0.137 |
| fastgpu_daily|hyperscaler_spot     |        0.137 |
| fastgpu_daily|neocloud_rate_card   |        0.156 |
| fastgpu_daily|neocloud_spot        |        0.189 |
| gpurentalprices|marketplace_ask    |        0.115 |
| gpurentalprices|neocloud_rate_card |        0.132 |

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
