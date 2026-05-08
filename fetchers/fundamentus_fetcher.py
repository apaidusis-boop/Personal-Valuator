"""fundamentus_fetcher — scrape fundamentos de fundamentus.com.br.

3ª fonte BR para triangulação (yfinance ↔ CVM filings ↔ Fundamentus).
Phase LL Sprint 1.5.

Fundamentus aggregates Brazilian listed-company fundamentals from CVM
filings + market data, surfaced on a single HTML page per ticker. No
auth, no rate limit visible (still throttled to 2s between requests
to be polite — personal use).

URL pattern:
    https://www.fundamentus.com.br/detalhes.php?papel=<TICKER>

HTML structure (relevant snippet):
    <span class="txt">LABEL</span></td>
    <td class="data wN"><span class="txt">VALUE</span></td>

Fields captured (BR convention, comma decimal):
    Cotação, P/L, P/VP, LPA, VPA, Div. Yield, ROE, ROIC,
    Marg. Líquida, Marg. EBIT, Liq. Corrente,
    Dív. Bruta/Patrim., Dív. Líquida/EBITDA,
    Patrim. Líq, Receita Líquida, Lucro Líquido (12m)

Persisted to new table `fundamentals_scraped` with provenance:
    source='fundamentus', scraped_at=ISO timestamp.

CLI:
    python -m fetchers.fundamentus_fetcher BBDC4
    python -m fetchers.fundamentus_fetcher --holdings   (default)
    python -m fetchers.fundamentus_fetcher --tickers BBDC4,ITSA4,VALE3
    python -m fetchers.fundamentus_fetcher --show BBDC4
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ii-fundamentus-fetcher/1.0"
BASE_URL = "https://www.fundamentus.com.br/detalhes.php?papel={ticker}"
THROTTLE_SEC = 2.0   # be polite

SCHEMA = """
CREATE TABLE IF NOT EXISTS fundamentals_scraped (
    ticker          TEXT NOT NULL,
    source          TEXT NOT NULL,
    scraped_at      TEXT NOT NULL,
    -- Per-share / valuation
    price           REAL,
    pe              REAL,
    pb              REAL,
    eps             REAL,
    bvps            REAL,
    dy              REAL,
    -- Profitability
    roe             REAL,
    roic            REAL,
    net_margin      REAL,
    ebit_margin     REAL,
    -- Leverage / solvency
    debt_to_equity  REAL,
    nd_ebitda       REAL,
    current_ratio   REAL,
    -- Absolute (BRL thousands except market cap which is BRL)
    market_cap      REAL,
    revenue_ttm     REAL,
    net_income_ttm  REAL,
    equity          REAL,
    -- Provenance
    raw_json        TEXT,
    PRIMARY KEY (ticker, source, scraped_at)
);
CREATE INDEX IF NOT EXISTS idx_fs_ticker ON fundamentals_scraped(ticker);
"""


def _ensure_schema() -> None:
    with sqlite3.connect(DB_BR) as c:
        c.executescript(SCHEMA)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _br_to_float(s: str | None) -> float | None:
    """'1.234,56' → 1234.56 ; '12,3%' → 0.123 ; 'N/A' → None"""
    if s is None:
        return None
    t = s.strip()
    if not t or t in ("-", "—", "N/A"):
        return None
    is_pct = t.endswith("%")
    t = t.replace("%", "").strip()
    # BR format uses '.' as thousand sep, ',' as decimal
    t = t.replace(".", "").replace(",", ".")
    try:
        v = float(t)
    except ValueError:
        return None
    if is_pct:
        v = v / 100.0
    return v


# Patterns: each captures the value that comes right after the labelled cell.
# We anchor on the label's closing </span></td> and the next data cell.
_LABEL_VALUE_RE = re.compile(
    r'<span class="txt">{label}</span></td>\s*'
    r'<td[^>]*class="data[^"]*"[^>]*>\s*<span[^>]*class="[^"]*"[^>]*>([^<]*)</span>',
    re.IGNORECASE | re.DOTALL,
)


def _extract(html: str, label: str) -> str | None:
    """Find the value following a label-cell in Fundamentus HTML."""
    pattern = re.compile(
        r'<span class="txt">' + re.escape(label) + r'</span></td>\s*'
        r'<td[^>]*class="data[^"]*"[^>]*>\s*<span[^>]*>([^<]*)</span>',
        re.IGNORECASE | re.DOTALL,
    )
    m = pattern.search(html)
    if not m:
        return None
    return m.group(1).strip()


def fetch_one(ticker: str) -> dict:
    """Scrape one ticker. Returns dict ready to persist (or empty if no data)."""
    url = BASE_URL.format(ticker=ticker.upper())
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
    except (urllib.error.URLError, TimeoutError) as e:
        return {"ticker": ticker, "_error": str(e)}

    # Fundamentus serves ISO-8859-1
    html = raw.decode("iso-8859-1")

    # Page returns 200 even for invalid tickers; check for marker
    if "Papel inv" in html or len(html) < 5000:
        return {"ticker": ticker, "_error": "ticker_not_found_or_empty_page"}

    raw_fields = {
        "price":          _extract(html, "Cota&ccedil;&atilde;o") or _extract(html, "Cotação"),
        "pe":             _extract(html, "P/L"),
        "pb":             _extract(html, "P/VP"),
        "eps":            _extract(html, "LPA"),
        "bvps":           _extract(html, "VPA"),
        "dy":             _extract(html, "Div. Yield"),
        "roe":            _extract(html, "ROE"),
        "roic":           _extract(html, "ROIC"),
        "net_margin":     _extract(html, "Marg. L&iacute;quida") or _extract(html, "Marg. Líquida"),
        "ebit_margin":    _extract(html, "Marg. EBIT"),
        "current_ratio":  _extract(html, "Liq. Corrente"),
        "debt_to_equity": _extract(html, "D&iacute;v. Bruta/ Patrim.") or _extract(html, "Dív. Bruta/ Patrim."),
        "nd_ebitda":      _extract(html, "D&iacute;v. L&iacute;quida/EBITDA") or _extract(html, "Dív. Líquida/EBITDA"),
        "market_cap":     _extract(html, "Valor de mercado"),
        "revenue_ttm":    _extract(html, "Receita L&iacute;quida"),
        "net_income_ttm": _extract(html, "Lucro L&iacute;quido"),
        "equity":         _extract(html, "Patrim. L&iacute;q") or _extract(html, "Patrim. Líq"),
    }

    parsed: dict = {"ticker": ticker.upper(), "source": "fundamentus",
                    "scraped_at": _now_iso()}
    for k, v in raw_fields.items():
        parsed[k] = _br_to_float(v)
    parsed["raw_json"] = json.dumps(raw_fields, ensure_ascii=False)
    return parsed


def persist(row: dict) -> None:
    if "_error" in row:
        return
    _ensure_schema()
    cols = ("ticker", "source", "scraped_at", "price", "pe", "pb", "eps", "bvps",
            "dy", "roe", "roic", "net_margin", "ebit_margin", "debt_to_equity",
            "nd_ebitda", "current_ratio", "market_cap", "revenue_ttm",
            "net_income_ttm", "equity", "raw_json")
    placeholders = ",".join("?" * len(cols))
    with sqlite3.connect(DB_BR) as c:
        c.execute(
            f"INSERT OR REPLACE INTO fundamentals_scraped ({','.join(cols)}) "
            f"VALUES ({placeholders})",
            tuple(row.get(k) for k in cols),
        )
        c.commit()


def latest(ticker: str) -> dict | None:
    _ensure_schema()
    with sqlite3.connect(DB_BR) as c:
        c.row_factory = sqlite3.Row
        r = c.execute(
            """SELECT * FROM fundamentals_scraped
               WHERE ticker=? AND source='fundamentus'
               ORDER BY scraped_at DESC LIMIT 1""",
            (ticker.upper(),),
        ).fetchone()
    return dict(r) if r else None


def _list_holdings() -> list[str]:
    with sqlite3.connect(DB_BR) as c:
        rows = c.execute(
            "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
        ).fetchall()
    return sorted({r[0] for r in rows})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true", help="(default)")
    g.add_argument("--tickers", help="comma-separated list")
    ap.add_argument("--show", metavar="TICKER", help="print latest scraped row for TICKER and exit")
    args = ap.parse_args()

    if args.show:
        r = latest(args.show)
        if not r:
            print(f"{args.show}: no scraped data yet")
            return 1
        print(f"\n=== {args.show} fundamentus scrape ===")
        for k in ("scraped_at", "price", "pe", "pb", "eps", "bvps", "dy", "roe",
                  "roic", "net_margin", "ebit_margin", "debt_to_equity",
                  "nd_ebitda", "current_ratio", "market_cap", "revenue_ttm",
                  "net_income_ttm", "equity"):
            v = r.get(k)
            print(f"  {k:<18} {v}")
        return 0

    if args.tickers:
        targets = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    elif args.ticker:
        targets = [args.ticker.upper()]
    else:
        targets = _list_holdings()

    print(f"Scraping Fundamentus for {len(targets)} ticker(s)...")
    ok = err = 0
    for i, tk in enumerate(targets):
        if i > 0:
            time.sleep(THROTTLE_SEC)
        r = fetch_one(tk)
        if "_error" in r:
            err += 1
            print(f"  {tk:<8} ERROR — {r['_error']}")
            continue
        persist(r)
        ok += 1
        print(f"  {tk:<8} price={r.get('price')} P/L={r.get('pe')} P/VP={r.get('pb')} "
              f"LPA={r.get('eps')} VPA={r.get('bvps')} ROE={(r.get('roe') or 0)*100:.1f}%")
    print(f"\nPersisted {ok} | errors {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
