# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.2045; truth above q50 in 44% of cells (50% if unbiased); above q90 16% and below q10 9% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.038 |         0.26  |       0.099 |       0.036 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.16  |         0.298 |       0.202 |       0.155 |              0.006 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.196 |         0.517 |       0.121 |       0.071 |              0.005 |
| fastgpu_daily|neocloud_spot        | 294 |   0.155 |         0.32  |       0.221 |       0.18  |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.2   |         0.229 |       0.021 |       0.042 |             -0.027 |
| gpurentalprices|neocloud_rate_card | 576 |   0.242 |         0.536 |       0.179 |       0.076 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |  -0.02  |         0.275 |       0.132 |       0.096 |              0.001 |
|              3 | 552 |   0.207 |         0.444 |       0.147 |       0.107 |              0.005 |
|              7 | 552 |   0.229 |         0.6   |       0.194 |       0.072 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.25  |         0.596 |       0.165 |       0.076 |              0.011 |
| 2-3          | 192 |   0.156 |         0.51  |       0.203 |       0.068 |              0.012 |
| 4-7          | 150 |   0.304 |         0.433 |       0.18  |       0.093 |              0.011 |
| 8-30         | 426 |   0.019 |         0.211 |       0.15  |       0.157 |              0.002 |
| >30          | 123 |  -0.026 |         0.154 |       0.041 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.971 |         0.056 |       0     |       0.111 |             -0.005 |
| more          |   75 |   0.381 |         0.507 |       0.08  |       0.107 |              0.018 |
| same          | 1563 |   0.192 |         0.441 |       0.163 |       0.091 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  42 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  48 |  -49.091 |         0.042 |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  48 |   -4.637 |         0     |       0     |       0     |             -0.001 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  42 |   -3.875 |         0.071 |       0     |       0.048 |              0.001 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  42 |   -1.008 |         0.19  |       0     |       0.024 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  48 |   -0.648 |         0.104 |       0.042 |       0.354 |             -0.005 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  42 |   -0.425 |         0.024 |       0     |       0.095 |             -0.003 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  42 |   -0.364 |         0     |       0     |       1     |             -0.002 |

## Each base model alone: skill by group
| group                              |   drift |   leader |
|:-----------------------------------|--------:|---------:|
| afhubbard|hyperscaler_spot         |   0.186 |    0.17  |
| fastgpu_daily|hyperscaler_spot     |  -0     |    0.146 |
| fastgpu_daily|neocloud_rate_card   |  -0     |    0.118 |
| fastgpu_daily|neocloud_spot        |  -0     |    0.066 |
| gpurentalprices|marketplace_ask    |   0.196 |    0.208 |
| gpurentalprices|neocloud_rate_card |   0.056 |    0.142 |

## Mean ensemble weight by group
| group                              |   drift |   leader |
|:-----------------------------------|--------:|---------:|
| afhubbard|hyperscaler_spot         |     0.5 |      0.5 |
| fastgpu_daily|hyperscaler_spot     |     0.5 |      0.5 |
| fastgpu_daily|neocloud_rate_card   |     0.5 |      0.5 |
| fastgpu_daily|neocloud_spot        |     0.5 |      0.5 |
| gpurentalprices|marketplace_ask    |     0.5 |      0.5 |
| gpurentalprices|neocloud_rate_card |     0.5 |      0.5 |

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
