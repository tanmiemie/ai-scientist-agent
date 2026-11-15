# Diagnosis (dev origins only)

Cells: 3256. Overall skill 0.0714; truth above q50 in 48% of cells (50% if unbiased); above q90 42% and below q10 12% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  372 |   0.174 |         0.223 |       0.099 |       0.226 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  174 |  -0.007 |         0.207 |       0.184 |       0.345 |             -0.016 |
| fastgpu_daily|neocloud_rate_card   |  957 |   0.054 |         0.546 |       0.531 |       0.133 |              0.005 |
| fastgpu_daily|neocloud_spot        |  609 |   0.006 |         0.422 |       0.42  |       0.099 |              0.011 |
| gpurentalprices|marketplace_ask    |   88 |   0.176 |         0.295 |       0.091 |       0.023 |              0.011 |
| gpurentalprices|neocloud_rate_card | 1056 |   0.089 |         0.591 |       0.498 |       0.071 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1094 |   0.022 |         0.342 |       0.328 |       0.091 |              0.003 |
|              3 | 1081 |   0.061 |         0.487 |       0.435 |       0.129 |              0.008 |
|              7 | 1081 |   0.087 |         0.6   |       0.498 |       0.156 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1685 |   0.086 |         0.628 |       0.561 |       0.134 |              0.011 |
| 2-3          |  405 |   0.037 |         0.388 |       0.341 |       0.079 |              0.009 |
| 4-7          |  398 |   0.079 |         0.41  |       0.317 |       0.136 |              0.011 |
| 8-30         |  600 |   0.02  |         0.23  |       0.207 |       0.16  |              0.002 |
| >30          |  168 |   0     |         0.196 |       0.196 |       0     |              0.014 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |  -0.091 |         0.44  |       0.411 |       0.119 |              0.009 |
| more          |  554 |   0.093 |         0.572 |       0.513 |       0.087 |              0.014 |
| same          | 2534 |   0.076 |         0.457 |       0.4   |       0.134 |              0.008 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  93 |  -0.574 |         0     |       0     |       0.118 |             -0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  88 |  -0.045 |         0.466 |       0.466 |       0     |              0.058 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      |  87 |  -0.029 |         0.494 |       0.494 |       0.149 |             -0.016 |
| fastgpu_daily.neocloud_rate_card.RTX_PRO_6000.on_demand.median   |  87 |  -0.015 |         0.575 |       0.575 |       0.207 |              0.024 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  87 |  -0.01  |         0.207 |       0.207 |       0.414 |             -0.027 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median |  88 |  -0.007 |         0.614 |       0.614 |       0.068 |              0.019 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  87 |   0     |         0.149 |       0.149 |       0.253 |             -0.017 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median           |  87 |   0     |         0.471 |       0.471 |       0.08  |              0.01  |

## Each base model alone: skill by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |   0.174 |
| fastgpu_daily|hyperscaler_spot     |  -0.007 |
| fastgpu_daily|neocloud_rate_card   |   0.054 |
| fastgpu_daily|neocloud_spot        |   0.006 |
| gpurentalprices|marketplace_ask    |   0.176 |
| gpurentalprices|neocloud_rate_card |   0.089 |

## Mean ensemble weight by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |       1 |
| fastgpu_daily|hyperscaler_spot     |       1 |
| fastgpu_daily|neocloud_rate_card   |       1 |
| fastgpu_daily|neocloud_spot        |       1 |
| gpurentalprices|marketplace_ask    |       1 |
| gpurentalprices|neocloud_rate_card |       1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                           | leader                                                            |   lag_days |   corr |
|:-----------------------------------------------------------------|:------------------------------------------------------------------|-----------:|-------:|
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_rate_card.B200.serverless.median         |          3 | -0.928 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     | gpurentalprices.neocloud_spot.B200.spot.median                    |          1 |  0.928 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      | gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median     |          3 | -0.925 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median |          2 |  0.922 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median | fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median      |          4 |  0.884 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median           |          4 |  0.868 |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | afhubbard.hyperscaler_list.B300.on_demand.median                  |          1 | -0.85  |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           | fastgpu_daily.hyperscaler_list.B300.on_demand.median              |          2 | -0.85  |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median        |          1 |  0.8   |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     | afhubbard.neocloud_spot.L40S.spot.median                          |          1 |  0.789 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  |          1 |  0.785 |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median |          3 |  0.762 |
| fastgpu_daily.neocloud_spot.L40S.spot.median                     | afhubbard.neocloud_rate_card.L40S.on_demand.median                |          1 |  0.736 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median       |          5 |  0.71  |
| fastgpu_daily.neocloud_spot.RTX_PRO_6000.spot.median             | fastgpu_daily.hyperscaler_list.RTX_PRO_6000.on_demand.median      |          5 |  0.705 |
