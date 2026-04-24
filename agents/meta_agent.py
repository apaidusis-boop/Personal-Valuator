"""MetaAgent — compliance officer. Audita os outros agents.

Responsabilidades:
  1. Detecta agents com N failures consecutivos → auto-disable via agents.yaml
  2. Detecta "zombie agents" — não correram em 2× o schedule interval
  3. Escreve dashboard de saúde em obsidian_vault/agents/_dashboard.md
  4. Se cohort está >50% non-ok → alerta founder via Telegram

Nota crítica: MetaAgent NUNCA se auto-audita (evita paradoxos). Se o próprio
MetaAgent falha consecutivamente, isso vai aparecer no state file mas ninguém
o vai desabilitar. Failsafe: healthcheck humano via `ii agents status`.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

from ._base import AgentContext, AgentResult, BaseAgent


class MetaAgent(BaseAgent):
    name = "meta_agent"
    description = "Audita outros agents: auto-disable failures + zombie detection + dashboard"
    default_schedule = "daily:23:00"

    FAILURE_THRESHOLD = 3
    UNHEALTHY_FRACTION_ALERT = 0.50
    ZOMBIE_MULTIPLIER = 2  # agent zombie se passa 2× seu schedule sem correr

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        root = ctx.root
        actions: list[str] = []
        data_dir = root / "data" / "agents"
        if not data_dir.exists():
            return AgentResult(
                agent=self.name, status="no_action",
                summary="Nenhum data/agents/ directory.",
                started_at="", finished_at="", duration_sec=0,
            )

        # 1. Load todos os state files
        cohort = []
        for state_file in sorted(data_dir.glob("*.json")):
            if state_file.name.startswith("_"):
                continue  # skip _llm_budget.json etc
            try:
                state = json.loads(state_file.read_text(encoding="utf-8"))
            except Exception:
                continue
            agent_name = state.get("agent") or state_file.stem
            if agent_name == self.name:
                continue  # no self-audit

            cohort.append({
                "name": agent_name,
                "run_count": state.get("run_count", 0),
                "last_run": state.get("last_run"),
                "last_status": state.get("last_status"),
                "last_error": state.get("last_error"),
                "failed_count": state.get("failed_count", 0),
                "consecutive_failures": state.get("consecutive_failures", 0),
            })

        if not cohort:
            return AgentResult(
                agent=self.name, status="no_action",
                summary="Nenhum agent state para auditar.",
                started_at="", finished_at="", duration_sec=0,
            )

        # 2. Determine health per agent
        schedule_map = self._load_schedule_map(root)
        disabled: list[str] = []
        zombies: list[str] = []
        for ag in cohort:
            schedule = schedule_map.get(ag["name"], "manual")
            ag["schedule"] = schedule

            # Auto-disable se consecutive failures acima threshold
            if ag["consecutive_failures"] >= self.FAILURE_THRESHOLD:
                if not ctx.dry_run and self._disable_in_yaml(root, ag["name"]):
                    disabled.append(ag["name"])
                    actions.append(
                        f"disabled {ag['name']} ({ag['consecutive_failures']} consecutive failures)"
                    )
                ag["health"] = "disabled"
                continue

            # Zombie check
            if self._is_zombie(ag["last_run"], schedule):
                zombies.append(ag["name"])
                ag["health"] = "zombie"
                continue

            # Determine from last_status
            if ag["last_status"] == "failed":
                ag["health"] = "degraded"
            elif ag["last_status"] in ("ok", "no_action"):
                ag["health"] = "ok"
            elif ag["last_status"] is None:
                ag["health"] = "never_ran"
            else:
                ag["health"] = "unknown"

        # 3. Cohort health summary
        unhealthy = [a for a in cohort if a["health"] not in ("ok", "never_ran")]
        unhealthy_pct = len(unhealthy) / len(cohort) if cohort else 0

        # 4. Write dashboard
        if not ctx.dry_run:
            self._write_dashboard(root, cohort)

        # 5. Telegram alert se cohort >=50% unhealthy
        alerted = False
        if unhealthy_pct >= self.UNHEALTHY_FRACTION_ALERT and not ctx.dry_run:
            alerted = self._telegram_alert(root, cohort, unhealthy)
            if alerted:
                actions.append(f"founder alert (cohort {unhealthy_pct*100:.0f}% unhealthy)")

        summary = (
            f"{len(cohort)} agents auditados — {len(unhealthy)} unhealthy "
            f"({len(disabled)} auto-disabled, {len(zombies)} zombies). "
            f"Cohort health: {(1-unhealthy_pct)*100:.0f}%."
        )

        return AgentResult(
            agent=self.name, status="ok",
            summary=summary,
            started_at="", finished_at="", duration_sec=0,
            actions=actions,
            data={
                "cohort": cohort,
                "unhealthy_pct": round(unhealthy_pct, 3),
                "disabled": disabled,
                "zombies": zombies,
                "alerted": alerted,
            },
        )

    # ─── Helpers ──────────────────────────────────────────────────────────

    def _load_schedule_map(self, root: Path) -> dict[str, str]:
        out: dict[str, str] = {}
        if not _HAS_YAML:
            return out
        yaml_path = root / "config" / "agents.yaml"
        if not yaml_path.exists():
            return out
        try:
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
            for entry in data.get("agents", []):
                out[entry["name"]] = entry.get("schedule", "manual")
        except Exception:
            pass
        return out

    def _is_zombie(self, last_run: str | None, schedule: str) -> bool:
        if not last_run or not schedule or schedule == "manual":
            return False
        try:
            last_dt = datetime.fromisoformat(last_run)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
        except Exception:
            return False
        elapsed = (datetime.now(timezone.utc) - last_dt).total_seconds()

        # Interval based on schedule
        if m := re.match(r"^daily:", schedule):
            interval_sec = 86400
        elif m := re.match(r"^every:(\d+)m", schedule):
            interval_sec = int(m.group(1)) * 60
        elif m := re.match(r"^every:(\d+)h", schedule):
            interval_sec = int(m.group(1)) * 3600
        elif m := re.match(r"^weekly:", schedule):
            interval_sec = 86400 * 7
        else:
            return False

        return elapsed > (interval_sec * self.ZOMBIE_MULTIPLIER)

    def _disable_in_yaml(self, root: Path, agent_name: str) -> bool:
        if not _HAS_YAML:
            return False
        yaml_path = root / "config" / "agents.yaml"
        if not yaml_path.exists():
            return False
        try:
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
            for entry in data.get("agents", []):
                if entry["name"] == agent_name:
                    if not entry.get("enabled", True):
                        return False  # already disabled
                    entry["enabled"] = False
                    yaml_path.write_text(
                        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
                        encoding="utf-8",
                    )
                    return True
        except Exception:
            pass
        return False

    def _write_dashboard(self, root: Path, cohort: list[dict]) -> None:
        vault = Path(root / "obsidian_vault")
        agents_dir = vault / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        path = agents_dir / "_dashboard.md"

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        health_icons = {
            "ok": "✅", "degraded": "⚠️", "disabled": "🚫",
            "zombie": "💤", "never_ran": "·", "unknown": "?",
        }
        ok_count = sum(1 for a in cohort if a["health"] == "ok")

        lines = [
            "---",
            "type: agent_dashboard",
            f"updated: {now}",
            "tags: [agent, dashboard, meta]",
            "---",
            "",
            f"# 🏢 Agents Dashboard",
            "",
            f"_Last audit: {now} (by meta_agent)_",
            "",
            f"**Cohort health**: {ok_count}/{len(cohort)} ok "
            f"({ok_count/max(len(cohort),1)*100:.0f}%)",
            "",
            "## Roster",
            "",
            "| Agent | Health | Schedule | Last Run | Runs | Failed | Consec. |",
            "|---|---|---|---|---|---|---|",
        ]
        for a in sorted(cohort, key=lambda x: (x["health"] != "ok", x["name"])):
            icon = health_icons.get(a["health"], "?")
            last = (a["last_run"] or "")[:16] or "(never)"
            lines.append(
                f"| [[agents/{a['name']}\\|{a['name']}]] | {icon} {a['health']} | "
                f"`{a['schedule']}` | {last} | {a['run_count']} | "
                f"{a['failed_count']} | {a['consecutive_failures']} |"
            )

        # Errors section
        errors = [a for a in cohort if a.get("last_error")]
        if errors:
            lines += ["", "## Recent errors", ""]
            for a in errors[:10]:
                lines.append(f"- **{a['name']}**: `{(a['last_error'] or '')[:200]}`")

        lines += [
            "",
            "## Meta-agent policy",
            "",
            f"- Auto-disable after **{self.FAILURE_THRESHOLD} consecutive failures**",
            f"- Zombie detection: **{self.ZOMBIE_MULTIPLIER}×** schedule interval sem run",
            f"- Founder alert: **≥{int(self.UNHEALTHY_FRACTION_ALERT*100)}%** cohort unhealthy",
            "",
            "## Actions available",
            "",
            "```bash",
            "ii agents status             # CLI detalhado",
            "ii agents enable <name>      # re-enable após fix",
            "ii agents logs <name>        # investigar failure",
            "ii agents run <name>         # manual retry",
            "```",
        ]
        path.write_text("\n".join(lines), encoding="utf-8")

    def _telegram_alert(self, root: Path, cohort: list, unhealthy: list) -> bool:
        msg_lines = [
            f"🏢 MetaAgent alert — {len(unhealthy)}/{len(cohort)} agents não-ok",
            "",
        ]
        for a in unhealthy[:8]:
            msg_lines.append(f"• {a['name']}: {a['health']} ({a.get('last_error', '')[:80]})")
        msg_lines.append("")
        msg_lines.append("Check: ii agents status")
        try:
            r = subprocess.run(
                [sys.executable, "-X", "utf8", "-m", "notifiers.telegram",
                 "\n".join(msg_lines)],
                capture_output=True, timeout=20, cwd=str(root),
            )
            return r.returncode == 0
        except Exception:
            return False
