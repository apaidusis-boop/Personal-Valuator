"""CVM code helper — resolve/validate ticker ↔ codigo_cvm via cad_cia_aberta.csv.

Source: dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv

Cache: library/ri/cache/cad_cia_aberta.csv (refresh weekly via TTL).

Uso:
    python -m library.ri.cvm_codes refresh
    python -m library.ri.cvm_codes lookup VALE3
    python -m library.ri.cvm_codes validate-catalog
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path
from typing import Iterator

import requests

from . import CACHE_DIR
from . import catalog as _catalog

CAD_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"
CAD_CACHE = CACHE_DIR / "cad_cia_aberta.csv"
CAD_TTL_SEC = 7 * 24 * 3600  # 1 week

CAD_FII_URL = "https://dados.cvm.gov.br/dados/FII/CAD/DADOS/cad_fii.csv"
CAD_FII_CACHE = CACHE_DIR / "cad_fii.csv"

USER_AGENT = "investment-intelligence-bot/1.0 (personal-research; non-commercial)"


def _is_cache_fresh(path: Path, ttl: int = CAD_TTL_SEC) -> bool:
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age < ttl


def fetch_cad(force: bool = False) -> Path:
    if not force and _is_cache_fresh(CAD_CACHE):
        return CAD_CACHE
    print(f"[cvm_codes] downloading {CAD_URL}")
    r = requests.get(CAD_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
    r.raise_for_status()
    CAD_CACHE.write_bytes(r.content)
    print(f"  saved {len(r.content)/1024:.1f}KB to {CAD_CACHE.name}")
    return CAD_CACHE


def fetch_cad_fii(force: bool = False) -> Path:
    if not force and _is_cache_fresh(CAD_FII_CACHE):
        return CAD_FII_CACHE
    print(f"[cvm_codes] downloading {CAD_FII_URL}")
    r = requests.get(CAD_FII_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
    r.raise_for_status()
    CAD_FII_CACHE.write_bytes(r.content)
    print(f"  saved {len(r.content)/1024:.1f}KB to {CAD_FII_CACHE.name}")
    return CAD_FII_CACHE


def _read_csv_latin1(path: Path) -> Iterator[dict]:
    """CVM CSVs use Latin-1 + ; separator."""
    with open(path, encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            yield row


def lookup_by_codigo_cvm(codigo: int) -> dict | None:
    fetch_cad()
    for row in _read_csv_latin1(CAD_CACHE):
        try:
            if int(row.get("CD_CVM", "0")) == codigo:
                return row
        except ValueError:
            continue
    return None


def lookup_by_cnpj(cnpj: str) -> dict | None:
    fetch_cad()
    cnpj_clean = "".join(c for c in cnpj if c.isdigit())
    for row in _read_csv_latin1(CAD_CACHE):
        row_cnpj = "".join(c for c in row.get("CNPJ_CIA", "") if c.isdigit())
        if row_cnpj == cnpj_clean:
            return row
    return None


def lookup_fii_by_cnpj(cnpj: str) -> dict | None:
    fetch_cad_fii()
    cnpj_clean = "".join(c for c in cnpj if c.isdigit())
    for row in _read_csv_latin1(CAD_FII_CACHE):
        row_cnpj = "".join(c for c in row.get("CNPJ_Fundo", row.get("CNPJ_FUNDO", "")) if c.isdigit())
        if row_cnpj == cnpj_clean:
            return row
    return None


def fii_search_by_ticker(ticker: str) -> list[dict]:
    """FIIs cadastram-se pelo CNPJ; ticker (ex: PVBI11) procura-se em DENOM_SOCIAL."""
    fetch_cad_fii()
    ticker_u = ticker.upper().rstrip("0123456789").rstrip()
    matches = []
    for row in _read_csv_latin1(CAD_FII_CACHE):
        denom = (row.get("DENOM_SOCIAL", "") or row.get("Nome_Fundo", "")).upper()
        if ticker_u and ticker_u in denom:
            matches.append(row)
    return matches[:10]


def validate_catalog(verbose: bool = True) -> dict:
    results = {"stocks_ok": 0, "stocks_fail": 0, "fiis_ok": 0, "fiis_fail": 0,
               "issues": []}

    for entry in _catalog.all_stocks(include_watchlist=True):
        ticker = entry["ticker"]
        codigo = entry.get("codigo_cvm")
        cnpj = entry.get("cnpj")
        row = lookup_by_codigo_cvm(codigo) if codigo else None
        if not row and cnpj:
            row = lookup_by_cnpj(cnpj)
        if row:
            results["stocks_ok"] += 1
            if verbose:
                print(f"  OK   {ticker:<8}  cvm={row.get('CD_CVM','?'):<8}  {row.get('DENOM_SOCIAL','')[:50]}")
        else:
            results["stocks_fail"] += 1
            msg = f"FAIL {ticker} (cvm={codigo}, cnpj={cnpj}) — not found in cad_cia_aberta.csv"
            results["issues"].append(msg)
            if verbose:
                print(f"  {msg}")

    for entry in _catalog.all_fiis(include_watchlist=True):
        ticker = entry["ticker"]
        cnpj = entry.get("cnpj")
        if not cnpj:
            results["fiis_fail"] += 1
            msg = f"FII {ticker}: CNPJ ausente — needs lookup via fii_search_by_ticker"
            results["issues"].append(msg)
            if verbose:
                print(f"  TODO {ticker:<8}  CNPJ ausente; tentar fii_search_by_ticker")
                hits = fii_search_by_ticker(ticker)
                for h in hits[:3]:
                    print(f"        candidate: {h.get('CNPJ_Fundo','?')}  {h.get('DENOM_SOCIAL','')[:60]}")
            continue
        row = lookup_fii_by_cnpj(cnpj)
        if row:
            results["fiis_ok"] += 1
            if verbose:
                print(f"  OK   {ticker:<8}  cnpj={cnpj}  {(row.get('DENOM_SOCIAL') or row.get('Nome_Fundo',''))[:50]}")
        else:
            results["fiis_fail"] += 1
            msg = f"FAIL FII {ticker} (cnpj={cnpj}) — not found in cad_fii.csv"
            results["issues"].append(msg)
            if verbose:
                print(f"  {msg}")

    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("refresh")

    p_lookup = sub.add_parser("lookup")
    p_lookup.add_argument("ticker_or_cnpj")

    sub.add_parser("validate-catalog")

    p_fii = sub.add_parser("fii-search")
    p_fii.add_argument("ticker")

    args = ap.parse_args()

    if args.cmd == "refresh":
        fetch_cad(force=True)
        fetch_cad_fii(force=True)
    elif args.cmd == "lookup":
        for e in _catalog.all_stocks(include_watchlist=True):
            if e["ticker"] == args.ticker_or_cnpj:
                row = lookup_by_codigo_cvm(e["codigo_cvm"])
                print(f"Catalog entry: {e}")
                print(f"CVM record:    {row}")
                return
        # else try as cnpj
        row = lookup_by_cnpj(args.ticker_or_cnpj)
        print(row)
    elif args.cmd == "validate-catalog":
        sys.stdout.reconfigure(encoding="utf-8")
        r = validate_catalog()
        print(f"\nSummary: stocks ok={r['stocks_ok']}/{r['stocks_ok']+r['stocks_fail']}, "
              f"fiis ok={r['fiis_ok']}/{r['fiis_ok']+r['fiis_fail']}")
    elif args.cmd == "fii-search":
        sys.stdout.reconfigure(encoding="utf-8")
        for h in fii_search_by_ticker(args.ticker):
            print(f"  {h.get('CNPJ_Fundo','?'):<22}  {h.get('DENOM_SOCIAL','')[:80]}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
