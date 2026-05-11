"""yt_digest — relatório compacto de video_insights/themes (SQL-only).

Zero LLM, zero rede. Output optimizado para copiar/colar em Claude ou ler
directamente. Útil para minimizar tokens: Claude vê o digest, não os 300+
raw insights.

Usos:
    python scripts/yt_digest.py --channel "Virtual Asset" --days 30
    python scripts/yt_digest.py --ticker PETR4 --days 60
    python scripts/yt_digest.py --holdings-only --days 30
    python scripts/yt_digest.py --themes --days 30
    python scripts/yt_digest.py --channel "Virtual Asset" --days 30 --md
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

PRICE_TARGET_RE = re.compile(
    r"(?:preço[- ]?alvo|preco[- ]?alvo|target|price target)[^.]*?(R\$|\$|US\$)\s?([\d.,]+)",
    re.IGNORECASE,
)


def _since(days: int) -> str:
    return (datetime.now(UTC) - timedelta(days=days)).strftime("%Y-%m-%d")


def _holdings_set() -> set[str]:
    holdings: set[str] = set()
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                for (t,) in c.execute("SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"):
                    holdings.add(t)
            except sqlite3.OperationalError:
                pass
    return holdings


def _fetch_videos(since: str, channel: str | None) -> list[tuple]:
    sql = """SELECT video_id, channel, title, published_at, duration_sec
             FROM videos WHERE (published_at >= ? OR processed_at >= ?)"""
    args = [since, since]
    if channel:
        sql += " AND channel = ?"
        args.append(channel)
    sql += " ORDER BY published_at DESC, processed_at DESC"
    with sqlite3.connect(DB_BR) as c:
        return c.execute(sql, args).fetchall()


def _fetch_insights(video_ids: list[str]) -> list[dict]:
    if not video_ids:
        return []
    rows: list[dict] = []
    placeholders = ",".join(["?"] * len(video_ids))
    sql = f"""SELECT video_id, ticker, kind, claim, confidence, created_at
              FROM video_insights WHERE video_id IN ({placeholders})"""
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            for r in c.execute(sql, video_ids):
                rows.append({
                    "video_id": r[0], "ticker": r[1], "kind": r[2],
                    "claim": r[3], "confidence": r[4], "created_at": r[5],
                })
    return rows


def _fetch_themes(video_ids: list[str]) -> list[dict]:
    if not video_ids:
        return []
    placeholders = ",".join(["?"] * len(video_ids))
    sql = f"""SELECT video_id, theme, stance, summary, confidence
              FROM video_themes WHERE video_id IN ({placeholders})"""
    rows: list[dict] = []
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            for r in c.execute(sql, video_ids):
                rows.append({
                    "video_id": r[0], "theme": r[1], "stance": r[2],
                    "summary": r[3], "confidence": r[4],
                })
    return rows


def _extract_price_targets(insights: list[dict]) -> dict[str, list[tuple[str, float, str]]]:
    """Por ticker, lista de (currency, value, claim_snippet)."""
    out: dict[str, list[tuple[str, float, str]]] = defaultdict(list)
    for i in insights:
        for m in PRICE_TARGET_RE.finditer(i["claim"]):
            cur = m.group(1)
            val_str = m.group(2).replace(".", "").replace(",", ".")
            try:
                val = float(val_str)
            except ValueError:
                continue
            out[i["ticker"]].append((cur, val, i["claim"][:100]))
    return out


def _kind_mix(insights: list[dict], ticker: str) -> Counter:
    return Counter(i["kind"] for i in insights if i["ticker"] == ticker)


def print_channel_rundown(channel: str, days: int, md: bool = False) -> None:
    since = _since(days)
    vids = _fetch_videos(since, channel)
    if not vids:
        print(f"(nenhum vídeo do canal '{channel}' nos últimos {days}d)")
        return
    video_ids = [v[0] for v in vids]
    insights = _fetch_insights(video_ids)
    themes = _fetch_themes(video_ids)

    H = "## " if md else ""
    HH = "### " if md else "  "
    print(f"{H}{channel} — últimos {days}d ({since} → hoje)")
    print(f"Vídeos: {len(vids)} | Insights: {len(insights)} | Temas: {len(themes)}")
    print()

    # Ranking de tickers por cobertura
    ticker_count = Counter(i["ticker"] for i in insights)
    print(f"{HH}Tickers mais mencionados")
    for tk, n in ticker_count.most_common(15):
        kinds = _kind_mix(insights, tk)
        kind_str = " ".join(f"{k}:{v}" for k, v in kinds.most_common(3))
        print(f"  {tk:<8} {n:>3}  ({kind_str})")
    print()

    # Themes
    theme_count = Counter(t["theme"] for t in themes)
    print(f"{HH}Temas macro")
    for th, n in theme_count.most_common(12):
        stances = Counter(t["stance"] for t in themes if t["theme"] == th)
        ss = ",".join(f"{k}:{v}" for k, v in stances.items() if k)
        print(f"  {th:<24} {n:>3}  ({ss})")
    print()

    # Price targets
    pts = _extract_price_targets(insights)
    if pts:
        print(f"{HH}Price-targets extraídos")
        for tk, lst in sorted(pts.items()):
            vals = [v for _, v, _ in lst]
            vals.sort()
            med = vals[len(vals) // 2]
            print(f"  {tk:<8}  n={len(vals):<2}  min={vals[0]:.2f}  med={med:.2f}  max={vals[-1]:.2f}")
        print()

    # Top claims por ticker (primeiros 2 por ticker, ordenados por confidence)
    print(f"{HH}Top insights (high confidence)")
    by_ticker: dict[str, list[dict]] = defaultdict(list)
    for i in insights:
        by_ticker[i["ticker"]].append(i)
    for tk in sorted(by_ticker, key=lambda x: -len(by_ticker[x]))[:10]:
        rows = sorted(by_ticker[tk], key=lambda x: -x["confidence"])[:2]
        print(f"  — {tk} —")
        for r in rows:
            print(f"    [{r['confidence']:.2f} {r['kind']}] {r['claim'][:140]}")
    print()

    # Vídeos processados
    print(f"{HH}Vídeos no período")
    for v in vids:
        d = v[4] or 0
        print(f"  {v[3] or '??????????'}  {v[0]}  ({d}s)  {(v[2] or '')[:80]}")


def print_ticker_rundown(ticker: str, days: int) -> None:
    since = _since(days)
    with sqlite3.connect(DB_BR) as c:
        rows_br = c.execute("""
            SELECT i.video_id, v.channel, v.published_at, i.kind, i.claim, i.confidence
            FROM video_insights i JOIN videos v ON i.video_id=v.video_id
            WHERE i.ticker=? AND (v.published_at >= ? OR i.created_at >= ?)
            ORDER BY v.published_at DESC, i.confidence DESC
        """, (ticker, since, since)).fetchall()
    with sqlite3.connect(DB_US) as c:
        rows_us = c.execute("""
            SELECT i.video_id, v.channel, v.published_at, i.kind, i.claim, i.confidence
            FROM video_insights i JOIN videos v ON i.video_id=v.video_id
            WHERE i.ticker=? AND (v.published_at >= ? OR i.created_at >= ?)
            ORDER BY v.published_at DESC, i.confidence DESC
        """, (ticker, since, since)).fetchall()
    rows = rows_br + rows_us
    print(f"{ticker} — últimos {days}d: {len(rows)} insights")
    print()
    kinds = Counter(r[3] for r in rows)
    print("Kinds:", dict(kinds.most_common()))
    print()
    for r in rows[:30]:
        print(f"  [{r[2] or '??'} {r[1][:16]:<16} conf={r[5]:.2f} {r[3]:<12}] {r[4][:150]}")


def print_holdings_scan(days: int) -> None:
    holdings = _holdings_set()
    if not holdings:
        print("Sem holdings activas em portfolio_positions.")
        return
    since = _since(days)
    print(f"Holdings scan — últimos {days}d (since {since})")
    print()
    for tk in sorted(holdings):
        for db in (DB_BR, DB_US):
            with sqlite3.connect(db) as c:
                try:
                    n = c.execute("""
                        SELECT COUNT(*) FROM video_insights i
                        JOIN videos v ON i.video_id=v.video_id
                        WHERE i.ticker=? AND (v.published_at >= ? OR i.created_at >= ?)
                    """, (tk, since, since)).fetchone()[0]
                except sqlite3.OperationalError:
                    n = 0
            if n > 0:
                print(f"  {tk:<8} {n:>3} insights")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--channel")
    ap.add_argument("--ticker")
    ap.add_argument("--holdings-only", action="store_true")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--md", action="store_true", help="Output markdown-friendly")
    args = ap.parse_args()

    if args.ticker:
        print_ticker_rundown(args.ticker, args.days)
    elif args.channel:
        print_channel_rundown(args.channel, args.days, md=args.md)
    elif args.holdings_only:
        print_holdings_scan(args.days)
    else:
        ap.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
