"""Shared low-level helpers for library/* — anti-duplication module.

Phase Workday Cleanup (2026-04-27): consolidates _chunk, _file_hash, _slugify
that were duplicated in library/ingest.py and library/clippings_ingest.py.

Convention: this module imports stdlib only; no external deps and never
touches network/DB. Pure helpers reusable by any library.* module.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

DEFAULT_CHUNK_SIZE = 2000
DEFAULT_CHUNK_OVERLAP = 200


def slugify(s: str, maxlen: int = 60) -> str:
    """Filename-safe slug: lowercase, underscore-separated. Truncated.

    Note: agents._common.slugify is the *vault-friendly* version (ascii fold
    via unicodedata, hyphens). This library version keeps underscores +
    raw chars and is what books/clippings ingest historically used.

    >>> slugify("Damodaran Investment Valuation 3rd ed")
    'damodaran_investment_valuation_3rd_ed'
    """
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[-\s]+", "_", s)[:maxlen]


def chunk_text(
    text: str,
    size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """Paragraph-aware chunker. Hard-splits any paragraph that alone exceeds size.

    Identical behavior to the prior _chunk() implementations in ingest.py +
    clippings_ingest.py (verified 2026-04-27).
    """
    if not text:
        return []
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    buf = ""
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


def file_hash(path: Path) -> str:
    """SHA-1 first-16-hex of file contents. Used as content-addressable id."""
    return hashlib.sha1(path.read_bytes()).hexdigest()[:16]
