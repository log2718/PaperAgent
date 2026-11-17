"""PDFs -> chunks.jsonl, in one of three chunkings (the retrieval unit differs, everything else is the same).

    python src/ingest.py                      # --mode token (default): ~700-token windows, ~100 overlap -> data/chunks.jsonl
    python src/ingest.py --mode paragraph     # PDF text blocks (paragraphs)                              -> data/paragraph/
    python src/ingest.py --mode paper         # one unit per paper: full text with [page N] markers       -> data/paper/
    python src/ingest.py --mode token --out /tmp/x    # write somewhere else (timing or checks)

One JSON object per chunk: chunk_id, paper_id, paper, title, page_start, page_end, section, text (paragraph and paper modes add
tokens; paper mode adds abstract and embed_text). Tokens are counted with the embedding model's tokenizer.
Section = the last heading-like line seen before the chunk starts (a simple regex, so it is approximate).
A stats.json next to the chunks records counts, token-length percentiles and the build time.
"""
import argparse
import bisect
import json
import re
import statistics
import time
from pathlib import Path

import openpyxl
import pymupdf
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = Path.home() / "Desktop" / "ML" / "Papers"          # source PDFs stay outside the repo
PAPERS_XLSX = ROOT / "evaluation" / "text_evaluation_candidates.xlsx"

EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"               # also used in retrieve.py
CHUNK_TOKENS, OVERLAP_TOKENS = 700, 100                      # token mode
MIN_WORDS, MAX_TOKENS = 40, 350                              # paragraph mode: merge blocks below MIN_WORDS, split above MAX_TOKENS
ABSTRACT_WORDS = 300                                         # paper mode: abstract words embedded with the title


def data_dir(mode="token"):
    return ROOT / "data" if mode == "token" else ROOT / "data" / mode



# "3.1 Training and Inference", "A. Object Detection", "Abstract", "References", "Appendix ..."
HEADING = re.compile(
    r"^(?:(?:[1-9]|1\d|20|[A-Z])(?:\.[1-9]\d?)*\.?\s+[A-Z][A-Za-z0-9 ,:;&'()\-–/]{2,80}"
    r"|Abstract|ABSTRACT|References|REFERENCES|Appendix(?: [A-Z])?[A-Za-z ]{0,40}|APPENDIX)$"
)


NUMBER = re.compile(r"^(?:[1-9]|1\d|20|[A-Z])(?:\.[1-9]\d?)*\.?$")                    # a section number alone on its line
SMALLCAPS = re.compile(r"\b([A-Z]) (?=[A-Z]{2,})")                      # "M ETHOD" -> "METHOD"
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[])")


def read_papers():
    rows = list(openpyxl.load_workbook(PAPERS_XLSX, read_only=True)["Papers"].iter_rows(values_only=True))
    keys = rows[0]
    return [dict(zip(keys, r)) for r in rows[1:]]


def headings_in(lines):
    """[(line index, heading)] for heading-like lines (a lone section number is joined with the title below it)."""
    found = []
    for i, line in enumerate(lines):
        s = line.strip()
        if NUMBER.match(s) and i + 1 < len(lines):               # number alone, title on the next line
            title = lines[i + 1].strip()
            if len(title.split()) >= 2 and title[0].isupper() and not title.endswith("."):
                s = f"{s} {title}"
        s = SMALLCAPS.sub(r"\1", s)
        if len(s) < 90 and HEADING.match(s):
            found.append((i, s))
    return found


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
        headings += [(pos[i], s) for i, s in headings_in(lines)]
    return text, page_starts, headings


def n_tokens(tok, text):
    return len(tok(text, add_special_tokens=False)["input_ids"])


def chunk_paper(paper, tok):
    """Token mode: sliding windows over the whole text."""
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


