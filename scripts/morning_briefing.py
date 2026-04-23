"""morning_briefing — 1 comando que produz o briefing matinal completo.

Orquestra:
  1. Refresh intraday de holdings (yfinance)
  2. FX rate actual (PTAX)
  3. Daily diff (moves + transitions + events + triggers fired)
  4. Earnings calendar (próximos 14 dias)
  5. Top holdings em watch (biggest drawdown / near trigger)
  6. Fired triggers novos (últimas 24h)
  7. YouTube insights novos (últimas 24h)

Output: markdown em `obsidian_vault/briefings/YYYY-MM-DD.md` + stdout.

Zero tokens Claude. Pensado para cron matinal às 09:45 ou run manual.

Uso:
    python scripts/morning_briefing.py                      # corre tudo
    python scripts/morning_briefing.py --no-refresh         # pula yfinance
    python scripts/morning_briefing.py --stdout-only        # não escreve ficheiro
"""
from __future__ import annotations

import argparse
import io
import json
import sqlite3
import subprocess
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


def _capture(cmd: list[str]) -> str:
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=300,
        )
        return (r.stdout or "") + (("\n" + r.stderr) if r.returncode != 0 else "")
    except Exception as e:  # noqa: BLE001
        return f"(erro correr {' '.join(cmd)}: {e})"


def _py(script: str, *args: str) -> list[str]:
    return [sys.executable, "-X", "utf8", str(ROOT / script), *args]


def _refresh_holdings() -> str:
    return _capture(_py("scripts/refresh_ticker.py", "--all-holdings", "--quiet"))


def _fx_total() -> dict:
    from analytics.fx import total_portfolio_brl
    return total_portfolio_brl()


def _daily_diff(since_days: int) -> str:
    out = _capture(_py("scripts/daily_diff.py", "--since", str(since_days), "--move-threshold", "2.0"))
    return out


def _earnings_next(days: int) -> list[tuple]:
    today = date.today().isoformat()
    cutoff = (date.today() + timedelta(days=days)).isoformat()
    rows: list[tuple] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            try:
                for r in c.execute(
                    """SELECT e.ticker, e.earnings_date, c.name, c.is_holding
                       FROM earnings_calendar e LEFT JOIN companies c ON e.ticker=c.ticker
                       WHERE e.earnings_date >= ? AND e.earnings_date <= ?
                       ORDER BY e.earnings_date ASC""",
                    (today, cutoff),
                ):
                    rows.append((r[1], r[0], r[2] or r[0], bool(r[3]), market))
            except sqlite3.OperationalError:
                pass
    return rows


def _fired_triggers(hours: int) -> list[dict]:
    cutoff_iso = (datetime.now(UTC) - timedelta(hours=hours)).isoformat()
    out: list[dict] = []
    log_dir = ROOT / "logs"
    for f in sorted(log_dir.glob("trigger_monitor_*.log"), reverse=True)[:3]:
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("event") == "fired" and d.get("ts", "") >= cutoff_iso[:19]:
                out.append(d)
    return out


def _holdings_watchlist() -> list[dict]:
    """Holdings com flags: em drawdown ≥ 10%, ou screen lost, ou piotroski ≤ 4."""
    out: list[dict] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            rows = c.execute("""
                SELECT p.ticker, p.quantity, p.entry_price,
                       (SELECT close FROM prices WHERE ticker=p.ticker ORDER BY date DESC LIMIT 1) AS px,
                       (SELECT score FROM scores WHERE ticker=p.ticker ORDER BY run_date DESC LIMIT 1) AS screen,
                       (SELECT passes_screen FROM scores WHERE ticker=p.ticker ORDER BY run_date DESC LIMIT 1) AS pass
                FROM portfolio_positions p WHERE p.active=1
            """).fetchall()
            for tk, qty, entry, px, scr, ps in rows:
                if not px or not entry:
                    continue
                pnl = (px / entry - 1) * 100
                flags = []
                if pnl <= -15:
                    flags.append(f"drawdown {pnl:.1f}%")
                if scr is not None and scr < 0.6:
                    flags.append(f"screen {scr:.2f}")
                if ps == 0 and scr and scr >= 0.6:
                    flags.append("near pass")
                if flags:
                    out.append({
                        "ticker": tk, "market": market, "px": px, "pnl": pnl,
                        "flags": flags,
                    })
    out.sort(key=lambda x: x["pnl"])
    return out


def _recent_yt(hours: int) -> list[dict]:
    cutoff = (datetime.now(UTC) - timedelta(hours=hours)).isoformat()
    out: list[dict] = []
    for db in (DB_BR, DB_US):
        with sqlite3.connect(db) as c:
            try:
                for r in c.execute("""
                    SELECT i.ticker, i.kind, i.claim, i.confidence, v.channel, v.published_at
                    FROM video_insights i LEFT JOIN videos v ON i.video_id=v.video_id
                    WHERE i.created_at >= ? ORDER BY i.confidence DESC LIMIT 15
                """, (cutoff,)):
                    out.append({
                        "ticker": r[0], "kind": r[1], "claim": r[2][:180],
                        "confidence": r[3], "channel": r[4] or "", "published": r[5] or "",
                    })
            except sqlite3.OperationalError:
                pass
    return out


