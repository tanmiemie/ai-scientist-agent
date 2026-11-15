"""Compare walkforward/llm_exa (Exa evidence each iteration) with walkforward/llm_openai_v2 (no Exa)."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent / "walkforward"


def slices(run):
    s = W / run / "summary.json"
    rows = json.loads(s.read_text()) if s.exists() else []
    out = {}
    for r in rows:
        out.setdefault(r["slice"], []).append(r)
    return out


def gain(rows):
    return round(rows[-1]["test"] - rows[0]["test"], 4) if rows else None


def main():
    exa, v2 = slices("llm_exa"), slices("llm_openai_v2")
    print("| slice | v2 seed TEST | v2 final TEST | v2 gain | Exa final TEST | Exa gain | Exa accepted |")
    print("|---|---|---|---|---|---|---|")
    for s in ("S1", "S2", "S3"):
        a, b = v2.get(s, []), exa.get(s, [])
        acc = sum(r["accepted"] for r in b[1:]) if b else "-"
        fin = b[-1]["test"] if b else "not run"
        print(f"| {s} | {a[0]['test']:.4f} | {a[-1]['test']:.4f} | {gain(a):+.4f} | {fin} | "
              f"{'' if gain(b) is None else f'{gain(b):+.4f}'} | {acc} |")
    print("\n| slice | exp | source_url | in Exa evidence | kind | published | accepted |")
    print("|---|---|---|---|---|---|---|")
    n_cited = n_kept = 0
    for s in ("S1", "S2", "S3"):
        d = W / "llm_exa" / s / "experiments"
        if not (d / "autoresearch_log.jsonl").exists():
            continue
        ev = {}
        if (d / "evidence.jsonl").exists():
            for l in (d / "evidence.jsonl").read_text().splitlines():
                r = json.loads(l)
                ev[r["url"]] = r
        for l in (d / "autoresearch_log.jsonl").read_text().splitlines():
            e = json.loads(l)
            u = e.get("source_url")
            if not u:
                continue
            n_cited += 1
            n_kept += bool(e.get("accepted"))
            r = ev.get(u, {})
            print(f"| {s} | {e['id']} | {u} | {'yes' if r else 'no'} | {r.get('kind', '')} | "
                  f"{r.get('published') or ''} | {e.get('accepted')} |")
    print(f"\ncited a source: {n_cited}; of these kept: {n_kept}")


if __name__ == "__main__":
    main()
