# Diagnosis (dev origins only)

Cells: 2642. Overall skill 0.1129; truth above q50 in 46% of cells (50% if unbiased); above q90 31% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |   0.198 |         0.207 |       0.08  |       0.077 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 138 |  -0.103 |         0.283 |       0.188 |       0.261 |             -0.001 |
| fastgpu_daily|neocloud_rate_card   | 759 |   0.103 |         0.52  |       0.401 |       0.124 |              0.003 |
| fastgpu_daily|neocloud_spot        | 483 |   0.085 |         0.387 |       0.34  |       0.124 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |   0.221 |         0.243 |       0.054 |       0.095 |             -0.016 |
| gpurentalprices|neocloud_rate_card | 888 |   0.12  |         0.57  |       0.336 |       0.06  |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |   0.067 |         0.316 |       0.182 |       0.071 |              0.002 |
|              3 | 885 |   0.125 |         0.467 |       0.298 |       0.104 |              0.007 |
|              7 | 872 |   0.117 |         0.589 |       0.453 |       0.135 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |   0.151 |         0.599 |       0.372 |       0.106 |              0.011 |
| 2-3          |  376 |   0.049 |         0.396 |       0.295 |       0.051 |              0.009 |
| 4-7          |  284 |   0.075 |         0.43  |       0.275 |       0.109 |              0.009 |
| 8-30         |  489 |   0.02  |         0.202 |       0.2   |       0.164 |              0.001 |
| >30          |  150 |   0     |         0.22  |       0.22  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |   0.061 |         0.43  |       0.259 |       0.141 |              0.009 |
| more          |  394 |   0.174 |         0.536 |       0.264 |       0.051 |              0.014 |
| same          | 2113 |   0.097 |         0.444 |       0.322 |       0.111 |              0.008 |

## Worst series
| series_id                                                     |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median              |  75 |  -0.646 |         0     |       0     |       0.013 |             -0.003 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median          |  69 |  -0.103 |         0.261 |       0.203 |       0.261 |             -0.008 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                 |  69 |  -0.103 |         0.304 |       0.174 |       0.261 |              0.007 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median |  74 |  -0.054 |         0.554 |       0.257 |       0     |              0.069 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median          |  69 |  -0.019 |         0.507 |       0.507 |       0     |              0.034 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median         |  69 |  -0.009 |         0.304 |       0.304 |       0     |              0.009 |
| fastgpu_daily.neocloud_rate_card.H200.on_demand.median        |  69 |   0.001 |         0.667 |       0.58  |       0.087 |              0.005 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median   |  69 |   0.009 |         0.623 |       0.522 |       0.159 |             -0.017 |

## Each base model alone: skill by group
| group                              |   vol_weighted_drift_broader |
|:-----------------------------------|-----------------------------:|
| afhubbard|hyperscaler_spot         |                        0.198 |
| fastgpu_daily|hyperscaler_spot     |                       -0.103 |
| fastgpu_daily|neocloud_rate_card   |                        0.103 |
| fastgpu_daily|neocloud_spot        |                        0.085 |
| gpurentalprices|marketplace_ask    |                        0.221 |
| gpurentalprices|neocloud_rate_card |                        0.12  |

## Mean ensemble weight by group
| group                              |   vol_weighted_drift_broader |
|:-----------------------------------|-----------------------------:|
| afhubbard|hyperscaler_spot         |                            1 |
| fastgpu_daily|hyperscaler_spot     |                            1 |
| fastgpu_daily|neocloud_rate_card   |                            1 |
| fastgpu_daily|neocloud_spot        |                            1 |
| gpurentalprices|marketplace_ask    |                            1 |
| gpurentalprices|neocloud_rate_card |                            1 |

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
