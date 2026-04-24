"""MorningBriefingAgent — compila briefing matinal via Ollama.

Combina:
  - Portfolio snapshot (total, P&L, top movers)
  - Triggers abertos (action_cli list)
  - Analyst insights novos (últimas 24h)
  - Earnings próximos 7d
  - YouTube insights recentes (últimas 24h)

Output:
  - obsidian_vault/briefings/YYYY-MM-DD.md  (canonical briefing)
  - Telegram push (se config.push_telegram and .env tem bot token)
  - Ollama sintetiza "top 3 things to know this morning"
"""
from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ._base import AgentContext, AgentResult, BaseAgent
from ._llm import llm_summarise


class MorningBriefingAgent(BaseAgent):
    name = "morning_briefing"
    description = "Compila briefing matinal + sintetiza via Ollama + push Telegram"
    default_schedule = "daily:07:00"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        today_iso = datetime.now().date().isoformat()
        actions: list[str] = []
        sections: list[str] = []
        raw_data: dict = {}

        # ── 1. Portfolio snapshot ────────────────────────────────
        try:
            total_br, total_us, top_gains, top_losses = self._portfolio_snapshot(root)
            raw_data["portfolio"] = {"br": total_br, "us": total_us}
            sections.append("## 💼 Portfolio")
            sections.append(f"- BR: R$ {total_br:,.0f}  |  US: $ {total_us:,.0f}")
            if top_gains:
                sections.append(f"- Top gains 1d: {', '.join(f'{t} +{p:.1f}%' for t, p in top_gains)}")
            if top_losses:
                sections.append(f"- Top losses 1d: {', '.join(f'{t} {p:.1f}%' for t, p in top_losses)}")
            sections.append("")
            actions.append(f"portfolio snapshot BR R${total_br:,.0f} + US ${total_us:,.0f}")
        except Exception as e:
            sections.append(f"## 💼 Portfolio\n- ⚠️ snapshot failed: {e}\n")

        # ── 2. Triggers abertos ──────────────────────────────────
        triggers = self._open_triggers(root, limit=self.config.get("max_triggers", 10))
        raw_data["triggers"] = triggers
        if triggers:
            sections.append(f"## ⚡ Open triggers ({len(triggers)})")
            for t in triggers[:10]:
                sections.append(f"- [{t['kind']}] {t['ticker']} → {t['action_hint']} — {t.get('note','')[:80]}")
            sections.append("")
            actions.append(f"{len(triggers)} open triggers flagged")
        else:
            sections.append("## ⚡ Open triggers\n- None open\n")

        # ── 3. Analyst insights novos (últimas 24h) ──────────────
        lookback_h = self.config.get("lookback_hours", 24)
        insights = self._recent_analyst_insights(root, hours=lookback_h,
                                                  limit=self.config.get("max_analyst_insights", 15))
        raw_data["analyst"] = insights
        if insights:
            sections.append(f"## 📰 Analyst insights (últimas {lookback_h}h, top {len(insights)})")
            for i in insights:
                stance = f" [{i['stance']}]" if i.get('stance') else ""
                tk = i.get('ticker') or 'MACRO'
                sections.append(f"- `{i['source']}` **{tk}**{stance}: {i['claim'][:150]}")
            sections.append("")
            actions.append(f"{len(insights)} analyst insights surfaced")

        # ── 4. Earnings próximos 7d ──────────────────────────────
        earnings = self._upcoming_earnings(root, days=7)
        raw_data["earnings"] = earnings
        if earnings:
            sections.append(f"## 📅 Earnings próximos 7d ({len(earnings)})")
            for e in earnings:
                sections.append(f"- {e['date']}  **{e['ticker']}**  ({e.get('name','')})")
            sections.append("")
            actions.append(f"{len(earnings)} earnings upcoming")

        # ── 5. Ollama synthesis ─────────────────────────────────
        synth_prompt = self._build_synth_prompt(raw_data)
        synth = llm_summarise(
            synth_prompt,
            system=(
                "És o analista pessoal do user. Escreve em PT BR curto e directo. "
                "Identifica max 3 TOP takeaways do dia. Sem fluff. Se nada material, diz "
                "'dia calmo'. Formato: bullet points numerados."
            ),
            max_tokens=500,
        )
        actions.append("ollama synth generated")

        # ── 6. Render final briefing ────────────────────────────
        body = [
            "---",
            f"type: daily_briefing",
            f"date: {today_iso}",
            f"generated_by: morning_briefing_agent",
            "tags: [briefing, agent]",
            "---",
            "",
            f"# 🌅 Morning Briefing — {today_iso}",
            "",
            "## 🎯 Top takeaways (Ollama)",
            "",
            synth,
            "",
        ] + sections

        briefing_md = "\n".join(body)

        # ── 7. Write to vault ───────────────────────────────────
        if not ctx.dry_run:
            vault = Path(os.environ.get("OBSIDIAN_VAULT_PATH") or (root / "obsidian_vault"))
            briefings_dir = vault / "briefings"
            briefings_dir.mkdir(parents=True, exist_ok=True)
            briefing_path = briefings_dir / f"{today_iso}.md"
            briefing_path.write_text(briefing_md, encoding="utf-8")
            actions.append(f"wrote {briefing_path}")

        # ── 8. Telegram push ────────────────────────────────────
        pushed = False
        if self.config.get("push_telegram") and not ctx.dry_run:
            pushed = self._telegram_push(root, today_iso, synth, raw_data)
            if pushed:
                actions.append("telegram push sent")

        summary = f"Briefing {today_iso} gerado. {len(triggers)} triggers, {len(insights)} insights, {len(earnings)} earnings."
        if pushed:
            summary += " Telegram ✓."

        return AgentResult(
            agent=self.name,
            status="ok" if sections else "no_action",
            summary=summary,
            started_at="", finished_at="", duration_sec=0,
            actions=actions,
            data=raw_data,
        )

    # ------ helpers ----------------------------------------------------

    def _portfolio_snapshot(self, root: Path) -> tuple[float, float, list, list]:
        total_br = 0.0
        total_us = 0.0
        gains, losses = [], []
        for market, db_name in [("br", "br_investments.db"), ("us", "us_investments.db")]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                rows = c.execute("""
                    SELECT p.ticker, p.quantity,
                      (SELECT close FROM prices pr WHERE pr.ticker=p.ticker ORDER BY pr.date DESC LIMIT 1) AS last_close,
                      (SELECT close FROM prices pr WHERE pr.ticker=p.ticker ORDER BY pr.date DESC LIMIT 1 OFFSET 1) AS prev_close
                    FROM portfolio_positions p WHERE p.active=1
                """).fetchall()
                for t, q, lc, pc in rows:
                    if not lc:
                        continue
                    mv = q * lc
                    if market == "br": total_br += mv
                    else: total_us += mv
                    if pc and pc > 0:
                        pct = (lc / pc - 1) * 100
                        if pct > 0.5: gains.append((t, pct))
                        elif pct < -0.5: losses.append((t, pct))
        gains = sorted(gains, key=lambda x: -x[1])[:3]
        losses = sorted(losses, key=lambda x: x[1])[:3]
        return total_br, total_us, gains, losses

    def _open_triggers(self, root: Path, limit: int = 10) -> list[dict]:
        out = []
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                try:
                    rows = c.execute(
                        "SELECT ticker, kind, action_hint, note, created_at "
                        "FROM watchlist_actions WHERE status='open' ORDER BY created_at DESC LIMIT ?",
                        (limit,),
                    ).fetchall()
                    for r in rows:
                        out.append(dict(r))
                except sqlite3.OperationalError:
                    pass
        return out[:limit]

    def _recent_analyst_insights(self, root: Path, hours: int = 24, limit: int = 15) -> list[dict]:
        out = []
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat(timespec="seconds")
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                try:
                    rows = c.execute("""
                        SELECT r.source, r.title, i.ticker, i.kind, i.claim, i.stance, i.confidence
                        FROM analyst_insights i JOIN analyst_reports r ON i.report_id=r.id
                        WHERE i.created_at >= ?
                        ORDER BY i.confidence DESC, i.created_at DESC LIMIT ?
                    """, (cutoff, limit)).fetchall()
                    for r in rows:
                        out.append(dict(r))
                except sqlite3.OperationalError:
                    pass
        return sorted(out, key=lambda x: -x.get("confidence", 0))[:limit]

    def _upcoming_earnings(self, root: Path, days: int = 7) -> list[dict]:
        out = []
        today = datetime.now().date().isoformat()
        cutoff = (datetime.now().date() + timedelta(days=days)).isoformat()
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                try:
                    rows = c.execute("""
                        SELECT e.ticker, e.event_date AS date, c.name
                        FROM events e LEFT JOIN companies c ON c.ticker=e.ticker
                        WHERE e.kind='earnings' AND e.event_date BETWEEN ? AND ?
                        ORDER BY e.event_date ASC
                    """, (today, cutoff)).fetchall()
                    for r in rows:
                        out.append(dict(r))
                except sqlite3.OperationalError:
                    pass
        return out

    def _build_synth_prompt(self, raw: dict) -> str:
        parts = []
        p = raw.get("portfolio", {})
        parts.append(f"Portfolio: BR R${p.get('br',0):,.0f}, US ${p.get('us',0):,.0f}")
        if raw.get("triggers"):
            parts.append(f"\nTriggers abertos ({len(raw['triggers'])}):")
            for t in raw["triggers"][:10]:
                parts.append(f"- {t.get('ticker')}: {t.get('kind')} → {t.get('action_hint')}")
        if raw.get("analyst"):
            parts.append(f"\nAnalyst insights recentes ({len(raw['analyst'])}):")
            for i in raw["analyst"][:10]:
                st = f"[{i.get('stance')}]" if i.get('stance') else ""
                parts.append(f"- {i.get('source')} {i.get('ticker') or 'MACRO'} {st}: {(i.get('claim') or '')[:200]}")
        if raw.get("earnings"):
            parts.append(f"\nEarnings próximos 7d: {', '.join(e['ticker'] for e in raw['earnings'])}")
        return "Dados:\n" + "\n".join(parts) + "\n\nEscreve o TOP 3 takeaways para o user investir tempo HOJE."

    def _telegram_push(self, root: Path, today: str, synth: str, raw: dict) -> bool:
        try:
            py = sys.executable
            msg = f"🌅 Briefing {today}\n\n{synth[:2800]}\n\n⚡ {len(raw.get('triggers', []))} triggers · 📰 {len(raw.get('analyst', []))} insights"
            r = subprocess.run(
                [py, "-X", "utf8", "-m", "notifiers.telegram", msg],
                capture_output=True, text=True, timeout=30, cwd=str(root),
            )
            return r.returncode == 0
        except Exception:
            return False
