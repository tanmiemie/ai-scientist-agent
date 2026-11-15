# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1792; truth above q50 in 43% of cells (50% if unbiased); above q90 19% and below q10 13% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.104 |         0.24  |       0.039 |       0.107 |             -0.003 |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.096 |         0.222 |       0.133 |       0.289 |             -0.019 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.168 |         0.472 |       0.196 |       0.161 |              0.002 |
| fastgpu_daily|neocloud_spot        |  630 |   0.273 |         0.414 |       0.181 |       0.138 |              0.009 |
| gpurentalprices|marketplace_ask    |   89 |   0.163 |         0.258 |       0.067 |       0.022 |              0.005 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.19  |         0.526 |       0.25  |       0.098 |              0.016 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.081 |         0.298 |       0.126 |       0.139 |              0     |
|              3 | 1118 |   0.181 |         0.432 |       0.166 |       0.134 |              0.004 |
|              7 | 1105 |   0.198 |         0.569 |       0.265 |       0.128 |              0.014 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.214 |         0.542 |       0.194 |       0.158 |              0.005 |
| 2-3          |  408 |   0.109 |         0.382 |       0.174 |       0.056 |              0.009 |
| 4-7          |  407 |   0.182 |         0.398 |       0.157 |       0.111 |              0.011 |
| 8-30         |  613 |   0.055 |         0.237 |       0.179 |       0.162 |              0.002 |
| >30          |  171 |  -0     |         0.216 |       0.216 |       0.018 |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.125 |         0.411 |       0.214 |       0.125 |              0.006 |
| more          |  583 |   0.172 |         0.484 |       0.172 |       0.146 |              0.009 |
| same          | 2590 |   0.187 |         0.422 |       0.187 |       0.131 |              0.005 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  96 |  -1.211 |         0.062 |       0     |       0.125 |             -0.003 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median            |  90 |  -0.048 |         0.233 |       0.144 |       0.078 |              0.004 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  89 |  -0.047 |         0.36  |       0.315 |       0.079 |              0.054 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  90 |  -0.019 |         0.1   |       0.033 |       0.256 |             -0.028 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  90 |   0.004 |         0.267 |       0.144 |       0.122 |              0.002 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    |  89 |   0.026 |         0.315 |       0.213 |       0.034 |              0.012 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  89 |   0.047 |         0.303 |       0.247 |       0.112 |              0.004 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                    |  90 |   0.05  |         0.222 |       0.144 |       0.189 |             -0.011 |

## Each base model alone: skill by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |   0.174 |     -0.034 |
| fastgpu_daily|hyperscaler_spot     |   0.001 |      0.038 |
| fastgpu_daily|neocloud_rate_card   |   0.05  |      0.17  |
| fastgpu_daily|neocloud_spot        |   0.008 |      0.286 |
| gpurentalprices|marketplace_ask    |   0.179 |      0.124 |
| gpurentalprices|neocloud_rate_card |   0.09  |      0.185 |

## Mean ensemble weight by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |    0.52 |       0.48 |
| fastgpu_daily|hyperscaler_spot     |    0.35 |       0.65 |
| fastgpu_daily|neocloud_rate_card   |    0.15 |       0.85 |
| fastgpu_daily|neocloud_spot        |    0.41 |       0.59 |
| gpurentalprices|marketplace_ask    |    0.64 |       0.36 |
| gpurentalprices|neocloud_rate_card |    0.17 |       0.83 |

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
