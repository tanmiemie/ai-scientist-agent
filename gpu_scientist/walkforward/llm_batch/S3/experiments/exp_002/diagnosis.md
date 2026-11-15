# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1781; truth above q50 in 46% of cells (50% if unbiased); above q90 21% and below q10 13% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.152 |         0.227 |       0.036 |       0.109 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.122 |         0.211 |       0.117 |       0.3   |             -0.018 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.165 |         0.527 |       0.232 |       0.154 |              0.004 |
| fastgpu_daily|neocloud_spot        |  630 |   0.26  |         0.422 |       0.216 |       0.137 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.171 |         0.292 |       0.079 |       0.022 |              0.007 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.184 |         0.576 |       0.272 |       0.079 |              0.018 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.096 |         0.334 |       0.13  |       0.123 |              0.002 |
|              3 | 1118 |   0.185 |         0.473 |       0.199 |       0.125 |              0.006 |
|              7 | 1105 |   0.192 |         0.59  |       0.299 |       0.129 |              0.016 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.215 |         0.607 |       0.238 |       0.15  |              0.009 |
| 2-3          |  408 |   0.111 |         0.387 |       0.176 |       0.056 |              0.009 |
| 4-7          |  407 |   0.176 |         0.4   |       0.167 |       0.106 |              0.011 |
| 8-30         |  613 |   0.045 |         0.232 |       0.181 |       0.152 |              0.002 |
| >30          |  171 |   0     |         0.193 |       0.193 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.086 |         0.44  |       0.238 |       0.137 |              0.008 |
| more          |  583 |   0.199 |         0.547 |       0.201 |       0.141 |              0.012 |
| same          | 2590 |   0.177 |         0.448 |       0.209 |       0.122 |              0.007 |

## Worst series
| series_id                                                       |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  96 |  -1.096 |         0     |       0     |       0.115 |             -0.003 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  89 |  -0.045 |         0.449 |       0.371 |       0.079 |              0.056 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  90 |   0.014 |         0.289 |       0.178 |       0.1   |              0.003 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median           |  90 |   0.018 |         0.233 |       0.189 |       0.067 |              0.006 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median   |  89 |   0.025 |         0.427 |       0.213 |       0.034 |              0.013 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  89 |   0.055 |         0.36  |       0.27  |       0.056 |              0.005 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median     |  90 |   0.057 |         0.478 |       0.211 |       0.167 |             -0.015 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median     |  90 |   0.067 |         0.678 |       0.267 |       0.2   |             -0.011 |

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
| afhubbard|hyperscaler_spot         |     0.5 |        0.5 |
| fastgpu_daily|hyperscaler_spot     |     0.5 |        0.5 |
| fastgpu_daily|neocloud_rate_card   |     0.5 |        0.5 |
| fastgpu_daily|neocloud_spot        |     0.5 |        0.5 |
| gpurentalprices|marketplace_ask    |     0.5 |        0.5 |
| gpurentalprices|neocloud_rate_card |     0.5 |        0.5 |

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
