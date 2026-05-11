"""Vitality Score — "será uma Premium Company nos próximos 20-30 anos?"

Filosofia (user, 2026-05-09): a régua quantitativa (Graham / Buffett / banco)
serve para evitar pagar caro. Mas casos de qualidade superior podem ter
multiplos ligeiramente acima da régua e ainda assim valer a pena entrar com
observações explícitas — "leap of faith" documentada. Para isso, precisamos
de uma medida ortogonal à régua: a *vitalidade* — durabilidade do estatuto
de Premium Company sobre décadas.

5 sub-scores 0-100, composite ponderado:

  1. scale_dominance        (20%)   tamanho + brand recognition + posição
  2. secular_tailwind_30y   (15%)   sector tailwind sobre décadas
  3. capital_allocation     (25%)   track record de dividendos+buybacks+ROE
  4. resilience_track_record(25%)   sobreviveu 2008/2020 sem cortar payouts
  5. earnings_durability    (15%)   estabilidade de net income / revenue

Composite tiers:
  ≥ 80   OVERWHELMING — justifica leap of faith se screen falha por pouco
  ≥ 65   STRONG       — mantém HOLD em near miss, não habilita BUY
   50-64 NEUTRAL      — sem override
   < 50  WEAK         — screen REJECT confirmado

Não substitui o moat. Moat mede vantagem competitiva (cross-sectional);
vitality mede expectativa longitudinal de continuar Premium. Banks são o
caso paradigmático: moat.py exclui-os, mas vitality aplica-se.

Uso:
    python -m scoring.vitality JPM
    python -m scoring.vitality ITSA4 --market br
    python -m scoring.vitality KO --json
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

WEIGHTS = {
    "scale_dominance":        0.20,
    "secular_tailwind":       0.15,
    "capital_allocation":     0.25,
    "resilience_track":       0.25,
    "earnings_durability":    0.15,
}

# Sector secular tailwind 30y view. Calibrado para refletir tendência
# estrutural, não ciclo curto. Pode ser overrided por config/vitality_overrides.yaml.
SECULAR_TAILWIND = {
    # US sectors
    "technology":              85,
    "communication services":  75,
    "consumer staples":        80,
    "healthcare":              80,
    "financials":              65,  # banks: digital, scale; insurance: ageing
    "industrials":             60,
    "consumer discretionary":  55,
    "energy":                  35,  # transition headwind
    "materials":               45,
    "utilities":               65,  # electrification
    "real estate":             55,
    # BR-specific overrides
    "banks":                   65,  # BR bancos com share institucional + spreads protegidos
    "insurance":               70,
    "papel e celulose":        50,
    "mineração":               40,  # commodity cycle
    "shopping":                40,  # secular headwind e-commerce
    "energia elétrica":        70,
    "saneamento":              80,
    "holding":                 60,
    "telecom":                 55,
    "consumer cyclical":       50,
}

# "Premium Company" status proxies for capital allocation
DIV_STREAK_TIER = [
    (40, 30),  # 40+ anos = 30 pts (rare — Aristocrat++ / BR equiv)
    (25, 25),
    (15, 20),
    (10, 15),
    (5, 10),
]


@dataclass
class VitalityScore:
    ticker: str
    market: str
    overall: int | None = None
    label: str = "N/A"
    scale_dominance: int | None = None
    secular_tailwind: int | None = None
    capital_allocation: int | None = None
    resilience_track: int | None = None
    earnings_durability: int | None = None
    details: dict = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def compute_label(self) -> str:
        if self.overall is None:
            return "N/A"
        if self.overall >= 80:
            return "OVERWHELMING"
        if self.overall >= 65:
            return "STRONG"
        if self.overall >= 50:
            return "NEUTRAL"
        return "WEAK"


def _db(market: str) -> Path:
    return DB_BR if market == "br" else DB_US


def _detect_market(ticker: str) -> str | None:
    for mk in ("br", "us"):
        path = _db(mk)
        if not path.exists():
            continue
        with sqlite3.connect(path) as c:
            r = c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone()
            if r:
                return mk
    return None


# ─── Sub 1: Scale dominance (market cap relative to sector peers) ─────────

def _scale_dominance(conn: sqlite3.Connection, snap: dict, details: dict) -> int | None:
    """Percentile of market cap among peers in the same sector.
    Top 10% = 100, top 25% = 80, top 50% = 60, bottom half = 40.
    For sectors with <5 peers in DB, fall back to absolute scale tiers.
    """
    sector = (snap.get("sector") or "").strip().lower()
    market_cap = snap.get("market_cap")
    if not market_cap or market_cap <= 0:
        return None

    if sector:
        peers = conn.execute(
            """SELECT f.market_cap FROM fundamentals f
               JOIN companies c ON f.ticker = c.ticker
               WHERE LOWER(TRIM(c.sector)) = ?
                 AND f.market_cap IS NOT NULL AND f.market_cap > 0
                 AND f.period_end = (
                     SELECT MAX(period_end) FROM fundamentals WHERE ticker = f.ticker
                 )""",
            (sector,),
        ).fetchall()
        peer_caps = sorted([p[0] for p in peers], reverse=True)
        details["peer_count"] = len(peer_caps)
    else:
        peer_caps = []

    if len(peer_caps) >= 5:
        rank = next((i for i, c in enumerate(peer_caps) if c <= market_cap), len(peer_caps))
        percentile = 1 - (rank / len(peer_caps))
        details["sector_percentile"] = round(percentile, 3)
        if percentile >= 0.90:
            return 100
        if percentile >= 0.75:
            return 85
        if percentile >= 0.50:
            return 65
        if percentile >= 0.25:
            return 45
        return 30

    # Fallback: absolute scale tiers (USD-equiv, rough proxy)
    cap_usd = market_cap if snap.get("currency", "").upper() == "USD" else market_cap / 5.0
    details["market_cap_usd_est"] = int(cap_usd)
    if cap_usd >= 200_000_000_000:  # mega-cap ($200B+)
        return 90
    if cap_usd >= 50_000_000_000:
        return 75
    if cap_usd >= 10_000_000_000:
        return 60
    if cap_usd >= 2_000_000_000:
        return 45
    return 30


# ─── Sub 2: Secular tailwind (sector lookup) ──────────────────────────────

def _secular_tailwind(snap: dict, details: dict) -> int | None:
    sector = (snap.get("sector") or "").strip().lower()
    if not sector:
        return 50  # unknown → neutral
    score = SECULAR_TAILWIND.get(sector)
    if score is None:
        # Try partial matches
        for k, v in SECULAR_TAILWIND.items():
            if k in sector or sector in k:
                score = v
                details["sector_match"] = k
                break
    details["sector_normalized"] = sector
    return score if score is not None else 50


# ─── Sub 3: Capital allocation (dividends + buybacks + ROE) ───────────────

def _capital_allocation(snap: dict, conn: sqlite3.Connection, details: dict) -> int | None:
    """0-100 from dividend streak + ROE + buyback signal.

    Score breakdown:
      - dividend streak 0-30 (40+y=30, 25y=25, 15y=20, 10y=15, 5y=10)
      - is_aristocrat bonus +10 (capped at total 100)
      - ROE/ROTCE tier 0-30 (>=18%=30, 15%=25, 12%=20, 8%=10)
      - buyback signal 0-20 (shares decreasing over 5y)
      - payout discipline 0-20 (DY positive + streak intact)
    """
    f_streak = snap.get("dividend_streak_years")
    f_arist = snap.get("is_aristocrat")
    f_roe = snap.get("rotce") or snap.get("roe")
    f_dy = snap.get("dy")

    pts = 0
    components: dict[str, int] = {}

    # Dividend streak
    streak_pts = 0
    if f_streak is not None:
        for tier_years, tier_pts in DIV_STREAK_TIER:
            if f_streak >= tier_years:
                streak_pts = tier_pts
                break
    components["streak_pts"] = streak_pts
    pts += streak_pts

    # Aristocrat bonus
    if f_arist:
        components["aristocrat_bonus"] = 10
        pts += 10

    # ROE / ROTCE tier
    roe_pts = 0
    if f_roe is not None:
        if f_roe >= 0.18:
            roe_pts = 30
        elif f_roe >= 0.15:
            roe_pts = 25
        elif f_roe >= 0.12:
            roe_pts = 20
        elif f_roe >= 0.08:
            roe_pts = 10
    components["roe_pts"] = roe_pts
    pts += roe_pts

    # Buyback signal — shares trending down over period available
    buyback_pts = 0
    rows = conn.execute(
        """SELECT period_end, shares_outstanding FROM deep_fundamentals
            WHERE ticker=? AND period_type='annual' AND shares_outstanding > 0
            ORDER BY period_end""",
        (snap["ticker"],),
    ).fetchall()
    if len(rows) >= 3:
        first, last = rows[0][1], rows[-1][1]
        delta = (last - first) / first
        components["shares_delta"] = round(delta, 4)
        if delta < -0.05:
            buyback_pts = 20
        elif delta < -0.02:
            buyback_pts = 15
        elif delta < 0.02:
            buyback_pts = 10
        elif delta < 0.10:
            buyback_pts = 5
    components["buyback_pts"] = buyback_pts
    pts += buyback_pts

    # Payout discipline (DY positive + no recent cut signal)
    payout_pts = 0
    if f_dy is not None and f_dy > 0:
        payout_pts = 10
        if f_streak is not None and f_streak >= 10:
            payout_pts = 20
    components["payout_pts"] = payout_pts
    pts += payout_pts

    details["capital_alloc_components"] = components
    return min(100, pts)


# ─── Sub 4: Resilience (post-2008, post-2020 survival) ────────────────────

def _resilience(snap: dict, conn: sqlite3.Connection, details: dict) -> int | None:
    """Did the company survive 2008/2020 with payouts intact and EPS recovery?

    Score:
      - dividend streak >= 16y (post-GFC + spans 2008): 35 pts
      - dividend streak >= 5y (spans 2020): 15 pts
      - net income CV over 5y: 0-30 pts (lower CV = better)
      - no negative net income year in last 5y: 20 pts
    """
    streak = snap.get("dividend_streak_years")
    pts = 0
    components: dict = {}

    streak_pts = 0
    if streak is not None:
        if streak >= 16:
            streak_pts = 35
        elif streak >= 5:
            streak_pts = 15
        elif streak >= 1:
            streak_pts = 5
    components["streak_pts"] = streak_pts
    pts += streak_pts

    # NI stability + no negative years
    rows = conn.execute(
        """SELECT period_end, net_income FROM deep_fundamentals
            WHERE ticker=? AND period_type='annual' AND net_income IS NOT NULL
            ORDER BY period_end DESC LIMIT 5""",
        (snap["ticker"],),
    ).fetchall()
    nis = [r[1] for r in rows]

    cv_pts = 0
    if len(nis) >= 3:
        try:
            mean = statistics.mean(nis)
            if mean > 0:
                cv = statistics.stdev(nis) / mean
                components["ni_cv"] = round(cv, 3)
                if cv < 0.10:
                    cv_pts = 30
                elif cv < 0.20:
                    cv_pts = 22
                elif cv < 0.35:
                    cv_pts = 15
                elif cv < 0.50:
                    cv_pts = 8
                else:
                    cv_pts = 0
        except statistics.StatisticsError:
            pass
    components["cv_pts"] = cv_pts
    pts += cv_pts

    no_loss_pts = 0
    if nis:
        if all(ni > 0 for ni in nis):
            no_loss_pts = 20
        components["years_in_sample"] = len(nis)
        components["losses"] = sum(1 for n in nis if n <= 0)
    pts += no_loss_pts
    components["no_loss_pts"] = no_loss_pts

    details["resilience_components"] = components
    return min(100, pts)


# ─── Sub 5: Earnings durability (revenue + NI stability) ──────────────────

def _earnings_durability(snap: dict, conn: sqlite3.Connection, details: dict) -> int | None:
    """0-100 from revenue trend stability + NI growth.

    Components:
      - revenue down-years count (0-3 years) → 30 pts
      - revenue CAGR 5y → 30 pts (>=5%=30, 2-5%=20, 0-2%=10)
      - NI CAGR 5y → 40 pts (>=8%=40, 4-8%=25, 0-4%=10)
    """
    rows = conn.execute(
        """SELECT period_end, total_revenue, net_income FROM deep_fundamentals
            WHERE ticker=? AND period_type='annual'
            ORDER BY period_end""",
        (snap["ticker"],),
    ).fetchall()
    if len(rows) < 3:
        return None

    revs = [r[1] for r in rows if r[1] is not None]
    nis = [r[2] for r in rows if r[2] is not None]

    pts = 0
    components: dict = {}

    # Down-years
    down_pts = 0
    if len(revs) >= 3:
        downs = sum(1 for i in range(1, len(revs)) if revs[i] < revs[i - 1])
        components["rev_down_years"] = downs
        if downs == 0:
            down_pts = 30
        elif downs == 1:
            down_pts = 20
        elif downs == 2:
            down_pts = 10
    pts += down_pts
    components["down_pts"] = down_pts

    # Revenue CAGR
    rev_cagr_pts = 0
    if len(revs) >= 3 and revs[0] > 0:
        n = len(revs) - 1
        cagr = (revs[-1] / revs[0]) ** (1 / n) - 1
        components["rev_cagr"] = round(cagr, 4)
        if cagr >= 0.05:
            rev_cagr_pts = 30
        elif cagr >= 0.02:
            rev_cagr_pts = 20
        elif cagr >= 0.0:
            rev_cagr_pts = 10
    pts += rev_cagr_pts
    components["rev_cagr_pts"] = rev_cagr_pts

    # NI CAGR
    ni_cagr_pts = 0
    if len(nis) >= 3 and nis[0] > 0 and nis[-1] > 0:
        n = len(nis) - 1
        cagr = (nis[-1] / nis[0]) ** (1 / n) - 1
        components["ni_cagr"] = round(cagr, 4)
        if cagr >= 0.08:
            ni_cagr_pts = 40
        elif cagr >= 0.04:
            ni_cagr_pts = 25
        elif cagr >= 0.0:
            ni_cagr_pts = 10
    pts += ni_cagr_pts
    components["ni_cagr_pts"] = ni_cagr_pts

    details["earnings_components"] = components
    return min(100, pts)


# ─── Snapshot loader ──────────────────────────────────────────────────────

def _load_snap(conn: sqlite3.Connection, ticker: str) -> dict | None:
    row = conn.execute(
        "SELECT ticker, name, sector, currency FROM companies WHERE ticker=?",
        (ticker,),
    ).fetchone()
    if not row:
        return None
    # BR DB doesn't have rotce column (US bank-specific). Try with, fall back without.
    try:
        fund = conn.execute(
            """SELECT roe, dy, dividend_streak_years, is_aristocrat,
                      market_cap, rotce
                 FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        rotce_available = True
    except sqlite3.OperationalError:
        fund = conn.execute(
            """SELECT roe, dy, dividend_streak_years, is_aristocrat,
                      market_cap
                 FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
        rotce_available = False
    snap = {
        "ticker": row[0], "name": row[1], "sector": row[2] or "", "currency": row[3] or "",
    }
    if fund:
        snap.update({
            "roe": fund[0], "dy": fund[1], "dividend_streak_years": fund[2],
            "is_aristocrat": bool(fund[3]) if fund[3] is not None else None,
            "market_cap": fund[4],
            "rotce": fund[5] if rotce_available else None,
        })
    return snap


# ─── Main entry point ─────────────────────────────────────────────────────

def compute(ticker: str, market: str | None = None) -> VitalityScore:
    market = market or _detect_market(ticker)
    if market is None:
        return VitalityScore(ticker=ticker, market="?", notes=[f"{ticker} not in any DB"])

    db = _db(market)
    if not db.exists():
        return VitalityScore(ticker=ticker, market=market, notes=[f"{db.name} missing"])

    score = VitalityScore(ticker=ticker, market=market)
    with sqlite3.connect(db) as conn:
        snap = _load_snap(conn, ticker)
        if snap is None:
            score.notes.append(f"{ticker} not in companies table")
            return score

        score.scale_dominance     = _scale_dominance(conn, snap, score.details)
        score.secular_tailwind    = _secular_tailwind(snap, score.details)
        score.capital_allocation  = _capital_allocation(snap, conn, score.details)
        score.resilience_track    = _resilience(snap, conn, score.details)
        score.earnings_durability = _earnings_durability(snap, conn, score.details)

        components = {
            "scale_dominance":     score.scale_dominance,
            "secular_tailwind":    score.secular_tailwind,
            "capital_allocation":  score.capital_allocation,
            "resilience_track":    score.resilience_track,
            "earnings_durability": score.earnings_durability,
        }
        # Compute weighted overall over available components
        weight_sum, score_sum = 0.0, 0.0
        for k, v in components.items():
            if v is None:
                score.notes.append(f"{k}: skipped (insufficient data)")
                continue
            score_sum += v * WEIGHTS[k]
            weight_sum += WEIGHTS[k]

        if weight_sum > 0:
            score.overall = round(score_sum / weight_sum)
            score.label = score.compute_label()

    return score


# ─── CLI ──────────────────────────────────────────────────────────────────

def _print_score(s: VitalityScore) -> None:
    print(f"=== Vitality — {s.ticker} ({s.market.upper()}) ===")
    if s.overall is None:
        print(f"  N/A — {'; '.join(s.notes) if s.notes else 'unknown'}")
        return
    print(f"  Overall: {s.overall}/100  →  {s.label}")
    print()
    print(f"  scale_dominance       {s.scale_dominance!s:>4} (w={int(WEIGHTS['scale_dominance']*100)}%)")
    print(f"  secular_tailwind      {s.secular_tailwind!s:>4} (w={int(WEIGHTS['secular_tailwind']*100)}%)")
    print(f"  capital_allocation    {s.capital_allocation!s:>4} (w={int(WEIGHTS['capital_allocation']*100)}%)")
    print(f"  resilience_track      {s.resilience_track!s:>4} (w={int(WEIGHTS['resilience_track']*100)}%)")
    print(f"  earnings_durability   {s.earnings_durability!s:>4} (w={int(WEIGHTS['earnings_durability']*100)}%)")
    if s.notes:
        print()
        for n in s.notes:
            print(f"  · {n}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--market", choices=["br", "us"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    s = compute(args.ticker.upper(), args.market)
    if args.json:
        print(json.dumps(asdict(s), indent=2, ensure_ascii=False))
    else:
        _print_score(s)


if __name__ == "__main__":
    main()
