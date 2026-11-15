# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.0351; truth above q50 in 44% of cells (50% if unbiased); above q90 14% and below q10 9% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.114 |         0.26  |       0.083 |       0.031 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.193 |         0.298 |       0.202 |       0.238 |              0.006 |
| fastgpu_daily|neocloud_rate_card   | 462 |  -0.028 |         0.517 |       0.11  |       0.071 |              0.005 |
| fastgpu_daily|neocloud_spot        | 294 |   0.134 |         0.32  |       0.19  |       0.163 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.161 |         0.229 |       0.021 |       0.042 |             -0.031 |
| gpurentalprices|neocloud_rate_card | 576 |   0.037 |         0.536 |       0.156 |       0.078 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |  -0.055 |         0.275 |       0.141 |       0.091 |              0.001 |
|              3 | 552 |  -0.108 |         0.444 |       0.125 |       0.101 |              0.005 |
|              7 | 552 |   0.107 |         0.6   |       0.152 |       0.087 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.07  |         0.596 |       0.144 |       0.084 |              0.011 |
| 2-3          | 192 |  -0.002 |         0.51  |       0.182 |       0.078 |              0.012 |
| 4-7          | 150 |   0.14  |         0.433 |       0.2   |       0.087 |              0.011 |
| 8-30         | 426 |  -0.088 |         0.211 |       0.127 |       0.146 |              0.002 |
| >30          | 123 |  -0.616 |         0.154 |       0.016 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -1.092 |         0.056 |       0     |       0.111 |             -0.006 |
| more          |   75 |   0.198 |         0.507 |       0.12  |       0.107 |              0.018 |
| same          | 1563 |   0.024 |         0.441 |       0.142 |       0.092 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  42 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  48 |  -88.779 |         0.042 |       0     |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  42 |   -7.39  |         0.071 |       0     |       0.048 |              0.001 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  48 |   -3.757 |         0     |       0     |       0     |             -0.001 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  42 |   -2.215 |         0.19  |       0.024 |       0.024 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  48 |   -1.446 |         0.104 |       0.021 |       0.375 |             -0.004 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  42 |   -0.992 |         0.024 |       0     |       0.095 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  42 |   -0.925 |         0.762 |       0.143 |       0     |              0.007 |

## Each base model alone: skill by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |   0.186 |
| fastgpu_daily|hyperscaler_spot     |  -0     |
| fastgpu_daily|neocloud_rate_card   |  -0     |
| fastgpu_daily|neocloud_spot        |  -0     |
| gpurentalprices|marketplace_ask    |   0.196 |
| gpurentalprices|neocloud_rate_card |   0.056 |

## Mean ensemble weight by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |       1 |
| fastgpu_daily|hyperscaler_spot     |       1 |
| fastgpu_daily|neocloud_rate_card   |       1 |
| fastgpu_daily|neocloud_spot        |       1 |
| gpurentalprices|marketplace_ask    |       1 |
| gpurentalprices|neocloud_rate_card |       1 |

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
