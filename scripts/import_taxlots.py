"""import_taxlots — parse JP Morgan tax-lot CSV export para DB.

O CSV tem 1 row por lot (mesma posição pode ter múltiplos lots).

Acções:
  1. Parse CSV → tax_lots (1 row/lot)
  2. Agrega lots → portfolio_positions (weighted avg, replace active US)
  3. Cash → broker_cash
  4. Mapa ticker "BRKB" → "BRK-B" (normalize)

Uso:
    python scripts/import_taxlots.py C:/Users/paidu/Downloads/taxlots.txt
    python scripts/import_taxlots.py <file> --dry-run
"""
from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_US = ROOT / "data" / "us_investments.db"


# Map from JPM CSV ticker → universe/DB ticker
TICKER_MAP = {
    "BRKB": "BRK-B",
}


def _normalize_ticker(t: str) -> str:
    return TICKER_MAP.get(t.upper(), t.upper())


def _parse_number(s: str) -> float | None:
    if s is None:
        return None
    s = s.strip().replace(",", "").replace('"', "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_date(s: str) -> str | None:
    if not s or s.strip() in ("", "0"):
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date().isoformat()
        except ValueError:
            continue
    return None


def parse_csv(path: Path) -> tuple[list[dict], dict, dict]:
    """Devolve (lots, cash, meta)."""
    lots: list[dict] = []
    cash: dict = {}
    asof_row = None
    with path.open(encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker_raw = row.get("Ticker") or ""
            ticker = _normalize_ticker(ticker_raw.strip()) if ticker_raw else ""
            if not ticker:
                continue
            asset_class = row.get("Asset Class", "").lower()
            # Cash
            if "cash" in asset_class or ticker == "QACDS":
                cash = {
                    "broker": "JPM",
                    "currency": row.get("Base CCY", "USD"),
                    "amount": _parse_number(row.get("Quantity")) or 0.0,
                    "as_of": _parse_date(row.get("As of", "").strip().split()[0]) or date.today().isoformat(),
                }
                continue
            qty = _parse_number(row.get("Quantity"))
            unit_cost = _parse_number(row.get("Unit Cost"))
            total_cost = _parse_number(row.get("Cost"))
            acq = _parse_date(row.get("Acquisition Date"))
            if qty is None or unit_cost is None or acq is None:
                continue
            lots.append({
                "ticker": ticker,
                "acquisition_date": acq,
                "quantity": qty,
                "unit_cost": unit_cost,
                "total_cost": total_cost or (qty * unit_cost),
                "tax_term": row.get("Tax term", "").strip(),
                "days_held": int(_parse_number(row.get("Days held")) or 0),
                "notes": (row.get("Description", "") or "")[:200],
            })
            asof_row = row.get("As of")
    meta = {"asof_jpm": asof_row}
    return lots, cash, meta


def persist_lots(lots: list[dict], dry_run: bool = False) -> dict:
    from scripts.init_db import init
    init(DB_US)
    now = datetime.now(UTC).isoformat()

    with sqlite3.connect(DB_US) as c:
        # Clear prior JPM lots (idempotente)
        if not dry_run:
            c.execute("DELETE FROM tax_lots WHERE source='jpm_import'")
        inserted = 0
        for lot in lots:
            if not dry_run:
                c.execute(
                    """INSERT INTO tax_lots
                        (ticker, acquisition_date, quantity, unit_cost, total_cost,
                         tax_term, days_held, source, imported_at, active, notes)
                       VALUES (?,?,?,?,?,?,?,'jpm_import',?,1,?)""",
                    (lot["ticker"], lot["acquisition_date"], lot["quantity"],
                     lot["unit_cost"], lot["total_cost"], lot["tax_term"],
                     lot["days_held"], now, lot["notes"]),
                )
                inserted += 1
        if not dry_run:
            c.commit()
    return {"lots_inserted": inserted}


def aggregate_to_positions(dry_run: bool = False) -> dict:
    """Agrega tax_lots por ticker → portfolio_positions (weighted avg)."""
    from collections import defaultdict
    agg: dict[str, dict] = defaultdict(lambda: {"qty": 0.0, "cost": 0.0, "min_date": None})
    with sqlite3.connect(DB_US) as c:
        for r in c.execute("""
            SELECT ticker, acquisition_date, quantity, total_cost
            FROM tax_lots WHERE source='jpm_import' AND active=1
        """):
            tk, acq, qty, cost = r
            agg[tk]["qty"] += qty
            agg[tk]["cost"] += cost
            if agg[tk]["min_date"] is None or acq < agg[tk]["min_date"]:
                agg[tk]["min_date"] = acq

        updated = 0
        inserted = 0
        if not dry_run:
            # Remove active JPM positions e re-insere
            c.execute("DELETE FROM portfolio_positions WHERE active=1 AND notes LIKE 'JPM%' OR notes LIKE '%jpm%'")
            for tk, d in agg.items():
                avg_cost = d["cost"] / d["qty"] if d["qty"] > 0 else 0
                c.execute(
                    """INSERT INTO portfolio_positions
                         (ticker, weight, entry_date, entry_price, active, quantity, notes)
                       VALUES (?, 0, ?, ?, 1, ?, ?)""",
                    (tk, d["min_date"], avg_cost, d["qty"],
                     f"JPM tax-lot import {date.today().isoformat()}"),
                )
                inserted += 1
            # Ensure companies row for each ticker
            for tk in agg:
                c.execute(
                    """INSERT OR IGNORE INTO companies (ticker, name, sector, is_holding, currency)
                       VALUES (?, ?, ?, 1, 'USD')""",
                    (tk, tk, None),
                )
                c.execute("UPDATE companies SET is_holding=1 WHERE ticker=?", (tk,))
            c.commit()

    return {
        "tickers": len(agg),
        "positions_inserted": inserted,
        "summary": {tk: {"qty": round(d["qty"], 4), "avg_cost": round(d["cost"]/d["qty"],2)}
                    for tk, d in agg.items()},
    }


def persist_cash(cash: dict, dry_run: bool = False) -> dict:
    if not cash:
        return {"status": "no_cash"}
    if dry_run:
        return {"status": "dry_run", "cash": cash}
    from scripts.init_db import init
    init(DB_US)
    with sqlite3.connect(DB_US) as c:
        c.execute(
            """INSERT INTO broker_cash (broker, currency, amount, as_of)
               VALUES (?,?,?,?)
               ON CONFLICT(broker, currency) DO UPDATE SET
                 amount=excluded.amount, as_of=excluded.as_of""",
            (cash["broker"], cash["currency"], cash["amount"], cash["as_of"]),
        )
        c.commit()
    return {"status": "persisted", "cash": cash}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", help="Path to JPM taxlots CSV/TXT")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    p = Path(args.file).expanduser().resolve()
    if not p.exists():
        print(f"[erro] ficheiro não encontrado: {p}")
        return 1

    print(f"Parsing {p}...")
    lots, cash, meta = parse_csv(p)
    print(f"  lots: {len(lots)}  cash: {cash.get('amount', 0)} {cash.get('currency','')}")
    print(f"  asof: {meta.get('asof_jpm')}")

    # Persist lots
    r1 = persist_lots(lots, dry_run=args.dry_run)
    print(f"  tax_lots: {r1}")

    # Cash
    r2 = persist_cash(cash, dry_run=args.dry_run)
    print(f"  cash: {r2}")

    # Aggregate → portfolio_positions
    r3 = aggregate_to_positions(dry_run=args.dry_run)
    print(f"  aggregated positions: {r3['tickers']} tickers")
    if args.dry_run:
        for tk, d in r3["summary"].items():
            print(f"    {tk:<8} qty={d['qty']} avg={d['avg_cost']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
