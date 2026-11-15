# Diagnosis (dev origins only)

Cells: 1656. Overall skill -35.9368; truth above q50 in 41% of cells (50% if unbiased); above q90 1% and below q10 17% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 | -59.91  |         0.229 |       0     |       0.203 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  84 | -35.758 |         0.274 |       0.024 |       0.345 |             -0.001 |
| fastgpu_daily|neocloud_rate_card   | 462 | -31.055 |         0.444 |       0.03  |       0.093 |              0.003 |
| fastgpu_daily|neocloud_spot        | 294 | -78.813 |         0.32  |       0.017 |       0.163 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |  -8.886 |         0.229 |       0     |       0.458 |             -0.031 |
| gpurentalprices|neocloud_rate_card | 576 | -36.158 |         0.536 |       0     |       0.167 |              0.017 |

## By horizon
|   horizon_days |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|---------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 | -170.71  |         0.275 |       0     |       0.123 |              0.001 |
|              3 | 552 |  -44.259 |         0.409 |       0     |       0.174 |              0.005 |
|              7 | 552 |  -17.287 |         0.558 |       0.038 |       0.205 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 | -31.184 |         0.553 |       0.004 |       0.192 |              0.009 |
| 2-3          | 192 | -33.136 |         0.474 |       0.021 |       0.146 |              0.01  |
| 4-7          | 150 | -29.107 |         0.42  |       0.027 |       0.227 |              0.008 |
| 8-30         | 426 | -56.113 |         0.211 |       0.023 |       0.16  |              0.002 |
| >30          | 123 | -98.917 |         0.154 |       0     |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 | -52.506 |         0.056 |       0     |       0.333 |             -0.006 |
| more          |   75 | -22.457 |         0.467 |       0     |       0.107 |              0.017 |
| same          | 1563 | -37.431 |         0.416 |       0.013 |       0.168 |              0.007 |

## Worst series
| series_id                                                       |   n |     skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|----------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  42 |  -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  48 | -7021.94  |         0.042 |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  48 |  -605.366 |         0     |       0     |       0.062 |             -0.001 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  42 |  -567.011 |         0.071 |       0     |       0.095 |              0.001 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  42 |  -325.834 |         0     |       0     |       1     |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  42 |  -202.334 |         0.19  |       0     |       0.119 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  48 |  -141.381 |         0.104 |       0     |       0.792 |             -0.005 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  42 |  -105.892 |         0.571 |       0.048 |       0     |              0.004 |

## Each base model alone: skill by group
| group                              |   vol_adapt |
|:-----------------------------------|------------:|
| afhubbard|hyperscaler_spot         |     -59.91  |
| fastgpu_daily|hyperscaler_spot     |     -35.758 |
| fastgpu_daily|neocloud_rate_card   |     -31.055 |
| fastgpu_daily|neocloud_spot        |     -78.813 |
| gpurentalprices|marketplace_ask    |      -8.886 |
| gpurentalprices|neocloud_rate_card |     -36.158 |

## Mean ensemble weight by group
| group                              |   vol_adapt |
|:-----------------------------------|------------:|
| afhubbard|hyperscaler_spot         |           1 |
| fastgpu_daily|hyperscaler_spot     |           1 |
| fastgpu_daily|neocloud_rate_card   |           1 |
| fastgpu_daily|neocloud_spot        |           1 |
| gpurentalprices|marketplace_ask    |           1 |
| gpurentalprices|neocloud_rate_card |           1 |

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
