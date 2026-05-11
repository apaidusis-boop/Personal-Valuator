"""Book ingest — lê PDFs/EPUBs/MDs de library/books/, chunka, guarda em library/chunks/.

Suporte:
  .pdf   via pypdf (reutiliza pattern de fetchers/subscriptions/_pdf_extract.py)
  .epub  via ebooklib (se instalado) — fallback: tratar como HTML/ZIP
  .md    directo
  .txt   directo

Chunks: ~2000 chars com overlap 200 chars. Respeita boundaries de parágrafo
quando possível.

Output por book: library/chunks/<book_slug>/<NNNN>.txt + <book_slug>/meta.json

Idempotent: re-running pulla diffs apenas.

Uso:
    python library/ingest.py                      # processa books novos
    python library/ingest.py --book "Dalio_*"     # subset
    python library/ingest.py --force              # re-ingest tudo
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from . import BOOKS_DIR, CHUNKS_DIR
from ._common import chunk_text as _chunk, file_hash as _file_hash, slugify

CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200


def _slugify(s: str) -> str:
    return slugify(s, maxlen=50)


def _extract_pdf(path: Path, engine: str = "pypdf") -> str:
    """Extract PDF book content. engine in {pypdf, markitdown, auto}.

    pypdf = legacy fast path. markitdown = structured Markdown (preserves
    tables/headers, much better for RAG ingestion of investment books).
    auto = markitdown first, pypdf fallback.
    """
    if engine in ("markitdown", "auto"):
        try:
            from library._md_extract import extract_text as _md_extract
            text = _md_extract(path, engine=engine)
            if text:
                return text
        except Exception:
            pass
    try:
        from pypdf import PdfReader
    except ImportError:
        print("pypdf not installed. `pip install pypdf`")
        return ""
    reader = PdfReader(str(path))
    return "\n\n".join((p.extract_text() or "") for p in reader.pages)


def _extract_epub(path: Path) -> str:
    try:
        from ebooklib import epub
        from bs4 import BeautifulSoup
    except ImportError:
        print(f"[warn] ebooklib/bs4 missing — skip {path.name}. `pip install ebooklib beautifulsoup4`")
        return ""
    book = epub.read_epub(str(path))
    parts = []
    for item in book.get_items():
        if item.get_type() == 9:  # ITEM_DOCUMENT
            soup = BeautifulSoup(item.get_content(), "html.parser")
            parts.append(soup.get_text("\n"))
    return "\n\n".join(parts)


def _extract_text(path: Path, engine: str = "pypdf") -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return _extract_pdf(path, engine=engine)
    if ext == ".epub":
        return _extract_epub(path)
    if ext in (".md", ".txt"):
        return path.read_text(encoding="utf-8", errors="ignore")
    # markitdown handles many formats pypdf/ebooklib don't (docx, pptx, xlsx, html, images)
    if engine in ("markitdown", "auto"):
        try:
            from library._md_extract import extract_text as _md_extract
            text = _md_extract(path, engine=engine)
            if text:
                return text
        except Exception:
            pass
    print(f"[warn] unsupported extension: {ext}")
    return ""




def ingest_book(path: Path, force: bool = False, engine: str = "pypdf") -> dict:
    slug = _slugify(path.stem)
    out_dir = CHUNKS_DIR / slug
    meta_path = out_dir / "meta.json"

    file_hash = _file_hash(path)

    if meta_path.exists() and not force:
        prev = json.loads(meta_path.read_text(encoding="utf-8"))
        if prev.get("file_hash") == file_hash and prev.get("engine", "pypdf") == engine:
            return {"book": slug, "status": "skipped_unchanged", "chunks": prev.get("chunks_count", 0)}

    print(f"[ingest] {path.name} ->{slug} (engine={engine})")
    text = _extract_text(path, engine=engine)
    if not text.strip():
        return {"book": slug, "status": "empty", "chunks": 0}

    chunks = _chunk(text)
    out_dir.mkdir(parents=True, exist_ok=True)

    for old in out_dir.glob("*.txt"):
        old.unlink()

    for i, ch in enumerate(chunks):
        (out_dir / f"{i:04d}.txt").write_text(ch, encoding="utf-8")

    meta = {
        "book": slug,
        "source_file": str(path.relative_to(path.parent.parent)),
        "file_hash": file_hash,
        "engine": engine,
        "chunks_count": len(chunks),
        "total_chars": len(text),
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return {**meta, "status": "ingested"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", help="Glob pattern for subset (e.g. 'Dalio_*')")
    ap.add_argument("--force", action="store_true", help="Re-ingest even if unchanged")
    ap.add_argument("--engine", default="pypdf",
                    choices=["pypdf", "markitdown", "auto"],
                    help="Text extraction engine. markitdown preserves "
                         "table/header structure (better RAG retrieval).")
    args = ap.parse_args()

    if not BOOKS_DIR.exists() or not any(BOOKS_DIR.iterdir()):
        print(f"No books in {BOOKS_DIR.relative_to(Path.cwd())}")
        print("Drop .pdf / .epub / .md files there and re-run.")
        return

    pattern = args.book or "*"
    books = [p for p in BOOKS_DIR.glob(pattern)
             if p.suffix.lower() in (".pdf", ".epub", ".md", ".txt")]

    if not books:
        print(f"No books matching {pattern}")
        return

    for b in books:
        result = ingest_book(b, force=args.force, engine=args.engine)
        print(f"  {result['status']:<25}  {result['book']:<30}  chunks={result.get('chunks_count', result.get('chunks', '?'))}")


if __name__ == "__main__":
    main()
