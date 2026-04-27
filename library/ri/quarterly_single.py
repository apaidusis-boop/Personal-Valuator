"""Single-quarter delta — resolve YTD artifact dos ITRs CVM.

Problema:
  ITRs CVM são acumulados YTD: Q3 ITR = 9 meses YTD, Q2 = 6 meses, Q1 = 3 meses.
  DFP é o ano completo (Jan-Dec).

Solução: derivar o "single-Q" subtraindo períodos.
  Q1 single = ITR Q1                              (já 3 meses)
  Q2 single = ITR Q2 - ITR Q1                     (6m - 3m)
  Q3 single = ITR Q3 - ITR Q2                     (9m - 6m)
  Q4 single = DFP - ITR Q3                        (12m - 9m)

Métricas de FLUXO (revenue, ebit, net_income, fco, fci, fcf_proxy, equity_method)
são SUBTRACT-eable. Métricas de STOCK (debt_total, equity, total_assets) são
SNAPSHOT — não subtraem; usar valor da data como está.

Output: tabela `quarterly_single` (idempotente, REPLACE).

Uso:
    python -m library.ri.quarterly_single build
    python -m library.ri.quarterly_single show VALE3
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "data" / "br_investments.db"

# Métricas que ACUMULAM (subtract-able)
FLOW_METRICS = ["revenue", "gross_profit", "ebit", "pretax_income",
                "net_income", "equity_method", "fco", "fci", "fcf_proxy"]
# Métricas SNAPSHOT (não subtrair, usar valor da data)
STOCK_METRICS = ["total_assets", "current_assets", "current_liab",
                 "total_liab", "equity", "debt_st", "debt_lt", "debt_total"]
# Computed após single-Q derivation
COMPUTED = ["gross_margin", "ebit_margin", "net_margin"]

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS quarterly_single (
    ticker          TEXT NOT NULL,
    period_end      TEXT NOT NULL,
    fiscal_quarter  TEXT NOT NULL,        -- '2024Q1', '2024Q2', etc.
    derived_from    TEXT NOT NULL,        -- 'ITR' | 'DFP' | 'DFP-ITR' (Q4)
    -- flow (single-quarter)
    revenue         REAL,
    gross_profit    REAL,
    ebit            REAL,
    pretax_income   REAL,
    net_income      REAL,
    equity_method   REAL,
    fco             REAL,
    fci             REAL,
    fcf_proxy       REAL,
    -- snapshot (period-end stock)
    total_assets    REAL,
    current_assets  REAL,
    current_liab    REAL,
    total_liab      REAL,
    equity          REAL,
    debt_st         REAL,
    debt_lt         REAL,
    debt_total      REAL,
    -- computed margins (single-Q)
    gross_margin    REAL,
    ebit_margin     REAL,
    net_margin      REAL,
    PRIMARY KEY (ticker, period_end)
);

CREATE INDEX IF NOT EXISTS idx_qs_ticker ON quarterly_single(ticker, fiscal_quarter);
"""


def ensure_schema() -> None:
    with sqlite3.connect(DB) as c:
        c.executescript(SCHEMA)
        c.commit()


def _quarter_label(period_end: str) -> str:
    """2024-09-30 → '2024Q3'."""
    y, m, _ = period_end.split("-")
    q = {"03": "1", "06": "2", "09": "3", "12": "4"}.get(m, "?")
    return f"{y}Q{q}"


def _periods_by_year(c: sqlite3.Connection, ticker: str) -> dict[int, dict[str, dict]]:
    """Returns {year: {'Q1': row, 'Q2': row, 'Q3': row, 'DFP': row}}."""
    out: dict[int, dict[str, dict]] = {}
    c.row_factory = sqlite3.Row
    rows = c.execute(
        "SELECT * FROM quarterly_history WHERE ticker=? ORDER BY period_end",
        (ticker,),
    ).fetchall()
    for r in rows:
        period = r["period_end"]
        if not period or len(period) != 10:
            continue
        y = int(period[:4]); m = period[5:7]
        bucket = {"03": "Q1", "06": "Q2", "09": "Q3", "12": "Q4"}.get(m)
        if not bucket:
            continue
        if bucket == "Q4" and r["source"] == "DFP":
            key = "DFP"
        elif bucket == "Q4" and r["source"] == "ITR":
            key = "Q4_ITR"
        else:
            key = bucket
        out.setdefault(y, {})[key] = dict(r)
    return out


def _diff_flow(curr: dict, prev: dict | None, fields: list[str]) -> dict:
    out = {}
    for f in fields:
        cv = curr.get(f)
        pv = prev.get(f) if prev else None
        if cv is None:
            out[f] = pv if prev is None else None
        elif pv is None:
            out[f] = cv
        else:
            out[f] = cv - pv
    return out


