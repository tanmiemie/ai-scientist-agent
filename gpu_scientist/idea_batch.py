"""Ideas in batches (DEVIN_NEXT task F): each iteration the LLM writes 5 candidate experiments,
scores each 1-10 on expected gain (against the diagnosis' biggest miss), feasibility and novelty vs
the ledger, reflects once on its own batch, and only the top-ranked valid idea is run. Every idea,
run or not, is kept in <experiments>/ideas.json.

    python autoresearch.py --proposer llm --ideas batch --iters 6
    python walkforward.py --proposer llm --ideas batch --iters 6 --run llm_batch
"""
from __future__ import annotations

import json
import re

import config as C
import run_experiment
from autoresearch import SYSTEM, LLMProposer, allowed_models, spec_hash, validate

N_IDEAS = 5
SEED_IDEAS = C.ROOT / "seed_ideas.json"
SCORES = ("gain", "feasibility", "novelty")

BATCH_RULES = f"""

BATCH MODE. Instead of one experiment, write {N_IDEAS} different candidate experiments (different
hypotheses, not {N_IDEAS} values of one parameter; a "sweep" inside an idea is fine). SEED IDEAS lists
starting points from the research protocol; use, combine or ignore them. Score each idea 1-10 on:
  gain:        expected improvement of the primary metric, judged against the BIGGEST miss in the
               diagnosis (the largest group/horizon/condition gap, with its number);
  feasibility: can the allowed models and parameters express it exactly, and will it run as specified;
  novelty:     how different it is from every experiment already in the history (10 = untried idea,
               1 = repeats a tried spec or a rejected idea unchanged).
Reply with JSON only:
{{"biggest_miss": "<the diagnosis number you rank against>",
 "ideas": [{{"seed_id": <id from SEED IDEAS or null>, "observation": ..., "hypothesis": ..., "change": ...,
            "expected_effect": ..., "spec": {{...}}, "sweep": <optional, as above>,
            "scores": {{"gain": <1-10>, "feasibility": <1-10>, "novelty": <1-10>}},
            "why_scores": "<one sentence>"}}, ... {N_IDEAS} ideas]}}"""

REFLECT = f"""Reflect once on your batch before anything is run. For each idea check: is the spec
valid and does every setting have an effect (see the rules)? Is the expected gain really tied to the
biggest miss, or to a small group? Is it a disguised repeat of a history entry? Is a gain of this kind
likely to survive the HOLDOUT gate, or is it fitting noise on ~45 DEV origins? Then fix specs and
re-score. Keep exactly {N_IDEAS} ideas (you may replace a weak one). Reply with JSON only, the same
format plus "reflection": "<what you changed and why, 2-4 sentences>"."""


def total(idea: dict) -> float:
    s = idea.get("scores") or {}
    try:
        return float(sum(min(10.0, max(1.0, float(s.get(k, 1)))) for k in SCORES))
    except (TypeError, ValueError):
        return 0.0


def rank(ideas: list[dict], tried: set, heavy: bool) -> list[dict]:
    """Annotate every idea with its total score and why it can or cannot run; best first."""
    out = []
    for i, idea in enumerate(ideas):
        spec = idea.get("spec") if isinstance(idea, dict) else None
        errs = validate(spec, heavy) if isinstance(spec, dict) and spec else ["no spec returned"]
        if not errs and spec_hash(spec) in tried:
            errs = ["this spec runs exactly like one already tried"]
        out.append({**(idea if isinstance(idea, dict) else {"raw": idea}), "index": i, "total": total(idea or {}),
                    "refused": errs or None})
    # the score decides; position in the reply breaks ties
    return sorted(out, key=lambda r: (-r["total"], -float((r.get("scores") or {}).get("gain", 0) or 0), r["index"]))


class BatchProposer(LLMProposer):
    def __init__(self, provider: str, model: str | None, heavy: bool):
        super().__init__(provider, model, heavy)
        self.seed_ideas = json.loads(SEED_IDEAS.read_text())["ideas"]

    def _json(self, system: str, user: str) -> dict:
        txt = self._chat(system, user, as_json=True)
        m = re.search(r"\{.*\}", txt, re.S)
        try:
            return json.loads(m.group(0)) if m else {}
        except json.JSONDecodeError:
            return {}

    def propose(self, ctx: dict, feedback: str | None = None) -> dict:
        system = SYSTEM.replace("Each turn you propose exactly ONE experiment that tests ONE hypothesis.",
                                f"Each turn you draft {N_IDEAS} candidate experiments; only the best one is run.")
        system += BATCH_RULES
        user = json.dumps({"allowed_models_and_default_params": allowed_models(self.heavy),
                           "champion": ctx["champion"], "history_most_recent_last": ctx["history"],
                           "seed_ideas": self.seed_ideas}, indent=1)
        user += "\n\nDIAGNOSIS OF THE CHAMPION (DEV):\n" + ctx["diagnosis_md"]
        if feedback:
            user += (f"\n\nNo idea of your previous batch could run: {feedback}\n"
                     f"Write a new batch of {N_IDEAS} valid, untried experiments.")
        draft = self._json(system, user)
        final = self._json(system, user + "\n\nYOUR DRAFT BATCH:\n" + json.dumps(draft, indent=1) + "\n\n" + REFLECT)
        if not isinstance(final.get("ideas"), list) or not final["ideas"]:
            final = {**draft, "reflection": "(reflection reply had no ideas; the draft is used)"}
        ideas = [x for x in final.get("ideas", []) if isinstance(x, dict)][:N_IDEAS]
        ranked = rank(ideas, ctx["tried"], self.heavy)
        chosen = next((r for r in ranked if not r["refused"]), None)
        self._record(ctx, draft, final, ranked, chosen, feedback)
        if chosen is None:
            # nothing runnable: hand the top idea back so the loop refuses it with its reason and retries
            return ranked[0] if ranked else {}
        return {k: v for k, v in chosen.items() if k not in ("index", "total", "refused")}

    def _record(self, ctx, draft, final, ranked, chosen, feedback):
        path = C.EXPERIMENTS / "ideas.json"
        log = json.loads(path.read_text()) if path.exists() else []
        log.append({"batch": len(log) + 1, "next_exp_id": run_experiment.next_id(),
                    "champion": ctx["champion"]["id"], "retry_after": feedback,
                    "biggest_miss": final.get("biggest_miss") or draft.get("biggest_miss"),
                    "reflection": final.get("reflection"),
                    "draft": draft.get("ideas"),
                    "ideas": [{**r, "selected": r is chosen} for r in ranked],
                    "selected_index": chosen["index"] if chosen else None})
        path.write_text(json.dumps(log, indent=1, default=str))
