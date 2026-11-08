"""Question -> grounded answer. The path is chosen by the question's data_source_type:

    text-only   retrieve top-k chunks            -> LLM answers from them
    table-only  LLM writes SQL -> query_timm     -> LLM answers from the result
    text+table  retrieve + LLM writes SQL        -> LLM answers from both

The LLM only ever sees the evidence we pass it. Prompts are general (no per-question tuning).
`llm()` is the single place that talks to a model, so swapping providers is a one-function change.
"""
import re
import subprocess
import tempfile
import time

from ingest import ROOT
from retrieve import search_papers
from sql_tool import as_text, query_timm

LLM_MODEL = "sonnet"                 # Claude Code CLI model alias
K = 5                                # passages retrieved per question
SQL_ATTEMPTS = 2                     # one retry if the query errors
SCHEMA = (ROOT / "tabular_data" / "data_dictionary.md").read_text(encoding="utf-8")

ANSWER_SYSTEM = (
    "You answer questions about machine-learning research papers using only the evidence given in the user "
    "message: numbered paper passages and/or the result of a database query. Cite each claim from a passage as "
    "[paper name, p.N] using the name and pages in the passage header, e.g. [BYOL, p.4]. "
    "Show calculations explicitly. If the evidence does not establish the answer, say so explicitly and say "
    "what it does show. Do not use outside knowledge."
)
SQL_SYSTEM = (
    "You write one SQLite SELECT query that answers the question from the timm results database described "
    "below. Reply with only the query in a ```sql block. Use only documented tables and columns.\n\n" + SCHEMA
)

_workdir = tempfile.mkdtemp(prefix="paperagent_llm_")      # empty cwd so the CLI sees no project files


def llm(prompt: str, system: str) -> str:
    """One call to the Claude Code CLI: no tools, no skills, no saved session, prompt on stdin."""
    run = subprocess.run(
        ["claude", "-p", "--model", LLM_MODEL, "--tools", "", "--system-prompt", system, "--no-session-persistence",
         "--disable-slash-commands", "--strict-mcp-config", "--setting-sources", ""],
        input=prompt, capture_output=True, text=True, cwd=_workdir, timeout=600)
    if run.returncode != 0:
        raise RuntimeError(f"llm call failed: {run.stderr.strip()[:300]}")
    return run.stdout.strip()


def format_passages(hits):
    return "\n\n".join(f"[{i}] {h['paper']}, p.{h['pages']}, section: {h['section'] or 'n/a'}\n{h['text']}"
                       for i, h in enumerate(hits, 1))


def write_and_run_sql(question, hits=None):
    """Ask the LLM for a query, run it, retry once on error. Returns a list of attempts."""
    prompt = f"Question: {question}"
    if hits:
        prompt = f"Paper passages (they may contain numbers or definitions the query needs):\n\n{format_passages(hits)}\n\n" + prompt
    attempts = []
    for _ in range(SQL_ATTEMPTS):
        reply = llm(prompt, SQL_SYSTEM)
        m = re.search(r"```(?:sql)?\s*(.*?)```", reply, re.S)
        sql = (m.group(1) if m else reply).strip()
        try:
            attempts.append({"sql": sql, "result": query_timm(sql)})
            break
        except ValueError as e:
            attempts.append({"sql": sql, "error": str(e)})
            prompt += f"\n\nYour previous query:\n{sql}\nfailed with: {e}\nReturn a corrected query."
    return attempts


def answer_question(q: dict) -> dict:
    """q needs question_id, question, data_source_type. Returns a log record."""
    start = time.perf_counter()
    kind = q["data_source_type"]
    hits = search_papers(q["question"], K) if kind in ("text-only", "text+table") else []
    attempts = write_and_run_sql(q["question"], hits) if kind in ("table-only", "text+table") else []

    parts = []
    if hits:
        parts.append("Paper passages:\n\n" + format_passages(hits))
    if attempts:
        last = attempts[-1]
        parts.append(f"SQL query run on the timm database:\n{last['sql']}\n\n" +
                     (f"Result:\n{as_text(last['result'])}" if "result" in last else f"The query failed: {last['error']}"))
    prompt = "\n\n".join(parts) + f"\n\nQuestion: {q['question']}"

    return {
        "question_id": q["question_id"], "question": q["question"], "source_type": kind,
        "retrieved": [{k: h[k] for k in ("chunk_id", "paper", "pages", "section", "score", "text")} for h in hits],
        "sql_attempts": attempts,
        "answer": llm(prompt, ANSWER_SYSTEM),
        "model": LLM_MODEL, "latency_s": round(time.perf_counter() - start, 1),
    }
