# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.175; truth above q50 in 46% of cells (50% if unbiased); above q90 12% and below q10 9% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.026 |         0.227 |       0.073 |       0.04  |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.153 |         0.261 |       0.123 |       0.123 |             -0.001 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.183 |         0.544 |       0.092 |       0.116 |              0.004 |
| fastgpu_daily|neocloud_spot        | 483 |   0.205 |         0.387 |       0.153 |       0.135 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.105 |         0.243 |       0.027 |       0.027 |             -0.014 |
| gpurentalprices|neocloud_rate_card | 888 |   0.184 |         0.564 |       0.139 |       0.073 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.043 |         0.32  |       0.113 |       0.098 |              0.003 |
|              3 | 885 |   0.152 |         0.473 |       0.107 |       0.088 |              0.008 |
|              7 | 872 |   0.213 |         0.597 |       0.13  |       0.096 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.209 |         0.608 |       0.116 |       0.088 |              0.012 |
| 2-3          |  376 |   0.14  |         0.404 |       0.122 |       0.072 |              0.01  |
| 4-7          |  284 |   0.189 |         0.43  |       0.116 |       0.077 |              0.009 |
| 8-30         |  489 |   0.003 |         0.202 |       0.131 |       0.168 |              0.001 |
| >30          |  150 |   0.08  |         0.22  |       0.06  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.053 |         0.43  |       0.067 |       0.111 |              0.009 |
| more          |  394 |   0.17  |         0.566 |       0.048 |       0.079 |              0.015 |
| same          | 2113 |   0.188 |         0.446 |       0.133 |       0.096 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -1.594 |         0     |       0     |       0.013 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -1.181 |         0.261 |       0     |       0.014 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.948 |         0.176 |       0.027 |       0.378 |             -0.004 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  69 |   -0.449 |         0.797 |       0.101 |       0.043 |              0.006 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   -0.363 |         0.284 |       0.014 |       0     |              0.006 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.343 |         0.676 |       0.189 |       0.027 |              0.008 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  74 |   -0.209 |         0.473 |       0.122 |       0     |              0.009 |

## Each base model alone: skill by group
| group                              |   drift |   leader |
|:-----------------------------------|--------:|---------:|
| afhubbard|hyperscaler_spot         |   0.169 |    0.127 |
| fastgpu_daily|hyperscaler_spot     |  -0.03  |    0.107 |
| fastgpu_daily|neocloud_rate_card   |   0.023 |    0.169 |
| fastgpu_daily|neocloud_spot        |  -0     |    0.209 |
| gpurentalprices|marketplace_ask    |   0.097 |    0.113 |
| gpurentalprices|neocloud_rate_card |   0.073 |    0.142 |

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
