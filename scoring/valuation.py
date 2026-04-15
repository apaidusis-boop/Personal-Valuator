"""Motor de valuation — Gordon Growth (DDM) para empresas pagadoras.

Nunca toca na rede. Lê dividends_annual + fundamentals + prices e escreve
em valuations.

Modelo Gordon:
    P = D1 / (r - g)      onde D1 = D0 * (1 + g)

Premissas:
    g   = CAGR dos dividendos nos últimos 5 anos completos, com cap
          em (r - safety_spread) para evitar denominador a zerar.
    r   = discount rate. Por mercado:
            BR: 14% (SELIC ~11% + prémio de risco de equity ~3%)
            US: 9%  (10Y ~4.5% + prémio ~4.5%)
    MoS = margem de segurança de 25% aplicada ao fair value para
          obter o preço de entrada ("compra abaixo de").

Tese (thesis break) — condições que invalidam a recomendação, guardadas
em details_json.thesis:
    - DY cai abaixo de 4% (BR) ou 2% (US)
    - ROE < 10% dois trimestres seguidos
    - Corte de dividendos >30% YoY
    - Payout consistentemente > 100%

Uso:
    python scoring/valuation.py              # ITSA4
    python scoring/valuation.py PRIO3
"""
from __future__ import annotations

import argparse
import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

DISCOUNT_RATE = {"br": 0.14, "us": 0.09}
# g tem dois caps para evitar o DDM explodir:
#   (a) spread mínimo vs r — denominador nunca fica demasiado pequeno
#   (b) cap absoluto — nenhuma empresa madura sustenta crescimento
#       de dividendos a longo prazo acima deste valor
SAFETY_SPREAD = 0.04
ABSOLUTE_G_CAP = {"br": 0.06, "us": 0.05}
MARGIN_OF_SAFETY = 0.25      # preço de entrada = fair × (1 - 0.25)
CAGR_WINDOW = 5

THESIS_BREAK_BR = [
    {"id": "dy_min",         "label": "DY cair abaixo de 4%",                  "threshold": 0.04},
    {"id": "roe_min",        "label": "ROE cair abaixo de 10%",                "threshold": 0.10},
    {"id": "div_cut",        "label": "Corte de dividendo > 30% YoY",          "threshold": -0.30},
    {"id": "streak_break",   "label": "Quebra do histórico de dividendos",     "threshold": None},
]
THESIS_BREAK_US = [
    {"id": "dy_min",       "label": "DY cair abaixo de 2%",   "threshold": 0.02},
    {"id": "roe_min",      "label": "ROE cair abaixo de 10%", "threshold": 0.10},
    {"id": "div_cut",      "label": "Corte de dividendo > 20% YoY",       "threshold": -0.20},
    {"id": "streak_break", "label": "Quebra do aristocrat / streak 10y",  "threshold": None},
]


