"""WatchdogAgent — event-driven poller (every:15m).

Responsabilidades:
  1. Detectar analyst_reports com extract_status='pending' → auto-extract (Ollama).
  2. Detectar watchlist_actions novos (criados < 15min atrás) → Telegram alert.
  3. Detectar earnings hoje → Telegram recordatório.

Não chama Claude. Se algo falha, log + continua. Idempotente.
"""
from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ._base import AgentContext, AgentResult, BaseAgent


class WatchdogAgent(BaseAgent):
    name = "watchdog"
    description = "Event-driven 15min poller — extract pending + trigger alerts"
    default_schedule = "every:15m"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        actions: list[str] = []
        errors: list[str] = []
        data = {}

        # ── 1. Auto-extract pending analyst reports ──────────────
        if self.config.get("auto_extract", True):
            try:
                n = self._auto_extract(root, limit=self.config.get("max_extract_per_run", 5))
                if n > 0:
                    actions.append(f"extracted {n} analyst reports")
                data["extracted"] = n
            except Exception as e:
                errors.append(f"auto_extract: {type(e).__name__}: {e}")

        # ── 2. Alert new triggers ────────────────────────────────
        if self.config.get("alert_new_triggers", True):
            try:
                new_triggers = self._new_triggers(root, minutes=20)
                data["new_triggers"] = new_triggers
                if new_triggers and not ctx.dry_run:
                    pushed = self._push_trigger_alerts(root, new_triggers)
                    if pushed:
                        actions.append(f"telegram alert for {len(new_triggers)} new triggers")
            except Exception as e:
                errors.append(f"trigger_alert: {type(e).__name__}: {e}")

        # ── 3. Earnings today reminder (once per day) ────────────
        try:
            from agents._state import AgentState
            state = AgentState(self.name, root=root)
            today_iso = datetime.now().date().isoformat()
            if state.get("earnings_pinged_for") != today_iso:
                earnings_today = self._earnings_today(root)
                if earnings_today and not ctx.dry_run:
                    self._push_earnings_reminder(root, earnings_today)
                    actions.append(f"earnings today reminder: {len(earnings_today)}")
                if earnings_today:
                    state.set("earnings_pinged_for", today_iso)
                    state.save()
        except Exception as e:
            errors.append(f"earnings: {type(e).__name__}: {e}")

        # Summary
        if not actions and not errors:
            return AgentResult(
                agent=self.name, status="no_action",
                summary="nothing new in last 15min",
                started_at="", finished_at="", duration_sec=0,
                data=data,
            )
        status = "failed" if errors and not actions else "ok"
        summary = " · ".join(actions) if actions else f"{len(errors)} errors"
        return AgentResult(
            agent=self.name, status=status, summary=summary,
            started_at="", finished_at="", duration_sec=0,
            actions=actions, errors=errors, data=data,
        )

    # ------ helpers ----------------------------------------------------

    def _auto_extract(self, root: Path, limit: int = 5) -> int:
        py = sys.executable
        total = 0
        for src in ("fool", "xp", "wsj"):
            try:
                r = subprocess.run(
                    [py, "-X", "utf8", str(root / "scripts" / "subscriptions_cli.py"),
                     "extract", "--source", src, "--limit", str(limit)],
                    capture_output=True, text=True, timeout=900, cwd=str(root),
                    encoding="utf-8", errors="replace",
                )
                # parse "N reports extracted" from output
                for line in (r.stdout or "").splitlines():
                    if "reports extracted" in line.lower():
                        import re
                        m = re.search(r"(\d+)\s+reports", line)
                        if m:
                            total += int(m.group(1))
            except subprocess.TimeoutExpired:
                pass
            except Exception:
                pass
        return total

    def _new_triggers(self, root: Path, minutes: int = 20) -> list[dict]:
        cutoff = (datetime.now() - timedelta(minutes=minutes)).isoformat(timespec="seconds")
        out = []
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                try:
                    rows = c.execute("""
                        SELECT ticker, kind, action_hint, note, created_at
                        FROM watchlist_actions
                        WHERE status='open' AND created_at >= ?
                        ORDER BY created_at DESC
                    """, (cutoff,)).fetchall()
                    for r in rows:
                        out.append(dict(r))
                except sqlite3.OperationalError:
                    pass
        return out

    def _earnings_today(self, root: Path) -> list[dict]:
        today = datetime.now().date().isoformat()
        out = []
        for db_name in ["br_investments.db", "us_investments.db"]:
            db = root / "data" / db_name
            if not db.exists():
                continue
            with sqlite3.connect(db) as c:
                c.row_factory = sqlite3.Row
                try:
                    rows = c.execute("""
                        SELECT e.ticker, e.event_date
                        FROM events e WHERE e.kind='earnings' AND e.event_date=?
                    """, (today,)).fetchall()
                    out.extend(dict(r) for r in rows)
                except sqlite3.OperationalError:
                    pass
        return out

    def _push_trigger_alerts(self, root: Path, triggers: list[dict]) -> bool:
        lines = ["⚡ New triggers (last 15min):", ""]
        for t in triggers[:10]:
            lines.append(f"• **{t['ticker']}** [{t['kind']}] → {t.get('action_hint','')}")
            if t.get("note"):
                lines.append(f"   _{t['note'][:100]}_")
        return self._telegram(root, "\n".join(lines))

    def _push_earnings_reminder(self, root: Path, earnings: list[dict]) -> bool:
        tickers = ", ".join(e["ticker"] for e in earnings[:10])
        msg = f"📅 Earnings HOJE: {tickers}"
        return self._telegram(root, msg)

    def _telegram(self, root: Path, msg: str) -> bool:
        try:
            py = sys.executable
            r = subprocess.run(
                [py, "-X", "utf8", "-m", "notifiers.telegram", msg],
                capture_output=True, text=True, timeout=20, cwd=str(root),
            )
            return r.returncode == 0
        except Exception:
            return False
