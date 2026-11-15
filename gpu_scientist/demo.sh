#!/usr/bin/env bash
# Live demo of the autonomous loop, ~1 minute from a clean clone with the pack beside this folder.
#   bash demo.sh          heuristic proposer (no API key needed)
#   bash demo.sh --llm    LLM proposer if OPENAI_API_KEY or ANTHROPIC_API_KEY is set, else heuristic
# Rebuilds the series, seeds a fresh ledger (demo_run/experiments) with specs/02_trend_tail_cal.json,
# runs 2 iterations of autoresearch.py, prints each hypothesis, decision and lesson, and the plot path.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
PY="${PYTHON:-python3}"

proposer=(--proposer heuristic)
if [[ "${1:-}" == "--llm" ]]; then
  if [[ -n "${OPENAI_API_KEY:-}" ]]; then proposer=(--proposer llm --provider openai)
  elif [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then proposer=(--proposer llm --provider anthropic)
  else echo "--llm: no OPENAI_API_KEY or ANTHROPIC_API_KEY in the environment; using the heuristic proposer"; fi
fi

export GPU_EXPERIMENTS="$PWD/demo_run/experiments"
rm -rf demo_run
start=$SECONDS

echo "== 1/3 rebuild the official series from the pack (starter kit build_series.py)"
"$PY" -c "import data; s, c = data.build(force=True); print('  ', s)"

echo "== 2/3 seed a fresh ledger with specs/02_trend_tail_cal.json, then 2 iterations (${proposer[*]})"
"$PY" autoresearch.py --iters 2 --max-rejects 3 "${proposer[@]}" --seed specs/02_trend_tail_cal.json \
  2>&1 | grep -v -e FutureWarning -e "g = df.groupby"

echo "== 3/3 what the scientist did"
"$PY" - <<'PY'
import json, textwrap
import config as C
recs = [json.loads(l) for l in open(C.EXPERIMENTS / "ledger.jsonl") if l.strip()]
k = C.PRIMARY_METRIC
for r in recs:
    print(f"\n[{r['id']}] {'ACCEPTED' if r['accepted'] else 'rejected'}   DEV {r['dev'][k]:+.4f}   "
          f"HOLDOUT {r['holdout'][k]:+.4f}   coverage {r['dev']['coverage_in']:.2f}")
    print(textwrap.fill("hypothesis: " + r["hypothesis"], 100, subsequent_indent="    "))
    print(textwrap.fill("decision:   " + r["reason"], 100, subsequent_indent="    "))
    print(textwrap.fill("lesson:     " + (r.get("lesson") or ""), 100, subsequent_indent="    "))
champ = json.loads((C.EXPERIMENTS / "champion.json").read_text())
print(f"\nchampion: {champ['id']}  DEV {champ['dev'][k]:+.4f}  HOLDOUT {champ['holdout'][k]:+.4f}")
PY

png="$GPU_EXPERIMENTS/progress.png"
echo
echo "progress plot: $png"
if [[ -z "${DEMO_NO_OPEN:-}" ]]; then
  if command -v open >/dev/null 2>&1 && [[ "$(uname)" == "Darwin" ]]; then open "$png" || true
  elif command -v xdg-open >/dev/null 2>&1 && [[ -n "${DISPLAY:-}" ]]; then xdg-open "$png" >/dev/null 2>&1 || true; fi
fi
echo "demo finished in $((SECONDS - start)) s"
