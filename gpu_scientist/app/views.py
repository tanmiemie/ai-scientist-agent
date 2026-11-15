"""Read-only pages: everything the scientist has already done."""
from __future__ import annotations

import json

import altair as alt
import pandas as pd
import streamlit as st

import config as C
import store
import ui
from store import K


def _ledger() -> tuple[str, "store.Path", pd.DataFrame]:
    label = st.session_state["ledger"]
    d = store.ledgers()[label]
    return label, d, store.load_ledger(d)


def _exp_picker(df: pd.DataFrame, exp_dir, key: str, label: str = "Experiment", default: str | None = None) -> str:
    champ = (store.champion(exp_dir) or {}).get("id")
    ids = list(df.id)
    names = {r.id: f"{r.id} · {'champion' if r.id == champ else 'accepted' if r.accepted else 'rejected'} · dev {ui.fmt(r.dev)}"
             for r in df.itertuples()}
    default = default or champ or ids[-1]
    return st.selectbox(label, ids, index=ids.index(default) if default in ids else len(ids) - 1,
                        format_func=names.get, key=f"{key}:{exp_dir}")


# ---------------------------------------------------------------- overview
def overview():
    label, d, df = _ledger()
    st.title("GPU Value AI Scientist")
    st.caption("A self-improving forecaster of posted GPU rental prices (q10 / q50 / q90, 1, 3 and 7 days ahead). "
               "It diagnoses its own errors, proposes one hypothesis at a time, tests it leak-free and keeps only "
               "what beats the champion on DEV without losing on the unseen HOLDOUT.")
    if df.empty:
        st.info("This ledger is empty.")
        return
    champ = store.champion(d) or {}
    seed = df.iloc[0]
    c = df[df.id == champ.get("id")].iloc[0] if champ.get("id") in set(df.id) else df[df.accepted].iloc[-1]
    cols = st.columns(5)
    cols[0].metric("Champion", c.id, help=ui.spec_summary(c.spec))
    cols[1].metric("DEV skill", ui.fmt(c.dev), ui.fmt(c.dev - seed.dev) + " vs seed",
                   help=f"{K}: 1 − pinball loss / last-value pinball loss on DEV origins {C.DEV_ORIGINS[0]}…{C.DEV_ORIGINS[1]}")
    cols[2].metric("HOLDOUT skill", ui.fmt(c.holdout), ui.fmt(c.holdout - seed.holdout) + " vs seed",
                   help=f"Gate only, never tuned on: origins {C.HOLDOUT_ORIGINS[0]}…{C.HOLDOUT_ORIGINS[1]}")
    cols[3].metric("DEV coverage", ui.fmt(c.dev_coverage, False, 2), ui.fmt(c.dev_coverage - seed.dev_coverage, True, 2),
                   help="Share of truths inside [q10, q90]; target 0.80")
    cols[4].metric("Experiments", f"{int(df.accepted.sum())} / {len(df)}", help="accepted / run")

    with st.container(border=True):
        st.markdown(f"**Self-improvement across iterations** · `{label}`")
        st.altair_chart(ui.progress_chart(df), width="stretch")
        st.caption("Blue = DEV (seen while iterating), orange = HOLDOUT (gate, never tuned on), green = champion on "
                   "HOLDOUT. Crosses are rejected experiments.")

    st.subheader("How one iteration works")
    steps = [
        (":material/monitoring:", "Diagnose", "Error health check of the champion on DEV: bias, interval misses by group, horizon and state, worst series."),
        (":material/lightbulb:", "Propose", "The proposer (gpt-4.1 or a rule-based scientist) writes one hypothesis grounded in a number from the diagnosis."),
        (":material/rule:", "Validate", "Only registered models and parameter ranges; a spec that runs like one already tried is refused."),
        (":material/science:", "Test", "Walk-forward over daily origins, scored by the organisers' own scorer.py."),
        (":material/gavel:", "Decide", f"Accept only if DEV gains ≥ {C.MIN_DEV_GAIN} and HOLDOUT does not drop."),
        (":material/menu_book:", "Learn", "A lesson goes into the ledger and is read before the next proposal."),
    ]
    for col, (icon, title, text) in zip(st.columns(len(steps)), steps):
        with col.container(border=True, height="stretch"):
            st.markdown(f"{icon} **{title}**")
            st.caption(text)

    left, right = st.columns([3, 2])
    with left:
        st.subheader("Latest lessons")
        for r in df.iloc[::-1].head(4).itertuples():
            with st.container(border=True):
                h = st.container(horizontal=True, vertical_alignment="center")
                h.markdown(f"**{r.id}**")
                with h:
                    ui.decision_badge(r.accepted, r.i == 0)
                st.caption(ui.short(r.hypothesis, 220))
                if r.lesson:
                    st.markdown(f"> {ui.short(r.lesson, 300)}")
    with right:
        st.subheader("Is the improvement real?")
        runs = store.walkforward_runs()
        if not runs:
            st.caption("No walk-forward runs yet.")
        for name, rd in runs.items():
            w = store.load_walkforward(rd)
            g = w.groupby("slice").test.agg(["first", "last"])
            gain = (g["last"] - g["first"])
            with st.container(border=True):
                st.markdown(f"**{name}**")
                st.metric("Mean TEST gain, seed → final champion", ui.fmt(gain.mean()),
                          f"{int((gain > 0).sum())} of {len(gain)} slices improved", delta_color="off")
        st.caption("Each slice pretends to be an earlier date; the champions it produces are scored on the following "
                   "week, which no decision saw. See the Walk-forward page.")


