"""Seed de portfolio_positions — pesos iguais entre as acções BR.

Simplificação deliberada do Sprint 1: pesos iguais, entry_date = 1 ano
atrás (ou o ponto mais antigo disponível na DB se menos que 1 ano),
entry_price = close nessa data.

Quando (Sprint 2) houver noção real de quando cada posição foi aberta,
substitui-se este seed por um carregamento a partir de um CSV/YAML
com as posições reais.

Uso:
    python scripts/seed_portfolio.py                  # BR stocks, peso igual
    python scripts/seed_portfolio.py --entry 2025-04-15
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB_PATH = ROOT / "data" / "br_investments.db"


def closest_price_on_or_after(conn: sqlite3.Connection, ticker: str, date: str) -> tuple[str, float] | None:
    row = conn.execute(
        "SELECT date, close FROM prices WHERE ticker=? AND date>=? ORDER BY date ASC LIMIT 1",
        (ticker, date),
    ).fetchone()
    if not row:
        row = conn.execute(
            "SELECT date, close FROM prices WHERE ticker=? ORDER BY date ASC LIMIT 1",
            (ticker,),
        ).fetchone()
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry", default=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"))
    args = ap.parse_args()

    with sqlite3.connect(DB_PATH) as conn:
        holdings = [r[0] for r in conn.execute(
            "SELECT ticker FROM companies WHERE is_holding=1 AND sector != 'FII Shopping' "
            "AND sector NOT LIKE 'FII%' ORDER BY ticker"
        ).fetchall()]
        if not holdings:
            raise SystemExit("sem holdings em companies — corre populate_br.py primeiro")

        weight = 1.0 / len(holdings)
        print(f"[seed] {len(holdings)} holdings, peso {weight:.2%} cada, entry_date {args.entry}")

        # Limpa seeds anteriores (mantém esquema simples: uma linha por ticker)
        conn.execute("DELETE FROM portfolio_positions")

        for ticker in holdings:
            row = closest_price_on_or_after(conn, ticker, args.entry)
            if not row:
                print(f"  [skip] {ticker}: sem preço na DB")
                continue
            date, price = row
            conn.execute(
                """INSERT INTO portfolio_positions (ticker, weight, entry_date, entry_price, active)
                   VALUES (?,?,?,?,1)""",
                (ticker, weight, date, float(price)),
            )
            print(f"  [ok]   {ticker}: {date} @ R$ {price:.2f}")
        conn.commit()


if __name__ == "__main__":
    main()
