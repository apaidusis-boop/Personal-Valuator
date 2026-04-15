"""brapi.dev fetcher — piloto ITSA4.

Idempotente. Persiste em data/br_investments.db nas tabelas
companies, prices, fundamentals. Salva também o JSON cru em
logs/ para inspecção manual (passo 2 do plano do HANDOFF).

Uso:
    python fetchers/brapi_fetcher.py            # default: ITSA4
    python fetchers/brapi_fetcher.py PRIO3      # outro ticker
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"

BRAPI_BASE = "https://brapi.dev/api"
# Nota: plano free do brapi.dev só expõe quote básica + fundamental simples
# (earningsPerShare, priceEarnings, marketCap, historicalDataPrice).
# Módulos avançados e ?dividends=true requerem upgrade. Os campos em falta
# (BVPS, ROE, P/B, DY, dívida, EBITDA, histórico de dividendos) ficam NULL
# na DB e serão preenchidos pelo Status Invest scraper (passo 4 do plano).


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False)
    with (LOG_DIR / "brapi_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def load_universe_entry(ticker: str) -> dict | None:
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    br = data.get("br", {})
    pools = []
    for bucket in ("holdings", "watchlist", "research_pool"):
        group = br.get(bucket, {}) or {}
        if isinstance(group, list):
            pools.extend(group)
        else:
            for v in group.values():
                pools.extend(v or [])
    for entry in pools:
        if entry["ticker"] == ticker:
            return entry
    return None


def fetch_brapi(ticker: str, token: str) -> dict:
    url = f"{BRAPI_BASE}/quote/{ticker}"
    params = {
        "token": token,
        "range": "3mo",
        "interval": "1d",
        "fundamental": "true",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    payload = r.json()
    if not payload.get("results"):
        raise RuntimeError(f"empty results for {ticker}: {payload}")
    return payload["results"][0]


def dump_raw(ticker: str, raw: dict) -> Path:
    LOG_DIR.mkdir(exist_ok=True)
    path = LOG_DIR / f"brapi_raw_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def upsert_company(conn: sqlite3.Connection, entry: dict) -> None:
    conn.execute(
        """INSERT INTO companies (ticker, name, sector, is_holding, currency)
           VALUES (?, ?, ?, ?, 'BRL')
           ON CONFLICT(ticker) DO UPDATE SET
             name=excluded.name, sector=excluded.sector, is_holding=excluded.is_holding""",
        (
            entry["ticker"],
            entry["name"],
            entry.get("sector"),
            1 if entry.get("is_holding") else 0,
        ),
    )


def upsert_prices(conn: sqlite3.Connection, ticker: str, raw: dict) -> int:
    history = raw.get("historicalDataPrice") or []
    rows = 0
    for bar in history:
        ts = bar.get("date")
        close = bar.get("close")
        if ts is None or close is None:
            continue
        if isinstance(ts, (int, float)):
            date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        else:
            date = str(ts)[:10]
        conn.execute(
            """INSERT INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)
               ON CONFLICT(ticker, date) DO UPDATE SET close=excluded.close, volume=excluded.volume""",
            (ticker, date, float(close), bar.get("volume")),
        )
        rows += 1
    # cotação actual como linha "hoje" se vier
    reg = raw.get("regularMarketPrice")
    reg_t = raw.get("regularMarketTime")
    if reg is not None and reg_t:
        if isinstance(reg_t, (int, float)):
            date = datetime.fromtimestamp(reg_t, tz=timezone.utc).strftime("%Y-%m-%d")
        else:
            date = str(reg_t)[:10]
        conn.execute(
            """INSERT INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)
               ON CONFLICT(ticker, date) DO UPDATE SET close=excluded.close, volume=excluded.volume""",
            (ticker, date, float(reg), raw.get("regularMarketVolume")),
        )
        rows += 1
    return rows


def _safe(d: dict | None, key: str):
    if not d:
        return None
    return d.get(key)


def compute_dividend_streak(raw: dict) -> int | None:
    cash = (raw.get("dividendsData") or {}).get("cashDividends") or []
    if not cash:
        return None
    years = set()
    for d in cash:
        pd = d.get("paymentDate") or d.get("lastDatePrior") or d.get("approvedOn")
        if not pd:
            continue
        years.add(int(pd[:4]))
    if not years:
        return None
    years_sorted = sorted(years, reverse=True)
    streak = 1
    for prev, cur in zip(years_sorted, years_sorted[1:]):
        if prev - cur == 1:
            streak += 1
        else:
            break
    return streak


def upsert_fundamentals(conn: sqlite3.Connection, ticker: str, raw: dict) -> tuple[str, dict]:
    # Plano free só dá EPS e P/E. Restantes campos ficam NULL e
    # serão preenchidos por outra fonte (Status Invest scraper).
    period_end = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fields = {
        "eps": raw.get("earningsPerShare"),
        "bvps": None,
        "roe": None,
        "pe": raw.get("priceEarnings"),
        "pb": None,
        "dy": None,
        "net_debt_ebitda": None,
        "dividend_streak_years": None,
        "is_aristocrat": None,
    }

    conn.execute(
        """INSERT INTO fundamentals
             (ticker, period_end, eps, bvps, roe, pe, pb, dy,
              net_debt_ebitda, dividend_streak_years, is_aristocrat)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(ticker, period_end) DO UPDATE SET
             eps=excluded.eps, bvps=excluded.bvps, roe=excluded.roe,
             pe=excluded.pe, pb=excluded.pb, dy=excluded.dy,
             net_debt_ebitda=excluded.net_debt_ebitda,
             dividend_streak_years=excluded.dividend_streak_years,
             is_aristocrat=excluded.is_aristocrat""",
        (ticker, period_end, *fields.values()),
    )
    return period_end, fields


def run(ticker: str = "ITSA4") -> None:
    load_dotenv(ROOT / ".env")
    token = os.getenv("BRAPI_TOKEN")
    if not token:
        raise SystemExit("BRAPI_TOKEN ausente em .env")

    entry = load_universe_entry(ticker)
    if entry is None:
        raise SystemExit(f"{ticker} não está em config/universe.yaml")

    _log({"event": "fetch_start", "ticker": ticker})
    raw = fetch_brapi(ticker, token)
    raw_path = dump_raw(ticker, raw)
    _log({"event": "raw_dumped", "ticker": ticker, "path": str(raw_path)})

    with sqlite3.connect(DB_PATH) as conn:
        upsert_company(conn, entry)
        n_prices = upsert_prices(conn, ticker, raw)
        period_end, fields = upsert_fundamentals(conn, ticker, raw)
        conn.commit()

    _log({
        "event": "persisted",
        "ticker": ticker,
        "prices_rows": n_prices,
        "fundamentals_period": period_end,
        "fundamentals": fields,
    })


if __name__ == "__main__":
    tk = sys.argv[1] if len(sys.argv) > 1 else "ITSA4"
    run(tk)
