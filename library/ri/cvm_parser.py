"""CVM parser — normaliza cvm_dre/bpa/bpp/dfc em quarterly_history table.

Para cada (ticker, period_end), extrai métricas-chave usando codigos de conta CVM:

  DRE:
    3.01 Receita líquida
    3.03 Resultado bruto
    3.05 EBIT (Resultado antes do resultado financeiro e dos tributos)
    3.07 Lucro antes de impostos
    3.09 / 3.11 Lucro líquido das operações continuadas / consolidado
    3.04.06 Equivalência patrimonial (especial p/ holdings)

  BPA (Ativo):
    1.01 Ativo Circulante
    1.02 Ativo Não Circulante
    1.00 Ativo Total

  BPP (Passivo):
    2.01 Passivo Circulante
    2.02 Passivo Não Circulante
    2.03 Patrimônio Líquido
    2.01.04 Empréstimos e Financiamentos CP
    2.02.01 Empréstimos e Financiamentos LP

  DFC:
    6.01 Caixa Líquido das Atividades Operacionais (FCO)
    6.02 Caixa Líquido das Atividades de Investimento (Capex when negative)
    6.03 Caixa Líquido das Atividades de Financiamento

Output: quarterly_history table c/ uma row por (ticker, period_end).
Idempotent — REPLACE se period existe.

Uso:
    python -m library.ri.cvm_parser build              # parse all from cvm_*
    python -m library.ri.cvm_parser show VALE3
    python -m library.ri.cvm_parser export csv         # exports quarterly_history.csv
"""
from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "data" / "br_investments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS quarterly_history (
    ticker          TEXT NOT NULL,
    period_end      TEXT NOT NULL,
    source          TEXT NOT NULL,        -- 'DFP' or 'ITR'
    -- DRE (R$ thousand)
    revenue         REAL,
    gross_profit    REAL,
    ebit            REAL,
    pretax_income   REAL,
    net_income      REAL,
    equity_method   REAL,                 -- equiv. patrimonial (holdings)
    -- BP
    total_assets    REAL,
    current_assets  REAL,
    current_liab    REAL,
    total_liab      REAL,
    equity          REAL,
    debt_st         REAL,
    debt_lt         REAL,
    -- DFC
    fco             REAL,                 -- operating cashflow
    fci             REAL,                 -- investment cashflow (capex usually negative)
    fcf_proxy       REAL,                 -- fco + fci (free cashflow approx)
    -- Computed
    gross_margin    REAL,
    ebit_margin     REAL,
    net_margin      REAL,
    debt_total      REAL,
    PRIMARY KEY (ticker, period_end)
);

