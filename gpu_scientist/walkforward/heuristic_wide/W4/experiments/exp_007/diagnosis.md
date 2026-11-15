# Diagnosis (dev origins only)

Cells: 2322. Overall skill 0.1926; truth above q50 in 46% of cells (50% if unbiased); above q90 19% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 264 |   0.181 |         0.239 |       0.08  |       0.061 |              0.001 |
| fastgpu_daily|hyperscaler_spot     | 120 |   0.055 |         0.283 |       0.242 |       0.25  |              0.004 |
| fastgpu_daily|neocloud_rate_card   | 660 |   0.154 |         0.539 |       0.215 |       0.136 |              0.004 |
| fastgpu_daily|neocloud_spot        | 420 |   0.211 |         0.371 |       0.217 |       0.143 |              0.011 |
| gpurentalprices|marketplace_ask    |  66 |   0.089 |         0.258 |       0.03  |       0.03  |             -0.023 |
| gpurentalprices|neocloud_rate_card | 792 |   0.255 |         0.562 |       0.196 |       0.057 |              0.021 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 774 |   0.077 |         0.305 |       0.141 |       0.105 |              0.002 |
|              3 | 774 |   0.134 |         0.473 |       0.168 |       0.106 |              0.008 |
|              7 | 774 |   0.248 |         0.606 |       0.26  |       0.103 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1185 |   0.236 |         0.591 |       0.201 |       0.092 |              0.012 |
| 2-3          |  294 |   0.144 |         0.469 |       0.17  |       0.075 |              0.012 |
| 4-7          |  216 |   0.146 |         0.468 |       0.269 |       0.148 |              0.011 |
| 8-30         |  483 |   0.055 |         0.205 |       0.161 |       0.166 |              0.001 |
| >30          |  144 |   0.169 |         0.229 |       0.111 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   90 |  -0.014 |         0.4   |       0.122 |       0.222 |              0.009 |
| more          |  273 |   0.209 |         0.59  |       0.15  |       0.081 |              0.018 |
| same          | 1959 |   0.205 |         0.446 |       0.198 |       0.103 |              0.009 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  60 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  66 |   -0.602 |         0     |       0     |       0.015 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  66 |   -0.169 |         0.197 |       0     |       0     |              0.004 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  66 |   -0.155 |         0.182 |       0.015 |       0.197 |             -0.004 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                    |  60 |   -0.023 |         0.267 |       0.217 |       0.3   |              0.006 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  60 |   -0.012 |         0.033 |       0     |       0.35  |             -0.034 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  60 |    0.007 |         0.1   |       0     |       0.9   |             -0.003 |
| fastgpu_daily.neocloud_rate_card.RTX_6000_Ada.on_demand.median   |  60 |    0.025 |         0.733 |       0.2   |       0.183 |             -0.018 |

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
