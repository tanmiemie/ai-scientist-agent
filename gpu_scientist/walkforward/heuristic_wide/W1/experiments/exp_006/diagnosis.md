# Diagnosis (dev origins only)

Cells: 657. Overall skill 0.2071; truth above q50 in 40% of cells (50% if unbiased); above q90 23% and below q10 7% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  84 |   0.274 |         0.262 |       0.06  |       0.048 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  30 |   0.375 |         0.3   |       0.3   |       0.367 |             -0.03  |
| fastgpu_daily|neocloud_rate_card   | 165 |   0.174 |         0.515 |       0.248 |       0.036 |              0.006 |
| fastgpu_daily|neocloud_spot        | 105 |  -0     |         0.152 |       0.152 |       0.143 |              0.002 |
| gpurentalprices|marketplace_ask    |  21 |   0.129 |         0.476 |       0.095 |       0.143 |              0.016 |
| gpurentalprices|neocloud_rate_card | 252 |   0.25  |         0.488 |       0.321 |       0.032 |              0.007 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 219 |   0.221 |         0.215 |       0.1   |       0.087 |              0.001 |
|              3 | 219 |   0.299 |         0.425 |       0.201 |       0.073 |              0.002 |
|              7 | 219 |   0.154 |         0.571 |       0.402 |       0.055 |              0.009 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 261 |   0.197 |         0.533 |       0.268 |       0.084 |              0.004 |
| 2-3          |  90 |   0.243 |         0.644 |       0.344 |       0     |              0.01  |
| 4-7          |  63 |   0.394 |         0.429 |       0.222 |       0.143 |             -0.003 |
| 8-30         | 180 |   0.054 |         0.194 |       0.183 |       0.089 |              0.004 |
| >30          |  63 |   0     |         0.095 |       0.095 |       0     |              0.002 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   6 |  -0.054 |         0     |       0     |       0.833 |             -0.005 |
| more          |   3 |   0.383 |         1     |       0.333 |       0     |              0.008 |
| same          | 648 |   0.208 |         0.404 |       0.236 |       0.065 |              0.004 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  21 | -inf     |         0     |       0     |       0     |              0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  15 | -inf     |         0     |       0     |       1     |             -0     |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  15 |   -0.181 |         0     |       0     |       0.333 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.RTX_PRO_6000.on_demand.median   |  15 |    0     |         0.4   |       0.4   |       0     |              0.009 |
| fastgpu_daily.neocloud_spot.B300.spot.median                     |  15 |    0     |         0.4   |       0.4   |       0     |              0.008 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median |  21 |    0     |         0.286 |       0.286 |       0     |              0.006 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             |  15 |    0     |         0.4   |       0.4   |       0     |              0.003 |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     |  15 |    0     |         0.267 |       0.267 |       0     |              0.005 |

## Each base model alone: skill by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.274 |
| fastgpu_daily|hyperscaler_spot     |      0.375 |
| fastgpu_daily|neocloud_rate_card   |      0.174 |
| fastgpu_daily|neocloud_spot        |     -0     |
| gpurentalprices|marketplace_ask    |      0.129 |
| gpurentalprices|neocloud_rate_card |      0.25  |

## Mean ensemble weight by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |          1 |
| fastgpu_daily|hyperscaler_spot     |          1 |
| fastgpu_daily|neocloud_rate_card   |          1 |
| fastgpu_daily|neocloud_spot        |          1 |
| gpurentalprices|marketplace_ask    |          1 |
| gpurentalprices|neocloud_rate_card |          1 |

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
