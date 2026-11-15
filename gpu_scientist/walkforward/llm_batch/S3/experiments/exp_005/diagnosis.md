# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1668; truth above q50 in 46% of cells (50% if unbiased); above q90 18% and below q10 13% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.107 |         0.25  |       0.055 |       0.112 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.142 |         0.228 |       0.128 |       0.3   |             -0.018 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.167 |         0.527 |       0.192 |       0.148 |              0.004 |
| fastgpu_daily|neocloud_spot        |  630 |   0.254 |         0.425 |       0.171 |       0.141 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.149 |         0.27  |       0.112 |       0.067 |              0.006 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.155 |         0.561 |       0.229 |       0.08  |              0.017 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.085 |         0.341 |       0.121 |       0.129 |              0.001 |
|              3 | 1118 |   0.139 |         0.47  |       0.148 |       0.12  |              0.006 |
|              7 | 1105 |   0.198 |         0.582 |       0.269 |       0.132 |              0.016 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.21  |         0.597 |       0.184 |       0.151 |              0.007 |
| 2-3          |  408 |   0.082 |         0.392 |       0.164 |       0.061 |              0.009 |
| 4-7          |  407 |   0.154 |         0.408 |       0.15  |       0.103 |              0.011 |
| 8-30         |  613 |   0.027 |         0.24  |       0.181 |       0.152 |              0.002 |
| >30          |  171 |  -0     |         0.216 |       0.216 |       0.006 |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.145 |         0.423 |       0.202 |       0.125 |              0.007 |
| more          |  583 |   0.167 |         0.525 |       0.149 |       0.136 |              0.011 |
| same          | 2590 |   0.168 |         0.453 |       0.184 |       0.125 |              0.007 |

## Worst series
| series_id                                                       |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  96 |  -1.372 |         0.083 |       0.021 |       0.104 |             -0.003 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  89 |  -0.161 |         0.438 |       0.292 |       0.056 |              0.056 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median   |  89 |  -0.04  |         0.326 |       0.213 |       0.034 |              0.012 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median           |  90 |  -0.037 |         0.233 |       0.156 |       0.1   |              0.005 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  90 |   0     |         0.322 |       0.167 |       0.1   |              0.002 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  90 |   0.004 |         0.233 |       0.133 |       0.189 |             -0.011 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median     |  90 |   0.049 |         0.489 |       0.178 |       0.156 |             -0.013 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  89 |   0.058 |         0.326 |       0.247 |       0.09  |              0.005 |

## Each base model alone: skill by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |   0.174 |      0.052 |
| fastgpu_daily|hyperscaler_spot     |   0.001 |      0.107 |
| fastgpu_daily|neocloud_rate_card   |   0.05  |      0.172 |
| fastgpu_daily|neocloud_spot        |   0.008 |      0.271 |
| gpurentalprices|marketplace_ask    |   0.179 |      0.12  |
| gpurentalprices|neocloud_rate_card |   0.09  |      0.162 |

## Mean ensemble weight by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |    0.41 |       0.59 |
| fastgpu_daily|hyperscaler_spot     |    0.3  |       0.7  |
| fastgpu_daily|neocloud_rate_card   |    0.11 |       0.89 |
| fastgpu_daily|neocloud_spot        |    0.32 |       0.68 |
| gpurentalprices|marketplace_ask    |    0.38 |       0.62 |
| gpurentalprices|neocloud_rate_card |    0.1  |       0.9  |

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
