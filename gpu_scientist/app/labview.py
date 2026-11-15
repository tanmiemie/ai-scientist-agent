"""Lab: design and run experiments, launch the autonomous scientist, watch jobs live."""
from __future__ import annotations

import json
import os

import pandas as pd
import streamlit as st

import autoresearch as AR
import config as C
import lab
import store
import ui

MODEL_HELP = {
    "last_value": "flat last value (the scoring baseline)",
    "drift": "starter kit: empirical random walk of past changes",
    "trend_tail": "recent-window changes, step-aware tails",
    "momentum": "trend_tail + shift up after a recent rise",
    "step_hazard": "simulated jumps from a step-change hazard",
    "vol_tail": "tails scaled by recent volatility",
    "leader": "follows lagged moves of other collectors",
    "chronos": "Amazon Chronos-Bolt (pretrained, heavy)",
    "chronos2": "Chronos-2 (pretrained, heavy)",
    "timestral": "Mistral Timestral (pretrained, heavy)",
}


def _status_bar():
    ready = store.pack_ready()
    h = st.container(horizontal=True)
    with h:
        st.badge("data pack found" if ready else "data pack missing", color="green" if ready else "red",
                 icon=":material/database:", help=str(C.PACK))
        for env, name in (("OPENAI_API_KEY", "OpenAI"), ("ANTHROPIC_API_KEY", "Anthropic")):
            ok = bool(os.environ.get(env))
            st.badge(f"{name} key {'set' if ok else 'not set'}", color="green" if ok else "gray", icon=":material/key:")
    if not ready:
        st.warning(f"Runs need the data pack at `{C.PACK}` (or set `GPU_PACK`). You can still browse and design specs.")
    return ready


def _workspace() -> "store.Path | None":
    wss = lab.workspaces()
    names = [w.name for w in wss]
    with st.container(border=True):
        st.markdown("**Workspace** · lab runs never touch the tracked ledgers; each workspace is its own ledger in "
                    "`experiments_app/`.")
        c1, c2 = st.columns([2, 3])
        with c1:
            cur = st.session_state.get("lab_ws")
            ws = st.selectbox("Workspace", names, index=names.index(cur) if cur in names else (len(names) - 1 if names else 0),
                              key="lab_ws_pick", placeholder="create one →") if names else None
        with c2.popover("New workspace", icon=":material/add:"):
            name = st.text_input("Name", key="lab_new_name", placeholder="e.g. llm-run-2")
            forkable = [k for k in store.ledgers() if not k.startswith("walk-forward")]
            src = st.selectbox("Start from", ["fresh (seed spec runs first)"] + forkable, key="lab_new_src",
                               help="Forking copies the ledger, champion and diagnoses, so the scientist continues from there. "
                                    "Walk-forward ledgers are scored on other DEV/GATE windows, so they cannot be forked.")
            if st.button("Create", type="primary", disabled=not name, key="lab_new_btn"):
                try:
                    w = lab.new_workspace(name) if src.startswith("fresh") else lab.fork(store.ledgers()[src], name)
                    st.session_state["lab_ws"] = w.name
                    st.session_state.pop("lab_ws_pick", None)
                    st.rerun()
                except FileExistsError as e:
                    st.error(str(e))
    if not ws:
        st.info("Create a workspace to start.")
        return None
    st.session_state["lab_ws"] = ws
    w = store.LAB / ws
    df = store.load_ledger(w)
    champ = store.champion(w)
    m = st.columns(4)
    m[0].metric("Experiments", len(df))
    m[1].metric("Champion", champ["id"] if champ else "none yet")
    m[2].metric("Champion DEV", ui.fmt(champ["dev"][store.K]) if champ else "–")
    m[3].metric("Champion HOLDOUT", ui.fmt(champ["holdout"][store.K]) if champ else "–")
    if len(df) > 1:
        with st.expander("Progress in this workspace"):
            st.altair_chart(ui.progress_chart(df, 240), width="stretch")
    return w


