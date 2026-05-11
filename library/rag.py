"""Local RAG over ingested book chunks — 100% in-house.

Pipeline:
  1. `build`    → embed every chunk via nomic-embed-text (Ollama local)
                  store embeddings in SQLite BLOB column
  2. `query <text>`  → embed query, cosine-similar top-K, return chunks
  3. `ask <q>`  → query + Qwen generates answer citing chunks (still 0 Claude tokens)

Storage: library/chunks_index.db (SQLite) with:
  CREATE TABLE chunk_index (
    book_slug   TEXT,
    chunk_file  TEXT,
    text        TEXT,
    embedding   BLOB,         -- numpy float32 serialized
    n_tokens    INTEGER,
    PRIMARY KEY (book_slug, chunk_file)
  )

Nomic-embed-text: 768 dims, 8k context. Great for book chunks.

Uso:
    python -m library.rag build                                # embed all chunks
    python -m library.rag build --book dalio_*                 # subset
    python -m library.rag query "capital flow crisis pre-signals" --k 5
    python -m library.rag ask "como o Dalio detecta bubble?" --k 8
    python -m library.rag status                               # index coverage
"""
from __future__ import annotations

import argparse
import sqlite3
import struct
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_DIR = ROOT / "library" / "chunks"
INDEX_DB = ROOT / "library" / "chunks_index.db"

OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text:latest"
GEN_MODEL_14B = "qwen2.5:14b-instruct-q4_K_M"


SCHEMA = """
CREATE TABLE IF NOT EXISTS chunk_index (
    book_slug   TEXT NOT NULL,
    chunk_file  TEXT NOT NULL,
    text        TEXT NOT NULL,
    embedding   BLOB NOT NULL,
    n_tokens    INTEGER,
    PRIMARY KEY (book_slug, chunk_file)
);
CREATE INDEX IF NOT EXISTS idx_chunk_book ON chunk_index(book_slug);
"""


def ensure_schema() -> None:
    with sqlite3.connect(INDEX_DB) as c:
        c.executescript(SCHEMA)
        c.commit()


def embed(text: str) -> list[float] | None:
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text[:8000]},
            timeout=60,
        )
        r.raise_for_status()
        return r.json().get("embedding")
    except Exception as e:
        print(f"[embed error] {e}")
        return None


def _pack(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def _unpack(blob: bytes) -> list[float]:
    n = len(blob) // 4
    return list(struct.unpack(f"{n}f", blob))


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x*y for x, y in zip(a, b))


def _norm(a: list[float]) -> float:
    return sum(x*x for x in a) ** 0.5


def _cosine(a: list[float], b: list[float]) -> float:
    na, nb = _norm(a), _norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return _dot(a, b) / (na * nb)


def build_index(book_pattern: str = "*", force: bool = False) -> None:
    ensure_schema()
    books = [d for d in CHUNKS_DIR.iterdir() if d.is_dir() and d.match(book_pattern)]
    if not books:
        print(f"No books matching {book_pattern}")
        return

    total_embedded = 0
    total_skipped = 0
    t0 = time.time()

    for book_dir in books:
        book_slug = book_dir.name
        chunk_files = sorted(book_dir.glob("*.txt"))
        print(f"[build] {book_slug}  chunks={len(chunk_files)}")
        for i, cf in enumerate(chunk_files, 1):
            with sqlite3.connect(INDEX_DB) as c:
                exists = c.execute(
                    "SELECT 1 FROM chunk_index WHERE book_slug=? AND chunk_file=?",
                    (book_slug, cf.name),
                ).fetchone()
            if exists and not force:
                total_skipped += 1
                continue

            text = cf.read_text(encoding="utf-8", errors="ignore")
            if len(text.strip()) < 50:
                continue
            vec = embed(text)
            if vec is None:
                continue

            with sqlite3.connect(INDEX_DB) as c:
                c.execute(
                    "INSERT OR REPLACE INTO chunk_index "
                    "(book_slug, chunk_file, text, embedding, n_tokens) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (book_slug, cf.name, text, _pack(vec), len(text.split())),
                )
                c.commit()
            total_embedded += 1

            if i % 50 == 0:
                elapsed = time.time() - t0
                rate = total_embedded / max(elapsed, 0.1)
                print(f"  [{i:>4}/{len(chunk_files)}]  embedded_total={total_embedded}  rate={rate:.1f}/s")

    elapsed = time.time() - t0
    print(f"\n[build] done. embedded={total_embedded}  skipped_existing={total_skipped}  elapsed={elapsed:.1f}s")


