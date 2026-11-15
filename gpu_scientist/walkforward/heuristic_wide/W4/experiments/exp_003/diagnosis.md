# Diagnosis (dev origins only)

Cells: 2322. Overall skill 0.1851; truth above q50 in 43% of cells (50% if unbiased); above q90 14% and below q10 12% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 264 |  -0.046 |         0.235 |       0.068 |       0.049 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 120 |   0.076 |         0.25  |       0.167 |       0.183 |              0.001 |
| fastgpu_daily|neocloud_rate_card   | 660 |   0.222 |         0.494 |       0.139 |       0.152 |              0.002 |
| fastgpu_daily|neocloud_spot        | 420 |   0.138 |         0.355 |       0.16  |       0.207 |              0.009 |
| gpurentalprices|marketplace_ask    |  66 |   0.065 |         0.212 |       0.03  |       0.03  |             -0.028 |
| gpurentalprices|neocloud_rate_card | 792 |   0.196 |         0.525 |       0.163 |       0.057 |              0.019 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 774 |  -0.01  |         0.269 |       0.12  |       0.128 |              0     |
|              3 | 774 |   0.119 |         0.442 |       0.133 |       0.115 |              0.006 |
|              7 | 774 |   0.261 |         0.578 |       0.171 |       0.105 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1185 |   0.2   |         0.535 |       0.134 |       0.127 |              0.008 |
| 2-3          |  294 |   0.16  |         0.459 |       0.146 |       0.051 |              0.012 |
| 4-7          |  216 |   0.255 |         0.444 |       0.167 |       0.106 |              0.011 |
| 8-30         |  483 |   0.075 |         0.205 |       0.155 |       0.166 |              0.001 |
| >30          |  144 |   0.059 |         0.229 |       0.104 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   90 |   0.046 |         0.344 |       0.1   |       0.178 |              0.006 |
| more          |  273 |   0.163 |         0.516 |       0.088 |       0.114 |              0.016 |
| same          | 1959 |   0.202 |         0.421 |       0.151 |       0.113 |              0.007 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  60 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  66 |   -1.688 |         0     |       0     |       0.061 |             -0.005 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  66 |   -0.511 |         0.197 |       0     |       0     |              0.004 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  66 |   -0.42  |         0.106 |       0.015 |       0.136 |             -0.005 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  60 |   -0.14  |         0.283 |       0.033 |       0.083 |              0.002 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  66 |   -0.139 |         0.47  |       0.167 |       0.03  |              0.007 |
| fastgpu_daily.neocloud_spot.H200.spot.median                    |  60 |   -0.132 |         0.333 |       0.133 |       0.1   |              0.004 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  60 |   -0.085 |         0.083 |       0     |       0.867 |             -0.004 |

## Each base model alone: skill by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.052 |
| fastgpu_daily|hyperscaler_spot     |      0.059 |
| fastgpu_daily|neocloud_rate_card   |      0.165 |
| fastgpu_daily|neocloud_spot        |      0.193 |
| gpurentalprices|marketplace_ask    |      0.065 |
| gpurentalprices|neocloud_rate_card |      0.152 |

## Mean ensemble weight by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |          1 |
| fastgpu_daily|hyperscaler_spot     |          1 |
| fastgpu_daily|neocloud_rate_card   |          1 |
| fastgpu_daily|neocloud_spot        |          1 |
| gpurentalprices|marketplace_ask    |          1 |
| gpurentalprices|neocloud_rate_card |          1 |

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
