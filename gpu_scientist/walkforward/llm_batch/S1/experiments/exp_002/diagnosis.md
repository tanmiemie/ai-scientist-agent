# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.1751; truth above q50 in 43% of cells (50% if unbiased); above q90 16% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |  -0.011 |         0.255 |       0.094 |       0.036 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.128 |         0.298 |       0.202 |       0.155 |              0.004 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.157 |         0.489 |       0.119 |       0.108 |              0.004 |
| fastgpu_daily|neocloud_spot        | 294 |   0.116 |         0.313 |       0.221 |       0.228 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.177 |         0.229 |       0.042 |       0.042 |             -0.033 |
| gpurentalprices|neocloud_rate_card | 576 |   0.224 |         0.535 |       0.181 |       0.075 |              0.016 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |  -0.204 |         0.264 |       0.138 |       0.134 |              0     |
|              3 | 552 |   0.147 |         0.433 |       0.141 |       0.12  |              0.004 |
|              7 | 552 |   0.23  |         0.591 |       0.194 |       0.076 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.209 |         0.574 |       0.162 |       0.131 |              0.009 |
| 2-3          | 192 |   0.134 |         0.51  |       0.208 |       0.047 |              0.012 |
| 4-7          | 150 |   0.267 |         0.433 |       0.18  |       0.093 |              0.011 |
| 8-30         | 426 |   0.033 |         0.211 |       0.153 |       0.138 |              0.002 |
| >30          | 123 |  -0.066 |         0.154 |       0.041 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.987 |         0.056 |       0     |       0.111 |             -0.005 |
| more          |   75 |   0.272 |         0.467 |       0.107 |       0.307 |              0.016 |
| same          | 1563 |   0.172 |         0.432 |       0.162 |       0.1   |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  42 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  48 |  -50.198 |         0.042 |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  48 |   -4.897 |         0     |       0     |       0     |             -0.002 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  42 |   -3.861 |         0.071 |       0     |       0     |              0.001 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  42 |   -1.059 |         0.19  |       0     |       0.024 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  48 |   -0.563 |         0.104 |       0.042 |       0.188 |             -0.005 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  42 |   -0.369 |         0.024 |       0     |       0.095 |             -0.003 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  42 |   -0.367 |         0     |       0     |       0.976 |             -0.002 |

## Each base model alone: skill by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |   0.186 |      0.071 |
| fastgpu_daily|hyperscaler_spot     |  -0     |      0.078 |
| fastgpu_daily|neocloud_rate_card   |  -0     |      0.122 |
| fastgpu_daily|neocloud_spot        |  -0     |      0.033 |
| gpurentalprices|marketplace_ask    |   0.196 |      0.164 |
| gpurentalprices|neocloud_rate_card |   0.056 |      0.168 |

## Mean ensemble weight by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |     0.5 |        0.5 |
| fastgpu_daily|hyperscaler_spot     |     0.5 |        0.5 |
| fastgpu_daily|neocloud_rate_card   |     0.5 |        0.5 |
| fastgpu_daily|neocloud_spot        |     0.5 |        0.5 |
| gpurentalprices|marketplace_ask    |     0.5 |        0.5 |
| gpurentalprices|neocloud_rate_card |     0.5 |        0.5 |

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
