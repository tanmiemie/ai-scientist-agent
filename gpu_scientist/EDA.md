# Data quality of the 37 scored series

`python eda.py` reproduces every number here (`eda/EDA_tables.json`, `eda/coverage.png`,
`eda/change_sizes.png`). Scope: the 37 headline rental series as built by the starter kit at
2026-11-06. Prices are posted medians in USD per GPU-hour.

## Summary

| check | finding | what it means for the model |
|---|---|---|
| Missing days | fastgpu: none (but only 60 days, from Sep 8). gpurentalprices: the same 6 days missing on all 13 series (Oct 14, 17, 23, 24, 30, Nov 1). afhubbard: a 58-day hole (Mar–May) plus 4 recent days | Collector outages, not series-level gaps. These gaps caused the look-ahead fixed in PR #10. Targets on those days are not scored |
| Spikes | 31% of series-days carry a change; median size 0.7%, 90th pct 6.4%, 99th pct 30%. 55 moves of 10%+, of which 17 (31%) were half undone within 7 days | Fat tails: a symmetric or Gaussian interval would be badly wrong; empirical, calibrated tails are the right tool |
| Provider counts | 14 of 37 series have a median of 3 or fewer providers. Only 12% of changes coincide with a provider-count change, but 45% of 10%+ moves do; such moves are 7x larger (3.7% vs 0.5%) | Big jumps are mostly composition (who is listed), not repricing. The largest moves are all in the gpurentalprices H100 marketplace-ask median when providers dropped to 1 (−50% on Oct 27, +137% the next day) |
| Dropped rows | 4.57M CPU-only rows and ~120k RunPod/Vast.ai rows were filtered by the pack's build rules | Expected. Marketplace asks therefore exclude the two largest marketplaces |
| Stale series | All 37 observed on Nov 6; median 1 day since the last change; 1 series unchanged for 30+ days | Nothing to drop |
| Levels and units | $0.09 to $9.75 per GPU-hour, consistent with per-GPU pricing. The same GPU and class differs across collectors: B200 rate cards $6.30 vs $7.89, RTX A6000 $0.50 vs $0.71, T4 spot $0.31 vs $0.09 | Collectors see different provider sets; never mix collectors in one series (as the brief says) |

## Checked against the champion (exp_004, DEV cells)

| providers at origin | cells | skill | above q90 | below q10 |
|---|---|---|---|---|
| 3 or fewer | 1,253 | 0.116 | 0.101 | 0.098 |
| 4 to 5 | 748 | 0.180 | 0.124 | 0.158 |
| more than 5 | 1,229 | 0.220 | 0.128 | 0.072 |

Thin series are the hardest to beat (skill 0.12 vs 0.22), but online calibration already keeps their
misses near 10% each side, so a blanket widening for thin series is not the fix. The 4-5 provider
bucket is under-covered on the downside (15.8% below q10): a candidate hypothesis for the loop
(calibration by provider-count bucket).

## Caveats

- The catalog notes that **the trailing day of tanod and gpurentalprices can be revised upstream**. Our
  q50 for those series equals the Nov 6 value; a revision of that day would move it. Its size cannot be
  measured from one snapshot.
- fastgpu history starts on Sep 8, so its series have ~60 days; DEV origins begin on Sep 15.

## Hypotheses this adds to the loop

1. Calibration by provider-count bucket (target the 4-5 bucket's downside misses).
2. Partial reversion after a 10%+ move that coincided with a provider-count change.
