"""Runner — decide qual agent deve correr agora (schedule match) + execute.

Schedule formats:
  - "manual"               — nunca corre auto (só via ii agent run)
  - "daily:HH:MM"          — uma vez ao dia na hora indicada
  - "every:Nm" / "every:Nh"— a cada N minutos/horas
  - "weekly:DOW:HH:MM"     — DOW em mon|tue|wed|thu|fri|sat|sun

Usado por scripts/agent_runner.py (cron every minute).
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

from ._base import AgentContext, AgentResult, BaseAgent
from ._registry import AgentRegistration, list_agents, find_registration, instantiate
from ._state import AgentState


_DOW_MAP = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}


def _schedule_due(schedule: str, state: AgentState, now: datetime) -> bool:
    """Returns True if schedule says 'should run now'."""
    if not schedule or schedule == "manual":
        return False
    last_run = state.last_run_dt()

    # daily:HH:MM
    m = re.match(r"^daily:(\d{1,2}):(\d{2})$", schedule)
    if m:
        hh, mm = int(m.group(1)), int(m.group(2))
        local_now = now.astimezone()
        if local_now.hour < hh or (local_now.hour == hh and local_now.minute < mm):
            return False
        if last_run and last_run.astimezone().date() == local_now.date():
            return False
        return True

    # every:Nm / every:Nh
    m = re.match(r"^every:(\d+)([mh])$", schedule)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        minutes = n if unit == "m" else n * 60
        if not last_run:
            return True
        elapsed_min = (now - last_run.astimezone(timezone.utc)).total_seconds() / 60
        return elapsed_min >= minutes

    # weekly:DOW:HH:MM
    m = re.match(r"^weekly:([a-z]{3}):(\d{1,2}):(\d{2})$", schedule)
    if m:
        dow = _DOW_MAP.get(m.group(1))
        hh, mm = int(m.group(2)), int(m.group(3))
        if dow is None:
            return False
        local_now = now.astimezone()
        if local_now.weekday() != dow:
            return False
        if local_now.hour < hh or (local_now.hour == hh and local_now.minute < mm):
            return False
        if last_run and last_run.astimezone().date() == local_now.date():
            return False
        return True

    return False


def run_one(reg: AgentRegistration, agent: BaseAgent, root, dry_run: bool = False, reason: str = "manual") -> AgentResult:
    ctx = AgentContext(root=root, config=reg.config, dry_run=dry_run, reason=reason)
    state = AgentState(reg.name, root=root)
    result = agent.execute(ctx)
    state.record_run(result.status, error=" | ".join(result.errors) if result.errors else None)
    # Write status to vault
    try:
        import os
        vault = os.environ.get("OBSIDIAN_VAULT_PATH") or str(root / "obsidian_vault")
        from pathlib import Path as _P
        status_dir = _P(vault) / "agents"
        status_dir.mkdir(parents=True, exist_ok=True)
        status_md = agent.render_status_md(result, state.as_dict())
        (status_dir / f"{reg.name}.md").write_text(status_md, encoding="utf-8")
    except Exception:
        pass
    return result


def run_all_due(root, dry_run: bool = False) -> list[AgentResult]:
    """Executa todos os agents cujo schedule está due. Main entry para cron."""
    now = datetime.now(timezone.utc)
    results = []
    for reg, agent in list_agents():
        if not reg.enabled or agent is None:
            continue
        state = AgentState(reg.name, root=root)
        if not _schedule_due(reg.schedule, state, now):
            continue
        print(f"[runner] running {reg.name} (schedule={reg.schedule})")
        r = run_one(reg, agent, root, dry_run=dry_run, reason="scheduled")
        print(f"[runner] {reg.name} → {r.status} ({r.duration_sec:.1f}s)")
        results.append(r)
    return results


def run_by_name(name: str, root, dry_run: bool = False) -> AgentResult | None:
    reg = find_registration(name)
    if not reg:
        return None
    try:
        agent = instantiate(reg)
    except Exception as e:
        return AgentResult(
            agent=name, status="failed",
            summary=f"failed to instantiate: {e}",
            started_at="", finished_at="", duration_sec=0,
            errors=[str(e)],
        )
    return run_one(reg, agent, root, dry_run=dry_run, reason="manual")
