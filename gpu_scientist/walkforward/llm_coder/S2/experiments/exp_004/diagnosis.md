# Diagnosis (dev origins only)

Cells: 2642. Overall skill -0.0; truth above q50 in 46% of cells (50% if unbiased); above q90 46% and below q10 16% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 300 |       0 |         0.227 |       0.227 |       0.27  |              0     |
| fastgpu_daily|hyperscaler_spot     | 138 |       0 |         0.239 |       0.239 |       0.268 |             -0     |
| fastgpu_daily|neocloud_rate_card   | 759 |      -0 |         0.545 |       0.545 |       0.134 |              0.005 |
| fastgpu_daily|neocloud_spot        | 483 |      -0 |         0.387 |       0.387 |       0.124 |              0.011 |
| gpurentalprices|marketplace_ask    |  74 |       0 |         0.216 |       0.216 |       0.338 |             -0.012 |
| gpurentalprices|neocloud_rate_card | 888 |       0 |         0.553 |       0.553 |       0.145 |              0.02  |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 885 |      -0 |         0.32  |       0.32  |       0.118 |              0.003 |
|              3 | 885 |      -0 |         0.467 |       0.467 |       0.166 |              0.008 |
|              7 | 872 |      -0 |         0.588 |       0.588 |       0.21  |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1343 |      -0 |         0.608 |       0.608 |       0.179 |              0.012 |
| 2-3          |  376 |      -0 |         0.396 |       0.396 |       0.141 |              0.01  |
| 4-7          |  284 |      -0 |         0.394 |       0.394 |       0.173 |              0.009 |
| 8-30         |  489 |      -0 |         0.202 |       0.202 |       0.186 |              0.001 |
| >30          |  150 |       0 |         0.22  |       0.22  |       0     |              0.015 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  135 |      -0 |         0.407 |       0.407 |       0.148 |              0.009 |
| more          |  394 |      -0 |         0.543 |       0.543 |       0.104 |              0.016 |
| same          | 2113 |      -0 |         0.445 |       0.445 |       0.177 |              0.009 |

## Worst series
| series_id                                                   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median            |  75 |       0 |         0     |       0     |       0.147 |             -0.003 |
| afhubbard.hyperscaler_spot.A100_SXM_80GB.spot.median        |  75 |       0 |         0.253 |       0.253 |       0.267 |              0.002 |
| afhubbard.hyperscaler_spot.T4.spot.median                   |  75 |       0 |         0.427 |       0.427 |       0.4   |              0.001 |
| afhubbard.hyperscaler_spot.V100.spot.median                 |  75 |       0 |         0.227 |       0.227 |       0.267 |              0.002 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median        |  69 |       0 |         0.275 |       0.275 |       0.261 |             -0.004 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median               |  69 |       0 |         0.203 |       0.203 |       0.275 |              0.003 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median |  69 |       0 |         0.696 |       0.696 |       0.159 |             -0.009 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median |  69 |       0 |         0.116 |       0.116 |       0.116 |             -0     |

## Each base model alone: skill by group
| group                              |   peer_leader_lag |
|:-----------------------------------|------------------:|
| afhubbard|hyperscaler_spot         |                -0 |
| fastgpu_daily|hyperscaler_spot     |                -0 |
| fastgpu_daily|neocloud_rate_card   |                -0 |
| fastgpu_daily|neocloud_spot        |                -0 |
| gpurentalprices|marketplace_ask    |                -0 |
| gpurentalprices|neocloud_rate_card |                -0 |

## Mean ensemble weight by group
| group                              |   peer_leader_lag |
|:-----------------------------------|------------------:|
| afhubbard|hyperscaler_spot         |                 1 |
| fastgpu_daily|hyperscaler_spot     |                 1 |
| fastgpu_daily|neocloud_rate_card   |                 1 |
| fastgpu_daily|neocloud_spot        |                 1 |
| gpurentalprices|marketplace_ask    |                 1 |
| gpurentalprices|neocloud_rate_card |                 1 |

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
