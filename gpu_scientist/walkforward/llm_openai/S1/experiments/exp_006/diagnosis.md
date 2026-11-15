# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.2414; truth above q50 in 45% of cells (50% if unbiased); above q90 15% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.079 |         0.312 |       0.047 |       0.125 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.108 |         0.298 |       0.25  |       0.286 |              0.006 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.243 |         0.53  |       0.154 |       0.102 |              0.005 |
| fastgpu_daily|neocloud_spot        | 294 |   0.08  |         0.32  |       0.095 |       0.102 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.151 |         0.229 |       0.021 |       0.042 |             -0.031 |
| gpurentalprices|neocloud_rate_card | 576 |   0.31  |         0.545 |       0.217 |       0.085 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.088 |         0.297 |       0.134 |       0.112 |              0.001 |
|              3 | 552 |   0.176 |         0.457 |       0.125 |       0.149 |              0.005 |
|              7 | 552 |   0.287 |         0.603 |       0.203 |       0.058 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.301 |         0.605 |       0.166 |       0.094 |              0.011 |
| 2-3          | 192 |   0.192 |         0.521 |       0.245 |       0.104 |              0.012 |
| 4-7          | 150 |   0.272 |         0.473 |       0.193 |       0.18  |              0.011 |
| 8-30         | 426 |   0.052 |         0.225 |       0.087 |       0.131 |              0.002 |
| >30          | 123 |   0.053 |         0.154 |       0.122 |       0.008 |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.984 |         0.056 |       0     |       0.111 |             -0.006 |
| more          |   75 |   0.298 |         0.52  |       0.093 |       0.093 |              0.018 |
| same          | 1563 |   0.244 |         0.454 |       0.159 |       0.107 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  42 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  48 |  -33.253 |         0.042 |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  48 |   -3.746 |         0.167 |       0.021 |       0.146 |             -0.001 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  42 |   -2.411 |         0.071 |       0     |       0.048 |              0.001 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  42 |   -1.489 |         0     |       0     |       0.619 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  42 |   -0.421 |         0.286 |       0     |       0.143 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  48 |   -0.241 |         0.104 |       0.021 |       0.312 |             -0.004 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  42 |   -0.15  |         0.024 |       0     |       0.095 |             -0.003 |

## Each base model alone: skill by group
| group                              |   drift |   last_value |
|:-----------------------------------|--------:|-------------:|
| afhubbard|hyperscaler_spot         |   0.186 |           -0 |
| fastgpu_daily|hyperscaler_spot     |  -0     |           -0 |
| fastgpu_daily|neocloud_rate_card   |  -0     |           -0 |
| fastgpu_daily|neocloud_spot        |  -0     |           -0 |
| gpurentalprices|marketplace_ask    |   0.196 |           -0 |
| gpurentalprices|neocloud_rate_card |   0.056 |           -0 |

## Mean ensemble weight by group
| group                              |   drift |   last_value |
|:-----------------------------------|--------:|-------------:|
| afhubbard|hyperscaler_spot         |    0.77 |         0.23 |
| fastgpu_daily|hyperscaler_spot     |    0.77 |         0.23 |
| fastgpu_daily|neocloud_rate_card   |    0.73 |         0.27 |
| fastgpu_daily|neocloud_spot        |    0.5  |         0.5  |
| gpurentalprices|marketplace_ask    |    1    |         0    |
| gpurentalprices|neocloud_rate_card |    0.71 |         0.29 |

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
