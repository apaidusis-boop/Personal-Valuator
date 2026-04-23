"""position_size — Kelly-lite sizing para BUY signals.

Dado:
  - Verdict score (0-10) + confidence %
  - Volatility (stdev de returns 90d) como proxy de risco
  - Cash disponível

Computa fracção do cash a alocar nessa posição, com:
  - Kelly base = (p·b − q) / b, onde p=win_prob, q=1-p, b=odds
  - Fracção cap em max_single_bet (default 5%)
  - Haircut por baixa confidence

Fórmula simplificada (Kelly-lite determinístico):
  p = 0.5 + (score/10 - 0.5) * 0.6       # 50%..80% win prob
  b = 1.5 - vol_90d                       # 1.5 = expected upside, penaliza vol
  f = (p*b - (1-p)) / b
  f = max(0, min(f, MAX_CAP))
  f *= confidence/100

Uso:
    python scripts/position_size.py ACN --cash 3000
    python scripts/position_size.py --ticker ACN --cash 3000 --max-bet 8
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path
from statistics import pstdev

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def _vol_90d(ticker: str, market: str) -> float | None:
    db = ROOT / "data" / f"{market}_investments.db"
    cutoff = (date.today() - timedelta(days=90)).isoformat()
    with sqlite3.connect(db) as c:
        rows = c.execute(
            "SELECT close FROM prices WHERE ticker=? AND date>=? ORDER BY date",
            (ticker, cutoff),
        ).fetchall()
    if len(rows) < 10:
        return None
    returns = [(rows[i][0] / rows[i - 1][0] - 1) for i in range(1, len(rows))]
    return pstdev(returns)


def kelly(score: float, confidence_pct: float, vol: float | None, max_bet: float = 0.05) -> dict:
    """Devolve fracção (0-1) do cash."""
    p = 0.5 + (score / 10 - 0.5) * 0.6   # 0.2-0.8 tipicamente
    p = max(0.3, min(p, 0.8))
    v = (vol or 0.02) * 100              # em pontos percentuais
    b = max(0.3, 1.5 - v)                # upside expected; penaliza high vol
    q = 1 - p
    f_raw = (p * b - q) / b if b > 0 else 0
    f_capped = max(0.0, min(f_raw, max_bet))
    f_final = f_capped * (confidence_pct / 100)
    return {
        "p_win": round(p, 3),
        "b_odds": round(b, 3),
        "kelly_raw": round(f_raw, 4),
        "kelly_capped": round(f_capped, 4),
        "kelly_final": round(f_final, 4),
        "daily_vol_pct": round(v, 2),
    }


def size_ticker(ticker: str, cash_brl: float, max_bet: float = 0.05,
                force: bool = False) -> dict:
    from scripts.verdict import compute_verdict
    from scripts.refresh_ticker import _market_of
    from analytics.fx import fx_rate

    market = _market_of(ticker)
    v = compute_verdict(ticker)
    if v.action not in ("BUY", "ADD", "WATCH") and not force:
        return {
            "ticker": ticker, "action": v.action,
            "suggestion": "sem sinal de compra — skip (usar --force para ver sizing)",
            "verdict_score": v.total_score,
        }

    vol = _vol_90d(ticker, market)
    k = kelly(v.total_score, v.confidence_pct, vol, max_bet=max_bet)
    amount_brl = cash_brl * k["kelly_final"]
    fx = fx_rate()
    price_native = None
    db = ROOT / "data" / f"{market}_investments.db"
    with sqlite3.connect(db) as c:
        r = c.execute(
            "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if r:
            price_native = float(r[0])
    if market == "us":
        amount_native = amount_brl / fx
    else:
        amount_native = amount_brl
    shares = int(amount_native / price_native) if price_native else 0

    return {
        "ticker": ticker, "market": market,
        "action": v.action,
        "verdict_score": v.total_score,
        "verdict_confidence": v.confidence_pct,
        "kelly": k,
        "cash_brl": cash_brl,
        "suggested_allocation_brl": round(amount_brl, 2),
        "suggested_allocation_native": round(amount_native, 2),
        "price_native": price_native,
        "suggested_shares": shares,
        "actual_cost_native": round(shares * price_native, 2) if price_native else None,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ticker")
    ap.add_argument("--cash", type=float, required=True, help="Cash disponível (BRL)")
    ap.add_argument("--max-bet", type=float, default=5.0, help="Max % em 1 ticker (default 5%)")
    ap.add_argument("--force", action="store_true", help="Mostrar sizing mesmo se HOLD/SKIP")
    args = ap.parse_args()

    r = size_ticker(args.ticker.upper(), args.cash, max_bet=args.max_bet / 100, force=args.force)
    import json
    print(json.dumps(r, indent=2, ensure_ascii=False))

    if "suggested_shares" in r and r["suggested_shares"]:
        print(f"\n💡 Sugestão: comprar **{r['suggested_shares']} shares** de {r['ticker']}")
        print(f"   a ~{r['price_native']:.2f} = {r['actual_cost_native']:.2f} ({r['market'].upper()})")
        print(f"   ({r['kelly']['kelly_final']*100:.2f}% do cash = R$ {r['suggested_allocation_brl']:,.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