def _param_input(model: str, key: str, default, current, prefix: str):
    k = f"{prefix}_{key}"
    if default is None or isinstance(default, str):
        v = st.text_input(key, value="" if current is None else str(current), key=k,
                          help="leave empty for the default" if default is None else None)
        return (None if v == "" else (int(v) if v.isdigit() else v)) if default is None else v
    if isinstance(default, bool):
        return st.checkbox(key, value=bool(current), key=k)
    if isinstance(default, int):
        return int(st.number_input(key, value=int(current), step=1, key=k))
    return float(st.number_input(key, value=float(current), step=0.05, format="%.3f", key=k))


def _designer(w, ready: bool):
    champ = store.champion(w)
    seed_path = AR.SEED_SPEC
    base = AR.clean(champ["spec"]) if champ else AR.clean(json.loads(seed_path.read_text()))
    st.caption(f"Starts from the {'champion ' + champ['id'] if champ else 'seed ' + seed_path.name}. Change one thing, "
               "write the hypothesis, run. The same validator and accept rule as the autonomous loop apply.")
    heavy = st.toggle("Allow heavy pretrained models (chronos, chronos2, timestral)", key=f"ds_heavy_{w.name}",
                      help="Need extra installs and weight downloads; a run takes ~20 minutes on CPU.")
    allowed = AR.allowed_models(heavy)
    pfx = f"ds_{w.name}_{champ['id'] if champ else 'seed'}"
    base_models = base.get("models", [])
    n = st.number_input("Number of base models", 1, 4, value=max(1, len(base_models)), key=f"{pfx}_n")
    models = []
    cols = st.columns(int(n))
    for i, col in enumerate(cols):
        with col.container(border=True):
            names = list(allowed)
            bm = base_models[i] if i < len(base_models) else {"name": "trend_tail", "params": {}}
            name = st.selectbox(f"Model {i + 1}", names, index=names.index(bm["name"]) if bm["name"] in names else 0,
                                key=f"{pfx}_m{i}", format_func=lambda x: x, help=MODEL_HELP.get(bm["name"]))
            st.caption(MODEL_HELP.get(name, ""))
            params = {}
            bparams = bm.get("params") or {} if bm["name"] == name else {}
            for k, dv in allowed[name].items():
                if k in ("model_id", "seed", "n_sims"):
                    continue
                params[k] = _param_input(name, k, dv, bparams.get(k, dv), f"{pfx}_m{i}_{name}")
            models.append({"name": name, "params": {k: v for k, v in params.items() if v != allowed[name].get(k)}})
    c1, c2 = st.columns(2)
    with c1.container(border=True):
        bc = {**AR.COMBINE_DEFAULTS, **base.get("combine", {})}
        meths = ["single", "mean", "hedge"]
        method = st.segmented_control("Combine", meths, default=bc["method"] if n > 1 or bc["method"] == "single" else "hedge",
                                      key=f"{pfx}_comb", help="hedge = per-group weights learned online from recent pinball loss") or "single"
        comb = {"method": method}
        if method == "hedge":
            comb["eta"] = st.slider("eta (learning rate)", 0.1, 10.0, float(bc["eta"]), 0.1, key=f"{pfx}_eta")
            comb["group_by"] = st.selectbox("Weights per", AR.GROUPS, index=AR.GROUPS.index(bc["group_by"]), key=f"{pfx}_cgb")
    with c2.container(border=True):
        bcal = {**AR.CAL_DEFAULTS, **base.get("calibrate", {})}
        en = st.toggle("Online interval calibration", value=bool(bcal["enabled"]), key=f"{pfx}_cal",
                       help="learns upper/lower offsets per group from realised misses, toward 10% on each side")
        cal = {"enabled": en}
        if en:
            cal["gamma"] = st.slider("gamma (step size)", 0.05, 3.0, float(bcal["gamma"]), 0.05, key=f"{pfx}_g")
            cal["scale"] = st.slider("scale (log units per step)", 0.001, 0.05, float(min(bcal["scale"], 0.05)), 0.001,
                                     format="%.3f", key=f"{pfx}_s")
            cal["group_by"] = st.selectbox("Offsets per", AR.GROUPS, index=AR.GROUPS.index(bcal["group_by"]), key=f"{pfx}_gb")
    spec = {"models": models, "combine": comb, "calibrate": cal}
    hyp = st.text_area("Hypothesis", key=f"{pfx}_hyp", placeholder="Observation (a number from the diagnosis) → hypothesis → "
                       "change → expected effect", help="Required. Stored in the ledger with the result.")

    errs = AR.validate(spec, heavy)
    tried = {AR.spec_hash(r.spec) for r in store.load_ledger(w).itertuples()} if (w / "ledger.jsonl").exists() else set()
    if not errs and AR.spec_hash(spec) in tried:
        errs.append("this spec runs exactly like one already tried in this workspace")
    left, right = st.columns([3, 2])
    with left:
        st.markdown("**Change vs the starting spec**")
        diff = ui.spec_diff(base, spec)
        st.dataframe(diff, hide_index=True, width="stretch") if len(diff) else st.caption("No effective change yet.")
        st.caption(ui.spec_summary(spec))
    with right:
        if errs:
            for e in errs:
                st.error(e, icon=":material/block:")
        else:
            st.success("Valid and new.", icon=":material/check:")
        can = ready and not errs and bool(hyp.strip()) and not lab.busy(w)
        if st.button("Run experiment", type="primary", disabled=not can, icon=":material/play_arrow:", key=f"{pfx}_run",
                     help=None if can else "needs the data pack, a valid new spec, a hypothesis and no running job here"):
            sp = w / "_specs"
            sp.mkdir(exist_ok=True)
            path = sp / f"{pd.Timestamp.now():%Y%m%d_%H%M%S}.json"
            path.write_text(json.dumps({"_hypothesis": hyp, **spec}, indent=1))
            args = ["run_experiment.py", "--spec", str(path), "--hypothesis", hyp] + (["--parent", champ["id"]] if champ else [])
            lab.start("experiment", args, w, f"manual experiment in {w.name}")
            st.toast("Experiment started", icon=":material/science:")
        with st.expander("Spec JSON"):
            st.json(spec)