def build_briefing(refresh: bool, since_days: int, earnings_days: int) -> str:
    buf: list[str] = []
    today = date.today().isoformat()
    buf.append(f"# 🌅 Morning Briefing — {today}")
    buf.append(f"_Gerado às {datetime.now(UTC).strftime('%H:%M UTC')}_\n")

    if refresh:
        buf.append("## 1. Refresh intraday\n")
        r = _refresh_holdings()
        # resume: só o essencial
        lines = [ln for ln in r.splitlines() if "%" in ln]
        if lines:
            buf.append("```")
            buf.extend(lines[:12])
            buf.append("```")
        else:
            buf.append("_refresh executado_")
        buf.append("")

    # 2. Portfolio snapshot
    buf.append("## 2. Portfolio snapshot (consolidado BRL)\n")
    try:
        fx = _fx_total()
        buf.append(f"- **Total BRL**: R$ {fx['total_brl']:,.2f}  |  USD ${fx['total_usd']:,.2f}")
        buf.append(f"- BR equity: R$ {fx['br_mv_brl']:,.2f} ({fx['holdings_br']} holdings)")
        buf.append(f"- US equity: ${fx['us_mv_usd']:,.2f} = R$ {fx['us_mv_brl']:,.2f} ({fx['holdings_us']} holdings)")
        buf.append(f"- PTAX USDBRL: {fx['fx_ptax']:.4f}")
    except Exception as e:  # noqa: BLE001
        buf.append(f"_(erro fx: {e})_")
    buf.append("")

    # 3. Holdings em watch
    watch = _holdings_watchlist()
    buf.append("## 3. Holdings em atenção\n")
    if watch:
        for h in watch[:15]:
            flags = ", ".join(h["flags"])
            buf.append(f"- **{h['ticker']}** ({h['market']}) @ {h['px']:.2f}  P&L {h['pnl']:.1f}%  🚩 _{flags}_")
    else:
        buf.append("_(todas OK)_")
    buf.append("")

    # 4. Diff
    buf.append(f"## 4. Daily diff (últimos {since_days}d)\n")
    diff = _daily_diff(since_days)
    # strip header line do daily_diff para não duplicar
    diff_lines = diff.splitlines()
    if diff_lines and diff_lines[0].startswith("Daily Diff"):
        diff_lines = diff_lines[1:]
    buf.append("\n".join(diff_lines).strip())
    buf.append("")

    # 5. Fired triggers
    fired = _fired_triggers(hours=24)
    buf.append("## 5. Triggers fired (últimas 24h)\n")
    if fired:
        for t in fired[:10]:
            snap = t.get("snapshot", {})
            key_vals = ", ".join(f"{k}={v}" for k, v in snap.items() if k in ("price", "drop_pct", "dy_pct", "threshold_price"))
            buf.append(f"- 🔔 **{t.get('ticker','?')}** / `{t.get('trigger_id','?')}` — {key_vals}")
    else:
        buf.append("_(nenhum)_")
    buf.append("")

    # 6. Earnings próximos
    earn = _earnings_next(earnings_days)
    buf.append(f"## 6. Earnings próximos ({earnings_days}d)\n")
    if earn:
        for dt, tk, name, is_h, market in earn[:20]:
            mark = "★" if is_h else " "
            buf.append(f"- **{dt}** {mark} {tk} ({market}) — {name}")
    else:
        buf.append("_(nenhum agendado)_")
    buf.append("")

    # 7. YouTube insights recentes
    yt = _recent_yt(hours=48)
    buf.append("## 7. YouTube insights (últimas 48h, top-15 por confidence)\n")
    if yt:
        for i in yt:
            buf.append(f"- [{i['confidence']:.2f} {i['kind']}] **{i['ticker']}** _({i['channel']})_ — {i['claim']}")
    else:
        buf.append("_(nenhum)_")
    buf.append("")

    buf.append("---")
    buf.append("*Para análise deep de um ticker: `ii research <TK> --intraday`*  ")
    buf.append("*Para query semântica vault: `ii vault \"<pergunta>\"`*  ")
    buf.append("*Para refresh + export Obsidian: `ii obsidian --refresh --holdings-only`*")

    return "\n".join(buf)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-refresh", action="store_true")
    ap.add_argument("--since-days", type=int, default=1)
    ap.add_argument("--earnings-days", type=int, default=14)
    ap.add_argument("--stdout-only", action="store_true")
    args = ap.parse_args()

    text = build_briefing(
        refresh=not args.no_refresh,
        since_days=args.since_days,
        earnings_days=args.earnings_days,
    )
    print(text)

    if not args.stdout_only:
        today = date.today().isoformat()
        # Também guarda no vault Obsidian se existir
        vault_dir = ROOT / "obsidian_vault" / "briefings"
        vault_dir.mkdir(parents=True, exist_ok=True)
        (vault_dir / f"{today}.md").write_text(text, encoding="utf-8")
        # E em reports/ também
        reports_dir = ROOT / "reports"
        reports_dir.mkdir(exist_ok=True)
        (reports_dir / f"briefing_{today}.md").write_text(text, encoding="utf-8")
        print(f"\n[saved] obsidian_vault/briefings/{today}.md")
        print(f"[saved] reports/briefing_{today}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
