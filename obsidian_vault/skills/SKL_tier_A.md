---
type: skill_group
tier: A
status: backlog
sprints: [W.5, W.6]
tags: [skill, tier_a, research, agent_ops]
---

# 🥈 Tier A — High-value (avaliar sprint-a-sprint)

Skills que resolvem dores reais do projeto mas exigem design/evaluation antes de adoptar.

---

## 🔬 Research automation

### autoresearch (Karpathy)
**Repo**: https://github.com/karpathy/autoresearch
**Sprint**: W.5
**Fit**: potencial alto para `scripts/research.py --deep`.
**Dor resolve**: research memo hoje é template + call manual a Claude. Karpathy's autoresearch faz multi-step search + synthesis autonomamente.
**Decisão**: estudar antes de adoptar; pode ser overkill. Alternativa: GPT Researcher (abaixo).

### GPT Researcher
**Repo**: https://github.com/assafelovic/gpt-researcher
**Sprint**: W.5
**Fit**: 🎯 alto. Production-grade, LangChain-based, multi-agent research.
**Dor resolve**: mesma que autoresearch. Mais maduro, mais docs.
**Integração**: backend de `ii research X --deep`. Output = markdown memo.
**Watch-out**: OpenAI-first (LangChain); precisa trocar LLM backend para Anthropic Claude + Ollama local.

### Deep Research Skill (199-biotechnologies)
**Repo**: https://github.com/199-biotechnologies/... (URL truncada no video)
**Sprint**: W.5
**Fit**: similar a GPT Researcher mas skill-based (mais leve).
**Decisão**: se for Claude-native skill, preferir a GPT Researcher (menos stack). Validar URL primeiro.

**Recomendação Sprint W.5**: A/B test real — pegar 1 ticker (ex: TFC), gerar memo com:
1. `scripts/research.py` actual
2. GPT Researcher (trocando LLM para Claude)
3. Deep Research skill

Escolher o que dá melhor memo para o mesmo custo.

---

## 🧪 Agent ops

### promptfoo
**Repo**: https://github.com/promptfoo/promptfoo
**Sprint**: W.6
**Fit**: 🎯 altíssimo para `agents/` framework (Phase V).
**Dor resolve**: não temos testes dos 12 agents. Um prompt-change no `meta_agent` pode quebrar `risk_auditor` silenciosamente.
**Entregável**: `tests/prompts/` com suite promptfoo:
- `risk_auditor` — 10 prompts típicos + expected outputs
- `devils_advocate` — 10 contrarian prompts
- `meta_agent` — orchestration prompts
- Rodar em pre-commit hook ou CI local
**Custo**: free (open source), mas cada run gasta tokens. Cap com cheap model (Haiku) para smoke tests.

### Task Master AI MCP
**Repo**: https://github.com/eyaltoledano/claude-task-master
**Sprint**: W.6
**Fit**: médio. Já temos TaskCreate built-in em Claude Code.
**Dor resolve**: tracking roadmap Phase W → Phase X. Task Master gerencia tasks cross-session (não apenas current).
**Decisão**: **adoptar só se** TaskCreate native não for suficiente para roadmap multi-sprint. Começar sem.
**Alternativa**: Roadmap.md actual (plain markdown) + checkboxes.

### Context7
**Repo**: https://github.com/upstash/context7
**Sprint**: W.6
**Fit**: alto. Docs lookup on-demand.
**Dor resolve**: quando tocamos `pypdf`, `openpyxl`, `playwright`, `yfinance`, Claude às vezes usa API outdated. Context7 resolve com docs fresh.
**Entregável**: adicionar MCP em `.claude/mcp.json`.
**Custo**: free tier generoso.

### Codebase Memory MCP
**Repo**: https://github.com/DeusData/codebase-... (URL truncada)
**Sprint**: W.6
**Fit**: alto. Nosso codebase tem 100+ scripts; Claude re-explora cada session.
**Dor resolve**: "onde está a lógica de damper no drip_projection?" — hoje grep manual.
**Decisão**: testar. Se funciona melhor que Grep nativo + CLAUDE.md catalogue, adoptar.
**Watch-out**: duplica CLAUDE.md script catalog. Ver qual é fonte canónica.

---

## 📊 Resumo Tier A

| Skill | Sprint | Adopt? | Racional |
|---|---|---|---|
| GPT Researcher | W.5 | Provável | Mais maduro que alternativas |
| autoresearch | W.5 | Avaliar | Karpathy é referência mas novo |
| Deep Research skill | W.5 | Avaliar | URL a confirmar |
| promptfoo | W.6 | **Sim** | Dor clara (testes agents) |
| Task Master MCP | W.6 | Improvável | TaskCreate native cobre |
| Context7 | W.6 | **Sim** | Custo zero + benefício claro |
| Codebase Memory | W.6 | Testar | Se beat Grep + CLAUDE.md |
