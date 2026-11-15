# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1117; truth above q50 in 46% of cells (50% if unbiased); above q90 33% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.148 |         0.207 |       0.093 |       0.21  |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 138 |  -0.115 |         0.283 |       0.217 |       0.268 |             -0.001 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.089 |         0.52  |       0.422 |       0.133 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.096 |         0.387 |       0.323 |       0.135 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.252 |         0.243 |       0.081 |       0.108 |             -0.016 |
| gpurentalprices|neocloud_rate_card | 888 |   0.131 |         0.57  |       0.386 |       0.032 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.087 |         0.316 |       0.184 |       0.066 |              0.002 |
|              3 | 885 |   0.142 |         0.467 |       0.315 |       0.108 |              0.007 |
|              7 | 872 |   0.101 |         0.589 |       0.506 |       0.17  |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.145 |         0.599 |       0.409 |       0.098 |              0.011 |
| 2-3          |  376 |   0.053 |         0.396 |       0.295 |       0.096 |              0.009 |
| 4-7          |  284 |   0.107 |         0.43  |       0.32  |       0.158 |              0.009 |
| 8-30         |  489 |   0.003 |         0.202 |       0.202 |       0.184 |              0.001 |
| >30          |  150 |   0     |         0.22  |       0.22  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.048 |         0.43  |       0.296 |       0.17  |              0.009 |
| more          |  394 |   0.186 |         0.536 |       0.302 |       0.076 |              0.014 |
| same          | 2113 |   0.092 |         0.444 |       0.343 |       0.118 |              0.008 |

## Worst series
| series_id                                                       |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  75 |  -0.387 |         0     |       0     |       0.147 |             -0.003 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median            |  69 |  -0.12  |         0.261 |       0.217 |       0.275 |             -0.008 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                   |  69 |  -0.06  |         0.304 |       0.217 |       0.261 |              0.007 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  69 |  -0.014 |         0.261 |       0.203 |       0.072 |              0.003 |
| fastgpu_daily.neocloud_spot.B200.spot.median                    |  69 |  -0.007 |         0.217 |       0.217 |       0.783 |             -0.001 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  74 |  -0.003 |         0.554 |       0.486 |       0     |              0.069 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  69 |  -0.002 |         0.116 |       0.116 |       0.116 |             -0     |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median          |  69 |   0     |         0.667 |       0.493 |       0.029 |              0.005 |

## Each base model alone: skill by group
| group                              |   vol_weighted_drift_floor2 |
|:-----------------------------------|----------------------------:|
| afhubbard|hyperscaler_spot         |                       0.148 |
| fastgpu_daily|hyperscaler_spot     |                      -0.115 |
| fastgpu_daily|neocloud_rate_card   |                       0.089 |
| fastgpu_daily|neocloud_spot        |                       0.096 |
| gpurentalprices|marketplace_ask    |                       0.252 |
| gpurentalprices|neocloud_rate_card |                       0.131 |

## Mean ensemble weight by group
| group                              |   vol_weighted_drift_floor2 |
|:-----------------------------------|----------------------------:|
| afhubbard|hyperscaler_spot         |                           1 |
| fastgpu_daily|hyperscaler_spot     |                           1 |
| fastgpu_daily|neocloud_rate_card   |                           1 |
| fastgpu_daily|neocloud_spot        |                           1 |
| gpurentalprices|marketplace_ask    |                           1 |
| gpurentalprices|neocloud_rate_card |                           1 |

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
