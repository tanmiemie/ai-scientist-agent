# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1534; truth above q50 in 45% of cells (50% if unbiased); above q90 27% and below q10 11% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.169 |         0.229 |       0.06  |       0.109 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     |  180 |  -0.04  |         0.233 |       0.139 |       0.3   |             -0.015 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.157 |         0.489 |       0.298 |       0.135 |              0.002 |
| fastgpu_daily|neocloud_spot        |  630 |   0.229 |         0.419 |       0.297 |       0.095 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.169 |         0.247 |       0.112 |       0.045 |              0.001 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.143 |         0.577 |       0.341 |       0.06  |              0.017 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.111 |         0.35  |       0.191 |       0.08  |              0.003 |
|              3 | 1118 |   0.156 |         0.459 |       0.254 |       0.106 |              0.006 |
|              7 | 1105 |   0.161 |         0.554 |       0.368 |       0.136 |              0.013 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.186 |         0.6   |       0.336 |       0.118 |              0.008 |
| 2-3          |  408 |   0.093 |         0.373 |       0.208 |       0.051 |              0.008 |
| 4-7          |  407 |   0.145 |         0.373 |       0.199 |       0.108 |              0.009 |
| 8-30         |  613 |   0.044 |         0.219 |       0.196 |       0.144 |              0.002 |
| >30          |  171 |   0     |         0.193 |       0.193 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.119 |         0.423 |       0.298 |       0.101 |              0.008 |
| more          |  583 |   0.184 |         0.533 |       0.274 |       0.091 |              0.011 |
| same          | 2590 |   0.143 |         0.438 |       0.268 |       0.111 |              0.006 |

## Worst series
| series_id                                                     |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median              |  96 |  -0.654 |         0     |       0     |       0.042 |             -0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median |  89 |  -0.087 |         0.461 |       0.348 |       0     |              0.055 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median          |  90 |  -0.044 |         0.156 |       0.122 |       0.4   |             -0.036 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median |  89 |  -0.024 |         0.517 |       0.202 |       0.124 |              0.015 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                 |  90 |   0.016 |         0.311 |       0.156 |       0.2   |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median   |  90 |   0.021 |         0.211 |       0.189 |       0.089 |              0.004 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median      |  89 |   0.023 |         0.371 |       0.258 |       0.022 |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median   |  90 |   0.036 |         0.689 |       0.478 |       0.178 |             -0.011 |

## Each base model alone: skill by group
| group                              |   log_empirical_window |
|:-----------------------------------|-----------------------:|
| afhubbard|hyperscaler_spot         |                  0.169 |
| fastgpu_daily|hyperscaler_spot     |                 -0.04  |
| fastgpu_daily|neocloud_rate_card   |                  0.157 |
| fastgpu_daily|neocloud_spot        |                  0.229 |
| gpurentalprices|marketplace_ask    |                  0.169 |
| gpurentalprices|neocloud_rate_card |                  0.143 |

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
