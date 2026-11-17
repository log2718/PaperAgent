"""Question -> grounded answer. The path is chosen by the question's data_source_type:

    text-only   retrieve top-k chunks            -> LLM answers from them
    table-only  LLM writes SQL -> query_timm     -> LLM answers from the result
    text+table  retrieve + LLM writes SQL        -> LLM answers from both

The LLM only ever sees the evidence we pass it. Prompts are general (no per-question tuning).
`llm()` is the single place that talks to a model, so swapping providers is a one-function change.
"""
import collections
import json
import re
import subprocess
import tempfile
import time

from ingest import CONFIG_MODE, ROOT
from retrieve import as_hit, load_chunks, search_budget, search_papers
from sql_tool import as_text, query_timm

LLM_MODEL = "sonnet"                 # Claude Code CLI model alias
K = 5                                # passages retrieved per question
SQL_ATTEMPTS = 2                     # one retry if the query errors

# Retrieval configurations (what the model is shown); everything else is identical across them.
#   token              ~700-token chunks, top K                          (the baseline)
#   paragraph          paragraph chunks, top K
#   paragraph_matched  paragraph chunks in rank order until MATCHED_BUDGET_TOKENS (the baseline's mean retrieved size)
#   paper              the PAPERS_N most similar whole papers (title + abstract vector)
#   no_embedding       the model picks up to PAPERS_N whole papers from titles and abstracts; no vectors anywhere
CONFIGS = tuple(CONFIG_MODE)
FULL_PAPER = ("paper", "no_embedding")
MATCHED_BUDGET_TOKENS = 3460         # mean tokens the baseline retrieves at K=5 over the 28 text-involving development questions
PAPERS_N, PAPER_CAP_TOKENS = 3, 100_000
FULL_TEXT_NOTE = ("Each passage below is a whole paper. Page markers such as [page 5] sit inside the text; cite the page "
                  "where the evidence appears, as [paper name, p.N].\n\n")
ROUTER_SYSTEM = (
    "You decide which papers a question needs. Below is a list of papers, each as 'Name: title' followed by the start of its "
    "abstract. Reply with only a JSON list of one to three paper names, most relevant first, written exactly as in the list "
    "before the colon. Include every paper the question refers to, and no others."
)
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


_usage = collections.Counter()                                # summed over the LLM calls of one question


class LimitReached(RuntimeError):
    """The CLI reports a usage or rate limit (HTTP 429): nothing more can be run until it resets."""


def llm(prompt: str, system: str) -> str:
    """One call to the Claude Code CLI: no tools, no skills, no saved session, prompt on stdin.
    Token usage and the API-equivalent cost of the call are added to `_usage`."""
    run = subprocess.run(
        ["claude", "-p", "--model", LLM_MODEL, "--tools", "", "--system-prompt", system, "--no-session-persistence",
         "--disable-slash-commands", "--strict-mcp-config", "--setting-sources", "", "--output-format", "json"],
        input=prompt, capture_output=True, text=True, cwd=_workdir, timeout=600)
    try:
        out = json.loads(run.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"llm call failed: {run.stderr.strip()[:300] or run.stdout.strip()[:300]}")
    if run.returncode != 0 or out.get("is_error"):
        raise (LimitReached if out.get("api_error_status") == 429 else RuntimeError)(f"llm call failed: {str(out.get('result'))[:300]}")
    u = out["usage"]
    _usage.update(calls=1, input_tokens=u["input_tokens"], output_tokens=u["output_tokens"],
                  cache_creation_tokens=u["cache_creation_input_tokens"], cache_read_tokens=u["cache_read_input_tokens"],
                  cost_usd=out["total_cost_usd"])
    return out["result"].strip()


def format_passages(hits, full=False):
    body = "\n\n".join(f"[{i}] {h['paper']}, p.{h['pages']}, section: {h['section'] or 'n/a'}\n{h['text']}"
                       for i, h in enumerate(hits, 1))
    return (FULL_TEXT_NOTE if full else "") + body


