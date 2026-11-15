# Diagnosis (dev origins only)

Cells: 1656. Overall skill 0.1698; truth above q50 in 44% of cells (50% if unbiased); above q90 32% and below q10 14% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 192 |   0.139 |         0.266 |       0.151 |       0.099 |              0.003 |
| fastgpu_daily|hyperscaler_spot     |  84 |   0.012 |         0.31  |       0.274 |       0.31  |              0.008 |
| fastgpu_daily|neocloud_rate_card   | 462 |   0.145 |         0.481 |       0.344 |       0.1   |              0.004 |
| fastgpu_daily|neocloud_spot        | 294 |   0.047 |         0.32  |       0.265 |       0.163 |              0.009 |
| gpurentalprices|marketplace_ask    |  48 |   0.233 |         0.25  |       0.125 |       0.333 |             -0.034 |
| gpurentalprices|neocloud_rate_card | 576 |   0.214 |         0.554 |       0.415 |       0.125 |              0.017 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 552 |   0.08  |         0.292 |       0.21  |       0.101 |              0.001 |
|              3 | 552 |   0.128 |         0.437 |       0.281 |       0.141 |              0.005 |
|              7 | 552 |   0.198 |         0.583 |       0.476 |       0.168 |              0.019 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 765 |   0.216 |         0.596 |       0.401 |       0.145 |              0.01  |
| 2-3          | 192 |   0.089 |         0.5   |       0.365 |       0.125 |              0.012 |
| 4-7          | 150 |   0.149 |         0.42  |       0.367 |       0.18  |              0.01  |
| 8-30         | 426 |   0.097 |         0.211 |       0.195 |       0.153 |              0.002 |
| >30          | 123 |  -0.003 |         0.154 |       0.154 |       0     |              0.01  |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   18 |  -0.205 |         0.056 |       0     |       0.333 |             -0.006 |
| more          |   75 |   0.223 |         0.493 |       0.307 |       0.107 |              0.017 |
| same          | 1563 |   0.166 |         0.439 |       0.327 |       0.136 |              0.008 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  42 | -inf    |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  48 |   -0.48 |         0     |       0     |       0     |             -0.001 |
| fastgpu_daily.neocloud_rate_card.L40S.on_demand.median           |  42 |    0    |         0.071 |       0.071 |       0.095 |              0.001 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  42 |    0    |         0     |       0     |       0.286 |             -0.032 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  42 |   -0    |         0     |       0     |       1     |             -0.002 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  48 |    0    |         0.042 |       0.042 |       0     |              0     |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median    |  48 |    0    |         0.125 |       0.125 |       0     |              0.021 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  42 |    0.01 |         0.214 |       0.214 |       0.262 |             -0.002 |

## Each base model alone: skill by group
| group                              |   leader_quantiles |
|:-----------------------------------|-------------------:|
| afhubbard|hyperscaler_spot         |              0.139 |
| fastgpu_daily|hyperscaler_spot     |              0.012 |
| fastgpu_daily|neocloud_rate_card   |              0.145 |
| fastgpu_daily|neocloud_spot        |              0.047 |
| gpurentalprices|marketplace_ask    |              0.233 |
| gpurentalprices|neocloud_rate_card |              0.214 |

## Mean ensemble weight by group
| group                              |   leader_quantiles |
|:-----------------------------------|-------------------:|
| afhubbard|hyperscaler_spot         |                  1 |
| fastgpu_daily|hyperscaler_spot     |                  1 |
| fastgpu_daily|neocloud_rate_card   |                  1 |
| fastgpu_daily|neocloud_spot        |                  1 |
| gpurentalprices|marketplace_ask    |                  1 |
| gpurentalprices|neocloud_rate_card |                  1 |

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
