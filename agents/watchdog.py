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
from datetime import datetime, timedelta
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

        # ── 4. Cron failure detection ────────────────────────────
        # Added 2026-05-08 after daily 2026-05-07 was killed at CVM step
        # and nothing alerted. Promotes scheduled-task failures to emergency.
        try:
            from agents._state import AgentState
            state = AgentState(self.name, root=root)
            failed = self._cron_failures()
            data["cron_failures"] = len(failed)
            for task in failed:
                key = f"cron_pinged_{task['name']}_{task['last_run_date']}"
                if state.get(key):
                    continue  # already alerted today for this failure
                if not ctx.dry_run:
                    self._push_cron_emergency(root, task)
                    self._heartbeat_resume_entry(root, task)
                    state.set(key, True)
                    state.save()
                actions.append(f"cron emergency: {task['name']} exit={task['last_result']}")
        except Exception as e:
            errors.append(f"cron_check: {type(e).__name__}: {e}")

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
                        SELECT id, ticker, kind, action_hint, notes, opened_at
                        FROM watchlist_actions
                        WHERE status='open' AND opened_at >= ?
                        ORDER BY opened_at DESC
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
        """JJ-AOW MVP: 1 mensagem por trigger com inline buttons
        approve/ignore/defer. Permite ao founder agir do Telegram sem CLI.

        Aggregate text-only message kept para summary > 3 triggers (evitar
        spam de N mensagens individuais)."""
        if not triggers:
            return False

        try:
            from notifiers.telegram import send as telegram_send
        except ImportError:
            return self._telegram(root, "⚡ Triggers detectados — ver MC /alerts")

        # Cap to 5 individual messages; rest goes to summary
        individual = triggers[:5]
        ok_count = 0
        for t in individual:
            action_id = t.get("id")
            if not action_id:
                continue
            kind = t.get("kind") or "?"
            note_field = t.get("notes") or t.get("note") or ""
            text = (
                f"⚡ *{t['ticker']}* — `{kind}`\n"
                f"→ {t.get('action_hint') or '(sem hint)'}"
            )
            if note_field:
                text += f"\n_{note_field[:200]}_"
            buttons = [[
                {"text": "✅ Approve", "callback_data": f"act:approve:{action_id}"},
                {"text": "❌ Ignore",  "callback_data": f"act:ignore:{action_id}"},
                {"text": "🕒 Defer",   "callback_data": f"act:defer:{action_id}"},
            ]]
            r = telegram_send(text, inline_buttons=buttons)
            if r.get("ok"):
                ok_count += 1

        if len(triggers) > len(individual):
            extra = "\n".join(
                f"• {t['ticker']} [{t.get('kind','?')}] action {t.get('id')}"
                for t in triggers[len(individual):10]
            )
            telegram_send(
                f"⚡ +{len(triggers)-len(individual)} triggers extra "
                f"(usa `/actions list` para detalhes):\n{extra}"
            )
        return ok_count > 0

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

    # ── cron failure detection (2026-05-08) ───────────────────────────────

    def _cron_failures(self) -> list[dict]:
        """Query Windows Task Scheduler for ii-* tasks and the legacy
        investment-intelligence-daily. Returns list of failing tasks
        (LastTaskResult != 0). Skips tasks that ran successfully <24h ago.
        """
        ps_script = (
            "Get-ScheduledTask | Where-Object { "
            "$_.TaskName -match '^(investment-intelligence-daily|ii-)' "
            "} | ForEach-Object { "
            "$info = Get-ScheduledTaskInfo $_; "
            "[PSCustomObject]@{ "
            "Name = $_.TaskName; "
            "LastResult = $info.LastTaskResult; "
            "LastRun = $info.LastRunTime.ToString('o'); "
            "NextRun = $info.NextRunTime.ToString('o'); "
            "} } | ConvertTo-Json -Compress"
        )
        try:
            r = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True, text=True, timeout=15,
            )
            if r.returncode != 0 or not r.stdout.strip():
                return []
            import json
            data = json.loads(r.stdout)
            if isinstance(data, dict):
                data = [data]  # single-task case returns object not array
        except Exception:
            return []

        out = []
        now = datetime.now().astimezone()
        for task in data or []:
            last_result = task.get("LastResult")
            if last_result in (0, None):
                continue
            # Parse last run timestamp
            last_run_str = task.get("LastRun") or ""
            try:
                last_run = datetime.fromisoformat(last_run_str.replace("Z", "+00:00"))
                if last_run.tzinfo is None:
                    last_run = last_run.astimezone()
                age_hours = (now - last_run).total_seconds() / 3600
                last_run_date = last_run.date().isoformat()
            except Exception:
                age_hours = 999
                last_run_date = "unknown"
            out.append({
                "name": task["Name"],
                "last_result": last_result,
                "last_result_hex": f"0x{last_result & 0xFFFFFFFF:08X}",
                "last_run": last_run_str,
                "last_run_date": last_run_date,
                "age_hours": round(age_hours, 1),
            })
        return out

    def _push_cron_emergency(self, root: Path, task: dict) -> bool:
        """🚨 cron failure — louder than regular alerts."""
        msg = (
            f"🚨 *CRON FAILURE*\n\n"
            f"Task: `{task['name']}`\n"
            f"Last result: `{task['last_result_hex']}` (exit {task['last_result']})\n"
            f"Last run: {task['last_run']}  ({task['age_hours']}h ago)\n\n"
            f"Replay queued in HEARTBEAT.md. Run `python -m agents._heartbeat` to retry."
        )
        return self._telegram(root, msg)

    def _heartbeat_resume_entry(self, root: Path, task: dict) -> None:
        """Write a HEARTBEAT.md note so the next daily run is aware."""
        hb = root / "obsidian_vault" / "workspace" / "HEARTBEAT.md"
        if not hb.exists():
            return
        body = hb.read_text(encoding="utf-8")
        marker = f"<!-- cron failure {task['name']} {task['last_run_date']} -->"
        if marker in body:
            return
        # Map the failing task to its replay command
        replay_cmd = {
            "investment-intelligence-daily": "scripts\\daily_run.bat",
            "ii-hourly": "scripts\\hourly_run.bat",
            "ii-q4h": "scripts\\q4h_run.bat",
        }.get(task["name"], f"# manual replay for {task['name']}")
        new_line = (
            f"- [ ] >> {replay_cmd}  {marker} <!-- exit={task['last_result_hex']}, "
            f"age={task['age_hours']}h -->"
        )
        if "## Auto-injected (retry wrapper failures)" in body:
            body = body.replace(
                "## Auto-injected (retry wrapper failures)\n\n",
                f"## Auto-injected (retry wrapper failures)\n\n{new_line}\n",
                1,
            )
        else:
            body = body.rstrip() + (
                f"\n\n## Auto-injected (retry wrapper failures)\n\n{new_line}\n"
            )
        hb.write_text(body, encoding="utf-8")
