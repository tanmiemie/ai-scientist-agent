# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1747; truth above q50 in 48% of cells (50% if unbiased); above q90 11% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.056 |         0.242 |       0.076 |       0.047 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.222 |         0.217 |       0.133 |       0.206 |             -0.016 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.174 |         0.559 |       0.083 |       0.114 |              0.006 |
| fastgpu_daily|neocloud_spot        |  630 |   0.215 |         0.438 |       0.122 |       0.149 |              0.011 |
| gpurentalprices|marketplace_ask    |   89 |   0.193 |         0.27  |       0.067 |       0.022 |              0.012 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.169 |         0.592 |       0.132 |       0.072 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.087 |         0.37  |       0.125 |       0.123 |              0.003 |
|              3 | 1118 |   0.163 |         0.484 |       0.095 |       0.097 |              0.007 |
|              7 | 1105 |   0.199 |         0.599 |       0.102 |       0.086 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.205 |         0.638 |       0.11  |       0.099 |              0.011 |
| 2-3          |  408 |   0.117 |         0.4   |       0.108 |       0.069 |              0.009 |
| 4-7          |  407 |   0.208 |         0.381 |       0.096 |       0.079 |              0.011 |
| 8-30         |  613 |   0.023 |         0.24  |       0.119 |       0.175 |              0.002 |
| >30          |  171 |   0.05  |         0.24  |       0.064 |       0.006 |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.085 |         0.429 |       0.065 |       0.083 |              0.009 |
| more          |  583 |   0.171 |         0.566 |       0.051 |       0.093 |              0.014 |
| same          | 2590 |   0.184 |         0.469 |       0.123 |       0.105 |              0.008 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  96 |   -1.906 |         0.042 |       0.01  |       0.042 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  90 |   -1.021 |         0.322 |       0.011 |       0.022 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  89 |   -0.986 |         0.258 |       0.022 |       0.326 |             -0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median         |  89 |   -0.416 |         0.663 |       0.169 |       0.056 |              0.007 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  89 |   -0.384 |         0.371 |       0.022 |       0.011 |              0.006 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      |  90 |   -0.052 |         0.489 |       0.089 |       0.133 |             -0.012 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  90 |   -0.041 |         0.144 |       0     |       0.2   |             -0.017 |

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
| afhubbard|hyperscaler_spot         |    0.33 |     0.67 |
| fastgpu_daily|hyperscaler_spot     |    0.33 |     0.67 |
| fastgpu_daily|neocloud_rate_card   |    0.01 |     0.99 |
| fastgpu_daily|neocloud_spot        |    0.23 |     0.77 |
| gpurentalprices|marketplace_ask    |    0.34 |     0.66 |
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
