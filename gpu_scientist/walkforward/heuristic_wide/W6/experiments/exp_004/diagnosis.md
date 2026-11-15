# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1759; truth above q50 in 46% of cells (50% if unbiased); above q90 11% and below q10 11% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.184 |         0.221 |       0.062 |       0.083 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.173 |         0.294 |       0.128 |       0.261 |             -0.008 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.172 |         0.492 |       0.116 |       0.118 |              0.002 |
| fastgpu_daily|neocloud_spot        |  630 |   0.261 |         0.421 |       0.122 |       0.124 |              0.01  |
| gpurentalprices|marketplace_ask    |   89 |   0.128 |         0.404 |       0.034 |       0.022 |              0.011 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.168 |         0.577 |       0.125 |       0.084 |              0.018 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.097 |         0.343 |       0.113 |       0.095 |              0.003 |
|              3 | 1118 |   0.101 |         0.474 |       0.103 |       0.106 |              0.007 |
|              7 | 1105 |   0.23  |         0.569 |       0.122 |       0.128 |              0.015 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.21  |         0.602 |       0.114 |       0.101 |              0.009 |
| 2-3          |  408 |   0.071 |         0.395 |       0.11  |       0.093 |              0.009 |
| 4-7          |  407 |   0.191 |         0.398 |       0.115 |       0.125 |              0.01  |
| 8-30         |  613 |   0.078 |         0.223 |       0.122 |       0.165 |              0.002 |
| >30          |  171 |   0.006 |         0.193 |       0.064 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.073 |         0.482 |       0.077 |       0.155 |              0.009 |
| more          |  583 |   0.156 |         0.53  |       0.065 |       0.07  |              0.01  |
| same          | 2590 |   0.193 |         0.445 |       0.125 |       0.115 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  96 |   -1.105 |         0     |       0     |       0.104 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  90 |   -0.669 |         0.289 |       0.011 |       0.056 |              0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  89 |   -0.596 |         0.315 |       0.011 |       0.191 |             -0.002 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  89 |   -0.205 |         0.371 |       0.022 |       0.022 |              0.006 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  89 |   -0.176 |         0.584 |       0.135 |       0.146 |              0.005 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median   |  89 |   -0.079 |         0.461 |       0.225 |       0.09  |              0.056 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median     |  90 |   -0.062 |         0.211 |       0.056 |       0.089 |              0.004 |

## Each base model alone: skill by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |         0.186 |
| fastgpu_daily|hyperscaler_spot     |         0.08  |
| fastgpu_daily|neocloud_rate_card   |         0.149 |
| fastgpu_daily|neocloud_spot        |         0.229 |
| gpurentalprices|marketplace_ask    |         0.122 |
| gpurentalprices|neocloud_rate_card |         0.129 |

## Mean ensemble weight by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |             1 |
| fastgpu_daily|hyperscaler_spot     |             1 |
| fastgpu_daily|neocloud_rate_card   |             1 |
| fastgpu_daily|neocloud_spot        |             1 |
| gpurentalprices|marketplace_ask    |             1 |
| gpurentalprices|neocloud_rate_card |             1 |

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
