"""rebalance — assistant para chegar à alocação alvo.

Lê `config/target_allocation.yaml` e compara com alocação actual.
Sugere trades para fechar gap respeitando tolerâncias (drift ≥ 5pp,
min trade R$500).

Não executa — apenas recomenda. User valida antes de trades reais.

Uso:
    python scripts/rebalance.py                      # análise full
    python scripts/rebalance.py --mode market        # só BR vs US
    python scripts/rebalance.py --mode sector        # só sectors BR
    python scripts/rebalance.py --cash-add 5000      # simula injecção adicional
    python scripts/rebalance.py --md                 # output markdown
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
CONFIG = ROOT / "config" / "target_allocation.yaml"


@dataclass
class Position:
    ticker: str
    market: str
    sector: str
    qty: float
    price: float
    mv_native: float
    mv_brl: float


def _load_positions() -> tuple[list[Position], float]:
    from analytics.fx import fx_rate
    fx = fx_rate()
    pos: list[Position] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            rows = c.execute("""
                SELECT p.ticker, p.quantity, c.sector,
                       (SELECT close FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1)
                FROM portfolio_positions p LEFT JOIN companies c ON c.ticker=p.ticker
                WHERE p.active=1
            """).fetchall()
            for tk, qty, sector, px in rows:
                if not px:
                    continue
                mv_native = px * qty
                mv_brl = mv_native * (fx if market == "us" else 1.0)
                pos.append(Position(tk, market, sector or "?", qty, px, mv_native, mv_brl))
    return pos, fx


def _load_targets() -> dict:
    with CONFIG.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def analyze(cash_add_brl: float = 0.0) -> dict:
    positions, fx = _load_positions()
    targets = _load_targets()
    total_brl = sum(p.mv_brl for p in positions) + cash_add_brl

    # By market
    br_mv = sum(p.mv_brl for p in positions if p.market == "br")
    us_mv = sum(p.mv_brl for p in positions if p.market == "us")
    tgt_m = targets.get("by_market", {})
    market_drift = {
        "br": {
            "actual_pct": br_mv / total_brl * 100,
            "target_pct": tgt_m.get("br", 50),
            "actual_brl": br_mv,
            "target_brl": total_brl * tgt_m.get("br", 50) / 100,
        },
        "us": {
            "actual_pct": us_mv / total_brl * 100,
            "target_pct": tgt_m.get("us", 50),
            "actual_brl": us_mv,
            "target_brl": total_brl * tgt_m.get("us", 50) / 100,
        },
    }
    for k in market_drift:
        market_drift[k]["drift_pp"] = market_drift[k]["actual_pct"] - market_drift[k]["target_pct"]
        market_drift[k]["delta_brl"] = market_drift[k]["target_brl"] - market_drift[k]["actual_brl"]

    # By sector (global) — simples agregação
    sec_mv: dict[str, float] = {}
    for p in positions:
        key = p.sector or "?"
        sec_mv[key] = sec_mv.get(key, 0) + p.mv_brl
    sector_drift = []
    for sec, mv in sorted(sec_mv.items(), key=lambda x: -x[1]):
        sector_drift.append({
            "sector": sec,
            "actual_pct": mv / total_brl * 100,
            "actual_brl": mv,
        })

    # Ticker concentration check
    max_weight_pct = targets.get("ticker_limits", {}).get("max_weight_pct", 15)
    min_weight_pct = targets.get("ticker_limits", {}).get("min_weight_pct", 0.2)
    concentration = []
    for p in positions:
        w = p.mv_brl / total_brl * 100
        if w > max_weight_pct:
            concentration.append({
                "ticker": p.ticker, "market": p.market,
                "weight_pct": w, "limit_pct": max_weight_pct,
                "violation": "too_concentrated",
                "suggest_sell_brl": (w - max_weight_pct) / 100 * total_brl,
            })
        elif w < min_weight_pct:
            concentration.append({
                "ticker": p.ticker, "market": p.market,
                "weight_pct": w, "limit_pct": min_weight_pct,
                "violation": "too_small",
                "suggest_close_brl": p.mv_brl,
            })

    # Suggest trades
    tol = targets.get("tolerance", {})
    drift_threshold = tol.get("drift_pct", 5.0)
    min_trade = tol.get("min_trade_brl", 500.0)

    trades: list[dict] = []
    for mk, d in market_drift.items():
        if abs(d["drift_pp"]) >= drift_threshold and abs(d["delta_brl"]) >= min_trade:
            action = "BUY" if d["delta_brl"] > 0 else "SELL"
            trades.append({
                "level": "market", "target": mk.upper(),
                "action": action, "amount_brl": abs(d["delta_brl"]),
                "reason": f"drift {d['drift_pp']:+.1f}pp > tolerância {drift_threshold}pp",
            })

    return {
        "total_brl": total_brl,
        "cash_add_brl": cash_add_brl,
        "fx": fx,
        "positions": len(positions),
        "market_drift": market_drift,
        "sector_agg": sector_drift,
        "concentration_alerts": concentration,
        "trade_suggestions": trades,
    }


def render_markdown(a: dict) -> str:
    lines = [f"# 🔄 Rebalance — {a['positions']} holdings\n"]
    lines.append(f"_Total: R$ {a['total_brl']:,.0f}  |  Cash extra considerado: R$ {a['cash_add_brl']:,.0f}_\n")

    # Market drift
    lines.append("## 🌐 Drift por mercado\n")
    lines.append("| Mercado | Actual | Target | Drift | Δ BRL |")
    lines.append("|---|---:|---:|---:|---:|")
    for mk, d in a["market_drift"].items():
        arrow = "▲" if d["drift_pp"] > 0 else "▼"
        lines.append(
            f"| {mk.upper()} | {d['actual_pct']:.1f}% | {d['target_pct']:.1f}% | "
            f"{arrow} {d['drift_pp']:+.1f}pp | R$ {d['delta_brl']:+,.0f} |"
        )
    lines.append("")

    # Concentration
    if a["concentration_alerts"]:
        lines.append("## ⚠️ Concentração alertas\n")
        for ca in a["concentration_alerts"]:
            if ca["violation"] == "too_concentrated":
                lines.append(
                    f"- 🔴 **{ca['ticker']}** ({ca['market']}): {ca['weight_pct']:.1f}% > limite {ca['limit_pct']}%. "
                    f"Sugerir trim ~R$ {ca['suggest_sell_brl']:,.0f}"
                )
            elif ca["violation"] == "too_small":
                lines.append(
                    f"- ⚪ **{ca['ticker']}** ({ca['market']}): {ca['weight_pct']:.2f}% < mínimo {ca['limit_pct']}%. "
                    f"Considerar fechar ou aumentar"
                )
        lines.append("")

    # Trade suggestions
    lines.append("## 💡 Trade suggestions\n")
    if not a["trade_suggestions"]:
        lines.append("_(dentro de tolerâncias — nada a fazer)_")
    else:
        for t in a["trade_suggestions"]:
            icon = "🟢" if t["action"] == "BUY" else "🔴"
            lines.append(
                f"- {icon} **{t['action']} {t['target']}** ~R$ {t['amount_brl']:,.0f}  "
                f"_({t['reason']})_"
            )
    lines.append("")

    # Sector breakdown (informativo)
    lines.append("## 🏢 Breakdown por sector (informativo)\n")
    lines.append("| Sector | MV (BRL) | % |")
    lines.append("|---|---:|---:|")
    for s in a["sector_agg"][:15]:
        lines.append(f"| {s['sector']} | R$ {s['actual_brl']:,.0f} | {s['actual_pct']:.1f}% |")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["full", "market", "sector"], default="full")
    ap.add_argument("--cash-add", type=float, default=0.0)
    ap.add_argument("--md", action="store_true", help="save to reports/")
    args = ap.parse_args()

    a = analyze(cash_add_brl=args.cash_add)
    out = render_markdown(a)
    print(out)

    if args.md:
        from datetime import date
        fp = ROOT / "reports" / f"rebalance_{date.today().isoformat()}.md"
        fp.write_text(out, encoding="utf-8")
        # Também para vault
        vp = ROOT / "obsidian_vault" / "Rebalance.md"
        vp.write_text(out, encoding="utf-8")
        print(f"\n[saved] {fp}")
        print(f"[saved] {vp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
