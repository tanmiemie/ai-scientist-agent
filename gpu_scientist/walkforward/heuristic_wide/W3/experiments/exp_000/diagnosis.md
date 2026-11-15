# Diagnosis (dev origins only)

Cells: 1878. Overall skill 0.039; truth above q50 in 46% of cells (50% if unbiased); above q90 43% and below q10 12% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 216 |   0.177 |         0.245 |       0.139 |       0.176 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  96 |   0     |         0.281 |       0.281 |       0.302 |              0.005 |
| fastgpu_daily|neocloud_rate_card   | 528 |  -0     |         0.544 |       0.544 |       0.1   |              0.007 |
| fastgpu_daily|neocloud_spot        | 336 |  -0     |         0.336 |       0.336 |       0.161 |              0.01  |
| gpurentalprices|marketplace_ask    |  54 |   0.148 |         0.222 |       0.056 |       0.037 |             -0.027 |
| gpurentalprices|neocloud_rate_card | 648 |   0.057 |         0.562 |       0.534 |       0.091 |              0.023 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 626 |   0.03  |         0.292 |       0.284 |       0.096 |              0.002 |
|              3 | 626 |   0.043 |         0.463 |       0.441 |       0.131 |              0.009 |
|              7 | 626 |   0.039 |         0.612 |       0.562 |       0.149 |              0.022 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 879 |   0.053 |         0.611 |       0.569 |       0.122 |              0.015 |
| 2-3          | 249 |   0.031 |         0.506 |       0.478 |       0.076 |              0.014 |
| 4-7          | 159 |   0.031 |         0.447 |       0.415 |       0.189 |              0.012 |
| 8-30         | 456 |  -0.003 |         0.211 |       0.208 |       0.173 |              0.002 |
| >30          | 135 |   0     |         0.193 |       0.193 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   42 |  -0.224 |         0.31  |       0.262 |       0.19  |              0.015 |
| more          |  120 |   0.009 |         0.6   |       0.6   |       0.075 |              0.026 |
| same          | 1716 |   0.054 |         0.449 |       0.421 |       0.127 |              0.01  |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  54 |  -0.631 |         0     |       0     |       0.111 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median      |  48 |   0     |         0.708 |       0.708 |       0.104 |             -0.01  |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                    |  48 |   0     |         0.292 |       0.292 |       0.375 |              0.006 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  48 |   0     |         0.271 |       0.271 |       0.229 |              0.005 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median      |  48 |   0     |         0.083 |       0.083 |       0.104 |              0.001 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  48 |   0     |         0     |       0     |       0.292 |             -0.031 |
| fastgpu_daily.neocloud_rate_card.B300.on_demand.median           |  48 |  -0     |         0.854 |       0.854 |       0.146 |              0.035 |
| fastgpu_daily.neocloud_rate_card.B200.on_demand.median           |  48 |  -0     |         0.771 |       0.771 |       0.021 |              0.031 |

## Each base model alone: skill by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |   0.177 |
| fastgpu_daily|hyperscaler_spot     |  -0     |
| fastgpu_daily|neocloud_rate_card   |  -0     |
| fastgpu_daily|neocloud_spot        |  -0     |
| gpurentalprices|marketplace_ask    |   0.148 |
| gpurentalprices|neocloud_rate_card |   0.057 |

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