# ---------------------------------------------------------------- research ledger
def timeline():
    label, d, df = _ledger()
    st.title("Research ledger")
    st.caption(f"Every hypothesis the scientist tested in `{label}`, why, what happened and what it learned.")
    if df.empty:
        st.info("This ledger is empty.")
        return
    bar = st.container(horizontal=True, vertical_alignment="bottom")
    show = bar.segmented_control("Show", ["all", "accepted", "rejected"], default="all", key="tl_show")
    q = bar.text_input("Search hypotheses and lessons", key="tl_q", placeholder="e.g. calibration, momentum, leader")
    newest = bar.toggle("Newest first", value=True, key="tl_order")
    rows = df
    if show == "accepted":
        rows = rows[rows.accepted]
    elif show == "rejected":
        rows = rows[~rows.accepted]
    if q:
        m = rows.hypothesis.str.contains(q, case=False, regex=False) | rows.lesson.str.contains(q, case=False, regex=False)
        rows = rows[m]
    by_id = df.set_index("id")
    for r in (rows.iloc[::-1] if newest else rows).itertuples():
        before = by_id.loc[r.champion_before] if r.champion_before in by_id.index else None
        with st.container(border=True):
            head = st.container(horizontal=True, vertical_alignment="center")
            head.markdown(f"### {r.id}")
            with head:
                ui.decision_badge(r.accepted, r.i == 0)
                if before is not None:
                    st.caption(f"vs champion {r.champion_before}")
                if r.time_utc:
                    st.caption(f"{r.time_utc[:16].replace('T', ' ')} UTC · {r.runtime_s}s")
            left, right = st.columns([3, 2])
            with left:
                st.markdown(f"**Hypothesis.** {r.hypothesis}")
                st.caption(ui.spec_summary(r.spec))
                if r.lesson:
                    st.markdown(f"**Lesson.** {r.lesson}")
            with right:
                m = st.columns(3)
                m[0].metric("DEV", ui.fmt(r.dev), None if before is None else ui.fmt(r.dev - before.dev, nd=4))
                m[1].metric("HOLDOUT", ui.fmt(r.holdout), None if before is None else ui.fmt(r.holdout - before.holdout, nd=4))
                m[2].metric("Coverage", ui.fmt(r.dev_coverage, False, 2),
                            None if before is None else ui.fmt(r.dev_coverage - before.dev_coverage, nd=2), delta_color="off")
                st.caption(f"**Decision:** {r.reason}")
            with st.expander("What changed vs the champion" if before is not None else "Spec"):
                if before is not None:
                    diff = ui.spec_diff(before.spec, r.spec)
                    st.dataframe(diff, hide_index=True, width="stretch") if len(diff) else st.caption("No effective change.")
                st.json(store_clean(r.spec), expanded=False)


