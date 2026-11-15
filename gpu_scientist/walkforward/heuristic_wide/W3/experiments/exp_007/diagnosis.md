# Diagnosis (dev origins only)

Cells: 1878. Overall skill 0.2181; truth above q50 in 46% of cells (50% if unbiased); above q90 20% and below q10 9% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 216 |   0.118 |         0.245 |       0.074 |       0.037 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  96 |   0.141 |         0.281 |       0.208 |       0.219 |              0.005 |
| fastgpu_daily|neocloud_rate_card   | 528 |   0.202 |         0.544 |       0.186 |       0.098 |              0.007 |
| fastgpu_daily|neocloud_spot        | 336 |   0.176 |         0.336 |       0.223 |       0.161 |              0.01  |
| gpurentalprices|marketplace_ask    |  54 |   0.16  |         0.241 |       0.056 |       0.037 |             -0.022 |
| gpurentalprices|neocloud_rate_card | 648 |   0.261 |         0.562 |       0.241 |       0.059 |              0.023 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 626 |   0.068 |         0.292 |       0.128 |       0.091 |              0.003 |
|              3 | 626 |   0.154 |         0.463 |       0.168 |       0.094 |              0.009 |
|              7 | 626 |   0.276 |         0.613 |       0.292 |       0.094 |              0.022 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 879 |   0.253 |         0.613 |       0.208 |       0.074 |              0.015 |
| 2-3          | 249 |   0.196 |         0.506 |       0.177 |       0.06  |              0.015 |
| 4-7          | 159 |   0.246 |         0.44  |       0.245 |       0.138 |              0.012 |
| 8-30         | 456 |   0.075 |         0.211 |       0.178 |       0.16  |              0.002 |
| >30          | 135 |   0.093 |         0.193 |       0.156 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   42 |  -0.091 |         0.286 |       0.143 |       0.167 |              0.016 |
| more          |  120 |   0.237 |         0.6   |       0.183 |       0.075 |              0.026 |
| same          | 1716 |   0.226 |         0.45  |       0.198 |       0.093 |              0.01  |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  48 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  54 |   -2.454 |         0.074 |       0     |       0     |              0.001 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  54 |   -1.948 |         0     |       0     |       0     |             -0.002 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  48 |   -0.177 |         0     |       0     |       1     |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  48 |   -0.027 |         0     |       0     |       0.271 |             -0.031 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median      |  48 |    0.05  |         0.708 |       0.167 |       0.104 |             -0.01  |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  54 |    0.053 |         0.093 |       0.019 |       0.222 |             -0.005 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  54 |    0.098 |         0.759 |       0.278 |       0     |              0.094 |

## Each base model alone: skill by group
| group                              |   trend_tail |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |        0.156 |
| fastgpu_daily|hyperscaler_spot     |        0.131 |
| fastgpu_daily|neocloud_rate_card   |        0.133 |
| fastgpu_daily|neocloud_spot        |        0.125 |
| gpurentalprices|marketplace_ask    |        0.161 |
| gpurentalprices|neocloud_rate_card |        0.129 |

## Mean ensemble weight by group
| group                              |   trend_tail |
|:-----------------------------------|-------------:|
| afhubbard|hyperscaler_spot         |            1 |
| fastgpu_daily|hyperscaler_spot     |            1 |
| fastgpu_daily|neocloud_rate_card   |            1 |
| fastgpu_daily|neocloud_spot        |            1 |
| gpurentalprices|marketplace_ask    |            1 |
| gpurentalprices|neocloud_rate_card |            1 |

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
