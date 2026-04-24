"""Persona lookup — extrai metadata humana de cada agent do agents.yaml.

Usado por:
  - BaseAgent para saber employee_name/title/department
  - Obsidian org chart generator
  - Telegram controller (formata mensagens com nome do funcionário)
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Persona:
    agent_name: str
    employee_name: str
    title: str
    bio: str
    department: str
    reports_to: str
    schedule: str


@lru_cache(maxsize=1)
def load_all() -> dict[str, Persona]:
    """Lê config/agents.yaml e devolve {agent_name: Persona}."""
    if not _HAS_YAML:
        return {}
    path = ROOT / "config" / "agents.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: dict[str, Persona] = {}
    for e in data.get("agents", []):
        out[e["name"]] = Persona(
            agent_name=e["name"],
            employee_name=e.get("employee_name", e["name"]),
            title=e.get("title", "Agent"),
            bio=e.get("bio", ""),
            department=e.get("department", "Operations"),
            reports_to=e.get("reports_to", "founder"),
            schedule=e.get("schedule", "manual"),
        )
    return out


def get(agent_name: str) -> Persona | None:
    return load_all().get(agent_name)


def by_department() -> dict[str, list[Persona]]:
    """Group personas by department."""
    out: dict[str, list[Persona]] = {}
    for p in load_all().values():
        out.setdefault(p.department, []).append(p)
    return out


def format_signature(agent_name: str) -> str:
    """'Valentina Prudente — Chief Risk Officer' — usado em alerts/briefings."""
    p = get(agent_name)
    if not p:
        return agent_name
    return f"{p.employee_name} — {p.title}"
