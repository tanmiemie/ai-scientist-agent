"""GPU Value AI Scientist: interactive app.  Run from this folder:  streamlit run main.py"""
from __future__ import annotations

import streamlit as st

import store  # noqa: F401  (puts gpu_scientist/ on sys.path)
import labview
import views

SESSION_URL = "https://app.devin.ai/sessions/30a4d7f30aa146118bf96df7d0dea605"

st.set_page_config(page_title="GPU Value AI Scientist", page_icon=":material/biotech:", layout="wide")
st.markdown("""<style>
.block-container {padding-top: 2.2rem; max-width: 1400px;}
[data-testid="stMetricValue"] {font-variant-numeric: tabular-nums; font-size: 1.6rem;}
code {font-size: 0.82em;}
</style>""", unsafe_allow_html=True)

pages = {
    "Results": [
        st.Page(views.overview, title="Overview", icon=":material/dashboard:", url_path="overview", default=True),
        st.Page(views.timeline, title="Research ledger", icon=":material/history_edu:", url_path="ledger"),
        st.Page(views.diagnosis, title="Diagnosis", icon=":material/monitor_heart:", url_path="diagnosis"),
        st.Page(views.forecasts, title="Forecast explorer", icon=":material/show_chart:", url_path="forecasts"),
        st.Page(views.walkforward, title="Walk-forward", icon=":material/timeline:", url_path="walkforward"),
        st.Page(views.proposer_log, title="Proposer log", icon=":material/forum:", url_path="proposer"),
        st.Page(views.submission, title="Submission", icon=":material/upload_file:", url_path="submission"),
    ],
    "Interact": [
        st.Page(labview.lab_page, title="Lab", icon=":material/science:", url_path="lab"),
    ],
}
nav = st.navigation(pages)

with st.sidebar:
    ledgers = list(store.ledgers())
    cur = st.session_state.get("ledger")
    st.selectbox("Ledger", ledgers, index=ledgers.index(cur) if cur in ledgers else 0, key="ledger",
                 help="Which research record the Results pages show. experiments_final is the main run; "
                      "walk-forward and lab runs each have their own.")
    st.caption(f"[Request changes]({SESSION_URL})")

nav.run()
