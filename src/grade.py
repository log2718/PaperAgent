"""Blind grading helpers for the 0/1/2 rubric in evaluation/grading_rubric.md. No model is called here.

    python src/grade.py packet runs/baseline runs/other     # one blind packet per question, all runs side by side
    python src/grade.py check runs/_grading/grades.jsonl    # validate grader output against the rubric's rules
    python src/grade.py summarize runs/_grading/grades.jsonl  # per-run grades.jsonl + grades.md, and comparison.md

`packet` writes runs/_grading/packets.jsonl (what a grader sees) and key.json (label -> run, kept apart so graders stay blind).
Identical answers from different runs share one label, so they are graded once. Each candidate carries a mechanical citation
check: cited papers/pages that lie outside every retrieved passage. Development questions only unless --split held-out.
"""
import argparse
import collections
import json
import random
import re
from pathlib import Path

from evaluate import gold_pages, load_sheet
from ingest import ROOT
from sql_tool import as_text

GRADING = ROOT / "runs" / "_grading"
FAILURES = {"none", "retrieval_miss", "partial_retrieval", "generation_error", "sql_error", "over_abstention",
            "abstention_failure", "citation_error", "other"}
ZERO_OK = {"over_abstention", "abstention_failure", "retrieval_miss", "sql_error"}
CITE = re.compile(r"\[([^\[\],]+?),\s*pp?\.\s*([^\]]*)\]")
key = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def load_runs(dirs):
    runs = {}
    for d in dirs:
        recs = [json.loads(l) for l in open(ROOT / d / "results.jsonl", encoding="utf-8")]
        runs[d] = {r["question_id"]: r for r in recs}            # last record per question wins
    return runs


def spans(rec):
    out = collections.defaultdict(list)
    for h in rec.get("retrieved") or []:
        a, _, b = h["pages"].partition("-")
        out[key(h["paper"])].append((int(a), int(b or a)))
    return out


def citations(answer, papers):
    """[(paper, [page numbers])] parsed from '[Paper, p.N]' style citations."""
    found = []
    for name, rest in CITE.findall(answer):
        rest = re.split(r"[A-Za-z\"]", re.sub(r"pp?\.", "", rest), maxsplit=1)[0]
        pages = []
        for a, b in re.findall(r"(\d+)(?:\s*[-–]\s*(\d+))?", rest):
            pages += list(range(int(a), int(b or a) + 1))
        found.append((name.strip(), pages))
    return found


def citation_check(rec, papers, gold):
    sp, cites = spans(rec), citations(rec.get("answer", ""), papers)
    chk = {"n_citations": len(cites), "unknown_papers": [], "paper_not_retrieved": [], "page_not_retrieved": []}
    cited_pairs = set()
    for name, pages in cites:
        if key(name) not in papers:
            chk["unknown_papers"].append(name); continue
        short = papers[key(name)]
        cited_pairs |= {(short, p) for p in pages}
        if key(name) not in sp:
            chk["paper_not_retrieved"].append(short)
        elif pages and not any(a <= p <= b for p in pages for a, b in sp[key(name)]):
            chk["page_not_retrieved"].append(f"{short} p.{pages[0]}-{pages[-1]}")
    covered = {(papers[k], p) for k, v in sp.items() for a, b in v for p in range(a, b + 1)}
    chk["gold_pairs_cited"] = f"{len(gold & cited_pairs)}/{len(gold)}" if gold else "n/a"
    chk["gold_pairs_retrieved"] = f"{len(gold & covered)}/{len(gold)}" if gold else "n/a"
    return chk


