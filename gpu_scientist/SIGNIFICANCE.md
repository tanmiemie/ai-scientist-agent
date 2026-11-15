# Are the gains real per series? (`python significance.py`)

Prompted by Hewamalage, Ackermann & Bergmeir (2023), *Forecast evaluation for data scientists:
common pitfalls and best practices*, Data Mining and Knowledge Discovery 37(2). Two of its pitfalls
apply to us: an aggregate error over series of different scale is driven by the largest series, and
differences against benchmarks need a statistical test.

Our gate uses **pooled** skill, a ratio of summed pinball losses in USD. A B300 hour costs about $10 and
a T4 hour $0.09, so pooled skill mostly reflects expensive GPUs. Below, every series counts once:
Wilcoxon signed-rank test (one-sided) on the per-series log ratio of total pinball loss.

| comparison | DEV: better / worse, p | HOLDOUT: better / worse, p |
|---|---|---|
| champion (07) vs last value | 30 / 6, p = 0.0003 | **27 / 7, p = 0.006** |
| champion (07) vs starter drift | 28 / 8, p = 0.006 | **21 / 15, p = 0.52** |
| 07 vs 04 (last upgrade) | 26 / 4, p < 0.001 | 15 / 16, p = 0.48 |

Scale-free aggregates from the official ledger (skill vs last value):

| exp | pooled DEV / HOLDOUT | geomean DEV / HOLDOUT | median DEV / HOLDOUT |
|---|---|---|---|
| 000 drift | +0.071 / +0.044 | +0.060 / +0.064 | +0.029 / +0.072 |
| 001 trend_tail | +0.168 / +0.090 | +0.166 / **+0.142** | +0.154 / +0.182 |
| 002 + calibration | +0.183 / +0.097 | +0.119 / +0.054 | +0.185 / +0.164 |
| 007 champion | +0.191 / +0.101 | +0.126 / +0.061 | +0.179 / +0.166 |

## What this says

1. **The champion beats the last value on unseen data, per series and significantly** (27 of 34 series,
   p = 0.006). This is the strongest, scale-free claim we can make.
2. **Against the starter drift, the unseen-data gain is not significant per series** (p = 0.52). The pooled
   gain over drift comes mostly from expensive GPUs.
3. **Online calibration traded cheap-series skill for expensive-series skill.** It raised pooled skill and
   coverage, but cut HOLDOUT geomean from +0.142 to +0.054. A gate on pooled skill alone could not see this.
4. The last two upgrades (04, 07) are significant on DEV, where they were selected, and flat on HOLDOUT:
   they are fine-tuning, not new capability.

## Consequences

- Which aggregate ranks teams on Sunday matters. If it is pooled, the champion is the right file. If it is
  per-series (median or geomean), exp_001 (no calibration) scored better on HOLDOUT geomean.
- Next gate: require no loss in geomean as well as a pooled gain, and make calibration scale-aware
  (per series, or offsets proportional to each series' own volatility).