def store_clean(spec: dict) -> dict:
    return {k: v for k, v in spec.items() if not k.startswith("_")}


# ---------------------------------------------------------------- diagnosis
def _bars(df: pd.DataFrame, cat: str, title: str):
    d = df.copy()
    d[cat] = d[cat].astype(str)
    skill = alt.Chart(d).mark_bar(color=ui.BLUE).encode(
        y=alt.Y(f"{cat}:N", title=None, sort=None), x=alt.X("skill:Q", title="skill"),
        tooltip=[cat, "n", alt.Tooltip("skill:Q", format="+.3f")]).properties(height=max(120, 28 * len(d)), title=title)
    miss = d.melt(id_vars=[cat, "n"], value_vars=["above_q90", "below_q10"], var_name="miss", value_name="share")
    m = alt.Chart(miss).mark_bar().encode(
        y=alt.Y(f"{cat}:N", title=None, sort=None, axis=None), yOffset="miss:N", x=alt.X("share:Q", title="share of truths outside", axis=alt.Axis(format="%")),
        color=alt.Color("miss:N", scale=alt.Scale(domain=["above_q90", "below_q10"], range=[ui.ORANGE, ui.GREY]), legend=alt.Legend(orient="bottom", title=None)),
        tooltip=[cat, "miss", alt.Tooltip("share:Q", format=".1%")]).properties(height=max(120, 28 * len(d)), title="Interval misses (target 10% each)")
    rule = alt.Chart(pd.DataFrame({"x": [0.10]})).mark_rule(strokeDash=[4, 3], color=ui.RED).encode(x="x:Q")
    st.altair_chart(alt.hconcat(skill, m + rule).resolve_scale(y="shared"), width="stretch")


