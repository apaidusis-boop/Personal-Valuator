"""{{AGENT_CLASS}} — {{DESCRIPTION}}.

Gerado por `ii agents create {{AGENT_NAME}}`.

Edit este ficheiro para implementar a lógica em `execute_impl()`.
"""
from __future__ import annotations

from agents._base import AgentContext, AgentResult, BaseAgent
from agents._llm import llm_summarise


class {{AGENT_CLASS}}(BaseAgent):
    name = "{{AGENT_NAME}}"
    description = "{{DESCRIPTION}}"
    default_schedule = "{{SCHEDULE}}"

    def execute_impl(self, ctx: AgentContext) -> AgentResult:
        actions: list[str] = []
        errors: list[str] = []

        # TODO: implementar lógica do agent
        # Exemplos:
        #   - sqlite queries: sqlite3.connect(ctx.root / "data" / "br_investments.db")
        #   - subprocess scripts: subprocess.run([...])
        #   - LLM synthesis: llm_summarise(prompt, system=...)
        #   - write vault: (ctx.root / "obsidian_vault" / "...").write_text(...)

        summary = "TODO: implement summary"

        return AgentResult(
            agent=self.name,
            status="no_action",
            summary=summary,
            started_at="", finished_at="", duration_sec=0,
            actions=actions,
            errors=errors,
        )
