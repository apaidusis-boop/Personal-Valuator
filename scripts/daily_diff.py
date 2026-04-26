"""daily_diff — o que mudou hoje vs ontem (ou vs N dias atrás).

Output: markdown compacto com:
  - Price moves ≥ threshold% (default ±3%)
  - Screen transitions (watchlist→pass, holding→fail)
  - Triggers fired (novos)
  - Eventos SEC/CVM novos
  - YouTube insights novos

Zero tokens Claude. Pensado para feed em briefing matinal ou Telegram.

Uso:
    python scripts/daily_diff.py                  # hoje vs ontem
    python scripts/daily_diff.py --since 3        # últimos 3 dias
    python scripts/daily_diff.py --move-threshold 2   # ≥2% move
    python scripts/daily_diff.py --md > reports/diff_<date>.md
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
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


def _price_moves(since: str, thr_pct: float) -> list[dict]:
    """Tickers com |Δ price| ≥ thr_pct% desde `since`.
    Retorna holdings primeiro, watchlist depois."""
    out: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            rows = c.execute(f"""
                SELECT c.ticker, c.is_holding, p_now.close AS now_close, p_now.date AS now_date,
                       p_base.close AS base_close, p_base.date AS base_date
                FROM companies c
                JOIN (
                    SELECT ticker, MAX(date) AS d FROM prices GROUP BY ticker
                ) last ON last.ticker = c.ticker
                JOIN prices p_now ON p_now.ticker = c.ticker AND p_now.date = last.d
                JOIN (
                    SELECT ticker, MAX(date) AS d FROM prices WHERE date < ? GROUP BY ticker
                ) prev ON prev.ticker = c.ticker
                JOIN prices p_base ON p_base.ticker = c.ticker AND p_base.date = prev.d
                WHERE p_base.close IS NOT NULL AND p_base.close > 0
            """, (since,)).fetchall()
            for tk, is_h, n_c, n_d, b_c, b_d in rows:
                pct = (n_c / b_c - 1) * 100
                if abs(pct) >= thr_pct:
                    out.append({
                        "ticker": tk, "market": market, "is_holding": bool(is_h),
                        "now_close": n_c, "now_date": n_d,
                        "base_close": b_c, "base_date": b_d,
                        "change_pct": pct,
                    })
    out.sort(key=lambda x: (not x["is_holding"], x["change_pct"]))
    return out


def _screen_transitions(since: str) -> list[dict]:
    """Tickers cujo passes_screen mudou desde `since`."""
    out: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            rows = c.execute("""
                SELECT s_now.ticker, s_now.passes_screen AS now_pass, s_base.passes_screen AS base_pass,
                       s_now.score AS now_score, s_base.score AS base_score, s_now.run_date
                FROM (
                    SELECT ticker, MAX(run_date) AS d FROM scores GROUP BY ticker
                ) last_row
                JOIN scores s_now ON s_now.ticker = last_row.ticker AND s_now.run_date = last_row.d
                JOIN (
                    SELECT ticker, MAX(run_date) AS d FROM scores WHERE run_date < ? GROUP BY ticker
                ) prev_row ON prev_row.ticker = s_now.ticker
                JOIN scores s_base ON s_base.ticker = prev_row.ticker AND s_base.run_date = prev_row.d
                WHERE s_now.passes_screen <> s_base.passes_screen
            """, (since,)).fetchall()
            for tk, now_p, base_p, now_s, base_s, run_d in rows:
                out.append({
                    "ticker": tk, "market": market,
                    "transition": "became_pass" if now_p else "lost_pass",
                    "score_now": now_s, "score_prev": base_s, "run_date": run_d,
                })
    return out


def _new_events(since: str) -> list[dict]:
    """SEC/CVM events persistidos desde since."""
    out: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            for r in c.execute("""
                SELECT event_date, ticker, kind, source, summary
                FROM events WHERE event_date >= ? ORDER BY event_date DESC LIMIT 100
            """, (since,)):
                out.append({
                    "date": r[0], "ticker": r[1], "kind": r[2],
                    "source": r[3], "summary": (r[4] or "")[:150],
                    "market": market,
                })
    return out


def _new_triggers_fired(since: str) -> list[dict]:
    """Leitura directa do log trigger_monitor."""
    out: list[dict] = []
    log_dir = ROOT / "logs"
    for f in sorted(log_dir.glob("trigger_monitor_*.log"), reverse=True)[:5]:
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("event") != "fired":
                continue
            if d.get("ts", "")[:10] < since:
                continue
            out.append(d)
    return out


def _new_yt_insights(since: str) -> list[dict]:
    out: list[dict] = []
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                for r in c.execute("""
                    SELECT v.published_at, v.channel, i.ticker, i.kind, i.claim, i.confidence
                    FROM video_insights i JOIN videos v ON i.video_id = v.video_id
                    WHERE i.created_at >= ?
                    ORDER BY i.created_at DESC LIMIT 50
                """, (since,)):
                    out.append({
                        "published": r[0] or "",
                        "channel": r[1] or "",
                        "ticker": r[2], "kind": r[3],
                        "claim": r[4][:180], "confidence": r[5],
                    })
            except sqlite3.OperationalError:
                pass
    return out


def render_diff(since: str, moves: list, transitions: list, events: list,
                triggers: list, yt_insights: list, md: bool = False) -> str:
    lines = []
    H = "## " if md else ""
    today = date.today().isoformat()
    lines.append(f"{'# ' if md else ''}Daily Diff — {today} (since {since})")
    lines.append("")

    lines.append(f"{H}Price moves")
    if moves:
        holdings_moves = [m for m in moves if m["is_holding"]]
        watch_moves = [m for m in moves if not m["is_holding"]]
        if holdings_moves:
            lines.append("**Holdings:**")
            for m in holdings_moves:
                arrow = "▼" if m["change_pct"] < 0 else "▲"
                lines.append(f"- {arrow} **{m['ticker']}** ({m['market']}) {m['change_pct']:+.2f}% — {m['base_close']:.2f} → {m['now_close']:.2f}")
        if watch_moves:
            lines.append("**Watchlist:**")
            for m in watch_moves[:10]:
                arrow = "▼" if m["change_pct"] < 0 else "▲"
                lines.append(f"- {arrow} {m['ticker']} ({m['market']}) {m['change_pct']:+.2f}%")
    else:
        lines.append("_(nenhum move significativo)_")
    lines.append("")

    lines.append(f"{H}Screen transitions")
    if transitions:
        for t in transitions:
            icon = "✓" if t["transition"] == "became_pass" else "✗"
            lines.append(f"- {icon} **{t['ticker']}** ({t['market']}): {t['transition']} — score {t['score_prev']:.2f} → {t['score_now']:.2f}")
    else:
        lines.append("_(nenhuma)_")
    lines.append("")

    lines.append(f"{H}Triggers disparados")
    if triggers:
        for t in triggers[:15]:
            lines.append(f"- 🔔 **{t.get('ticker','?')}** / `{t.get('trigger_id','?')}` — {t.get('snapshot',{})}")
    else:
        lines.append("_(nenhum novo)_")
    lines.append("")

    lines.append(f"{H}Eventos SEC/CVM")
    if events:
        for e in events[:20]:
            lines.append(f"- **{e['date']}** {e['ticker']} `{e['kind']}` — {e['summary']}")
    else:
        lines.append("_(nenhum)_")
    lines.append("")

    lines.append(f"{H}YouTube insights (novos)")
    if yt_insights:
        for i in yt_insights[:15]:
            lines.append(f"- {i['published']} **{i['ticker']}** ({i['channel']}) [{i['kind']} conf={i['confidence']:.2f}] {i['claim']}")
    else:
        lines.append("_(nenhum)_")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--since", type=int, default=1, help="Dias atrás para comparar (default 1)")
    ap.add_argument("--move-threshold", type=float, default=3.0)
    ap.add_argument("--md", action="store_true", help="Output markdown para ficheiro")
    ap.add_argument("--save", action="store_true", help="Grava em reports/diff_<date>.md")
    args = ap.parse_args()

    since = (date.today() - timedelta(days=args.since)).isoformat()

    moves = _price_moves(since, args.move_threshold)
    transitions = _screen_transitions(since)
    events = _new_events(since)
    triggers = _new_triggers_fired(since)
    yt_insights = _new_yt_insights(since)

    out = render_diff(since, moves, transitions, events, triggers, yt_insights, md=args.md)
    print(out)

    if args.save:
        (ROOT / "reports").mkdir(exist_ok=True)
        fp = ROOT / "reports" / f"diff_{date.today().isoformat()}.md"
        fp.write_text(out, encoding="utf-8")
        print(f"\n[saved] {fp}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
