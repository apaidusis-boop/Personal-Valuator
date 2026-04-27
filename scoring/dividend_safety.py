"""Dividend Safety Score 0-100 — forward-looking.

Responde à pergunta "vai manter o dividendo 5+ anos?". Diferente do screen
Graham/Buffett (que avalia *se comprar agora*), este score avalia *se o
dividendo actual é sustentável*.

Componentes (pesos re-normalizados se algum não tiver dados):

  1. PAYOUT RATIO           (35%)  div_ttm / EPS
       <50%  = 35   |  50-70% = 25  |  70-100% = 15  |  >100% = 0
  2. ROE LEVEL              (20%)  capacidade de gerar lucro
       >=15% = 20   |  10-15% = 15  |  5-10%  = 10   |  <5%   = 0
  3. STREAK HISTÓRICO       (25%)  prova empírica
       25y+ (aristocrat) = 25 | 15-25y = 20 | 10-15y = 15 | 5-10y = 8 | <5y = 0
  4. NET DEBT / EBITDA      (20%)  alavancagem
       <1x = 20 | 1-2x = 15 | 2-3x = 10 | 3-4x = 5 | >4x = 0

Verdict:
  SAFE   80-100  — cortar dividendo seria surpresa estrutural
  WATCH  60-79   — razoável mas requer monitoring
  RISK   <60     — red flag em algum componente

CLI:
    python -m scoring.dividend_safety JNJ
    python -m scoring.dividend_safety ITSA4 --market br
    python -m scoring.dividend_safety --all            # scoreia todos holdings
"""
from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


@dataclass
class Component:
    name: str
    weight: float
    raw_value: float | None           # valor numérico (para display)
    score: float | None               # contribuição para o total (0 .. weight)
    verdict: str                      # uma palavra: SAFE | OK | WATCH | RISK | n/a


@dataclass
class SafetyScore:
    ticker: str
    market: str
    total: float                      # 0..100
    verdict: str                      # SAFE / WATCH / RISK / N/A
    components: list[Component] = field(default_factory=list)


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _detect_market(ticker: str) -> str | None:
    for mkt in ("br", "us"):
        with sqlite3.connect(_db(mkt)) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mkt
    return None


def _ttm_div_per_share(conn: sqlite3.Connection, ticker: str) -> float:
    cutoff = (date.today() - timedelta(days=365)).isoformat()
    r = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM dividends "
        "WHERE ticker=? AND ex_date>=? AND amount>0",
        (ticker, cutoff),
    ).fetchone()
    return float(r[0] or 0.0)


