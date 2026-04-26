"""Clippings ingest — vault `obsidian_vault/Clippings/*.md` → chunks_index.db.

Mirrors `library/ingest.py` mas para clippings web salvos via Obsidian Web
Clipper (Investopedia, Suno, Motley Fool, etc.). Cada clip vira N chunks
embedded localmente (Ollama nomic-embed), prefixados com `book_slug='clip_<slug>'`
para namespace separado dos books.

Idempotente: skip se file_hash inalterado. Chunks armazenados em
`library/chunks/clip_<slug>/*.txt` para inspecção.

Uso:
    python -m library.clippings_ingest                  # ingere novos
    python -m library.clippings_ingest --force          # re-ingest tudo
    python -m library.clippings_ingest --rag-build      # após ingest, embed
    python -m library.clippings_ingest --list           # mostra quais já têm chunks
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIPPINGS_DIR = ROOT / "obsidian_vault" / "Clippings"
CHUNKS_DIR = ROOT / "library" / "chunks"
INDEX_DB = ROOT / "library" / "chunks_index.db"

CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200
SLUG_PREFIX = "clip_"


def _slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[-\s]+", "_", s)[:60]


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Returns (meta, body). Meta is a flat dict from YAML frontmatter."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    raw = parts[1]
    body = parts[2].lstrip("\n")
    meta: dict = {}
    for line in raw.splitlines():
        line = line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2).strip().strip('"').strip("'")
            meta[k] = v
    return meta, body


def _strip_md_artifacts(body: str) -> str:
    """Remove markdown image refs e excessive whitespace para texto mais limpo."""
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def _chunk(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if not text:
        return []
    paragraphs = re.split(r"\n\s*\n", text)
    chunks, buf = [], ""
    for p in paragraphs:
        if len(buf) + len(p) + 2 > size:
            if buf:
                chunks.append(buf.strip())
                tail = buf[-overlap:] if len(buf) > overlap else buf
                buf = tail + "\n\n" + p
            else:
                for i in range(0, len(p), size - overlap):
                    chunks.append(p[i:i + size].strip())
                buf = ""
        else:
            buf = (buf + "\n\n" + p) if buf else p
    if buf.strip():
        chunks.append(buf.strip())
    return chunks


def _file_hash(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()[:16]


def ingest_clip(path: Path, force: bool = False) -> dict:
    slug = SLUG_PREFIX + _slugify(path.stem)
    out_dir = CHUNKS_DIR / slug
    meta_path = out_dir / "meta.json"

    file_hash = _file_hash(path)
    if meta_path.exists() and not force:
        prev = json.loads(meta_path.read_text(encoding="utf-8"))
        if prev.get("file_hash") == file_hash:
            return {"clip": slug, "status": "skipped_unchanged",
                    "chunks": prev.get("chunks_count", 0)}

    raw = path.read_text(encoding="utf-8", errors="ignore")
    fm, body = _parse_frontmatter(raw)
    body = _strip_md_artifacts(body)
    if len(body) < 200:
        return {"clip": slug, "status": "too_short", "chunks": 0,
                "title": fm.get("title", path.stem)}

    chunks = _chunk(body)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.txt"):
        old.unlink()
    for i, ch in enumerate(chunks):
        (out_dir / f"{i:04d}.txt").write_text(ch, encoding="utf-8")

    meta = {
        "clip": slug,
        "source_file": str(path.relative_to(ROOT)),
        "file_hash": file_hash,
        "chunks_count": len(chunks),
        "total_chars": len(body),
        "title": fm.get("title", path.stem),
        "source_url": fm.get("source", ""),
        "author": fm.get("author", ""),
        "published": fm.get("published", ""),
        "tags": fm.get("tags", ""),
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False),
                         encoding="utf-8")
    return {**meta, "status": "ingested"}


def list_clips() -> None:
    print(f"Clippings inventory ({CLIPPINGS_DIR.relative_to(ROOT)}):")
    in_db: set[str] = set()
    if INDEX_DB.exists():
        with sqlite3.connect(INDEX_DB) as c:
            in_db = {r[0] for r in c.execute(
                f"SELECT DISTINCT book_slug FROM chunk_index "
                f"WHERE book_slug LIKE '{SLUG_PREFIX}%'"
            ).fetchall()}
    for p in sorted(CLIPPINGS_DIR.glob("*.md")):
        if p.stem.startswith("_"):
            continue
        slug = SLUG_PREFIX + _slugify(p.stem)
        embed_status = "✓ embed" if slug in in_db else "✗ embed"
        chunks_dir = CHUNKS_DIR / slug
        chunks_count = len(list(chunks_dir.glob("*.txt"))) if chunks_dir.exists() else 0
        print(f"  {embed_status} | {chunks_count:>3} chunks | {p.name[:60]}")
    print(f"\nClippings dir: {len(list(CLIPPINGS_DIR.glob('*.md')))} files")
    print(f"In RAG index:  {len(in_db)}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--list", action="store_true",
                    help="show inventory + embed status")
    ap.add_argument("--rag-build", action="store_true",
                    help="after ingest, run library.rag build for clip_*")
    args = ap.parse_args()

    if args.list:
        list_clips()
        return

    if not CLIPPINGS_DIR.exists():
        print(f"[ingest] no clippings dir at {CLIPPINGS_DIR}")
        return

    files = [p for p in CLIPPINGS_DIR.glob("*.md") if not p.stem.startswith("_")]
    if not files:
        print("[ingest] no clippings to process")
        return

    print(f"[ingest] {len(files)} clippings in {CLIPPINGS_DIR.relative_to(ROOT)}")
    ok = skipped = err = 0
    for p in files:
        try:
            r = ingest_clip(p, force=args.force)
            status = r.get("status", "?")
            print(f"  {status:<22} {r.get('clip', '?'):<60} chunks={r.get('chunks_count', 0)}")
            if status == "ingested":
                ok += 1
            elif status == "skipped_unchanged":
                skipped += 1
            else:
                err += 1
        except Exception as e:
            err += 1
            print(f"  ERROR  {p.name}: {e}")
    print(f"\n[summary] ingested={ok} skipped={skipped} errors={err}")

    if args.rag_build:
        print("\n[rag] building embeddings for new clips...")
        # delegate to library.rag (same DB schema, just different book_slug prefix)
        from library import rag
        rag.ensure_schema()
        # iterate every clip_* slug in chunks dir and embed each missing chunk
        with sqlite3.connect(INDEX_DB) as c:
            for clip_dir in sorted(CHUNKS_DIR.glob(f"{SLUG_PREFIX}*")):
                if not clip_dir.is_dir():
                    continue
                slug = clip_dir.name
                txts = sorted(clip_dir.glob("*.txt"))
                if not txts:
                    continue
                existing = {r[0] for r in c.execute(
                    "SELECT chunk_file FROM chunk_index WHERE book_slug=?",
                    (slug,)
                ).fetchall()}
                missing = [p for p in txts if p.name not in existing]
                if not missing:
                    continue
                print(f"  embed {slug}: {len(missing)}/{len(txts)} new chunks")
                for txt_path in missing:
                    text = txt_path.read_text(encoding="utf-8")
                    emb = rag.embed(text)
                    if emb is None:
                        continue
                    import struct
                    blob = struct.pack(f"<{len(emb)}f", *emb)
                    c.execute(
                        "INSERT OR REPLACE INTO chunk_index "
                        "(book_slug, chunk_file, text, embedding, n_tokens) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (slug, txt_path.name, text, blob, len(text) // 4)
                    )
                c.commit()
        print("[rag] embeddings complete")


if __name__ == "__main__":
    main()
