# Diagnosis (dev origins only)

Cells: 1101. Overall skill 0.1185; truth above q50 in 40% of cells (50% if unbiased); above q90 17% and below q10 9% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 132 |  -0.107 |         0.25  |       0.061 |       0.023 |              0     |
| fastgpu_daily|hyperscaler_spot     |  54 |   0.154 |         0.222 |       0.222 |       0.259 |             -0.017 |
| fastgpu_daily|neocloud_rate_card   | 297 |   0.148 |         0.455 |       0.165 |       0.108 |              0.004 |
| fastgpu_daily|neocloud_spot        | 189 |  -0.077 |         0.249 |       0.238 |       0.18  |              0.006 |
| gpurentalprices|marketplace_ask    |  33 |   0.189 |         0.333 |       0.061 |       0.03  |             -0.029 |
| gpurentalprices|neocloud_rate_card | 396 |   0.137 |         0.497 |       0.179 |       0.038 |              0.006 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 367 |  -0.116 |         0.24  |       0.142 |       0.125 |             -0.001 |
|              3 | 367 |   0.182 |         0.403 |       0.112 |       0.06  |              0.001 |
|              7 | 367 |   0.132 |         0.542 |       0.256 |       0.084 |              0.008 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 492 |   0.139 |         0.516 |       0.163 |       0.11  |              0     |
| 2-3          | 123 |   0.143 |         0.553 |       0.211 |       0.033 |              0.008 |
| 4-7          |  90 |   0.299 |         0.433 |       0.167 |       0.089 |             -0     |
| 8-30         | 303 |  -0.054 |         0.208 |       0.205 |       0.109 |              0.004 |
| >30          |  93 |  -0.35  |         0.118 |       0.043 |       0     |              0.003 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |    6 |  -0.274 |           0   |       0     |       0.833 |             -0.008 |
| more          |   15 |  -1.459 |           0.2 |       0.133 |       0.4   |             -0.005 |
| same          | 1080 |   0.13  |           0.4 |       0.171 |       0.081 |              0.003 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  33 | -inf     |         0     |        0    |       0     |             -0.002 |
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  27 | -inf     |         0     |        0    |       0     |              0     |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  27 | -inf     |         0     |        0    |       1     |             -0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  33 | -inf     |         0     |        0    |       0     |              0     |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median   |  33 | -inf     |         0     |        0    |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  27 |   -3.874 |         0     |        0    |       0.037 |             -0     |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  27 |   -0.725 |         0.037 |        0    |       0.185 |             -0.001 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  33 |   -0.417 |         0.152 |        0.03 |       0.03  |             -0.004 |

## Each base model alone: skill by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.072 |
| fastgpu_daily|hyperscaler_spot     |      0.157 |
| fastgpu_daily|neocloud_rate_card   |      0.141 |
| fastgpu_daily|neocloud_spot        |     -0.052 |
| gpurentalprices|marketplace_ask    |      0.191 |
| gpurentalprices|neocloud_rate_card |      0.286 |

## Mean ensemble weight by group
| group                              |   momentum |
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
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median     |          1 |  0.896 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median |          1 | -0.515 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median          | afhubbard.hyperscaler_spot.B200.spot.median                    |          5 | -0.513 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | afhubbard.hyperscaler_spot.H100_SXM_80GB.spot.median           |          1 | -0.464 |
| gpurentalprices.neocloud_rate_card.A100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.A100_SXM_80GB.spot.median     |          5 |  0.418 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  | afhubbard.neocloud_rate_card.RTX_PRO_6000.on_demand.median     |          1 |  0.398 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_spot.H200.spot.median              |          5 |  0.338 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | afhubbard.neocloud_rate_card.H200.on_demand.median             |          4 |  0.326 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median         |          5 |  0.312 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_spot.H100_80GB.spot.median            |          3 | -0.308 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median     | gpurentalprices.marketplace_ask.H100_80GB.spot.median          |          1 |  0.308 |