def _latest_fund(conn: sqlite3.Connection, ticker: str) -> dict:
    """Read latest fundamentals row. ffo_per_share is US-only (REITs);
    BR schema doesn't have it, so detect column presence first.
    """
    cols = {row[1] for row in conn.execute("PRAGMA table_info(fundamentals)").fetchall()}
    base = ["eps", "bvps", "roe", "pe", "pb", "dy",
            "net_debt_ebitda", "dividend_streak_years", "is_aristocrat"]
    select_cols = list(base)
    if "ffo_per_share" in cols:
        select_cols.append("ffo_per_share")
    r = conn.execute(
        f"SELECT {', '.join(select_cols)} "
        "FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    if not r:
        return {}
    keys = ["eps", "bvps", "roe", "pe", "pb", "dy",
            "net_debt_ebitda", "streak", "aristocrat"]
    if "ffo_per_share" in cols:
        keys.append("ffo")
    return dict(zip(keys, r))


def _is_reit(conn: sqlite3.Connection, ticker: str) -> bool:
    r = conn.execute("SELECT sector FROM companies WHERE ticker=?", (ticker,)).fetchone()
    if not r or not r[0]:
        return False
    s = r[0].lower()
    return "reit" in s or "real estate" in s


# --- Scorers (cada um devolve Component) -----------------------------------

def _score_payout(
    div_ttm: float,
    eps: float | None,
    *,
    ffo: float | None = None,
    is_reit: bool = False,
) -> Component:
    """For REITs use FFO instead of EPS (REIT structure has high non-cash D&A).
    Falls back to EPS if FFO is unavailable.
    """
    if is_reit and ffo and ffo > 0 and div_ttm > 0:
        payout = div_ttm / ffo
        name = "payout_ratio_ffo"
        if payout < 0.7:   return Component(name, 35, payout, 35, "SAFE")
        if payout < 0.85:  return Component(name, 35, payout, 25, "OK")
        if payout < 1.0:   return Component(name, 35, payout, 15, "WATCH")
        return Component(name, 35, payout, 0, "RISK")
    if eps is None or eps <= 0 or div_ttm <= 0:
        return Component("payout_ratio", 35, None, None, "n/a")
    payout = div_ttm / eps
    if payout < 0.5:   return Component("payout_ratio", 35, payout, 35, "SAFE")
    if payout < 0.7:   return Component("payout_ratio", 35, payout, 25, "OK")
    if payout < 1.0:   return Component("payout_ratio", 35, payout, 15, "WATCH")
    return Component("payout_ratio", 35, payout, 0, "RISK")


def _score_roe(roe: float | None) -> Component:
    if roe is None:
        return Component("roe_level", 20, None, None, "n/a")
    # fundamentals guarda ROE como 0.18 ou 18 (varia pelo fetcher); normaliza
    r = roe if abs(roe) > 1.5 else roe * 100  # se veio como 0.18, vira 18
    if r >= 15:  return Component("roe_level", 20, r/100, 20, "SAFE")
    if r >= 10:  return Component("roe_level", 20, r/100, 15, "OK")
    if r >= 5:   return Component("roe_level", 20, r/100, 10, "WATCH")
    return Component("roe_level", 20, r/100, 0, "RISK")


def _score_streak(streak: int | None, aristocrat: int | None) -> Component:
    if streak is None:
        return Component("streak_years", 25, None, None, "n/a")
    s = int(streak)
    if aristocrat or s >= 25:  return Component("streak_years", 25, s, 25, "SAFE")
    if s >= 15:                return Component("streak_years", 25, s, 20, "SAFE")
    if s >= 10:                return Component("streak_years", 25, s, 15, "OK")
    if s >= 5:                 return Component("streak_years", 25, s, 8, "WATCH")
    return Component("streak_years", 25, s, 0, "RISK")


def _score_leverage(net_debt_ebitda: float | None, *, is_reit: bool = False) -> Component:
    if net_debt_ebitda is None:
        return Component("net_debt_ebitda", 20, None, None, "n/a")
    x = float(net_debt_ebitda)
    # Caixa líquida (valor negativo) é positivo para safety.
    if x < 0:   return Component("net_debt_ebitda", 20, x, 20, "SAFE")
    if is_reit:
        # REITs are structurally debt-financed (real estate). Industry norm
        # is ~5-6x. Use softer thresholds anchored at real estate medians.
        if x < 4:   return Component("net_debt_ebitda", 20, x, 20, "SAFE")
        if x < 5.5: return Component("net_debt_ebitda", 20, x, 15, "OK")
        if x < 7:   return Component("net_debt_ebitda", 20, x, 10, "WATCH")
        if x < 9:   return Component("net_debt_ebitda", 20, x, 5, "RISK")
        return Component("net_debt_ebitda", 20, x, 0, "RISK")
    if x < 1:   return Component("net_debt_ebitda", 20, x, 20, "SAFE")
    if x < 2:   return Component("net_debt_ebitda", 20, x, 15, "OK")
    if x < 3:   return Component("net_debt_ebitda", 20, x, 10, "WATCH")
    if x < 4:   return Component("net_debt_ebitda", 20, x, 5, "RISK")
    return Component("net_debt_ebitda", 20, x, 0, "RISK")


# --- Aggregation -----------------------------------------------------------

def compute(ticker: str, market: str | None = None) -> SafetyScore | None:
    ticker = ticker.upper()
    mkt = market or _detect_market(ticker)
    if not mkt:
        return None
    with sqlite3.connect(_db(mkt)) as conn:
        div_ttm = _ttm_div_per_share(conn, ticker)
        fund = _latest_fund(conn, ticker)
        is_reit = _is_reit(conn, ticker)

    if not fund and div_ttm == 0:
        return SafetyScore(ticker, mkt, 0.0, "N/A")

    comps = [
        _score_payout(div_ttm, fund.get("eps"), ffo=fund.get("ffo"), is_reit=is_reit),
        _score_roe(fund.get("roe")),
        _score_streak(fund.get("streak"), fund.get("aristocrat")),
        _score_leverage(fund.get("net_debt_ebitda"), is_reit=is_reit),
    ]

    # re-normalização: se algum componente é n/a, distribui o peso nos outros
    applicable = [c for c in comps if c.score is not None]
    if not applicable:
        return SafetyScore(ticker, mkt, 0.0, "N/A", components=comps)
    total_weight_applicable = sum(c.weight for c in applicable)
    raw_sum = sum(c.score for c in applicable)
    total = 100 * raw_sum / total_weight_applicable  # re-normalizado a 0-100

    if total >= 80:    verdict = "SAFE"
    elif total >= 60:  verdict = "WATCH"
    else:              verdict = "RISK"

    return SafetyScore(ticker, mkt, round(total, 1), verdict, components=comps)


# --- CLI -------------------------------------------------------------------

def _fmt_component(c: Component) -> str:
    if c.raw_value is None:
        return f"  {c.name:<18} weight={c.weight:>4}   value=—          score=n/a     [{c.verdict}]"
    # formato raw_value por tipo
    if c.name in ("payout_ratio", "payout_ratio_ffo"):
        val = f"{c.raw_value*100:>6.1f}%"
    elif c.name == "roe_level":
        val = f"{c.raw_value*100:>6.1f}%"
    elif c.name == "streak_years":
        val = f"{int(c.raw_value):>6}y"
    elif c.name == "net_debt_ebitda":
        val = f"{c.raw_value:>6.2f}x"
    else:
        val = f"{c.raw_value}"
    sc = f"{c.score:>5.1f}/{c.weight}" if c.score is not None else "  n/a"
    return f"  {c.name:<18} weight={c.weight:>4}   value={val}   score={sc}   [{c.verdict}]"


def _print_one(s: SafetyScore) -> None:
    print()
    print(f"DIVIDEND SAFETY — {s.ticker}  [{s.market}]")
    print("-" * 70)
    for c in s.components:
        print(_fmt_component(c))
    print("-" * 70)
    print(f"  TOTAL: {s.total:>5.1f} / 100     VERDICT: {s.verdict}")


def _holdings(market: str) -> list[str]:
    with sqlite3.connect(_db(market)) as c:
        return [r[0] for r in c.execute(
            "SELECT ticker FROM companies WHERE is_holding=1 ORDER BY ticker"
        )]


def _print_all() -> None:
    print(f"\n{'TICKER':<8} {'MKT':<4} {'TOTAL':>7}  {'VERDICT':<7}  "
          f"{'PAYOUT':>8} {'ROE':>6} {'STREAK':>7} {'ND/EB':>7}")
    print("-" * 78)
    for mkt in ("br", "us"):
        for tk in _holdings(mkt):
            s = compute(tk, mkt)
            if not s:
                continue
            by = {c.name: c for c in s.components}
            # REITs use payout_ratio_ffo; fall back to standard payout_ratio
            payout_c = by.get("payout_ratio_ffo") or by.get("payout_ratio")
            if payout_c:
                by["payout_ratio"] = payout_c
            def _v(name, fmt_):
                c = by.get(name)
                if not c or c.raw_value is None: return "  —"
                if name == "payout_ratio":  return f"{c.raw_value*100:>6.1f}%"
                if name == "roe_level":     return f"{c.raw_value*100:>5.1f}%"
                if name == "streak_years":  return f"{int(c.raw_value):>5}y"
                if name == "net_debt_ebitda": return f"{c.raw_value:>5.2f}x"
                return "—"
            print(f"{s.ticker:<8} {mkt:<4} {s.total:>6.1f}  {s.verdict:<7}  "
                  f"{_v('payout_ratio','%'):>8} {_v('roe_level','%'):>6} "
                  f"{_v('streak_years','y'):>7} {_v('net_debt_ebitda','x'):>7}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Dividend Safety Score (forward).")
    ap.add_argument("ticker", nargs="?", help="Ticker (BR sem .SA, US normal)")
    ap.add_argument("--market", choices=["br", "us"], help="Desambigua se necessário")
    ap.add_argument("--all", action="store_true",
                    help="Ranking de todos os holdings BR+US")
    args = ap.parse_args()

    if args.all:
        _print_all()
        return
    if not args.ticker:
        ap.error("passa um ticker ou --all")
    s = compute(args.ticker, args.market)
    if not s:
        print(f"[erro] ticker '{args.ticker}' não encontrado em nenhuma DB.")
        return
    _print_one(s)


if __name__ == "__main__":
    main()
