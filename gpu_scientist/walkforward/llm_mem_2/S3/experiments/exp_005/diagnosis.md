# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1759; truth above q50 in 46% of cells (50% if unbiased); above q90 10% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |  -0.035 |         0.227 |       0.076 |       0.049 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.188 |         0.194 |       0.1   |       0.194 |             -0.017 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.184 |         0.531 |       0.081 |       0.133 |              0.005 |
| fastgpu_daily|neocloud_spot        |  630 |   0.204 |         0.427 |       0.119 |       0.137 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.181 |         0.258 |       0.079 |       0.022 |              0.009 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.176 |         0.566 |       0.125 |       0.059 |              0.018 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.011 |         0.334 |       0.114 |       0.109 |              0.002 |
|              3 | 1118 |   0.157 |         0.47  |       0.092 |       0.097 |              0.006 |
|              7 | 1105 |   0.22  |         0.585 |       0.101 |       0.097 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.211 |         0.611 |       0.103 |       0.124 |              0.009 |
| 2-3          |  408 |   0.094 |         0.38  |       0.1   |       0.039 |              0.009 |
| 4-7          |  407 |   0.208 |         0.373 |       0.098 |       0.066 |              0.011 |
| 8-30         |  613 |   0.023 |         0.23  |       0.116 |       0.127 |              0.002 |
| >30          |  171 |   0.021 |         0.193 |       0.058 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.073 |         0.423 |       0.065 |       0.095 |              0.008 |
| more          |  583 |   0.184 |         0.535 |       0.055 |       0.12  |              0.013 |
| same          | 2590 |   0.181 |         0.449 |       0.115 |       0.097 |              0.007 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  96 |   -2.351 |         0     |       0     |       0.042 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  90 |   -1.018 |         0.289 |       0     |       0.056 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  89 |   -0.854 |         0.258 |       0.034 |       0.18  |             -0.003 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  89 |   -0.354 |         0.36  |       0.022 |       0.011 |              0.005 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  89 |   -0.353 |         0.652 |       0.135 |       0.034 |              0.006 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median           |  90 |   -0.075 |         0.233 |       0.1   |       0.067 |              0.006 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median     |  90 |   -0.04  |         0.478 |       0.078 |       0.167 |             -0.013 |

## Each base model alone: skill by group
| group                              |   leader |   momentum |
|:-----------------------------------|---------:|-----------:|
| afhubbard|hyperscaler_spot         |    0.115 |      0.041 |
| fastgpu_daily|hyperscaler_spot     |    0.105 |      0.072 |
| fastgpu_daily|neocloud_rate_card   |    0.166 |      0.174 |
| fastgpu_daily|neocloud_spot        |    0.25  |      0.275 |
| gpurentalprices|marketplace_ask    |    0.194 |      0.161 |
| gpurentalprices|neocloud_rate_card |    0.152 |      0.173 |

## Mean ensemble weight by group
| group                              |   leader |   momentum |
|:-----------------------------------|---------:|-----------:|
| afhubbard|hyperscaler_spot         |      0.5 |        0.5 |
| fastgpu_daily|hyperscaler_spot     |      0.5 |        0.5 |
| fastgpu_daily|neocloud_rate_card   |      0.5 |        0.5 |
| fastgpu_daily|neocloud_spot        |      0.5 |        0.5 |
| gpurentalprices|marketplace_ask    |      0.5 |        0.5 |
| gpurentalprices|neocloud_rate_card |      0.5 |        0.5 |

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
