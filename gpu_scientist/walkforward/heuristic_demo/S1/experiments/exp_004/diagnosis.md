# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.2041; truth above q50 in 43% of cells (50% if unbiased); above q90 16% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.162 |         0.266 |       0.078 |       0.047 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.043 |         0.333 |       0.25  |       0.274 |              0.017 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.207 |         0.45  |       0.171 |       0.136 |              0.003 |
| fastgpu_daily|neocloud_spot        | 294 |   0.168 |         0.316 |       0.221 |       0.173 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.101 |         0.375 |       0.021 |       0.042 |             -0.024 |
| gpurentalprices|neocloud_rate_card | 576 |   0.241 |         0.536 |       0.156 |       0.056 |              0.016 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.081 |         0.279 |       0.129 |       0.089 |              0.001 |
|              3 | 552 |   0.068 |         0.428 |       0.139 |       0.129 |              0.005 |
|              7 | 552 |   0.276 |         0.574 |       0.223 |       0.109 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.242 |         0.571 |       0.166 |       0.094 |              0.01  |
| 2-3          | 192 |   0.139 |         0.505 |       0.188 |       0.104 |              0.012 |
| 4-7          | 150 |   0.271 |         0.427 |       0.233 |       0.153 |              0.012 |
| 8-30         | 426 |   0.088 |         0.211 |       0.157 |       0.153 |              0.002 |
| >30          | 123 |  -0.059 |         0.154 |       0.049 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -1.064 |         0.333 |       0     |       0.333 |             -0.001 |
| more          |   75 |   0.319 |         0.467 |       0.107 |       0.16  |              0.016 |
| same          | 1563 |   0.199 |         0.426 |       0.168 |       0.104 |              0.008 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  42 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  48 |  -41.274 |         0.042 |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  48 |   -3.224 |         0     |       0     |       0.042 |             -0.001 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median           |  42 |   -0.946 |         0.071 |       0     |       0.048 |              0.001 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  42 |   -0.372 |         0     |       0     |       1     |             -0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  48 |   -0.345 |         0.104 |       0.021 |       0.229 |             -0.004 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median         |  48 |   -0.084 |         0.562 |       0.229 |       0     |              0.009 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  42 |   -0.058 |         0     |       0     |       0.286 |             -0.032 |

## Each base model alone: skill by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |         0.22  |
| fastgpu_daily|hyperscaler_spot     |        -0.008 |
| fastgpu_daily|neocloud_rate_card   |         0.08  |
| fastgpu_daily|neocloud_spot        |         0.035 |
| gpurentalprices|marketplace_ask    |         0.098 |
| gpurentalprices|neocloud_rate_card |         0.112 |

## Mean ensemble weight by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |             1 |
| fastgpu_daily|hyperscaler_spot     |             1 |
| fastgpu_daily|neocloud_rate_card   |             1 |
| fastgpu_daily|neocloud_spot        |             1 |
| gpurentalprices|marketplace_ask    |             1 |
| gpurentalprices|neocloud_rate_card |             1 |

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
