"""Closed-loop AI scientist: runs the research loop with no human in it.

Every iteration:
  1. read the memory (ledger with lessons) and the champion's automatic diagnosis,
  2. a proposer writes ONE hypothesis and the experiment spec that tests it,
  3. the spec is validated (known models and parameters only, not a repeat of anything tried),
  4. run_experiment.run() evaluates it with the official scorer and applies the fixed accept rule,
  5. the proposer writes the lesson, which is stored in the ledger for the next iteration.
It stops after --iters iterations or after --max-rejects rejections in a row.

Proposers
  llm        an LLM chooses (OpenAI or Anthropic API; key from OPENAI_API_KEY / ANTHROPIC_API_KEY,
             model from GPU_LLM_MODEL). Prompts and replies are logged in autoresearch_log.jsonl.
  heuristic  a deterministic rule-based scientist that maps diagnosis numbers to mutations of the
             champion. No API needed; used for offline runs and as a control for the LLM.

The proposer can only recombine and retune registered models (models/m_*.py); it does not write
code, so a run can never break the pipeline or touch the evaluation.

  python autoresearch.py --iters 6 --proposer llm --provider openai
  python autoresearch.py --iters 6 --proposer heuristic
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import urllib.request

import config as C
import ledger
import models as M
import run_experiment

HEAVY = {"chronos", "chronos2", "timestral"}          # need extra installs and weights
GROUPS = ["all", "source_class", "instrument_class", "source_id", "gpu_model", "series_id"]
SEED_SPEC = C.ROOT / "specs" / "04_momentum.json"


# ---------------------------------------------------------------- search space and validation
def allowed_models(heavy: bool) -> dict:
    return {n: dict(cls.defaults) for n, cls in M.REGISTRY.items() if heavy or n not in HEAVY}


def validate(spec: dict, heavy: bool) -> list[str]:
    errs, am = [], allowed_models(heavy)
    ms = spec.get("models")
    if not isinstance(ms, list) or not 1 <= len(ms) <= 4:
        return ["spec.models must be a list of 1-4 models"]
    for m in ms:
        name = m.get("name")
        if name not in am:
            errs.append(f"unknown or disallowed model {name!r}; allowed: {sorted(am)}")
            continue
        for k, v in (m.get("params") or {}).items():
            if k not in am[name]:
                errs.append(f"{name}: unknown param {k!r}; allowed: {sorted(am[name])}")
            elif not isinstance(v, (int, float)) or isinstance(v, bool):
                if not (am[name][k] is None or isinstance(am[name][k], str)):
                    errs.append(f"{name}.{k} must be a number")
    comb = spec.get("combine", {"method": "single"})
    if comb.get("method") not in ("single", "mean", "hedge"):
        errs.append("combine.method must be single, mean or hedge")
    if comb.get("method") == "single" and len(ms) > 1:
        errs.append("combine.method single uses only the first model; use mean or hedge for several")
    if "group_by" in comb and comb["group_by"] not in GROUPS:
        errs.append(f"combine.group_by must be one of {GROUPS}")
    if not 0 < float(comb.get("eta", 1.0)) <= 10:
        errs.append("combine.eta must be in (0, 10]")
    cal = spec.get("calibrate", {})
    if cal.get("enabled"):
        if not 0 < float(cal.get("gamma", 0.5)) <= 3:
            errs.append("calibrate.gamma must be in (0, 3]")
        if not 0 < float(cal.get("scale", 0.01)) <= 0.05:
            errs.append("calibrate.scale must be in (0, 0.05]")
        if cal.get("group_by", "instrument_class") not in GROUPS:
            errs.append(f"calibrate.group_by must be one of {GROUPS}")
    return errs


def clean(spec: dict) -> dict:
    return {k: v for k, v in spec.items() if not k.startswith("_")}


COMBINE_DEFAULTS = {"method": "single", "eta": 2.0, "group_by": "instrument_class"}
CAL_DEFAULTS = {"enabled": False, "gamma": 0.5, "scale": 0.01, "group_by": "instrument_class"}


def normalize(spec: dict) -> dict:
    """The spec as the pipeline actually runs it: defaults filled in, settings that have no effect
    dropped (eta/group_by unless hedge, models after the first under single, calibration settings
    when calibration is off). Two specs with the same normal form are the same experiment."""
    s = clean(spec)
    comb = {**COMBINE_DEFAULTS, **s.get("combine", {})}
    if comb["method"] != "hedge":
        comb = {"method": comb["method"]}
    ms = s.get("models", [])[:1] if comb["method"] == "single" else s.get("models", [])
    models = []
    for m in ms:
        d = dict(M.REGISTRY[m["name"]].defaults) if m.get("name") in M.REGISTRY else {}
        models.append({"name": m.get("name"), "params": {**d, **(m.get("params") or {})}})
    cal = {**CAL_DEFAULTS, **s.get("calibrate", {})}
    if not cal["enabled"]:
        cal = {"enabled": False}
    else:   # online.py only uses gamma * scale, so specs with the same product are the same model
        cal = {"enabled": True, "step": round(float(cal["gamma"]) * float(cal["scale"]), 12), "group_by": cal["group_by"]}
    return {"models": models, "combine": comb, "calibrate": cal}


def spec_hash(spec: dict) -> str:
    return hashlib.sha1(json.dumps(normalize(spec), sort_keys=True, default=str).encode()).hexdigest()[:10]


# ---------------------------------------------------------------- context the proposer sees
USE_EXA = False    # set by --exa: outside evidence from exa_scout.py each iteration
NO_MEMORY = False  # set by --no-memory: the proposer sees no past hypotheses or lessons (ablation)


def context(n_recent: int = 15) -> dict:
    champ = json.loads((C.EXPERIMENTS / "champion.json").read_text())
    diag_path = C.EXPERIMENTS / champ["id"] / "diagnosis.md"
    diag_json = json.loads((C.EXPERIMENTS / champ["id"] / "diagnosis.json").read_text())
    recs = ledger.load()
    hist = [{"id": r["id"], "accepted": r["accepted"], "dev": round(r["dev"][C.PRIMARY_METRIC], 4),
             "holdout_gate_passed": r["accepted"], "coverage_dev": round(r["dev"]["coverage_in"], 3),
             "hypothesis": r["hypothesis"][:300], "lesson": (r.get("lesson") or "")[:300],
             "spec": clean(r["spec"])} for r in recs[-n_recent:]]
    if NO_MEMORY:
        hist = []  # ablation: champion + diagnosis only; exact-duplicate specs are still refused below
    return {"champion": {"id": champ["id"], "spec": clean(champ["spec"]),
                         "dev": {k: champ["dev"][k] for k in ("skill_pooled", "skill_median_of_series",
                                                               "skill_geomean", "coverage_in",
                                                               "coverage_above_q90", "coverage_below_q10")}},
            "diagnosis_md": diag_path.read_text()[:7000], "diagnosis": diag_json, "history": hist,
            "tried": {spec_hash(r["spec"]) for r in recs}}


# ---------------------------------------------------------------- LLM proposer
SYSTEM = """You are the research agent of a self-improving forecaster of posted GPU rental prices
(0.1/0.5/0.9 quantiles at 1, 3 and 7 days; scored by pinball loss relative to the last value; target
interval coverage 0.80). Each turn you propose exactly ONE experiment that tests ONE hypothesis.