def diagnosis():
    label, d, df = _ledger()
    st.title("Diagnosis")
    st.caption("The automatic error health check the proposer reads before every hypothesis (DEV origins only).")
    if df.empty:
        return
    eid = _exp_picker(df, d, "dg_exp")
    r = df[df.id == eid].iloc[0]
    diag = store.exp_json(d, eid, "diagnosis.json")
    rep_h = store.exp_json(d, eid, "report_holdout.json")
    cols = st.columns(6)
    cols[0].metric("DEV pooled", ui.fmt(r.dev))
    cols[1].metric("HOLDOUT pooled", ui.fmt(r.holdout))
    cols[2].metric("DEV geomean", ui.fmt(r.dev_geomean))
    cols[3].metric("Coverage", ui.fmt(r.dev_coverage, False, 2), help="target 0.80")
    cols[4].metric("Above q90", f"{r.above_q90:.0%}", help="target 10%")
    cols[5].metric("Below q10", f"{r.below_q10:.0%}", help="target 10%")
    st.caption(ui.spec_summary(r.spec))
    if not diag:
        st.info("No diagnosis.json for this experiment.")
        return
    t1, t2, t3, t4 = st.tabs(["Where it errs", "Series", "Models and signals", "Learned online state"])
    with t1:
        hz = pd.DataFrame({"horizon": [f"{h}d" for h in r.dev_by_h], "DEV": list(r.dev_by_h.values())})
        if rep_h:
            hz["HOLDOUT"] = [rep_h["by_horizon"].get(str(h), {}).get("skill_pooled") for h in r.dev_by_h]
        st.markdown("**Skill by horizon**")
        hl = hz.melt("horizon", var_name="window", value_name="skill")
        st.altair_chart(alt.Chart(hl).mark_bar().encode(
            x=alt.X("horizon:N", title=None, axis=alt.Axis(labelAngle=0)), xOffset="window:N", y=alt.Y("skill:Q", title=K),
            color=alt.Color("window:N", scale=alt.Scale(domain=["DEV", "HOLDOUT"], range=[ui.BLUE, ui.ORANGE]), legend=alt.Legend(orient="top", title=None)),
            tooltip=["horizon", "window", alt.Tooltip("skill:Q", format="+.3f")]).properties(height=220), width="stretch")
        for key, cat, title in [("by_group", "group", "By collector × instrument class"),
                                ("by_days_since_change", "dsc_bucket", "By days since the last price change"),
                                ("by_provider_change_7d", "prov_bucket", "By change in provider count (7 days)")]:
            if diag.get(key):
                st.markdown(f"**{title}**")
                _bars(pd.DataFrame(diag[key]), cat, "Skill")
    with t2:
        for key, title in [("worst_series", "Worst series"), ("best_series", "Best series")]:
            if diag.get(key):
                st.markdown(f"**{title}**")
                st.dataframe(pd.DataFrame(diag[key]), hide_index=True, width="stretch")
        ps = store.per_series(d, eid, "dev")
        if ps is not None:
            st.markdown("**Every scored series (DEV, from scorer.py)**")
            st.dataframe(ps.sort_values("skill_pooled"), hide_index=True, width="stretch")
    with t3:
        if diag.get("per_model_skill_by_group"):
            st.markdown("**Each base model alone: skill by group**")
            st.dataframe(pd.DataFrame(diag["per_model_skill_by_group"]), hide_index=True, width="stretch")
        if diag.get("mean_weight_by_group"):
            st.markdown("**Mean ensemble weight by group**")
            st.dataframe(pd.DataFrame(diag["mean_weight_by_group"]), hide_index=True, width="stretch")
        if diag.get("candidate_leading_signals"):
            st.markdown("**Candidate leading signals** (other series, lagged, correlated with the target's changes)")
            st.dataframe(pd.DataFrame(diag["candidate_leading_signals"]), hide_index=True, width="stretch")
    with t4:
        state = store.exp_json(d, eid, "state.json") or {}
        rows = []
        for side in ("calibration_up", "calibration_dn"):
            for k, v in (state.get(side) or {}).items():
                g, h = k.rsplit("|", 1)
                rows.append({"side": "upper edge" if side.endswith("up") else "lower edge", "group": g, "horizon": h, "offset": v})
        if rows:
            st.markdown("**Interval offsets learned from realised misses** (log-price units, end of the walk-forward)")
            st.altair_chart(alt.Chart(pd.DataFrame(rows)).mark_rect().encode(
                x=alt.X("horizon:N", title=None), y=alt.Y("group:N", title=None),
                color=alt.Color("offset:Q", scale=alt.Scale(scheme="blueorange", domainMid=0)),
                column=alt.Column("side:N", title=None), tooltip=["side", "group", "horizon", alt.Tooltip("offset:Q", format="+.3f")]
            ).properties(width=160), width="content")
        else:
            st.caption("No online calibration in this experiment.")
        w = state.get("weights") or {}
        if w:
            st.markdown("**Ensemble weights learned from recent pinball loss**")
            st.json(w, expanded=False)
    with st.expander("diagnosis.md (exactly what the proposer reads)"):
        st.markdown(store.exp_text(d, eid, "diagnosis.md") or "")


