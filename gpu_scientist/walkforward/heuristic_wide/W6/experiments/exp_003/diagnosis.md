# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1838; truth above q50 in 45% of cells (50% if unbiased); above q90 11% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |  -0.018 |         0.227 |       0.06  |       0.049 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.156 |         0.178 |       0.117 |       0.25  |             -0.018 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.206 |         0.513 |       0.115 |       0.117 |              0.004 |
| fastgpu_daily|neocloud_spot        |  630 |   0.195 |         0.416 |       0.119 |       0.144 |              0.009 |
| gpurentalprices|marketplace_ask    |   89 |   0.164 |         0.258 |       0.079 |       0.022 |              0.005 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.177 |         0.549 |       0.13  |       0.073 |              0.017 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.029 |         0.313 |       0.113 |       0.114 |              0.001 |
|              3 | 1118 |   0.128 |         0.459 |       0.106 |       0.101 |              0.005 |
|              7 | 1105 |   0.245 |         0.575 |       0.121 |       0.1   |              0.016 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.212 |         0.584 |       0.113 |       0.125 |              0.007 |
| 2-3          |  408 |   0.111 |         0.38  |       0.11  |       0.051 |              0.009 |
| 4-7          |  407 |   0.211 |         0.373 |       0.098 |       0.076 |              0.011 |
| 8-30         |  613 |   0.071 |         0.23  |       0.134 |       0.134 |              0.002 |
| >30          |  171 |   0.014 |         0.193 |       0.088 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.096 |         0.411 |       0.077 |       0.107 |              0.007 |
| more          |  583 |   0.164 |         0.515 |       0.072 |       0.075 |              0.011 |
| same          | 2590 |   0.2   |         0.436 |       0.125 |       0.112 |              0.006 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  96 |   -2.341 |         0     |       0     |       0.042 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  89 |   -0.576 |         0.258 |       0.011 |       0.169 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  90 |   -0.463 |         0.289 |       0.022 |       0.056 |              0.002 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median         |  89 |   -0.199 |         0.652 |       0.169 |       0.034 |              0.006 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  89 |   -0.196 |         0.326 |       0.011 |       0.067 |              0.005 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median            |  90 |   -0.154 |         0.233 |       0.111 |       0.056 |              0.005 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  90 |   -0.017 |         0.1   |       0.011 |       0.189 |             -0.023 |

## Each base model alone: skill by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.041 |
| fastgpu_daily|hyperscaler_spot     |      0.072 |
| fastgpu_daily|neocloud_rate_card   |      0.174 |
| fastgpu_daily|neocloud_spot        |      0.275 |
| gpurentalprices|marketplace_ask    |      0.161 |
| gpurentalprices|neocloud_rate_card |      0.173 |

## Mean ensemble weight by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |          1 |
| fastgpu_daily|hyperscaler_spot     |          1 |
| fastgpu_daily|neocloud_rate_card   |          1 |
| fastgpu_daily|neocloud_spot        |          1 |
| gpurentalprices|marketplace_ask    |          1 |
| gpurentalprices|neocloud_rate_card |          1 |

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
