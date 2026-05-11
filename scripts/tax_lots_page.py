"""tax_lots_page — gera página TaxLots.md no Obsidian + tabela tax_lots por ticker.

Exibe lots detalhados (FIFO-style) com P&L por lote, tax term, days held.

Uso:
    python scripts/tax_lots_page.py            # regenera TaxLots.md no vault
    python scripts/tax_lots_page.py --ticker ACN
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_US = ROOT / "data" / "us_investments.db"
DB_BR = ROOT / "data" / "br_investments.db"
VAULT = ROOT / "obsidian_vault"


def _latest_price(conn, ticker: str) -> float | None:
    r = conn.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    return r[0] if r else None


def _lots(ticker: str | None = None):
    from collections import defaultdict
    grouped: dict = defaultdict(list)
    with sqlite3.connect(DB_US) as c:
        q = """SELECT ticker, acquisition_date, quantity, unit_cost, total_cost,
                      tax_term, days_held, notes
               FROM tax_lots WHERE active=1"""
        args = []
        if ticker:
            q += " AND ticker=?"
            args.append(ticker)
        q += " ORDER BY ticker, acquisition_date"
        rows = c.execute(q, args).fetchall()
        for r in rows:
            grouped[r[0]].append({
                "acq_date": r[1], "qty": r[2], "unit_cost": r[3],
                "total_cost": r[4], "tax_term": r[5], "days_held": r[6],
                "notes": r[7],
            })
        # Prices
        prices: dict = {}
        for tk in grouped:
            prices[tk] = _latest_price(c, tk)
        # Cash
        cash = c.execute(
            "SELECT broker, currency, amount, as_of FROM broker_cash"
        ).fetchall()
    return grouped, prices, cash


def render() -> str:
    grouped, prices, cash = _lots()
    if not grouped:
        return "_(sem tax lots — corre import_taxlots.py)_"
    today = date.today().isoformat()
    lines = [
        "---", "tags: [taxlots, positions]", f"date: {today}", "---",
        "# 📜 Tax Lots (JPM)\n",
        f"_Última importação: `{today}`. Fonte: `portfolio_positions.tax_lots` via JPM CSV export._\n",
    ]

    # Cash
    if cash:
        lines.append("## 💵 Cash disponível\n")
        for b, cur, amt, asof in cash:
            lines.append(f"- **{b}** `{cur}` {amt:,.2f}  _(as of {asof})_")
        lines.append("")

    # Aggregated summary
    lines.append("## 📊 Resumo agregado por ticker\n")
    lines.append("| Ticker | Lots | Qty | Avg Cost | Current | Cost Total | MV | P&L % | P&L abs |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    total_cost = 0.0
    total_mv = 0.0
    for tk in sorted(grouped):
        lots = grouped[tk]
        qty = sum(l["qty"] for l in lots)
        cost = sum(l["total_cost"] for l in lots)
        avg = cost / qty if qty else 0
        px = prices.get(tk) or 0
        mv = qty * px
        pnl_abs = mv - cost
        pnl_pct = (mv / cost - 1) * 100 if cost else 0
        total_cost += cost
        total_mv += mv
        lines.append(
            f"| [[{tk}]] | {len(lots)} | {qty:.4f} | ${avg:.2f} | ${px:.2f} | "
            f"${cost:,.2f} | ${mv:,.2f} | {pnl_pct:+.2f}% | ${pnl_abs:+,.2f} |"
        )
    lines.append(
        f"| **TOTAL** |  |  |  |  | **${total_cost:,.2f}** | **${total_mv:,.2f}** | "
        f"**{(total_mv/total_cost-1)*100:+.2f}%** | **${total_mv-total_cost:+,.2f}** |"
    )
    lines.append("")

    # Per-ticker breakdown
    lines.append("## 🔍 Breakdown por ticker\n")
    for tk in sorted(grouped):
        lots = grouped[tk]
        px = prices.get(tk)
        lines.append(f"### [[{tk}]]\n")
        lines.append("| Acq date | Qty | Unit cost | Total cost | Tax term | Days | Unrealized % |")
        lines.append("|---|---:|---:|---:|---|---:|---:|")
        for l in lots:
            pnl_pct = (px / l["unit_cost"] - 1) * 100 if px and l["unit_cost"] else 0
            lines.append(
                f"| {l['acq_date']} | {l['qty']:.4f} | ${l['unit_cost']:.2f} | "
                f"${l['total_cost']:,.2f} | {l['tax_term']} | {l['days_held']} | "
                f"{pnl_pct:+.2f}% |"
            )
        lines.append("")

    # Tax term summary (useful for tax planning)
    lines.append("## 🗓 Tax term summary (IRS relevante)\n")
    short_cost = 0.0; short_mv = 0.0
    long_cost = 0.0; long_mv = 0.0
    for tk, lots in grouped.items():
        px = prices.get(tk) or 0
        for l in lots:
            if l["tax_term"] == "Short":
                short_cost += l["total_cost"]
                short_mv += l["qty"] * px
            else:
                long_cost += l["total_cost"]
                long_mv += l["qty"] * px
    lines.append("| Term | Cost | MV | P&L abs | P&L % |")
    lines.append("|---|---:|---:|---:|---:|")
    if short_cost > 0:
        lines.append(
            f"| Short (≤1y) | ${short_cost:,.2f} | ${short_mv:,.2f} | "
            f"${short_mv-short_cost:+,.2f} | {(short_mv/short_cost-1)*100:+.2f}% |"
        )
    if long_cost > 0:
        lines.append(
            f"| **Long (>1y)** | ${long_cost:,.2f} | ${long_mv:,.2f} | "
            f"${long_mv-long_cost:+,.2f} | {(long_mv/long_cost-1)*100:+.2f}% |"
        )

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ticker")
    args = ap.parse_args()

    out = render()
    print(out)
    fp = VAULT / "TaxLots.md"
    fp.write_text(out, encoding="utf-8")
    print(f"\n[saved] {fp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
