"""Tests for Phase MCP-5 wiring (markitdown + portal_playwright).

Locks in:
  - library/_md_extract.py multi-engine routing
  - monitors/cvm_pdf_extractor accepts engine arg + defaults preserved
  - library/ingest accepts engine arg + defaults preserved
  - fetchers/subscriptions/_pdf_extract accepts engine kwarg + defaults preserved
  - portal_playwright module loads (no chromium needed for import test)

Does NOT cover:
  - Live Playwright rendering (requires chromium + network)
  - Live Tavily calls (requires API key + network)
  - MCP server activation (requires Claude Code restart)
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def cvm_pdf() -> Path:
    """Return any existing CVM PDF for live extraction testing."""
    candidates = sorted((ROOT / "data" / "cvm_pdfs").glob("*.pdf"))
    if not candidates:
        pytest.skip("no CVM PDFs available — populate data/cvm_pdfs/ to run live tests")
    return candidates[0]


def test_md_extract_imports():
    from library import _md_extract
    assert hasattr(_md_extract, "extract_text")
    assert hasattr(_md_extract, "SUPPORTED_MARKITDOWN_EXTS")


def test_md_extract_engine_dispatch(cvm_pdf):
    from library._md_extract import extract_text

    pl = extract_text(cvm_pdf, engine="pdfplumber")
    pp = extract_text(cvm_pdf, engine="pypdf")
    mt = extract_text(cvm_pdf, engine="markitdown")

    # all three should return non-empty text on a clean CVM fato relevante
    assert len(pl) > 100, "pdfplumber returned no text"
    assert len(pp) > 100, "pypdf returned no text"
    assert len(mt) > 100, "markitdown returned no text"


def test_md_extract_auto_falls_back():
    """auto engine should produce non-empty even if one engine misbehaves."""
    from library._md_extract import extract_text
    candidates = sorted((ROOT / "data" / "cvm_pdfs").glob("*.pdf"))
    if not candidates:
        pytest.skip("no CVM PDFs")
    text = extract_text(candidates[0], engine="auto")
    assert len(text) > 100


def test_md_extract_unknown_engine_raises(tmp_path: Path):
    from library._md_extract import extract_text
    # need a real path so we get past the existence check before the engine check
    p = tmp_path / "real.pdf"
    p.write_bytes(b"%PDF-1.4 dummy")
    with pytest.raises(ValueError):
        extract_text(p, engine="bogus")


def test_md_extract_unsupported_extension_returns_empty(tmp_path: Path):
    from library._md_extract import extract_text
    # write a fake .xyz file
    p = tmp_path / "weird.xyz"
    p.write_text("hello world", encoding="utf-8")
    # markitdown should refuse, fallback engines should also refuse non-PDF
    assert extract_text(p, engine="markitdown") == ""
    assert extract_text(p, engine="pdfplumber") == ""
    assert extract_text(p, engine="pypdf") == ""


def test_cvm_extractor_default_preserved():
    """Cron-invoked path must keep pdfplumber as default to avoid regression."""
    from monitors.cvm_pdf_extractor import run, extract_text, process_event
    sig = inspect.signature(run)
    assert sig.parameters["engine"].default == "pdfplumber"
    sig2 = inspect.signature(extract_text)
    assert sig2.parameters["engine"].default == "pdfplumber"
    sig3 = inspect.signature(process_event)
    assert sig3.parameters["engine"].default == "pdfplumber"


def test_cvm_extractor_markitdown_engine_works(cvm_pdf):
    from monitors.cvm_pdf_extractor import extract_text
    text = extract_text(cvm_pdf, engine="markitdown")
    assert len(text) > 100


def test_library_ingest_default_preserved():
    """Library ingest cron must keep pypdf as default."""
    from library.ingest import ingest_book, _extract_pdf, _extract_text
    assert inspect.signature(ingest_book).parameters["engine"].default == "pypdf"
    assert inspect.signature(_extract_pdf).parameters["engine"].default == "pypdf"
    assert inspect.signature(_extract_text).parameters["engine"].default == "pypdf"


def test_library_ingest_markitdown_engine_works(cvm_pdf):
    """Even though it's a CVM PDF, the library ingest path should accept it."""
    from library.ingest import _extract_pdf
    text = _extract_pdf(cvm_pdf, engine="markitdown")
    assert len(text) > 100


def test_subs_pdf_extract_default_preserved():
    """Subscriptions pipeline default must remain pypdf."""
    from fetchers.subscriptions._pdf_extract import extract_pdf_text
    assert inspect.signature(extract_pdf_text).parameters["engine"].default == "pypdf"


def test_subs_pdf_extract_markitdown_works(cvm_pdf):
    from fetchers.subscriptions._pdf_extract import extract_pdf_text
    # using a CVM PDF as a stand-in for a clean text-based subscription PDF
    text = extract_pdf_text(cvm_pdf, engine="markitdown")
    assert len(text) > 100


def test_portal_playwright_module_loads():
    """Module-level import + signature check; does NOT launch browser."""
    from fetchers import portal_playwright
    assert hasattr(portal_playwright, "fetch")
    sig = inspect.signature(portal_playwright.fetch)
    assert "md" in sig.parameters
    assert "screenshot" in sig.parameters
    assert "ttl_hours" in sig.parameters


def test_portal_playwright_cache_paths_isolated():
    """Cache key must be deterministic (sha1 of URL) and unique per URL."""
    from fetchers.portal_playwright import _cache_key
    assert _cache_key("https://a.com") != _cache_key("https://b.com")
    assert _cache_key("https://a.com") == _cache_key("https://a.com")
