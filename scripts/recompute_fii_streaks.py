"""Recalcula distribution_streak_months para todos os FIIs a partir da
tabela `dividends` (populada por yf_br_fetcher).

Regra: meses consecutivos a contar do mais recente para trás.
Um gap > 1 mês interrompe o streak. Um mês com múltiplos proventos
conta como 1 mês.

Puro: não toca em rede.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "br_investments.db"


def streak_from_dividends(conn: sqlite3.Connection, ticker: str) -> int:
    rows = conn.execute(
        "SELECT DISTINCT substr(ex_date,1,7) FROM dividends WHERE ticker=? ORDER BY 1 DESC",
        (ticker,),
    ).fetchall()
    months = [r[0] for r in rows]
    if not months:
        return 0
    streak = 1
    for i in range(1, len(months)):
        y1, m1 = map(int, months[i - 1].split("-"))
        y2, m2 = map(int, months[i].split("-"))
        if (y1 - y2) * 12 + (m1 - m2) == 1:
            streak += 1
        else:
            break
    return streak


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with sqlite3.connect(DB) as conn:
        tickers = [r[0] for r in conn.execute(
            "SELECT DISTINCT ticker FROM fii_fundamentals"
        )]
        print(f"FIIs a processar: {len(tickers)}")
        for t in sorted(tickers):
            streak = streak_from_dividends(conn, t)
            if streak == 0:
                print(f"  {t}: sem dividendos na DB — skip")
                continue
            conn.execute(
                """UPDATE fii_fundamentals
                   SET distribution_streak_months=?, fetched_at=?
                   WHERE ticker=? AND period_end=(
                     SELECT MAX(period_end) FROM fii_fundamentals WHERE ticker=?
                   )""",
                (streak, now, t, t),
            )
            print(f"  {t}: streak={streak}m")
        conn.commit()


if __name__ == "__main__":
    main()
