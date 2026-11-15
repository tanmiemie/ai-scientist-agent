# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.0643; truth above q50 in 45% of cells (50% if unbiased); above q90 37% and below q10 14% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.001 |         0.26  |       0.188 |       0.167 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |  -0.017 |         0.298 |       0.298 |       0.298 |              0.006 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.038 |         0.517 |       0.379 |       0.093 |              0.005 |
| fastgpu_daily|neocloud_spot        | 294 |   0.007 |         0.32  |       0.313 |       0.163 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.309 |         0.292 |       0.104 |       0.271 |             -0.028 |
| gpurentalprices|neocloud_rate_card | 576 |   0.061 |         0.55  |       0.479 |       0.118 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.117 |         0.292 |       0.163 |       0.074 |              0.001 |
|              3 | 552 |   0.079 |         0.446 |       0.364 |       0.143 |              0.005 |
|              7 | 552 |   0.052 |         0.601 |       0.576 |       0.197 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.085 |         0.61  |       0.48  |       0.137 |              0.011 |
| 2-3          | 192 |   0.087 |         0.51  |       0.406 |       0.12  |              0.012 |
| 4-7          | 150 |   0.018 |         0.433 |       0.373 |       0.22  |              0.011 |
| 8-30         | 426 |   0.006 |         0.211 |       0.209 |       0.16  |              0.002 |
| >30          | 123 |   0     |         0.154 |       0.154 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.446 |         0.056 |       0     |       0.333 |             -0.004 |
| more          |   75 |   0.029 |         0.507 |       0.44  |       0.107 |              0.018 |
| same          | 1563 |   0.072 |         0.448 |       0.369 |       0.138 |              0.008 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  42 |  -0.029 |         0.262 |       0.262 |       0.262 |              0.005 |
| afhubbard.hyperscaler_spot.A100_SXM_80GB.spot.median             |  48 |  -0.006 |         0.229 |       0.229 |       0.271 |              0.005 |
| afhubbard.hyperscaler_spot.V100.spot.median                      |  48 |  -0.004 |         0.229 |       0.229 |       0.25  |              0.004 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  42 |  -0.003 |         0.19  |       0.19  |       0.119 |              0.002 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median      |  42 |   0     |         0.024 |       0.024 |       0.095 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median           |  42 |   0     |         0.071 |       0.071 |       0.095 |              0.001 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  42 |   0     |         0     |       0     |       0.286 |             -0.032 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  48 |   0     |         0     |       0     |       0.062 |             -0.001 |

## Each base model alone: skill by group
| group                              |   stale_aware_quantiles |
|:-----------------------------------|------------------------:|
| afhubbard|hyperscaler_spot         |                   0.001 |
| fastgpu_daily|hyperscaler_spot     |                  -0.017 |
| fastgpu_daily|neocloud_rate_card   |                   0.038 |
| fastgpu_daily|neocloud_spot        |                   0.007 |
| gpurentalprices|marketplace_ask    |                   0.309 |
| gpurentalprices|neocloud_rate_card |                   0.061 |

## Mean ensemble weight by group
| group                              |   stale_aware_quantiles |
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
