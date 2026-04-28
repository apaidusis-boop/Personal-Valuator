"""Thin wrapper para notifiers.telegram com convenções dos agents.

Cada agent chama `push(...)` e o helper resolve:
  - persona automática a partir do agent name (via _personas.load_all)
  - route default a partir do department
  - thread_id opcional para Forum Topics

Por que um wrapper:
  - DRY — todos agents formatam signature consistente
  - Fácil mudar route mapping num sítio
  - Fallback gracioso se .env não tem route específica
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# Default route por department. User pode override no .env adicionando
# TELEGRAM_CHAT_ID_<ROUTE> + TELEGRAM_THREAD_<ROUTE> específicos.
DEPARTMENT_ROUTE = {
    "Operations": "ops",
    "Research": "research",
    "Risk": "risk",
    "Compliance": "compliance",
    "Performance": "performance",
    "Desk": "main",
}


def push(
    text: str,
    *,
    agent_name: str | None = None,
    route: str | None = None,
    silent: bool = False,
) -> dict:
    """Envia mensagem via Telegram com persona + route automáticos.

    Args:
        text: corpo da mensagem
        agent_name: slug do agent (ex: 'morning_briefing'); usado para
                    persona signature + route default
        route: override do route (opcional)
        silent: sem notification sound
    """
    # Auto-resolve route se não especificado
    if route is None and agent_name:
        try:
            from agents._personas import get as get_persona
            p = get_persona(agent_name)
            if p:
                route = DEPARTMENT_ROUTE.get(p.department, "main")
        except Exception:
            pass

    from notifiers.telegram import send
    return send(text, silent=silent, persona=agent_name, route=route)


def push_founder_alert(text: str, agent_name: str | None = None) -> dict:
    """Mensagem directa ao founder (route='main'), não num topic especializado.
    Usado para alerts críticos que devem aparecer no chat principal."""
    return push(text, agent_name=agent_name, route="main")
