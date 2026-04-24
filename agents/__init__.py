"""agents — autonomy framework.

Cada agent é uma classe que herda de `BaseAgent` e implementa `execute()`.
Agents são declarados em `config/agents.yaml`, executados via
`scripts/agents_cli.py` (manual) ou `scripts/agent_runner.py` (cron).

Ver `obsidian_vault/wiki/playbooks/Agents_layer.md` para arquitectura.
"""
from ._base import BaseAgent, AgentResult, AgentContext
from ._state import AgentState
from ._llm import llm_summarise, LLMBudget

__all__ = [
    "BaseAgent", "AgentResult", "AgentContext",
    "AgentState", "llm_summarise", "LLMBudget",
]
