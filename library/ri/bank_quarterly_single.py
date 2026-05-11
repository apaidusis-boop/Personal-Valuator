"""Bank single-quarter delta — espelha quarterly_single mas para schema bancário.

ITRs CVM são acumulados YTD (Q3 ITR = 9 meses). Para análise QoQ real:
  Q1 single = ITR Q1 (3 meses já)
  Q2 single = ITR Q2 - ITR Q1 (6m - 3m)
  Q3 single = ITR Q3 - ITR Q2 (9m - 6m)
  Q4 single = DFP - ITR Q3 (12m - 9m)

Para banks, FLOW metrics = subtraem; STOCK (TA, equity) = snapshot.

Output: bank_quarterly_single table.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "data" / "br_investments.db"

FLOW = ["nii", "interest_income", "interest_expense", "fee_income",
        "personnel_expenses", "admin_expenses", "tax_expenses",
        "loan_loss_provisions", "other_op_income", "other_op_expenses",
        "pretax_income", "net_income", "pre_provision_profit"]
STOCK = ["total_assets", "equity"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS bank_quarterly_single (
    ticker                  TEXT NOT NULL,
    period_end              TEXT NOT NULL,
    fiscal_quarter          TEXT NOT NULL,
    derived_from            TEXT NOT NULL,
    -- flow (single-Q)
    nii                     REAL,
    interest_income         REAL,
    interest_expense        REAL,
    fee_income              REAL,
    personnel_expenses      REAL,
    admin_expenses          REAL,
    tax_expenses            REAL,
    loan_loss_provisions    REAL,
    other_op_income         REAL,
    other_op_expenses       REAL,
    pretax_income           REAL,
    net_income              REAL,
    pre_provision_profit    REAL,
    -- stock (snapshot)
    total_assets            REAL,
    equity                  REAL,
    -- derived ratios single-Q based
    cost_to_income_ratio    REAL,
    nim_proxy               REAL,
    PRIMARY KEY (ticker, period_end)
);
CREATE INDEX IF NOT EXISTS idx_bqs_ticker ON bank_quarterly_single(ticker, fiscal_quarter);
"""


def ensure_schema() -> None:
    with sqlite3.connect(DB) as c:
        c.executescript(SCHEMA)
        c.commit()


def _quarter_label(period_end: str) -> str:
    y, m, _ = period_end.split("-")
    q = {"03": "1", "06": "2", "09": "3", "12": "4"}.get(m, "?")
    return f"{y}Q{q}"