def packet(args):
    qs = {q["question_id"]: q for q in load_sheet("Questions")}
    papers = {key(p["short_name"]): p["short_name"] for p in load_sheet("Papers")}
    gold, ev = gold_pages(), collections.defaultdict(list)
    for r in load_sheet("Evidence"):
        ev[r["question_id"]].append({"paper": r["paper_short_name"], "page": r["page"], "passage": (r["supporting_passage"] or "")[:300]})
    tab = {r["question_id"]: (r["supporting_rows_or_result"] or "")[:800] for r in load_sheet("TabularEvidence")}
    runs = load_runs(args.runs)
    ids = [i for i in qs if qs[i]["split"] == args.split and any(i in r for r in runs.values()) and (not args.ids or i in args.ids)]
    GRADING.mkdir(parents=True, exist_ok=True)
    out, labels = [], {}
    for qid in ids:
        groups = collections.defaultdict(list)                   # identical answers share one candidate
        for d, recs in runs.items():
            if qid in recs:
                groups[recs[qid].get("answer") or f"(run error) {recs[qid].get('error', '')}"].append(d)
        order = list(groups.items())
        random.Random(f"{args.seed}-{qid}").shuffle(order)
        cands, labels[qid] = [], {}
        for letter, (answer, ds) in zip("ABCDEFGH", order):
            rec = runs[ds[0]][qid]
            att = (rec.get("sql_attempts") or [{}])[-1]
            c = {"label": letter, "answer": answer,
                 "retrieved": [f"{h['paper']} p.{h['pages']}" for h in rec.get("retrieved") or []],
                 "citation_check": citation_check(rec, papers, gold[qid]),
                 "sql": att.get("sql"), "sql_result": as_text(att["result"])[:500] if "result" in att else att.get("error")}
            if args.with_text:
                c["retrieved_text"] = [{"where": f"{h['paper']} p.{h['pages']}", "text": h.get("text", "")[:1500]} for h in rec.get("retrieved") or []]
            cands.append(c); labels[qid][letter] = ds
        q = qs[qid]
        out.append({"question_id": qid, "question": q["question"], "source_type": q["data_source_type"], "answerable": q["answerable"],
                    "reference_answer": q["reference_answer"], "notes": q["notes"], "gold_evidence": ev[qid], "gold_sql_result": tab.get(qid),
                    "candidates": cands})
    with open(GRADING / "packets.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(p, ensure_ascii=False) + "\n" for p in out)
    (GRADING / "key.json").write_text(json.dumps({"runs": args.runs, "seed": args.seed, "labels": labels}, indent=1))
    print(f"{len(out)} packets, {sum(len(p['candidates']) for p in out)} candidates -> {GRADING}")


def read_grades(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def problems(g):
    bad = []
    if g.get("score") not in (0, 1, 2):
        return ["score must be 0, 1 or 2"]
    if g.get("failure_mode") not in FAILURES:
        bad.append(f"failure_mode must be one of {sorted(FAILURES)}")
    if not (g.get("rationale") or "").strip():
        bad.append("rationale is empty")
    lists = [g.get(k) for k in ("missing_points", "wrong_claims", "citation_issues")]
    if not all(isinstance(x, list) for x in lists):
        return bad + ["missing_points, wrong_claims and citation_issues must be lists"]
    s, fm = g["score"], g.get("failure_mode")
    if s == 2 and (any(lists) or fm != "none"):
        bad.append("score 2 needs empty lists and failure_mode none")
    if s == 1 and not any(lists):
        bad.append("score 1 needs at least one missing point, wrong claim or citation issue")
    if s == 0 and not (lists[1] or fm in ZERO_OK):
        bad.append(f"score 0 needs a wrong claim or failure_mode in {sorted(ZERO_OK)}")
    return bad


def check(args):
    grades, packets = read_grades(args.grades), GRADING / "packets.jsonl"
    seen, errors = set(), 0
    for i, g in enumerate(grades, 1):
        k = (g.get("question_id"), g.get("label"))
        msgs = problems(g) + (["duplicate (question_id, label)"] if k in seen else [])
        seen.add(k)
        for m in msgs:
            print(f"line {i} {k}: {m}"); errors += 1
    if packets.exists():
        want = {(p["question_id"], c["label"]) for p in map(json.loads, open(packets)) for c in p["candidates"]}
        for k in sorted(want - seen): print("not graded:", k); errors += 1
        for k in sorted(seen - want): print("not in packets:", k); errors += 1
    print(f"{len(grades)} grades, {errors} problems")
    raise SystemExit(1 if errors else 0)


def bootstrap(diffs, n=2000):
    rng = random.Random(0)
    means = sorted(sum(rng.choices(diffs, k=len(diffs))) / len(diffs) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n)]


def summarize(args):
    meta = {q["question_id"]: q for q in load_sheet("Questions")}
    keyfile = json.loads((GRADING / "key.json").read_text())
    per_run = collections.defaultdict(dict)                      # run -> question_id -> grade
    for g in read_grades(args.grades):
        for run in keyfile["labels"][g["question_id"]][g["label"]]:
            per_run[run][g["question_id"]] = g
    pct = lambda gs: f"{100 * sum(g['score'] for g in gs) / (2 * len(gs)):.1f}% (n={len(gs)})" if gs else "-"
    groups = [("all", lambda q: True), ("text-involving", lambda q: q["data_source_type"] != "table-only")] + \
             [(f"source: {s}", lambda q, s=s: q["data_source_type"] == s) for s in ("text-only", "table-only", "text+table")] + \
             [(f"type: {t}", lambda q, t=t: q["question_type"] == t) for t in sorted({q["question_type"] for q in meta.values()})]
    for run, gr in per_run.items():
        rows = [(meta[i], g) for i, g in sorted(gr.items())]
        lines = [f"# Grades: {run}", "", "Score = points / (2 x questions); 0 wrong, 1 correct but incomplete, 2 correct and complete (evaluation/grading_rubric.md).", "",
                 "| Group | Score |", "|---|---|"]
        lines += [f"| {name} | {pct([g for q, g in rows if pick(q)])} |" for name, pick in groups]
        dist = collections.Counter(g["score"] for _, g in rows)
        fm = collections.Counter(g["failure_mode"] for _, g in rows if g["score"] < 2)
        lines += ["", f"Distribution: 2 x {dist[2]}, 1 x {dist[1]}, 0 x {dist[0]}.", "Failure modes (score below 2): " + (", ".join(f"{k} {v}" for k, v in fm.most_common()) or "none"),
                  "", "| ID | Source | Score | Failure mode | Missing / wrong / citation issues |", "|---|---|---|---|---|"]
        for q, g in rows:
            note = "; ".join(g["missing_points"] + g["wrong_claims"] + g["citation_issues"]).replace("|", "/")[:200]
            lines.append(f"| {q['question_id']} | {q['data_source_type']} | {g['score']} | {g['failure_mode']} | {note} |")
        (ROOT / run / "grades.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        with open(ROOT / run / "grades.jsonl", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(g, ensure_ascii=False) + "\n" for g in gr.values())
        print(f"{run}: {pct(list(gr.values()))}")
    if len(per_run) > 1:
        names = list(per_run)
        lines = ["# Comparison of runs", "", "| Group | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
        for name, pick in groups:
            lines.append(f"| {name} | " + " | ".join(pct([g for i, g in per_run[r].items() if pick(meta[i])]) for r in names) + " |")
        base = names[0]
        lines += ["", f"Paired against {base} (questions graded in both; mean score difference on the 0-2 scale, bootstrap 95% interval):", "",
                  "| Run | Questions | Mean difference | 95% interval | Better / same / worse |", "|---|---|---|---|---|"]
        for r in names[1:]:
            common = [i for i in per_run[r] if i in per_run[base]]
            d = [per_run[r][i]["score"] - per_run[base][i]["score"] for i in common]
            lo, hi = bootstrap(d) if d else (0, 0)
            lines.append(f"| {r} | {len(d)} | {sum(d) / max(len(d), 1):+.2f} | {lo:+.2f} to {hi:+.2f} | {sum(x > 0 for x in d)} / {sum(x == 0 for x in d)} / {sum(x < 0 for x in d)} |")
        ids = sorted({i for r in names for i in per_run[r]})
        lines += ["", "| ID | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
        lines += [f"| {i} | " + " | ".join(str(per_run[r][i]["score"]) if i in per_run[r] else "-" for r in names) + " |" for i in ids]
        (GRADING / "comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"comparison -> {GRADING / 'comparison.md'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("packet")
    p.add_argument("runs", nargs="+")
    p.add_argument("--ids", nargs="*")
    p.add_argument("--split", default="development", choices=["development", "held-out"])
    p.add_argument("--seed", default="0")
    p.add_argument("--with-text", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("grades")
    s = sub.add_parser("summarize")
    s.add_argument("grades")
    a = ap.parse_args()
    {"packet": packet, "check": check, "summarize": summarize}[a.cmd](a)
