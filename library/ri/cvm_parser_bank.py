"""CVM bank-specific parser — schema BACEN para BBDC4, ITUB4, etc.

Bancos têm DRE estruturalmente diferente das empresas operacionais:
  - Em vez de "Receita Líquida" + "Custo dos produtos vendidos" + "Resultado Bruto",
    bancos têm "Receitas de Intermediação Financeira" + "Despesas" + "NII".
  - Loan loss provisions (PDD) são item operacional crucial.
  - Fee income separado de NII (mix matters).
  - Equity (PL) é regulatory para Basel ratios.

Account codes mapeados (CVM standard para bancos):
  DRE bancária:
    3.01 Receitas de Intermediação Financeira
    3.02 Despesas de Intermediação Financeira (negative)
    3.03 Resultado Bruto de Intermediação Financeira  → NII
    3.04.01 Despesa de PDD/Perda Esperada              → loan_loss_provisions
    3.04.02 Receitas de Prestação de Serviços          → fee_income
    3.04.03 Despesas com Pessoal                       → personnel_expenses
    3.04.04 Outras Despesas Administrativas            → admin_expenses
    3.04.05 Despesas Tributárias                       → tax_expenses
    3.04.06 Outras Receitas Operacionais               → other_op_income (incl seguros)
    3.04.07 Outras Despesas Operacionais               → other_op_expenses (incl D&A)
    3.05 Resultado antes dos Tributos sobre o Lucro    → pretax
    3.07 / 3.09 Lucro Líquido                          → net_income

  Derived metrics:
    cost_to_income_ratio = (personnel + admin) / (NII + fee_income)
    pre_provision_profit = NII + fee_income - personnel - admin (before PDD + taxes)
    cost_of_risk = PDD / loan_book (need BPA)
    efficiency_ratio = opex / total_revenue

Output: bank_quarterly_history table (parallel a quarterly_history mas para bancos).

Aplicado a tickers onde catalog tem `bank: true` flag.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "data" / "br_investments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS bank_quarterly_history (
    ticker                  TEXT NOT NULL,
    period_end              TEXT NOT NULL,
    source                  TEXT NOT NULL,            -- 'DFP' or 'ITR'
    -- DRE bancária (R$ thousand from CVM CSVs)
    nii                     REAL,                     -- Net Interest Income (3.03)
    interest_income         REAL,                     -- 3.01
    interest_expense        REAL,                     -- 3.02 (negative)
    fee_income              REAL,                     -- 3.04.02
    personnel_expenses      REAL,                     -- 3.04.03
    admin_expenses          REAL,                     -- 3.04.04
    tax_expenses            REAL,                     -- 3.04.05
    loan_loss_provisions    REAL,                     -- 3.04.01 (negative)
    other_op_income         REAL,                     -- 3.04.06
    other_op_expenses       REAL,                     -- 3.04.07
    pretax_income           REAL,                     -- 3.05
    net_income              REAL,                     -- 3.07 or 3.09 (consolidated total)
    net_income_attributable REAL,                     -- 3.11.01 (atribuível aos controladores)
    net_income_minorities   REAL,                     -- 3.11.02 (atribuível aos não-controladores)
    -- BP relevantes
    total_assets            REAL,
    equity                  REAL,
    -- BS bank-specific (extracted from BPA via ds_conta)
    loan_book               REAL,                     -- Operações de Crédito (gross)
    pdd_reserve             REAL,                     -- Provisão para Perdas Esperadas (negative)
    deposits                REAL,                     -- Depósitos (BPP 2.02.01 ou ds_conta)
    -- Derived ratios
    cost_to_income_ratio    REAL,
    pre_provision_profit    REAL,
    nim_proxy               REAL,                     -- NII / total_assets
    coverage_ratio_bs       REAL,                     -- abs(pdd_reserve) / loan_book
    equity_to_assets        REAL,                     -- equity / total_assets (leverage proxy)
    cost_of_risk_ytd        REAL,                     -- abs(loan_loss_provisions) / loan_book — annualized later
    -- BACEN-target columns (filled by future BACEN fetcher; NULL for now)
    cet1_ratio              REAL,                     -- Common Equity Tier 1 (BACEN)
    rwa                     REAL,                     -- Risk-Weighted Assets (BACEN)
    basel_ratio             REAL,                     -- Total capital / RWA (BACEN Pillar III)
    npl_ratio               REAL,                     -- Non-performing loans / loan_book
    PRIMARY KEY (ticker, period_end)
);

CREATE INDEX IF NOT EXISTS idx_bqh_ticker ON bank_quarterly_history(ticker, period_end);
"""