def split_long(text, tok):
    """Pack sentences into pieces of at most MAX_TOKENS; one sentence that is longer (a flattened table) is cut by words."""
    pieces, cur, cur_n = [], [], 0
    for s in SENTENCE.split(text):
        n = n_tokens(tok, s)
        if n > MAX_TOKENS:
            if cur:
                pieces.append(" ".join(cur)); cur, cur_n = [], 0
            words, step = s.split(), max(1, len(s.split()) * MAX_TOKENS // n)
            pieces += [" ".join(words[i:i + step]) for i in range(0, len(words), step)]
        elif cur_n + n > MAX_TOKENS:
            pieces.append(" ".join(cur)); cur, cur_n = [s], n
        else:
            cur.append(s); cur_n += n
    return pieces + ([" ".join(cur)] if cur else [])


def chunk_paragraphs(paper, tok):
    """Paragraph mode: PyMuPDF text blocks per page. Blocks under MIN_WORDS (headings, captions, page numbers) join the block
    below them; a short tail at the end of a page joins the paragraph above; paragraphs over MAX_TOKENS are split."""
    chunks, section = [], ""
    for page_no, page in enumerate(pymupdf.open(PDF_DIR / paper["pdf_filename"]), start=1):
        paras, buf, buf_section = [], "", ""
        for b in page.get_text("blocks"):
            if b[6] != 0:                                        # skip image blocks
                continue
            lines = b[4].splitlines()
            heads = headings_in(lines)
            if heads:
                section = heads[-1][1]
            text = re.sub(r"\s*\n\s*", " ", re.sub(r"-\n(?=[a-z])", "", b[4])).strip()
            if not text:
                continue
            buf_section = buf_section or section
            buf = f"{buf} {text}".strip()
            if len(buf.split()) >= MIN_WORDS:
                paras.append((buf, buf_section)); buf, buf_section = "", ""
        if buf and paras:
            paras[-1] = (f"{paras[-1][0]} {buf}", paras[-1][1])
        elif buf:
            paras.append((buf, buf_section))
        for text, sec in paras:
            for piece in (split_long(text, tok) if n_tokens(tok, text) > MAX_TOKENS else [text]):
                chunks.append({"chunk_id": f"{paper['paper_id']}-p{len(chunks):03d}", "paper_id": paper["paper_id"],
                               "paper": paper["short_name"], "title": paper["full_title"], "page_start": page_no,
                               "page_end": page_no, "section": sec, "text": piece, "tokens": n_tokens(tok, piece)})
    return chunks


def whole_paper(paper, tok):
    """Paper mode: one unit per paper. The text carries [page N] markers so answers can still cite pages. The vector is
    made from the title and the first ABSTRACT_WORDS words of the abstract (the embedding window is far shorter than a paper)."""
    pages = [p.get_text() for p in pymupdf.open(PDF_DIR / paper["pdf_filename"])]
    text = "\n".join(f"[page {i}]\n{t}" for i, t in enumerate(pages, start=1))
    m = re.search(r"\babstract\b", pages[0], re.I)
    abstract = " ".join((pages[0][m.end():] if m else pages[0]).split()[:ABSTRACT_WORDS])
    return [{"chunk_id": f"{paper['paper_id']}-full", "paper_id": paper["paper_id"], "paper": paper["short_name"],
             "title": paper["full_title"], "page_start": 1, "page_end": len(pages), "section": "", "text": text,
             "tokens": n_tokens(tok, text), "abstract": abstract, "embed_text": f"{paper['full_title']}\n{abstract}"}]


MODES = {"token": chunk_paper, "paragraph": chunk_paragraphs, "paper": whole_paper}
# retrieval configuration (src/answer.py) -> chunk mode, which decides the data directory
CONFIG_MODE = {"token": "token", "paragraph": "paragraph", "paragraph_matched": "paragraph", "paper": "paper", "no_embedding": "paper"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=list(MODES), default="token")
    ap.add_argument("--out", help="directory to write into (default: data/ or data/<mode>/)")
    args = ap.parse_args()
    out = Path(args.out) if args.out else data_dir(args.mode)
    tok = AutoTokenizer.from_pretrained(EMBED_MODEL, trust_remote_code=True)
    tok.model_max_length = 10**9                                  # we window manually
    out.mkdir(parents=True, exist_ok=True)
    start, per_paper, lengths = time.perf_counter(), {}, []
    with open(out / "chunks.jsonl", "w", encoding="utf-8") as f:
        for paper in read_papers():
            chunks = MODES[args.mode](paper, tok)
            f.writelines(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks)
            per_paper[paper["short_name"]] = len(chunks)
            lengths += [c.get("tokens") or n_tokens(tok, c["text"]) for c in chunks]
            print(f"{paper['paper_id']} {paper['short_name']:<22} {len(chunks):>3} chunks")
    q = statistics.quantiles(lengths, n=10) if len(lengths) > 1 else lengths * 9
    stats = {"mode": args.mode, "n_chunks": len(lengths), "per_paper": per_paper, "ingest_seconds": round(time.perf_counter() - start, 1),
             "tokens": {"min": min(lengths), "p10": round(q[0]), "median": round(statistics.median(lengths)), "mean": round(statistics.mean(lengths)),
                        "p90": round(q[8]), "max": max(lengths)}}
    (out / "stats.json").write_text(json.dumps(stats, indent=1))
    print(f"{len(lengths)} chunks -> {out / 'chunks.jsonl'}; tokens per chunk {stats['tokens']}; {stats['ingest_seconds']} s")


if __name__ == "__main__":
    main()
