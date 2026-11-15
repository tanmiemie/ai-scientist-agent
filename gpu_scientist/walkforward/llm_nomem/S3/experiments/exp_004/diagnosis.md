# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.0319; truth above q50 in 48% of cells (50% if unbiased); above q90 11% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |  -0.485 |         0.229 |       0.049 |       0.164 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.001 |         0.211 |       0.072 |       0.294 |             -0.018 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.103 |         0.545 |       0.131 |       0.114 |              0.004 |
| fastgpu_daily|neocloud_spot        |  630 |  -0.216 |         0.425 |       0.071 |       0.067 |              0.011 |
| gpurentalprices|marketplace_ask    |   89 |   0.069 |         0.292 |       0.056 |       0.045 |              0.009 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.046 |         0.591 |       0.153 |       0.071 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.091 |         0.346 |       0.118 |       0.105 |              0.003 |
|              3 | 1118 |   0.099 |         0.487 |       0.126 |       0.112 |              0.007 |
|              7 | 1105 |  -0.015 |         0.597 |       0.092 |       0.099 |              0.016 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.106 |         0.628 |       0.128 |       0.112 |              0.01  |
| 2-3          |  408 |  -0.038 |         0.39  |       0.135 |       0.086 |              0.009 |
| 4-7          |  407 |   0.016 |         0.4   |       0.086 |       0.118 |              0.011 |
| 8-30         |  613 |  -0.299 |         0.232 |       0.083 |       0.119 |              0.003 |
| >30          |  171 |  -0.25  |         0.193 |       0.064 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |  -0.123 |         0.44  |       0.048 |       0.107 |              0.009 |
| more          |  583 |   0.066 |         0.568 |       0.089 |       0.074 |              0.013 |
| same          | 2590 |   0.03  |         0.458 |       0.122 |       0.112 |              0.008 |

## Worst series
| series_id                                                       |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median               |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                |  96 |   -4.294 |         0     |       0     |       0.083 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median |  90 |   -1.77  |         0.289 |       0.033 |       0.033 |              0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median          |  89 |   -1.609 |         0.326 |       0.034 |       0.315 |             -0.002 |
| afhubbard.hyperscaler_spot.T4.spot.median                       |  96 |   -0.865 |         0.438 |       0.094 |       0.271 |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median        |  89 |   -0.864 |         0.371 |       0.045 |       0.022 |              0.006 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median        |  89 |   -0.767 |         0.652 |       0.157 |       0.034 |              0.007 |
| fastgpu_daily.neocloud_spot.H100_SXM_80GB.spot.median           |  90 |   -0.72  |         0.233 |       0.011 |       0     |              0.007 |

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
