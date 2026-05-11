"""RI Knowledge Base — primary-source IR documents para tickers BR.

Phase Y. Ver `obsidian_vault/skills/Phase_Y_Roadmap.md`.

Módulos:
    catalog    — leitor do catalog.yaml
    cvm_codes  — resolve/valida codigo_cvm e CNPJ via CVM cadastral CSV

Mais a vir em Y.2+: cvm_filings, cvm_parser, ri_scraper, indexer, cli.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "catalog.yaml"
CACHE_DIR = ROOT / "cache"
CACHE_DIR.mkdir(exist_ok=True)

__all__ = ["ROOT", "CATALOG_PATH", "CACHE_DIR"]
