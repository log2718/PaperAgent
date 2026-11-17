"""Embeddings + FAISS retrieval over a chunks.jsonl (token chunks by default; see ingest.py for the other modes).

    python src/retrieve.py build [mode] [dir]       # embed all chunks once, write index.faiss next to chunks.jsonl
    python src/retrieve.py "your question" [k] [mode]   # try a query

    from retrieve import search_papers, search_budget
    search_papers("What does BYOL use as its target?", k=5)                 # token chunks
    search_papers("...", k=3, mode="paper")                                 # whole papers
    search_budget("...", budget_tokens=3300, mode="paragraph")              # top paragraphs until the budget is reached
"""
import json
import sys
import time
from functools import lru_cache
from pathlib import Path

from sentence_transformers import SentenceTransformer
import faiss  # keep this import after torch/sentence_transformers: the reverse order segfaults on macOS

from ingest import EMBED_MODEL, data_dir


@lru_cache(maxsize=1)
def _model():
    model = SentenceTransformer(EMBED_MODEL, trust_remote_code=True)
    model.max_seq_length = 1024                      # chunks are at most ~700 tokens
    return model


@lru_cache(maxsize=None)
def _chunks(d):
    return [json.loads(line) for line in open(d / "chunks.jsonl", encoding="utf-8")]


def _embed(texts, prefix):
    # nomic-embed expects a task prefix on every input
    return _model().encode([prefix + t for t in texts], batch_size=8, normalize_embeddings=True,
                           show_progress_bar=len(texts) > 50).astype("float32")


def build_index(d):
    start = time.perf_counter()
    chunks = _chunks(d)
    vectors = _embed([c.get("embed_text", c["text"]) for c in chunks], "search_document: ")
    index = faiss.IndexFlatIP(vectors.shape[1])      # exact inner product = cosine (vectors are normalized)
    index.add(vectors)
    faiss.write_index(index, str(d / "index.faiss"))
    seconds = round(time.perf_counter() - start, 1)
    stats_file = d / "stats.json"
    stats = json.loads(stats_file.read_text()) if stats_file.exists() else {}
    stats.update(index_seconds=seconds, index_bytes=(d / "index.faiss").stat().st_size, embed_model=EMBED_MODEL)
    stats_file.write_text(json.dumps(stats, indent=1))
    print(f"indexed {index.ntotal} chunks, dim {vectors.shape[1]}, {seconds} s -> {d / 'index.faiss'}")


@lru_cache(maxsize=None)
def _index(d):
    return faiss.read_index(str(d / "index.faiss"))


def load_chunks(mode: str = "token"):
    return _chunks(data_dir(mode))


def as_hit(c, score=None):
    pages = str(c["page_start"]) if c["page_start"] == c["page_end"] else f"{c['page_start']}-{c['page_end']}"
    return {"score": None if score is None else round(float(score), 4), "chunk_id": c["chunk_id"], "paper": c["paper"],
            "pages": pages, "page_start": c["page_start"], "page_end": c["page_end"],
            "section": c["section"], "tokens": c.get("tokens"), "text": c["text"]}


@lru_cache(maxsize=256)
def _query_vector(query):
    return _embed([query], "search_query: ")        # one embedding per distinct query, shared by every search


def search_papers(query: str, k: int = 5, mode: str = "token"):
    """Return the k most similar chunks: score, chunk_id, paper, pages, section, tokens, text."""
    d = data_dir(mode)
    scores, ids = _index(d).search(_query_vector(query), k)
    return [as_hit(_chunks(d)[i], score) for score, i in zip(scores[0], ids[0])]


def search_budget(query: str, budget_tokens: int, mode: str = "paragraph", max_k: int = 30):
    """Take chunks in rank order until their tokens reach budget_tokens (at most max_k chunks)."""
    out, total = [], 0
    for h in search_papers(query, max_k, mode):
        out.append(h)
        total += h["tokens"]
        if total >= budget_tokens:
            break
    return out


if __name__ == "__main__":
    if sys.argv[1:2] == ["build"]:
        build_index(Path(sys.argv[3]) if len(sys.argv) > 3 else data_dir(sys.argv[2] if len(sys.argv) > 2 else "token"))
    else:
        mode = sys.argv[3] if len(sys.argv) > 3 else "token"
        for h in search_papers(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 5, mode):
            print(f"{h['score']:.3f}  {h['paper']} p.{h['pages']}  [{h['section']}]  {h['text'][:110]!r}")
