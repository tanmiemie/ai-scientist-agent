# Diagnosis (dev origins only)

Cells: 1878. Overall skill 0.2104; truth above q50 in 44% of cells (50% if unbiased); above q90 20% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 216 |   0.129 |         0.231 |       0.056 |       0.042 |              0.001 |
| fastgpu_daily|hyperscaler_spot     |  96 |   0     |         0.354 |       0.219 |       0.24  |              0.016 |
| fastgpu_daily|neocloud_rate_card   | 528 |   0.183 |         0.473 |       0.205 |       0.142 |              0.005 |
| fastgpu_daily|neocloud_spot        | 336 |   0.202 |         0.333 |       0.229 |       0.17  |              0.01  |
| gpurentalprices|marketplace_ask    |  54 |   0.041 |         0.407 |       0.019 |       0.037 |             -0.021 |
| gpurentalprices|neocloud_rate_card | 648 |   0.278 |         0.562 |       0.227 |       0.059 |              0.022 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 626 |   0.088 |         0.288 |       0.139 |       0.099 |              0.002 |
|              3 | 626 |   0.117 |         0.449 |       0.166 |       0.121 |              0.009 |
|              7 | 626 |   0.277 |         0.593 |       0.28  |       0.105 |              0.022 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 879 |   0.247 |         0.584 |       0.205 |       0.096 |              0.014 |
| 2-3          | 249 |   0.176 |         0.506 |       0.177 |       0.092 |              0.015 |
| 4-7          | 159 |   0.228 |         0.447 |       0.277 |       0.151 |              0.013 |
| 8-30         | 456 |   0.075 |         0.211 |       0.175 |       0.16  |              0.002 |
| >30          | 135 |   0.12  |         0.193 |       0.133 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   42 |  -0.176 |         0.5   |       0.143 |       0.19  |              0.018 |
| more          |  120 |   0.257 |         0.567 |       0.2   |       0.108 |              0.024 |
| same          | 1716 |   0.216 |         0.433 |       0.196 |       0.107 |              0.01  |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  48 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  54 |   -2.986 |         0.074 |       0     |       0     |              0.001 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  54 |   -1.731 |         0     |       0     |       0.019 |             -0.002 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  48 |   -0.178 |         0     |       0     |       1     |             -0.003 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                    |  48 |   -0.048 |         0.458 |       0.25  |       0.25  |              0.029 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  48 |   -0.034 |         0     |       0     |       0.292 |             -0.031 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  48 |    0.01  |         0.25  |       0.188 |       0.229 |              0.004 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  54 |    0.017 |         0.093 |       0.019 |       0.222 |             -0.005 |

## Each base model alone: skill by group
| group                              |   step_hazard |
|:-----------------------------------|--------------:|
| afhubbard|hyperscaler_spot         |         0.207 |
| fastgpu_daily|hyperscaler_spot     |        -0.016 |
| fastgpu_daily|neocloud_rate_card   |         0.097 |
| fastgpu_daily|neocloud_spot        |         0.087 |
| gpurentalprices|marketplace_ask    |         0.039 |
| gpurentalprices|neocloud_rate_card |         0.11  |

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
| series                                                            | leader                                                          |   lag_days |   corr |
|:------------------------------------------------------------------|:----------------------------------------------------------------|-----------:|-------:|
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_list.H100_SXM_80GB.on_demand.median |          2 | -0.952 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.H100_SXM_80GB.spot.median      |          2 | -0.952 |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median      |          1 |  0.869 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median          | afhubbard.hyperscaler_spot.B200.spot.median                     |          5 | -0.508 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median  |          1 | -0.504 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  | afhubbard.neocloud_rate_card.RTX_PRO_6000.on_demand.median      |          1 |  0.487 |
| gpurentalprices.neocloud_rate_card.A100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.A100_SXM_80GB.spot.median      |          5 |  0.378 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.neocloud_rate_card.B300.on_demand.median              |          3 |  0.352 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_spot.H200.spot.median               |          5 |  0.339 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_spot.H100_80GB.spot.median             |          3 | -0.306 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median          |          5 |  0.301 |
