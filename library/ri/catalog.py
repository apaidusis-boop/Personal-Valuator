"""Catalog accessor — fonte canónica única de tickers.

Resolve bug pattern recorrente onde código novo lia só `stocks` section
e ignorava `watchlist_stocks`/`fiis`/`watchlist_fiis` adicionados depois.

Use ESTAS funções (não yaml.safe_load directo no catalog.yaml):

    from library.ri.catalog import all_tickers, all_stocks, all_fiis, by_cnpj_index, by_codigo_cvm_index

    for ticker in all_tickers():    # holdings + watchlist, both stocks + fiis
        ...

    for entry in all_stocks(include_watchlist=True):
        ...
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

CATALOG_PATH = Path(__file__).resolve().parent / "catalog.yaml"


@lru_cache(maxsize=1)
def _load_raw() -> dict:
    """Cached load. Use clear_cache() if catalog.yaml is edited mid-process."""
    return yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8")) or {}


def clear_cache() -> None:
    """Force reload (useful em testes ou após edit programático)."""
    _load_raw.cache_clear()


def all_stocks(include_watchlist: bool = True) -> list[dict]:
    """Returns all stock entries (holdings only, ou + watchlist)."""
    cat = _load_raw()
    out = list(cat.get("stocks") or [])
    if include_watchlist:
        out.extend(cat.get("watchlist_stocks") or [])
    return out


def all_fiis(include_watchlist: bool = True) -> list[dict]:
    """Returns all FII entries (holdings only, ou + watchlist)."""
    cat = _load_raw()
    out = list(cat.get("fiis") or [])
    if include_watchlist:
        out.extend(cat.get("watchlist_fiis") or [])
    return out


def all_entries(include_watchlist: bool = True,
                include_fiis: bool = True) -> list[dict]:
    """All entries (stocks + FIIs), holdings + watchlist by default."""
    out = list(all_stocks(include_watchlist=include_watchlist))
    if include_fiis:
        out.extend(all_fiis(include_watchlist=include_watchlist))
    return out


def all_tickers(include_watchlist: bool = True,
                include_fiis: bool = True) -> list[str]:
    """Just ticker symbols."""
    return [e["ticker"] for e in all_entries(include_watchlist=include_watchlist,
                                              include_fiis=include_fiis)]


def by_cnpj_index(include_watchlist: bool = True,
                  include_fiis: bool = True) -> dict[str, dict]:
    """{cnpj_clean (digits only): entry}."""
    out = {}
    for e in all_entries(include_watchlist=include_watchlist,
                         include_fiis=include_fiis):
        cnpj = e.get("cnpj")
        if cnpj:
            out["".join(c for c in cnpj if c.isdigit())] = e
    return out


def by_codigo_cvm_index(include_watchlist: bool = True) -> dict[str, dict]:
    """{codigo_cvm (str): entry} for stocks (FIIs use CNPJ, not codigo_cvm)."""
    out = {}
    for e in all_stocks(include_watchlist=include_watchlist):
        cv = e.get("codigo_cvm")
        if cv:
            out[str(cv)] = e
    return out


def find_by_ticker(ticker: str) -> dict | None:
    for e in all_entries():
        if e.get("ticker") == ticker:
            return e
    return None


def banks() -> list[dict]:
    """Entries with bank=true OR sector='Banks'."""
    return [e for e in all_entries() if e.get("bank") or e.get("sector") == "Banks"]


def __ack_legacy():
    """Tests: validate this module is being adopted everywhere."""
    return {"all_tickers": len(all_tickers()), "stocks": len(all_stocks()), "fiis": len(all_fiis())}
