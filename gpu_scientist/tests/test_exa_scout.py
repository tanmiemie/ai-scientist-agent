"""Exa scout: no page dated after the run's cutoff reaches the proposer, undated market news is
dropped, and the evidence memory deduplicates by URL. Exa itself is mocked (no key, no network)."""
import json

import config as C
import exa_scout


def fake_post(body):
    assert body["endPublishedDate"].startswith(exa_scout.cutoff_date())
    return {"results": [
        {"title": "ok", "url": "https://a.example/1", "publishedDate": "2026-10-01T00:00:00Z", "highlights": ["h"]},
        {"title": "late", "url": "https://a.example/2", "publishedDate": "2099-01-01T00:00:00Z"},
        {"title": "undated", "url": "https://a.example/3"},
    ]}


def test_scout_filters_and_remembers(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "EXPERIMENTS", tmp_path)
    monkeypatch.setattr(exa_scout, "_post", fake_post)
    ctx = {"champion": {"dev": {"coverage_above_q90": 0.2, "coverage_below_q10": 0.05, "coverage_in": 0.75}}}
    out = exa_scout.scout(ctx, iteration=1)
    urls = {(r["kind"], r["url"]) for r in out["found_this_turn"]}
    assert ("market", "https://a.example/2") not in urls and ("method", "https://a.example/2") not in urls
    assert ("market", "https://a.example/3") not in urls          # undated market news dropped
    assert ("method", "https://a.example/3") in urls              # undated method page kept
    assert "above the upper" in out["queries"]["method"]
    n1 = sum(1 for _ in open(tmp_path / "evidence.jsonl"))
    exa_scout.scout(ctx, iteration=2)
    assert sum(1 for _ in open(tmp_path / "evidence.jsonl")) == n1  # same URLs are not stored twice
    assert all((r.get("published") or "") <= exa_scout.cutoff_date() for r in out["memory_for_prompt"]
               if r["kind"] == "market")


def test_scout_survives_exa_errors(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "EXPERIMENTS", tmp_path)

    def boom(body):
        raise RuntimeError("down")
    monkeypatch.setattr(exa_scout, "_post", boom)
    ctx = {"champion": {"dev": {"coverage_above_q90": 0.1, "coverage_below_q10": 0.1, "coverage_in": 0.8}}}
    out = exa_scout.scout(ctx, 1)
    assert out["errors"] and out["found_this_turn"] == []
