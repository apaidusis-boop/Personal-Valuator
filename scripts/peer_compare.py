"""peer_compare — percentil de um ticker vs peers do mesmo sector.

Output por métrica (P/E, P/B, DY, ROE, streak_years): percentil + quartil
+ comparação side-by-side com top-N peers. Útil como "onde estou dentro
do sector?".

Uso:
    python scripts/peer_compare.py ACN              # top 10 peers
    python scripts/peer_compare.py ITSA4 --md       # markdown
    python scripts/peer_compare.py --all-holdings
    python scripts/peer_compare.py ACN --write      # injecta em ticker note
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
VAULT = ROOT / "obsidian_vault"


def _sector_peers(market: str, sector: str) -> list[dict]:
    """Todos os tickers do sector com métricas latest."""
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        rows = c.execute("""
            SELECT c.ticker, c.name, c.is_holding,
                   f.pe, f.pb, f.dy, f.roe, f.dividend_streak_years,
                   (SELECT close FROM prices WHERE ticker=c.ticker ORDER BY date DESC LIMIT 1) AS price
            FROM companies c
            LEFT JOIN (SELECT ticker, MAX(period_end) AS mp FROM fundamentals GROUP BY ticker) lf
                ON lf.ticker = c.ticker
            LEFT JOIN fundamentals f ON f.ticker=c.ticker AND f.period_end=lf.mp
            WHERE c.sector=?
        """, (sector,)).fetchall()
    out = []
    for r in rows:
        tk, name, is_h, pe, pb, dy, roe, streak, price = r
        out.append({
            "ticker": tk, "name": name, "is_holding": bool(is_h),
            "pe": pe, "pb": pb, "dy": dy, "roe": roe,
            "streak": streak, "price": price,
        })
    return out


def _percentile(value, series: list) -> float | None:
    """Percentil (0-100) de `value` dentro de `series`. Ignora None."""
    if value is None:
        return None
    xs = sorted(x for x in series if x is not None)
    if not xs:
        return None
    below = sum(1 for x in xs if x < value)
    return below / len(xs) * 100


def compare(ticker: str) -> dict:
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            r = c.execute(
                "SELECT sector FROM companies WHERE ticker=?", (ticker,)
            ).fetchone()
            if r:
                sector = r[0]
                break
    else:
        raise ValueError(f"{ticker} não encontrado")

    if not sector:
        return {"ticker": ticker, "error": "sem sector"}

    peers = _sector_peers(market, sector)
    me = next((p for p in peers if p["ticker"] == ticker), None)
    if not me:
        return {"ticker": ticker, "error": "ticker não encontrado no sector"}

    others = [p for p in peers if p["ticker"] != ticker]

    # Percentis
    pcts = {}
    for k in ("pe", "pb", "dy", "roe", "streak"):
        series = [p[k] for p in peers]
        pcts[k] = _percentile(me[k], series)

    # Interpretar: P/E e P/B baixos = bom (percentil baixo = mais barato)
    # DY, ROE, streak altos = bom (percentil alto)
    interp = {
        "pe": "barato" if pcts["pe"] is not None and pcts["pe"] <= 25 else (
              "caro" if pcts["pe"] is not None and pcts["pe"] >= 75 else "médio"),
        "pb": "barato" if pcts["pb"] is not None and pcts["pb"] <= 25 else (
              "caro" if pcts["pb"] is not None and pcts["pb"] >= 75 else "médio"),
        "dy": "generoso" if pcts["dy"] is not None and pcts["dy"] >= 75 else (
              "magro" if pcts["dy"] is not None and pcts["dy"] <= 25 else "médio"),
        "roe": "forte" if pcts["roe"] is not None and pcts["roe"] >= 75 else (
               "fraco" if pcts["roe"] is not None and pcts["roe"] <= 25 else "médio"),
        "streak": "longo" if pcts["streak"] is not None and pcts["streak"] >= 75 else (
                  "curto" if pcts["streak"] is not None and pcts["streak"] <= 25 else "médio"),
    }

    return {
        "ticker": ticker,
        "sector": sector,
        "market": market,
        "n_peers": len(peers),
        "me": me,
        "peers": sorted(peers, key=lambda p: -(p.get("roe") or 0)),
        "percentiles": pcts,
        "interp": interp,
    }


def render_markdown(c: dict) -> str:
    if "error" in c:
        return f"_(erro peer_compare: {c['error']})_"

    lines = [f"## 🧩 Peer comparison — {c['sector']} ({c['n_peers']} tickers)\n"]
    lines.append(f"_Mercado: {c['market'].upper()}. {c['ticker']} destacado em **negrito**._\n")

    # Percentile summary
    p = c["percentiles"]; i = c["interp"]
    lines.append("| Métrica | Valor | Percentil | Interpretação |")
    lines.append("|---|---:|---:|---|")
    def fp(v, fmt="{:.2f}"): return fmt.format(v) if v is not None else "—"
    me = c["me"]
    lines.append(f"| P/E    | {fp(me['pe'])}   | P{p['pe']:.0f}   | {i['pe']} |" if p['pe'] is not None else "| P/E | — | — | — |")
    lines.append(f"| P/B    | {fp(me['pb'])}   | P{p['pb']:.0f}   | {i['pb']} |" if p['pb'] is not None else "| P/B | — | — | — |")
    dy_s = f"{me['dy']*100:.2f}%" if me['dy'] is not None else "—"
    lines.append(f"| DY     | {dy_s}          | P{p['dy']:.0f}   | {i['dy']} |" if p['dy'] is not None else "| DY | — | — | — |")
    roe_s = f"{me['roe']*100:.1f}%" if me['roe'] is not None else "—"
    lines.append(f"| ROE    | {roe_s}         | P{p['roe']:.0f}  | {i['roe']} |" if p['roe'] is not None else "| ROE | — | — | — |")
    lines.append(f"| Streak | {fp(me['streak'],'{:.0f}y')} | P{p['streak']:.0f} | {i['streak']} |" if p['streak'] is not None else "| Streak | — | — | — |")
    lines.append("")

    # Table with peers
    lines.append("### Peers (ranked ROE)\n")
    lines.append("| Ticker | Price | P/E | P/B | DY % | ROE % | Streak |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for p in c["peers"][:15]:
        is_me = p["ticker"] == c["ticker"]
        prefix = "**" if is_me else ""
        suffix = "**" if is_me else ""
        tk_link = f"{prefix}[[{p['ticker']}]]{suffix}"
        price_s = f"{p['price']:.2f}" if p['price'] is not None else "—"
        pe_s = f"{p['pe']:.2f}" if p['pe'] is not None else "—"
        pb_s = f"{p['pb']:.2f}" if p['pb'] is not None else "—"
        dy_s = f"{p['dy']*100:.2f}" if p['dy'] is not None else "—"
        roe_s = f"{p['roe']*100:.1f}" if p['roe'] is not None else "—"
        streak_s = f"{p['streak']}" if p['streak'] is not None else "—"
        lines.append(f"| {tk_link} | {price_s} | {pe_s} | {pb_s} | {dy_s} | {roe_s} | {streak_s} |")
    lines.append("")
    return "\n".join(lines)


def write_into_vault(ticker: str, md: str) -> Path:
    import re
    path = VAULT / "tickers" / f"{ticker}.md"
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n## 🧩 Peer comparison.*?(?=\n## |\Z)", "", text, count=1, flags=re.DOTALL)
    # Insert before "## Fundamentals" if present, else append near end
    insert_at = text.find("## Fundamentals")
    if insert_at > 0:
        text = text[:insert_at] + md + "\n" + text[insert_at:]
    else:
        text = text.rstrip() + "\n\n" + md + "\n"
    path.write_text(text, encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("ticker", nargs="?")
    g.add_argument("--all-holdings", action="store_true")
    ap.add_argument("--md", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    if args.all_holdings:
        for market, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                tickers = [r[0] for r in c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                )]
            for tk in tickers:
                try:
                    c_ = compare(tk)
                    md = render_markdown(c_)
                    print(f"\n=== {tk} ({c_.get('sector','?')}) ===")
                    if args.write:
                        p = write_into_vault(tk, md)
                        print(f"  wrote {p}")
                    else:
                        print(md[:500])
                except Exception as e:  # noqa: BLE001
                    print(f"  {tk}: ERROR — {e}")
        return 0

    if not args.ticker:
        ap.print_help()
        return 1
    tk = args.ticker.upper()
    c_ = compare(tk)
    md = render_markdown(c_)
    print(md)
    if args.write:
        p = write_into_vault(tk, md)
        print(f"\n[wrote] {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
