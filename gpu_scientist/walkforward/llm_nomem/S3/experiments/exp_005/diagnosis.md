# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1749; truth above q50 in 47% of cells (50% if unbiased); above q90 11% and below q10 12% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.09  |         0.253 |       0.06  |       0.057 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.123 |         0.317 |       0.15  |       0.261 |             -0.011 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.172 |         0.497 |       0.117 |       0.136 |              0.002 |
| fastgpu_daily|neocloud_spot        |  630 |   0.26  |         0.432 |       0.122 |       0.132 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.163 |         0.393 |       0.045 |       0.022 |              0.012 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.173 |         0.59  |       0.125 |       0.095 |              0.018 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.097 |         0.362 |       0.121 |       0.118 |              0.003 |
|              3 | 1118 |   0.111 |         0.484 |       0.098 |       0.116 |              0.007 |
|              7 | 1105 |   0.224 |         0.576 |       0.122 |       0.116 |              0.015 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.211 |         0.608 |       0.116 |       0.112 |              0.009 |
| 2-3          |  408 |   0.071 |         0.409 |       0.108 |       0.105 |              0.009 |
| 4-7          |  407 |   0.185 |         0.42  |       0.111 |       0.125 |              0.01  |
| 8-30         |  613 |   0.071 |         0.24  |       0.126 |       0.16  |              0.002 |
| >30          |  171 |   0.018 |         0.222 |       0.07  |       0.018 |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.083 |         0.482 |       0.071 |       0.167 |              0.009 |
| more          |  583 |   0.158 |         0.549 |       0.069 |       0.091 |              0.01  |
| same          | 2590 |   0.19  |         0.456 |       0.127 |       0.119 |              0.007 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  96 |   -1.613 |         0.104 |       0.021 |       0.062 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  90 |   -0.669 |         0.344 |       0.022 |       0.122 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  89 |   -0.583 |         0.315 |       0.011 |       0.202 |             -0.002 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  89 |   -0.188 |         0.371 |       0.022 |       0.022 |              0.006 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  89 |   -0.166 |         0.629 |       0.146 |       0.169 |              0.005 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  89 |   -0.076 |         0.461 |       0.225 |       0.09  |              0.056 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  90 |   -0.062 |         0.211 |       0.056 |       0.089 |              0.004 |

## Each base model alone: skill by group
| group                              |   drift |   step_hazard |
|:-----------------------------------|--------:|--------------:|
| afhubbard|hyperscaler_spot         |   0.174 |         0.186 |
| fastgpu_daily|hyperscaler_spot     |   0.001 |         0.08  |
| fastgpu_daily|neocloud_rate_card   |   0.05  |         0.149 |
| fastgpu_daily|neocloud_spot        |   0.008 |         0.229 |
| gpurentalprices|marketplace_ask    |   0.179 |         0.122 |
| gpurentalprices|neocloud_rate_card |   0.09  |         0.129 |

## Mean ensemble weight by group
| group                              |   drift |   step_hazard |
|:-----------------------------------|--------:|--------------:|
| afhubbard|hyperscaler_spot         |    0.21 |          0.79 |
| fastgpu_daily|hyperscaler_spot     |    0.2  |          0.8  |
| fastgpu_daily|neocloud_rate_card   |    0.02 |          0.98 |
| fastgpu_daily|neocloud_spot        |    0.28 |          0.72 |
| gpurentalprices|marketplace_ask    |    0.34 |          0.66 |
| gpurentalprices|neocloud_rate_card |    0.03 |          0.97 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                           | leader                                                            |   lag_days |   corr |
|:-----------------------------------------------------------------|:------------------------------------------------------------------|-----------:|-------:|
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      | gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median     |          3 | -0.924 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_rate_card.B200.serverless.median         |          3 | -0.924 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_spot.B200.spot.median                    |          1 |  0.924 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median |          2 |  0.921 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median      |          4 |  0.884 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median           |          4 |  0.865 |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | afhubbard.hyperscaler_list.B300.on_demand.median                  |          1 | -0.85  |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | fastgpu_daily.hyperscaler_list.B300.on_demand.median              |          2 | -0.85  |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median        |          1 |  0.805 |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     | afhubbard.neocloud_spot.L40S.spot.median                          |          1 |  0.797 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  |          1 |  0.778 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median |          3 |  0.762 |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     | afhubbard.neocloud_rate_card.L40S.on_demand.median                |          1 |  0.746 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median       |          5 |  0.71  |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median      |          5 |  0.705 |
