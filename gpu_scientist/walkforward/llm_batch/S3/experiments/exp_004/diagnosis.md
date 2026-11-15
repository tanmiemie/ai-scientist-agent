# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1711; truth above q50 in 47% of cells (50% if unbiased); above q90 20% and below q10 13% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.14  |         0.253 |       0.034 |       0.107 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.121 |         0.228 |       0.122 |       0.289 |             -0.018 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.154 |         0.527 |       0.223 |       0.156 |              0.004 |
| fastgpu_daily|neocloud_spot        |  630 |   0.244 |         0.427 |       0.198 |       0.149 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.173 |         0.258 |       0.067 |       0.022 |              0.008 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.183 |         0.581 |       0.261 |       0.083 |              0.018 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.11  |         0.345 |       0.132 |       0.131 |              0.002 |
|              3 | 1118 |   0.173 |         0.479 |       0.189 |       0.126 |              0.006 |
|              7 | 1105 |   0.183 |         0.588 |       0.278 |       0.13  |              0.016 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.206 |         0.602 |       0.222 |       0.148 |              0.008 |
| 2-3          |  408 |   0.106 |         0.407 |       0.164 |       0.064 |              0.009 |
| 4-7          |  407 |   0.175 |         0.43  |       0.17  |       0.123 |              0.011 |
| 8-30         |  613 |   0.04  |         0.243 |       0.179 |       0.162 |              0.002 |
| >30          |  171 |   0     |         0.193 |       0.193 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.074 |         0.423 |       0.226 |       0.167 |              0.008 |
| more          |  583 |   0.171 |         0.552 |       0.19  |       0.144 |              0.012 |
| same          | 2590 |   0.179 |         0.455 |       0.2   |       0.124 |              0.007 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  96 |  -0.956 |         0.073 |       0.021 |       0.177 |             -0.003 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  89 |  -0.046 |         0.449 |       0.348 |       0.079 |              0.056 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median            |  90 |  -0.027 |         0.244 |       0.189 |       0.156 |              0.006 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  90 |  -0.02  |         0.356 |       0.211 |       0.1   |              0.002 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    |  89 |   0.025 |         0.461 |       0.213 |       0.034 |              0.013 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  90 |   0.047 |         0.122 |       0.078 |       0.244 |             -0.021 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  89 |   0.047 |         0.348 |       0.258 |       0.067 |              0.005 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                    |  90 |   0.055 |         0.233 |       0.122 |       0.189 |             -0.011 |

## Each base model alone: skill by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |   0.174 |      0.041 |
| fastgpu_daily|hyperscaler_spot     |   0.001 |      0.072 |
| fastgpu_daily|neocloud_rate_card   |   0.05  |      0.174 |
| fastgpu_daily|neocloud_spot        |   0.008 |      0.275 |
| gpurentalprices|marketplace_ask    |   0.179 |      0.161 |
| gpurentalprices|neocloud_rate_card |   0.09  |      0.173 |

## Mean ensemble weight by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |    0.45 |       0.55 |
| fastgpu_daily|hyperscaler_spot     |    0.29 |       0.71 |
| fastgpu_daily|neocloud_rate_card   |    0.29 |       0.71 |
| fastgpu_daily|neocloud_spot        |    0.41 |       0.59 |
| gpurentalprices|marketplace_ask    |    0.34 |       0.66 |
| gpurentalprices|neocloud_rate_card |    0.3  |       0.7  |

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
