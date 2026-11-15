# Diagnosis (dev origins only)

Cells: 657. Overall skill 0.1924; truth above q50 in 40% of cells (50% if unbiased); above q90 28% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  84 |   0.279 |         0.321 |       0.06  |       0.155 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  30 |   0.202 |         0.3   |       0.3   |       0.367 |             -0.029 |
| fastgpu_daily|neocloud_rate_card   | 165 |   0.08  |         0.473 |       0.321 |       0.042 |              0.006 |
| fastgpu_daily|neocloud_spot        | 105 |  -0     |         0.152 |       0.152 |       0.143 |              0.002 |
| gpurentalprices|marketplace_ask    |  21 |   0.233 |         0.476 |       0.048 |       0.048 |              0.015 |
| gpurentalprices|neocloud_rate_card | 252 |   0.225 |         0.492 |       0.385 |       0.079 |              0.007 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 219 |   0.223 |         0.237 |       0.137 |       0.1   |              0.001 |
|              3 | 219 |   0.285 |         0.411 |       0.237 |       0.1   |              0.002 |
|              7 | 219 |   0.135 |         0.557 |       0.452 |       0.105 |              0.009 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 261 |   0.214 |         0.521 |       0.318 |       0.13  |              0.004 |
| 2-3          |  90 |   0.187 |         0.644 |       0.411 |       0.022 |              0.01  |
| 4-7          |  63 |   0.292 |         0.46  |       0.317 |       0.238 |             -0.003 |
| 8-30         | 180 |   0.04  |         0.194 |       0.194 |       0.089 |              0.004 |
| >30          |  63 |   0     |         0.095 |       0.095 |       0     |              0.002 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   6 |  -0.027 |         0     |       0     |       0.833 |             -0.005 |
| more          |   3 |   0.35  |         1     |       1     |       0     |              0.008 |
| same          | 648 |   0.193 |         0.403 |       0.275 |       0.096 |              0.004 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  21 | -inf     |         0.143 |       0     |       0.095 |              0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  15 | -inf     |         0     |       0     |       1     |             -0     |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median          |  15 |   -0.148 |         0.6   |       0.333 |       0     |              0.005 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  15 |   -0.105 |         0     |       0     |       0.333 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.RTX_PRO_6000.on_demand.median  |  15 |    0     |         0.4   |       0.4   |       0     |              0.009 |
| fastgpu_daily.neocloud_spot.B300.spot.median                    |  15 |    0     |         0.4   |       0.4   |       0     |              0.008 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median            |  15 |    0     |         0.4   |       0.4   |       0     |              0.003 |
| fastgpu_daily.neocloud_spot.L40S.spot.median                    |  15 |    0     |         0.267 |       0.267 |       0     |              0.005 |

## Each base model alone: skill by group
| group                              |   step_hazard |   trend_tail |
|:-----------------------------------|--------------:|-------------:|
| afhubbard|hyperscaler_spot         |         0.287 |        0.239 |
| fastgpu_daily|hyperscaler_spot     |         0.021 |        0.393 |
| fastgpu_daily|neocloud_rate_card   |        -0.081 |        0.174 |
| fastgpu_daily|neocloud_spot        |        -0     |       -0     |
| gpurentalprices|marketplace_ask    |         0.207 |        0.296 |
| gpurentalprices|neocloud_rate_card |         0.149 |        0.259 |

## Mean ensemble weight by group
| group                              |   step_hazard |   trend_tail |
|:-----------------------------------|--------------:|-------------:|
| afhubbard|hyperscaler_spot         |          0.32 |         0.68 |
| fastgpu_daily|hyperscaler_spot     |          0.52 |         0.48 |
| fastgpu_daily|neocloud_rate_card   |          0.46 |         0.54 |
| fastgpu_daily|neocloud_spot        |          0.5  |         0.5  |
| gpurentalprices|marketplace_ask    |          0.67 |         0.33 |
| gpurentalprices|neocloud_rate_card |          0.45 |         0.55 |

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
