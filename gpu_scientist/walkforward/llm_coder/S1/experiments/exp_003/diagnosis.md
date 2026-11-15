# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.0927; truth above q50 in 45% of cells (50% if unbiased); above q90 30% and below q10 21% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.108 |         0.302 |       0.151 |       0.229 |              0.002 |
| fastgpu_daily|hyperscaler_spot     |  84 |  -0.698 |         0.381 |       0.333 |       0.536 |              0.013 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.09  |         0.407 |       0.271 |       0.255 |              0.002 |
| fastgpu_daily|neocloud_spot        | 294 |   0.057 |         0.313 |       0.282 |       0.252 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.188 |         0.271 |       0.042 |       0.104 |             -0.055 |
| gpurentalprices|neocloud_rate_card | 576 |   0.12  |         0.62  |       0.398 |       0.095 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.057 |         0.366 |       0.221 |       0.263 |              0.001 |
|              3 | 552 |   0.086 |         0.431 |       0.264 |       0.174 |              0.004 |
|              7 | 552 |   0.1   |         0.543 |       0.413 |       0.181 |              0.016 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.119 |         0.613 |       0.348 |       0.216 |              0.008 |
| 2-3          | 192 |   0.061 |         0.5   |       0.365 |       0.24  |              0.011 |
| 4-7          | 150 |   0.077 |         0.44  |       0.34  |       0.367 |              0.009 |
| 8-30         | 426 |   0.041 |         0.211 |       0.211 |       0.176 |              0.002 |
| >30          | 123 |   0     |         0.154 |       0.154 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.586 |         0.278 |       0.111 |       0.389 |             -0.008 |
| more          |   75 |   0.161 |         0.427 |       0.307 |       0.44  |              0.014 |
| same          | 1563 |   0.089 |         0.45  |       0.301 |       0.193 |              0.007 |

## Worst series
| series_id                                                         |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:------------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                  |  48 |  -1.835 |         0     |       0     |       0.333 |             -0.002 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median              |  42 |  -0.822 |         0.143 |       0.071 |       0.857 |             -0.019 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median                     |  42 |  -0.07  |         0.619 |       0.595 |       0.214 |              0.044 |
| gpurentalprices.neocloud_rate_card.A100_SXM_80GB.on_demand.median |  48 |  -0.069 |         0.812 |       0.667 |       0.062 |              0.012 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median  |  42 |  -0.001 |         0.048 |       0.048 |       0.286 |             -0.031 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median            |  42 |   0     |         0.071 |       0.071 |       0.095 |              0.001 |
| fastgpu_daily.neocloud_spot.B200.spot.median                      |  42 |  -0     |         0     |       0     |       1     |             -0.002 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median       |  42 |   0     |         0.024 |       0.024 |       0.095 |             -0.003 |

## Each base model alone: skill by group
| group                              |   trend_aware_empirical |
|:-----------------------------------|------------------------:|
| afhubbard|hyperscaler_spot         |                   0.108 |
| fastgpu_daily|hyperscaler_spot     |                  -0.698 |
| fastgpu_daily|neocloud_rate_card   |                   0.09  |
| fastgpu_daily|neocloud_spot        |                   0.057 |
| gpurentalprices|marketplace_ask    |                   0.188 |
| gpurentalprices|neocloud_rate_card |                   0.12  |

## Mean ensemble weight by group
| group                              |   trend_aware_empirical |
|:-----------------------------------|------------------------:|
| afhubbard|hyperscaler_spot         |                       1 |
| fastgpu_daily|hyperscaler_spot     |                       1 |
| fastgpu_daily|neocloud_rate_card   |                       1 |
| fastgpu_daily|neocloud_spot        |                       1 |
| gpurentalprices|marketplace_ask    |                       1 |
| gpurentalprices|neocloud_rate_card |                       1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                            | leader                                                          |   lag_days |   corr |
|:------------------------------------------------------------------|:----------------------------------------------------------------|-----------:|-------:|
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_list.H100_SXM_80GB.on_demand.median |          2 | -0.952 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.H100_SXM_80GB.spot.median      |          2 | -0.952 |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median      |          1 |  0.87  |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.neocloud_rate_card.B300.on_demand.median              |          3 |  0.535 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median          | afhubbard.hyperscaler_spot.B200.spot.median                     |          5 | -0.511 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median  |          1 | -0.505 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  | afhubbard.neocloud_rate_card.RTX_PRO_6000.on_demand.median      |          5 |  0.427 |
| gpurentalprices.neocloud_rate_card.A100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.A100_SXM_80GB.spot.median      |          5 |  0.379 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_spot.H200.spot.median               |          5 |  0.339 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median            | afhubbard.hyperscaler_spot.L4.spot.median                       |          3 |  0.314 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median     | gpurentalprices.marketplace_ask.H100_80GB.spot.median           |          1 |  0.31  |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_spot.H100_80GB.spot.median             |          3 | -0.306 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median          |          5 |  0.306 |
