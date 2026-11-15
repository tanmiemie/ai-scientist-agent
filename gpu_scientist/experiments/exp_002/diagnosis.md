# Diagnosis (dev origins only)

Cells: 3256. Overall skill 0.1742; truth above q50 in 47% of cells (50% if unbiased); above q90 12% and below q10 8% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  372 |   0.033 |         0.234 |       0.073 |       0.054 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  174 |   0.18  |         0.19  |       0.115 |       0.241 |             -0.015 |
| fastgpu_daily|neocloud_rate_card   |  957 |   0.197 |         0.531 |       0.116 |       0.109 |              0.006 |
| fastgpu_daily|neocloud_spot        |  609 |   0.2   |         0.424 |       0.123 |       0.072 |              0.011 |
| gpurentalprices|marketplace_ask    |   88 |   0.193 |         0.273 |       0.08  |       0.023 |              0.014 |
| gpurentalprices|neocloud_rate_card | 1056 |   0.146 |         0.576 |       0.131 |       0.056 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1094 |   0.064 |         0.336 |       0.102 |       0.083 |              0.003 |
|              3 | 1081 |   0.132 |         0.473 |       0.105 |       0.085 |              0.008 |
|              7 | 1081 |   0.22  |         0.591 |       0.141 |       0.081 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1685 |   0.201 |         0.625 |       0.125 |       0.084 |              0.012 |
| 2-3          |  405 |   0.114 |         0.37  |       0.091 |       0.069 |              0.009 |
| 4-7          |  398 |   0.196 |         0.367 |       0.103 |       0.083 |              0.011 |
| 8-30         |  600 |   0.069 |         0.227 |       0.13  |       0.115 |              0.002 |
| >30          |  168 |   0.032 |         0.196 |       0.071 |       0     |              0.014 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.065 |         0.423 |       0.077 |       0.095 |              0.009 |
| more          |  554 |   0.16  |         0.518 |       0.063 |       0.058 |              0.015 |
| same          | 2534 |   0.189 |         0.458 |       0.13  |       0.088 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  87 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  93 |   -2.182 |         0     |       0     |       0.043 |             -0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  88 |   -0.699 |         0.25  |       0.011 |       0.216 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  87 |   -0.41  |         0.299 |       0.023 |       0.057 |              0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  88 |   -0.345 |         0.659 |       0.159 |       0.023 |              0.007 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  88 |   -0.277 |         0.364 |       0.011 |       0.023 |              0.006 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median           |  87 |   -0.008 |         0.241 |       0.103 |       0     |              0.007 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  87 |    0.001 |         0.184 |       0.046 |       0.092 |              0.002 |

## Each base model alone: skill by group
| group                              |   trend_tail |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |        0.113 |
| fastgpu_daily|hyperscaler_spot     |        0.095 |
| fastgpu_daily|neocloud_rate_card   |        0.172 |
| fastgpu_daily|neocloud_spot        |        0.241 |
| gpurentalprices|marketplace_ask    |        0.191 |
| gpurentalprices|neocloud_rate_card |        0.151 |

## Mean ensemble weight by group
| group                              |   trend_tail |
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
