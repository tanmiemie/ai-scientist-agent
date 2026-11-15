"""The research memory.

  python ledger.py show                 # every experiment, one line each
  python ledger.py lesson exp_004 "..."  # record what an experiment taught us (do this every time)
  python ledger.py lessons              # all lessons so far (read before proposing a hypothesis)
  python ledger.py plot                 # experiments/progress.png: dev and holdout skill per iteration
"""
import json
import sys

import config as C

PATH = C.EXPERIMENTS / "ledger.jsonl"


def load():
    return [json.loads(l) for l in PATH.read_text().splitlines() if l.strip()] if PATH.exists() else []


def save(recs):
    PATH.write_text("".join(json.dumps(r, default=str) + "\n" for r in recs))


def show():
    for r in load():
        k = C.PRIMARY_METRIC
        print(f"{r['id']}  {'ACC' if r['accepted'] else 'rej'}  dev {r['dev'][k]:+.4f}  hold {r['holdout'][k]:+.4f}  "
              f"cov {r['dev']['coverage_in']:.2f}  parent={r['parent']}  | {r['hypothesis'][:90]}")


def lesson(eid, text):
    recs = load()
    for r in recs:
        if r["id"] == eid:
            r["lesson"] = text
    save(recs)


def lessons():
    for r in load():
        print(f"- {r['id']} ({'accepted' if r['accepted'] else 'rejected'}): {r['hypothesis']}\n    lesson: {r.get('lesson')}")


def plot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    recs, k = load(), C.PRIMARY_METRIC
    if not recs:
        return
    x = range(len(recs))
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(x, [r["dev"][k] for r in recs], "o-", label="dev (seen while iterating)", color="#4C78A8")
    ax.plot(x, [r["holdout"][k] for r in recs], "s--", label="holdout (unseen)", color="#F58518")
    champ, best = [], -9
    for r in recs:
        if r["accepted"]:
            best = r["holdout"][k]
        champ.append(best)
    ax.step(x, champ, where="post", color="#54A24B", label="champion on holdout")
    for i, r in enumerate(recs):
        ax.annotate(r["id"].replace("exp_", ""), (i, r["dev"][k]), textcoords="offset points", xytext=(0, 6),
                    ha="center", fontsize=7, color="#4C78A8" if r["accepted"] else "#999")
    ax.axhline(0, color="#999", lw=0.8)
    ax.set_xlabel("experiment"); ax.set_ylabel(f"{k} (vs last value)")
    ax.set_title("Self-improvement across iterations"); ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(C.EXPERIMENTS / "progress.png", dpi=150)
    print(C.EXPERIMENTS / "progress.png")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    {"show": show, "lessons": lessons, "plot": plot}.get(cmd, lambda: lesson(sys.argv[2], sys.argv[3]))()
