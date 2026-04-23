"""tx — regista transacções (buy/sell) no portfolio_positions.

Writes uma nova row com active=1 (buy) ou marca row existente active=0 com
exit_price/exit_date (sell). Notes são preservadas.

Uso:
    python scripts/tx_cli.py buy ACN 2 176.50 "thesis turnaround after Q2"
    python scripts/tx_cli.py sell TEN 35 38.76 "distress signal converged"
    python scripts/tx_cli.py list --ticker ACN
    python scripts/tx_cli.py list --recent 30
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _market_of(ticker: str) -> str:
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
                return market
    return "br" if ticker[-1].isdigit() else "us"


def buy(ticker: str, qty: float, price: float, notes: str) -> dict:
    market = _market_of(ticker)
    db = DB_BR if market == "br" else DB_US
    today = date.today().isoformat()
    with sqlite3.connect(db) as c:
        # Se já existe active, avisa mas cria adicional (lot management)
        existing = c.execute(
            "SELECT quantity, entry_price FROM portfolio_positions WHERE ticker=? AND active=1",
            (ticker,),
        ).fetchone()
        if existing:
            # Combina em posição pesada existente (weighted avg)
            old_qty, old_px = existing
            new_qty = old_qty + qty
            new_avg = (old_qty * old_px + qty * price) / new_qty if new_qty else price
            c.execute(
                """UPDATE portfolio_positions
                   SET quantity=?, entry_price=?, notes=?
                   WHERE ticker=? AND active=1""",
                (new_qty, new_avg, f"{notes} (avg merge)", ticker),
            )
            c.commit()
            return {
                "action": "merged_into_existing", "ticker": ticker, "market": market,
                "old_qty": old_qty, "old_avg": old_px,
                "added_qty": qty, "added_price": price,
                "new_qty": new_qty, "new_avg": round(new_avg, 4),
            }
        # Nova posição
        c.execute(
            """INSERT INTO portfolio_positions
                 (ticker, weight, entry_date, entry_price, active, quantity, notes)
               VALUES (?, 0, ?, ?, 1, ?, ?)""",
            (ticker, today, price, qty, notes),
        )
        c.commit()
        return {
            "action": "inserted", "ticker": ticker, "market": market,
            "qty": qty, "price": price, "date": today,
        }


def sell(ticker: str, qty: float, price: float, notes: str) -> dict:
    market = _market_of(ticker)
    db = DB_BR if market == "br" else DB_US
    today = date.today().isoformat()
    with sqlite3.connect(db) as c:
        existing = c.execute(
            """SELECT quantity, entry_price, entry_date, notes
               FROM portfolio_positions WHERE ticker=? AND active=1""",
            (ticker,),
        ).fetchone()
        if not existing:
            return {"action": "error", "error": f"nenhuma posição activa em {ticker}"}
        old_qty, old_px, entry_date, old_notes = existing
        if qty > old_qty + 1e-6:
            return {"action": "error", "error": f"qty {qty} > posição actual {old_qty}"}

        if abs(qty - old_qty) < 1e-6:
            # full exit
            c.execute(
                """UPDATE portfolio_positions
                   SET active=0, exit_date=?, exit_price=?, notes=?
                   WHERE ticker=? AND active=1""",
                (today, price, f"{old_notes} | EXIT: {notes}", ticker),
            )
            c.commit()
            pnl_pct = (price / old_px - 1) * 100 if old_px else None
            return {
                "action": "full_exit", "ticker": ticker, "market": market,
                "qty": old_qty, "entry_price": old_px, "exit_price": price,
                "pnl_pct": round(pnl_pct, 2) if pnl_pct is not None else None,
            }
        # partial exit: reduz qty restante, cria row histórica do vendido
        remaining = old_qty - qty
        c.execute(
            """UPDATE portfolio_positions SET quantity=? WHERE ticker=? AND active=1""",
            (remaining, ticker),
        )
        c.execute(
            """INSERT INTO portfolio_positions
                 (ticker, weight, entry_date, entry_price, active, quantity, notes,
                  exit_date, exit_price)
               VALUES (?, 0, ?, ?, 0, ?, ?, ?, ?)""",
            (ticker, entry_date, old_px, qty, f"partial exit: {notes}", today, price),
        )
        c.commit()
        pnl_pct = (price / old_px - 1) * 100 if old_px else None
        return {
            "action": "partial_exit", "ticker": ticker, "market": market,
            "qty_sold": qty, "qty_remaining": remaining,
            "entry_price": old_px, "exit_price": price,
            "pnl_pct": round(pnl_pct, 2) if pnl_pct is not None else None,
        }


def list_tx(ticker: str | None = None, recent_days: int | None = None) -> list[tuple]:
    from datetime import timedelta
    out: list[tuple] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            q = """SELECT ticker, quantity, entry_price, entry_date, exit_price, exit_date,
                          active, notes FROM portfolio_positions"""
            conds: list[str] = []
            args: list = []
            if ticker:
                conds.append("ticker=?")
                args.append(ticker)
            if recent_days is not None:
                cutoff = (date.today() - timedelta(days=recent_days)).isoformat()
                conds.append("(entry_date >= ? OR exit_date >= ?)")
                args.extend([cutoff, cutoff])
            if conds:
                q += " WHERE " + " AND ".join(conds)
            q += " ORDER BY COALESCE(exit_date, entry_date) DESC"
            for r in c.execute(q, args):
                out.append((market, *r))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("buy")
    b.add_argument("ticker")
    b.add_argument("qty", type=float)
    b.add_argument("price", type=float)
    b.add_argument("notes", nargs="*", default=[""])

    s = sub.add_parser("sell")
    s.add_argument("ticker")
    s.add_argument("qty", type=float)
    s.add_argument("price", type=float)
    s.add_argument("notes", nargs="*", default=[""])

    l = sub.add_parser("list")
    l.add_argument("--ticker")
    l.add_argument("--recent", type=int, default=None)

    args = ap.parse_args()

    if args.cmd == "buy":
        res = buy(args.ticker.upper(), args.qty, args.price, " ".join(args.notes))
        print(res)
    elif args.cmd == "sell":
        res = sell(args.ticker.upper(), args.qty, args.price, " ".join(args.notes))
        print(res)
    elif args.cmd == "list":
        rows = list_tx(args.ticker.upper() if args.ticker else None, args.recent)
        print(f"{'Mkt':<4}{'Ticker':<10}{'Qty':<8}{'Entry':<10}{'EntryDate':<12}{'Exit':<10}{'ExitDate':<12}{'A':<3}Notes")
        for r in rows:
            market, tk, qty, entry, ed, ep, xd, active, notes = r
            ep_s = f"{ep:.2f}" if ep else "—"
            xd_s = xd or "—"
            print(f"{market:<4}{tk:<10}{qty:<8.1f}{entry or 0:<10.2f}{ed or '—':<12}{ep_s:<10}{xd_s:<12}{'Y' if active else 'N':<3}{(notes or '')[:50]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
