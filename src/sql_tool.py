"""Read-only SQL access to the cleaned timm results (tabular_data/timm_results.sqlite).

    from sql_tool import query_timm
    query_timm("SELECT model, top1_val FROM model_results ORDER BY top1_val DESC LIMIT 3")

Only a single SELECT (or WITH ... SELECT) is allowed. The database is opened read-only, and a
SQLite authorizer rejects everything except reading (no PRAGMA, ATTACH, writes), so the check
does not rely on string matching alone.

    python src/sql_tool.py     # self-check: re-run the 21 SQL statements stored in the workbook
"""
import re
import sqlite3
import time

import openpyxl

from ingest import PAPERS_XLSX, ROOT

DB = ROOT / "tabular_data" / "timm_results.sqlite"
MAX_ROWS, TIMEOUT_S = 200, 20
_READ_ONLY_ACTIONS = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_RECURSIVE}


def query_timm(sql: str, max_rows: int = MAX_ROWS):
    """Run one read-only SELECT. Returns {"columns", "rows", "truncated"}; raises ValueError if refused or failing."""
    sql = sql.strip().rstrip(";").strip()
    if not re.match(r"(?is)(select|with)\b", sql) or ";" in sql:
        raise ValueError("only a single SELECT query is allowed")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.set_authorizer(lambda action, *_: sqlite3.SQLITE_OK if action in _READ_ONLY_ACTIONS else sqlite3.SQLITE_DENY)
    start = time.time()
    con.set_progress_handler(lambda: time.time() - start > TIMEOUT_S, 100_000)   # abort runaway queries
    try:
        cur = con.execute(sql)
        rows = cur.fetchmany(max_rows + 1)
        return {"columns": [d[0] for d in cur.description], "rows": [list(r) for r in rows[:max_rows]],
                "truncated": len(rows) > max_rows}
    except sqlite3.Error as e:
        raise ValueError(str(e))
    finally:
        con.close()


def as_text(result):
    """Compact text form of a result, as stored in the workbook: 'N row(s) col | col  val | val ...'."""
    lines = [" | ".join(result["columns"])] + [" | ".join(str(v) for v in r) for r in result["rows"]]
    return f"{len(result['rows'])} row(s) " + " ".join(lines) + (" (truncated)" if result["truncated"] else "")


def self_check():
    ws = openpyxl.load_workbook(PAPERS_XLSX, read_only=True)["TabularEvidence"]
    ok = 0
    rows = list(ws.iter_rows(values_only=True))[1:]
    for qid, _, sql, _, stored, _ in rows:
        got = " ".join(as_text(query_timm(sql)).split())
        same = got == " ".join(stored.split())
        ok += same
        print(f"{qid} {'ok' if same else 'DIFFERS'}")
    print(f"{ok}/{len(rows)} statements reproduce the stored workbook result")
    for bad in ("DROP TABLE model_results", "SELECT 1; DELETE FROM model_results", "PRAGMA table_info(model_results)",
                "ATTACH DATABASE 'x.db' AS x", "WITH t AS (SELECT 1) DELETE FROM model_results"):
        try:
            query_timm(bad)
            print("NOT REFUSED:", bad)
        except ValueError as e:
            print(f"refused: {bad[:45]!r}")


if __name__ == "__main__":
    self_check()