# ---------------------------------------------------------------- forecasts
def forecasts():
    label, d, df = _ledger()
    st.title("Forecast explorer")
    st.caption("Truth against the forecast band, per series and horizon, on DEV and HOLDOUT origins.")
    if df.empty:
        return
    a_col, b_col = st.columns(2)
    with a_col:
        ea = _exp_picker(df, d, "fc_a", "Experiment")
    with b_col:
        compare = st.toggle("Compare with another experiment", key="fc_cmp")
        eb = _exp_picker(df, d, "fc_b", "Compare with", default=df.id.iloc[0]) if compare else None
    ca = store.cells(d, ea)
    if ca is None:
        st.warning("Per-cell forecasts for this experiment are not on this machine (CSVs are not kept in git). "
                   "Pick a ledger such as `experiments_final`, or regenerate them with `bash run_all.sh`.")
        return
    cb = store.cells(d, eb) if eb else None
    sids = sorted(ca.series_id.unique())
    ps = store.per_series(d, ea, "dev")
    worst = ps.sort_values("skill_pooled").series_id.iloc[0] if ps is not None and len(ps) else sids[0]
    s1, s2 = st.columns([3, 1])
    sid = s1.selectbox("Series", sids, index=sids.index(st.session_state.get("fc_sid", sids[min(3, len(sids) - 1)]))
                       if st.session_state.get("fc_sid") in sids else 0, key="fc_sid",
                       help=f"Worst DEV series for {ea}: {worst}")
    h = s2.segmented_control("Horizon", [1, 3, 7], default=1, format_func=lambda x: f"{x} day{'s' if x > 1 else ''}", key="fc_h") or 1
    sa = ca[(ca.series_id == sid) & (ca.horizon_days == h)].sort_values("target_date")

    truth = alt.Chart(sa).mark_line(color="#191919", strokeWidth=1.8, point=alt.OverlayMarkDef(size=18, color="#191919")).encode(
        x=alt.X("target_date:T", title="target date"), y=alt.Y("y:Q", title="USD per GPU-hour", scale=alt.Scale(zero=False)),
        tooltip=[alt.Tooltip("target_date:T"), alt.Tooltip("y:Q", title="truth", format=".4f"),
                 alt.Tooltip("q10:Q", format=".4f"), alt.Tooltip("q50:Q", format=".4f"), alt.Tooltip("q90:Q", format=".4f")])
    band = alt.Chart(sa).mark_area(color=ui.BLUE, opacity=0.18).encode(x="target_date:T", y="q10:Q", y2="q90:Q")
    med = alt.Chart(sa).mark_line(color=ui.BLUE, strokeWidth=1.5).encode(x="target_date:T", y="q50:Q")
    layers = [band, med]
    if cb is not None:
        sb = cb[(cb.series_id == sid) & (cb.horizon_days == h)].sort_values("target_date")
        layers += [alt.Chart(sb).mark_line(color=ui.ORANGE, strokeDash=[2, 2], strokeWidth=1).encode(x="target_date:T", y="q10:Q"),
                   alt.Chart(sb).mark_line(color=ui.ORANGE, strokeDash=[2, 2], strokeWidth=1).encode(x="target_date:T", y="q90:Q"),
                   alt.Chart(sb).mark_line(color=ui.ORANGE, strokeDash=[6, 3], strokeWidth=1.5).encode(x="target_date:T", y="q50:Q")]
    split = sa[sa.window == "holdout"].target_date.min()
    if pd.notna(split):
        layers.append(alt.Chart(pd.DataFrame({"x": [split]})).mark_rule(color=ui.GREY, strokeDash=[4, 4]).encode(x="x:T"))
        layers.append(alt.Chart(pd.DataFrame({"x": [split], "t": ["HOLDOUT →"]})).mark_text(align="left", dx=4, dy=-140, color="#666").encode(x="x:T", text="t:N"))
    with st.container(border=True):
        st.altair_chart(alt.layer(*layers, truth).properties(height=380).interactive(bind_y=False), width="stretch")
        legend = f"Black = truth · blue band/line = {ea} q10–q90 / q50"
        if cb is not None:
            legend += f" · orange dashed = {eb}"
        st.caption(legend + ". Scroll to zoom.")

    def stats(c, tag):
        x = c[c.series_id == sid]
        out = {}
        for w in ("dev", "holdout"):
            z = x[x.window == w]
            if len(z):
                out[f"{w} skill"] = 1 - z.loss.mean() / z.baseline_loss.mean() if z.baseline_loss.mean() > 0 else float("nan")
                out[f"{w} coverage"] = ((z.y >= z.q10) & (z.y <= z.q90)).mean()
        return {"experiment": tag, **out}
    tbl = [stats(ca, ea)] + ([stats(cb, eb)] if cb is not None else [])
    st.markdown("**This series, all horizons** (skill vs last value)")
    ui.metric_table(pd.DataFrame(tbl), [c for c in tbl[0] if c != "experiment"])

    st.markdown("**Skill per series**")
    win = st.segmented_control("Window", ["dev", "holdout"], default="dev", key="fc_win") or "dev"
    pa = store.per_series(d, ea, win)
    if pa is not None:
        p = pa[["series_id", "skill_pooled"]].rename(columns={"skill_pooled": ea})
        if eb:
            pb = store.per_series(d, eb, win)
            if pb is not None:
                p = p.merge(pb[["series_id", "skill_pooled"]].rename(columns={"skill_pooled": eb}), on="series_id", how="left")
        p = p.replace([float("inf"), float("-inf")], float("nan"))
        pl = p.melt("series_id", var_name="experiment", value_name="skill").dropna()
        pl["skill_clipped"] = pl.skill.clip(-1, 1)
        st.altair_chart(alt.Chart(pl).mark_bar().encode(
            y=alt.Y("series_id:N", sort=alt.EncodingSortField("skill", op="min"), title=None, axis=alt.Axis(labelLimit=380)),
            x=alt.X("skill_clipped:Q", title="skill (clipped to ±1)"), yOffset="experiment:N",
            color=alt.Color("experiment:N", scale=alt.Scale(range=[ui.BLUE, ui.ORANGE]), legend=alt.Legend(orient="top", title=None)),
            tooltip=["series_id", "experiment", alt.Tooltip("skill:Q", format="+.3f")]).properties(height=16 * len(p) * (2 if eb else 1)), width="stretch")


