# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1497; truth above q50 in 46% of cells (50% if unbiased); above q90 26% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.144 |         0.211 |       0.021 |       0.102 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     |  180 |  -0.023 |         0.233 |       0.122 |       0.267 |             -0.015 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.16  |         0.49  |       0.271 |       0.131 |              0.003 |
| fastgpu_daily|neocloud_spot        |  630 |   0.237 |         0.421 |       0.259 |       0.095 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.122 |         0.292 |       0.034 |       0.011 |              0.009 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.136 |         0.59  |       0.37  |       0.062 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.104 |         0.343 |       0.178 |       0.076 |              0.003 |
|              3 | 1118 |   0.159 |         0.466 |       0.252 |       0.105 |              0.007 |
|              7 | 1105 |   0.155 |         0.565 |       0.342 |       0.129 |              0.015 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.176 |         0.602 |       0.324 |       0.108 |              0.009 |
| 2-3          |  408 |   0.092 |         0.368 |       0.184 |       0.054 |              0.008 |
| 4-7          |  407 |   0.173 |         0.388 |       0.165 |       0.101 |              0.01  |
| 8-30         |  613 |   0.036 |         0.227 |       0.194 |       0.15  |              0.002 |
| >30          |  171 |   0     |         0.193 |       0.193 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.077 |         0.44  |       0.28  |       0.095 |              0.009 |
| more          |  583 |   0.192 |         0.537 |       0.25  |       0.086 |              0.012 |
| same          | 2590 |   0.138 |         0.441 |       0.257 |       0.107 |              0.007 |

## Worst series
| series_id                                                     |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median              |  96 |  -1.376 |         0     |       0     |       0.115 |             -0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median |  89 |  -0.067 |         0.461 |       0.404 |       0     |              0.057 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median          |  90 |  -0.025 |         0.156 |       0.089 |       0.389 |             -0.036 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                 |  90 |   0.013 |         0.311 |       0.156 |       0.144 |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median   |  90 |   0.02  |         0.211 |       0.189 |       0.089 |              0.004 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median      |  89 |   0.026 |         0.371 |       0.315 |       0.022 |              0.006 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median |  89 |   0.039 |         0.461 |       0.213 |       0.124 |              0.013 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median   |  90 |   0.042 |         0.689 |       0.456 |       0.178 |             -0.011 |

## Each base model alone: skill by group
| group                              |   log_empirical_scaled_window |
|:-----------------------------------|------------------------------:|
| afhubbard|hyperscaler_spot         |                         0.144 |
| fastgpu_daily|hyperscaler_spot     |                        -0.023 |
| fastgpu_daily|neocloud_rate_card   |                         0.16  |
| fastgpu_daily|neocloud_spot        |                         0.237 |
| gpurentalprices|marketplace_ask    |                         0.122 |
| gpurentalprices|neocloud_rate_card |                         0.136 |

## Mean ensemble weight by group
| group                              |   log_empirical_scaled_window |
|:-----------------------------------|------------------------------:|
| afhubbard|hyperscaler_spot         |                             1 |
| fastgpu_daily|hyperscaler_spot     |                             1 |
| fastgpu_daily|neocloud_rate_card   |                             1 |
| fastgpu_daily|neocloud_spot        |                             1 |
| gpurentalprices|marketplace_ask    |                             1 |
| gpurentalprices|neocloud_rate_card |                             1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                           | leader                                                            |   lag_days |   corr |
|:-----------------------------------------------------------------|:------------------------------------------------------------------|-----------:|-------:|
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      | gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median     |          3 | -0.924 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_rate_card.B200.serverless.median         |          3 | -0.924 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_spot.B200.spot.median                    |          1 |  0.924 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median |          2 |  0.921 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median      |          4 |  0.884 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median           |          4 |  0.865 |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | afhubbard.hyperscaler_list.B300.on_demand.median                  |          1 | -0.85  |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | fastgpu_daily.hyperscaler_list.B300.on_demand.median              |          2 | -0.85  |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median        |          1 |  0.805 |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     | afhubbard.neocloud_spot.L40S.spot.median                          |          1 |  0.797 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  |          1 |  0.778 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median |          3 |  0.762 |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     | afhubbard.neocloud_rate_card.L40S.on_demand.median                |          1 |  0.746 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median       |          5 |  0.71  |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median      |          5 |  0.705 |
