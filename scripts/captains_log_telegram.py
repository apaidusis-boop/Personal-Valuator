"""captains_log_telegram — empacota Captain's Log num push diário Telegram.

Phase DD/H (2026-04-25). Builds on Phase CC (Captain's Log data layer).

Renderização text-first compact (mobile-friendly):
  - Pulse summary line (1 linha)
  - Top 3 conviction (uma linha cada)
  - Top 3 pending decisions
  - Top 3 IC committee latest verdicts
  - Top 2 variant views (high magnitude)
  - Top 3 RI material changes
  - Top 3 alerts

Total ~30-40 linhas, ~2000 chars (Telegram limit 4096; conservador).

Zero tokens Claude. Lê de DB + vault frontmatter.

Uso:
  python scripts/captains_log_telegram.py              # send
  python scripts/captains_log_telegram.py --dry-run    # print only
  python scripts/captains_log_telegram.py --silent     # no notification sound
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts import _captains_log as cl


def _emoji_for_score(s: int) -> str:
    if s >= 80:
        return "🟢"
    if s >= 60:
        return "🟡"
    if s >= 40:
        return "🟠"
    return "🔴"


def _emoji_for_verdict(v: str) -> str:
    v = (v or "").upper()
    if v in ("BUY", "ACCUMULATE"):
        return "🟢"
    if v in ("HOLD", "MIXED"):
        return "🟡"
    if v in ("AVOID", "SELL", "EXIT"):
        return "🔴"
    return "⚪"


def render() -> str:
    today = date.today()
    lines: list[str] = []
    lines.append(f"*🧭 Captain's Log — {today.strftime('%a %d %b')}*")

    # Pulse
    p = cl.pulse()
    pulse_line = (
        f"`{p.holdings_count} holdings · "
        f"{p.open_actions_count} pending · "
        f"{p.perpetuum_alerts_count} alerts · "
        f"{p.high_variance_count} variant`"
    )
    lines.append(pulse_line)
    lines.append("")

    # Top conviction (3)
    top = cl.top_conviction(3)
    if top:
        lines.append("*🏆 Top conviction*")
        for c in top:
            tag = _emoji_for_score(c.composite_score)
            lines.append(f"{tag} `{c.ticker:<7}` {c.composite_score}/100 "
                         f"({c.market.upper()})  th={c.thesis_health} ic={c.ic_consensus} v={c.variant}")
        lines.append("")

    # Pending decisions (3) — wrap kind+hint in code to escape underscores
    actions = cl.open_actions(3)
    if actions:
        lines.append("*📥 Pending decisions*")
        for a in actions:
            kind_short = (a.kind or "").replace("perpetuum:", "")[:18]
            hint_short = (a.action_hint or "")[:60]
            lines.append(f"⚠️ #{a.id} `{a.ticker}` `{a.market.upper()}/{kind_short}` `{hint_short}`")
        lines.append("")

    # Committee latest (3)
    debates = cl.recent_ic_debates(3)
    if debates:
        lines.append("*🏛️ Committee latest*")
        for d in debates:
            tag = _emoji_for_verdict(d.verdict)
            consensus = f" {d.consensus_pct:.0f}%" if d.consensus_pct else ""
            lines.append(f"{tag} `{d.ticker:<7}` {d.verdict}{consensus} "
                         f"({d.confidence})")
        lines.append("")

    # Variant view (2)
    variants = cl.high_variance_views(2, min_magnitude=2)
    if variants:
        lines.append("*🎯 Variant view*")
        for v in variants:
            lines.append(f"• `{v.ticker:<7}` {v.variance.replace('_', ' ')} "
                         f"(mag {v.magnitude}/5)")
        lines.append("")

    # RI changes (3)
    changes = cl.recent_ri_changes(3, threshold_pct=15.0)
    if changes:
        lines.append("*📊 RI material changes (YoY)*")
        for r in changes:
            arrow = "▲" if r.direction == "up" else "▼"
            lines.append(f"{arrow} `{r.ticker:<7}` {r.metric.replace('_', ' '):<12} "
                         f"{r.yoy_pct:+.1f}%  ({r.period_end})")
        lines.append("")

    # Alerts (3) — wrap perpetuum_name in code to escape underscores
    alerts = cl.recent_alerts(3)
    if alerts:
        lines.append("*🚨 Perpetuum alerts*")
        for al in alerts:
            lines.append(f"• `{al.subject_id[:30]}` `{al.perpetuum_name}` "
                         f"score {al.score} (was {al.prev_score}, drop {al.drop})")
        lines.append("")

    lines.append("_Open dashboard for drill-down: localhost:8501_")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print message; do not send")
    ap.add_argument("--silent", action="store_true",
                    help="send without notification sound")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    msg = render()
    if args.dry_run:
        print(msg)
        print(f"\n[dry-run — {len(msg)} chars]")
        return 0

    from notifiers.telegram import send
    result = send(msg, silent=args.silent)
    if result.get("ok"):
        print(f"sent ({len(msg)} chars) ok")
        return 0
    print(f"send failed: {result}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
