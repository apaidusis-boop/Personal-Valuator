"""earnings_surprise — compara YT price-targets / guidance vs preço actual.

Extrai price-targets mencionados em video_insights via regex sobre `claim`,
por ticker. Compara com preço actual + 30d forward-return pós-mention.
Mede accuracy / bias dos canais retroactivamente.

Uso:
    python scripts/earnings_surprise.py                 # overview all tickers
    python scripts/earnings_surprise.py --ticker ACN
    python scripts/earnings_surprise.py --channel "Virtual Asset"
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

TARGET_RE = re.compile(
    r"(?:preço[- ]?alvo|preco[- ]?alvo|target|price target)[^.]*?(R\$|US\$|\$)\s?([\d.,]+)",
    re.IGNORECASE,
)


def _parse_target(claim: str) -> tuple[str, float] | None:
    m = TARGET_RE.search(claim)
    if not m:
        return None
    cur = m.group(1)
    val_s = m.group(2).replace(".", "").replace(",", ".")
    try:
        return cur, float(val_s)
    except ValueError:
        return None


def _price_on_or_after(conn: sqlite3.Connection, ticker: str, iso_date: str) -> float | None:
    r = conn.execute(
        "SELECT close FROM prices WHERE ticker=? AND date>=? ORDER BY date LIMIT 1",
        (ticker, iso_date),
    ).fetchone()
    return r[0] if r else None


def _latest_price(conn: sqlite3.Connection, ticker: str) -> float | None:
    r = conn.execute(
        "SELECT close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    return r[0] if r else None


def collect(ticker_filter: str | None = None, channel_filter: str | None = None) -> list[dict]:
    """Devolve lista de mentions [{ticker, channel, date, target, price_then, price_now, upside_then, return_since}]."""
    out: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            q = """SELECT i.ticker, v.channel, v.published_at, i.claim, i.confidence
                   FROM video_insights i LEFT JOIN videos v ON v.video_id=i.video_id
                   WHERE v.published_at IS NOT NULL"""
            args: list = []
            if ticker_filter:
                q += " AND i.ticker=?"; args.append(ticker_filter)
            if channel_filter:
                q += " AND v.channel=?"; args.append(channel_filter)
            q += " ORDER BY v.published_at DESC"
            rows = c.execute(q, args).fetchall()
            for tk, ch, d, claim, conf in rows:
                t = _parse_target(claim)
                if not t:
                    continue
                cur, target_val = t
                price_then = _price_on_or_after(c, tk, d)
                price_now = _latest_price(c, tk)
                if price_then is None:
                    continue
                upside_then = (target_val / price_then - 1) * 100
                ret_since = ((price_now / price_then - 1) * 100) if price_now else None
                out.append({
                    "ticker": tk, "market": market, "channel": ch,
                    "date": d, "claim": claim[:140], "confidence": conf,
                    "currency": cur, "target": target_val,
                    "price_then": round(price_then, 2),
                    "price_now": round(price_now, 2) if price_now else None,
                    "upside_pct_then": round(upside_then, 2),
                    "return_since_pct": round(ret_since, 2) if ret_since is not None else None,
                    "reached_target": (price_now is not None and price_now >= target_val),
                })
    return out


def summarize(mentions: list[dict]) -> dict:
    by_channel: dict[str, list] = defaultdict(list)
    by_ticker: dict[str, list] = defaultdict(list)
    for m in mentions:
        by_channel[m["channel"]].append(m)
        by_ticker[m["ticker"]].append(m)

    ch_stats = {}
    for ch, rows in by_channel.items():
        reached = sum(1 for r in rows if r["reached_target"])
        rets = [r["return_since_pct"] for r in rows if r["return_since_pct"] is not None]
        avg_ret = sum(rets) / len(rets) if rets else None
        ch_stats[ch] = {
            "n_targets": len(rows),
            "reached_pct": round(reached / len(rows) * 100, 1) if rows else 0,
            "avg_return_since": round(avg_ret, 2) if avg_ret is not None else None,
        }

    return {"channels": ch_stats, "total_mentions": len(mentions)}


def render(mentions: list[dict], summary: dict) -> str:
    if not mentions:
        return "(sem price-targets encontrados)"
    out = [f"# 🎯 Earnings / price-target surprise tracker — {summary['total_mentions']} mentions\n"]
    out.append("## Channel accuracy retrospectiva\n")
    out.append("| Canal | N | Reached % | Avg return since |")
    out.append("|---|---:|---:|---:|")
    for ch, s in sorted(summary["channels"].items(), key=lambda x: -x[1]["n_targets"]):
        r_pct = f"{s['reached_pct']:.1f}%" if s['reached_pct'] is not None else "—"
        a_ret = f"{s['avg_return_since']:+.2f}%" if s['avg_return_since'] is not None else "—"
        out.append(f"| {ch} | {s['n_targets']} | {r_pct} | {a_ret} |")
    out.append("")

    out.append("## Price-targets activos (top 30 recentes)\n")
    out.append("| Data | Ticker | Canal | Target | Price then | Price now | Upside então | Return since | Hit? |")
    out.append("|---|---|---|---:|---:|---:|---:|---:|---|")
    for m in mentions[:30]:
        hit = "✅" if m["reached_target"] else "—"
        now = f"{m['currency']}{m['price_now']:.2f}" if m['price_now'] else "—"
        ret = f"{m['return_since_pct']:+.2f}%" if m['return_since_pct'] is not None else "—"
        out.append(
            f"| {m['date']} | {m['ticker']} | {m['channel'][:16]} | "
            f"{m['currency']}{m['target']:.2f} | {m['currency']}{m['price_then']:.2f} | "
            f"{now} | {m['upside_pct_then']:+.1f}% | {ret} | {hit} |"
        )
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ticker")
    ap.add_argument("--channel")
    ap.add_argument("--md", action="store_true")
    args = ap.parse_args()

    mentions = collect(
        ticker_filter=args.ticker.upper() if args.ticker else None,
        channel_filter=args.channel,
    )
    summary = summarize(mentions)
    out = render(mentions, summary)
    print(out)

    if args.md:
        from datetime import date
        fp = ROOT / "reports" / f"earnings_surprise_{date.today().isoformat()}.md"
        fp.write_text(out, encoding="utf-8")
        vp = ROOT / "obsidian_vault" / "Earnings Surprise.md"
        vp.write_text(out, encoding="utf-8")
        print(f"\n[saved] {fp}")
        print(f"[saved] {vp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
