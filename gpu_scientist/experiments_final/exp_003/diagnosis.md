# Diagnosis (dev origins only)

Cells: 3256. Overall skill 0.1768; truth above q50 in 50% of cells (50% if unbiased); above q90 12% and below q10 12% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  372 |   0.067 |         0.293 |       0.099 |       0.081 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  174 |   0.133 |         0.31  |       0.132 |       0.247 |             -0.013 |
| fastgpu_daily|neocloud_rate_card   |  957 |   0.182 |         0.538 |       0.122 |       0.138 |              0.006 |
| fastgpu_daily|neocloud_spot        |  609 |   0.224 |         0.452 |       0.148 |       0.141 |              0.011 |
| gpurentalprices|marketplace_ask    |   88 |   0.162 |         0.42  |       0.068 |       0.023 |              0.013 |
| gpurentalprices|neocloud_rate_card | 1056 |   0.176 |         0.611 |       0.126 |       0.1   |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1094 |   0.088 |         0.385 |       0.13  |       0.142 |              0.003 |
|              3 | 1081 |   0.117 |         0.511 |       0.11  |       0.12  |              0.008 |
|              7 | 1081 |   0.227 |         0.612 |       0.134 |       0.105 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1685 |   0.21  |         0.643 |       0.123 |       0.108 |              0.011 |
| 2-3          |  405 |   0.098 |         0.43  |       0.111 |       0.116 |              0.009 |
| 4-7          |  398 |   0.194 |         0.425 |       0.121 |       0.158 |              0.011 |
| 8-30         |  600 |   0.057 |         0.278 |       0.157 |       0.173 |              0.002 |
| >30          |  168 |   0.015 |         0.244 |       0.071 |       0.018 |              0.014 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.107 |         0.482 |       0.083 |       0.155 |              0.009 |
| more          |  554 |   0.157 |         0.578 |       0.072 |       0.105 |              0.015 |
| same          | 2534 |   0.19  |         0.487 |       0.139 |       0.124 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  87 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  93 |   -1.85  |         0.183 |       0.086 |       0.14  |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  87 |   -0.592 |         0.345 |       0.011 |       0.115 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  88 |   -0.573 |         0.341 |       0.034 |       0.239 |             -0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  88 |   -0.216 |         0.67  |       0.136 |       0.148 |              0.007 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  88 |   -0.168 |         0.364 |       0.023 |       0.023 |              0.006 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  87 |   -0.027 |         0.184 |       0.046 |       0.092 |              0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  88 |   -0.026 |         0.466 |       0.182 |       0.136 |              0.058 |

## Each base model alone: skill by group
| group                              |   drift_30 |   step_hazard |   trend_tail |
|:-----------------------------------|-----------:|--------------:|-------------:|
| afhubbard|hyperscaler_spot         |      0.164 |         0.182 |        0.113 |
| fastgpu_daily|hyperscaler_spot     |     -0.078 |         0.071 |        0.095 |
| fastgpu_daily|neocloud_rate_card   |      0.146 |         0.152 |        0.172 |
| fastgpu_daily|neocloud_spot        |      0.209 |         0.224 |        0.241 |
| gpurentalprices|marketplace_ask    |      0.164 |         0.119 |        0.191 |
| gpurentalprices|neocloud_rate_card |      0.143 |         0.129 |        0.151 |

## Mean ensemble weight by group
| group                              |   drift_30 |   step_hazard |   trend_tail |
|:-----------------------------------|-----------:|--------------:|-------------:|
| afhubbard|hyperscaler_spot         |       0.16 |          0.18 |         0.66 |
| fastgpu_daily|hyperscaler_spot     |       0.2  |          0.2  |         0.6  |
| fastgpu_daily|neocloud_rate_card   |       0.13 |          0.18 |         0.69 |
| fastgpu_daily|neocloud_spot        |       0.25 |          0.29 |         0.46 |
| gpurentalprices|marketplace_ask    |       0.03 |          0.31 |         0.66 |
| gpurentalprices|neocloud_rate_card |       0.16 |          0.13 |         0.72 |

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
