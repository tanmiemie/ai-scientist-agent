# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1506; truth above q50 in 45% of cells (50% if unbiased); above q90 29% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.201 |         0.216 |       0.055 |       0.078 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     |  180 |  -0.043 |         0.233 |       0.139 |       0.3   |             -0.015 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.156 |         0.49  |       0.301 |       0.135 |              0.003 |
| fastgpu_daily|neocloud_spot        |  630 |   0.227 |         0.421 |       0.302 |       0.095 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.17  |         0.247 |       0.124 |       0.034 |              0.006 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.133 |         0.581 |       0.388 |       0.066 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.105 |         0.343 |       0.209 |       0.082 |              0.003 |
|              3 | 1118 |   0.162 |         0.462 |       0.271 |       0.105 |              0.007 |
|              7 | 1105 |   0.154 |         0.557 |       0.382 |       0.129 |              0.014 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.178 |         0.601 |       0.365 |       0.115 |              0.009 |
| 2-3          |  408 |   0.091 |         0.368 |       0.213 |       0.051 |              0.008 |
| 4-7          |  407 |   0.164 |         0.373 |       0.201 |       0.101 |              0.009 |
| 8-30         |  613 |   0.044 |         0.22  |       0.199 |       0.144 |              0.002 |
| >30          |  171 |   0     |         0.193 |       0.193 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.096 |         0.423 |       0.298 |       0.101 |              0.007 |
| more          |  583 |   0.188 |         0.535 |       0.278 |       0.091 |              0.011 |
| same          | 2590 |   0.139 |         0.438 |       0.288 |       0.108 |              0.007 |

## Worst series
| series_id                                                     |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median              |  96 |  -1.02  |         0     |       0     |       0.042 |             -0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median |  89 |  -0.06  |         0.461 |       0.404 |       0     |              0.057 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median          |  90 |  -0.047 |         0.156 |       0.122 |       0.4   |             -0.036 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median |  89 |   0.015 |         0.461 |       0.236 |       0.146 |              0.014 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                 |  90 |   0.017 |         0.311 |       0.156 |       0.2   |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median   |  90 |   0.019 |         0.211 |       0.189 |       0.089 |              0.004 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median      |  89 |   0.026 |         0.371 |       0.27  |       0.022 |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median   |  90 |   0.035 |         0.689 |       0.478 |       0.178 |             -0.011 |

## Each base model alone: skill by group
| group                              |   log_empirical_window |
|:-----------------------------------|-----------------------:|
| afhubbard|hyperscaler_spot         |                  0.201 |
| fastgpu_daily|hyperscaler_spot     |                 -0.043 |
| fastgpu_daily|neocloud_rate_card   |                  0.156 |
| fastgpu_daily|neocloud_spot        |                  0.227 |
| gpurentalprices|marketplace_ask    |                  0.17  |
| gpurentalprices|neocloud_rate_card |                  0.133 |

## Mean ensemble weight by group
| group                              |   log_empirical_window |
|:-----------------------------------|-----------------------:|
| afhubbard|hyperscaler_spot         |                      1 |
| fastgpu_daily|hyperscaler_spot     |                      1 |
| fastgpu_daily|neocloud_rate_card   |                      1 |
| fastgpu_daily|neocloud_spot        |                      1 |
| gpurentalprices|marketplace_ask    |                      1 |
| gpurentalprices|neocloud_rate_card |                      1 |

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
