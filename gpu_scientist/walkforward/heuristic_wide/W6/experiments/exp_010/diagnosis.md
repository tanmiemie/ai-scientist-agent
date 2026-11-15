# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.2087; truth above q50 in 47% of cells (50% if unbiased); above q90 13% and below q10 9% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.103 |         0.229 |       0.052 |       0.057 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.15  |         0.194 |       0.117 |       0.25  |             -0.016 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.204 |         0.553 |       0.131 |       0.117 |              0.006 |
| fastgpu_daily|neocloud_spot        |  630 |   0.26  |         0.43  |       0.14  |       0.095 |              0.011 |
| gpurentalprices|marketplace_ask    |   89 |   0.188 |         0.27  |       0.09  |       0.022 |              0.012 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.222 |         0.576 |       0.163 |       0.06  |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.092 |         0.346 |       0.113 |       0.091 |              0.003 |
|              3 | 1118 |   0.171 |         0.48  |       0.115 |       0.092 |              0.008 |
|              7 | 1105 |   0.252 |         0.594 |       0.168 |       0.094 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.242 |         0.631 |       0.138 |       0.092 |              0.011 |
| 2-3          |  408 |   0.138 |         0.38  |       0.115 |       0.064 |              0.009 |
| 4-7          |  407 |   0.214 |         0.373 |       0.113 |       0.093 |              0.011 |
| 8-30         |  613 |   0.084 |         0.23  |       0.142 |       0.139 |              0.002 |
| >30          |  171 |   0.101 |         0.193 |       0.123 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.114 |         0.423 |       0.083 |       0.101 |              0.009 |
| more          |  583 |   0.21  |         0.554 |       0.084 |       0.077 |              0.014 |
| same          | 2590 |   0.216 |         0.458 |       0.146 |       0.095 |              0.008 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  96 |   -1.733 |         0     |       0     |       0.042 |             -0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  89 |   -0.227 |         0.258 |       0.011 |       0.191 |             -0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median         |  89 |   -0.088 |         0.652 |       0.169 |       0.022 |              0.007 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  90 |   -0.068 |         0.289 |       0.033 |       0.056 |              0.003 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  89 |    0.011 |         0.461 |       0.169 |       0     |              0.057 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median            |  90 |    0.036 |         0.233 |       0.133 |       0     |              0.007 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  90 |    0.041 |         0.144 |       0.011 |       0.211 |             -0.017 |

## Each base model alone: skill by group
| group                              |   trend_tail |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |        0.111 |
| fastgpu_daily|hyperscaler_spot     |        0.105 |
| fastgpu_daily|neocloud_rate_card   |        0.166 |
| fastgpu_daily|neocloud_spot        |        0.246 |
| gpurentalprices|marketplace_ask    |        0.188 |
| gpurentalprices|neocloud_rate_card |        0.154 |

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
