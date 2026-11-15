# Devin: run the autonomous loop with an LLM proposer

PR #2 (merged) added `autoresearch.py` and `walkforward.py`; see "Autonomous loop" in README.md.
The heuristic proposer has been run (`walkforward/heuristic_demo/`: mean TEST gain +0.034, 2/3 slices).
Now run the same check with an LLM proposing the hypotheses, so the two can be compared.

## Steps

1. `git pull` on `devin/gpu-scientist-handoff`.
2. API key: the user sets `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`) as an environment variable or
   secret on this VM. Never write a key into a file, a commit, a log or a chat message. If no key is
   available, stop and say so.
3. Smoke test (one iteration, separate ledger):
   `GPU_EXPERIMENTS=$PWD/experiments_llm_smoke python autoresearch.py --iters 1 --proposer llm --provider openai`
   Check `experiments_llm_smoke/autoresearch_log.jsonl`: the proposal must cite diagnosis numbers and
   the spec must have passed validation. If the default model name is rejected by the API, set
   `GPU_LLM_MODEL` to a model the account can use and say which.
4. Full run:
   `python walkforward.py --proposer llm --provider openai --iters 6 --run llm_openai`
5. Compare `walkforward/llm_openai/summary.md` with `walkforward/heuristic_demo/summary.md`: per-slice
   seed and final TEST skill, gain, and which changes each proposer tried. Use TEST only for this
   comparison, never to pick a spec.
6. Add a section "LLM vs heuristic proposer" to `FINDINGS_devin.md`: the comparison table, 3-5
   representative LLM hypotheses (quote the observation it acted on), any invalid or repeated
   proposals that validation refused, and the number of API calls.
7. Commit `walkforward/llm_openai/` (CSV files are git-ignored), the findings update and the smoke
   ledger to a branch `devin/llm-walkforward`, and open a PR into `devin/gpu-scientist-handoff`.

Do not change the Sunday submission (`submission_final/`) in this PR. Rules from HANDOFF_DEVIN.md still apply.
