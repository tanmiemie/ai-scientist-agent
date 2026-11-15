# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1342; truth above q50 in 45% of cells (50% if unbiased); above q90 31% and below q10 12% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.129 |         0.223 |       0.053 |       0.177 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.037 |         0.261 |       0.145 |       0.239 |             -0.002 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.144 |         0.519 |       0.353 |       0.132 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.145 |         0.383 |       0.321 |       0.124 |              0.01  |
| gpurentalprices|marketplace_ask    |  74 |   0.083 |         0.243 |       0.054 |       0.027 |             -0.018 |
| gpurentalprices|neocloud_rate_card | 888 |   0.133 |         0.553 |       0.408 |       0.073 |              0.019 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.087 |         0.308 |       0.198 |       0.086 |              0.001 |
|              3 | 885 |   0.143 |         0.459 |       0.299 |       0.118 |              0.006 |
|              7 | 872 |   0.14  |         0.587 |       0.442 |       0.153 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.163 |         0.585 |       0.399 |       0.117 |              0.01  |
| 2-3          |  376 |   0.104 |         0.404 |       0.255 |       0.08  |              0.01  |
| 4-7          |  284 |   0.127 |         0.43  |       0.232 |       0.127 |              0.009 |
| 8-30         |  489 |   0.018 |         0.202 |       0.192 |       0.184 |              0.001 |
| >30          |  150 |   0     |         0.22  |       0.22  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.026 |         0.43  |       0.311 |       0.141 |              0.008 |
| more          |  394 |   0.22  |         0.538 |       0.302 |       0.074 |              0.014 |
| same          | 2113 |   0.115 |         0.436 |       0.314 |       0.125 |              0.007 |

## Worst series
| series_id                                                     |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median              |  75 |  -1.042 |         0     |       0     |       0.147 |             -0.003 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                 |  69 |  -0.002 |         0.261 |       0.159 |       0.217 |              0.004 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median |  74 |   0.012 |         0.541 |       0.324 |       0     |              0.068 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median   |  69 |   0.037 |         0.116 |       0.101 |       0.116 |             -0.001 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median   |  69 |   0.039 |         0.681 |       0.435 |       0.159 |             -0.009 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median          |  69 |   0.04  |         0.261 |       0.13  |       0.261 |             -0.008 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median |  74 |   0.055 |         0.378 |       0.243 |       0.176 |              0.015 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median      |  74 |   0.072 |         0.284 |       0.284 |       0     |              0.006 |

## Each base model alone: skill by group
| group                              |   drift |   momentum |
|:-----------------------------------|--------:|-----------:|
| afhubbard|hyperscaler_spot         |   0.169 |      0.05  |
| fastgpu_daily|hyperscaler_spot     |  -0.03  |      0.039 |
| fastgpu_daily|neocloud_rate_card   |   0.023 |      0.18  |
| fastgpu_daily|neocloud_spot        |  -0     |      0.221 |
| gpurentalprices|marketplace_ask    |   0.097 |      0.067 |
| gpurentalprices|neocloud_rate_card |   0.073 |      0.163 |

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