def _periods_by_year(c: sqlite3.Connection, ticker: str) -> dict[int, dict[str, dict]]:
    out = {}
    c.row_factory = sqlite3.Row
    rows = c.execute(
        "SELECT * FROM bank_quarterly_history WHERE ticker=? ORDER BY period_end",
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
        else:
            key = bucket
        out.setdefault(y, {})[key] = dict(r)
    return out


def _diff_flow(curr: dict, prev: dict | None) -> dict:
    out = {}
    for f in FLOW:
        cv = curr.get(f); pv = prev.get(f) if prev else None
        if cv is None: out[f] = pv if prev is None else None
        elif pv is None: out[f] = cv
        else: out[f] = cv - pv
    return out


def _build_single(ticker: str, row: dict, snapshot_row: dict,
                  delta_against: dict | None, derived_from: str) -> dict:
    rec = {"ticker": ticker, "period_end": row["period_end"],
           "fiscal_quarter": _quarter_label(row["period_end"]),
           "derived_from": derived_from}
    if delta_against:
        flow = _diff_flow(row, delta_against)
    else:
        flow = {f: row.get(f) for f in FLOW}
    rec.update(flow)
    for s in STOCK:
        rec[s] = snapshot_row.get(s)
    # Compute single-Q ratios
    nii = rec.get("nii") or 0
    fee = rec.get("fee_income") or 0
    pers = rec.get("personnel_expenses") or 0
    admin = rec.get("admin_expenses") or 0
    revenue_proxy = nii + fee
    if revenue_proxy != 0:
        rec["cost_to_income_ratio"] = abs((pers or 0) + (admin or 0)) / revenue_proxy
    if rec.get("total_assets") and rec["total_assets"] != 0 and nii:
        # NIM annualized: single-Q NII * 4 / TA
        rec["nim_proxy"] = (nii * 4) / rec["total_assets"]
    return rec


def derive_for_ticker(ticker: str) -> int:
    inserted = 0
    ensure_schema()
    with sqlite3.connect(DB) as c:
        years = _periods_by_year(c, ticker)
        for year, qmap in sorted(years.items()):
            if "Q1" in qmap:
                rec = _build_single(ticker, qmap["Q1"], qmap["Q1"], None, "ITR")
                _upsert(c, rec); inserted += 1
            if "Q2" in qmap:
                rec = _build_single(ticker, qmap["Q2"], qmap["Q2"], qmap.get("Q1"), "ITR")
                _upsert(c, rec); inserted += 1
            if "Q3" in qmap:
                rec = _build_single(ticker, qmap["Q3"], qmap["Q3"], qmap.get("Q2"), "ITR")
                _upsert(c, rec); inserted += 1
            if "DFP" in qmap:
                if "Q3" in qmap:
                    rec = _build_single(ticker, qmap["DFP"], qmap["DFP"], qmap["Q3"], "DFP-ITR")
                else:
                    rec = _build_single(ticker, qmap["DFP"], qmap["DFP"], None, "DFP")
                _upsert(c, rec); inserted += 1
        c.commit()
    return inserted


def _upsert(c: sqlite3.Connection, rec: dict) -> None:
    keys = ", ".join(rec.keys())
    placeholders = ", ".join("?" * len(rec))
    c.execute(
        f"INSERT OR REPLACE INTO bank_quarterly_single ({keys}) VALUES ({placeholders})",
        tuple(rec.values()),
    )


def build_all() -> dict:
    counts = {"tickers": 0, "rows": 0}
    with sqlite3.connect(DB) as c:
        try:
            tickers = [r[0] for r in c.execute(
                "SELECT DISTINCT ticker FROM bank_quarterly_history"
            ).fetchall()]
        except sqlite3.OperationalError:
            return {"error": "bank_quarterly_history empty — run cvm_parser_bank build first"}
    for t in tickers:
        n = derive_for_ticker(t)
        counts["tickers"] += 1
        counts["rows"] += n
        print(f"  {t}: {n} single-Q rows")
    return counts


def show(ticker: str) -> None:
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            "SELECT period_end, fiscal_quarter, derived_from, nii, fee_income, "
            "loan_loss_provisions, personnel_expenses, admin_expenses, "
            "net_income, cost_to_income_ratio, nim_proxy, total_assets "
            "FROM bank_quarterly_single WHERE ticker=? ORDER BY period_end DESC",
            (ticker,),
        ).fetchall()
    if not rows:
        print(f"No single-Q data for {ticker}")
        return
    print(f"\n=== {ticker} — bank_quarterly_single (single-Q, R$ bi) ===")
    print(f"{'period':<12} {'q':<7} {'src':<8} {'NII':>7} {'fees':>6} {'PDD':>7} {'opex':>7} {'NI':>6} {'C/I%':>5} {'NIM%':>5}")
    print("-" * 90)
    for r in rows[:16]:
        nii = (r['nii'] or 0)/1e6
        fees = (r['fee_income'] or 0)/1e6
        pdd = (r['loan_loss_provisions'] or 0)/1e6
        opex = ((r['personnel_expenses'] or 0) + (r['admin_expenses'] or 0))/1e6
        ni = (r['net_income'] or 0)/1e6
        ci = (r['cost_to_income_ratio'] or 0)*100
        nim = (r['nim_proxy'] or 0)*100
        print(f"{r['period_end']:<12} {r['fiscal_quarter']:<7} {r['derived_from']:<8} {nii:>7,.1f} {fees:>6,.1f} {pdd:>7,.1f} {opex:>7,.1f} {ni:>6,.1f} {ci:>5.1f} {nim:>5.2f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("build")
    p_show = sub.add_parser("show")
    p_show.add_argument("ticker")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.cmd == "build":
        r = build_all()
        if "error" in r:
            print(r["error"])
        else:
            print(f"\nbuild done: tickers={r['tickers']} rows={r['rows']}")
    elif args.cmd == "show":
        show(args.ticker.upper())
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
