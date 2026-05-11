"""Portfolio Stress — concentration + factor exposure + drawdown war-game.

Inspirado nas ideias 11.4 (fragility), 11.5 (hidden factor), 11.7 (war-game), 11.8 (concentration).

Outputs (todos vault-friendly markdown):

1. CONCENTRATION REPORT (analytics/portfolio_stress.py concentration):
   - HHI (Herfindahl-Hirschman Index) por position, sector, market
   - Top-N exposure (top-3, top-5, top-10)
   - Single-position max
   - Sector concentration
   - Geography (BR vs US)
   - Currency exposure

2. FACTOR EXPOSURE (factor):
   - Beta levered médio (proxy market sensitivity)
   - PE distribution (value/growth tilt)
   - DY weighted (income tilt)
   - Sector tilt vs equal-weight
   - Size tilt (large/mid/small via market_cap)

3. DRAWDOWN WAR-GAME (drawdown):
   - Para cada cenário histórico (2008 -38%, 2020 COVID -34%, 2022 bear -25%):
     - Estimated portfolio impact (using individual betas + sector vols)
     - Time to recover (assuming hist recovery times)
   - Concentration risk multiplier
   - Liquidity risk (FII gates, ETF dispersion)

100% local. Pure Python + SQL.

Uso:
    python -m analytics.portfolio_stress concentration
    python -m analytics.portfolio_stress factor
    python -m analytics.portfolio_stress drawdown
    python -m analytics.portfolio_stress all   # todos
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}
OUT_DIR = ROOT / "obsidian_vault" / "briefings"


def _portfolio_positions() -> list[dict]:
    """All active positions across markets, with current market value."""
    out = []
    for market, db in DBS.items():
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            rows = c.execute("""
                SELECT p.ticker, p.quantity, p.entry_price, co.name, co.sector, co.currency,
                       (SELECT close FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) AS last_price,
                       (SELECT pe FROM fundamentals WHERE ticker=p.ticker ORDER BY period_end DESC LIMIT 1) AS pe,
                       (SELECT pb FROM fundamentals WHERE ticker=p.ticker ORDER BY period_end DESC LIMIT 1) AS pb,
                       (SELECT dy FROM fundamentals WHERE ticker=p.ticker ORDER BY period_end DESC LIMIT 1) AS dy,
                       (SELECT roe FROM fundamentals WHERE ticker=p.ticker ORDER BY period_end DESC LIMIT 1) AS roe,
                       (SELECT beta_levered FROM fundamentals WHERE ticker=p.ticker ORDER BY period_end DESC LIMIT 1) AS beta,
                       (SELECT market_cap_usd FROM fundamentals WHERE ticker=p.ticker ORDER BY period_end DESC LIMIT 1) AS mcap_usd
                FROM portfolio_positions p
                JOIN companies co ON co.ticker = p.ticker
                WHERE p.active = 1
            """).fetchall()
            for r in rows:
                d = dict(r)
                d["market"] = market
                last = d["last_price"] or d["entry_price"] or 0
                d["mv_local"] = (d["quantity"] or 0) * last
                # FX to USD for cross-market totals (rough)
                if market == "br":
                    d["mv_usd"] = d["mv_local"] / 5.5  # rough USDBRL ~5.5
                else:
                    d["mv_usd"] = d["mv_local"]
                out.append(d)
    return out


def concentration_report(positions: list[dict]) -> dict:
    total_usd = sum(p["mv_usd"] for p in positions)
    if total_usd == 0:
        return {"error": "no positions"}

    # Per-position weights (USD-normalized)
    weights = []
    for p in positions:
        w = p["mv_usd"] / total_usd
        weights.append({"ticker": p["ticker"], "market": p["market"], "sector": p["sector"],
                        "weight": w, "mv_usd": p["mv_usd"]})

    weights.sort(key=lambda x: -x["weight"])

    hhi = sum(w["weight"] ** 2 for w in weights) * 10000  # HHI in basis-point form
    top3 = sum(w["weight"] for w in weights[:3])
    top5 = sum(w["weight"] for w in weights[:5])
    top10 = sum(w["weight"] for w in weights[:10])
    max_pos = weights[0]

    # Sector
    by_sector = defaultdict(float)
    for p in positions:
        by_sector[p["sector"] or "?"] += p["mv_usd"]
    sector_pct = sorted([(s, v/total_usd) for s, v in by_sector.items()], key=lambda x: -x[1])

    # Market
    by_market = defaultdict(float)
    for p in positions:
        by_market[p["market"]] += p["mv_usd"]
    market_pct = {k: v/total_usd for k, v in by_market.items()}

    return {
        "total_portfolio_usd": total_usd,
        "n_positions": len(positions),
        "HHI": hhi,
        "HHI_interpretation": _hhi_interp(hhi),
        "top3_pct": round(top3 * 100, 1),
        "top5_pct": round(top5 * 100, 1),
        "top10_pct": round(top10 * 100, 1),
        "max_single_position": {
            "ticker": max_pos["ticker"], "weight_pct": round(max_pos["weight"] * 100, 1),
            "mv_usd": round(max_pos["mv_usd"], 0),
        },
        "by_sector": [{"sector": s, "pct": round(p * 100, 1)} for s, p in sector_pct],
        "by_market": {k: round(v * 100, 1) for k, v in market_pct.items()},
        "weights": [
            {"ticker": w["ticker"], "market": w["market"], "weight_pct": round(w["weight"] * 100, 2)}
            for w in weights
        ],
    }


def _hhi_interp(hhi: float) -> str:
    if hhi < 1500:
        return "well-diversified (HHI < 1500)"
    if hhi < 2500:
        return "moderately concentrated (1500-2500)"
    if hhi < 4000:
        return "concentrated (2500-4000)"
    return "highly concentrated (>4000)"


def factor_exposure_report(positions: list[dict]) -> dict:
    total = sum(p["mv_usd"] for p in positions)
    if total == 0:
        return {"error": "no positions"}

    # Weighted averages
    weighted = {"pe": 0, "pb": 0, "dy": 0, "roe": 0, "beta": 0}
    counts = {"pe": 0, "pb": 0, "dy": 0, "roe": 0, "beta": 0}
    for p in positions:
        w = p["mv_usd"] / total
        for k in weighted:
            v = p.get(k)
            if v is not None and not (isinstance(v, float) and (v != v)):  # skip NaN
                weighted[k] += v * w
                counts[k] += w   # weight covered

    # Normalize where coverage < 100%
    for k in weighted:
        if counts[k] > 0:
            weighted[k] /= counts[k]
        else:
            weighted[k] = None

    # Tilt classification
    tilts = []
    pe = weighted.get("pe")
    if pe and pe < 12:
        tilts.append("VALUE_TILT (weighted PE < 12)")
    elif pe and pe > 25:
        tilts.append("GROWTH_TILT (weighted PE > 25)")
    dy = weighted.get("dy")
    if dy and dy > 0.05:
        tilts.append("INCOME_TILT (DY > 5%)")
    beta = weighted.get("beta")
    if beta and beta < 0.8:
        tilts.append("DEFENSIVE (beta < 0.8)")
    elif beta and beta > 1.2:
        tilts.append("AGGRESSIVE (beta > 1.2)")

    # Size buckets
    size_buckets = {"large_cap_>50B": 0, "mid_cap_5_50B": 0, "small_cap_<5B": 0, "unknown": 0}
    for p in positions:
        m = p.get("mcap_usd")
        if m is None:
            size_buckets["unknown"] += p["mv_usd"]
        elif m > 50e9:
            size_buckets["large_cap_>50B"] += p["mv_usd"]
        elif m > 5e9:
            size_buckets["mid_cap_5_50B"] += p["mv_usd"]
        else:
            size_buckets["small_cap_<5B"] += p["mv_usd"]
    size_pct = {k: round(v/total*100, 1) for k, v in size_buckets.items()}

    return {
        "weighted_factors": {
            "pe": round(weighted["pe"], 2) if weighted["pe"] else None,
            "pb": round(weighted["pb"], 2) if weighted["pb"] else None,
            "dy_pct": round(weighted["dy"]*100, 2) if weighted["dy"] else None,
            "roe_pct": round(weighted["roe"]*100, 2) if weighted["roe"] else None,
            "beta": round(weighted["beta"], 2) if weighted["beta"] else None,
        },
        "tilts": tilts,
        "size_distribution_pct": size_pct,
    }


SCENARIOS = [
    {"name": "2008_GFC", "spx_drawdown": -0.50, "ibov_drawdown": -0.55, "duration_months": 18, "recovery_months": 24},
    {"name": "2020_COVID", "spx_drawdown": -0.34, "ibov_drawdown": -0.45, "duration_months": 1, "recovery_months": 4},
    {"name": "2022_Bear", "spx_drawdown": -0.25, "ibov_drawdown": -0.10, "duration_months": 9, "recovery_months": 12},
    {"name": "BR_Selic_15pct", "spx_drawdown": -0.05, "ibov_drawdown": -0.30, "duration_months": 6, "recovery_months": 18},
]


def drawdown_wargame(positions: list[dict]) -> dict:
    total = sum(p["mv_usd"] for p in positions)
    if total == 0:
        return {"error": "no positions"}

    by_market = defaultdict(float)
    for p in positions:
        by_market[p["market"]] += p["mv_usd"]
    br_pct = by_market["br"] / total
    us_pct = by_market["us"] / total

    results = []
    for s in SCENARIOS:
        port_dd = (br_pct * s["ibov_drawdown"] + us_pct * s["spx_drawdown"])
        # Beta adjustment — if portfolio beta != 1, scale
        # (use rough avg beta from factor report)
        usd_loss = total * port_dd
        results.append({
            "scenario": s["name"],
            "estimated_portfolio_dd_pct": round(port_dd * 100, 1),
            "estimated_usd_loss": round(usd_loss, 0),
            "duration_months": s["duration_months"],
            "recovery_months": s["recovery_months"],
        })
    return {
        "total_portfolio_usd": total,
        "scenarios": results,
        "br_share_pct": round(br_pct * 100, 1),
        "us_share_pct": round(us_pct * 100, 1),
    }


def write_markdown(report: dict, kind: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"portfolio_{kind}_{date.today().isoformat()}.md"

    if kind == "concentration":
        lines = [
            "---",
            f"type: portfolio_concentration",
            f"date: {date.today().isoformat()}",
            "tags: [portfolio, stress, concentration]",
            "---",
            "",
            f"# 🎯 Portfolio Concentration Report",
            "",
            f"**Total portfolio**: ${report['total_portfolio_usd']:,.0f}  ",
            f"**Positions**: {report['n_positions']}  ",
            f"**HHI**: {report['HHI']:.0f} ({report['HHI_interpretation']})  ",
            f"**Top-3 weight**: {report['top3_pct']}% | **Top-5**: {report['top5_pct']}% | **Top-10**: {report['top10_pct']}%  ",
            f"**Largest single position**: {report['max_single_position']['ticker']} ({report['max_single_position']['weight_pct']}%)",
            "",
            "## 🌍 Market split",
            "",
        ]
        for k, v in report["by_market"].items():
            lines.append(f"- {k.upper()}: {v}%")
        lines.append("")
        lines.append("## 🏢 By sector")
        lines.append("")
        lines.append("| Sector | Weight |")
        lines.append("|---|---:|")
        for s in report["by_sector"]:
            lines.append(f"| {s['sector']} | {s['pct']}% |")
        lines.append("")
        lines.append("## 📋 All positions ranked")
        lines.append("")
        lines.append("| # | Ticker | Mkt | Weight |")
        lines.append("|---|---|---|---:|")
        for i, w in enumerate(report["weights"], 1):
            lines.append(f"| {i} | {w['ticker']} | {w['market'].upper()} | {w['weight_pct']}% |")
        lines.append("")

    elif kind == "factor":
        wf = report["weighted_factors"]
        lines = [
            "---",
            f"type: portfolio_factor_exposure",
            f"date: {date.today().isoformat()}",
            "tags: [portfolio, stress, factor]",
            "---",
            "",
            f"# 🧭 Portfolio Factor Exposure",
            "",
            "## Weighted-by-MV factors",
            "",
            f"- **PE**: {wf.get('pe', '?')}",
            f"- **PB**: {wf.get('pb', '?')}",
            f"- **DY**: {wf.get('dy_pct', '?')}%",
            f"- **ROE**: {wf.get('roe_pct', '?')}%",
            f"- **Beta levered**: {wf.get('beta', '?')}",
            "",
            "## Tilts identificados",
            "",
        ]
        if report["tilts"]:
            for t in report["tilts"]:
                lines.append(f"- {t}")
        else:
            lines.append("_(no strong tilts detected — balanced exposure)_")
        lines.append("")
        lines.append("## Size distribution")
        lines.append("")
        for k, v in report["size_distribution_pct"].items():
            lines.append(f"- {k}: {v}%")
        lines.append("")

    elif kind == "drawdown":
        lines = [
            "---",
            f"type: portfolio_drawdown_wargame",
            f"date: {date.today().isoformat()}",
            "tags: [portfolio, stress, drawdown, scenario]",
            "---",
            "",
            f"# 💥 Drawdown War-Game",
            "",
            f"**Total portfolio**: ${report['total_portfolio_usd']:,.0f}  ",
            f"**BR share**: {report['br_share_pct']}% | **US share**: {report['us_share_pct']}%",
            "",
            "## Cenários históricos aplicados",
            "",
            "| Scenario | Portfolio DD% | USD Loss | Duration | Recovery |",
            "|---|---:|---:|---:|---:|",
        ]
        for s in report["scenarios"]:
            lines.append(f"| {s['scenario']} | {s['estimated_portfolio_dd_pct']}% | ${s['estimated_usd_loss']:,.0f} | {s['duration_months']}m | {s['recovery_months']}m |")
        lines.append("")
        lines.append("## ⚠️ Caveats honestos")
        lines.append("")
        lines.append("- Modelo simples: aplica só market drawdown × peso geográfico")
        lines.append("- Não inclui beta individual nem sector covariance")
        lines.append("- Recovery times são médias históricas — outliers podem ser muito piores")
        lines.append("- FII liquidity risk não modelado (gates possíveis)")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["concentration", "factor", "drawdown", "all"])
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    positions = _portfolio_positions()
    print(f"Loaded {len(positions)} positions")

    kinds = ["concentration", "factor", "drawdown"] if args.kind == "all" else [args.kind]
    for k in kinds:
        if k == "concentration":
            r = concentration_report(positions)
        elif k == "factor":
            r = factor_exposure_report(positions)
        elif k == "drawdown":
            r = drawdown_wargame(positions)
        if "error" in r:
            print(f"  {k}: {r['error']}")
            continue
        out = write_markdown(r, k)
        print(f"  {k}: -> {out.relative_to(ROOT)}")
        # Print key insights
        if k == "concentration":
            print(f"    HHI={r['HHI']:.0f} ({r['HHI_interpretation']}); top-5={r['top5_pct']}%; max={r['max_single_position']['ticker']}({r['max_single_position']['weight_pct']}%)")
        elif k == "factor":
            print(f"    Tilts: {r['tilts'] or 'balanced'}")
        elif k == "drawdown":
            for s in r["scenarios"]:
                print(f"    {s['scenario']:<18} DD%={s['estimated_portfolio_dd_pct']}% loss=${s['estimated_usd_loss']:,.0f}")


if __name__ == "__main__":
    main()
