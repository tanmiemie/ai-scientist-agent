"""Shared formatting, spec helpers and charts."""
from __future__ import annotations

import json

import altair as alt
import pandas as pd
import streamlit as st

import autoresearch as AR
from store import K

BLUE, ORANGE, GREEN, GREY, RED = "#317CFF", "#E8833A", "#2E9E5B", "#A0A4AB", "#D64545"


def fmt(x, signed: bool = True, nd: int = 3) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "–"
    return f"{x:+.{nd}f}" if signed else f"{x:.{nd}f}"


def short(text: str, n: int = 160) -> str:
    text = (text or "").replace("\n", " ")
    return text if len(text) <= n else text[: n - 1] + "…"


def decision_badge(accepted: bool, is_seed: bool = False):
    if is_seed:
        st.badge("seed", color="gray")
    elif accepted:
        st.badge("accepted", icon=":material/check:", color="green")
    else:
        st.badge("rejected", icon=":material/close:", color="red")


def spec_summary(spec: dict) -> str:
    try:
        s = AR.normalize(spec)
    except Exception:
        return json.dumps(AR.clean(spec))[:120]
    parts = []
    for m in s["models"]:
        cls_defaults = AR.M.REGISTRY[m["name"]].defaults if m["name"] in AR.M.REGISTRY else {}
        changed = {k: v for k, v in m["params"].items() if cls_defaults.get(k) != v}
        parts.append(m["name"] + (f"({', '.join(f'{k}={v}' for k, v in changed.items())})" if changed else ""))
    comb = s["combine"]
    txt = " + ".join(parts)
    if comb["method"] != "single":
        txt += f" · {comb['method']}" + (f" η={comb['eta']} by {comb['group_by']}" if comb["method"] == "hedge" else "")
    cal = s["calibrate"]
    txt += f" · calibrated by {cal['group_by']} (γ={cal['gamma']}, scale={cal['scale']})" if cal["enabled"] else " · no calibration"
    return txt


def _flat(d, prefix=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(_flat(v, f"{prefix}{k}."))
    elif isinstance(d, list):
        for i, v in enumerate(d):
            name = v.get("name") if isinstance(v, dict) else None
            out.update(_flat(v, f"{prefix}{i}{'(' + name + ')' if name else ''}."))
    else:
        out[prefix[:-1]] = d
    return out


def spec_diff(old: dict | None, new: dict) -> pd.DataFrame:
    """What actually changes in the run (normal form), parameter by parameter."""
    try:
        a = _flat(AR.normalize(old)) if old else {}
        b = _flat(AR.normalize(new))
    except Exception:
        a, b = _flat(AR.clean(old or {})), _flat(AR.clean(new))
    keys = sorted(set(a) | set(b))
    rows = [{"setting": k, "before": a.get(k, "—"), "after": b.get(k, "—")} for k in keys if a.get(k) != b.get(k)]
    return pd.DataFrame(rows, columns=["setting", "before", "after"]).astype(str)


def progress_chart(df: pd.DataFrame, height: int = 320) -> alt.Chart:
    d = df.assign(outcome=df.accepted.map({True: "accepted", False: "rejected"}),
                  hyp=df.hypothesis.map(lambda h: short(h, 120)))
    long = d.melt(id_vars=["i", "id", "outcome", "hyp", "lesson"], value_vars=["dev", "holdout"],
                  var_name="window", value_name="skill")
    base = alt.Chart(long).encode(x=alt.X("i:O", title="experiment"))
    tooltip = ["id", "window", alt.Tooltip("skill:Q", format="+.4f"), "outcome", alt.Tooltip("hyp:N", title="hypothesis")]
    pts = base.mark_point(size=90, filled=True, opacity=0.9).encode(
        y=alt.Y("skill:Q", title=f"{K} vs last value", scale=alt.Scale(zero=False)),
        color=alt.Color("window:N", scale=alt.Scale(domain=["dev", "holdout"], range=[BLUE, ORANGE]),
                        legend=alt.Legend(title=None, orient="top-left")),
        shape=alt.Shape("outcome:N", scale=alt.Scale(domain=["accepted", "rejected"], range=["circle", "cross"]),
                        legend=alt.Legend(title=None, orient="top-left")),
        tooltip=tooltip)
    champ = alt.Chart(d).mark_line(interpolate="step-after", color=GREEN, strokeWidth=2.5).encode(
        x="i:O", y="champion_holdout:Q", tooltip=["champion_after", alt.Tooltip("champion_holdout:Q", format="+.4f")])
    zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color=GREY, strokeDash=[3, 3]).encode(y="y:Q")
    labels = alt.Chart(d).mark_text(dy=-12, fontSize=10, color="#666").encode(
        x="i:O", y="dev:Q", text=alt.Text("id:N"))
    return (zero + champ + pts + labels).properties(height=height).configure_view(stroke=None)


def metric_table(df: pd.DataFrame, value_cols: list[str], fmt: str = "%+.3f"):
    st.dataframe(df, hide_index=True, width="stretch",
                 column_config={c: st.column_config.NumberColumn(c, format=fmt) for c in value_cols})
