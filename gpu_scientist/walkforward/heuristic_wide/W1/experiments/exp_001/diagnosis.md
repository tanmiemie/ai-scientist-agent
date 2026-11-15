# Diagnosis (dev origins only)

Cells: 657. Overall skill 0.0875; truth above q50 in 40% of cells (50% if unbiased); above q90 24% and below q10 7% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  84 |   0.117 |         0.262 |       0.024 |       0.06  |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  30 |  -0.002 |         0.3   |       0.3   |       0.433 |             -0.03  |
| fastgpu_daily|neocloud_rate_card   | 165 |   0.016 |         0.515 |       0.364 |       0.036 |              0.006 |
| fastgpu_daily|neocloud_spot        | 105 |  -0     |         0.152 |       0.152 |       0.143 |              0.002 |
| gpurentalprices|marketplace_ask    |  21 |   0.278 |         0.381 |       0.048 |       0.048 |              0.007 |
| gpurentalprices|neocloud_rate_card | 252 |   0.03  |         0.488 |       0.286 |       0.02  |              0.007 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 219 |   0.147 |         0.215 |       0.151 |       0.082 |              0     |
|              3 | 219 |   0.103 |         0.425 |       0.205 |       0.068 |              0.002 |
|              7 | 219 |   0.065 |         0.562 |       0.374 |       0.055 |              0.008 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 261 |   0.118 |         0.525 |       0.303 |       0.065 |              0.004 |
| 2-3          |  90 |   0.116 |         0.644 |       0.289 |       0.011 |              0.01  |
| 4-7          |  63 |   0.138 |         0.429 |       0.317 |       0.175 |             -0.003 |
| 8-30         | 180 |  -0.055 |         0.194 |       0.189 |       0.089 |              0.004 |
| >30          |  63 |  -0.586 |         0.095 |       0.016 |       0     |              0.002 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   6 |  -0.009 |         0     |       0     |       0.833 |             -0.005 |
| more          |   3 |  -0.451 |         1     |       1     |       0     |              0.008 |
| same          | 648 |   0.09  |         0.401 |       0.242 |       0.062 |              0.004 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  21 | -inf     |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median      |  15 | -inf     |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median           |  15 | -inf     |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  15 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  21 | -inf     |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  15 | -inf     |         0     |       0     |       1     |             -0     |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median    |  21 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  21 |   -0.369 |         0.143 |       0.048 |       0.048 |             -0.003 |

## Each base model alone: skill by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |   0.16  |
| fastgpu_daily|hyperscaler_spot     |  -0     |
| fastgpu_daily|neocloud_rate_card   |  -0     |
| fastgpu_daily|neocloud_spot        |  -0     |
| gpurentalprices|marketplace_ask    |   0.289 |
| gpurentalprices|neocloud_rate_card |   0.051 |

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
| series                                                            | leader                                                         |   lag_days |   corr |
|:------------------------------------------------------------------|:---------------------------------------------------------------|-----------:|-------:|
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median     |          1 |  0.872 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | afhubbard.hyperscaler_spot.H100_SXM_80GB.spot.median           |          1 | -0.586 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median          | afhubbard.hyperscaler_spot.B200.spot.median                    |          5 | -0.519 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median |          1 | -0.517 |
| gpurentalprices.neocloud_rate_card.A100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.A100_SXM_80GB.spot.median     |          5 |  0.451 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_spot.H200.spot.median              |          5 |  0.41  |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | afhubbard.neocloud_rate_card.H200.on_demand.median             |          4 |  0.342 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median         |          5 |  0.332 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_spot.H100_80GB.spot.median            |          3 | -0.308 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median     | gpurentalprices.marketplace_ask.H100_80GB.spot.median          |          1 |  0.307 |
