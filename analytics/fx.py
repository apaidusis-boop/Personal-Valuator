"""FX layer — conversão USD/BRL via PTAX (BCB SGS série 1).

Fonte: tabela `series` em `data/br_investments.db`, series_id='USDBRL_PTAX'.

Uso:
    from analytics.fx import usd_to_brl, brl_to_usd, fx_rate, total_portfolio_brl

    r = fx_rate("2026-04-22")        # 4.9653
    brl = usd_to_brl(1000)            # usa taxa mais recente
    brl = usd_to_brl(1000, "2026-04-22")
"""
from __future__ import annotations

import sqlite3
from datetime import date
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"


@lru_cache(maxsize=128)
def fx_rate(iso_date: str | None = None) -> float:
    """PTAX USDBRL para a data (ou mais recente disponível).

    Se `iso_date` é None ou futura, usa a última observação.
    Se `iso_date` não tem PTAX (weekend/holiday), usa a última anterior.
    """
    with sqlite3.connect(DB_BR) as c:
        if iso_date:
            r = c.execute(
                """SELECT value FROM series
                   WHERE series_id='USDBRL_PTAX' AND date<=?
                   ORDER BY date DESC LIMIT 1""",
                (iso_date,),
            ).fetchone()
        else:
            r = c.execute(
                """SELECT value FROM series
                   WHERE series_id='USDBRL_PTAX'
                   ORDER BY date DESC LIMIT 1"""
            ).fetchone()
    if not r:
        raise ValueError("PTAX não disponível — correr fetchers/bcb_fetcher.py")
    return float(r[0])


def usd_to_brl(amount_usd: float, iso_date: str | None = None) -> float:
    return amount_usd * fx_rate(iso_date)


def brl_to_usd(amount_brl: float, iso_date: str | None = None) -> float:
    return amount_brl / fx_rate(iso_date)


def total_portfolio_brl(iso_date: str | None = None) -> dict:
    """Market value agregado BR + US convertido para BRL.

    Usa preço mais recente em `prices` × `quantity` em `portfolio_positions`.
    Devolve breakdown por mercado + total + FX usado.
    """
    DB_US = ROOT / "data" / "us_investments.db"
    rate = fx_rate(iso_date)

    def _mv(db: Path) -> tuple[float, int]:
        total = 0.0
        n = 0
        with sqlite3.connect(db) as c:
            for tk, qty in c.execute(
                "SELECT ticker, quantity FROM portfolio_positions WHERE active=1"
            ):
                row = c.execute(
                    "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
                    (tk,),
                ).fetchone()
                if row:
                    total += row[0] * qty
                    n += 1
        return total, n

    mv_br, n_br = _mv(DB_BR)
    mv_us, n_us = _mv(DB_US)
    mv_us_in_brl = mv_us * rate

    return {
        "br_mv_brl": round(mv_br, 2),
        "us_mv_usd": round(mv_us, 2),
        "us_mv_brl": round(mv_us_in_brl, 2),
        "total_brl": round(mv_br + mv_us_in_brl, 2),
        "total_usd": round((mv_br / rate) + mv_us, 2),
        "fx_ptax": rate,
        "fx_date": iso_date or "latest",
        "holdings_br": n_br,
        "holdings_us": n_us,
    }


def __cli():
    import argparse, json, sys
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--total", action="store_true", help="Portfolio agregado BR+US em BRL")
    ap.add_argument("--rate", action="store_true", help="Mostra PTAX")
    ap.add_argument("--date", help="ISO date (default: latest)")
    ap.add_argument("--usd", type=float, help="Converte USD→BRL")
    ap.add_argument("--brl", type=float, help="Converte BRL→USD")
    args = ap.parse_args()
    if args.total:
        print(json.dumps(total_portfolio_brl(args.date), indent=2))
    elif args.rate:
        print(f"USDBRL PTAX {args.date or '(latest)'}: {fx_rate(args.date):.4f}")
    elif args.usd is not None:
        print(f"${args.usd:,.2f} USD = R${usd_to_brl(args.usd, args.date):,.2f} BRL")
    elif args.brl is not None:
        print(f"R${args.brl:,.2f} BRL = ${brl_to_usd(args.brl, args.date):,.2f} USD")
    else:
        ap.print_help()


if __name__ == "__main__":
    __cli()
