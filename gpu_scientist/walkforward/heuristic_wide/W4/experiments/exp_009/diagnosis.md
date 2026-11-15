# Diagnosis (dev origins only)

Cells: 2322. Overall skill 0.1997; truth above q50 in 43% of cells (50% if unbiased); above q90 17% and below q10 12% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 264 |   0.035 |         0.235 |       0.076 |       0.057 |             -0.001 |
| fastgpu_daily|hyperscaler_spot     | 120 |   0.073 |         0.25  |       0.167 |       0.192 |              0.001 |
| fastgpu_daily|neocloud_rate_card   | 660 |   0.202 |         0.494 |       0.159 |       0.158 |              0.002 |
| fastgpu_daily|neocloud_spot        | 420 |   0.181 |         0.355 |       0.183 |       0.207 |              0.009 |
| gpurentalprices|marketplace_ask    |  66 |   0.064 |         0.212 |       0.045 |       0.03  |             -0.028 |
| gpurentalprices|neocloud_rate_card | 792 |   0.241 |         0.525 |       0.211 |       0.054 |              0.019 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 774 |   0.022 |         0.269 |       0.121 |       0.125 |              0     |
|              3 | 774 |   0.156 |         0.442 |       0.142 |       0.121 |              0.006 |
|              7 | 774 |   0.261 |         0.578 |       0.243 |       0.107 |              0.017 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1185 |   0.226 |         0.535 |       0.161 |       0.129 |              0.008 |
| 2-3          |  294 |   0.168 |         0.459 |       0.167 |       0.048 |              0.012 |
| 4-7          |  216 |   0.225 |         0.444 |       0.213 |       0.125 |              0.011 |
| 8-30         |  483 |   0.076 |         0.205 |       0.176 |       0.166 |              0.001 |
| >30          |  144 |   0.113 |         0.229 |       0.146 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   90 |   0.048 |         0.344 |       0.122 |       0.211 |              0.006 |
| more          |  273 |   0.186 |         0.516 |       0.114 |       0.117 |              0.016 |
| same          | 1959 |   0.215 |         0.421 |       0.179 |       0.114 |              0.007 |

## Worst series
| series_id                                                   |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median           |  60 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median            |  66 |   -1.238 |         0     |       0     |       0.061 |             -0.005 |
| fastgpu_daily.neocloud_spot.H200.spot.median                |  60 |   -0.084 |         0.333 |       0.183 |       0.1   |              0.004 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median      |  66 |   -0.042 |         0.106 |       0.015 |       0.106 |             -0.005 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median    |  66 |   -0.027 |         0.197 |       0     |       0     |              0.004 |
| fastgpu_daily.neocloud_spot.B200.spot.median                |  60 |    0.022 |         0.083 |       0     |       0.867 |             -0.004 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median               |  60 |    0.034 |         0.183 |       0.183 |       0.167 |              0.002 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median |  60 |    0.061 |         0.667 |       0.183 |       0.167 |             -0.001 |

## Each base model alone: skill by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.052 |
| fastgpu_daily|hyperscaler_spot     |      0.059 |
| fastgpu_daily|neocloud_rate_card   |      0.165 |
| fastgpu_daily|neocloud_spot        |      0.193 |
| gpurentalprices|marketplace_ask    |      0.065 |
| gpurentalprices|neocloud_rate_card |      0.152 |

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
| series                                                            | leader                                                                  |   lag_days |   corr |
|:------------------------------------------------------------------|:------------------------------------------------------------------------|-----------:|-------:|
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median             |          5 |  0.997 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median                  |          5 |  0.994 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median       |          2 |  0.933 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_list.H100_SXM_80GB.on_demand.median         |          5 |  0.913 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.H100_SXM_80GB.spot.median              |          5 |  0.913 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median     | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median                 |          4 |  0.868 |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median              |          1 |  0.86  |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.neocloud_rate_card.B300.on_demand.median                      |          1 |  0.712 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median     | gpurentalprices_cheapest.aggregator_cheapest.RTX_A6000.on_demand.median |          2 | -0.712 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | gpurentalprices.neocloud_rate_card.B300.serverless.median               |          1 |  0.703 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.hyperscaler_list.B300.on_demand.median                        |          2 | -0.648 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.neocloud_rate_card.H200.serverless.median               |          2 |  0.586 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | afhubbard.neocloud_rate_card.H200.on_demand.median                      |          2 |  0.57  |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_list.H200.on_demand.median                  |          1 | -0.538 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median          |          1 | -0.504 |
