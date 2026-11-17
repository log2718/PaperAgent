"""Retrieval-only metrics: how well each retrieval configuration finds the gold evidence, with no answer-model calls.

    python src/retrieval_metrics.py        # writes runs/retrieval_metrics.md and .json

For each of the text-involving development questions (the workbook's gold evidence is a list of (paper, page) pairs):
  gold pages covered  share of gold (paper, page) pairs inside a retrieved unit's page span (a whole paper covers all its pages)
  papers retrieved    share of the question's required papers that appear among the retrieved units
  MRR                 1 / rank of the first retrieved unit that covers a gold page (0 if none does)
  context tokens      size of what would be shown to the model
Sweeps: K in {1, 3, 5, 10, 20} for token and paragraph chunks, N in {1, 2, 3, 5} papers for the paper-level index, plus the
paragraph budget run and the logged choices of the no_embedding router.
"""
import collections
import json
import statistics

from transformers import AutoTokenizer

from answer import MATCHED_BUDGET_TOKENS
from evaluate import gold_pages, load_sheet
from ingest import EMBED_MODEL, ROOT, n_tokens
from retrieve import search_budget, search_papers

SWEEPS = {"token": (1, 3, 5, 10, 20), "paragraph": (1, 3, 5, 10, 20), "paper": (1, 2, 3, 5)}
DEFAULT = [("token", 5), ("paragraph", 5), ("paragraph budget", None), ("paper", 3), ("no_embedding", None)]


def score(hits, gold, required, tokens):
    """hits: dicts with paper, page_start, page_end (in rank order)."""
    covered = {(h["paper"], p) for h in hits for p in range(h["page_start"], h["page_end"] + 1)}
    mrr = next((1 / r for r, h in enumerate(hits, 1) if any((h["paper"], p) in gold for p in range(h["page_start"], h["page_end"] + 1))), 0)
    return {"pages": len(gold & covered) / len(gold), "papers": len(required & {h["paper"] for h in hits}) / len(required),
            "mrr": mrr, "tokens": tokens}


def main():
    tok = AutoTokenizer.from_pretrained(EMBED_MODEL, trust_remote_code=True)
    tok.model_max_length = 10**9
    sizes = {}                                                   # chunk_id -> tokens (counted once)

    def size(h):
        if h["chunk_id"] not in sizes:
            sizes[h["chunk_id"]] = h["tokens"] or n_tokens(tok, h["text"])
        return sizes[h["chunk_id"]]

    qs = [q for q in load_sheet("Questions") if q["split"] == "development" and q["data_source_type"] != "table-only"]
    gold = gold_pages()
    req = {q["question_id"]: {x.strip() for x in q["required_papers"].split(";")} for q in qs}
    res = collections.defaultdict(dict)                          # (config, setting) -> question_id -> metrics
    for q in qs:
        i, text = q["question_id"], q["question"]
        for mode, ks in SWEEPS.items():
            hits = search_papers(text, max(ks), mode)
            for k in ks:
                res[(mode, k)][i] = score(hits[:k], gold[i], req[i], sum(size(h) for h in hits[:k]))
        hits = search_budget(text, MATCHED_BUDGET_TOKENS, "paragraph")
        res[("paragraph budget", None)][i] = score(hits, gold[i], req[i], sum(size(h) for h in hits))
    path = ROOT / "runs" / "no_embedding" / "results.jsonl"
    if path.exists():
        for r in map(json.loads, open(path, encoding="utf-8")):
            if r["question_id"] in req and "router" in r:
                hits = [{"paper": h["paper"], "page_start": int(h["pages"].partition("-")[0]),
                         "page_end": int((h["pages"].partition("-")[2] or h["pages"])), "chunk_id": h["chunk_id"]} for h in r["retrieved"]]
                res[("no_embedding", None)][r["question_id"]] = score(hits, gold[r["question_id"]], req[r["question_id"]], sum(h["tokens"] for h in r["retrieved"]))

    mean = lambda xs: statistics.mean(xs) if xs else float("nan")
    name = lambda c, k: f"{c} K={k}" if c in ("token", "paragraph") else f"{c} N={k}" if c == "paper" else c
    lines = ["# Retrieval-only metrics", "", f"{len(qs)} text-involving development questions. Gold evidence = the workbook's (paper, page) pairs. "
             "A whole paper covers all its pages, so for paper-level configurations 'gold pages covered' equals the share of gold pairs whose paper was retrieved. "
             "`no_embedding` uses the router's logged choices.", "",
             "| Configuration | Questions | Gold pages covered | Papers retrieved | MRR | Mean context tokens |", "|---|---|---|---|---|---|"]
    for (c, k), per in res.items():
        m = list(per.values())
        lines.append(f"| {name(c, k)} | {len(m)} | {mean([x['pages'] for x in m]):.2f} | {mean([x['papers'] for x in m]):.2f} | "
                     f"{mean([x['mrr'] for x in m]):.2f} | {mean([x['tokens'] for x in m]):,.0f} |")
    types = sorted({q["question_type"] for q in qs})
    qtype = {q["question_id"]: q["question_type"] for q in qs}
    lines += ["", "Gold pages covered by question type, at the default settings:", "",
              "| Configuration | " + " | ".join(f"{t} (n={sum(v == t for v in qtype.values())})" for t in types) + " |", "|---|" + "---|" * len(types)]
    for c, k in DEFAULT:
        if (c, k) in res:
            lines.append(f"| {name(c, k)} | " + " | ".join(f"{mean([x['pages'] for i, x in res[(c, k)].items() if qtype[i] == t]):.2f}" for t in types) + " |")
    present = [d for d in DEFAULT if d in res]
    lines += ["", "Gold pages covered per question at the default settings:", "", "| ID | Type | " + " | ".join(name(*d) for d in present) + " |",
              "|---|---|" + "---|" * len(present)]
    for q in qs:
        lines.append(f"| {q['question_id']} | {q['question_type']} | " + " | ".join(f"{res[d][q['question_id']]['pages']:.2f}" if q["question_id"] in res[d] else "-" for d in present) + " |")
    never = [q["question_id"] for q in qs if all(res[d].get(q["question_id"], {"pages": 0})["pages"] == 0 for d in present)]
    lines += ["", "Questions with no gold page retrieved under every default configuration: " + (", ".join(never) or "none") + "."]
    out = ROOT / "runs"
    (out / "retrieval_metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "retrieval_metrics.json").write_text(json.dumps({name(c, k): per for (c, k), per in res.items()}, indent=1))
    print("\n".join(lines[:4 + len(res) + 2]))
    print(f"-> {out / 'retrieval_metrics.md'}")


if __name__ == "__main__":
    main()
