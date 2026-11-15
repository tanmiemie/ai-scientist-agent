# Diagnosis (dev origins only)

Cells: 2322. Overall skill 0.1254; truth above q50 in 46% of cells (50% if unbiased); above q90 15% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 264 |   0.116 |         0.239 |       0.068 |       0.068 |              0.001 |
| fastgpu_daily|hyperscaler_spot     | 120 |   0.055 |         0.283 |       0.183 |       0.2   |              0.004 |
| fastgpu_daily|neocloud_rate_card   | 660 |   0.145 |         0.539 |       0.168 |       0.132 |              0.004 |
| fastgpu_daily|neocloud_spot        | 420 |   0.156 |         0.371 |       0.16  |       0.143 |              0.011 |
| gpurentalprices|marketplace_ask    |  66 |   0.065 |         0.258 |       0.015 |       0.03  |             -0.023 |
| gpurentalprices|neocloud_rate_card | 792 |   0.109 |         0.562 |       0.152 |       0.057 |              0.021 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 774 |   0.037 |         0.305 |       0.132 |       0.103 |              0.002 |
|              3 | 774 |   0.069 |         0.473 |       0.134 |       0.103 |              0.008 |
|              7 | 774 |   0.174 |         0.606 |       0.172 |       0.098 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1185 |   0.149 |         0.591 |       0.151 |       0.089 |              0.012 |
| 2-3          |  294 |   0.098 |         0.469 |       0.16  |       0.078 |              0.012 |
| 4-7          |  216 |   0.186 |         0.468 |       0.208 |       0.111 |              0.011 |
| 8-30         |  483 |  -0.007 |         0.205 |       0.13  |       0.172 |              0.001 |
| >30          |  144 |  -0.102 |         0.229 |       0.035 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   90 |  -0.036 |         0.4   |       0.067 |       0.222 |              0.009 |
| more          |  273 |   0.114 |         0.59  |       0.084 |       0.066 |              0.018 |
| same          | 1959 |   0.142 |         0.446 |       0.158 |       0.101 |              0.009 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  60 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  66 |   -1.262 |         0.197 |       0     |       0     |              0.004 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  66 |   -1.027 |         0.182 |       0.015 |       0.242 |             -0.004 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  66 |   -0.943 |         0     |       0     |       0.061 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  60 |   -0.862 |         0.283 |       0.017 |       0.083 |              0.003 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  60 |   -0.596 |         0.783 |       0.2   |       0.033 |              0.005 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  66 |   -0.385 |         0.515 |       0.182 |       0     |              0.009 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  66 |   -0.351 |         0.742 |       0.197 |       0.03  |              0.009 |

## Each base model alone: skill by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |   0.162 |
| fastgpu_daily|hyperscaler_spot     |  -0.026 |
| fastgpu_daily|neocloud_rate_card   |   0     |
| fastgpu_daily|neocloud_spot        |  -0     |
| gpurentalprices|marketplace_ask    |   0.101 |
| gpurentalprices|neocloud_rate_card |   0.063 |

## Mean ensemble weight by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |       1 |
| fastgpu_daily|hyperscaler_spot     |       1 |
| fastgpu_daily|neocloud_rate_card   |       1 |
| fastgpu_daily|neocloud_spot        |       1 |
| gpurentalprices|marketplace_ask    |       1 |
| gpurentalprices|neocloud_rate_card |       1 |

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