def query_index(query_text: str, k: int = 5, book_filter: str | None = None) -> list[dict]:
    ensure_schema()
    qvec = embed(query_text)
    if qvec is None:
        return []

    with sqlite3.connect(INDEX_DB) as c:
        c.row_factory = sqlite3.Row
        if book_filter:
            rows = c.execute(
                "SELECT book_slug, chunk_file, text, embedding FROM chunk_index WHERE book_slug LIKE ?",
                (f"%{book_filter}%",),
            ).fetchall()
        else:
            rows = c.execute("SELECT book_slug, chunk_file, text, embedding FROM chunk_index").fetchall()

    scored = []
    for r in rows:
        sim = _cosine(qvec, _unpack(r["embedding"]))
        scored.append((sim, r))
    scored.sort(key=lambda x: -x[0])

    return [{
        "score": round(s, 4),
        "book": r["book_slug"],
        "chunk": r["chunk_file"],
        "text": r["text"],
    } for s, r in scored[:k]]


def ask(query: str, k: int = 6, book_filter: str | None = None) -> str:
    """Local LLM synthesis based on top-k retrieved chunks."""
    hits = query_index(query, k=k, book_filter=book_filter)
    if not hits:
        return "(no chunks matched — run `build` first)"

    context = "\n\n---\n\n".join(
        f"[Source: {h['book']} chunk {h['chunk']}  score={h['score']}]\n{h['text'][:1500]}"
        for h in hits
    )

    prompt = f"""You are a careful analyst. Answer the question using ONLY the sources below.
Cite each claim with [book:chunk]. If the sources don't answer, say so.

QUESTION: {query}

SOURCES:
{context}

ANSWER (structured, cite sources like [book:chunk], max 400 words):"""

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": GEN_MODEL_14B, "prompt": prompt, "stream": False,
                  "options": {"temperature": 0.3, "num_predict": 600}},
            timeout=300,
        )
        r.raise_for_status()
        return r.json().get("response", "(empty)")
    except Exception as e:
        return f"(generation failed: {e})"


def status() -> None:
    ensure_schema()
    with sqlite3.connect(INDEX_DB) as c:
        rows = c.execute("""
            SELECT book_slug, COUNT(*) as n
            FROM chunk_index GROUP BY book_slug
            ORDER BY book_slug
        """).fetchall()
    if not rows:
        print("Index empty. Run: python -m library.rag build")
        return
    total = 0
    print(f"{'Book':<52} {'Indexed':>10}")
    print("-" * 65)
    for book_slug, n in rows:
        print(f"{book_slug[:50]:<52} {n:>10}")
        total += n
    print("-" * 65)
    print(f"{'TOTAL':<52} {total:>10}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")

    p_build = sub.add_parser("build")
    p_build.add_argument("--book", default="*", help="Glob filter")
    p_build.add_argument("--force", action="store_true")

    p_query = sub.add_parser("query")
    p_query.add_argument("text")
    p_query.add_argument("--k", type=int, default=5)
    p_query.add_argument("--book", default=None)

    p_ask = sub.add_parser("ask")
    p_ask.add_argument("question")
    p_ask.add_argument("--k", type=int, default=6)
    p_ask.add_argument("--book", default=None)

    sub.add_parser("status")

    args = ap.parse_args()
    if args.cmd == "build":
        build_index(book_pattern=args.book, force=args.force)
    elif args.cmd == "query":
        sys.stdout.reconfigure(encoding="utf-8")
        for i, hit in enumerate(query_index(args.text, args.k, args.book), 1):
            print(f"\n[{i}] score={hit['score']}  {hit['book']}  {hit['chunk']}")
            print(hit["text"][:700])
            print("...")
    elif args.cmd == "ask":
        sys.stdout.reconfigure(encoding="utf-8")
        print(ask(args.question, args.k, args.book))
    elif args.cmd == "status":
        status()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
