import json

import pytest

import review
from conftest import ROOT

FINAL = ROOT / "experiments_final"


def _reply(**over):
    items = {k: {"flag": False, "evidence": "", "severity": 1} for k in review.ITEMS}
    items.update(over)
    return json.dumps({"items": items, "summary": ""})


def test_parse_accepts_complete_checklist():
    out = review._parse(_reply(other={"flag": True, "evidence": "x", "severity": 3}))
    assert out["other"] == {"flag": True, "evidence": "x", "severity": 3}


@pytest.mark.parametrize("bad", [
    "no json here",
    "{}",
    json.dumps({"items": {"other": {"flag": True, "evidence": "x", "severity": 2}}}),  # omitted items
    _reply(other={"flag": "false", "evidence": "x", "severity": 2}),                  # string boolean
    _reply(other={"flag": True, "evidence": "x", "severity": 4}),                     # severity out of range
    _reply(other={"flag": True, "evidence": "x", "severity": True}),
])
def test_parse_rejects_invalid(bad):
    with pytest.raises(ValueError):
        review._parse(bad)


def test_invalid_replies_are_retried_not_counted(monkeypatch):
    replies = iter(["{}", _reply(other={"flag": True, "evidence": "x", "severity": 2})])
    monkeypatch.setattr(review, "_chat", lambda *a: next(replies))
    assert review._one_review("openai", "m", "u")["other"]["flag"] is True
    monkeypatch.setattr(review, "_chat", lambda *a: "{}")
    with pytest.raises(RuntimeError):
        review._one_review("openai", "m", "u")


def test_archived_evidence_ignores_current_windows(monkeypatch):
    if not (FINAL / "ledger.jsonl").exists():
        pytest.skip("experiments_final not present")
    before = review.evidence(FINAL, "exp_002")["mean_log_interval_width_q90_over_q10"]
    monkeypatch.setattr(review.C, "DEV_ORIGINS", ("2026-09-15", "2026-09-30"))
    monkeypatch.setattr(review.C, "HOLDOUT_ORIGINS", ("2026-10-20", "2026-10-21"))
    assert review.evidence(FINAL, "exp_002")["mean_log_interval_width_q90_over_q10"] == before
