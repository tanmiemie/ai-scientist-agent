# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.1176; truth above q50 in 43% of cells (50% if unbiased); above q90 29% and below q10 11% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.156 |         0.266 |       0.109 |       0.057 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |  -0.208 |         0.31  |       0.274 |       0.274 |              0.009 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.106 |         0.444 |       0.273 |       0.104 |              0.003 |
| fastgpu_daily|neocloud_spot        | 294 |   0.06  |         0.32  |       0.282 |       0.163 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.229 |         0.229 |       0.042 |       0.083 |             -0.043 |
| gpurentalprices|neocloud_rate_card | 576 |   0.129 |         0.552 |       0.378 |       0.071 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.117 |         0.292 |       0.163 |       0.074 |              0.001 |
|              3 | 552 |   0.12  |         0.42  |       0.266 |       0.114 |              0.005 |
|              7 | 552 |   0.116 |         0.565 |       0.428 |       0.129 |              0.018 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.139 |         0.574 |       0.335 |       0.099 |              0.009 |
| 2-3          | 192 |   0.114 |         0.49  |       0.328 |       0.052 |              0.012 |
| 4-7          | 150 |   0.135 |         0.42  |       0.307 |       0.16  |              0.01  |
| 8-30         | 426 |   0.035 |         0.211 |       0.209 |       0.153 |              0.002 |
| >30          | 123 |   0     |         0.154 |       0.154 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.551 |         0.056 |       0     |       0.333 |             -0.008 |
| more          |   75 |   0.147 |         0.467 |       0.307 |       0.107 |              0.016 |
| same          | 1563 |   0.119 |         0.428 |       0.288 |       0.103 |              0.008 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  48 |  -1.769 |         0     |       0     |       0     |             -0.001 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  42 |  -0.255 |         0.214 |       0.214 |       0.286 |             -0.009 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median      |  42 |   0     |         0.024 |       0.024 |       0.095 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  42 |   0     |         0     |       0     |       0.286 |             -0.032 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median           |  42 |   0     |         0.071 |       0.071 |       0.095 |              0.001 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  42 |  -0     |         0     |       0     |       1     |             -0.002 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median    |  48 |   0     |         0.125 |       0.125 |       0     |              0.021 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  48 |   0     |         0.042 |       0.042 |       0     |              0     |

## Each base model alone: skill by group
| group                              |   gentle_stale_aware_quantiles |
|:-----------------------------------|-------------------------------:|
| afhubbard|hyperscaler_spot         |                          0.156 |
| fastgpu_daily|hyperscaler_spot     |                         -0.208 |
| fastgpu_daily|neocloud_rate_card   |                          0.106 |
| fastgpu_daily|neocloud_spot        |                          0.06  |
| gpurentalprices|marketplace_ask    |                          0.229 |
| gpurentalprices|neocloud_rate_card |                          0.129 |

## Mean ensemble weight by group
| group                              |   gentle_stale_aware_quantiles |
|:-----------------------------------|-------------------------------:|
| afhubbard|hyperscaler_spot         |                              1 |
| fastgpu_daily|hyperscaler_spot     |                              1 |
| fastgpu_daily|neocloud_rate_card   |                              1 |
| fastgpu_daily|neocloud_spot        |                              1 |
| gpurentalprices|marketplace_ask    |                              1 |
| gpurentalprices|neocloud_rate_card |                              1 |

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