def _autoloop(w, ready: bool):
    st.caption("Runs autoresearch.py in this workspace: diagnose → propose → validate → test → decide → learn, "
               "with no human in the loop.")
    c1, c2, c3 = st.columns(3)
    prop = c1.segmented_control("Proposer", ["heuristic", "llm"], default="heuristic", key="al_prop",
                                format_func={"heuristic": "rule-based (no API)", "llm": "LLM"}.get) or "heuristic"
    provider = model = None
    if prop == "llm":
        provider = c2.segmented_control("Provider", ["openai", "anthropic"], default="openai", key="al_provider") or "openai"
        model = c3.text_input("Model", value="gpt-4.1" if provider == "openai" else "", key=f"al_model_{provider}",
                              placeholder="default")
    c4, c5, c6 = st.columns(3)
    iters = c4.slider("Iterations", 1, 12, 3, key="al_iters")
    max_rej = c5.slider("Stop after N rejections in a row", 1, 12, 4, key="al_rej")
    specs = sorted(p.name for p in (C.ROOT / "specs").glob("*.json"))
    has_champ = (w / "champion.json").exists()
    seed = c6.selectbox("Seed spec", specs, index=specs.index(AR.SEED_SPEC.name) if AR.SEED_SPEC.name in specs else 0,
                        key="al_seed", disabled=has_champ, help="Only used when the workspace has no champion yet.")
    heavy = st.checkbox("Let the proposer use heavy pretrained models", key="al_heavy")
    key_env = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}.get(provider or "")
    missing_key = prop == "llm" and not os.environ.get(key_env)
    if missing_key:
        st.warning(f"{key_env} is not set in the app's environment; restart the app with it to use the LLM proposer.")
    running = lab.busy(w)
    if running:
        st.caption("A job is already running in this workspace; wait for it or stop it below.")
    if st.button("Start autonomous run", type="primary", icon=":material/rocket_launch:", key="al_go",
                 disabled=not ready or missing_key or running):
        args = ["autoresearch.py", "--iters", str(iters), "--max-rejects", str(max_rej), "--proposer", prop,
                "--seed", str(C.ROOT / "specs" / seed)]
        if prop == "llm":
            args += ["--provider", provider] + (["--model", model] if model else [])
        if heavy:
            args.append("--allow-heavy")
        lab.start("autoresearch", args, w, f"{iters} iterations, {prop}{' ' + (model or provider) if prop == 'llm' else ''} in {w.name}")
        st.toast("Autonomous run started", icon=":material/rocket_launch:")


