# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1048; truth above q50 in 48% of cells (50% if unbiased); above q90 11% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |  -0.366 |         0.229 |       0.034 |       0.159 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.099 |         0.211 |       0.05  |       0.267 |             -0.017 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.157 |         0.551 |       0.135 |       0.11  |              0.005 |
| fastgpu_daily|neocloud_spot        |  630 |  -0.064 |         0.429 |       0.076 |       0.078 |              0.011 |
| gpurentalprices|marketplace_ask    |   89 |   0.105 |         0.292 |       0.045 |       0.045 |              0.011 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.124 |         0.587 |       0.141 |       0.076 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.069 |         0.346 |       0.122 |       0.106 |              0.003 |
|              3 | 1118 |   0.096 |         0.487 |       0.121 |       0.112 |              0.007 |
|              7 | 1105 |   0.117 |         0.599 |       0.08  |       0.099 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.172 |         0.63  |       0.129 |       0.11  |              0.011 |
| 2-3          |  408 |   0.021 |         0.387 |       0.12  |       0.088 |              0.009 |
| 4-7          |  407 |   0.108 |         0.4   |       0.069 |       0.108 |              0.011 |
| 8-30         |  613 |  -0.202 |         0.232 |       0.077 |       0.131 |              0.002 |
| >30          |  171 |  -0.108 |         0.193 |       0.058 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |  -0.014 |         0.44  |       0.071 |       0.107 |              0.009 |
| more          |  583 |   0.166 |         0.569 |       0.087 |       0.069 |              0.013 |
| same          | 2590 |   0.089 |         0.459 |       0.114 |       0.114 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  96 |   -3.985 |         0     |       0     |       0.083 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  90 |   -1.242 |         0.289 |       0.033 |       0.033 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  89 |   -1.21  |         0.258 |       0.022 |       0.371 |             -0.003 |
| afhubbard.hyperscaler_spot.T4.spot.median                       |  96 |   -0.624 |         0.438 |       0.073 |       0.271 |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  89 |   -0.553 |         0.371 |       0.034 |       0.022 |              0.006 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  89 |   -0.524 |         0.652 |       0.169 |       0.034 |              0.007 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median           |  90 |   -0.443 |         0.233 |       0     |       0     |              0.007 |

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
| afhubbard|hyperscaler_spot         |     0.5 |      0.5 |
| fastgpu_daily|hyperscaler_spot     |     0.5 |      0.5 |
| fastgpu_daily|neocloud_rate_card   |     0.5 |      0.5 |
| fastgpu_daily|neocloud_spot        |     0.5 |      0.5 |
| gpurentalprices|marketplace_ask    |     0.5 |      0.5 |
| gpurentalprices|neocloud_rate_card |     0.5 |      0.5 |

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