# ---------------------------------------------------------------- walk-forward
def walkforward():
    import walkforward as WF
    st.title("Walk-forward: is the self-improvement real?")
    st.caption("Each slice pretends to be an earlier date. The autonomous loop starts from the starter drift and iterates "
               "using only DEV and GATE origins up to that date. Every champion it produces is scored on the next TEST "
               "week, which no decision saw.")
    runs = store.walkforward_runs()
    if not runs:
        st.info("No walk-forward runs yet. Start one from the Lab.")
        return
    st.dataframe(pd.DataFrame([{"slice": s["name"], "DEV origins": " → ".join(s["dev"]), "GATE origins": " → ".join(s["gate"]),
                                "TEST origins (unseen)": " → ".join(s["test"])} for s in WF.SLICES]), hide_index=True, width="stretch")
    st.caption("S1–S3 come from walkforward.py; the W1–W6 slices of `*_wide` runs come from walkforward_wide.py.")
    pick = st.multiselect("Runs", list(runs), default=list(runs), key="wf_runs",
                          help="heuristic = rule-based proposer (no API); llm_* = gpt-4.1 proposer")
    if not pick:
        return
    w = pd.concat([store.load_walkforward(runs[n]).assign(run=n) for n in pick], ignore_index=True)
    w["outcome"] = w.accepted.map({True: "accepted", False: "rejected"})
    chart = alt.Chart(w).mark_line(point=alt.OverlayMarkDef(size=60, filled=True)).encode(
        x=alt.X("iteration:O", title="iteration of the autonomous loop"),
        y=alt.Y("test:Q", title=f"champion {K} on unseen TEST week", scale=alt.Scale(zero=False)),
        color=alt.Color("run:N", legend=alt.Legend(orient="top", title=None), scale=alt.Scale(range=[ui.BLUE, ui.ORANGE, ui.GREEN, ui.RED])),
        tooltip=["run", "slice", "iteration", "exp", "outcome", "champion", alt.Tooltip("test:Q", format="+.4f"),
                 alt.Tooltip("test_coverage:Q", format=".2f"), alt.Tooltip("hypothesis:N")]
    ).properties(height=260, width=260).facet(column=alt.Column("slice:N", title=None))
    with st.container(border=True):
        st.altair_chart(chart, width="content")
    g = w.groupby(["run", "slice"]).agg(seed_test=("test", "first"), final_test=("test", "last"),
                                        final_champion=("champion", "last"), iterations=("iteration", "count")).reset_index()
    g["gain"] = g.final_test - g.seed_test
    cols = st.columns(len(pick))
    for col, n in zip(cols, pick):
        x = g[g.run == n]
        col.metric(n, ui.fmt(x.gain.mean()), f"{int((x.gain > 0).sum())}/{len(x)} slices improved", delta_color="off",
                   help="mean TEST gain from the seed (drift) to the final champion")
    ui.metric_table(g[["run", "slice", "seed_test", "final_test", "gain", "final_champion", "iterations"]], ["seed_test", "final_test", "gain"])
    st.subheader("Every iteration")
    c1, c2 = st.columns(2)
    rn = c1.selectbox("Run", pick, key="wf_run")
    slices = sorted(w[w.run == rn].slice.unique())
    sl = c2.segmented_control("Slice", slices, default=slices[0], key=f"wf_slice_{rn}") or slices[0]
    x = w[(w.run == rn) & (w.slice == sl)][["iteration", "exp", "outcome", "champion", "dev", "gate", "test", "test_coverage", "hypothesis", "lesson"]]
    st.dataframe(x, hide_index=True, width="stretch",
                 column_config={c: st.column_config.NumberColumn(c, format="%+.4f") for c in ("dev", "gate", "test")}
                 | {"test_coverage": st.column_config.NumberColumn("test_coverage", format="%.2f")})
    st.caption(f"Full ledger: choose `walk-forward / {rn} / {sl}` in the sidebar and open the Research ledger.")


