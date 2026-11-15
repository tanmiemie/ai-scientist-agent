"""Ranking and bookkeeping of the batch proposer (idea_batch.py); no API calls."""
import json

import autoresearch as A
import idea_batch as B

SPEC = {"models": [{"name": "momentum", "params": {"beta": 0.5}}], "combine": {"method": "single"},
        "calibrate": {"enabled": True, "gamma": 0.5, "scale": 0.01, "group_by": "source_class"}}


def idea(g, f, n, spec=SPEC):
    return {"hypothesis": f"{g}{f}{n}", "spec": spec, "scores": {"gain": g, "feasibility": f, "novelty": n}}


def test_seed_ideas_cover_the_protocol_menu():
    ideas = json.loads(B.SEED_IDEAS.read_text())["ideas"]
    assert len(ideas) == 7 and len({i["id"] for i in ideas}) == 7
    assert all({"id", "title", "diagnosis_signal", "change", "tools"} <= set(i) for i in ideas)


def test_total_clamps_scores_to_1_10():
    assert B.total(idea(15, 0, 5)) == 10 + 1 + 5
    assert B.total({"scores": {"gain": "x"}}) == 0.0
    assert B.total({}) == 3.0


def test_rank_orders_by_total_then_gain_then_position():
    r = B.rank([idea(5, 5, 5), idea(9, 9, 9), idea(6, 5, 4), idea(5, 5, 5)], set(), False)
    assert [x["index"] for x in r] == [1, 2, 0, 3]


def test_invalid_and_tried_ideas_are_marked_not_dropped():
    bad = {"models": [{"name": "nope"}]}
    r = B.rank([idea(10, 10, 10, bad), idea(9, 9, 9), idea(1, 1, 1, {})], {A.spec_hash(SPEC)}, False)
    assert len(r) == 3
    assert all(x["refused"] for x in r)
    assert "unknown or disallowed model" in r[0]["refused"][0]
    assert "already tried" in r[1]["refused"][0]


def test_propose_runs_top_valid_idea_and_logs_every_idea(tmp_path, monkeypatch):
    monkeypatch.setattr(B.C, "EXPERIMENTS", tmp_path)
    monkeypatch.setattr(B.run_experiment, "next_id", lambda: "exp_009")
    spec2 = {**SPEC, "models": [{"name": "momentum", "params": {"beta": 0.75}}]}
    batch = {"biggest_miss": "x", "ideas": [idea(10, 10, 10, {"models": []}), idea(8, 8, 8), idea(9, 9, 9, spec2),
                                            idea(2, 2, 2), idea(3, 3, 3)]}
    replies = [json.dumps(batch), json.dumps({**batch, "reflection": "checked"})]
    p = B.BatchProposer.__new__(B.BatchProposer)
    p.heavy, p.calls, p.seed_ideas = False, [], []
    p._chat = lambda system, user, as_json: replies.pop(0)
    ctx = {"champion": {"id": "exp_000"}, "history": [], "diagnosis_md": "", "tried": set()}
    out = p.propose(ctx)
    assert out["spec"] == spec2 and "refused" not in out and "total" not in out
    log = json.loads((tmp_path / "ideas.json").read_text())
    assert len(log) == 1 and len(log[0]["ideas"]) == 5 and log[0]["selected_index"] == 2
    assert sum(i["selected"] for i in log[0]["ideas"]) == 1 and log[0]["reflection"] == "checked"


def test_rank_survives_non_numeric_scores():
    from idea_batch import rank
    good = {"scores": {"gain": 5, "feasibility": 5, "novelty": 5}}
    bad = {"scores": {"gain": "8/10", "feasibility": 9, "novelty": 9}}
    out = rank([bad, good], set(), False)
    assert [r["index"] for r in out] == [1, 0]
    assert out[1]["total"] == 0.0
