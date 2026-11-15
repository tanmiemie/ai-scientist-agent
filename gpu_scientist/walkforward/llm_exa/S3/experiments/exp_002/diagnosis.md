# Diagnosis (dev origins only)

Cells: 3341. Overall skill 0.2186; truth above q50 in 48% of cells (50% if unbiased); above q90 15% and below q10 10% (10% each if calibrated).

## By series group
| group                              |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         |  384 |   0.204 |         0.229 |       0.068 |       0.068 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  180 |   0.141 |         0.211 |       0.139 |       0.267 |             -0.018 |
| fastgpu_daily|neocloud_rate_card   |  990 |   0.209 |         0.545 |       0.123 |       0.118 |              0.004 |
| fastgpu_daily|neocloud_spot        |  630 |   0.286 |         0.425 |       0.197 |       0.1   |              0.011 |
| gpurentalprices|marketplace_ask    |   89 |   0.175 |         0.292 |       0.079 |       0.022 |              0.009 |
| gpurentalprices|neocloud_rate_card | 1068 |   0.232 |         0.591 |       0.172 |       0.064 |              0.019 |

## By horizon
|   horizon_days |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|-----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 1118 |   0.114 |         0.346 |       0.128 |       0.096 |              0.003 |
|              3 | 1118 |   0.176 |         0.487 |       0.13  |       0.1   |              0.007 |
|              7 | 1105 |   0.262 |         0.597 |       0.181 |       0.095 |              0.016 |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1742 |   0.256 |         0.628 |       0.151 |       0.099 |              0.01  |
| 2-3          |  408 |   0.142 |         0.39  |       0.147 |       0.071 |              0.009 |
| 4-7          |  407 |   0.208 |         0.4   |       0.14  |       0.101 |              0.011 |
| 8-30         |  613 |   0.091 |         0.232 |       0.144 |       0.132 |              0.003 |
| >30          |  171 |   0.154 |         0.193 |       0.117 |       0     |              0.013 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |  168 |   0.125 |         0.44  |       0.071 |       0.095 |              0.009 |
| more          |  583 |   0.214 |         0.568 |       0.117 |       0.086 |              0.013 |
| same          | 2590 |   0.228 |         0.458 |       0.158 |       0.1   |              0.008 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  90 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  96 |   -0.927 |         0     |       0     |       0.01  |             -0.002 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median           |  89 |   -0.36  |         0.326 |       0.011 |       0.247 |             -0.002 |
| fastgpu_daily.neocloud_rate_card.H100_SXM_80GB.on_demand.median  |  90 |   -0.347 |         0.289 |       0.022 |       0.011 |              0.003 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median         |  89 |   -0.066 |         0.652 |       0.169 |       0.022 |              0.007 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median    |  89 |   -0.002 |         0.461 |       0.247 |       0     |              0.057 |
| fastgpu_daily.neocloud_rate_card.RTX_A6000.on_demand.median      |  90 |    0.003 |         0.478 |       0.144 |       0.133 |             -0.016 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  90 |    0.047 |         0.144 |       0.033 |       0.244 |             -0.017 |

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
