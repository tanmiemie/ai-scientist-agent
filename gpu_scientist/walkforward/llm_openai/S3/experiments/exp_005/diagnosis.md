# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1383; truth above q50 in 49% of cells (50% if unbiased); above q90 12% and below q10 12% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |  -0.265 |         0.26  |       0.023 |       0.156 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.059 |         0.211 |       0.072 |       0.289 |             -0.016 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.166 |         0.563 |       0.13  |       0.129 |              0.006 |
| fastgpu_daily|neocloud_spot        |  630 |   0.034 |         0.438 |       0.083 |       0.083 |              0.011 |
| gpurentalprices|marketplace_ask    |   89 |   0.138 |         0.27  |       0.045 |       0.022 |              0.012 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.176 |         0.596 |       0.167 |       0.084 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.073 |         0.38  |       0.123 |       0.131 |              0.003 |
|              3 | 1118 |   0.164 |         0.489 |       0.102 |       0.115 |              0.007 |
|              7 | 1105 |   0.139 |         0.596 |       0.12  |       0.099 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.188 |         0.639 |       0.126 |       0.121 |              0.011 |
| 2-3          |  408 |   0.06  |         0.409 |       0.135 |       0.086 |              0.009 |
| 4-7          |  407 |   0.145 |         0.4   |       0.069 |       0.135 |              0.011 |
| 8-30         |  613 |  -0.078 |         0.243 |       0.103 |       0.134 |              0.002 |
| >30          |  171 |   0.044 |         0.228 |       0.111 |       0.006 |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |  -0.024 |         0.423 |       0.06  |       0.107 |              0.009 |
| more          |  583 |   0.126 |         0.578 |       0.058 |       0.106 |              0.014 |
| same          | 2590 |   0.157 |         0.472 |       0.132 |       0.117 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  96 |   -3.902 |         0.094 |       0     |       0.177 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  90 |   -0.79  |         0.322 |       0.022 |       0.078 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  89 |   -0.773 |         0.258 |       0.022 |       0.315 |             -0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  89 |   -0.353 |         0.697 |       0.191 |       0.045 |              0.007 |
| afhubbard.hyperscaler_spot.T4.spot.median                       |  96 |   -0.348 |         0.448 |       0.021 |       0.24  |              0     |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median           |  90 |   -0.304 |         0.256 |       0.022 |       0.044 |              0.007 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  89 |   -0.19  |         0.371 |       0.022 |       0.022 |              0.006 |

## Each base model alone: skill by group
| group                              |   drift |   leader |
|:-----------------------------------|--------:|---------:|
| afhubbard|hyperscaler_spot         |   0.174 |    0.115 |
| fastgpu_daily|hyperscaler_spot     |   0.001 |    0.105 |
| fastgpu_daily|neocloud_rate_card   |   0.05  |    0.166 |
| fastgpu_daily|neocloud_spot        |   0.008 |    0.25  |
| gpurentalprices|marketplace_ask    |   0.179 |    0.194 |
| gpurentalprices|neocloud_rate_card |   0.09  |    0.152 |

## Mean ensemble weight by group
| group                              |   drift |   leader |
|:-----------------------------------|--------:|---------:|
| afhubbard|hyperscaler_spot         |    0.03 |     0.97 |
| fastgpu_daily|hyperscaler_spot     |    0.03 |     0.97 |
| fastgpu_daily|neocloud_rate_card   |    0.03 |     0.97 |
| fastgpu_daily|neocloud_spot        |    0.03 |     0.97 |
| gpurentalprices|marketplace_ask    |    0.04 |     0.96 |
| gpurentalprices|neocloud_rate_card |    0.04 |     0.96 |

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
