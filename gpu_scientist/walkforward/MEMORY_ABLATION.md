# Memory ablation (Devin task C)

Does the proposer's memory (past hypotheses and lessons in the prompt) matter? Same 3-slice walk-forward, gpt-4.1, seed `00_drift.json`, 6 iterations per slice. The only difference is `--no-memory`. With that flag, the proposer sees the champion and its DEV diagnosis but no history. The duplicate-spec check in `autoresearch.py` is unchanged in both arms. Each arm was run twice because LLM runs are not deterministic (`llm_mem`, `llm_mem_2`, `llm_nomem`, `llm_nomem_2`): 12 slice runs in total.

```
python walkforward.py --proposer llm --provider openai --iters 6 --run llm_mem
python walkforward.py --proposer llm --provider openai --iters 6 --run llm_nomem --no-memory
python scratch/memory_ablation_table.py -v      # the table below
```

## Per slice

Column definitions:
- **acc / rej:** experiments the gate accepted or rejected.
- **refused iters:** iterations lost because all 3 proposals were refused.
- **refused props:** every refused proposal.
- **repeats of rejected:** proposals, including refused ones, that are the same experiment as one already rejected in that slice. Same experiment means the same spec, or an equivalent one (`gamma*scale` is the only quantity calibration uses).
- **variants:** executed experiments that turn the same knob in the same direction as a rejected one, with a different value.

| run | slice | seed TEST | final TEST | champion | acc | rej | refused iters | refused props | repeats of rejected | variants |
|---|---|---|---|---|---|---|---|---|---|---|
| mem | S1 | 0.1449 | 0.2021 | exp_004 | 2 | 4 | 0 | 2 | 0 | 1 |
| mem | S2 | 0.0217 | 0.0877 | exp_001 | 1 | 5 | 0 | 0 | 0 | 0 |
| mem | S3 | 0.0774 | 0.0787 | exp_005 | 2 | 4 | 0 | 0 | 0 | 1 |
| mem_2 | S1 | 0.1449 | 0.2165 | exp_004 | 2 | 4 | 0 | 3 | 1 | 0 |
| mem_2 | S2 | 0.0217 | 0.0877 | exp_001 | 1 | 5 | 0 | 0 | 0 | 1 |
| mem_2 | S3 | 0.0774 | 0.0787 | exp_002 | 2 | 4 | 0 | 0 | 0 | 1 |
| nomem | S1 | 0.1449 | 0.2115 | exp_004 | 2 | 3 | 1 | 5 | 4 | 1 |
| nomem | S2 | 0.0217 | 0.0877 | exp_001 | 1 | 5 | 0 | 1 | 1 | 0 |
| nomem | S3 | 0.0774 | 0.0211 | exp_002 | 2 | 3 | 1 | 4 | 2 | 0 |
| nomem_2 | S1 | 0.1449 | 0.2304 | exp_001 | 1 | 5 | 0 | 3 | 3 | 0 |
| nomem_2 | S2 | 0.0217 | 0.0877 | exp_001 | 1 | 4 | 1 | 4 | 4 | 0 |
| nomem_2 | S3 | 0.0774 | 0.0574 | exp_001 | 1 | 4 | 1 | 4 | 3 | 0 |

| arm (2 runs x 3 slices) | mean TEST gain over seed | repeats of rejected | iterations lost | variants |
|---|---|---|---|---|
| memory | +0.0439 (+0.0415, +0.0463) | **1** | **0 / 36** | 4 |
| no memory | +0.0346 (+0.0254, +0.0438) | **17** | **4 / 36** | 1 |

## The repeats

- **With memory:** 1 repeat. In `mem_2` S1 the proposer suggested `gamma 1.0, scale 0.01`, which is equivalent to the rejected `scale 0.02`. It was refused.
- **Without memory:** 17 repeats. All of them were refused by the duplicate check, so none was run twice.
  - nomem S1: `gamma 1.0` (rejected exp_002) once; `scale 0.02`, which is equivalent, twice; `gamma 1.0` again once. The last 3 cost a whole iteration.
  - nomem S2: `group_by series_id` (rejected exp_003) once.
  - nomem S3: `group_by series_id` (rejected exp_003) twice. This cost a whole iteration.
  - nomem_2 S1: `scale 0.02` (rejected exp_003) 3 times.
  - nomem_2 S2: `group_by series_id` (rejected exp_002) 4 times. Three of them cost a whole iteration.
  - nomem_2 S3: `group_by series_id` (rejected exp_003) 3 times. This cost a whole iteration.
- **Variants,** which are not counted as repeats: the same knob in the same direction after a rejection.
  - With memory:
    - `scale 0.012` after `0.02` (mem S1)
    - `scale 0.015` after `0.02` (mem S3)
    - `gamma 0.35` after `0.25` (mem_2 S2)
    - hedge grouped by `series_id` after hedge grouped by `instrument_class` (mem_2 S3)
  - Without memory: `scale 0.015` after `gamma 1.0` (nomem S1).
  - In the memory runs, the hypotheses cite the earlier failure and explain the smaller step, e.g. "Increasing calibrate.scale from 0.01 to 0.02 caused a drastic skill_pooled drop ... therefore, tune ..."
- **Other refused proposals** that are not repeats of a rejected idea:
  - With memory: 4 refusals of specs equal to an earlier accepted champion (e.g. re-proposing calibration by `instrument_class` when that is already the champion's setting).
  - Without memory: 1 such refusal, plus 1 out-of-range `group_by` (`dsc_bucket`).

## Verdict

- **Memory changes the search process.**
  - Without it, the proposer keeps coming back to the same rejected idea, `series_id` calibration or a wider `scale`: 17 times vs 1.
  - 4 of 36 iterations were lost because all 3 retries were refused.
  - The duplicate check in `autoresearch.py` stops these repeats from being re-run or re-scored. Without that check, the no-memory arm would have re-run rejected experiments.
- **On the TEST score the result is null.**
  - Mean gain is +0.044 with memory vs +0.035 without. With 2 runs per arm, the range inside each arm (+0.042 to +0.046 vs +0.025 to +0.044) overlaps.
  - The whole gap comes from S3: the memory runs found `leader + mean` (TEST 0.079), while `nomem` accepted `group_by source_class`, which fell to 0.021 on TEST.
  - S2 is identical in all four runs: only the first calibration step was accepted.
  - On S1, the no-memory arm is slightly ahead (0.221 vs 0.209 mean final TEST).
  - Six iterations per slice is probably too short a budget for the lost iterations to show up in TEST skill.

API calls: 38, 39 (memory) and 42, 43 (no memory) per run, counted from `autoresearch_log.jsonl`; the no-memory runs needed more retries; keys were read from the environment only. `experiments_final/` and `submission_final/` are unchanged.
