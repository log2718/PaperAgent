"""Run the answer pipeline on a set of questions, log every run to JSONL, and write a report.

    python src/evaluate.py run --ids Q01 Q11 Q21 Q31 Q18 --out runs/sample      # small sample
    python src/evaluate.py run --split development --out runs/baseline          # full development set
    python src/evaluate.py report runs/baseline                                 # (re)write report.md

Held-out questions are refused unless --split held-out is given explicitly (not used until the final test).
Re-running a `run` resumes: questions already in results.jsonl are skipped.

The report has no overall accuracy: it lists reference and system answers side by side for manual grading,
plus three cheap diagnostics (retrieval page hit, SQL value overlap, abstention wording).
"""
import argparse
import collections
import json
import re
import sys
import traceback

import openpyxl

from ingest import PAPERS_XLSX, ROOT
from sql_tool import query_timm

ABSTAIN = re.compile(r"(does not|do not|doesn't|don't|did not|not) (establish|show|report|state|provide|specify|support)|"
                     r"no (evidence|result|data)|cannot be (determined|answered)|not (established|reported|shown)", re.I)


def load_sheet(name):
    rows = list(openpyxl.load_workbook(PAPERS_XLSX, read_only=True)[name].iter_rows(values_only=True))
    return [dict(zip(rows[0], r)) for r in rows[1:]]


def run(args):
    from answer import answer_question                       # imported late: loads the embedding model
    questions = load_sheet("Questions")
    if args.ids:
        chosen = [q for q in questions if q["question_id"] in args.ids]
    else:
        chosen = [q for q in questions if q["split"] == args.split]
    if args.split != "held-out" and any(q["split"] == "held-out" for q in chosen):
        sys.exit("refusing to run held-out questions (use --split held-out deliberately)")
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    path = out / "results.jsonl"
    done = {json.loads(l)["question_id"] for l in open(path)} if path.exists() else set()
    for q in chosen:
        if q["question_id"] in done:
            continue
        try:
            rec = answer_question(q)
        except Exception as e:                               # keep going; the failure is logged
            rec = {"question_id": q["question_id"], "question": q["question"], "source_type": q["data_source_type"],
                   "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-600:]}
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"{rec['question_id']} {rec['source_type']:<10} {rec.get('latency_s', '-')}s {'ERROR' if 'error' in rec else 'ok'}", flush=True)
    report(args.out)


def gold_pages():
    gold = collections.defaultdict(set)
    for r in load_sheet("Evidence"):
        gold[r["question_id"]].add((r["paper_short_name"], r["page"]))
    return gold


def retrieval_hit(rec, gold):
    """Fraction of gold (paper, page) pairs that lie inside a retrieved chunk's page span."""
    if not rec.get("retrieved") or not gold:
        return None
    covered = set()
    for h in rec["retrieved"]:
        first, _, last = h["pages"].partition("-")
        covered |= {(h["paper"], p) for p in range(int(first), int(last or first) + 1)}
    return len(gold & covered) / len(gold)


def sql_overlap(rec, gold_sql):
    """Fraction of cells of the workbook's reference SQL result that also appear in the system's result."""
    att = rec.get("sql_attempts") or []
    if not att or "result" not in att[-1] or not gold_sql:
        return None
    cells = lambda res: {str(round(v, 3)) if isinstance(v, float) else str(v) for row in res["rows"] for v in row}
    ref = cells(query_timm(gold_sql[0]))
    return len(ref & cells(att[-1]["result"])) / len(ref) if ref else None


def report(out_dir):
    out = ROOT / out_dir
    recs = [json.loads(l) for l in open(out / "results.jsonl", encoding="utf-8")]
    meta = {q["question_id"]: q for q in load_sheet("Questions")}
    gold = gold_pages()
    gold_sql = collections.defaultdict(list)
    for r in load_sheet("TabularEvidence"):
        gold_sql[r["question_id"]].append(r["SQL"])

    rows, lines = [], []
    for r in recs:
        m = meta[r["question_id"]]
        if "error" in r:
            rows.append((r, m, None, None, None)); continue
        hit = retrieval_hit(r, gold[r["question_id"]])
        ov = sql_overlap(r, gold_sql[r["question_id"]])
        abst = bool(ABSTAIN.search(r["answer"]))
        rows.append((r, m, hit, ov, abst))

    mean = lambda xs: f"{sum(xs) / len(xs):.2f} (n={len(xs)})" if xs else "-"
    times = [r["latency_s"] for r in recs if "latency_s" in r]
    lines += [f"# Report: {out_dir}", "", f"{len(recs)} questions, {sum('error' in r for r in recs)} errors, "
              f"mean latency {sum(times) / max(len(times), 1):.1f} s.", "",
              "| Source type | Retrieval page hit | SQL value overlap | Answers with abstention wording |", "|---|---|---|---|"]
    for kind in ("text-only", "table-only", "text+table"):
        sub = [x for x in rows if x[0]["source_type"] == kind and "error" not in x[0]]
        hits = [x[2] for x in sub if x[2] is not None]
        ovs = [x[3] for x in sub if x[3] is not None]
        ab = sum(1 for x in sub if x[4])
        lines.append(f"| {kind} | {mean(hits)} | {mean(ovs)} | {ab} of {len(sub)} |")
    no = [x for x in rows if x[1]["answerable"] == "no" and x[4] is not None]
    lines += ["", f"Insufficient-evidence questions ({', '.join(x[0]['question_id'] for x in no) or 'none'}): "
              f"{sum(1 for x in no if x[4])} of {len(no)} answers use abstention wording (keyword heuristic, check by reading).",
              "", "Diagnostics are heuristics, not grades. *Retrieval page hit*: share of the workbook's gold evidence pages "
              "covered by retrieved chunks. *SQL value overlap*: share of cells of the workbook's reference SQL result that "
              "also appear in the system's result. Grade answers by reading them against the reference.", ""]
    for r, m, hit, ov, abst in rows:
        lines += [f"## {r['question_id']} ({r['source_type']}, {m['question_type']}, {m['difficulty']}, answerable: {m['answerable']})", "",
                  f"**Question.** {r['question']}", "", f"**Reference answer.** {m['reference_answer']}", ""]
        if "error" in r:
            lines += [f"**ERROR.** {r['error']}", ""]; continue
        lines += [f"**System answer.** {r['answer']}", ""]
        if r["retrieved"]:
            lines.append("**Retrieved:** " + "; ".join(f"{h['paper']} p.{h['pages']} ({h['score']:.2f})" for h in r["retrieved"])
                         + f" | gold page hit: {hit:.2f}")
        if r["sql_attempts"]:
            lines.append("**SQL:** `" + r["sql_attempts"][-1]["sql"].replace("\n", " ") + "`" +
                         (f" | overlap with reference result: {ov:.2f}" if ov is not None else " | failed"))
        lines.append(f"*{r['latency_s']} s*"); lines.append("")
    (out / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"report -> {out / 'report.md'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--ids", nargs="*")
    r.add_argument("--split", default="development", choices=["development", "held-out"])
    r.add_argument("--out", required=True)
    p = sub.add_parser("report")
    p.add_argument("out")
    a = ap.parse_args()
    run(a) if a.cmd == "run" else report(a.out)
