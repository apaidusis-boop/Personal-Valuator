"""Status Invest scraper — fallback BR.

Preenche os campos que o plano free do brapi.dev não expõe:
DY, P/VP, BVPS (VPA), ROE, Dív. líq/EBITDA, dividend_streak_years.

Fonte:
  - https://statusinvest.com.br/acoes/<ticker>          (HTML, indicadores)
  - https://statusinvest.com.br/acao/companytickerprovents
                                                        (JSON, série anual)

Idempotente. Faz UPDATE da linha mais recente em fundamentals
para o ticker — não cria novas linhas. O brapi_fetcher cria-a primeiro.

Uso:
    python fetchers/statusinvest_scraper.py            # default ITSA4
    python fetchers/statusinvest_scraper.py PRIO3
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import requests
import sys

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from fetchers.cache_policy import is_fresh, now_iso  # noqa: E402

ROOT = _ROOT
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"

BASE = "https://statusinvest.com.br"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

PAIR_RE = re.compile(
    r'<h3[^>]*class="title[^"]*"[^>]*>([^<]+)</h3>'
    r'.*?<strong[^>]*class="value[^"]*"[^>]*>([^<]+)</strong>',
    re.S,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False)
    with (LOG_DIR / "statusinvest_scraper.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _to_float(s: str) -> float | None:
    """'8,54%' -> 0.0854 ; '1,78' -> 1.78 ; '-' -> None."""
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


def fetch_indicators(ticker: str) -> dict:
    url = f"{BASE}/acoes/{ticker.lower()}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    html = r.text
    pairs: dict[str, str] = {}
    for m in PAIR_RE.finditer(html):
        label = unescape(re.sub(r"\s+", " ", m.group(1)).strip())
        value = m.group(2).strip()
        # primeiro vence — o site repete alguns labels em secções diferentes
        pairs.setdefault(label, value)
    return pairs


def fetch_dividend_history(ticker: str) -> list[dict]:
    url = f"{BASE}/acao/companytickerprovents"
    r = requests.get(
        url,
        params={"ticker": ticker, "chartProventsType": "2"},
        headers={**HEADERS, "X-Requested-With": "XMLHttpRequest"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("assetEarningsYearlyModels") or []


def compute_streak(yearly: list[dict]) -> int | None:
    """Conta anos consecutivos a contar do mais recente para trás
    em que o valor pago foi > 0. Ignora o ano corrente se ainda
    não houve pagamento (rank == ano actual com value 0)."""
    if not yearly:
        return None
    by_year = {int(d["rank"]): float(d["value"] or 0) for d in yearly}
    current_year = datetime.now().year
    years_desc = sorted(by_year.keys(), reverse=True)
    if years_desc and years_desc[0] == current_year and by_year[current_year] == 0:
        years_desc = years_desc[1:]
    streak = 0
    expected = years_desc[0] if years_desc else None
    for y in years_desc:
        if y != expected or by_year[y] <= 0:
            break
        streak += 1
        expected -= 1
    return streak


def parse_indicators(pairs: dict) -> dict:
    """Mapeia labels do Status Invest para campos da tabela fundamentals."""
    return {
        "dy":              _to_float(pairs.get("D.Y") or pairs.get("Dividend Yield")),
        "pe":              _to_float(pairs.get("P/L")),
        "pb":              _to_float(pairs.get("P/VP")),
        "bvps":            _to_float(pairs.get("VPA")),
        "eps":             _to_float(pairs.get("LPA")),
        "roe":             _to_float(pairs.get("ROE")),
        "net_debt_ebitda": _to_float(pairs.get("Dív. líquida/EBITDA")),
    }


def latest_period_end(conn: sqlite3.Connection, ticker: str) -> str | None:
    row = conn.execute(
        "SELECT period_end FROM fundamentals WHERE ticker=? "
        "ORDER BY period_end DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    return row[0] if row else None


def update_fundamentals(conn: sqlite3.Connection, ticker: str, fields: dict, streak: int | None) -> str:
    period = latest_period_end(conn, ticker) or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # COALESCE: só sobrescreve se o scraper trouxe valor; preserva o que brapi pôs.
    conn.execute(
        """INSERT INTO fundamentals
             (ticker, period_end, eps, bvps, roe, pe, pb, dy,
              net_debt_ebitda, dividend_streak_years, is_aristocrat)
           VALUES (?,?,?,?,?,?,?,?,?,?,NULL)
           ON CONFLICT(ticker, period_end) DO UPDATE SET
             eps                   = COALESCE(excluded.eps, fundamentals.eps),
             bvps                  = COALESCE(excluded.bvps, fundamentals.bvps),
             roe                   = COALESCE(excluded.roe, fundamentals.roe),
             pe                    = COALESCE(excluded.pe, fundamentals.pe),
             pb                    = COALESCE(excluded.pb, fundamentals.pb),
             dy                    = COALESCE(excluded.dy, fundamentals.dy),
             net_debt_ebitda       = COALESCE(excluded.net_debt_ebitda, fundamentals.net_debt_ebitda),
             dividend_streak_years = COALESCE(excluded.dividend_streak_years, fundamentals.dividend_streak_years)""",
        (
            ticker, period,
            fields.get("eps"), fields.get("bvps"), fields.get("roe"),
            fields.get("pe"), fields.get("pb"), fields.get("dy"),
            fields.get("net_debt_ebitda"), streak,
        ),
    )
    return period


def upsert_dividends_annual(conn: sqlite3.Connection, ticker: str, yearly: list[dict]) -> int:
    n = 0
    for d in yearly:
        year = int(d.get("rank") or 0)
        amount = float(d.get("value") or 0)
        if year <= 0:
            continue
        conn.execute(
            """INSERT INTO dividends_annual (ticker, year, amount) VALUES (?,?,?)
               ON CONFLICT(ticker, year) DO UPDATE SET amount=excluded.amount""",
            (ticker, year, amount),
        )
        n += 1
    return n


def run(ticker: str = "ITSA4", force: bool = False) -> None:
    # Cache check: se o snapshot corrente já foi buscado hoje, skip.
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT fetched_at FROM fundamentals WHERE ticker=? "
            "ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        ).fetchone()
    if not force and row and is_fresh(row[0], "fundamental_snapshot"):
        _log({"event": "scrape_skip_fresh", "ticker": ticker, "fetched_at": row[0]})
        return

    _log({"event": "scrape_start", "ticker": ticker})
    pairs = fetch_indicators(ticker)
    fields = parse_indicators(pairs)
    yearly = fetch_dividend_history(ticker)
    streak = compute_streak(yearly)

    with sqlite3.connect(DB_PATH) as conn:
        period = update_fundamentals(conn, ticker, fields, streak)
        n_div = upsert_dividends_annual(conn, ticker, yearly)
        conn.execute(
            "UPDATE fundamentals SET fetched_at=? WHERE ticker=? AND period_end=?",
            (now_iso(), ticker, period),
        )
        conn.commit()

    _log({
        "event": "scraped",
        "ticker": ticker,
        "period_end": period,
        "fields": fields,
        "dividend_streak_years": streak,
        "dividend_years_persisted": n_div,
    })


if __name__ == "__main__":
    tk = sys.argv[1] if len(sys.argv) > 1 else "ITSA4"
    run(tk)