def load_inputs(conn: sqlite3.Connection, ticker: str) -> dict | None:
    co = conn.execute(
        "SELECT ticker, name, sector, currency FROM companies WHERE ticker=?",
        (ticker,),
    ).fetchone()
    if not co:
        return None
    fund = conn.execute(
        """SELECT eps, bvps, roe, pe, pb, dy, dividend_streak_years
           FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
        (ticker,),
    ).fetchone()
    price = conn.execute(
        "SELECT close, date FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    divs = conn.execute(
        "SELECT year, amount FROM dividends_annual WHERE ticker=? ORDER BY year ASC",
        (ticker,),
    ).fetchall()
    return {
        "company": {"ticker": co[0], "name": co[1], "sector": co[2], "currency": co[3]},
        "fundamentals": dict(zip(
            ["eps", "bvps", "roe", "pe", "pb", "dy", "streak"], fund
        )) if fund else {},
        "price": {"close": price[0], "date": price[1]} if price else {},
        "dividends": [{"year": y, "amount": a} for y, a in divs],
    }


def compute_cagr(divs: list[dict], window: int = CAGR_WINDOW) -> tuple[float | None, int, int | None]:
    """Devolve (cagr, n_anos_usados, ano_base). Ignora o ano corrente se
    ainda não tiver pagamento consolidado (amount == 0 ou muito baixo)."""
    current = datetime.now().year
    clean = [d for d in divs if d["amount"] and d["amount"] > 0 and d["year"] < current]
    if len(clean) < 2:
        return None, len(clean), None
    clean.sort(key=lambda d: d["year"])
    end = clean[-1]
    start_idx = max(0, len(clean) - 1 - window)
    start = clean[start_idx]
    years = end["year"] - start["year"]
    if years <= 0:
        return None, len(clean), None
    cagr = (end["amount"] / start["amount"]) ** (1 / years) - 1
    return cagr, years, start["year"]


def gordon_fair_value(d0: float, g: float, r: float) -> float:
    d1 = d0 * (1 + g)
    return d1 / (r - g)


def run(ticker: str, market: str = "br") -> dict:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as conn:
        inputs = load_inputs(conn, ticker)
        if inputs is None:
            raise SystemExit(f"{ticker} não encontrado em {db.name}")

        r = DISCOUNT_RATE[market]
        g_raw, g_years, g_start = compute_cagr(inputs["dividends"])
        g_cap = min(r - SAFETY_SPREAD, ABSOLUTE_G_CAP[market])
        g = min(g_raw, g_cap) if g_raw is not None else None

        # D0 = último ano completo
        current = datetime.now().year
        completed = [d for d in inputs["dividends"] if d["year"] < current and d["amount"] > 0]
        d0 = completed[-1]["amount"] if completed else None

        fair_value = None
        entry_price = None
        notes: list[str] = []

        if d0 is None:
            notes.append("sem dividendo anual consolidado para D0")
        elif g is None:
            notes.append("CAGR de dividendos indisponível (histórico < 2 anos)")
        elif g >= r:
            notes.append(f"g ({g:.2%}) ≥ r ({r:.2%}); modelo Gordon não aplicável")
        else:
            fair_value = gordon_fair_value(d0, g, r)
            entry_price = fair_value * (1 - MARGIN_OF_SAFETY)
            if g_raw is not None and g_raw > g_cap:
                notes.append(f"g cru={g_raw:.2%} limitado ao cap {g_cap:.2%}")

        close = inputs["price"].get("close")
        upside = None
        verdict = None
        if fair_value and close:
            upside = fair_value / close - 1
            if close <= entry_price:
                verdict = "BUY"
            elif close <= fair_value:
                verdict = "HOLD"
            else:
                verdict = "OVERVALUED"

        thesis_break = THESIS_BREAK_BR if market == "br" else THESIS_BREAK_US

        details = {
            "inputs": {
                "d0": d0,
                "g": g,
                "g_raw": g_raw,
                "g_years_window": g_years,
                "g_start_year": g_start,
                "r": r,
                "margin_of_safety": MARGIN_OF_SAFETY,
            },
            "outputs": {
                "fair_value": fair_value,
                "entry_price": entry_price,
                "current_price": close,
                "upside": upside,
                "verdict": verdict,
            },
            "thesis_break": thesis_break,
            "notes": notes,
        }

        run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        conn.execute(
            """INSERT INTO valuations (ticker, run_date, model, fair_value, entry_price, details_json)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(ticker, run_date, model) DO UPDATE SET
                 fair_value=excluded.fair_value,
                 entry_price=excluded.entry_price,
                 details_json=excluded.details_json""",
            (ticker, run_date, "gordon_ddm",
             fair_value, entry_price, json.dumps(details, ensure_ascii=False)),
        )
        conn.commit()

    out = {"ticker": ticker, "run_date": run_date, **details}
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="ITSA4")
    ap.add_argument("--market", choices=["br", "us"], default="br")
    args = ap.parse_args()
    run(args.ticker, args.market)


if __name__ == "__main__":
    main()
