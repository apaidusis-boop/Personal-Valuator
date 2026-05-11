"""DRIP Quality Optimizer — carteira BR.

Paralelo do drip_optimizer.py mas adaptado às estruturas BR:

1. **Ações não-banco** (VALE3, ITSA4, PRIO3): Graham screen + streak + growth
2. **Bancos** (BBDC4): screen bancário (P/E, P/B, DY alto), relax no ROE
3. **FIIs** (XPML11, VGIR11, BTLG11, RBRX11, PVBI11): distribution streak em MESES,
   spread DY sobre Selic-real, segment (papel/tijolo/híbrido)
4. **ETFs** (LFTB11, IVVB11): classificação separada — LFTB = SELIC tracker,
   IVVB = S&P exposure; fora do DRIP clássico mas importantes como alocação

Thresholds BR refletem realidade macro (Selic 14,75%, DYs altos típicos):
- Chowder cap: 16% (vs 12% US) — mercado BR paga mais
- DY threshold: 8% para full pts (vs 4% US)
- Streak cap: 20a (vs 25a US) — IPOs BR tipicamente mais recentes

Uso:
    python scripts/br_drip_optimizer.py                # análise
    python scripts/br_drip_optimizer.py --cash 10000   # optimiza aporte
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.drip_projection import _annual_divs_per_share, _ttm_div_per_share, _latest_fundamentals

DB_BR = ROOT / "data" / "br_investments.db"


def quality_stock(streak: int | None, growth_5y: float | None,
                  dy: float, screen: float, net_debt_ebitda: float | None,
                  is_bank: bool = False) -> tuple[float, dict]:
    """Quality score para ações BR non-FII non-ETF. Thresholds BR-adjusted."""
    b = {}

    # Streak (25 pts BR — máximos mais baixos que US)
    if streak is None:
        b["streak"] = 0
    else:
        b["streak"] = round(min(streak / 15.0, 1.0) * 25.0, 1)

    # Growth (25 pts — 12%+ full, mais permissivo que US devido inflação BR)
    if growth_5y is None:
        b["growth"] = 0
    else:
        b["growth"] = round(max(0, min(growth_5y / 0.12, 1.0)) * 25.0, 1)

    # DY (20 pts — BR paga alto; 8%+ = full)
    b["dy"] = round(min(dy / 0.08, 1.0) * 20.0, 1)

    # Chowder (10 pts — BR cap em 20%)
    chowder = dy * 100 + (growth_5y or 0) * 100
    b["chowder"] = round(max(0, min(chowder / 20.0, 1.0)) * 10.0, 1)

    # Screen (15 pts)
    b["screen"] = round((screen or 0) * 15.0, 1)

    # Leverage (5 pts) — só aplica a não-bancos
    if is_bank:
        b["leverage"] = 5.0
    elif net_debt_ebitda is None:
        b["leverage"] = 2.5
    elif net_debt_ebitda < 2:
        b["leverage"] = 5.0
    elif net_debt_ebitda > 4:
        b["leverage"] = 0
    else:
        b["leverage"] = round((4 - net_debt_ebitda) / 2 * 5.0, 1)

    total = sum(b.values())
    return round(total, 1), b


def quality_fii(dy_12m: float, pvp: float | None,
                distribution_streak_months: int | None,
                segment: str | None,
                physical_vacancy: float | None,
                spread_selic_real: float | None) -> tuple[float, dict]:
    """Quality score para FIIs. Adaptado ao universo Suno/Baroni.

    Pesos:
      - DY 12m           (25) — 10%+ = full
      - Distribution     (25) — 60 meses (5a) = full
      - P/VP             (20) — ≤0.95 = full, 1.10+ = 0
      - Spread Selic     (15) — DY - (Selic real) positivo = full
      - Liquidez/segment (15) — tijolo < 15% vacância OR papel = full
    """
    b = {}

    # DY 12m (25)
    b["dy_12m"] = round(min(dy_12m / 0.10, 1.0) * 25.0, 1)

    # Distribution streak (25) — em meses
    if distribution_streak_months is None:
        b["distribution"] = 10  # neutro
    else:
        b["distribution"] = round(min(distribution_streak_months / 60.0, 1.0) * 25.0, 1)

    # P/VP (20)
    if pvp is None:
        b["pvp"] = 10
    elif pvp <= 0.95:
        b["pvp"] = 20.0
    elif pvp >= 1.10:
        b["pvp"] = 0
    else:
        b["pvp"] = round((1.10 - pvp) / 0.15 * 20.0, 1)

    # Spread Selic (15)
    if spread_selic_real is None:
        b["spread"] = 7
    elif spread_selic_real >= 0:
        b["spread"] = round(min(spread_selic_real * 100 / 3, 1.0) * 15.0, 1) if spread_selic_real < 0.03 else 15.0
    else:
        b["spread"] = 0

    # Segmento + vacância (15)
    is_papel = segment and any(k in segment.lower() for k in ("papel", "cri", "papéis"))
    if is_papel:
        b["segment"] = 15.0  # papel: ok
    elif physical_vacancy is None:
        b["segment"] = 7.5
    elif physical_vacancy < 0.10:
        b["segment"] = 15.0
    elif physical_vacancy > 0.20:
        b["segment"] = 0
    else:
        b["segment"] = round((0.20 - physical_vacancy) / 0.10 * 15.0, 1)

    total = sum(b.values())
    return round(total, 1), b


def classify_asset(ticker: str, sector: str | None) -> str:
    if sector in ("ETF-RF",): return "etf_selic"
    if sector in ("ETF-US",): return "etf_sp"
    if sector == "Banks": return "bank"
    if sector in ("Holding",): return "holding"
    if ticker.endswith("11") and sector and any(s in sector.lower() for s in
        ("papel", "shopping", "logística", "híbrido", "corporativo", "tijolo", "cri")):
        return "fii"
    return "stock"


def analyze_br_holdings(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT pp.ticker, pp.quantity, pp.entry_price,
               (SELECT close FROM prices p WHERE p.ticker=pp.ticker ORDER BY date DESC LIMIT 1) lp,
               co.name, co.sector
        FROM portfolio_positions pp
        LEFT JOIN companies co ON co.ticker=pp.ticker
        WHERE pp.active=1 AND pp.quantity>0
        ORDER BY pp.ticker
    """).fetchall()

    out = []
    as_of = date.today().isoformat()
    for t, q, ep, lp, nm, sec in rows:
        if not lp:
            continue
        kind = classify_asset(t, sec)
        mv = q * lp
        ttm_ps = _ttm_div_per_share(conn, t, as_of)
        annual = _annual_divs_per_share(conn, t)
        fund = _latest_fundamentals(conn, t)

        dy = ttm_ps / lp if lp else 0

        # div growth 5y
        years = sorted(annual.keys())
        div_5y = None
        if len(years) >= 6:
            w = years[-6:-1]
            if annual[w[0]] > 0:
                div_5y = (annual[w[-1]] / annual[w[0]]) ** (1 / 4) - 1

        # Score depending on kind
        if kind == "fii":
            fii_fund = conn.execute(
                """SELECT pvp, dy_12m, distribution_streak_months, segment_anbima,
                          physical_vacancy
                   FROM fii_fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
                (t,)
            ).fetchone()
            if fii_fund:
                pvp, dy12m, dstream, segment, vac = fii_fund
                dy_use = dy12m or dy
            else:
                pvp = dy12m = dstream = segment = vac = None
                dy_use = dy
            # Spread SELIC: DY - Selic_real (~ Selic nominal - IPCA 12m)
            selic_row = conn.execute(
                "SELECT value FROM series WHERE series_id='SELIC_META' ORDER BY date DESC LIMIT 1"
            ).fetchone()
            selic = selic_row[0]/100.0 if selic_row else 0.1475
            ipca_rows = conn.execute(
                "SELECT value FROM series WHERE series_id='IPCA_MONTHLY' ORDER BY date DESC LIMIT 12"
            ).fetchall()
            ipca12 = 1.0
            for (v,) in ipca_rows:
                ipca12 *= (1+v)
            ipca12 -= 1
            selic_real = selic - ipca12
            spread = (dy_use or 0) - selic_real
            q_score, breakdown = quality_fii(dy_use, pvp, dstream, segment, vac, spread)
        elif kind == "bank":
            q_score, breakdown = quality_stock(
                fund.get("streak"), div_5y, dy,
                0.80,  # BBDC4 screen
                fund.get("net_debt_ebitda"), is_bank=True
            )
        elif kind in ("etf_selic", "etf_sp"):
            # ETFs: quality especial — LFTB tracks Selic, IVVB tracks S&P
            breakdown = {"etf_type": kind}
            if kind == "etf_selic":
                q_score = 85  # aceitável como cash-like com yield Selic
            else:
                q_score = 75  # S&P exposure moderada em BRL
        else:
            sc_row = conn.execute(
                "SELECT score FROM scores WHERE ticker=? "
                "AND run_date=(SELECT MAX(run_date) FROM scores WHERE ticker=?)", (t, t)
            ).fetchone()
            screen = sc_row[0] if sc_row else 0
            q_score, breakdown = quality_stock(
                fund.get("streak"), div_5y, dy, screen,
                fund.get("net_debt_ebitda")
            )

        income_ttm = q * ttm_ps

        out.append({
            "ticker": t, "name": nm, "sector": sec, "kind": kind,
            "qty": q, "entry_price": ep, "last_price": lp, "mv": mv,
            "dy": dy, "ttm_ps": ttm_ps, "income_ttm": income_ttm,
            "div_growth_5y": div_5y,
            "quality": q_score, "breakdown": breakdown,
            "fund": fund,
        })
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cash", type=float, default=0.0)
    args = ap.parse_args()

    conn = sqlite3.connect(DB_BR)
    scorecard = analyze_br_holdings(conn)
    scorecard.sort(key=lambda r: -r["quality"])

    print("=" * 110)
    print("DRIP QUALITY SCORECARD — carteira BR (equity + FIIs + ETFs)")
    print("=" * 110)

    groups = defaultdict(list)
    for r in scorecard:
        groups[r["kind"]].append(r)

    kind_order = ["bank", "holding", "stock", "fii", "etf_selic", "etf_sp"]
    kind_label = {
        "bank": "BANCOS",
        "holding": "HOLDINGS (conglomerado)",
        "stock": "AÇÕES operacionais",
        "fii": "FIIs",
        "etf_selic": "ETF-RF (Selic tracker)",
        "etf_sp": "ETF-US (S&P exposure)",
    }

    for kind in kind_order:
        items = groups.get(kind, [])
        if not items:
            continue
        print(f"\n### {kind_label[kind]}  ({len(items)} tickers)")
        print(f"  {'Ticker':<8}{'Q':>6}{'MV':>14}{'DY':>8}{'Streak/Growth':>16}{'P/VP':>7}{'Notas'}")
        for r in items:
            mv = f"R$ {r['mv']:,.0f}"
            dy_s = f"{r['dy']*100:.2f}%"
            fund = r.get("fund") or {}
            streak = fund.get("streak")
            growth = r.get("div_growth_5y")
            s_g = ""
            if streak is not None or growth is not None:
                s = f"{int(streak)}a" if streak else "-"
                g = f"{growth*100:+.1f}%" if growth is not None else "-"
                s_g = f"{s}/{g}"
            pvp = "-"
            if kind == "fii":
                fii_row = conn.execute(
                    "SELECT pvp FROM fii_fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
                    (r["ticker"],)
                ).fetchone()
                if fii_row and fii_row[0]:
                    pvp = f"{fii_row[0]:.2f}"
            # breakdown summary
            b = r["breakdown"]
            bd_str = " ".join(f"{k}={v}" for k, v in b.items() if k != "etf_type")[:50]
            print(f"  {r['ticker']:<8}{r['quality']:>6.1f}  {mv:>12}  {dy_s:>6}  {s_g:>14}  {pvp:>5}  {bd_str}")

    # Tiers
    tier_a = [r for r in scorecard if r["quality"] >= 70]
    tier_b = [r for r in scorecard if 50 <= r["quality"] < 70]
    tier_c = [r for r in scorecard if r["quality"] < 50]
    print(f"\nTier A (≥70): " + ", ".join(f"{r['ticker']} ({r['quality']})" for r in tier_a))
    print(f"Tier B (50-70): " + ", ".join(f"{r['ticker']} ({r['quality']})" for r in tier_b))
    print(f"Tier C (<50): " + ", ".join(f"{r['ticker']} ({r['quality']})" for r in tier_c))

    # Income totals
    total_mv = sum(r["mv"] for r in scorecard)
    total_inc = sum(r["income_ttm"] for r in scorecard)
    payers = [r for r in scorecard if r["income_ttm"] > 0]
    total_payer_mv = sum(r["mv"] for r in payers)
    blend_dy = sum(r["income_ttm"] for r in payers) / total_payer_mv * 100 if total_payer_mv else 0
    print(f"\nTOTAIS BR: MV R$ {total_mv:,.0f}  |  Income TTM R$ {total_inc:,.0f}/ano  |  DY blend (pagadores) {blend_dy:.2f}%")

    # Alocação óptima
    if args.cash > 0:
        # Pool: só tickers Tier A/B, excluindo ETFs (já altas concentração)
        pool = [r for r in scorecard if r["quality"] >= 60 and r["kind"] not in ("etf_selic", "etf_sp")]
        pool.sort(key=lambda r: -r["quality"])
        top = pool[:6]
        if top:
            total_q = sum(r["quality"] for r in top)
            print(f"\n{'='*110}")
            print(f"ALOCAÇÃO ÓPTIMA de R$ {args.cash:,.2f}  (top-6 Tier A/B, ponderado por quality)")
            print(f"{'='*110}")
            print(f"  {'Ticker':<8}{'%':>6}{'R$ Alloc':>13}{'Shares/cotas':>14}{'+Inc/yr':>12}  Kind")
            for r in top:
                amt = args.cash * r["quality"] / total_q
                sh = amt / r["last_price"]
                inc = sh * r["ttm_ps"]
                print(f"  {r['ticker']:<8}{amt/args.cash*100:>5.1f}%  R$ {amt:>9,.2f}  {sh:>10.2f}    R$ {inc:>6,.2f}  {r['kind']}")

    conn.close()


if __name__ == "__main__":
    main()
