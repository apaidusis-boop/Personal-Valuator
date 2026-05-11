"""Universal document → markdown extraction (markitdown-first, fallbacks).

Adopted 2026-05-10 (Phase MCP-5 sweep). Replaces PDF-only extractors when
the markitdown engine is selected.

Why markitdown:
  - Microsoft `markitdown[pdf]` outputs structured Markdown (headers,
    tables, lists) — better RAG retrieval and LLM ingestion than plain
    text. Empirical bench on 5 CVM PDFs: +3-7% chars vs pdfplumber,
    preserves table structure pdfplumber loses.
  - Handles PDF / DOCX / XLSX / PPTX / HTML / images / audio out of the box,
    enabling formats we currently throw away (presentations, audio earnings,
    YT thumbnails).
  - Slightly slower (~2x) than pdfplumber on plain PDFs, but absolute time
    is negligible (< 1s per CVM PDF).

Engines:
  'markitdown' — primary, MS markitdown
  'pdfplumber' — PDFs only, faster baseline
  'pypdf'      — lightweight PDF, what we used historically
  'auto'       — markitdown first, fall back to pdfplumber/pypdf on error

Surgical: existing call sites can opt in via engine='markitdown' or env
var II_PDF_ENGINE=markitdown. Default remains the legacy engine to keep
diffs zero-impact when not opted in.

Usage:
    from library._md_extract import extract_text
    text = extract_text(Path("report.pdf"), engine="auto")
"""
from __future__ import annotations

import os
from pathlib import Path

DEFAULT_ENGINE = os.environ.get("II_PDF_ENGINE", "pdfplumber")  # legacy default
SUPPORTED_MARKITDOWN_EXTS = {
    ".pdf", ".docx", ".xlsx", ".xls", ".pptx", ".html", ".htm",
    ".txt", ".md", ".csv", ".json", ".xml",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff",
    ".mp3", ".wav", ".m4a", ".flac",
    ".epub", ".zip",
}


def extract_text(path: Path, engine: str | None = None, max_chars: int | None = None) -> str:
    """Extract text/markdown from a document.

    Args:
        path: input file
        engine: 'markitdown' | 'pdfplumber' | 'pypdf' | 'auto' | None
                When None, uses DEFAULT_ENGINE (env II_PDF_ENGINE or pdfplumber).
        max_chars: optional cap

    Returns text (markdown when engine=markitdown). Empty string on failure.
    """
    engine = (engine or DEFAULT_ENGINE).lower()
    path = Path(path)
    if not path.exists():
        return ""

    text = ""
    if engine == "auto":
        text = _try_markitdown(path) or _try_pdfplumber(path) or _try_pypdf(path)
    elif engine == "markitdown":
        text = _try_markitdown(path)
        if not text:
            text = _try_pdfplumber(path) or _try_pypdf(path)  # safety net
    elif engine == "pdfplumber":
        text = _try_pdfplumber(path)
    elif engine == "pypdf":
        text = _try_pypdf(path)
    else:
        raise ValueError(f"unknown engine: {engine}")

    if max_chars and len(text) > max_chars:
        text = text[:max_chars]
    return text


def _try_markitdown(path: Path) -> str:
    if path.suffix.lower() not in SUPPORTED_MARKITDOWN_EXTS:
        return ""
    try:
        from markitdown import MarkItDown
    except ImportError:
        return ""
    try:
        md = MarkItDown()
        return md.convert(str(path)).text_content or ""
    except Exception:
        return ""


def _try_pdfplumber(path: Path) -> str:
    if path.suffix.lower() != ".pdf":
        return ""
    try:
        import pdfplumber
    except ImportError:
        return ""
    try:
        chunks: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                chunks.append(t)
        full = "\n\n".join(c.strip() for c in chunks if c.strip())
        return "\n".join(ln.rstrip() for ln in full.splitlines()).strip()
    except Exception:
        return ""


def _try_pypdf(path: Path) -> str:
    if path.suffix.lower() != ".pdf":
        return ""
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    try:
        reader = PdfReader(str(path))
        return "\n\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        return ""
