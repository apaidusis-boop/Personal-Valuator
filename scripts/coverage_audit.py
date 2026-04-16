"""Audit de cobertura de dados por ticker.

Lê as DBs BR e US e reporta, por ticker, que campos críticos estão
NULL ou em falta. Útil para detectar gaps pós-populate e antes de
correr scoring/valuation.

Não toca na rede. Só leitura.

Uso:
    python scripts/coverage_audit.py              # BR
    python scripts/coverage_audit.py --market us  # US
    python scripts/coverage_audit.py --json       # output JSON (para CI)
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

# Campos que devem estar preenchidos para cada tabela.
# Cada item: (nome_display, sql_expression).
STOCK_CHECKS = {
    "company": [
        ("name",    "c.name IS NOT NULL AND c.name != ''"),
        ("sector",  "c.sector IS NOT NULL AND c.sector != ''"),
    ],
    "prices": [
        ("has_prices",      "p.cnt > 0"),
        ("prices_recent",   "p.max_date >= date('now', '-7 days')"),
        ("prices_depth",    "p.cnt >= 100"),
    ],
    "fundamentals": [
        ("eps",             "f.eps IS NOT NULL"),
        ("bvps",            "f.bvps IS NOT NULL"),
        ("roe",             "f.roe IS NOT NULL"),
        ("pe",              "f.pe IS NOT NULL"),
        ("pb",              "f.pb IS NOT NULL"),
        ("dy",              "f.dy IS NOT NULL"),
        ("net_debt_ebitda", "f.net_debt_ebitda IS NOT NULL"),
        ("dividend_streak", "f.dividend_streak_years IS NOT NULL"),
    ],
    "dividends_annual": [
        ("has_div_annual",  "da.cnt > 0"),
        ("div_years_depth", "da.cnt >= 3"),
    ],
    "scores": [
        ("has_score",       "s.run_date IS NOT NULL"),
    ],
    "valuations": [
        ("has_valuation",   "v.fair_value IS NOT NULL"),
    ],
    "events": [
        ("has_cvm_events",  "e.cnt > 0"),
    ],
}

FII_CHECKS = {
    "company": [
        ("name",    "c.name IS NOT NULL AND c.name != ''"),
    ],
    "fii_fundamentals": [
        ("price",               "ff.price IS NOT NULL"),
        ("vpa",                 "ff.vpa IS NOT NULL"),
        ("pvp",                 "ff.pvp IS NOT NULL"),
        ("dy_12m",              "ff.dy_12m IS NOT NULL"),
        ("distribution_streak", "ff.distribution_streak_months IS NOT NULL"),
        ("adtv_daily",          "ff.adtv_daily IS NOT NULL"),
        ("segment_anbima",      "ff.segment_anbima IS NOT NULL"),
    ],
    "scores": [
        ("has_score",           "s.run_date IS NOT NULL"),
    ],
}


def _audit_stocks(conn: sqlite3.Connection) -> list[dict]:
    """Audita cada ticker stock (não FII) na tabela companies."""
    tickers = [r[0] for r in conn.execute(
        "SELECT ticker FROM companies WHERE ticker NOT LIKE '%11' ORDER BY ticker"
    ).fetchall()]

    results = []
    for ticker in tickers:
        row = {"ticker": ticker, "type": "stock", "ok": [], "missing": [], "warnings": []}

        # company
        c = conn.execute("SELECT name, sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
        if c:
            _check(row, "name", c[0] is not None and c[0] != "")
            _check(row, "sector", c[1] is not None and c[1] != "")

        # prices
        p = conn.execute(
            "SELECT COUNT(*), MAX(date) FROM prices WHERE ticker=?", (ticker,)
        ).fetchone()
        _check(row, "has_prices", (p[0] or 0) > 0)
        _check(row, "prices_recent", p[1] is not None and p[1] >= _days_ago(7),
               warn_only=True)
        _check(row, "prices_depth", (p[0] or 0) >= 100, warn_only=True)

        # fundamentals (latest)
        f = conn.execute(
            """SELECT eps, bvps, roe, pe, pb, dy, net_debt_ebitda, dividend_streak_years
               FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if f:
            for i, name in enumerate(["eps", "bvps", "roe", "pe", "pb", "dy",
                                       "net_debt_ebitda", "dividend_streak"]):
                _check(row, name, f[i] is not None)
        else:
            row["missing"].append("fundamentals_row")

        # dividends_annual
        da = conn.execute(
            "SELECT COUNT(*) FROM dividends_annual WHERE ticker=?", (ticker,)
        ).fetchone()
        _check(row, "has_div_annual", (da[0] or 0) > 0)
        _check(row, "div_years_depth", (da[0] or 0) >= 3, warn_only=True)

        # scores
        s = conn.execute(
            "SELECT run_date FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        _check(row, "has_score", s is not None)

        # valuations
        v = conn.execute(
            "SELECT fair_value FROM valuations WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        _check(row, "has_valuation", v is not None and v[0] is not None)

        # events
        e = conn.execute(
            "SELECT COUNT(*) FROM events WHERE ticker=?", (ticker,)
        ).fetchone()
        _check(row, "has_cvm_events", (e[0] or 0) > 0, warn_only=True)

        results.append(row)
    return results


def _audit_fiis(conn: sqlite3.Connection) -> list[dict]:
    """Audita cada ticker FII na tabela companies."""
    tickers = [r[0] for r in conn.execute(
        "SELECT ticker FROM companies WHERE ticker LIKE '%11' ORDER BY ticker"
    ).fetchall()]

    results = []
    for ticker in tickers:
        row = {"ticker": ticker, "type": "fii", "ok": [], "missing": [], "warnings": []}

        c = conn.execute("SELECT name FROM companies WHERE ticker=?", (ticker,)).fetchone()
        _check(row, "name", c is not None and c[0] is not None and c[0] != "")

        ff = conn.execute(
            """SELECT price, vpa, pvp, dy_12m, distribution_streak_months,
                      adtv_daily, segment_anbima
               FROM fii_fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        if ff:
            for i, name in enumerate(["price", "vpa", "pvp", "dy_12m",
                                       "distribution_streak", "adtv_daily",
                                       "segment_anbima"]):
                _check(row, name, ff[i] is not None)
        else:
            row["missing"].append("fii_fundamentals_row")

        s = conn.execute(
            "SELECT run_date FROM scores WHERE ticker=? ORDER BY run_date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        _check(row, "has_score", s is not None)

        results.append(row)
    return results


def _check(row: dict, name: str, ok: bool, warn_only: bool = False) -> None:
    if ok:
        row["ok"].append(name)
    elif warn_only:
        row["warnings"].append(name)
    else:
        row["missing"].append(name)


def _days_ago(n: int) -> str:
    from datetime import datetime, timedelta
    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")


def run(market: str = "br") -> list[dict]:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as conn:
        stocks = _audit_stocks(conn)
        fiis = _audit_fiis(conn) if market == "br" else []
    return stocks + fiis


def print_report(results: list[dict]) -> None:
    total_ok = 0
    total_missing = 0
    total_warn = 0

    for r in results:
        n_ok = len(r["ok"])
        n_miss = len(r["missing"])
        n_warn = len(r["warnings"])
        total_ok += n_ok
        total_missing += n_miss
        total_warn += n_warn

        if n_miss == 0 and n_warn == 0:
            status = "[OK]"
        elif n_miss == 0:
            status = "[WARN]"
        else:
            status = "[GAP]"

        fields_total = n_ok + n_miss + n_warn
        pct = (n_ok / fields_total * 100) if fields_total else 0
        line = f"  {status:6} {r['ticker']:8} ({r['type']:5})  {n_ok}/{fields_total} ({pct:.0f}%)"
        if r["missing"]:
            line += f"  missing: {', '.join(r['missing'])}"
        if r["warnings"]:
            line += f"  warn: {', '.join(r['warnings'])}"
        print(line)

    print(f"\n  TOTAL: {total_ok} ok, {total_missing} missing, {total_warn} warnings"
          f"  ({len(results)} tickers)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit de cobertura de dados por ticker")
    ap.add_argument("--market", choices=["br", "us"], default="br")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    results = run(args.market)
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\n=== Coverage Audit ({args.market.upper()}) ===\n")
        print_report(results)


if __name__ == "__main__":
    main()
