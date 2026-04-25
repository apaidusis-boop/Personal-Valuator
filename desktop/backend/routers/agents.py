"""agents — /api/agents/list, /api/agents/run/{name}."""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

ROOT = Path(__file__).resolve().parents[3]

router = APIRouter()


@router.get("/agents/list")
def agents_list() -> list[dict]:
    """Returns registered agents from config/agents.yaml."""
    try:
        from agents._registry import load_registrations  # type: ignore
    except Exception as e:
        raise HTTPException(500, f"registry import failed: {e}")
    regs = load_registrations()
    return [
        {"name": r.name, "description": r.description,
         "schedule": r.schedule, "enabled": r.enabled}
        for r in regs
    ]


@router.post("/agents/run/{name}")
def agents_run(name: str, dry_run: bool = False) -> dict:
    """Trigger an agent on-demand. Returns result summary."""
    try:
        from agents._registry import find_registration, instantiate
        from agents._base import AgentContext
    except Exception as e:
        raise HTTPException(500, f"registry import failed: {e}")
    reg = find_registration(name)
    if not reg:
        raise HTTPException(404, f"agent {name!r} not found")
    agent = instantiate(reg)
    ctx = AgentContext(root=ROOT, config={}, dry_run=dry_run, reason="manual")
    result = agent.execute(ctx)
    return {
        "agent": result.agent,
        "status": result.status,
        "summary": result.summary,
        "duration_sec": result.duration_sec,
        "actions": result.actions,
        "errors": result.errors,
    }