# ---------------------------------------------------------------- proposer log
def proposer_log():
    st.title("Proposer log")
    st.caption("What the proposer saw, what it proposed, what the validator refused, and the lesson it wrote. "
               "Proposals can only recombine and retune registered models, so a run can never break the evaluation.")
    have = {k: v for k, v in store.ledgers().items() if (v / "autoresearch_log.jsonl").exists()}
    if not have:
        st.info("No autonomous runs with a log yet.")
        return
    cur = st.session_state["ledger"]
    keys = list(have)
    label = st.selectbox("Autonomous run", keys, index=keys.index(cur) if cur in have else 0, key="pl_ledger")
    d = have[label]
    log = store.autoresearch_log(d)
    df = store.load_ledger(d).set_index("id")
    n_llm = sum(len(e.get("llm_calls") or []) for e in log)
    n_ref = sum(len(e.get("refused_before") or e.get("refused") or []) for e in log)
    m = st.columns(4)
    m[0].metric("Iterations", len(log))
    m[1].metric("Accepted", sum(1 for e in log if e.get("accepted")))
    m[2].metric("Refused proposals", n_ref, help="invalid or duplicate specs sent back to the proposer with the reason")
    m[3].metric("LLM calls", n_llm, help="0 means the rule-based (heuristic) proposer")
    for i, e in enumerate(log, 1):
        eid = e.get("id")
        with st.container(border=True):
            head = st.container(horizontal=True, vertical_alignment="center")
            head.markdown(f"### Iteration {e.get('iteration', i)}" + (f" · {eid}" if eid else ""))
            with head:
                if eid is None:
                    st.badge("no valid proposal", color="orange")
                else:
                    ui.decision_badge(bool(e.get("accepted")))
                    if eid in df.index:
                        st.caption(f"dev {ui.fmt(df.loc[eid, 'dev'])} · holdout {ui.fmt(df.loc[eid, 'holdout'])}")
            p = e.get("proposal") or {}
            if p:
                c1, c2 = st.columns(2)
                c1.markdown(f"**Observation.** {p.get('observation', '–')}")
                c1.markdown(f"**Hypothesis.** {p.get('hypothesis', '–')}")
                c2.markdown(f"**Change.** {p.get('change', '–')}")
                if p.get("expected_effect"):
                    c2.markdown(f"**Expected effect.** {p['expected_effect']}")
                if p.get("spec"):
                    c2.caption(ui.spec_summary(p["spec"]))
            if e.get("lesson"):
                st.markdown(f"**Lesson.** {e['lesson']}")
            refused = e.get("refused_before") or e.get("refused") or []
            for j, rf in enumerate(refused, 1):
                st.error(f"Refused attempt {j}: " + "; ".join(rf.get("errors", [])), icon=":material/block:")
            calls = e.get("llm_calls") or []
            if calls:
                with st.expander(f"{len(calls)} LLM call{'s' if len(calls) > 1 else ''} (prompt and reply)"):
                    for k, c in enumerate(calls, 1):
                        st.markdown(f"**Call {k}** · system: _{ui.short(c.get('system', ''), 140)}_")
                        t1, t2 = st.tabs(["Reply", "Prompt"])
                        with t1:
                            rep = c.get("reply", "")
                            try:
                                st.json(json.loads(rep), expanded=True)
                            except Exception:
                                st.markdown(rep)
                        with t2:
                            st.code(c.get("user", ""), language="json", height=320)


