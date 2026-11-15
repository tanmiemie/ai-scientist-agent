# Hindsight-free and per-collector checks (`python honest_eval.py`)

**Series chosen before HOLDOUT.** The 37 scored series were chosen with data up to Nov 6. Rebuilding the
headline set with data up to Oct 15 (the day before HOLDOUT) gives 17 series (13 gpurentalprices, 4
afhubbard; the 20 fastgpu series did not yet have enough history). HOLDOUT on those 17:

| spec | pooled | median of series | geomean | coverage |
|---|---|---|---|---|
| 00 drift | +0.156 | +0.146 | +0.155 | 0.59 |
| 01 trend_tail (no calibration) | **+0.169** | **+0.197** | **+0.188** | 0.69 |
| 02 + calibration | +0.095 | +0.160 | +0.107 | 0.69 |
| 07 champion | +0.112 | +0.156 | +0.118 | 0.70 |

Per series (Wilcoxon, one-sided): the champion beats the last value (13 of 16, p = 0.013) but not drift
(8 of 17, p = 0.80) and not trend_tail without calibration (5 of 17).

**HOLDOUT on all 37, by collector (pooled skill):**

| collector | drift | trend_tail | champion |
|---|---|---|---|
| fastgpu (20 series) | −0.034 | +0.036 | **+0.094** |
| gpurentalprices (13) | +0.158 | **+0.162** | +0.097 |
| afhubbard (4) | +0.136 | +0.226 | **+0.239** |

## Reading

- Online calibration helped on DEV for every collector, and keeps helping fastgpu on HOLDOUT, but its DEV
  gain on gpurentalprices did not carry into late October. That collector had outages on Oct 23, 24 and
  30 and its largest spikes on Oct 27-28 in the same window (EDA.md); the S3 walk-forward week (Oct 24-30)
  showed the same reversal.
- Choosing per-collector models from these HOLDOUT numbers would be selection on HOLDOUT, so the champion
  and the Sunday file are unchanged. The next research step is calibration that adapts faster, or resets,
  after outages and composition spikes, judged on new weeks.
- Robust claim: the system beats "no change" per series on data it never saw, with or without hindsight in
  the series selection.
