"""DRIP Quality Optimizer — US dividend portfolio.

Pontua cada posição num score composto (0-100) baseado em:
  - Streak de dividendos (profundidade histórica)
  - Div growth 5y (compound potential)
  - Chowder number (DY + growth)
  - Screen score (qualidade Buffett/Graham)
  - Sustentabilidade (payout ratio)

Para cada ticker, simula: "se eu investisse $1.000 hoje, quanto receberia em
dividendos acumulados em 15 anos?" — a métrica-chave para optimização DRIP.

Depois calcula a alocação óptima de um aporte específico entre os top-N
tickers, respeitando limites de concentração sectorial.

Uso:
    python scripts/drip_optimizer.py                      # analisa tudo
    python scripts/drip_optimizer.py --cash 3644          # optimiza aporte
    python scripts/drip_optimizer.py --top 4              # top-N holdings
    python scripts/drip_optimizer.py --max-sector 0.30    # cap sectorial
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

from scripts.drip_projection import (
    derive_scenarios, _annual_divs_per_share, _ttm_div_per_share,
    _latest_fundamentals, project_drip,
)

DB_US = ROOT / "data" / "us_investments.db"


def quality_score(streak: int | None, div_growth_5y: float | None,
                  dy: float, screen_score: float, payout: float | None,
                  is_aristocrat: bool) -> tuple[float, dict]:
    """DRIP Quality Score 0-100, ponderado para holdings de income de longo prazo.

    Componentes:
    - Streak    (30 pts): anos consecutivos de dividendo. 25a = full. Aristocrat bump +5.
    - Growth    (25 pts): div growth 5y. 10%+ = full.
    - Chowder   (20 pts): DY + growth. 12+ = full (regra Chowder).
    - Screen    (15 pts): score Buffett/Graham.
    - Payout    (10 pts): sustentabilidade. <60% = full; 100%+ = 0.
    """
    breakdown = {}

    # Streak (30 pts)
    if streak is None:
        streak_pts = 0
    else:
        streak_pts = min(streak / 25.0, 1.0) * 25.0
        if is_aristocrat:
            streak_pts = min(streak_pts + 5.0, 30.0)
    breakdown["streak"] = round(streak_pts, 1)

    # Growth (25 pts)
    if div_growth_5y is None:
        growth_pts = 0
    else:
        growth_pts = max(0, min(div_growth_5y / 0.10, 1.0)) * 25.0
    breakdown["growth"] = round(growth_pts, 1)

    # Chowder (20 pts) — DY + growth (percent sum)
    growth_val = div_growth_5y or 0
    chowder = dy * 100 + growth_val * 100
    chowder_pts = max(0, min(chowder / 12.0, 1.0)) * 20.0
    breakdown["chowder"] = round(chowder_pts, 1)

    # Screen (15 pts)
    screen_pts = (screen_score or 0) * 15.0
    breakdown["screen"] = round(screen_pts, 1)

    # Payout sustainability (10 pts)
    if payout is None:
        payout_pts = 5.0  # neutro
    elif payout <= 0.60:
        payout_pts = 10.0
    elif payout >= 1.00:
        payout_pts = 0
    else:
        payout_pts = (1.0 - payout) / 0.40 * 10.0
    breakdown["payout"] = round(payout_pts, 1)

    total = streak_pts + growth_pts + chowder_pts + screen_pts + payout_pts
    return round(total, 1), breakdown


def projected_income_15y(conn, ticker: str, test_amount: float = 1000.0) -> dict:
    """Simula $test_amount investidos hoje: shares, income 15y acumulado."""
    px_row = conn.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (ticker,)
    ).fetchone()
    if not px_row or not px_row[0]:
        return {"ok": False}
    lp = px_row[0]
    sector_row = conn.execute("SELECT sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
    sector = sector_row[0] if sector_row else ""

    shares = test_amount / lp
    ttm = _ttm_div_per_share(conn, ticker, date.today().isoformat())
    annual = _annual_divs_per_share(conn, ticker)
    fund = _latest_fundamentals(conn, ticker)
    scen = derive_scenarios(ticker, lp, ttm, annual, fund, conn, sector)

    # Projecta 15y — Base
    sh_15, px_15, divs_15, mv_15 = project_drip(
        shares, lp, ttm, scen["base"]["g"], scen["base"]["md"], 15
    )
    sh_10, _, divs_10, mv_10 = project_drip(
        shares, lp, ttm, scen["base"]["g"], scen["base"]["md"], 10
    )
    sh_5, _, divs_5, mv_5 = project_drip(
        shares, lp, ttm, scen["base"]["g"], scen["base"]["md"], 5
    )

    # Income final (ano 15): shares × div per share no ano 15
    d_15 = ttm * (1 + scen["base"]["g"]) ** 15
    income_year_15 = sh_15 * d_15

    return {
        "ok": True,
        "last_price": lp,
        "shares_today": shares,
        "ttm_ps": ttm,
        "dy": ttm / lp if lp else 0,
        "scen_g": scen["base"]["g"],
        "scen_md": scen["base"]["md"],
        "divs_accumulated_5y": divs_5,
        "divs_accumulated_10y": divs_10,
        "divs_accumulated_15y": divs_15,
        "mv_15y": mv_15,
        "income_year_15": income_year_15,
        "drip_efficiency": divs_15 / test_amount,  # income total / capital
    }


def load_scorecard(conn, include_watchlist: bool = False) -> list[dict]:
    """Devolve todos os tickers pagadores de dividendos com métricas DRIP."""
    where = "is_holding=1" if not include_watchlist else "1=1"
    tickers = [r[0] for r in conn.execute(
        f"SELECT ticker FROM companies WHERE currency='USD' AND {where}"
    ).fetchall()]

    as_of = date.today().isoformat()
    out: list[dict] = []
    for t in tickers:
        px_row = conn.execute(
            "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1", (t,)
        ).fetchone()
        if not px_row:
            continue
        lp = px_row[0]
        ttm = _ttm_div_per_share(conn, t, as_of)
        if ttm == 0:
            continue  # sem dividendo = fora do escopo DRIP

        fund = _latest_fundamentals(conn, t)
        annual = _annual_divs_per_share(conn, t)

        # div growth 5y
        years = sorted(annual.keys())
        div_5y = None
        if len(years) >= 6:
            w = years[-6:-1]
            if annual[w[0]] > 0:
                div_5y = (annual[w[-1]] / annual[w[0]]) ** (1 / 4) - 1

        # payout ratio (TTM_div_ps / EPS)
        eps = fund.get("eps")
        payout = (ttm / eps) if eps and eps > 0 else None
        if payout is not None and payout > 2.0:
            payout = None  # provavelmente data bug

        # score screen
        sc_row = conn.execute(
            "SELECT score FROM scores WHERE ticker=? "
            "AND run_date=(SELECT MAX(run_date) FROM scores WHERE ticker=?)", (t, t)
        ).fetchone()
        screen = sc_row[0] if sc_row else 0

        streak = fund.get("streak")
        arist = bool(fund.get("aristocrat"))
        dy = ttm / lp if lp else 0

        qs, breakdown = quality_score(streak, div_5y, dy, screen, payout, arist)
        proj = projected_income_15y(conn, t, test_amount=1000.0)

        co_row = conn.execute(
            "SELECT name, sector FROM companies WHERE ticker=?", (t,)
        ).fetchone()
        name, sector = co_row if co_row else ("", "")

        # posição actual
        pp_row = conn.execute(
            "SELECT quantity FROM portfolio_positions WHERE ticker=? AND active=1", (t,)
        ).fetchone()
        cur_qty = pp_row[0] if pp_row else 0

        out.append({
            "ticker": t, "name": name, "sector": sector,
            "last_price": lp, "dy": dy, "ttm_ps": ttm,
            "streak": streak, "aristocrat": arist,
            "div_growth_5y": div_5y,
            "payout": payout,
            "screen": screen,
            "quality": qs, "breakdown": breakdown,
            "is_holding": cur_qty > 0,
            "cur_qty": cur_qty,
            "cur_mv": cur_qty * lp,
            **proj,
        })
    return out


def optimize_allocation(scorecard: list[dict], cash: float,
                        top_n: int = 5, max_sector: float = 0.40) -> list[dict]:
    """Aloca `cash` aos top-N tickers por DRIP efficiency (income 15y / $).
    Pesa proporcionalmente à quality_score, mas respeita max sectorial."""
    eligible = [r for r in scorecard if r.get("ok") and r["quality"] >= 40]
    eligible.sort(key=lambda r: (-r["drip_efficiency"], -r["quality"]))
    pool = eligible[:top_n]
    if not pool:
        return []

    # Pesos proporcionais a quality (não à eff — income gain é consequência)
    total_q = sum(r["quality"] for r in pool)
    raw_alloc = {r["ticker"]: (r["quality"] / total_q) * cash for r in pool}

    # Aplica cap sectorial
    sector_sums: dict[str, float] = defaultdict(float)
    for r in pool:
        sector_sums[r["sector"]] += raw_alloc[r["ticker"]]

    max_per_sector = cash * max_sector
    # Iterações simples: se um sector excede, realoca o excedente proporcionalmente aos outros
    for _ in range(3):
        over = {s: v - max_per_sector for s, v in sector_sums.items() if v > max_per_sector}
        if not over:
            break
        excess = sum(over.values())
        # tira pro-rata dos tickers do sector over
        for s, v in over.items():
            scale = (v - max_per_sector) / v
            for r in pool:
                if r["sector"] == s:
                    raw_alloc[r["ticker"]] -= raw_alloc[r["ticker"]] * scale
        # recalcula sector_sums
        sector_sums = defaultdict(float)
        for r in pool:
            sector_sums[r["sector"]] += raw_alloc[r["ticker"]]
        # redistribui o que sobrou para não-over
        unassigned = cash - sum(raw_alloc.values())
        non_over = [r for r in pool if sector_sums[r["sector"]] < max_per_sector]
        if non_over and unassigned > 0.01:
            tot = sum(r["quality"] for r in non_over)
            for r in non_over:
                raw_alloc[r["ticker"]] += unassigned * r["quality"] / tot
            sector_sums = defaultdict(float)
            for r in pool:
                sector_sums[r["sector"]] += raw_alloc[r["ticker"]]

    result = []
    for r in pool:
        amt = raw_alloc[r["ticker"]]
        sh_add = amt / r["last_price"]
        inc_add = sh_add * r["ttm_ps"]
        result.append({
            **r,
            "alloc_amount": amt,
            "alloc_shares": sh_add,
            "alloc_income": inc_add,
            "alloc_pct": amt / cash if cash else 0,
        })
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cash", type=float, default=0.0,
                    help="Aporte a optimizar. 0 = só análise")
    ap.add_argument("--top", type=int, default=5,
                    help="Top-N holdings para o pool de alocação")
    ap.add_argument("--max-sector", type=float, default=0.40,
                    help="% max por sector na alocação (default 0.40)")
    ap.add_argument("--include-watchlist", action="store_true",
                    help="inclui watchlist (promote candidates)")
    args = ap.parse_args()

    conn = sqlite3.connect(DB_US)
    scorecard = load_scorecard(conn, include_watchlist=args.include_watchlist)
    scorecard.sort(key=lambda r: -r["quality"])

    print("=" * 116)
    print(f"DRIP QUALITY SCORECARD — US dividend holdings")
    print("=" * 116)
    print(f"  {'Ticker':<7}{'Quality':>8}{'Breakdown (streak/growth/chowder/screen/payout)':<50}"
          f"{'DY':>7}{'Streak':>8}{'Div5y':>9}{'$1k→15y':>11}")
    for r in scorecard:
        b = r["breakdown"]
        bd = f"{b['streak']:>4.1f}/{b['growth']:>4.1f}/{b['chowder']:>4.1f}/{b['screen']:>4.1f}/{b['payout']:>4.1f}"
        g5 = f"{r['div_growth_5y']*100:+5.2f}%" if r['div_growth_5y'] is not None else "    -"
        streak = f"{int(r['streak'])}a{'★' if r['aristocrat'] else ''}" if r['streak'] else "-"
        income_15 = f"${r['divs_accumulated_15y']:>7.0f}" if r.get("ok") else "-"
        print(f"  {r['ticker']:<6}{r['quality']:>7.1f}  {bd:<50}{r['dy']*100:>6.2f}%{streak:>8}{g5:>9}  {income_15:>9}")

    # Separação por tier
    tier_a = [r for r in scorecard if r["quality"] >= 70]
    tier_b = [r for r in scorecard if 50 <= r["quality"] < 70]
    tier_c = [r for r in scorecard if r["quality"] < 50]
    print(f"\n  Tier A (quality ≥70 — core DRIP):  {len(tier_a)} → " + ", ".join(r["ticker"] for r in tier_a))
    print(f"  Tier B (50-70 — secundários):       {len(tier_b)} → " + ", ".join(r["ticker"] for r in tier_b))
    print(f"  Tier C (<50 — marginais):            {len(tier_c)} → " + ", ".join(r["ticker"] for r in tier_c))

    # Eficiência $1k → 15y
    print(f"\n=== $1.000 investido hoje → income 15y (Base) ===")
    eff = [r for r in scorecard if r.get("ok")]
    eff.sort(key=lambda r: -r["drip_efficiency"])
    print(f"  {'Ticker':<7}{'$→15y':>9}{'eff':>7}{'Year 15 income':>18}{'MV 15y':>13}  Sector")
    for r in eff[:15]:
        print(f"  {r['ticker']:<6}  ${r['divs_accumulated_15y']:>6.0f}  {r['drip_efficiency']:>5.2f}x"
              f"     ${r['income_year_15']:>8.0f}    ${r['mv_15y']:>8,.0f}   {r['sector']}")

    # Alocação óptima
    if args.cash > 0:
        print(f"\n" + "=" * 116)
        print(f"ALOCAÇÃO ÓPTIMA de $ {args.cash:,.2f}  (top-{args.top}, cap sectorial {args.max_sector*100:.0f}%)")
        print(f"=" * 116)
        alloc = optimize_allocation(scorecard, args.cash, top_n=args.top, max_sector=args.max_sector)
        print(f"  {'Ticker':<7}{'%':>6}{'$ Alloc':>11}{'Shares':>10}{'+Inc/yr':>10}{'Quality':>9}  Sector")
        total_add_inc = 0
        for a in alloc:
            total_add_inc += a["alloc_income"]
            print(f"  {a['ticker']:<6}{a['alloc_pct']*100:>5.1f}%  ${a['alloc_amount']:>8,.2f}"
                  f"  {a['alloc_shares']:>8.2f}  ${a['alloc_income']:>7.2f}{a['quality']:>8.1f}  {a['sector']}")
        print(f"\n  Income adicional anual: $ {total_add_inc:.2f}")

        # Projecção combined 15y dos tickers alocados
        print(f"\n  PROJECÇÃO 15y DO APORTE (Base):")
        tot_divs_15 = sum(a["alloc_amount"] * a["drip_efficiency"] for a in alloc)
        tot_mv_15 = sum(a["alloc_amount"] / a["last_price"] * a["mv_15y"] / 1000 * 1000 for a in alloc)
        # recalcular: para cada alloc, shares_add * mv_by_dollar_15y
        tot_mv_15 = 0
        for a in alloc:
            # mv_15y é para $1k test. escalar pelo valor real.
            scale = a["alloc_amount"] / 1000.0
            tot_mv_15 += a["mv_15y"] * scale
        tot_income_15 = sum(a["alloc_income"] * (1 + a["scen_g"])**15 * (a["mv_15y"]/(1000 if a["last_price"] else 1)) for a in alloc) if False else 0
        # simpler: re-simulate with real dollar amount
        tot_income_year15 = 0
        for a in alloc:
            scale = a["alloc_amount"] / 1000.0
            tot_income_year15 += a["income_year_15"] * scale
        print(f"    Dividendos acumulados 15y (só este aporte): $ {tot_divs_15:,.2f}")
        print(f"    MV do aporte em 15y (com DRIP):              $ {tot_mv_15:,.2f}  ({tot_mv_15/args.cash:.2f}x)")
        print(f"    Income anual ano 15 (só este aporte):        $ {tot_income_year15:,.2f}")

    conn.close()


if __name__ == "__main__":
    main()
