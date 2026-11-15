# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.2074; truth above q50 in 45% of cells (50% if unbiased); above q90 16% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.114 |         0.312 |       0.078 |       0.036 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.166 |         0.31  |       0.226 |       0.155 |              0.006 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.196 |         0.526 |       0.119 |       0.093 |              0.005 |
| fastgpu_daily|neocloud_spot        | 294 |   0.156 |         0.323 |       0.221 |       0.184 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.204 |         0.271 |       0.021 |       0.042 |             -0.025 |
| gpurentalprices|neocloud_rate_card | 576 |   0.239 |         0.54  |       0.177 |       0.085 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.034 |         0.284 |       0.132 |       0.123 |              0.001 |
|              3 | 552 |   0.199 |         0.464 |       0.145 |       0.109 |              0.005 |
|              7 | 552 |   0.23  |         0.607 |       0.188 |       0.072 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.247 |         0.603 |       0.163 |       0.089 |              0.011 |
| 2-3          | 192 |   0.164 |         0.547 |       0.188 |       0.083 |              0.012 |
| 4-7          | 150 |   0.311 |         0.46  |       0.18  |       0.107 |              0.011 |
| 8-30         | 426 |   0.035 |         0.221 |       0.15  |       0.16  |              0.002 |
| >30          | 123 |  -0.021 |         0.154 |       0.041 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.962 |         0.056 |       0     |       0.111 |             -0.004 |
| more          |   75 |   0.375 |         0.533 |       0.12  |       0.133 |              0.018 |
| same          | 1563 |   0.196 |         0.452 |       0.159 |       0.1   |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  42 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  48 |  -47.446 |         0.042 |       0     |       0     |              0     |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median          |  42 |   -3.715 |         0.071 |       0     |       0.048 |              0.001 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  48 |   -3.399 |         0.167 |       0     |       0.021 |             -0.001 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  42 |   -0.944 |         0.262 |       0.024 |       0.143 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  48 |   -0.629 |         0.104 |       0.042 |       0.354 |             -0.005 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  42 |   -0.397 |         0.024 |       0     |       0.095 |             -0.003 |
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
| afhubbard|hyperscaler_spot         |    0.35 |     0.65 |
| fastgpu_daily|hyperscaler_spot     |    0.3  |     0.7  |
| fastgpu_daily|neocloud_rate_card   |    0.42 |     0.58 |
| fastgpu_daily|neocloud_spot        |    0.49 |     0.51 |
| gpurentalprices|marketplace_ask    |    0.33 |     0.67 |
| gpurentalprices|neocloud_rate_card |    0.35 |     0.65 |

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