_key = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def route_papers(question):
    """no_embedding: the model picks up to PAPERS_N papers from their titles and abstracts. Returns (hits, router log)."""
    papers = {_key(p["paper"]): p for p in load_chunks("paper")}
    listing = "\n\n".join(f"{p['paper']}: {p['title']}\n{' '.join(p['abstract'].split()[:150])}" for p in papers.values())
    prompt = f"Papers:\n\n{listing}\n\nQuestion: {question}"
    for _ in range(2):
        reply = llm(prompt, ROUTER_SYSTEM)
        m = re.search(r"\[.*?\]", reply, re.S)
        try:
            names = json.loads(m.group(0)) if m else []
        except json.JSONDecodeError:
            names = []
        names = [n.split(":")[0] for n in names if isinstance(n, str)]          # tolerate "Name: title" for "Name"
        chosen = list(dict.fromkeys(_key(n) for n in names if _key(n) in papers))[:PAPERS_N]
        if chosen:
            return [as_hit(papers[c]) for c in chosen], {"raw": reply, "papers": [papers[c]["paper"] for c in chosen]}
        prompt += "\n\nYour reply did not contain a JSON list of names from the list. Reply with only that list."
    raise ValueError(f"router returned no known paper: {reply[:200]}")


def cap_tokens(hits):
    """Keep whole papers in rank order; cut the last one(s) so the total stays within PAPER_CAP_TOKENS."""
    left, out = PAPER_CAP_TOKENS, []
    for h in hits:
        h = dict(h)
        if h["tokens"] > left:
            h["text"], h["truncated"], h["tokens"] = h["text"][:int(len(h["text"]) * left / h["tokens"])], True, left
        left -= h["tokens"]
        out.append(h)
        if left <= 0:
            break
    return out


def get_context(question, config):
    """Passages for a question under a retrieval configuration; returns (hits, extra fields for the log)."""
    if config == "token":
        return search_papers(question, K), {}
    if config == "paragraph":
        return search_papers(question, K, "paragraph"), {}
    if config == "paragraph_matched":
        return search_budget(question, MATCHED_BUDGET_TOKENS, "paragraph"), {}
    if config == "paper":
        return cap_tokens(search_papers(question, PAPERS_N, "paper")), {}
    hits, router = route_papers(question)
    return cap_tokens(hits), {"router": router}


def write_and_run_sql(question, hits=None, full=False):
    """Ask the LLM for a query, run it, retry once on error. Returns a list of attempts."""
    prompt = f"Question: {question}"
    if hits:
        prompt = f"Paper passages (they may contain numbers or definitions the query needs):\n\n{format_passages(hits, full)}\n\n" + prompt
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


def answer_question(q: dict, config: str = "token") -> dict:
    """q needs question_id, question, data_source_type. Returns a log record."""
    assert config in CONFIGS, config
    start = time.perf_counter()
    _usage.clear()
    kind, full = q["data_source_type"], config in FULL_PAPER
    hits, extra = get_context(q["question"], config) if kind in ("text-only", "text+table") else ([], {})
    attempts = write_and_run_sql(q["question"], hits, full) if kind in ("table-only", "text+table") else []

    keys = ("chunk_id", "paper", "pages", "section", "score") + (() if config == "token" else ("tokens",))
    retrieved = [{**{k: h[k] for k in keys}, **({"chars": len(h["text"]), "truncated": h.get("truncated", False)} if full
                                                else {"text": h["text"]})} for h in hits]
    parts = []
    if hits:
        parts.append("Paper passages:\n\n" + format_passages(hits, full))
    if attempts:
        last = attempts[-1]
        parts.append(f"SQL query run on the timm database:\n{last['sql']}\n\n" +
                     (f"Result:\n{as_text(last['result'])}" if "result" in last else f"The query failed: {last['error']}"))
    prompt = "\n\n".join(parts) + f"\n\nQuestion: {q['question']}"
    answer = llm(prompt, ANSWER_SYSTEM)                        # before the usage is read below

    return {
        "question_id": q["question_id"], "question": q["question"], "source_type": kind, "config": config,
        "retrieved": retrieved, **extra,
        "sql_attempts": attempts,
        "answer": answer,
        "model": LLM_MODEL, "latency_s": round(time.perf_counter() - start, 1),
        "usage": {k: round(v, 5) for k, v in _usage.items()},
    }
