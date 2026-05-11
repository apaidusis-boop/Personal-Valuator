"""Scraper de FIIs via Status Invest.

Fonte: https://statusinvest.com.br/fundos-imobiliarios/<ticker>

Persiste em fii_fundamentals. Idempotente. Cache-aware via
fetchers.cache_policy.

Métricas extraídas do padrão <h3 class="title"> + <strong class="value">:
  - Valor atual                      → price
  - Val. patrimonial p/cota          → vpa
  - P/VP                              → pvp
  - RENDIMENTO MENSAL MÉDIO (24M)    → avg_monthly_rendimento_24m
  - Tipo ANBIMA                       → segment_anbima

Métricas calculadas:
  - dy_12m = avg_monthly_rendimento_24m * 12 / price

Métricas ainda n/a (scraping futuro):
  - physical_vacancy, financial_vacancy  (só para tijolo)
  - adtv_daily                            (liquidez)
  - distribution_streak_months           (requer histórico de dividendos)

Uso:
    python fetchers/fii_statusinvest_scraper.py XPML11
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import requests
import yaml

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from fetchers.cache_policy import is_fresh, now_iso  # noqa: E402

ROOT = _ROOT
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"

BASE = "https://statusinvest.com.br"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

PAIR_RE = re.compile(
    r'<h3[^>]*class="title[^"]*"[^>]*>([^<]+)</h3>'
    r'.*?<strong[^>]*class="value[^"]*"[^>]*>([^<]+)</strong>',
    re.S,
)


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": now_iso(), **event}, ensure_ascii=False)
    with (LOG_DIR / "fii_statusinvest_scraper.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _to_float(s: str | None) -> float | None:
    if s is None:
        return None
    s = unescape(s).strip()
    if s in {"-", "", "n/a", "N/A"}:
        return None
    pct = s.endswith("%")
    s = s.replace("%", "").replace(".", "").replace(",", ".").strip()
    try:
        v = float(s)
    except ValueError:
        return None
    return v / 100 if pct else v


def load_fii_entry(ticker: str) -> dict | None:
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    br = data.get("br", {}) or {}
    pools: list[dict] = []
    pools.extend((br.get("holdings") or {}).get("fiis", []) or [])
    pools.extend((br.get("watchlist") or {}).get("fiis", []) or [])
    for entry in pools:
        if entry["ticker"] == ticker:
            return entry
    return None


def fetch_indicators(ticker: str) -> dict:
    url = f"{BASE}/fundos-imobiliarios/{ticker.lower()}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    pairs: dict[str, str] = {}
    for m in PAIR_RE.finditer(r.text):
        label = unescape(re.sub(r"\s+", " ", m.group(1)).strip())
        pairs.setdefault(label, m.group(2).strip())
    return pairs


def parse_fii(pairs: dict) -> dict:
    price = _to_float(pairs.get("Valor atual"))
    vpa = _to_float(pairs.get("Val. patrimonial p/cota"))
    pvp = _to_float(pairs.get("P/VP"))
    avg_24m = _to_float(pairs.get("RENDIMENTO MENSAL MÉDIO (24M)"))
    dy_12m = None
    if avg_24m is not None and price and price > 0:
        dy_12m = (avg_24m * 12) / price
    segment = pairs.get("Tipo ANBIMA")
    segment = unescape(segment).strip() if segment else None
    return {
        "price": price,
        "vpa": vpa,
        "pvp": pvp,
        "avg_monthly_rendimento_24m": avg_24m,
        "dy_12m": dy_12m,
        "segment_anbima": segment,
    }


def upsert_company(conn: sqlite3.Connection, entry: dict) -> None:
    conn.execute(
        """INSERT INTO companies (ticker, name, sector, is_holding, currency)
           VALUES (?, ?, ?, ?, 'BRL')
           ON CONFLICT(ticker) DO UPDATE SET
             name=excluded.name, sector=excluded.sector, is_holding=excluded.is_holding""",
        (
            entry["ticker"],
            entry["name"],
            entry.get("segment") or entry.get("sector"),
            1 if entry.get("is_holding") else 0,
        ),
    )


def upsert_fii_fundamentals(conn: sqlite3.Connection, ticker: str, fields: dict) -> str:
    period = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    conn.execute(
        """INSERT INTO fii_fundamentals
             (ticker, period_end, price, vpa, pvp, dy_12m,
              last_monthly_rendimento, avg_monthly_rendimento_24m,
              physical_vacancy, financial_vacancy, adtv_daily,
              distribution_streak_months, segment_anbima, management_type,
              source, fetched_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(ticker, period_end) DO UPDATE SET
             price=excluded.price, vpa=excluded.vpa, pvp=excluded.pvp,
             dy_12m=excluded.dy_12m,
             avg_monthly_rendimento_24m=excluded.avg_monthly_rendimento_24m,
             segment_anbima=excluded.segment_anbima,
             fetched_at=excluded.fetched_at""",
        (
            ticker, period,
            fields.get("price"), fields.get("vpa"), fields.get("pvp"),
            fields.get("dy_12m"),
            None,  # last_monthly_rendimento — TODO
            fields.get("avg_monthly_rendimento_24m"),
            None, None, None, None,  # vacancy/adtv/streak — TODO
            fields.get("segment_anbima"), None,
            "statusinvest", now_iso(),
        ),
    )
    return period


def run(ticker: str, force: bool = False) -> None:
    entry = load_fii_entry(ticker)
    if entry is None:
        raise SystemExit(f"{ticker} não é um FII conhecido em universe.yaml")

    # cache check
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT fetched_at FROM fii_fundamentals WHERE ticker=? "
            "ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
    if not force and row and is_fresh(row[0], "fundamental_snapshot"):
        _log({"event": "fii_scrape_skip_fresh", "ticker": ticker, "fetched_at": row[0]})
        return

    _log({"event": "fii_scrape_start", "ticker": ticker})
    pairs = fetch_indicators(ticker)
    fields = parse_fii(pairs)

    with sqlite3.connect(DB_PATH) as conn:
        upsert_company(conn, entry)
        period = upsert_fii_fundamentals(conn, ticker, fields)
        conn.commit()

    _log({"event": "fii_scraped", "ticker": ticker, "period": period, "fields": fields})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="XPML11")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    run(args.ticker, force=args.force)


if __name__ == "__main__":
    main()
