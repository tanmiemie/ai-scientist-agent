# Diagnosis (dev origins only)

Cells: 3256. Overall skill 0.1871; truth above q50 in 46% of cells (50% if unbiased); above q90 12% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  372 |   0.008 |         0.22  |       0.07  |       0.051 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     |  174 |   0.164 |         0.19  |       0.115 |       0.247 |             -0.016 |
| fastgpu_daily|neocloud_rate_card   |  957 |   0.203 |         0.532 |       0.119 |       0.117 |              0.005 |
| fastgpu_daily|neocloud_spot        |  609 |   0.202 |         0.42  |       0.123 |       0.146 |              0.01  |
| gpurentalprices|marketplace_ask    |   88 |   0.179 |         0.261 |       0.08  |       0.023 |              0.01  |
| gpurentalprices|neocloud_rate_card | 1056 |   0.183 |         0.566 |       0.13  |       0.062 |              0.018 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1094 |   0.035 |         0.329 |       0.112 |       0.115 |              0.002 |
|              3 | 1081 |   0.145 |         0.469 |       0.108 |       0.098 |              0.007 |
|              7 | 1081 |   0.242 |         0.586 |       0.13  |       0.092 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1685 |   0.217 |         0.609 |       0.119 |       0.116 |              0.01  |
| 2-3          |  405 |   0.113 |         0.378 |       0.111 |       0.052 |              0.009 |
| 4-7          |  398 |   0.216 |         0.382 |       0.108 |       0.078 |              0.011 |
| 8-30         |  600 |   0.069 |         0.228 |       0.128 |       0.138 |              0.002 |
| >30          |  168 |   0.026 |         0.196 |       0.083 |       0     |              0.014 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.095 |         0.423 |       0.071 |       0.107 |              0.008 |
| more          |  554 |   0.166 |         0.538 |       0.074 |       0.072 |              0.014 |
| same          | 2534 |   0.203 |         0.447 |       0.129 |       0.108 |              0.007 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  87 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  93 |   -2.098 |         0     |       0     |       0.043 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  88 |   -0.593 |         0.25  |       0.011 |       0.17  |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  87 |   -0.418 |         0.299 |       0.011 |       0.057 |              0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  88 |   -0.22  |         0.659 |       0.125 |       0.023 |              0.006 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  88 |   -0.21  |         0.352 |       0.011 |       0.034 |              0.005 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median           |  87 |   -0.051 |         0.241 |       0.103 |       0.057 |              0.006 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  88 |   -0.004 |         0.455 |       0.193 |       0.034 |              0.057 |

## Each base model alone: skill by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.075 |
| fastgpu_daily|hyperscaler_spot     |      0.078 |
| fastgpu_daily|neocloud_rate_card   |      0.177 |
| fastgpu_daily|neocloud_spot        |      0.257 |
| gpurentalprices|marketplace_ask    |      0.176 |
| gpurentalprices|neocloud_rate_card |      0.163 |

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
