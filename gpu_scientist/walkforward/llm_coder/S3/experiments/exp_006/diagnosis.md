# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1508; truth above q50 in 46% of cells (50% if unbiased); above q90 27% and below q10 11% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.169 |         0.211 |       0.036 |       0.122 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     |  180 |  -0.033 |         0.233 |       0.122 |       0.294 |             -0.015 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.157 |         0.49  |       0.282 |       0.133 |              0.003 |
| fastgpu_daily|neocloud_spot        |  630 |   0.233 |         0.421 |       0.27  |       0.095 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.161 |         0.292 |       0.056 |       0.022 |              0.009 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.134 |         0.59  |       0.383 |       0.064 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.104 |         0.343 |       0.188 |       0.08  |              0.003 |
|              3 | 1118 |   0.159 |         0.466 |       0.263 |       0.106 |              0.007 |
|              7 | 1105 |   0.156 |         0.565 |       0.357 |       0.139 |              0.015 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.176 |         0.602 |       0.34  |       0.111 |              0.009 |
| 2-3          |  408 |   0.097 |         0.368 |       0.194 |       0.064 |              0.008 |
| 4-7          |  407 |   0.175 |         0.388 |       0.179 |       0.118 |              0.01  |
| 8-30         |  613 |   0.041 |         0.227 |       0.197 |       0.155 |              0.002 |
| >30          |  171 |   0     |         0.193 |       0.193 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.087 |         0.44  |       0.286 |       0.101 |              0.009 |
| more          |  583 |   0.193 |         0.537 |       0.269 |       0.087 |              0.012 |
| same          | 2590 |   0.138 |         0.441 |       0.268 |       0.114 |              0.007 |

## Worst series
| series_id                                                     |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median              |  96 |  -1.169 |         0     |       0     |       0.115 |             -0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median |  89 |  -0.052 |         0.461 |       0.404 |       0     |              0.057 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median          |  90 |  -0.037 |         0.156 |       0.089 |       0.4   |             -0.036 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                 |  90 |   0.019 |         0.311 |       0.156 |       0.189 |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median   |  90 |   0.019 |         0.211 |       0.189 |       0.089 |              0.004 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median      |  89 |   0.026 |         0.371 |       0.337 |       0.022 |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median   |  90 |   0.038 |         0.689 |       0.456 |       0.178 |             -0.011 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median |  89 |   0.041 |         0.461 |       0.225 |       0.135 |              0.013 |

## Each base model alone: skill by group
| group                              |   log_empirical_adjvol_window |
|:-----------------------------------|------------------------------:|
| afhubbard|hyperscaler_spot         |                         0.169 |
| fastgpu_daily|hyperscaler_spot     |                        -0.033 |
| fastgpu_daily|neocloud_rate_card   |                         0.157 |
| fastgpu_daily|neocloud_spot        |                         0.233 |
| gpurentalprices|marketplace_ask    |                         0.161 |
| gpurentalprices|neocloud_rate_card |                         0.134 |

## Mean ensemble weight by group
| group                              |   log_empirical_adjvol_window |
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
