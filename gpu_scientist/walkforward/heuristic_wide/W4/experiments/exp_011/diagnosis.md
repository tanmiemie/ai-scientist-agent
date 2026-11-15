# Diagnosis (dev origins only)

Cells: 2322. Overall skill 0.1947; truth above q50 in 46% of cells (50% if unbiased); above q90 16% and below q10 10% (10% each if calibrated).

## By series group
| group                              |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-----------------------------------|----:|--------:|--------------:|------------:|------------:|-------------------:|
| afhubbard|hyperscaler_spot         | 264 |   0.147 |         0.239 |       0.068 |       0.057 |              0.001 |
| fastgpu_daily|hyperscaler_spot     | 120 |   0.151 |         0.275 |       0.167 |       0.183 |              0.004 |
| fastgpu_daily|neocloud_rate_card   | 660 |   0.172 |         0.539 |       0.162 |       0.13  |              0.004 |
| fastgpu_daily|neocloud_spot        | 420 |   0.207 |         0.371 |       0.186 |       0.143 |              0.011 |
| gpurentalprices|marketplace_ask    |  66 |   0.104 |         0.227 |       0.03  |       0.076 |             -0.019 |
| gpurentalprices|neocloud_rate_card | 792 |   0.238 |         0.548 |       0.197 |       0.059 |              0.021 |

## By horizon
|   horizon_days |   n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|---------------:|----:|--------:|--------------:|------------:|------------:|-------------------:|
|              1 | 774 |   0.075 |         0.305 |       0.119 |       0.097 |              0.003 |
|              3 | 774 |   0.14  |         0.468 |       0.137 |       0.103 |              0.008 |
|              7 | 774 |   0.249 |         0.593 |       0.236 |       0.103 |              0.02  |

## By days since the last price change at the origin
| dsc_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:-------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| 0-1          | 1185 |   0.215 |         0.586 |       0.159 |       0.089 |              0.012 |
| 2-3          |  294 |   0.176 |         0.459 |       0.153 |       0.068 |              0.012 |
| 4-7          |  216 |   0.231 |         0.444 |       0.194 |       0.111 |              0.011 |
| 8-30         |  483 |   0.072 |         0.205 |       0.176 |       0.178 |              0.001 |
| >30          |  144 |   0.155 |         0.229 |       0.139 |       0     |              0.016 |

## By change in provider count over the 7 days before the origin
| prov_bucket   |    n |   skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:--------------|-----:|--------:|--------------:|------------:|------------:|-------------------:|
| fewer         |   90 |   0.082 |         0.367 |       0.122 |       0.189 |              0.009 |
| more          |  273 |   0.145 |         0.568 |       0.11  |       0.081 |              0.019 |
| same          | 1959 |   0.217 |         0.444 |       0.174 |       0.1   |              0.009 |

## Worst series
| series_id                                                |   n |    skill |   y_above_q50 |   above_q90 |   below_q10 |   mean_log_err_q50 |
|:---------------------------------------------------------|----:|---------:|--------------:|------------:|------------:|-------------------:|
| fastgpu_daily.neocloud_spot.A100_80GB.spot.median        |  60 | -inf     |         0     |       0     |       0     |              0     |
| afhubbard.hyperscaler_spot.A100_40GB.spot.median         |  66 |   -0.591 |         0     |       0     |       0.106 |             -0.003 |
| gpurentalprices.neocloud_rate_card.L4.on_demand.median   |  66 |   -0.113 |         0.106 |       0.015 |       0.212 |             -0.004 |
| fastgpu_daily.hyperscaler_spot.T4.spot.median            |  60 |   -0.036 |         0.233 |       0.183 |       0.167 |              0.005 |
| fastgpu_daily.neocloud_spot.B200.spot.median             |  60 |   -0.013 |         0.1   |       0     |       0.9   |             -0.003 |
| gpurentalprices.neocloud_rate_card.L40S.on_demand.median |  66 |   -0.001 |         0.197 |       0     |       0     |              0.004 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median |  66 |    0.019 |         0.515 |       0.242 |       0     |              0.009 |
| gpurentalprices.neocloud_rate_card.B200.on_demand.median |  66 |    0.052 |         0.742 |       0.212 |       0.045 |              0.009 |

## Each base model alone: skill by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |      0.168 |
| fastgpu_daily|hyperscaler_spot     |      0.136 |
| fastgpu_daily|neocloud_rate_card   |      0.13  |
| fastgpu_daily|neocloud_spot        |      0.184 |
| gpurentalprices|marketplace_ask    |      0.108 |
| gpurentalprices|neocloud_rate_card |      0.154 |

## Mean ensemble weight by group
| group                              |   vol_tail |
|:-----------------------------------|-----------:|
| afhubbard|hyperscaler_spot         |          1 |
| fastgpu_daily|hyperscaler_spot     |          1 |
| fastgpu_daily|neocloud_rate_card   |          1 |
| fastgpu_daily|neocloud_spot        |          1 |
| gpurentalprices|marketplace_ask    |          1 |
| gpurentalprices|neocloud_rate_card |          1 |

## Candidate leading signals (same GPU, other collector, moves `lag_days` earlier)
| series                                                            | leader                                                                  |   lag_days |   corr |
|:------------------------------------------------------------------|:------------------------------------------------------------------------|-----------:|-------:|
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_list.A100_40GB.on_demand.median             |          5 |  0.997 |
| gpurentalprices.neocloud_rate_card.A100_40GB.on_demand.median     | gpurentalprices.hyperscaler_spot.A100_40GB.spot.median                  |          5 |  0.994 |
| gpurentalprices.neocloud_rate_card.RTX_PRO_6000.on_demand.median  | gpurentalprices.neocloud_rate_card.RTX_PRO_6000.serverless.median       |          2 |  0.933 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_list.H100_SXM_80GB.on_demand.median         |          5 |  0.913 |
| gpurentalprices.neocloud_rate_card.H100_SXM_80GB.on_demand.median | gpurentalprices.hyperscaler_spot.H100_SXM_80GB.spot.median              |          5 |  0.913 |
| gpurentalprices.neocloud_rate_card.H100_80GB.on_demand.median     | afhubbard.neocloud_rate_card.H100_80GB.on_demand.median                 |          4 |  0.868 |
| gpurentalprices.neocloud_rate_card.RTX_6000_Ada.on_demand.median  | afhubbard.neocloud_rate_card.RTX_6000_Ada.on_demand.median              |          1 |  0.86  |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.neocloud_rate_card.B300.on_demand.median                      |          1 |  0.712 |
| gpurentalprices.neocloud_rate_card.RTX_A6000.on_demand.median     | gpurentalprices_cheapest.aggregator_cheapest.RTX_A6000.on_demand.median |          2 | -0.712 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | gpurentalprices.neocloud_rate_card.B300.serverless.median               |          1 |  0.703 |
| gpurentalprices.neocloud_rate_card.B300.on_demand.median          | afhubbard.hyperscaler_list.B300.on_demand.median                        |          2 | -0.648 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.neocloud_rate_card.H200.serverless.median               |          2 |  0.586 |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | afhubbard.neocloud_rate_card.H200.on_demand.median                      |          2 |  0.57  |
| gpurentalprices.neocloud_rate_card.H200.on_demand.median          | gpurentalprices.hyperscaler_list.H200.on_demand.median                  |          1 | -0.538 |
| gpurentalprices.marketplace_ask.H100_80GB.spot.median             | gpurentalprices.neocloud_rate_card.H100_80GB.serverless.median          |          1 | -0.504 |
