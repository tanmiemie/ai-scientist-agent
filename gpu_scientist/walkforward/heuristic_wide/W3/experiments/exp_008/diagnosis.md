# Diagnosis (dev origins only)

Cells: 1878. Overall skill 0.2109; truth above q50 in 43% of cells (50% if unbiased); above q90 20% and below q10 12% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 216 |   0.026 |         0.241 |       0.083 |       0.046 |             -0     |
| fastgpu_daily|hyperscaler_spot     |  96 |   0.073 |         0.25  |       0.208 |       0.219 |              0.002 |
| fastgpu_daily|neocloud_rate_card   | 528 |   0.2   |         0.5   |       0.18  |       0.136 |              0.006 |
| fastgpu_daily|neocloud_spot        | 336 |   0.136 |         0.327 |       0.214 |       0.22  |              0.009 |
| gpurentalprices|marketplace_ask    |  54 |   0.116 |         0.222 |       0.056 |       0.037 |             -0.031 |
| gpurentalprices|neocloud_rate_card | 648 |   0.268 |         0.545 |       0.25  |       0.062 |              0.021 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 626 |   0.012 |         0.262 |       0.128 |       0.129 |              0.001 |
|              3 | 626 |   0.149 |         0.439 |       0.165 |       0.123 |              0.008 |
|              7 | 626 |   0.276 |         0.601 |       0.299 |       0.097 |              0.021 |

## By days since the last price change at the origin
| dsc_bucket   |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 879 |   0.245 |         0.565 |       0.199 |       0.129 |              0.011 |
| 2-3          | 249 |   0.188 |         0.506 |       0.197 |       0.052 |              0.015 |
| 4-7          | 159 |   0.235 |         0.44  |       0.258 |       0.138 |              0.012 |
| 8-30         | 456 |   0.074 |         0.211 |       0.184 |       0.156 |              0.002 |
| >30          | 135 |   0.071 |         0.193 |       0.156 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   42 |  -0.098 |         0.286 |       0.143 |       0.167 |              0.015 |
| more          |  120 |   0.209 |         0.542 |       0.183 |       0.208 |              0.023 |
| same          | 1716 |   0.223 |         0.43  |       0.199 |       0.109 |              0.009 |

## Worst series
| series_id                                                        |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median                |  48 | -inf     |         0     |       0     |       0     |              0     |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median         |  54 |   -2.452 |         0.074 |       0     |       0     |              0.001 |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median                 |  54 |   -2.195 |         0     |       0     |       0.019 |             -0.004 |
| fastgpu_daily.neocloud_spot.B200.spot.median                     |  48 |   -0.17  |         0     |       0     |       0.958 |             -0.003 |
| fastgpu_daily.neocloud_rate_card.H100_PCIe_80GB.on_demand.median |  48 |   -0.024 |         0     |       0     |       0.271 |             -0.031 |
| fastgpu_daily.neocloud_spot.H200.spot.median                     |  48 |   -0.013 |         0.292 |       0.229 |       0.104 |              0.005 |
| fastgpu_daily.neocloud_rate_card.A100_40GB.on_demand.median      |  48 |    0.053 |         0.646 |       0.167 |       0.167 |             -0.011 |
| fastgpu_daily.hyperscaler_spot.A100_80GB.spot.median             |  48 |    0.069 |         0.271 |       0.188 |       0.229 |              0.002 |

## Each base model alone: skill by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.065 |
| fastgpu_daily|hyperscaler_spot     |      0.064 |
| fastgpu_daily|neocloud_rate_card   |      0.143 |
| fastgpu_daily|neocloud_spot        |      0.121 |
| gpurentalprices|marketplace_ask    |      0.117 |
| gpurentalprices|neocloud_rate_card |      0.151 |

## Mean ensemble weight by group
| group                              |   momentum |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |          1 |
| fastgpu_daily|hyperscaler_spot     |          1 |
| fastgpu_daily|neocloud_rate_card   |          1 |
| fastgpu_daily|neocloud_spot        |          1 |
| gpurentalprices|marketplace_ask    |          1 |
| gpurentalprices|neocloud_rate_card |          1 |

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