# ---------------------------------------------------------------- submission
def submission():
    st.title("Submission")
    st.caption(f"The frozen Sunday forecast: origin {C.CUTOFF}, horizons {', '.join(map(str, C.HORIZONS))} days, "
               "written by submit.py from the champion.")
    subs = store.submissions()
    if not subs:
        st.info("No submission files yet.")
        return
    keys = list(subs)
    default = next((k for k in keys if k.startswith("submission_final")), keys[0])
    name = st.selectbox("File", keys, index=keys.index(default), key="sb_file")
    sub = pd.read_csv(subs[name], parse_dates=["origin_date", "target_date"])
    m = st.columns(4)
    m[0].metric("Rows", len(sub))
    m[1].metric("Series", sub.series_id.nunique())
    m[2].metric("Method", (sub.method_note.dropna().iloc[0] if "method_note" in sub and sub.method_note.notna().any() else "–").replace("gpu_scientist ", ""))
    m[3].metric("Median relative width", f"{((sub.q90 - sub.q10) / sub.q50).median():.1%}", help="(q90 − q10) / q50")
    sid = st.selectbox("Series", sorted(sub.series_id.unique()), key="sb_sid")
    s = sub[sub.series_id == sid]
    hist = None
    for led in store.ledgers().values():
        ch = (store.champion(led) or {}).get("id")
        c = store.cells(led, ch) if ch else None
        if c is not None:
            hist = c[(c.series_id == sid) & (c.horizon_days == 1)][["target_date", "y"]].drop_duplicates("target_date")
            break
    layers = []
    if hist is not None and len(hist):
        hist = hist[hist.target_date >= hist.target_date.max() - pd.Timedelta(days=45)]
        layers.append(alt.Chart(hist).mark_line(color="#191919").encode(
            x=alt.X("target_date:T", title=None), y=alt.Y("y:Q", title="USD per GPU-hour", scale=alt.Scale(zero=False)),
            tooltip=[alt.Tooltip("target_date:T"), alt.Tooltip("y:Q", format=".4f")]))
    layers += [alt.Chart(s).mark_errorbar(color=ui.BLUE, thickness=2, ticks=True).encode(x="target_date:T", y="q10:Q", y2="q90:Q"),
               alt.Chart(s).mark_point(color=ui.BLUE, filled=True, size=80).encode(
                   x="target_date:T", y="q50:Q", tooltip=["horizon_days", alt.Tooltip("q10:Q", format=".4f"),
                                                          alt.Tooltip("q50:Q", format=".4f"), alt.Tooltip("q90:Q", format=".4f")])]
    with st.container(border=True):
        st.altair_chart(alt.layer(*layers).properties(height=320), width="stretch")
        st.caption("Black = last 45 days of the series up to the cutoff · blue = forecast median with the q10–q90 interval.")
    st.dataframe(sub, hide_index=True, width="stretch")
    st.download_button("Download CSV", subs[name].read_bytes(), file_name=subs[name].name, mime="text/csv", icon=":material/download:")
