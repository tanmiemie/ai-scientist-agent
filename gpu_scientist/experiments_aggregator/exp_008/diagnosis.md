# Diagnosis (dev origins only)

Cells: 3256. Overall skill 0.1964; truth above q50 in 46% of cells (50% if unbiased); above q90 11% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  372 |  -0.008 |         0.22  |       0.07  |       0.046 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     |  174 |   0.189 |         0.19  |       0.115 |       0.23  |             -0.016 |
| fastgpu_daily|neocloud_rate_card   |  957 |   0.21  |         0.539 |       0.116 |       0.114 |              0.005 |
| fastgpu_daily|neocloud_spot        |  609 |   0.236 |         0.424 |       0.115 |       0.12  |              0.011 |
| gpurentalprices|marketplace_ask    |   88 |   0.173 |         0.261 |       0.045 |       0.023 |              0.01  |
| gpurentalprices|neocloud_rate_card | 1056 |   0.193 |         0.566 |       0.129 |       0.063 |              0.018 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1094 |   0.056 |         0.331 |       0.111 |       0.112 |              0.002 |
|              3 | 1081 |   0.154 |         0.472 |       0.103 |       0.09  |              0.007 |
|              7 | 1081 |   0.248 |         0.59  |       0.125 |       0.082 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1685 |   0.228 |         0.614 |       0.115 |       0.101 |              0.01  |
| 2-3          |  405 |   0.114 |         0.378 |       0.106 |       0.057 |              0.009 |
| 4-7          |  398 |   0.22  |         0.382 |       0.103 |       0.075 |              0.011 |
| 8-30         |  600 |   0.085 |         0.228 |       0.128 |       0.14  |              0.002 |
| >30          |  168 |   0.028 |         0.196 |       0.071 |       0     |              0.014 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.116 |         0.423 |       0.065 |       0.089 |              0.009 |
| more          |  554 |   0.179 |         0.554 |       0.072 |       0.045 |              0.015 |
| same          | 2534 |   0.21  |         0.447 |       0.125 |       0.106 |              0.007 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  87 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  93 |   -2.193 |         0     |       0     |       0.032 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  88 |   -0.483 |         0.25  |       0.011 |       0.216 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  87 |   -0.47  |         0.299 |       0.034 |       0.034 |              0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  88 |   -0.144 |         0.659 |       0.148 |       0.045 |              0.006 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  88 |   -0.141 |         0.352 |       0.011 |       0.057 |              0.005 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  88 |   -0.015 |         0.455 |       0.148 |       0.057 |              0.057 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  87 |    0.016 |         0.184 |       0.034 |       0.092 |              0.002 |

## Each base model alone: skill by group
| group                              |   aggregator |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |        0.094 |
| fastgpu_daily|hyperscaler_spot     |        0.13  |
| fastgpu_daily|neocloud_rate_card   |        0.189 |
| fastgpu_daily|neocloud_spot        |        0.291 |
| gpurentalprices|marketplace_ask    |        0.172 |
| gpurentalprices|neocloud_rate_card |        0.165 |

## Mean ensemble weight by group
| group                              |   aggregator |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |            1 |
| fastgpu_daily|hyperscaler_spot     |            1 |
| fastgpu_daily|neocloud_rate_card   |            1 |
| fastgpu_daily|neocloud_spot        |            1 |
| gpurentalprices|marketplace_ask    |            1 |
| gpurentalprices|neocloud_rate_card |            1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                           | leader                                                            |   lag_days |   corr |
|:-----------------------------------------------------------------|:------------------------------------------------------------------|-----------:|-------:|
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_rate_card.B200.serverless.median         |          3 | -0.928 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_spot.B200.spot.median                    |          1 |  0.928 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      | gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median     |          3 | -0.925 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median |          2 |  0.922 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median      |          4 |  0.884 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median           |          4 |  0.868 |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | afhubbard.hyperscaler_list.B300.on_demand.median                  |          1 | -0.85  |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | fastgpu_daily.hyperscaler_list.B300.on_demand.median              |          2 | -0.85  |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median        |          1 |  0.8   |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     | afhubbard.neocloud_spot.L40S.spot.median                          |          1 |  0.789 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  |          1 |  0.785 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median |          3 |  0.762 |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     | afhubbard.neocloud_rate_card.L40S.on_demand.median                |          1 |  0.736 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median       |          5 |  0.71  |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median      |          5 |  0.705 |