def derive_for_ticker(ticker: str) -> int:
    inserted = 0
    ensure_schema()
    with sqlite3.connect(DB) as c:
        years = _periods_by_year(c, ticker)
        for year, qmap in sorted(years.items()):
            # Q1 — single = Q1 ITR (já 3 meses)
            if "Q1" in qmap:
                row = qmap["Q1"]
                rec = _build_single(ticker, row, row, derived_from="ITR")
                _upsert(c, rec)
                inserted += 1
            # Q2 = Q2 ITR - Q1 ITR (flow); snapshots from Q2
            if "Q2" in qmap:
                rec = _build_single(ticker, qmap["Q2"], qmap["Q2"],
                                    delta_against=qmap.get("Q1"), derived_from="ITR")
                _upsert(c, rec)
                inserted += 1
            # Q3 = Q3 ITR - Q2 ITR
            if "Q3" in qmap:
                rec = _build_single(ticker, qmap["Q3"], qmap["Q3"],
                                    delta_against=qmap.get("Q2"), derived_from="ITR")
                _upsert(c, rec)
                inserted += 1
            # Q4 = DFP - Q3 ITR (preferred); fallback DFP standalone
            if "DFP" in qmap:
                if "Q3" in qmap:
                    rec = _build_single(ticker, qmap["DFP"], qmap["DFP"],
                                        delta_against=qmap["Q3"], derived_from="DFP-ITR")
                else:
                    # No Q3 ITR — best-effort: use DFP as-is (annual single)
                    rec = _build_single(ticker, qmap["DFP"], qmap["DFP"], derived_from="DFP")
                _upsert(c, rec)
                inserted += 1
        c.commit()
    return inserted


def _build_single(ticker: str, row: dict, snapshot_row: dict,
                  delta_against: dict | None = None,
                  derived_from: str = "ITR") -> dict:
    rec = {
        "ticker": ticker,
        "period_end": row["period_end"],
        "fiscal_quarter": _quarter_label(row["period_end"]),
        "derived_from": derived_from,
    }
    # Flow metrics: subtract if delta_against provided
    if delta_against:
        flow = _diff_flow(row, delta_against, FLOW_METRICS)
    else:
        flow = {f: row.get(f) for f in FLOW_METRICS}
    rec.update(flow)
    # Snapshot metrics: from snapshot_row as-is
    for s in STOCK_METRICS:
        rec[s] = snapshot_row.get(s)
    # Computed margins (single-Q based)
    rev = rec.get("revenue")
    if rev and rev != 0:
        rec["gross_margin"] = (rec.get("gross_profit") / rev) if rec.get("gross_profit") is not None else None
        rec["ebit_margin"] = (rec.get("ebit") / rev) if rec.get("ebit") is not None else None
        rec["net_margin"] = (rec.get("net_income") / rev) if rec.get("net_income") is not None else None
    else:
        rec["gross_margin"] = rec["ebit_margin"] = rec["net_margin"] = None
    return rec


def _upsert(c: sqlite3.Connection, rec: dict) -> None:
    keys = ", ".join(rec.keys())
    placeholders = ", ".join("?" * len(rec))
    c.execute(
        f"INSERT OR REPLACE INTO quarterly_single ({keys}) VALUES ({placeholders})",
        tuple(rec.values()),
    )


def build_all() -> dict:
    counts = {"tickers": 0, "rows": 0}
    with sqlite3.connect(DB) as c:
        tickers = [r[0] for r in c.execute(
            "SELECT DISTINCT ticker FROM quarterly_history"
        ).fetchall()]
    for t in tickers:
        n = derive_for_ticker(t)
        counts["tickers"] += 1
        counts["rows"] += n
        print(f"  {t}: {n} single-Q rows")
    return counts


def show(ticker: str) -> None:
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT period_end, fiscal_quarter, derived_from,
                   revenue, ebit, net_income, fco, fcf_proxy,
                   ebit_margin, net_margin,
                   debt_total, equity
            FROM quarterly_single WHERE ticker=?
            ORDER BY period_end DESC
        """, (ticker,)).fetchall()
    if not rows:
        print(f"No data for {ticker}")
        return
    print(f"\n=== {ticker} — quarterly_single (R$ bi) ===")
    print(f"{'period':<12} {'q':<7} {'src':<8} {'rev':>7} {'ebit':>7} {'net':>7} {'fco':>7} {'fcf':>7} {'em%':>5} {'nm%':>5} {'debt':>7}")
    print("-" * 100)
    for r in rows:
        rev = (r['revenue'] or 0)/1e6
        ebit = (r['ebit'] or 0)/1e6
        ni = (r['net_income'] or 0)/1e6
        fco = (r['fco'] or 0)/1e6
        fcf = (r['fcf_proxy'] or 0)/1e6
        em = (r['ebit_margin'] or 0)*100
        nm = (r['net_margin'] or 0)*100
        dbt = (r['debt_total'] or 0)/1e6
        print(f"{r['period_end']:<12} {r['fiscal_quarter']:<7} {r['derived_from']:<8} {rev:>7,.1f} {ebit:>7,.1f} {ni:>7,.1f} {fco:>7,.1f} {fcf:>7,.1f} {em:>5.1f} {nm:>5.1f} {dbt:>7,.0f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("build")
    p_show = sub.add_parser("show"); p_show.add_argument("ticker")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.cmd == "build":
        r = build_all()
        print(f"\ndone: tickers={r['tickers']} rows={r['rows']}")
    elif args.cmd == "show":
        show(args.ticker.upper())
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
