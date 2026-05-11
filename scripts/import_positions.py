"""import_positions — importa JPM positions.csv (formato agregado).

Diferente do taxlots.txt: 1 row por ticker (não por lot). Usado quando
o user exporta um snapshot mais recente. Detecta diffs vs tax_lots e
cria synthetic lots para posições novas ou deltas positivos.

Uso:
    python scripts/import_positions.py "C:/Users/paidu/Downloads/positions (3).csv"
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

TICKER_MAP = {"BRKB": "BRK-B"}


def _num(s):
    if s is None:
        return None
    s = str(s).strip().replace(",", "").replace('"', "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _norm(t: str) -> str:
    return TICKER_MAP.get((t or "").upper(), (t or "").upper())


def parse(path: Path) -> tuple[list[dict], dict]:
    pos: list[dict] = []
    cash_sweep = None
    cash_debit = None
    with path.open(encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tk_raw = (row.get("Ticker") or "").strip()
            tk = _norm(tk_raw)
            asset = (row.get("Asset Class") or "").lower()
            desc = (row.get("Description") or "").strip()

            if "cash" in asset:
                amt = _num(row.get("Quantity")) or 0
                if tk == "QACDS":
                    cash_sweep = amt
                elif "US DOLLAR" in desc.upper():
                    cash_debit = amt  # typically negative
                continue
            if not tk:
                continue
            pos.append({
                "ticker": tk,
                "quantity": _num(row.get("Quantity")),
                "unit_cost": _num(row.get("Unit Cost")),
                "total_cost": _num(row.get("Cost")),
                "price_now": _num(row.get("Price") or row.get("Local Price")),
                "description": desc,
                "asset_strategy": (row.get("Asset Strategy") or "").strip(),
            })
    return pos, {"sweep": cash_sweep, "debit": cash_debit}


def sync_positions(positions: list[dict]) -> dict:
    """Compara com DB actual. Devolve diffs + aplica updates."""
    from scripts.init_db import init
    init(DB_US)
    now = datetime.now(UTC).isoformat()
    today = date.today().isoformat()

    diffs = {"new_tickers": [], "qty_changed": [], "unchanged": []}

    with sqlite3.connect(DB_US) as c:
        # Existing active US positions (from portfolio_positions)
        existing = {
            r[0]: {"qty": r[1], "avg": r[2]}
            for r in c.execute(
                "SELECT ticker, quantity, entry_price FROM portfolio_positions WHERE active=1"
            )
        }

        for p in positions:
            tk = p["ticker"]
            new_qty = p["quantity"] or 0
            new_avg = p["unit_cost"] or 0

            if tk not in existing:
                diffs["new_tickers"].append(p)
                # Insert company + position
                c.execute(
                    """INSERT OR IGNORE INTO companies (ticker, name, sector, is_holding, currency)
                       VALUES (?, ?, 'Unknown', 1, 'USD')""",
                    (tk, (p["description"][:60] or tk)),
                )
                c.execute("UPDATE companies SET is_holding=1 WHERE ticker=?", (tk,))
                c.execute(
                    """INSERT INTO portfolio_positions
                         (ticker, weight, entry_date, entry_price, active, quantity, notes)
                       VALUES (?, 0, ?, ?, 1, ?, ?)""",
                    (tk, today, new_avg, new_qty,
                     f"JPM positions.csv import {today}"),
                )
                # Synthetic tax lot (approximate; use today as acquisition)
                c.execute(
                    """INSERT INTO tax_lots
                         (ticker, acquisition_date, quantity, unit_cost, total_cost,
                          tax_term, days_held, source, imported_at, active, notes)
                       VALUES (?,?,?,?,?,?,?,'positions_csv',?,1,?)""",
                    (tk, today, new_qty, new_avg, p["total_cost"] or (new_qty * new_avg),
                     "Short", 0, now,
                     f"Synthetic lot from positions.csv ({p['description'][:80]})"),
                )
                continue

            ex = existing[tk]
            if abs((ex["qty"] or 0) - new_qty) < 0.0001 and abs((ex["avg"] or 0) - new_avg) < 0.01:
                diffs["unchanged"].append(tk)
                continue

            # Qty or avg changed
            delta_qty = new_qty - (ex["qty"] or 0)
            diffs["qty_changed"].append({
                "ticker": tk,
                "old_qty": ex["qty"], "new_qty": new_qty, "delta": delta_qty,
                "old_avg": ex["avg"], "new_avg": new_avg,
                "price_now": p.get("price_now"),
            })
            # Update portfolio_positions
            c.execute(
                """UPDATE portfolio_positions SET quantity=?, entry_price=?, notes=?
                   WHERE ticker=? AND active=1""",
                (new_qty, new_avg, f"JPM positions.csv sync {today}", tk),
            )
            # If positive delta, add synthetic lot for the addition
            if delta_qty > 0.0001:
                # Estimate unit cost of the new lot: assume it's close to price_now
                est_unit = p.get("price_now") or new_avg
                total_cost_new_lot = delta_qty * est_unit
                c.execute(
                    """INSERT INTO tax_lots
                         (ticker, acquisition_date, quantity, unit_cost, total_cost,
                          tax_term, days_held, source, imported_at, active, notes)
                       VALUES (?,?,?,?,?,?,?,'positions_csv_delta',?,1,?)""",
                    (tk, today, delta_qty, est_unit, total_cost_new_lot,
                     "Short", 0, now,
                     f"Synthetic delta lot +{delta_qty:.4f} sh (est @ ${est_unit:.2f})"),
                )
        c.commit()
    return diffs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file")
    args = ap.parse_args()

    p = Path(args.file).expanduser().resolve()
    if not p.exists():
        print(f"[erro] {p}")
        return 1
    print(f"Parsing {p}...")
    positions, cash = parse(p)
    print(f"  positions: {len(positions)} tickers")
    print(f"  cash sweep: ${cash['sweep']}  debit: ${cash['debit']}")

    diffs = sync_positions(positions)
    print(f"\n  NEW tickers: {len(diffs['new_tickers'])}")
    for p in diffs["new_tickers"]:
        print(f"    + {p['ticker']:<6}  qty={p['quantity']}  @ ${p['unit_cost']}")
    print(f"\n  QTY CHANGED: {len(diffs['qty_changed'])}")
    for d in diffs["qty_changed"]:
        print(f"    ~ {d['ticker']:<6}  {d['old_qty']:.4f} → {d['new_qty']:.4f}  "
              f"(Δ {d['delta']:+.4f})  avg ${d['old_avg']:.2f} → ${d['new_avg']:.2f}")
    print(f"\n  unchanged: {len(diffs['unchanged'])}")

    # Update cash (net = sweep + debit)
    if cash["sweep"] is not None:
        net = cash["sweep"] + (cash["debit"] or 0)
        with sqlite3.connect(DB_US) as c:
            c.execute(
                """INSERT INTO broker_cash (broker, currency, amount, as_of)
                   VALUES (?,?,?,?)
                   ON CONFLICT(broker, currency) DO UPDATE SET
                     amount=excluded.amount, as_of=excluded.as_of""",
                ("JPM", "USD", net, date.today().isoformat()),
            )
            c.commit()
        print(f"\n  net cash JPM: ${net:+.2f} (sweep {cash['sweep']} + debit {cash['debit']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
