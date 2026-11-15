# Diagnosis (dev origins only)

Cells: 3341. Overall skill -1.9528; truth above q50 in 47% of cells (50% if unbiased); above q90 32% and below q10 13% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.177 |         0.211 |       0.044 |       0.133 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     |  180 |  -0.043 |         0.233 |       0.139 |       0.3   |             -0.015 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.084 |         0.519 |       0.345 |       0.138 |              0.019 |
| fastgpu_daily|neocloud_spot        |  630 | -13.833 |         0.508 |       0.398 |       0.01  |              0.185 |
| gpurentalprices|marketplace_ask    |   89 |   0.186 |         0.292 |       0.09  |       0.022 |              0.009 |
| gpurentalprices|neocloud_rate_card | 1068 |  -2.477 |         0.554 |       0.404 |       0.165 |             -0.01  |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |  -5.789 |         0.369 |       0.25  |       0.102 |              0.031 |
|              3 | 1118 |  -2.235 |         0.474 |       0.318 |       0.123 |              0.035 |
|              7 | 1105 |  -1.007 |         0.572 |       0.398 |       0.158 |              0.044 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |  -1.37  |         0.607 |       0.4   |       0.141 |              0.046 |
| 2-3          |  408 |  -0.815 |         0.387 |       0.235 |       0.088 |              0.013 |
| 4-7          |  407 |  -1.008 |         0.376 |       0.214 |       0.162 |              0.002 |
| 8-30         |  613 |  -6.95  |         0.302 |       0.281 |       0.083 |              0.071 |
| >30          |  171 | -11.144 |         0.129 |       0.129 |       0.158 |             -0.045 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |  -6.196 |         0.446 |       0.304 |       0.101 |              0.241 |
| more          |  583 |  -0.911 |         0.532 |       0.317 |       0.153 |              0.004 |
| same          | 2590 |  -2.04  |         0.459 |       0.324 |       0.124 |              0.03  |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  90 | -70.361 |         1     |       1     |       0     |              1.223 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    |  89 | -22.168 |         0.64  |       0.64  |       0.36  |             -0.031 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median |  89 | -14.313 |         0     |       0     |       1     |             -0.288 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      |  90 |  -4.774 |         0.8   |       0.8   |       0.178 |              0.162 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  96 |  -1.139 |         0     |       0     |       0.115 |             -0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  89 |  -0.053 |         0.461 |       0.404 |       0     |              0.057 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  90 |  -0.047 |         0.156 |       0.122 |       0.4   |             -0.036 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                    |  90 |   0.017 |         0.311 |       0.156 |       0.2   |              0.006 |

## Each base model alone: skill by group
| group                              |   simple_leader |
|:-----------------------------------|----------------:|
| afhubbard|hyperscaler_spot         |           0.177 |
| fastgpu_daily|hyperscaler_spot     |          -0.043 |
| fastgpu_daily|neocloud_rate_card   |           0.084 |
| fastgpu_daily|neocloud_spot        |         -13.833 |
| gpurentalprices|marketplace_ask    |           0.186 |
| gpurentalprices|neocloud_rate_card |          -2.477 |

## Mean ensemble weight by group
| group                              |   simple_leader |
|:-----------------------------------|----------------:|
| afhubbard|hyperscaler_spot         |               1 |
| fastgpu_daily|hyperscaler_spot     |               1 |
| fastgpu_daily|neocloud_rate_card   |               1 |
| fastgpu_daily|neocloud_spot        |               1 |
| gpurentalprices|marketplace_ask    |               1 |
| gpurentalprices|neocloud_rate_card |               1 |

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
