"""Monitor de filings SEC EDGAR — 8-K, 10-K, 10-Q, dividend declarations.

Fonte: SEC EDGAR EFTS (full-text search API), gratuita, sem auth.
  https://efts.sec.gov/LATEST/search-index?q=...&dateRange=...&forms=...

Alternativa: company filings RSS feed
  https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<cik>&type=<form>&dateb=&owner=include&count=40&search_text=&action=getcompany

Idempotente: desduplica por (ticker, source='sec', event_date, url).

Uso:
    python monitors/sec_monitor.py AAPL
    python monitors/sec_monitor.py KO --forms 8-K,10-K
    python monitors/sec_monitor.py --all          # todos os tickers US do universe.yaml
    python monitors/sec_monitor.py --all --year 2025
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "us_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"

# SEC EDGAR full-text search (EFTS) — pública, sem auth, rate limit ~10 req/s.
# User-Agent obrigatório: SEC exige identificação.
EFTS_URL = "https://efts.sec.gov/LATEST/search-index"
EDGAR_FILINGS_URL = "https://www.sec.gov/cgi-bin/browse-edgar"
EDGAR_FILING_BASE = "https://www.sec.gov/Archives/edgar/data"

# Forms que nos interessam para a estratégia DRIP / Buffett.
DEFAULT_FORMS = ["8-K", "10-K", "10-Q"]

# SEC exige User-Agent com nome e email reais.
# O utilizador deve preencher em .env ou aqui. Default genérico para dev.
HEADERS = {
    "User-Agent": "PersonalValuator/1.0 (personal research; contact@example.com)",
    "Accept": "application/json",
}

# Rate limit: SEC pede no máximo 10 req/s. Usamos 0.15s entre pedidos.
RATE_LIMIT_SLEEP = 0.15


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with (LOG_DIR / "sec_monitor.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


# ---------- universe.yaml ----------

def _load_us_tickers() -> list[dict]:
    """Devolve todas as entradas US do universe.yaml."""
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    us = data.get("us", {}) or {}
    entries: list[dict] = []
    for bucket in ("holdings", "watchlist"):
        group = us.get(bucket, {}) or {}
        if isinstance(group, list):
            entries.extend(group)
        else:
            for section in group.values():
                entries.extend(section or [])
    return entries


def all_us_tickers() -> list[str]:
    return [e["ticker"] for e in _load_us_tickers()]


# ---------- EDGAR search ----------

def _ticker_to_cik(ticker: str) -> str | None:
    """Resolve ticker para CIK via EDGAR company search.
    Usa o endpoint JSON de tickers da SEC."""
    url = "https://www.sec.gov/files/company_tickers.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        # data é {0: {cik_str, ticker, title}, 1: ...}
        for entry in data.values():
            if entry.get("ticker", "").upper() == ticker.upper():
                return str(entry["cik_str"]).zfill(10)
    except Exception as exc:  # noqa: BLE001
        _log({"event": "sec_cik_lookup_failed", "ticker": ticker, "err": str(exc)})
    return None


def fetch_filings(ticker: str, forms: list[str] | None = None,
                  year: int | None = None) -> list[dict]:
    """Busca filings via EDGAR EFTS search API.

    Devolve lista de dicts com: accessionNo, filedAt, formType, description, url.
    """
    forms = forms or DEFAULT_FORMS
    cik = _ticker_to_cik(ticker)
    if not cik:
        _log({"event": "sec_cik_not_found", "ticker": ticker})
        return []

    results = []
    for form in forms:
        params = {
            "q": f'"{ticker}"',
            "forms": form,
            "dateRange": "custom",
        }
        if year:
            params["startdt"] = f"{year}-01-01"
            params["enddt"] = f"{year}-12-31"
        else:
            # Último ano
            now = datetime.now()
            params["startdt"] = f"{now.year - 1}-01-01"
            params["enddt"] = now.strftime("%Y-%m-%d")

        try:
            r = requests.get(EFTS_URL, params=params, headers=HEADERS, timeout=30)
            r.raise_for_status()
            data = r.json()
            hits = data.get("hits", {}).get("hits", [])
            for hit in hits:
                src = hit.get("_source", {})
                filing = {
                    "accession": src.get("file_num", ""),
                    "filed_at": (src.get("file_date") or "")[:10],
                    "form_type": src.get("form_type", form),
                    "description": src.get("display_names", [None])[0] if src.get("display_names") else None,
                    "url": _filing_url(cik, src) if src.get("file_num") else None,
                }
                results.append(filing)
        except Exception as exc:  # noqa: BLE001
            _log({"event": "sec_fetch_error", "ticker": ticker, "form": form,
                  "err": str(exc)})

        time.sleep(RATE_LIMIT_SLEEP)

    return results


def _filing_url(cik: str, src: dict) -> str | None:
    """Monta URL para a filing page. Best-effort."""
    accession = src.get("accession_no") or src.get("file_num")
    if not accession:
        return None
    accession_clean = accession.replace("-", "")
    return f"{EDGAR_FILING_BASE}/{cik.lstrip('0')}/{accession_clean}/{accession}-index.htm"


def _kind_from_form(form_type: str) -> str:
    """Mapeia form type para kind na tabela events."""
    form = form_type.upper().strip()
    if form == "8-K":
        return "8-K"
    if form in ("10-K", "10-K/A"):
        return "10-K"
    if form in ("10-Q", "10-Q/A"):
        return "10-Q"
    if "DIV" in form or "EX-" in form:
        return "dividend"
    return form.lower()


# ---------- persistência ----------

def persist(conn: sqlite3.Connection, ticker: str, filings: list[dict]) -> int:
    inserted = 0
    for f in filings:
        event_date = f["filed_at"]
        url = f["url"]
        if not event_date:
            continue
        exists = conn.execute(
            """SELECT 1 FROM events
               WHERE ticker=? AND source='sec' AND event_date=? AND url=?""",
            (ticker, event_date, url),
        ).fetchone()
        if exists:
            continue

        kind = _kind_from_form(f["form_type"])
        summary = f"{f['form_type']}"
        if f.get("description"):
            summary += f" — {f['description']}"

        conn.execute(
            """INSERT INTO events (ticker, event_date, source, kind, url, summary)
               VALUES (?,?,?,?,?,?)""",
            (ticker, event_date, "sec", kind, url, summary),
        )
        inserted += 1
    return inserted


# ---------- pipeline ----------

def run(ticker: str, forms: list[str] | None = None,
        year: int | None = None) -> dict:
    _log({"event": "sec_fetch_start", "ticker": ticker, "forms": forms or DEFAULT_FORMS,
          "year": year})

    filings = fetch_filings(ticker, forms=forms, year=year)
    _log({"event": "sec_fetched", "ticker": ticker, "filings_count": len(filings)})

    with sqlite3.connect(DB_PATH) as conn:
        # Garantir que o ticker existe em companies
        conn.execute(
            """INSERT INTO companies (ticker, name, sector, is_holding, currency)
               VALUES (?, ?, NULL, 0, 'USD')
               ON CONFLICT(ticker) DO NOTHING""",
            (ticker, ticker),
        )
        inserted = persist(conn, ticker, filings)
        conn.commit()

    result = {"ticker": ticker, "fetched": len(filings), "inserted": inserted,
              "already_in_db": len(filings) - inserted}
    _log({"event": "sec_persisted", **result})
    return result


def run_all(forms: list[str] | None = None, year: int | None = None) -> list[dict]:
    """Corre o monitor para todos os tickers US do universe.yaml."""
    tickers = all_us_tickers()
    _log({"event": "sec_batch_start", "tickers": tickers, "year": year})

    results = []
    for ticker in tickers:
        try:
            r = run(ticker, forms=forms, year=year)
            results.append(r)
        except KeyboardInterrupt:
            raise
        except (Exception, SystemExit) as exc:  # noqa: BLE001
            _log({"event": "sec_ticker_error", "ticker": ticker, "err": str(exc)})
            results.append({"ticker": ticker, "error": str(exc)})
        time.sleep(RATE_LIMIT_SLEEP)

    _log({"event": "sec_batch_done", "total_tickers": len(tickers),
          "total_inserted": sum(r.get("inserted", 0) for r in results)})
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description="SEC EDGAR filing monitor")
    ap.add_argument("ticker", nargs="?", default="AAPL")
    ap.add_argument("--forms", default=None,
                    help="Comma-separated form types (default: 8-K,10-K,10-Q)")
    ap.add_argument("--year", type=int, default=None)
    ap.add_argument("--all", action="store_true",
                    help="Correr para todos os tickers US do universe.yaml")
    args = ap.parse_args()

    forms = args.forms.split(",") if args.forms else None
    if args.all:
        run_all(forms=forms, year=args.year)
    else:
        run(args.ticker, forms=forms, year=args.year)


if __name__ == "__main__":
    main()
