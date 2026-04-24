"""Registry — descobre + instancia agentes a partir de config/agents.yaml.

Cada entry em agents.yaml:
    - name: morning_briefing
      class: agents.morning_briefing:MorningBriefingAgent
      enabled: true
      schedule: "daily:07:00"
      config: {...}
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

from ._base import BaseAgent

ROOT = Path(__file__).resolve().parents[1]
AGENTS_YAML = ROOT / "config" / "agents.yaml"


@dataclass
class AgentRegistration:
    name: str
    class_path: str
    enabled: bool
    schedule: str
    config: dict
    description: str = ""


def load_registrations() -> list[AgentRegistration]:
    """Lê config/agents.yaml e devolve lista de registrations."""
    if not _HAS_YAML:
        raise RuntimeError("pyyaml required — pip install pyyaml")
    if not AGENTS_YAML.exists():
        return []
    with AGENTS_YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    out = []
    for entry in data.get("agents", []):
        out.append(AgentRegistration(
            name=entry["name"],
            class_path=entry["class"],
            enabled=bool(entry.get("enabled", True)),
            schedule=entry.get("schedule", "manual"),
            config=entry.get("config", {}) or {},
            description=entry.get("description", ""),
        ))
    return out


def find_registration(name: str) -> AgentRegistration | None:
    for r in load_registrations():
        if r.name == name:
            return r
    return None


def instantiate(reg: AgentRegistration) -> BaseAgent:
    """Carrega classe via dotted path + instancia com config."""
    module_path, class_name = reg.class_path.split(":")
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    agent: BaseAgent = cls(config=reg.config)
    if not agent.name:
        agent.name = reg.name
    if not agent.description:
        agent.description = reg.description
    agent.default_schedule = reg.schedule
    return agent


def list_agents() -> list[tuple[AgentRegistration, BaseAgent | None]]:
    """Lista registrations com instance (ou None se falhou carregar)."""
    out = []
    for reg in load_registrations():
        try:
            agent = instantiate(reg)
        except Exception:
            agent = None
        out.append((reg, agent))
    return out