def _walkforward(ready: bool):
    st.caption("Runs walkforward.py: the autonomous loop on three slices, each champion scored on the following unseen "
               "week. Results appear on the Walk-forward page.")
    c1, c2, c3 = st.columns(3)
    prop = c1.segmented_control("Proposer", ["heuristic", "llm"], default="heuristic", key="wf_prop") or "heuristic"
    iters = c2.slider("Iterations per slice", 1, 10, 3, key="wf_iters")
    name = c3.text_input("Run name", value=f"{prop}_{pd.Timestamp.now():%m%d_%H%M}", key=f"wf_name_{prop}",
                         help="Saved as walkforward/app_<name>/ (git-ignored).")
    run = "app_" + lab.slug(name).replace("-", "_").removeprefix("app_")
    missing_key = prop == "llm" and not os.environ.get("OPENAI_API_KEY")
    if missing_key:
        st.warning("OPENAI_API_KEY is not set in the app's environment.")
    exists = (C.ROOT / "walkforward" / run).exists()
    if exists:
        st.error("A run with this name already exists.")
    if st.button("Start walk-forward", type="primary", icon=":material/timeline:", key="wf_go",
                 disabled=not ready or missing_key or exists or not name):
        lab.start("walkforward", ["walkforward.py", "--proposer", prop, "--iters", str(iters), "--run", run],
                  None, f"walk-forward {run}")
        st.toast("Walk-forward started", icon=":material/timeline:")


@st.fragment(run_every=2)
def _jobs_panel():
    js = lab.jobs()
    st.subheader("Jobs")
    if not js:
        st.caption("Nothing has run yet.")
        return
    ids = [j["id"] for j in js]
    labels = {j["id"]: f"{'● running' if j['running'] else '○ done'} · {j['title']} · {j['started'][11:16]}" for j in js}
    sel = st.selectbox("Job", ids, format_func=labels.get, key="job_sel")
    j = next(x for x in js if x["id"] == sel)
    h = st.container(horizontal=True, vertical_alignment="center")
    with h:
        st.badge("running" if j["running"] else "finished", color="blue" if j["running"] else "gray")
        st.caption(" ".join(a if " " not in a else "\"…\"" for a in j["args"]))
        if j["running"] and st.button("Stop", icon=":material/stop:", key=f"stop_{sel}"):
            lab.stop(sel)
    st.code(lab.log_text(sel) or "(waiting for output)", language="text", height=360)
    if any(x["running"] for x in js):
        st.caption("Refreshes every 2 s. Results land in the workspace ledger; switch the sidebar ledger to "
                   "`lab / <workspace>` to browse them on every page.")


def lab_page():
    st.title("Lab")
    ready = _status_bar()
    w = _workspace()
    t1, t2, t3 = st.tabs(["Autonomous loop", "Design an experiment", "Walk-forward check"])
    with t1:
        if w is not None:
            _autoloop(w, ready)
    with t2:
        if w is not None:
            _designer(w, ready)
    with t3:
        _walkforward(ready)
    _jobs_panel()