# Migration: add columns to existing table if missing (idempotent)
MIGRATION_COLUMNS = [
    ("loan_book",         "REAL"),
    ("pdd_reserve",       "REAL"),
    ("deposits",          "REAL"),
    ("coverage_ratio_bs", "REAL"),
    ("equity_to_assets",  "REAL"),
    ("cost_of_risk_ytd",  "REAL"),
    ("cet1_ratio",        "REAL"),
    ("rwa",               "REAL"),
    ("basel_ratio",       "REAL"),
    ("npl_ratio",         "REAL"),
    # Phase LL Sprint 1.1.x — split consolidated NI into controladora vs minoritários
    ("net_income_attributable", "REAL"),
    ("net_income_minorities",   "REAL"),
]

# BS lookups (ds_conta-based — bancos usam cd_conta diferentes mas descrição uniforme)
BANK_BPA_DESC_ACCOUNTS = {
    "loan_book":  ["operações de crédito e arrendamento mercantil financeir",  # Itaú
                   "operações de crédito"],                                       # Bradesco etc.
    "pdd_reserve": ["(-) provisão para perda esperada",                          # Itaú prefix
                    "provisão para perdas esperadas associadas ao risco de c",   # Bradesco
                    "provisão para perda esperada associadas ao risco de c"],
}
BANK_BPP_DESC_ACCOUNTS = {
    "deposits":   ["depósitos a vista e a prazo",
                   "depósitos"],
}

# Cada banco usa códigos diferentes para mesmas contas. Usamos descrição (ds_conta substring).
# Lista ordenada — primeira match wins. Case-insensitive substring.
BANK_DRE_ACCOUNTS_BY_DESC = {
    "interest_income":      ["receitas da intermediação financeira", "receitas de intermediação financeira",
                             "receita de intermediação"],
    "interest_expense":     ["despesas da intermediação financeira", "despesas de intermediação financeira"],
    "nii":                  ["resultado bruto intermediação financeira",   # Itaú
                             "resultado bruto de intermediação financeira",  # Bradesco/std
                             "resultado bruto da intermediação"],
    "loan_loss_provisions": ["despesa de provisão para perda esperada",
                             "perda esperada para risco de crédito",
                             "perda) esperada com operações de crédito",  # Itaú substring
                             "perda esperada com operações de crédito",
                             "despesa de pdd",
                             "provisão para crédito"],
    "fee_income":           ["receitas de prestação de serviços e tarifas bancárias",  # Itaú 3.01.05
                             "receitas de prestação de serviços",
                             "receitas de prestações de serviços",
                             "receita de tarifas"],
    "personnel_expenses":   ["despesas com pessoal", "despesa de pessoal", "despesas de pessoal"],
    "admin_expenses":       ["outras despesas administrativas", "despesas administrativas",
                             "outras despesas de administrativas"],
    "tax_expenses":         ["despesas tributárias", "despesa tributária"],
    "other_op_income":      ["outras receitas operacionais"],
    "other_op_expenses":    ["outras despesas operacionais"],
    "pretax_income":        ["resultado antes dos tributos sobre o lucro", "resultado antes dos tributos",
                             "lucro antes do imposto de renda", "lucro antes dos impostos"],
    "net_income":           ["lucro/prejuízo consolidado do período",
                             "lucro ou prejuízo das operações continuadas",
                             "lucro líquido do período",
                             "resultado líquido das operações continuadas"],
    # 3.11.01 — what flows into EPS calc (excludes minorities)
    "net_income_attributable": ["atribuído aos sócios da empresa controladora",   # BBDC4 actual
                                "atribuível aos sócios da empresa controladora",
                                "atribuído a sócios da empresa controladora",
                                "atribuível a sócios da empresa controladora",
                                "atribuível aos acionistas controladores",
                                "atribuível ao acionista controlador",
                                "atribuível à controladora",
                                "atribuído à controladora",
                                "atribuído à empresa controladora",
                                "atribuível à empresa controladora"],
    # 3.11.02 — minorities (informational, validates that total = attrib + minorities)
    "net_income_minorities":   ["atribuído aos sócios não controladores",
                                "atribuível aos sócios não controladores",
                                "atribuído a sócios não controladores",
                                "atribuível a sócios não controladores",
                                "atribuível aos não controladores",
                                "participação dos não controladores",
                                "participação não controladora"],
}

BPA_ACCOUNTS = {
    "total_assets": ("1",),
}
# Equity per bank uses different cd_conta (BBDC4=2.07, ITUB4=2.06).
# Use ds_conta lookup ("patrimônio líquido") which is uniform.
BPP_ACCOUNTS: dict[str, tuple[str, ...]] = {}

