"""BaseAgent — contrato comum para todos os agentes.

Agents são instanciados por `_registry.load_agent()` com config vinda de
`config/agents.yaml`. Cada agent:
  - `name` — slug único
  - `schedule` — cron-style OR simple interval (e.g. "daily:07:00", "every:15m")
  - `execute(ctx)` — trabalho real, devolve AgentResult
  - `state` — persistido em data/agents/<name>.json

Design principles:
  - Idempotent — mesma run repetida = sem efeitos duplicados
  - Fail-soft — errors são logged + reported, não crash
  - Observable — cada run escreve summary para obsidian_vault/agents/<name>_status.md
  - Token-aware — usa Ollama por default; Claude só via escalation explícito
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class AgentResult:
    """Output de uma execução de agent."""
    agent: str
    status: str            # 'ok' | 'no_action' | 'failed' | 'skipped'
    summary: str           # 1-3 linhas humano-legível
    started_at: str        # ISO UTC
    finished_at: str       # ISO UTC
    duration_sec: float
    data: dict = field(default_factory=dict)  # agent-specific payload
    errors: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)  # lista de efeitos (p.ex. "fetched 5 reports")


@dataclass
class AgentContext:
    """Ambiente passado ao execute()."""
    root: Path
    config: dict
    dry_run: bool = False
    reason: str = "scheduled"   # 'scheduled' | 'manual' | 'triggered_by:<other>'


class BaseAgent(ABC):
    """Contrato comum. Subclasses implementam execute()."""
    name: str = ""
    description: str = ""
    default_schedule: str = "manual"   # 'manual' | 'daily:HH:MM' | 'every:Nm' | 'weekly:DOW:HH:MM'
    write_daily_log: bool = True       # append run summary to obsidian_vault/daily_logs/<name>/YYYY-MM-DD.md

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def execute(self, ctx: AgentContext) -> AgentResult:
        """Wrap execute_impl with timing + catch-all error handling."""
        start = datetime.now(timezone.utc)
        start_iso = start.isoformat(timespec="seconds")
        try:
            result = self.execute_impl(ctx)
            finish = datetime.now(timezone.utc)
            result.started_at = start_iso
            result.finished_at = finish.isoformat(timespec="seconds")
            result.duration_sec = (finish - start).total_seconds()
            result.agent = self.name
        except Exception as e:
            finish = datetime.now(timezone.utc)
            result = AgentResult(
                agent=self.name,
                status="failed",
                summary=f"{type(e).__name__}: {e}",
                started_at=start_iso,
                finished_at=finish.isoformat(timespec="seconds"),
                duration_sec=(finish - start).total_seconds(),
                errors=[f"{type(e).__name__}: {e}"],
            )
        if self.write_daily_log and not getattr(ctx, "dry_run", False):
            try:
                self._append_daily_log(ctx, result)
            except Exception:
                pass  # daily-log failure must not break agent run
        return result

    def _append_daily_log(self, ctx: AgentContext, result: AgentResult) -> None:
        """Append one run entry to obsidian_vault/daily_logs/<name>/YYYY-MM-DD.md.

        Format: append-only, append new section per run. Markdown.
        OpenClaw pattern (memory/YYYY-MM-DD.md analogue, scoped per-agent).
        """
        if not self.name:
            return
        root = getattr(ctx, "root", None) or Path.cwd()
        day = result.finished_at[:10] if result.finished_at else datetime.now(timezone.utc).date().isoformat()
        log_dir = Path(root) / "obsidian_vault" / "daily_logs" / self.name
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f"{day}.md"
        new_file = not log_path.exists()
        icon = {"ok": "✅", "no_action": "·", "failed": "❌", "skipped": "⏭"}.get(result.status, "?")
        lines: list[str] = []
        if new_file:
            lines += [
                "---",
                f"type: agent_daily_log",
                f"agent: {self.name}",
                f"date: {day}",
                "---",
                "",
                f"# {self.name} — {day}",
                "",
            ]
        lines += [
            f"## {icon} {result.finished_at} ({result.duration_sec:.2f}s) — {result.status}",
            "",
            result.summary or "_(no summary)_",
            "",
        ]
        if result.actions:
            lines.append("**Actions:**")
            for a in result.actions[:10]:
                lines.append(f"- {a}")
            if len(result.actions) > 10:
                lines.append(f"- _(+{len(result.actions) - 10} more)_")
            lines.append("")
        if result.errors:
            lines.append("**Errors:**")
            for e in result.errors[:5]:
                lines.append(f"- ❌ {e}")
            lines.append("")
        with log_path.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    @abstractmethod
    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        """Subclass implements this. Deve devolver AgentResult com status + summary."""
        raise NotImplementedError

    def render_status_md(self, result: AgentResult, state: dict) -> str:
        """Markdown para obsidian_vault/agents/<name>_status.md.
        Override para formato custom."""
        icon = {"ok": "✅", "no_action": "·", "failed": "❌", "skipped": "⏭"}.get(result.status, "?")
        lines = [
            "---",
            f"type: agent_status",
            f"agent: {self.name}",
            f"status: {result.status}",
            f"last_run: {result.finished_at}",
            f"duration_sec: {result.duration_sec:.2f}",
            "tags: [agent, status]",
            "---",
            "",
            f"# {icon} Agent: {self.name}",
            "",
            f"**Description**: {self.description}",
            f"**Schedule**: {self.default_schedule}",
            f"**Last run**: {result.finished_at}  ({result.duration_sec:.1f}s)",
            f"**Status**: `{result.status}`",
            "",
            "## Last summary",
            "",
            result.summary,
            "",
        ]
        if result.actions:
            lines.append("## Actions taken")
            for a in result.actions:
                lines.append(f"- {a}")
            lines.append("")
        if result.errors:
            lines.append("## Errors")
            for e in result.errors:
                lines.append(f"- ❌ {e}")
            lines.append("")
        run_count = state.get("run_count", 0)
        failed_count = state.get("failed_count", 0)
        lines += [
            "## Lifetime stats",
            f"- Runs: {run_count}",
            f"- Failed: {failed_count}",
            f"- Last error: {state.get('last_error', 'none')}",
        ]
        return "\n".join(lines)
