# Reviewer ensemble (Devin task D)

`review.py` sends one experiment's evidence to an LLM five times (temperature 0.1) with a fixed checklist and keeps an item only if at least 3 of 5 reviews flag it. It writes `<exp>/review.json`. `report.py` prints the kept flags under each experiment in `REPORT.md`. Flags never change the numeric gate's decision.

The evidence is computed by `review.py` from files the loop already writes, for this experiment and the champion it was compared with:
- hypothesis, gate decision, spec diff (`report._diff`)
- DEV and HOLDOUT pooled / median / geomean skill, coverage, skill by horizon
- DEV per-series loss change: series better/worse, the 3 largest changes, and their share of the absolute change
- DEV skill by collector x class
- mean log(q90/q10) on DEV and HOLDOUT origins (from `forecast_all.csv[.gz]`)
- earlier rejected hypotheses and their lessons from the ledger
- `diagnosis.md` (DEV only, first 6000 characters)

No TEST data is used.

```
cp -r experiments_final experiments_review
GPU_EXPERIMENTS=experiments_review python review.py --all          # OPENAI_API_KEY; --provider anthropic also works
```

## Run on exp_001-exp_007 (gpt-4.1, 35 calls, in a copy: `experiments_review/`)

`experiments_final/` and `submission_final/` are unchanged. Only `review.json` and `REPORT.md` from the copy are committed.

| exp | gate | kept flags (votes/5, severity) |
|---|---|---|
| 001 | kept | interval widened (5, 2) |
| 002 | kept | few series (5, 2); interval widened (5, 2); other: DEV/HOLDOUT gap (5, 2) |
| 003 | rejected | few series (3, 2); interval widened (3, 2); other: DEV lower than champion (5, 2) |
| 004 | kept | other: DEV/HOLDOUT gap (5, 2) |
| 005 | rejected | few series (5, 2); repeats rejected idea (5, 2); **other: HOLDOUT 0.022 vs champion 0.100, overfitting (5, 3)** |
| 006 | rejected | interval widened (5, 2); other: DEV −0.051 vs champion, HOLDOUT +0.088 (5, 2) |
| 007 | kept | few series (5, 2); other: DEV gain +0.0036 may not generalise (5, 2) |

No experiment got a leakage flag.

## Agreement with the known cases

- **exp_005 (per-GPU calibration overfit): caught.** It is the only experiment with a severity-3 flag, and the evidence is the right one: HOLDOUT 0.022 vs 0.100 for the champion. The `few series` flag also fits: the largest change is a gain of 0.587 on one B200 series, offset by losses on two others. Two parts are wrong:
  - `repeats_rejected_idea` points at `trend_tail` from exp_003, but exp_003 tested hedge weights, not calibration groups.
  - Reviewers did not flag that the DEV gain came from narrower intervals (width 0.066 vs 0.092, coverage 0.74 vs 0.78). The checklist only asks about the opposite case.
- **exp_006 (Chronos lost on DEV): caught**, as `other` with the right numbers (DEV −0.051, HOLDOUT +0.088). The `interval widened` flag is a misfire: the item is about a score that improved because intervals widened, and exp_006's DEV score fell.

## What the flags are worth

- **Discriminating:** severity 3, and `repeats_rejected_idea` (only on exp_005).
- **Weak:** `gain_from_few_series` fired on 4 of 7 experiments.
- **Mostly noise:**
  - `other` fired 5/5 on 6 of 7 experiments. In 3 of these, the only point is DEV skill being higher than HOLDOUT. That gap exists for every experiment, including the champion, because HOLDOUT is a different, harder period. A useful reviewer would compare the gap to the champion's.
  - `interval_widened_not_centred` was correct for exp_001 and exp_002: the calibration steps did widen intervals, and that was the intended fix for under-coverage. The flag is accurate, but it is not a defect.
- **Agreement across reviewers is very high:** 19 of the 21 kept flags had 5/5 votes, so 5 runs at temperature 0.1 behave close to one review. Disagreement would need different prompts or models, not just more samples.

Possible next steps (not done):
- Give the reviewer the champion's own DEV/HOLDOUT gap as the reference.
- Add a "narrowed intervals" item.
- Report only severity ≥ 2 flags whose evidence names a number different from the champion's.