Rules:
- Ground the hypothesis in specific numbers from the diagnosis (DEV data only).
- Build on the champion; change one thing. Never repeat a spec that was already tried.
- Learn from the history: rejected ideas and their lessons tell you what not to try again unchanged.
- Gains under ~0.005 are noise. A DEV gain that comes with lower coverage is usually overfitting.
- You may only use the models and parameters listed below. You cannot write code.

Spec format:
{"models": [{"name": <model>, "params": {...}}, ...],
 "combine": {"method": "single"|"mean"|"hedge", "eta": <float>, "group_by": <group>},
 "calibrate": {"enabled": true|false, "gamma": <float>, "scale": <float>, "group_by": <group>}}
"single" uses only the first model; "mean" weights equally; only "hedge" uses eta and group_by.
Ranges and defaults (a value outside a range is refused):
  combine.eta in (0, 10], default 2.0 (hedge only: how fast weights follow recent loss)
  calibrate.gamma in (0, 3], default 0.5 (step size of the online interval correction)
  calibrate.scale in (0, 0.05], default 0.01 (log-price units per step; 0.01 is about 1%)
  Only the product gamma * scale matters: changing one while keeping the product is no change.
  calibrate.group_by / combine.group_by: one of """ + ", ".join(GROUPS) + """ (default instrument_class)
Settings that have no effect (eta or group_by without hedge, calibration settings with enabled
false, extra models under single) make the spec identical to the champion and are refused.