BANK_BPP_EQUITY_DESCS = ["patrimônio líquido consolidado",
                          "patrimônio líquido"]


def ensure_schema() -> None:
    with sqlite3.connect(DB) as c:
        c.executescript(SCHEMA)
        # Idempotent migration for existing DBs that pre-date the BACEN columns
        existing = {row[1] for row in c.execute(
            "PRAGMA table_info(bank_quarterly_history)").fetchall()}
        for col, typ in MIGRATION_COLUMNS:
            if col not in existing:
                c.execute(f"ALTER TABLE bank_quarterly_history ADD COLUMN {col} {typ}")
        c.commit()


def _lookup_by_desc(c: sqlite3.Connection, table: str, ticker: str, period_end: str,
                    desc_patterns: list[str]) -> float | None:
    """Lookup vl_conta where ds_conta matches any pattern (case-insensitive substring).
    Prefer Consolidado over Individual. First match wins per pattern order.

    Tiebreaker: prefer shortest ds_conta (= most general account, not sub-categories
    like "Arrendamento" or "Outros Créditos"); then shortest cd_conta; then largest |vl_conta|
    (main account usually has biggest absolute value).
    """
    for pattern in desc_patterns:
        for grupo_pref in ("%Consolidad%", "%Individual%"):
            row = c.execute(
                f"SELECT vl_conta, ds_conta FROM {table} "
                f"WHERE ticker=? AND period_end=? "
                f"AND LOWER(ds_conta) LIKE LOWER(?) "
                f"AND grupo_dfp LIKE ? "
                f"ORDER BY LENGTH(ds_conta) ASC, LENGTH(cd_conta) ASC, ABS(vl_conta) DESC, id DESC LIMIT 1",
                (ticker, period_end, f"%{pattern}%", grupo_pref),
            ).fetchone()
            if row and row[0] is not None:
                return float(row[0])
    return None


def _lookup(c: sqlite3.Connection, table: str, ticker: str, period_end: str,
            cd_codes: tuple[str, ...]) -> float | None:
    """Legacy cd_conta lookup (used for BPA/BPP)."""
    for cd in cd_codes:
        for grupo_pref in ("%Consolidad%", "%Individual%"):
            row = c.execute(
                f"SELECT vl_conta FROM {table} "
                f"WHERE ticker=? AND period_end=? AND cd_conta=? "
                f"AND grupo_dfp LIKE ? ORDER BY id DESC LIMIT 1",
                (ticker, period_end, cd, grupo_pref),
            ).fetchone()
            if row and row[0] is not None:
                return float(row[0])
    return None


def parse_period(c: sqlite3.Connection, ticker: str, period_end: str, source: str) -> dict:
    rec = {"ticker": ticker, "period_end": period_end, "source": source}
    # DRE — by description (handles ITUB4 vs BBDC4 código differences)
    for k, descs in BANK_DRE_ACCOUNTS_BY_DESC.items():
        rec[k] = _lookup_by_desc(c, "cvm_dre", ticker, period_end, descs)
    # BPA total_assets — by code (estável)
    for k, codes in BPA_ACCOUNTS.items():
        rec[k] = _lookup(c, "cvm_bpa", ticker, period_end, codes)
    # BPA bank-specific — by ds_conta (varia entre bancos)
    for k, descs in BANK_BPA_DESC_ACCOUNTS.items():
        rec[k] = _lookup_by_desc(c, "cvm_bpa", ticker, period_end, descs)
    # BPP equity — by ds_conta (cd_conta varia entre bancos)
    rec["equity"] = _lookup_by_desc(c, "cvm_bpp", ticker, period_end, BANK_BPP_EQUITY_DESCS)
    # BPP deposits — by ds_conta
    for k, descs in BANK_BPP_DESC_ACCOUNTS.items():
        rec[k] = _lookup_by_desc(c, "cvm_bpp", ticker, period_end, descs)

    # Derived
    nii = rec.get("nii") or 0
    fee = rec.get("fee_income") or 0
    pers = rec.get("personnel_expenses") or 0
    admin = rec.get("admin_expenses") or 0
    revenue_proxy = nii + fee
    opex = (pers or 0) + (admin or 0)   # both stored as negative typically
    if revenue_proxy != 0:
        rec["cost_to_income_ratio"] = abs(opex) / revenue_proxy
    rec["pre_provision_profit"] = revenue_proxy + opex   # opex negative
    if rec.get("total_assets") and rec["total_assets"] != 0 and rec.get("nii"):
        rec["nim_proxy"] = rec["nii"] / rec["total_assets"]
    # Bank-specific BS derived
    loan_book = rec.get("loan_book") or 0
    pdd_bs = rec.get("pdd_reserve") or 0
    if loan_book and loan_book > 0:
        rec["coverage_ratio_bs"] = abs(pdd_bs) / loan_book
        if rec.get("loan_loss_provisions") is not None:
            # Cost of risk: PDD expense (DRE) / loan book — YTD basis (annualize later)
            rec["cost_of_risk_ytd"] = abs(rec["loan_loss_provisions"]) / loan_book
    if rec.get("total_assets") and rec["total_assets"] > 0 and rec.get("equity"):
        rec["equity_to_assets"] = rec["equity"] / rec["total_assets"]
    # BACEN columns (cet1_ratio, rwa, basel_ratio, npl_ratio) deixados NULL —
    # serão preenchidos por fetcher BACEN dedicado (futuro).
    return rec


