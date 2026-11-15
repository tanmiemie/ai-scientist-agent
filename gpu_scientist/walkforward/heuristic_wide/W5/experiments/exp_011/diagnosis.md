# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1865; truth above q50 in 46% of cells (50% if unbiased); above q90 15% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.151 |         0.227 |       0.063 |       0.053 |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.138 |         0.239 |       0.145 |       0.188 |             -0     |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.165 |         0.545 |       0.144 |       0.123 |              0.005 |
| fastgpu_daily|neocloud_spot        | 483 |   0.219 |         0.387 |       0.168 |       0.124 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.099 |         0.216 |       0.041 |       0.068 |             -0.012 |
| gpurentalprices|neocloud_rate_card | 888 |   0.224 |         0.553 |       0.177 |       0.057 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.082 |         0.32  |       0.111 |       0.09  |              0.003 |
|              3 | 885 |   0.132 |         0.467 |       0.121 |       0.095 |              0.008 |
|              7 | 872 |   0.235 |         0.588 |       0.211 |       0.1   |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.216 |         0.608 |       0.145 |       0.085 |              0.012 |
| 2-3          |  376 |   0.148 |         0.396 |       0.125 |       0.066 |              0.01  |
| 4-7          |  284 |   0.175 |         0.394 |       0.148 |       0.092 |              0.009 |
| 8-30         |  489 |   0.071 |         0.202 |       0.174 |       0.176 |              0.001 |
| >30          |  150 |   0.147 |         0.22  |       0.133 |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.112 |         0.407 |       0.096 |       0.126 |              0.009 |
| more          |  394 |   0.123 |         0.543 |       0.081 |       0.076 |              0.016 |
| same          | 2113 |   0.215 |         0.445 |       0.163 |       0.097 |              0.009 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -0.726 |         0     |       0     |       0.093 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.17  |         0.176 |       0.014 |       0.203 |             -0.004 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |   -0.091 |         0.203 |       0.159 |       0.145 |              0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -0.022 |         0.261 |       0.072 |       0.072 |              0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.012 |         0.676 |       0.189 |       0.041 |              0.008 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |    0.043 |         0.554 |       0.243 |       0     |              0.069 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  74 |    0.045 |         0.473 |       0.216 |       0     |              0.009 |

## Each base model alone: skill by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.171 |
| fastgpu_daily|hyperscaler_spot     |      0.103 |
| fastgpu_daily|neocloud_rate_card   |      0.134 |
| fastgpu_daily|neocloud_spot        |      0.2   |
| gpurentalprices|marketplace_ask    |      0.102 |
| gpurentalprices|neocloud_rate_card |      0.16  |

## Mean ensemble weight by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |          1 |
| fastgpu_daily|hyperscaler_spot     |          1 |
| fastgpu_daily|neocloud_rate_card   |          1 |
| fastgpu_daily|neocloud_spot        |          1 |
| gpurentalprices|marketplace_ask    |          1 |
| gpurentalprices|neocloud_rate_card |          1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                           | leader                                                                  |   lag_days |   corr |
|:-----------------------------------------------------------------|:------------------------------------------------------------------------|-----------:|-------:|
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_rate_card.B200.serverless.median               |          3 | -0.974 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_spot.B200.spot.median                          |          1 |  0.974 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      | gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median           |          3 | -0.956 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median       |          2 |  0.933 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median                 |          4 |  0.868 |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median              |          1 |  0.86  |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | afhubbard.hyperscaler_list.B300.on_demand.median                        |          1 | -0.856 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median        |          1 |  0.787 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 | fastgpu_daily.neocloud_spot.A100_40GB.spot.median                       |          1 | -0.764 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median       |          3 |  0.761 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    | fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median             |          1 | -0.724 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median         | afhubbard.neocloud_rate_card.B300.on_demand.median                      |          1 |  0.713 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median    | gpurentalprices_cheapest.aggregator_cheapest.RTX_A6000.on_demand.median |          2 | -0.712 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median             |          5 |  0.711 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      | gpurentalprices_cheapest.aggregator_cheapest.RTX_A6000.on_demand.median |          5 |  0.705 |
