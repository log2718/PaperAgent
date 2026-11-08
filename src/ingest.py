"""PDFs -> data/chunks.jsonl

One JSON object per chunk: chunk_id, paper_id, paper, title, page_start, page_end, section, text.
Chunks are ~700 tokens with ~100 tokens of overlap, counted with the embedding model's tokenizer.
Section = the last heading-like line seen before the chunk starts (a simple regex, so it is approximate).

Run:  python src/ingest.py
"""
import bisect
import json
import re
from pathlib import Path

import openpyxl
import pymupdf
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = Path.home() / "Desktop" / "ML" / "Papers"          # source PDFs stay outside the repo
PAPERS_XLSX = ROOT / "evaluation" / "text_evaluation_candidates.xlsx"
CHUNKS = ROOT / "data" / "chunks.jsonl"

EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"               # also used in retrieve.py
CHUNK_TOKENS, OVERLAP_TOKENS = 700, 100

# "3.1 Training and Inference", "A. Object Detection", "Abstract", "References", "Appendix ..."
HEADING = re.compile(
    r"^(?:(?:[1-9]|1\d|20|[A-Z])(?:\.[1-9]\d?)*\.?\s+[A-Z][A-Za-z0-9 ,:;&'()\-–/]{2,80}"
    r"|Abstract|ABSTRACT|References|REFERENCES|Appendix(?: [A-Z])?[A-Za-z ]{0,40}|APPENDIX)$"
)


NUMBER = re.compile(r"^(?:[1-9]|1\d|20|[A-Z])(?:\.[1-9]\d?)*\.?$")                    # a section number alone on its line
SMALLCAPS = re.compile(r"\b([A-Z]) (?=[A-Z]{2,})")                      # "M ETHOD" -> "METHOD"


def read_papers():
    rows = list(openpyxl.load_workbook(PAPERS_XLSX, read_only=True)["Papers"].iter_rows(values_only=True))
    keys = rows[0]
    return [dict(zip(keys, r)) for r in rows[1:]]


def pdf_text(path):
    """Return the full text, the char offset where each page starts, and (offset, heading) pairs."""
    text, page_starts, headings = "", [], []
    for page in pymupdf.open(path):
        page_starts.append(len(text))
        lines, pos = page.get_text().splitlines(keepends=True), []
        for line in lines:
            pos.append(len(text))
            text += line
        text += "\n"
        for i, line in enumerate(lines):
            s = line.strip()
            if NUMBER.match(s) and i + 1 < len(lines):               # number alone, title on the next line
                title = lines[i + 1].strip()
                if len(title.split()) >= 2 and title[0].isupper() and not title.endswith("."):
                    s = f"{s} {title}"
            s = SMALLCAPS.sub(r"\1", s)
            if len(s) < 90 and HEADING.match(s):
                headings.append((pos[i], s))
    return text, page_starts, headings


def chunk_paper(paper, tok):
    text, page_starts, headings = pdf_text(PDF_DIR / paper["pdf_filename"])
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    offsets = enc["offset_mapping"]
    n, step = len(offsets), CHUNK_TOKENS - OVERLAP_TOKENS
    head_pos = [p for p, _ in headings]
    chunks = []
    for i, s in enumerate(range(0, n, step)):
        e = min(s + CHUNK_TOKENS, n)
        a, b = offsets[s][0], offsets[e - 1][1]
        h = bisect.bisect_right(head_pos, a) - 1
        chunks.append({
            "chunk_id": f"{paper['paper_id']}-c{i:03d}",
            "paper_id": paper["paper_id"],
            "paper": paper["short_name"],
            "title": paper["full_title"],
            "page_start": bisect.bisect_right(page_starts, a),      # 1-based PDF page
            "page_end": bisect.bisect_right(page_starts, b - 1),
            "section": headings[h][1] if h >= 0 else "",
            "text": text[a:b].strip(),
        })
        if e == n:
            break
    return chunks


def main():
    tok = AutoTokenizer.from_pretrained(EMBED_MODEL, trust_remote_code=True)
    tok.model_max_length = 10**9                                  # we window manually
    CHUNKS.parent.mkdir(exist_ok=True)
    total = 0
    with open(CHUNKS, "w", encoding="utf-8") as f:
        for paper in read_papers():
            chunks = chunk_paper(paper, tok)
            f.writelines(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks)
            total += len(chunks)
            print(f"{paper['paper_id']} {paper['short_name']:<22} {len(chunks):>3} chunks")
    print(f"{total} chunks -> {CHUNKS}")


if __name__ == "__main__":
    main()
