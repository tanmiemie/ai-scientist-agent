# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.1902; truth above q50 in 45% of cells (50% if unbiased); above q90 16% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.037 |         0.281 |       0.109 |       0.026 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.108 |         0.321 |       0.238 |       0.19  |              0.006 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.175 |         0.526 |       0.121 |       0.1   |              0.005 |
| fastgpu_daily|neocloud_spot        | 294 |   0.151 |         0.327 |       0.221 |       0.19  |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.186 |         0.229 |       0.021 |       0.021 |             -0.029 |
| gpurentalprices|neocloud_rate_card | 576 |   0.232 |         0.549 |       0.167 |       0.087 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.018 |         0.299 |       0.147 |       0.132 |              0.001 |
|              3 | 552 |   0.162 |         0.446 |       0.129 |       0.111 |              0.005 |
|              7 | 552 |   0.221 |         0.609 |       0.194 |       0.072 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.23  |         0.607 |       0.165 |       0.102 |              0.011 |
| 2-3          | 192 |   0.148 |         0.521 |       0.177 |       0.073 |              0.012 |
| 4-7          | 150 |   0.27  |         0.447 |       0.187 |       0.1   |              0.011 |
| 8-30         | 426 |   0.033 |         0.218 |       0.153 |       0.157 |              0.002 |
| >30          | 123 |  -0.032 |         0.187 |       0.049 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -1.05  |         0.111 |       0.056 |       0.111 |             -0.006 |
| more          |   75 |   0.328 |         0.573 |       0.12  |       0.2   |              0.018 |
| same          | 1563 |   0.183 |         0.449 |       0.159 |       0.1   |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  42 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  48 |  -46.077 |         0.042 |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  48 |   -3.769 |         0.083 |       0     |       0     |             -0.001 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  42 |   -3.576 |         0.071 |       0     |       0.048 |              0.001 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  42 |   -0.939 |         0.238 |       0.048 |       0.095 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  48 |   -0.579 |         0.104 |       0.042 |       0.312 |             -0.005 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  42 |   -0.374 |         0.024 |       0     |       0.095 |             -0.003 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  42 |   -0.364 |         0     |       0     |       1     |             -0.002 |

## Each base model alone: skill by group
| group                              |   drift |   vol_tail |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |   0.186 |      0.2   |
| fastgpu_daily|hyperscaler_spot     |  -0     |      0.143 |
| fastgpu_daily|neocloud_rate_card   |  -0     |      0.107 |
| fastgpu_daily|neocloud_spot        |  -0     |      0.06  |
| gpurentalprices|marketplace_ask    |   0.196 |      0.157 |
| gpurentalprices|neocloud_rate_card |   0.056 |      0.158 |

## Mean ensemble weight by group
| group                              |   drift |   vol_tail |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |    0.54 |       0.46 |
| fastgpu_daily|hyperscaler_spot     |    0.52 |       0.48 |
| fastgpu_daily|neocloud_rate_card   |    0.03 |       0.97 |
| fastgpu_daily|neocloud_spot        |    0.46 |       0.54 |
| gpurentalprices|marketplace_ask    |    0.67 |       0.33 |
| gpurentalprices|neocloud_rate_card |    0.09 |       0.91 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                            | leader                                                          |   lag_days |   corr |
|:------------------------------------------------------------------|:----------------------------------------------------------------|-----------:|-------:|
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_list.H100_SXM_80GB.on_demand.median |          2 | -0.952 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.H100_SXM_80GB.spot.median      |          2 | -0.952 |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median      |          1 |  0.87  |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.neocloud_rate_card.B300.on_demand.median              |          3 |  0.535 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median          | afhubbard.hyperscaler_spot.B200.spot.median                     |          5 | -0.511 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median  |          1 | -0.505 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  | afhubbard.neocloud_rate_card.RTX_PRO_6000.on_demand.median      |          5 |  0.427 |
| gpurentalprices.neocloud_rate_card.A100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.A100_SXM_80GB.spot.median      |          5 |  0.379 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_spot.H200.spot.median               |          5 |  0.339 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median            | afhubbard.hyperscaler_spot.L4.spot.median                       |          3 |  0.314 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median     | gpurentalprices.marketplace_ask.H100_80GB.spot.median           |          1 |  0.31  |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_spot.H100_80GB.spot.median             |          3 | -0.306 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median          |          5 |  0.306 |