CREATE INDEX IF NOT EXISTS idx_qh_ticker ON quarterly_history(ticker, period_end);
"""

# CVM account codes mapping (mostly stable across years)
DRE_ACCOUNTS = {
    "revenue":       ("3.01",),       # Receita Líquida
    "gross_profit":  ("3.03",),       # Lucro Bruto
    "ebit":          ("3.05",),       # Resultado antes do Resultado Financeiro
    "pretax_income": ("3.07",),       # Resultado antes dos Tributos
    "net_income":    ("3.11", "3.09"),# Consolidado / Continuadas
    "equity_method": ("3.04.06",),    # Equivalência patrimonial
}

BPA_ACCOUNTS = {
    "total_assets":   ("1",),
    "current_assets": ("1.01",),
}

BPP_ACCOUNTS = {
    "total_liab":     ("2",),
    "current_liab":   ("2.01",),
    "equity":         ("2.03",),
    "debt_st":        ("2.01.04",),
    "debt_lt":        ("2.02.01",),
}

DFC_ACCOUNTS = {
    "fco": ("6.01",),
    "fci": ("6.02",),
}


def ensure_schema() -> None:
    with sqlite3.connect(DB) as c:
        c.executescript(SCHEMA)
        c.commit()


def _lookup(c: sqlite3.Connection, table: str, ticker: str, period_end: str,
            cd_codes: tuple[str, ...]) -> float | None:
    """Try each cd_conta in order, prefer Consolidado then Individual."""
    for cd in cd_codes:
        for grupo_pref in ("%Consolidad%", "%Individual%"):
            row = c.execute(
                f"""SELECT vl_conta FROM {table}
                    WHERE ticker=? AND period_end=? AND cd_conta=?
                      AND grupo_dfp LIKE ?
                    ORDER BY id DESC LIMIT 1""",
                (ticker, period_end, cd, grupo_pref),
            ).fetchone()
            if row and row[0] is not None:
                return float(row[0])
    return None


def parse_period(c: sqlite3.Connection, ticker: str, period_end: str, source: str) -> dict:
    rec = {"ticker": ticker, "period_end": period_end, "source": source}
    for k, codes in DRE_ACCOUNTS.items():
        rec[k] = _lookup(c, "cvm_dre", ticker, period_end, codes)
    for k, codes in BPA_ACCOUNTS.items():
        rec[k] = _lookup(c, "cvm_bpa", ticker, period_end, codes)
    for k, codes in BPP_ACCOUNTS.items():
        rec[k] = _lookup(c, "cvm_bpp", ticker, period_end, codes)
    for k, codes in DFC_ACCOUNTS.items():
        rec[k] = _lookup(c, "cvm_dfc", ticker, period_end, codes)

    # Computed
    rev = rec.get("revenue")
    if rev and rev != 0:
        if rec.get("gross_profit") is not None:
            rec["gross_margin"] = rec["gross_profit"] / rev
        if rec.get("ebit") is not None:
            rec["ebit_margin"] = rec["ebit"] / rev
        if rec.get("net_income") is not None:
            rec["net_margin"] = rec["net_income"] / rev
    if rec.get("debt_st") is not None or rec.get("debt_lt") is not None:
        rec["debt_total"] = (rec.get("debt_st") or 0) + (rec.get("debt_lt") or 0)
    if rec.get("fco") is not None and rec.get("fci") is not None:
        rec["fcf_proxy"] = rec["fco"] + rec["fci"]
    return rec


def build() -> dict:
    ensure_schema()
    counts = {"tickers": 0, "periods": 0, "rows": 0}
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        # Find all (ticker, period_end, source) combinations from cvm_dre
        rows = c.execute("""
            SELECT DISTINCT ticker, period_end, source FROM cvm_dre
            ORDER BY ticker, period_end DESC
        """).fetchall()

        seen_tickers = set()
        for r in rows:
            ticker = r["ticker"]; period_end = r["period_end"]; source = r["source"]
            seen_tickers.add(ticker)
            rec = parse_period(c, ticker, period_end, source)
            keys = ", ".join(rec.keys())
            placeholders = ", ".join("?" * len(rec))
            c.execute(
                f"INSERT OR REPLACE INTO quarterly_history ({keys}) VALUES ({placeholders})",
                tuple(rec.values()),
            )
            counts["periods"] += 1
        c.commit()

        counts["tickers"] = len(seen_tickers)
        counts["rows"] = c.execute("SELECT COUNT(*) FROM quarterly_history").fetchone()[0]

    return counts


def show(ticker: str) -> None:
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT period_end, source, revenue, ebit, net_income,
                   gross_margin, ebit_margin, net_margin,
                   debt_total, fco, fcf_proxy, equity
            FROM quarterly_history WHERE ticker=?
            ORDER BY period_end DESC
        """, (ticker,)).fetchall()
    if not rows:
        print(f"No data for {ticker}. Run: python -m library.ri.cvm_filings ingest dfp --year YYYY --all-catalog")
        return
    print(f"\n=== {ticker} — quarterly history ({len(rows)} periods) ===")
    print(f"{'period':<12} {'src':<4} {'revenue':>12} {'ebit':>10} {'net_inc':>10} {'gm%':>5} {'em%':>5} {'nm%':>5} {'debt':>10} {'fco':>10} {'fcf':>10}")
    print("-" * 110)
    for r in rows:
        rev = (r['revenue'] or 0) / 1e6
        ebit = (r['ebit'] or 0) / 1e6
        ni = (r['net_income'] or 0) / 1e6
        gm = (r['gross_margin'] or 0) * 100
        em = (r['ebit_margin'] or 0) * 100
        nm = (r['net_margin'] or 0) * 100
        dbt = (r['debt_total'] or 0) / 1e6
        fco = (r['fco'] or 0) / 1e6
        fcf = (r['fcf_proxy'] or 0) / 1e6
        print(f"{r['period_end']:<12} {r['source']:<4} {rev:>12,.1f} {ebit:>10,.1f} {ni:>10,.1f} {gm:>5.1f} {em:>5.1f} {nm:>5.1f} {dbt:>10,.0f} {fco:>10,.0f} {fcf:>10,.0f}")
    print("\n(values in R$ billions)")


def export_csv(out: Path) -> None:
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("SELECT * FROM quarterly_history ORDER BY ticker, period_end DESC").fetchall()
    if not rows:
        print("Empty quarterly_history.")
        return
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        for r in rows:
            w.writerow(dict(r))
    print(f"Exported {len(rows)} rows to {out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("build")
    p_show = sub.add_parser("show"); p_show.add_argument("ticker")
    p_exp = sub.add_parser("export"); p_exp.add_argument("kind", choices=["csv"]); p_exp.add_argument("--out", default="quarterly_history.csv")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.cmd == "build":
        r = build()
        print(f"build done: tickers={r['tickers']} periods_processed={r['periods']} total_rows_in_db={r['rows']}")
    elif args.cmd == "show":
        show(args.ticker.upper())
    elif args.cmd == "export":
        export_csv(Path(args.out))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
