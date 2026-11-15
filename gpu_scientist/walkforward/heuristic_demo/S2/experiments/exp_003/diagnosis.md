# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1809; truth above q50 in 43% of cells (50% if unbiased); above q90 13% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |  -0.033 |         0.227 |       0.067 |       0.043 |             -0.002 |
| fastgpu_daily|hyperscaler_spot     | 138 |   0.098 |         0.217 |       0.145 |       0.188 |             -0.003 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.215 |         0.489 |       0.123 |       0.137 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.155 |         0.373 |       0.143 |       0.18  |              0.009 |
| gpurentalprices|marketplace_ask    |  74 |   0.068 |         0.203 |       0.041 |       0.027 |             -0.02  |
| gpurentalprices|neocloud_rate_card | 888 |   0.187 |         0.532 |       0.146 |       0.054 |              0.018 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |  -0.002 |         0.284 |       0.112 |       0.115 |              0     |
|              3 | 885 |   0.106 |         0.438 |       0.116 |       0.103 |              0.005 |
|              7 | 872 |   0.255 |         0.57  |       0.153 |       0.1   |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.207 |         0.555 |       0.121 |       0.117 |              0.008 |
| 2-3          |  376 |   0.134 |         0.388 |       0.122 |       0.051 |              0.01  |
| 4-7          |  284 |   0.201 |         0.394 |       0.127 |       0.085 |              0.009 |
| 8-30         |  489 |   0.074 |         0.202 |       0.153 |       0.164 |              0.001 |
| >30          |  150 |   0.046 |         0.22  |       0.1   |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.076 |         0.393 |       0.081 |       0.119 |              0.007 |
| more          |  394 |   0.147 |         0.475 |       0.063 |       0.089 |              0.013 |
| same          | 2113 |   0.202 |         0.424 |       0.142 |       0.108 |              0.007 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  69 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |   -1.906 |         0     |       0     |       0.053 |             -0.004 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  74 |   -0.484 |         0.176 |       0.014 |       0.135 |             -0.004 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |   -0.359 |         0.261 |       0.029 |       0.072 |              0.002 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  74 |   -0.132 |         0.676 |       0.203 |       0.027 |              0.006 |
| fastgpu_daily.neocloud_spot.H200.spot.median                    |  69 |   -0.107 |         0.348 |       0.116 |       0.087 |              0.004 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  74 |   -0.103 |         0.284 |       0     |       0     |              0.005 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median        |  74 |   -0.101 |         0.432 |       0.149 |       0.027 |              0.007 |

## Each base model alone: skill by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.05  |
| fastgpu_daily|hyperscaler_spot     |      0.039 |
| fastgpu_daily|neocloud_rate_card   |      0.18  |
| fastgpu_daily|neocloud_spot        |      0.221 |
| gpurentalprices|marketplace_ask    |      0.067 |
| gpurentalprices|neocloud_rate_card |      0.163 |

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
