# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.1503; truth above q50 in 48% of cells (50% if unbiased); above q90 25% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.193 |         0.229 |       0.052 |       0.133 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.085 |         0.211 |       0.156 |       0.328 |             -0.018 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.122 |         0.545 |       0.298 |       0.136 |              0.004 |
| fastgpu_daily|neocloud_spot        |  630 |   0.208 |         0.425 |       0.27  |       0.095 |              0.011 |
| gpurentalprices|marketplace_ask    |   89 |   0.165 |         0.292 |       0.056 |       0.022 |              0.009 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.174 |         0.591 |       0.291 |       0.042 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.111 |         0.346 |       0.157 |       0.079 |              0.003 |
|              3 | 1118 |   0.164 |         0.487 |       0.232 |       0.108 |              0.007 |
|              7 | 1105 |   0.151 |         0.597 |       0.357 |       0.129 |              0.016 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.185 |         0.628 |       0.296 |       0.104 |              0.01  |
| 2-3          |  408 |   0.08  |         0.39  |       0.199 |       0.066 |              0.009 |
| 4-7          |  407 |   0.143 |         0.4   |       0.209 |       0.12  |              0.011 |
| 8-30         |  613 |   0.037 |         0.232 |       0.188 |       0.155 |              0.003 |
| >30          |  171 |   0     |         0.193 |       0.193 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.034 |         0.44  |       0.28  |       0.119 |              0.009 |
| more          |  583 |   0.171 |         0.568 |       0.269 |       0.099 |              0.013 |
| same          | 2590 |   0.151 |         0.458 |       0.241 |       0.106 |              0.008 |

## Worst series
| series_id                                                        |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  96 |  -0.611 |         0     |       0     |       0.115 |             -0.002 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  89 |  -0.046 |         0.461 |       0.393 |       0     |              0.057 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      |  90 |  -0.002 |         0.478 |       0.267 |       0.144 |             -0.016 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  90 |   0.004 |         0.144 |       0.144 |       0.244 |             -0.017 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median            |  90 |   0.011 |         0.233 |       0.233 |       0     |              0.007 |
| fastgpu_daily.neocloud_rate_card.A100_80GB.on_demand.median      |  90 |   0.012 |         0.211 |       0.211 |       0.089 |              0.004 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median    |  89 |   0.024 |         0.449 |       0.213 |       0.034 |              0.013 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  90 |   0.027 |         0.289 |       0.2   |       0.067 |              0.003 |

## Each base model alone: skill by group
| group                              |   drift |
|:-----------------------------------|--------:|
| afhubbard|hyperscaler_spot         |   0.174 |
| fastgpu_daily|hyperscaler_spot     |   0.001 |
| fastgpu_daily|neocloud_rate_card   |   0.05  |
| fastgpu_daily|neocloud_spot        |   0.008 |
| gpurentalprices|marketplace_ask    |   0.179 |
| gpurentalprices|neocloud_rate_card |   0.09  |

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
