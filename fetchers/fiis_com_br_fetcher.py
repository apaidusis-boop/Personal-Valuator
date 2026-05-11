"""fiis_com_br_fetcher — scrape FII fundamentals from fiis.com.br.

Phase LL Sprint 1.5b. Specialized FII source — depth that Fundamentus +
Status Invest don't match (DY mensal trail, vacância imóvel-a-imóvel,
gestor track record, CRI rating composition for paper FIIs).

URL pattern: https://fiis.com.br/<ticker_lower>/

HTML structure (key indicators):
    <div class="indicators__box">
        <p><b>VALUE</b></p>            ← captured
        <p>LABEL</p>                   ← matched
    </div>

Some indicators have prefixes:
    <p><small>R$</small> <b>2,0 B</b></p>  → "2,0 B" parsed as 2.0e9

Fields captured:
    Cotação atual         → price
    P/VP                  → pb
    Patrimônio Líquido    → equity (BRL)
    Número de cotas       → shares
    Dividend Yield        → dy_12m (fraction)
    Último rendimento     → last_dividend_brl
    Patrimônio por cota   → vpa
    Vacância              → vacancy_pct
    Gestor                → manager
    Tipo                  → fund_type (Tijolo / Papel / Híbrido / FOF)
    Segmento              → segment

Persisted to new table `fii_extras` in BR DB. Throttled 2s.

CLI:
    python -m fetchers.fiis_com_br_fetcher KNHF11
    python -m fetchers.fiis_com_br_fetcher --holdings   (default)
    python -m fetchers.fiis_com_br_fetcher --tickers KNHF11,BTLG11,XPML11
    python -m fetchers.fiis_com_br_fetcher KNHF11 --show
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
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ii-fiis-fetcher/1.0"
BASE_URL = "https://fiis.com.br/{ticker_lower}/"
THROTTLE_SEC = 2.0

SCHEMA = """
CREATE TABLE IF NOT EXISTS fii_extras (
    ticker             TEXT NOT NULL,
    source             TEXT NOT NULL,
    scraped_at         TEXT NOT NULL,
    -- Valuation
    price              REAL,
    pb                 REAL,                    -- P/VP
    vpa                REAL,                    -- Patrimônio por cota
    market_cap         REAL,
    equity             REAL,                    -- Patrimônio Líquido
    shares             REAL,                    -- Número de cotas
    -- Yield
    dy_12m             REAL,                    -- Dividend Yield 12m (fraction)
    last_dividend      REAL,                    -- R$/cota último mês
    -- FII-specific
    fund_type          TEXT,                    -- Tijolo / Papel / Híbrido / FOF
    segment            TEXT,                    -- Logística / Shopping / Corporativo / etc
    manager            TEXT,                    -- gestor
    vacancy_pct        REAL,                    -- vacância física (Tijolo only)
    n_imoveis          INTEGER,                 -- número de imóveis
    -- Provenance
    raw_json           TEXT,
    PRIMARY KEY (ticker, source, scraped_at)
);
CREATE INDEX IF NOT EXISTS idx_fe_ticker ON fii_extras(ticker);
"""


def _ensure_schema() -> None:
    with sqlite3.connect(DB_BR) as c:
        c.executescript(SCHEMA)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _br_to_float(s: str | None) -> float | None:
    """'1.234,56' → 1234.56 ; '12,3%' → 0.123 ; '2,0 B' → 2_000_000_000"""
    if s is None:
        return None
    t = s.strip()
    if not t or t in ("-", "—", "N/A", ""):
        return None
    is_pct = t.endswith("%")
    t = t.replace("%", "").strip()
    # Magnitude suffix
    mult = 1.0
    if t.endswith("B"):
        mult = 1e9
        t = t[:-1].strip()
    elif t.endswith("M"):
        mult = 1e6
        t = t[:-1].strip()
    elif t.endswith("k") or t.endswith("K"):
        mult = 1e3
        t = t[:-1].strip()
    elif t.endswith("Mi"):
        mult = 1e6
        t = t[:-2].strip()
    elif t.endswith("Bi"):
        mult = 1e9
        t = t[:-2].strip()
    # BR format: '.' thousand sep, ',' decimal
    t = t.replace(".", "").replace(",", ".")
    try:
        v = float(t) * mult
    except ValueError:
        return None
    if is_pct:
        v = v / 100.0
    return v


def _extract_indicator(html: str, label: str) -> str | None:
    """Find the value that PRECEDES the labelled <p> tag (indicators__box layout).

    Pattern A (standard):  <p><b>VALUE</b></p><p>LABEL</p>
    Pattern B (R$ prefix): <p><small>R$</small> <b>VALUE</b></p><p>LABEL</p>
    Pattern C (% suffix):  <p><b>VALUE</b> <small>%</small></p><p>LABEL</p>
    Pattern D (with unit): <p><b>VALUE</b> <small>UNIT</small></p><p>LABEL</p>
                           e.g. small="B" or "M" → magnitude suffix

    Returns concatenated VALUE+suffix when % or magnitude are present so the
    BR parser knows to apply percentage / magnitude mult.
    """
    # Standard: <b>...</b>, optional preceding small (R$), optional trailing small (% or magnitude)
    pat = re.compile(
        r'<p>\s*(?:<small>[^<]*</small>\s*)?<b>([^<]+)</b>'
        r'(?:\s*<small>([^<]*)</small>)?\s*</p>\s*'
        r'<p>\s*' + re.escape(label) + r'\s*</p>',
        re.IGNORECASE | re.DOTALL,
    )
    m = pat.search(html)
    if not m:
        return None
    value = m.group(1).strip()
    suffix = (m.group(2) or "").strip()
    # Append suffix only if it's a unit/magnitude indicator
    if suffix in ("%", "B", "M", "k", "K", "Mi", "Bi"):
        return f"{value}{suffix}"
    return value


def _extract_label_value_p(html: str, label: str) -> str | None:
    """Layout C: <p><span>LABEL</span><b>VALUE</b></p>
    Used for Tipo, Segmento, Gestor, Patrimônio (structured info block)."""
    pat = re.compile(
        r'<p>\s*<span>\s*' + re.escape(label) + r'\s*</span>\s*<b>([^<]+)</b>\s*</p>',
        re.IGNORECASE | re.DOTALL,
    )
    m = pat.search(html)
    return m.group(1).strip() if m else None


def _extract_text(html: str, label: str) -> str | None:
    """Like _extract_indicator but value is plain text in <p> (no <b>)."""
    pat = re.compile(
        r'<p>([^<]+)</p>\s*<p>\s*' + re.escape(label) + r'\s*</p>',
        re.IGNORECASE | re.DOTALL,
    )
    m = pat.search(html)
    return m.group(1).strip() if m else None


def fetch_one(ticker: str) -> dict:
    url = BASE_URL.format(ticker_lower=ticker.lower())
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        return {"ticker": ticker, "_error": f"http_{e.code}"}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"ticker": ticker, "_error": str(e)}

    html = raw.decode("utf-8", errors="replace")
    if "Página não encontrada" in html or len(html) < 5000:
        return {"ticker": ticker, "_error": "page_not_found"}

    raw_fields = {
        # indicators__box layout (value <b> precedes label <p>)
        "pb":           _extract_indicator(html, "P/VP"),
        "dy_12m":       _extract_indicator(html, "Dividend Yield"),
        "last_dividend": _extract_indicator(html, "Último Rendimento") or _extract_indicator(html, "Último rendimento"),
        "vacancy_pct":  _extract_indicator(html, "Vacância") or _extract_indicator(html, "Vacância Física"),
        "equity":       _extract_indicator(html, "Patrimônio Líquido"),
        # info-block layout (<span>LABEL</span><b>VALUE</b>)
        "shares":       _extract_label_value_p(html, "Número de Cotas") or _extract_label_value_p(html, "Número de cotas"),
        "vpa":          _extract_label_value_p(html, "Valor Patrimonial p/Cota") or _extract_label_value_p(html, "VPA"),
    }
    text_fields = {
        "fund_type":    _extract_label_value_p(html, "Tipo ANBIMA") or _extract_label_value_p(html, "Tipo"),
        "segment":      _extract_label_value_p(html, "Segmento ANBIMA") or _extract_label_value_p(html, "Segmento"),
        "manager":      _extract_label_value_p(html, "Gestora") or _extract_label_value_p(html, "Gestor"),
    }

    out: dict = {"ticker": ticker.upper(), "source": "fiis_com_br",
                 "scraped_at": _now_iso()}
    for k, v in raw_fields.items():
        out[k] = _br_to_float(v)
    out.update({k: (v.strip() if v else None) for k, v in text_fields.items()})
    out["raw_json"] = json.dumps({**raw_fields, **text_fields}, ensure_ascii=False)
    return out


def persist(row: dict) -> None:
    if "_error" in row:
        return
    _ensure_schema()
    cols = ("ticker", "source", "scraped_at", "price", "pb", "vpa", "market_cap",
            "equity", "shares", "dy_12m", "last_dividend", "fund_type",
            "segment", "manager", "vacancy_pct", "n_imoveis", "raw_json")
    placeholders = ",".join("?" * len(cols))
    with sqlite3.connect(DB_BR) as c:
        c.execute(
            f"INSERT OR REPLACE INTO fii_extras ({','.join(cols)}) VALUES ({placeholders})",
            tuple(row.get(k) for k in cols),
        )
        c.commit()


def latest(ticker: str) -> dict | None:
    _ensure_schema()
    with sqlite3.connect(DB_BR) as c:
        c.row_factory = sqlite3.Row
        r = c.execute(
            """SELECT * FROM fii_extras WHERE ticker=? AND source='fiis_com_br'
               ORDER BY scraped_at DESC LIMIT 1""",
            (ticker.upper(),),
        ).fetchone()
    return dict(r) if r else None


def _list_fii_holdings() -> list[str]:
    """Return active BR FII tickers (sector ∈ {Tijolo, Papel, Logística, etc})."""
    fii_sectors = {"Logística", "Logistica", "Shopping", "Papel (CRI)", "Híbrido",
                   "Hibrido", "Corporativo", "Tijolo", "Residencial", "Agro",
                   "Fundo de Fundos", "Real Estate"}
    with sqlite3.connect(DB_BR) as c:
        rows = c.execute(
            """SELECT DISTINCT pp.ticker, c.sector
               FROM portfolio_positions pp
               LEFT JOIN companies c ON c.ticker = pp.ticker
               WHERE pp.active=1"""
        ).fetchall()
    return sorted({r[0] for r in rows if r[1] in fii_sectors})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("ticker", nargs="?")
    g.add_argument("--holdings", action="store_true", help="(default — FII holdings only)")
    g.add_argument("--tickers", help="comma-separated list")
    ap.add_argument("--show", action="store_true",
                    help="(with ticker) print latest scraped row")
    args = ap.parse_args()

    if args.show and args.ticker:
        r = latest(args.ticker)
        if not r:
            print(f"{args.ticker}: no scraped data yet")
            return 1
        print(f"\n=== {args.ticker} fiis.com.br ===")
        for k in ("scraped_at", "price", "pb", "vpa", "market_cap", "equity",
                  "shares", "dy_12m", "last_dividend", "fund_type", "segment",
                  "manager", "vacancy_pct"):
            v = r.get(k)
            print(f"  {k:<20} {v}")
        return 0

    if args.tickers:
        targets = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    elif args.ticker:
        targets = [args.ticker.upper()]
    else:
        targets = _list_fii_holdings()

    if not targets:
        print("No FII targets — pass ticker explicitly or check holdings sector classification.")
        return 1

    print(f"Scraping fiis.com.br for {len(targets)} FII(s)...")
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
        price_s = f"{r.get('price'):.2f}" if r.get("price") else "—"
        pb_s = f"{r.get('pb'):.2f}" if r.get("pb") else "—"
        dy_s = f"{(r.get('dy_12m') or 0)*100:.1f}%" if r.get("dy_12m") else "—"
        vac_s = f"{(r.get('vacancy_pct') or 0)*100:.1f}%" if r.get("vacancy_pct") is not None else "—"
        ftype = (r.get("fund_type") or "—")[:12]
        print(f"  {tk:<8} price={price_s:<8} P/VP={pb_s:<5} DY12m={dy_s:<6} "
              f"vac={vac_s:<6} type={ftype}")
    print(f"\nPersisted {ok} | errors {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
