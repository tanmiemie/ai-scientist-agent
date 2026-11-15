# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1678; truth above q50 in 45% of cells (50% if unbiased); above q90 13% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.177 |         0.217 |       0.06  |       0.08  |             -0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.082 |         0.37  |       0.159 |       0.196 |              0.009 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.175 |         0.476 |       0.136 |       0.138 |              0.002 |
| fastgpu_daily|neocloud_spot        | 483 |   0.222 |         0.385 |       0.145 |       0.149 |              0.01  |
| gpurentalprices|marketplace_ask    |  74 |  -0.005 |         0.378 |       0.014 |       0.027 |             -0.012 |
| gpurentalprices|neocloud_rate_card | 888 |   0.175 |         0.565 |       0.142 |       0.063 |              0.019 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.073 |         0.315 |       0.116 |       0.098 |              0.002 |
|              3 | 885 |   0.061 |         0.463 |       0.118 |       0.108 |              0.007 |
|              7 | 872 |   0.24  |         0.578 |       0.153 |       0.118 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.199 |         0.583 |       0.128 |       0.092 |              0.011 |
| 2-3          |  376 |   0.1   |         0.41  |       0.12  |       0.098 |              0.01  |
| 4-7          |  284 |   0.178 |         0.437 |       0.151 |       0.134 |              0.01  |
| 8-30         |  489 |   0.074 |         0.202 |       0.141 |       0.178 |              0.001 |
| >30          |  150 |   0.038 |         0.22  |       0.073 |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.04  |         0.481 |       0.074 |       0.178 |              0.009 |
| more          |  394 |   0.138 |         0.513 |       0.069 |       0.079 |              0.012 |
| same          | 2113 |   0.189 |         0.438 |       0.143 |       0.109 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -0.898 |         0     |       0     |       0.133 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -0.553 |         0.261 |       0.014 |       0.072 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.484 |         0.23  |       0.014 |       0.203 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  69 |   -0.152 |         0.507 |       0.145 |       0.13  |              0.003 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |   -0.138 |         0.478 |       0.174 |       0.174 |              0.023 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.126 |         0.662 |       0.162 |       0.081 |              0.006 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   -0.124 |         0.284 |       0.014 |       0     |              0.006 |

## Each base model alone: skill by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |         0.193 |
| fastgpu_daily|hyperscaler_spot     |         0.012 |
| fastgpu_daily|neocloud_rate_card   |         0.128 |
| fastgpu_daily|neocloud_spot        |         0.165 |
| gpurentalprices|marketplace_ask    |        -0.012 |
| gpurentalprices|neocloud_rate_card |         0.114 |

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