Reply with JSON only:
{"observation": "<the number(s) you act on>", "hypothesis": "<what you expect and why>",
 "change": "<the one change vs the champion>", "expected_effect": "<which groups/metric should move>",
 "spec": {...},
 "source_url": <url or null>,
 "sweep": {"param": "<dotted path in spec, e.g. models.0.params.window or calibrate.gamma>",
           "values": [<2 to 5 values>]}}
If OUTSIDE EVIDENCE (web results found by Exa, dated on or before this run's cutoff) is given, you may
build on it: a method to borrow, or market context that explains a pattern in the diagnosis. Put the URL
you relied on in "source_url" (or null if none), and still express the idea with the allowed models
and parameters. Never treat a web claim as a result: the experiment tests it.
"sweep" is optional: use it when the right value of one numeric parameter is unknown. Each value is
scored on DEV only; only the best one is run as the experiment and meets the HOLDOUT gate."""

LESSON_SYSTEM = """You write the one- or two-sentence lesson for a research ledger. State what the
numbers showed (dev and holdout change vs champion, coverage) and what it implies for the next
experiment. Plain text, no preamble."""


class LLMProposer:
    def __init__(self, provider: str, model: str | None, heavy: bool):
        self.provider, self.heavy = provider, heavy
        self.model = model or os.environ.get("GPU_LLM_MODEL") or (
            "gpt-4.1" if provider == "openai" else "claude-sonnet-5-5")
        key_env = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
        self.key = os.environ.get(key_env)
        if not self.key:
            raise SystemExit(f"set {key_env} in your environment (never paste keys into chat or code)")
        self.calls = []

    def _chat(self, system: str, user: str, as_json: bool) -> str:
        if self.provider == "openai":
            body = {"model": self.model, "messages": [{"role": "system", "content": system},
                                                      {"role": "user", "content": user}]}
            if as_json:
                body["response_format"] = {"type": "json_object"}
            req = urllib.request.Request("https://api.openai.com/v1/chat/completions", json.dumps(body).encode(),
                                         {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"})
            out = json.loads(urllib.request.urlopen(req, timeout=180).read())["choices"][0]["message"]["content"]
        else:
            body = {"model": self.model, "max_tokens": 2000, "system": system,
                    "messages": [{"role": "user", "content": user}]}
            req = urllib.request.Request("https://api.anthropic.com/v1/messages", json.dumps(body).encode(),
                                         {"x-api-key": self.key, "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
            out = "".join(b.get("text", "") for b in json.loads(urllib.request.urlopen(req, timeout=180).read())["content"])
        self.calls.append({"system": system[:200], "user": user, "reply": out})
        return out

    def propose(self, ctx: dict, feedback: str | None = None) -> dict:
        user = json.dumps({"allowed_models_and_default_params": allowed_models(self.heavy),
                           "champion": ctx["champion"], "history_most_recent_last": ctx["history"]}, indent=1)
        user += "\n\nDIAGNOSIS OF THE CHAMPION (DEV):\n" + ctx["diagnosis_md"]
        if ctx.get("outside"):
            o = ctx["outside"]
            user += (f"\n\nOUTSIDE EVIDENCE (Exa, published on or before {o['cutoff']}; newest found this turn, "
                     f"then the evidence memory):\n" + json.dumps(o["memory_for_prompt"], indent=1))
        if feedback:
            user += f"\n\nYour previous proposal was refused: {feedback}\nPropose a different, valid experiment."
        txt = self._chat(SYSTEM, user, as_json=True)
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0)) if m else {}

    def lesson(self, rec: dict, ctx: dict) -> str:
        k = C.PRIMARY_METRIC
        facts = {"hypothesis": rec["hypothesis"], "accepted": rec["accepted"], "reason": rec["reason"],
                 "dev": {x: rec["dev"][x] for x in (k, "skill_geomean", "coverage_in")},
                 "champion_dev": {x: ctx["champion"]["dev"][x] for x in (k, "skill_geomean", "coverage_in")}}
        return self._chat(LESSON_SYSTEM, json.dumps(facts, indent=1), as_json=False).strip()


# ---------------------------------------------------------------- heuristic proposer (no API)
class HeuristicProposer:
    """Maps diagnosis numbers to one-change mutations of the champion, most-indicated first."""

    def __init__(self, heavy: bool = False):
        self.heavy, self.calls = heavy, []

    def candidates(self, ctx: dict):
        ch, d = ctx["champion"]["spec"], ctx["champion"]["dev"]
        above, below, cov = d["coverage_above_q90"], d["coverage_below_q10"], d["coverage_in"]
        gap = d["skill_pooled"] - d["skill_geomean"]
        cal = ch.get("calibrate", {})
        g, sc = float(cal.get("gamma", 0.5)), float(cal.get("scale", 0.01))
        first = ch["models"][0]
        out = []

        def mut(obs, hyp, change, f):
            s = copy.deepcopy(ch)
            f(s)
            out.append({"observation": obs, "hypothesis": hyp, "change": change, "spec": s})

        if not cal.get("enabled"):
            mut(f"no calibration; truth above q90 in {above:.0%} and below q10 in {below:.0%} of dev cells "
                f"(10% each if calibrated), coverage {cov:.2f}",
                "Learning an upper and lower offset per collector x class from realised misses should bring "
                "coverage to 0.80 and cut pinball loss.", "enable online calibration (source_class)",
                lambda s: s.update(calibrate={"enabled": True, "gamma": 0.5, "scale": 0.01, "group_by": "source_class"}))
        for alt in ("trend_tail", "momentum", "step_hazard", "vol_tail"):
            if alt in M.REGISTRY and alt != first["name"]:
                mut(f"champion model {first['name']} has dev skill {d['skill_pooled']:.3f}, coverage {cov:.2f}",
                    f"Replacing {first['name']} by {alt} (recent-window, step-aware) should fit posted prices better.",
                    f"primary model {first['name']} -> {alt}",
                    lambda s, alt=alt: s["models"].__setitem__(0, {"name": alt, "params": {}}))

        if cov < 0.78 or above > 0.12 or below > 0.12:
            mut(f"dev coverage {cov:.2f} (above q90 {above:.2f}, below q10 {below:.2f}; target 0.80 / 0.10 / 0.10)",
                "Calibration reacts too slowly to misses; a larger step should pull coverage to target.",
                f"calibrate.gamma {g} -> {round(g * 1.6, 3)}",
                lambda s: s.setdefault("calibrate", {}).update(gamma=round(g * 1.6, 3)))
        if cov > 0.82:
            mut(f"dev coverage {cov:.2f} above the 0.80 target", "Intervals are wider than needed; a smaller "
                "calibration step should tighten them and lower pinball loss.",
                f"calibrate.gamma {g} -> {round(g * 0.6, 3)}",
                lambda s: s.setdefault("calibrate", {}).update(gamma=round(g * 0.6, 3)))
        if gap > 0.03:
            mut(f"pooled {d['skill_pooled']:.3f} vs geomean {d['skill_geomean']:.3f}: quiet series score much worse",
                "One calibration offset per group over-widens low-volatility series; a smaller step per update "
                "should help quiet series without losing coverage.",
                f"calibrate.scale {sc} -> {round(sc * 0.5, 4)}",
                lambda s: s.setdefault("calibrate", {}).update(scale=round(sc * 0.5, 4)))
            mut("same pooled/geomean gap", "Calibrating by instrument class pools rate cards across collectors, "
                "which may suit step-like series better.", "calibrate.group_by -> instrument_class",
                lambda s: s.setdefault("calibrate", {}).update(group_by="instrument_class"))
        for w in (30, 90, 120):
            if "window" in M.REGISTRY[first["name"]].defaults and first.get("params", {}).get("window", 60) != w:
                mut(f"champion uses a {first.get('params', {}).get('window', 60)}-day window",
                    f"A {w}-day window trades reactivity for stability of the change distribution.",
                    f"{first['name']}.window -> {w}",
                    lambda s, w=w: s["models"][0].setdefault("params", {}).update(window=w))
        for fl in (0.5, 1.5):
            if "floor" in M.REGISTRY[first["name"]].defaults:
                mut(f"truth above q90 in {above:.0%} of dev cells", f"Upper floor of {fl} typical moves "
                    f"{'tightens' if fl < 1 else 'widens'} the upper edge where no recent rise exists.",
                    f"{first['name']}.floor -> {fl}",
                    lambda s, fl=fl: s["models"][0].setdefault("params", {}).update(floor=fl))
        # an ensemble with the base model that wins some group alone
        table = ctx["diagnosis"].get("per_model_skill_by_group") or []
        for alt in ("step_hazard", "trend_tail", "vol_tail"):
            if alt in M.REGISTRY and alt != first["name"]:
                mut("groups behave differently (step-like rate cards vs drifting spot/asks)",
                    f"Letting per-group weights choose between {first['name']} and {alt} from recent pinball loss "
                    "should help where one model dominates.", f"hedge ensemble {first['name']} + {alt}",
                    lambda s, alt=alt: (s["models"].append({"name": alt, "params": {"window": 60}}),
                                        s.update(combine={"method": "hedge", "eta": 0.5, "group_by": "source_class"})))
        return out

    def propose(self, ctx: dict, feedback: str | None = None) -> dict:
        for c in self.candidates(ctx):
            if spec_hash(c["spec"]) not in ctx["tried"] and not validate(c["spec"], self.heavy):
                return c
        return {}

    def lesson(self, rec: dict, ctx: dict) -> str:
        k, cd = C.PRIMARY_METRIC, ctx["champion"]["dev"]
        dd = rec["dev"][k] - cd[k]
        cov = rec["dev"]["coverage_in"]
        verdict = "kept" if rec["accepted"] else ("overfit: DEV up, gate failed" if dd > C.MIN_DEV_GAIN else "no DEV gain")
        return (f"{verdict}. DEV {k} {dd:+.4f} vs champion, geomean {rec['dev']['skill_geomean'] - cd['skill_geomean']:+.4f}, "
                f"coverage {cd['coverage_in']:.2f}->{cov:.2f}. {rec['reason']}")


# ---------------------------------------------------------------- automatic DEV sweep
MAX_SWEEP = 5


def _set(spec: dict, path: str, value) -> dict:
    out = json.loads(json.dumps(spec))
    keys = path.split(".")
    node = out
    for k in keys[:-1]:
        k = int(k) if isinstance(node, list) else k
        if isinstance(node, dict) and k not in node:
            node[k] = {}
        node = node[k]
    last = keys[-1]
    node[int(last) if isinstance(node, list) else last] = value
    return out


def dev_sweep(spec: dict, sweep: dict, heavy: bool, tried: set) -> tuple[dict, list]:
    """Score each value of one parameter on DEV only; return the best spec and the sweep table.
    HOLDOUT is never forecast here, so the gate sees exactly one candidate per idea."""
    import tempfile
    from pathlib import Path
    rows = []
    for v in list(sweep.get("values", []))[:MAX_SWEEP]:
        cand = _set(spec, sweep["param"], v)
        errs = validate(cand, heavy)
        if not errs and spec_hash(cand) in tried:
            errs = ["already tried"]
        if errs:
            rows.append({"value": v, "refused": errs})
            continue
        with tempfile.TemporaryDirectory() as d:
            m = run_experiment.dev_score(cand, Path(d))
        rows.append({"value": v, "dev": round(m[C.PRIMARY_METRIC], 5), "coverage": round(m["coverage_in"], 3)})
    scored = [r for r in rows if "dev" in r]
    if not scored:
        return spec, rows
    best = max(scored, key=lambda r: r["dev"])
    return _set(spec, sweep["param"], best["value"]), rows


# ---------------------------------------------------------------- the loop
def loop(proposer, iters: int, max_rejects: int, seed: str | None, heavy: bool):
    C.EXPERIMENTS.mkdir(parents=True, exist_ok=True)
    log = C.EXPERIMENTS / "autoresearch_log.jsonl"
    if not (C.EXPERIMENTS / "champion.json").exists():
        spec = json.loads(open(seed or SEED_SPEC).read())
        rec = run_experiment.run(spec, spec.get("_hypothesis", "seed champion"), verbose=False)
        ledger.lesson(rec["id"], "seed: starting champion for this autonomous run")
        print(f"[seed] {rec['id']} dev {rec['dev'][C.PRIMARY_METRIC]:+.4f}")
    rejects = 0
    for i in range(iters):
        ctx = context()
        if USE_EXA:
            import exa_scout
            ctx["outside"] = exa_scout.scout(ctx, i + 1)
            o = ctx["outside"]
            print(f"[iter {i + 1}] Exa: {len(o['found_this_turn'])} results, {o['new_in_memory']} new in memory"
                  + (f", errors {o['errors']}" if o["errors"] else ""))
        prop, feedback, refused = {}, None, []
        for _ in range(3):
            prop = proposer.propose(ctx, feedback) or {}
            spec = prop.get("spec") or {}
            errs = validate(spec, heavy) if spec else ["no spec returned"]
            if not errs and spec_hash(spec) in ctx["tried"]:
                errs = ["this spec runs exactly like one already tried (settings without effect count as unchanged)"]
            if not errs:
                break
            feedback = "; ".join(errs)
            refused.append({"proposal": prop, "errors": errs})
        else:
            # no valid proposal this iteration: record it, count it as a rejection, keep going
            with open(log, "a") as f:
                f.write(json.dumps({"id": None, "iteration": i + 1, "refused": refused,
                                    "llm_calls": getattr(proposer, "calls", [])}, default=str) + "\n")
            proposer.calls = []
            rejects += 1
            print(f"[iter {i + 1}] no valid new proposal after 3 tries ({feedback}); counted as a rejection")
            if rejects >= max_rejects:
                print(f"stopping: {rejects} rejections in a row")
                break
            continue
        hyp = f"{prop.get('observation', '')} -> {prop.get('hypothesis', '')} Change: {prop.get('change', '')}".strip()
        sweep_rows = None
        if isinstance(prop.get("sweep"), dict) and prop["sweep"].get("param") and prop["sweep"].get("values"):
            spec, sweep_rows = dev_sweep(clean(spec), prop["sweep"], heavy, ctx["tried"])
            ok = [r for r in sweep_rows if "dev" in r]
            if ok:
                hyp += (f" DEV sweep of {prop['sweep']['param']}: " +
                        ", ".join(f"{r['value']}->{r['dev']:+.4f}" for r in ok) +
                        f"; chose {max(ok, key=lambda r: r['dev'])['value']}.")
            if spec_hash(spec) in ctx["tried"]:
                print(f"[iter {i + 1}] sweep winner was already tried; counted as a rejection")
                rejects += 1
                if rejects >= max_rejects:
                    break
                continue
        spec = {"_hypothesis": hyp, **clean(spec)}
        rec = run_experiment.run(spec, hyp, parent=ctx["champion"]["id"], verbose=False)
        lesson = proposer.lesson(rec, ctx)
        ledger.lesson(rec["id"], lesson)
        with open(log, "a") as f:
            exa_log = ({k: ctx["outside"][k] for k in ("cutoff", "queries", "found_this_turn", "errors")}
                       if ctx.get("outside") else None)
            f.write(json.dumps({"id": rec["id"], "proposal": prop, "refused_before": refused, "sweep": sweep_rows,
                                "exa": exa_log, "source_url": prop.get("source_url"),
                                "accepted": rec["accepted"],
                                "lesson": lesson, "llm_calls": getattr(proposer, "calls", [])}, default=str) + "\n")
        proposer.calls = []
        k = C.PRIMARY_METRIC
        print(f"[iter {i + 1}] {rec['id']} {'ACCEPTED' if rec['accepted'] else 'rejected'}  "
              f"dev {rec['dev'][k]:+.4f}  holdout {rec['holdout'][k]:+.4f}  cov {rec['dev']['coverage_in']:.2f}  | {prop.get('change', '')}")
        rejects = 0 if rec["accepted"] else rejects + 1
        if rejects >= max_rejects:
            print(f"stopping: {rejects} rejections in a row")
            break
    ledger.plot()
    try:
        import report
        print(report.build())
    except Exception as e:  # the report must never break a research run
        print(f"report.py failed: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=6)
    ap.add_argument("--max-rejects", type=int, default=4)
    ap.add_argument("--proposer", choices=["llm", "heuristic"], default="heuristic")
    ap.add_argument("--provider", choices=["openai", "anthropic"], default="openai")
    ap.add_argument("--model", default=None)
    ap.add_argument("--seed", default=None, help=f"spec used if the ledger has no champion (default {SEED_SPEC.name})")
    ap.add_argument("--allow-heavy", action="store_true", help="let the proposer use chronos/chronos2/timestral")
    ap.add_argument("--exa", action="store_true",
                    help="each iteration, search the web with Exa (EXA_API_KEY) for methods and dated market news")
    ap.add_argument("--no-memory", action="store_true",
                    help="ablation: hide past hypotheses and lessons from the proposer")
    ap.add_argument("--ideas", choices=["single", "batch"], default="single",
                    help="llm proposer: one idea per turn, or 5 scored ideas + one reflection, run the top one")
    a = ap.parse_args()
    global NO_MEMORY, USE_EXA
    NO_MEMORY = a.no_memory
    USE_EXA = a.exa
    if a.proposer == "llm" and a.ideas == "batch":
        from idea_batch import BatchProposer
        prop = BatchProposer(a.provider, a.model, a.allow_heavy)
    else:
        prop = (LLMProposer(a.provider, a.model, a.allow_heavy) if a.proposer == "llm"
                else HeuristicProposer(a.allow_heavy))
    loop(prop, a.iters, a.max_rejects, a.seed, a.allow_heavy)


if __name__ == "__main__":
    main()
