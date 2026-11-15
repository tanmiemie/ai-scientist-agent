# Diagnosis (dev origins only)

Cells: 3256. Overall skill 0.1677; truth above q50 in 47% of cells (50% if unbiased); above q90 25% and below q10 11% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  372 |   0.113 |         0.223 |       0.04  |       0.134 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  174 |   0.095 |         0.19  |       0.115 |       0.287 |             -0.015 |
| fastgpu_daily|neocloud_rate_card   |  957 |   0.172 |         0.554 |       0.251 |       0.127 |              0.006 |
| fastgpu_daily|neocloud_spot        |  609 |   0.241 |         0.424 |       0.259 |       0.099 |              0.011 |
| gpurentalprices|marketplace_ask    |   88 |   0.191 |         0.273 |       0.091 |       0.023 |              0.014 |
| gpurentalprices|neocloud_rate_card | 1056 |   0.151 |         0.576 |       0.342 |       0.07  |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1094 |   0.099 |         0.342 |       0.144 |       0.084 |              0.003 |
|              3 | 1081 |   0.168 |         0.479 |       0.25  |       0.11  |              0.008 |
|              7 | 1081 |   0.182 |         0.596 |       0.347 |       0.136 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1685 |   0.195 |         0.63  |       0.32  |       0.113 |              0.012 |
| 2-3          |  405 |   0.121 |         0.378 |       0.153 |       0.062 |              0.009 |
| 4-7          |  398 |   0.189 |         0.382 |       0.148 |       0.118 |              0.011 |
| 8-30         |  600 |   0.049 |         0.228 |       0.182 |       0.158 |              0.002 |
| >30          |  168 |   0     |         0.196 |       0.196 |       0     |              0.014 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.103 |         0.423 |       0.232 |       0.101 |              0.009 |
| more          |  554 |   0.212 |         0.558 |       0.229 |       0.083 |              0.015 |
| same          | 2534 |   0.156 |         0.456 |       0.251 |       0.116 |              0.008 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  93 |  -1.817 |         0     |       0     |       0.118 |             -0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  88 |  -0.032 |         0.466 |       0.17  |       0     |              0.058 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median      |  87 |   0.042 |         0.678 |       0.345 |       0.184 |             -0.011 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    |  88 |   0.047 |         0.307 |       0.239 |       0.148 |              0.013 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  87 |   0.095 |         0.218 |       0.103 |       0.391 |             -0.022 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                    |  87 |   0.099 |         0.161 |       0.126 |       0.184 |             -0.008 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median      |  87 |   0.104 |         0.184 |       0.069 |       0.092 |              0.002 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  87 |   0.106 |         0.149 |       0.034 |       0.218 |             -0.017 |

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