def get_bank_tickers() -> list[str]:
    """Use canonical catalog accessor."""
    from library.ri.catalog import banks as _banks
    return [e["ticker"] for e in _banks()]


def build() -> dict:
    ensure_schema()
    counts = {"tickers": 0, "rows": 0}
    bank_tickers = get_bank_tickers()
    print(f"Bank tickers: {bank_tickers}")
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        for ticker in bank_tickers:
            rows = c.execute(
                "SELECT DISTINCT period_end, source FROM cvm_dre WHERE ticker=? ORDER BY period_end",
                (ticker,),
            ).fetchall()
            n = 0
            for r in rows:
                rec = parse_period(c, ticker, r["period_end"], r["source"])
                if rec.get("nii") is None and rec.get("net_income") is None:
                    continue   # no data
                keys = ", ".join(rec.keys())
                placeholders = ", ".join("?" * len(rec))
                c.execute(
                    f"INSERT OR REPLACE INTO bank_quarterly_history ({keys}) VALUES ({placeholders})",
                    tuple(rec.values()),
                )
                n += 1
            counts["rows"] += n
            counts["tickers"] += 1 if n else 0
            print(f"  {ticker}: {n} rows")
        c.commit()
    return counts


def show(ticker: str) -> None:
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT period_end, source, nii, fee_income, loan_loss_provisions,
                   personnel_expenses, admin_expenses, pretax_income, net_income,
                   total_assets, equity, cost_to_income_ratio, pre_provision_profit,
                   loan_book, pdd_reserve, coverage_ratio_bs, equity_to_assets,
                   cost_of_risk_ytd, cet1_ratio, basel_ratio
            FROM bank_quarterly_history WHERE ticker=? ORDER BY period_end DESC
        """, (ticker,)).fetchall()
    if not rows:
        print(f"No data for {ticker}")
        return
    print(f"\n=== {ticker} — bank_quarterly_history (R$ bi, valores YTD para ITRs) ===")
    print(f"{'period':<12} {'src':<4} {'NII':>8} {'fees':>7} {'PDD':>8} {'NI':>7} {'loans':>8} {'cov%':>5} {'CoR%':>5} {'E/A%':>5} {'CET1':>5}")
    print("-" * 110)
    for r in rows[:16]:
        nii = (r['nii'] or 0)/1e6
        fees = (r['fee_income'] or 0)/1e6
        pdd = (r['loan_loss_provisions'] or 0)/1e6
        ni = (r['net_income'] or 0)/1e6
        loans = (r['loan_book'] or 0)/1e6
        cov = (r['coverage_ratio_bs'] or 0)*100
        cor = (r['cost_of_risk_ytd'] or 0)*100
        ea = (r['equity_to_assets'] or 0)*100
        cet1 = r['cet1_ratio']
        cet1_s = f"{cet1*100:.1f}" if cet1 else "—"
        print(f"{r['period_end']:<12} {r['source']:<4} {nii:>8,.1f} {fees:>7,.1f} {pdd:>8,.1f} {ni:>7,.1f} {loans:>8,.1f} {cov:>5.1f} {cor:>5.2f} {ea:>5.1f} {cet1_s:>5}")
    print("\n(NII/fees/PDD/NI/loans em R$ bi YTD; cov=PDD reserve/loans; CoR=PDD expense/loans;")
    print(" E/A=equity/total_assets; CET1=BACEN data, NULL até fetcher BACEN integrado)")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("build")
    p_show = sub.add_parser("show")
    p_show.add_argument("ticker")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.cmd == "build":
        r = build()
        print(f"\nbuild done: tickers={r['tickers']} rows={r['rows']}")
    elif args.cmd == "show":
        show(args.ticker.upper())
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
