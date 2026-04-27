"""Investment Library — book ingestion + method extraction + signal generation.

Pipeline:
    1. Drop books in library/books/ (PDF, EPUB, MD, TXT)
    2. `python library/ingest.py` → extracts chunks with metadata
    3. `python library/extract_methods.py` → Ollama extracts structured rules
    4. Methods stored in library/methods/ as YAML
    5. `python library/match_signals.py` → runs methods vs current state
    6. Signals logged in paper_trade_signals table (NOT real trades!)
    7. Monthly backtest measures hit rate per method

SAFETY PHILOSOPHY:
    - Books generate SIGNALS, never TRADES
    - All signals go to paper_trade_signals first
    - Real capital only after 3-6 months of tracked track record
    - Options/derivative plays require separate consent + vol data we don't have yet
"""
from __future__ import annotations

from pathlib import Path

LIBRARY_ROOT = Path(__file__).resolve().parent
BOOKS_DIR = LIBRARY_ROOT / "books"
METHODS_DIR = LIBRARY_ROOT / "methods"
CHUNKS_DIR = LIBRARY_ROOT / "chunks"

for d in (BOOKS_DIR, METHODS_DIR, CHUNKS_DIR):
    d.mkdir(exist_ok=True)

__all__ = ["LIBRARY_ROOT", "BOOKS_DIR", "METHODS_DIR", "CHUNKS_DIR"]
