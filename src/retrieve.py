"""Embeddings + FAISS retrieval over data/chunks.jsonl.

    python src/retrieve.py build                 # embed all chunks once, write data/index.faiss
    python src/retrieve.py "your question" [k]   # try a query

    from retrieve import search_papers
    search_papers("What does BYOL use as its target?", k=5)
"""
import json
import sys
from functools import lru_cache
from pathlib import Path

from sentence_transformers import SentenceTransformer
import faiss  # keep this import after torch/sentence_transformers: the reverse order segfaults on macOS

from ingest import CHUNKS, EMBED_MODEL, ROOT

INDEX = ROOT / "data" / "index.faiss"


@lru_cache(maxsize=1)
def _model():
    model = SentenceTransformer(EMBED_MODEL, trust_remote_code=True)
    model.max_seq_length = 1024                      # chunks are ~700 tokens
    return model


@lru_cache(maxsize=1)
def _chunks():
    return [json.loads(line) for line in open(CHUNKS, encoding="utf-8")]


def _embed(texts, prefix):
    # nomic-embed expects a task prefix on every input
    return _model().encode([prefix + t for t in texts], batch_size=8, normalize_embeddings=True,
                           show_progress_bar=len(texts) > 50).astype("float32")


def build_index():
    vectors = _embed([c["text"] for c in _chunks()], "search_document: ")
    index = faiss.IndexFlatIP(vectors.shape[1])      # exact inner product = cosine (vectors are normalized)
    index.add(vectors)
    faiss.write_index(index, str(INDEX))
    print(f"indexed {index.ntotal} chunks, dim {vectors.shape[1]} -> {INDEX}")


@lru_cache(maxsize=1)
def _index():
    return faiss.read_index(str(INDEX))


def search_papers(query: str, k: int = 5):
    """Return the k most similar chunks: score, chunk_id, paper, pages, section, text."""
    scores, ids = _index().search(_embed([query], "search_query: "), k)
    hits = []
    for score, i in zip(scores[0], ids[0]):
        c = _chunks()[i]
        pages = str(c["page_start"]) if c["page_start"] == c["page_end"] else f"{c['page_start']}-{c['page_end']}"
        hits.append({"score": round(float(score), 4), "chunk_id": c["chunk_id"], "paper": c["paper"],
                     "pages": pages, "page_start": c["page_start"], "page_end": c["page_end"],
                     "section": c["section"], "text": c["text"]})
    return hits


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        build_index()
    else:
        for h in search_papers(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 5):
            print(f"{h['score']:.3f}  {h['paper']} p.{h['pages']}  [{h['section']}]  {h['text'][:110]!r}")
