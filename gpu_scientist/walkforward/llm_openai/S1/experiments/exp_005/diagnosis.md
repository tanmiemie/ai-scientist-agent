# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.2158; truth above q50 in 49% of cells (50% if unbiased); above q90 17% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.018 |         0.495 |       0.094 |       0.109 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.072 |         0.298 |       0.202 |       0.25  |              0.006 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.219 |         0.556 |       0.162 |       0.071 |              0.005 |
| fastgpu_daily|neocloud_spot        | 294 |  -0.006 |         0.384 |       0.122 |       0.116 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.224 |         0.25  |       0.083 |       0.167 |             -0.026 |
| gpurentalprices|neocloud_rate_card | 576 |   0.277 |         0.547 |       0.219 |       0.076 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.069 |         0.357 |       0.161 |       0.094 |              0.001 |
|              3 | 552 |   0.177 |         0.495 |       0.125 |       0.136 |              0.005 |
|              7 | 552 |   0.249 |         0.629 |       0.214 |       0.062 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.283 |         0.629 |       0.175 |       0.092 |              0.011 |
| 2-3          | 192 |   0.164 |         0.583 |       0.271 |       0.083 |              0.012 |
| 4-7          | 150 |   0.271 |         0.527 |       0.2   |       0.147 |              0.011 |
| 8-30         | 426 |  -0.022 |         0.296 |       0.113 |       0.124 |              0.002 |
| >30          | 123 |   0.021 |         0.154 |       0.098 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.773 |         0.056 |       0     |       0.111 |             -0.005 |
| more          |   75 |   0.266 |         0.6   |       0.08  |       0.08  |              0.018 |
| same          | 1563 |   0.217 |         0.493 |       0.173 |       0.098 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  42 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  48 |  -36.416 |         0.042 |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  48 |   -4.588 |         0.938 |       0.083 |       0.062 |             -0.001 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  42 |   -2.752 |         0.071 |       0     |       0.048 |              0.001 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  42 |   -1.764 |         0     |       0     |       0.619 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  42 |   -0.584 |         0.19  |       0     |       0.024 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  48 |   -0.33  |         0.104 |       0.021 |       0.354 |             -0.005 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  42 |   -0.219 |         0.024 |       0     |       0.095 |             -0.003 |

## Each base model alone: skill by group
| group                              |   drift |   last_value |   leader |
|:-----------------------------------|--------:|-------------:|---------:|
| afhubbard|hyperscaler_spot         |   0.186 |           -0 |    0.17  |
| fastgpu_daily|hyperscaler_spot     |  -0     |           -0 |    0.146 |
| fastgpu_daily|neocloud_rate_card   |  -0     |           -0 |    0.118 |
| fastgpu_daily|neocloud_spot        |  -0     |           -0 |    0.066 |
| gpurentalprices|marketplace_ask    |   0.196 |           -0 |    0.208 |
| gpurentalprices|neocloud_rate_card |   0.056 |           -0 |    0.142 |

## Mean ensemble weight by group
| group                              |   drift |   last_value |   leader |
|:-----------------------------------|--------:|-------------:|---------:|
| afhubbard|hyperscaler_spot         |    0.33 |         0.33 |     0.33 |
| fastgpu_daily|hyperscaler_spot     |    0.33 |         0.33 |     0.33 |
| fastgpu_daily|neocloud_rate_card   |    0.33 |         0.33 |     0.33 |
| fastgpu_daily|neocloud_spot        |    0.33 |         0.33 |     0.33 |
| gpurentalprices|marketplace_ask    |    0.33 |         0.33 |     0.33 |
| gpurentalprices|neocloud_rate_card |    0.33 |         0.33 |     0.33 |

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
