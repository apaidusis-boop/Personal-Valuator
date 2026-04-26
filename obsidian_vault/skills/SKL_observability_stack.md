---
type: skill_group
tier: Gold
skill_name: observability-stack
status: backlog
sprint: W.6
tags: [skill, gold, observability, langfuse, dspy, instructor, agent_ops]
---

# 🔭 Observability Stack — Gold extras

Para ir para Gold, agents precisam de **observability real**, não prints. Estas são ferramentas Claude não mencionou mas essenciais para profissionalização.

## 1. LangFuse — Agent observability 📊
**Repo**: https://github.com/langfuse/langfuse
**Self-host**: sim (Docker)
**O que faz**: traces, eval, metrics para LLM apps. Cada chamada (Claude, Ollama, agent) é traced — vemos latency, tokens, cost, output quality.

**Onde integra**:
- Wrap todos os calls em `agents/_llm.py` com LangFuse decorator
- Dashboard LangFuse local (http://localhost:3000) com:
  - Cost-per-agent (breakdown Claude vs Ollama)
  - Latency por tipo de task
  - Eval scores (regression detection se output piora)
  - Session replay (debug "por que meta_agent disse X?")

**Self-host**:
```bash
git clone https://github.com/langfuse/langfuse
cd langfuse && docker-compose up -d
```

**Integração com perpetuum validator**: cada decisão do validator é tracked. Weekly review inclui "latency avg: 3.2s, cost total: $0.42".

## 2. DSPy — Prompt Optimization 🧠
**Repo**: https://github.com/stanfordnlp/dspy (Stanford)
**O que faz**: framework para **auto-optimizar prompts** por examples. Em vez de tuning manual, DSPy aprende o best prompt por optimization.

**Onde integra**:
- Os 12 agents do Phase V têm prompts hand-written. DSPy pode optimizá-los:
  - Dar 20 exemplos de "risk_auditor input → expected output"
  - DSPy gera variants + avalia + converge em best prompt
  - Ganho médio observado em benchmarks: 15-30% em quality score
- Sinergia com **promptfoo** (W.6) — promptfoo é test suite; DSPy é optimizer

**Sprint W.6**:
- [ ] Piloto DSPy em `risk_auditor` (agent mais crítico)
- [ ] Benchmark quality score pré vs pós-optimization
- [ ] Se ganho >15%, expandir para outros 11 agents

## 3. Instructor — Structured Outputs 🎯
**Repo**: https://github.com/jxnl/instructor
**O que faz**: força outputs JSON structured de LLMs via Pydantic models. Elimina parsing frágil.

**Onde integra**:
- `agents/_base.py` usa parsing manual de JSON do Ollama/Claude. Frágil.
- Instructor + Pydantic → schema estrito, validation automática, retry on malformed
- Ganho: **zero parsing errors** → mais stable agent framework

**Exemplo**:
```python
from instructor import from_anthropic
from pydantic import BaseModel

class RiskAuditOutput(BaseModel):
    ticker: str
    overall_risk: Literal["low", "medium", "high"]
    flags: list[str]
    recommendation: str

client = from_anthropic(anthropic.Anthropic())
result: RiskAuditOutput = client.messages.create(
    model="claude-opus-4-7",
    response_model=RiskAuditOutput,
    messages=[...]
)
# result é garantidamente validado — zero try/except
```

**Sprint W.6**:
- [ ] Adicionar Instructor ao `agents/_base.py`
- [ ] Definir Pydantic output schema para cada um dos 12 agents
- [ ] Migrar 1 agent piloto (`risk_auditor`)

## 4. LlamaIndex — RAG framework (opcional) 📚
**Repo**: https://github.com/run-llama/llama_index
**O que faz**: RAG (retrieval-augmented generation) framework.

**Onde integra (potencial)**:
- **Vault RAG**: índice sobre os 53 wiki + 35 ticker notes + briefings. User pergunta "o que disse sobre ITSA4 em janeiro?" → resposta exacta com fonte.
- **Subscription RAG**: índice sobre todos os `analyst_reports` ingeridos → "quais analistas disseram BUY em VALE3 nos últimos 90d?"
- Hoje temos Qwen semantic search (`ii vault "pergunta"`) — LlamaIndex pode ser upgrade com retrieval mais sofisticado.

**Decisão**: adicionar só se Qwen native search começar a ficar aquém. Baseline primeiro.

## 5. Agent Protocols

Além destas, **considerar**:
- **Pydantic AI** — https://github.com/pydantic/pydantic-ai — alternativa a Instructor, mais recente, Pydantic team
- **Guardrails AI** — https://github.com/guardrails-ai/guardrails — validação de LLM outputs
- **Semantic Kernel** (Microsoft) — agent framework enterprise

## Sprint W.6 consolidado

Ordem recomendada:
1. **Instructor** primeiro — menor effort, ganho em stability imediato
2. **LangFuse self-host** — dá visibility antes de otimizar
3. **promptfoo** test suite — baseline quality antes de optimizar
4. **DSPy optimization** — só depois de ter baseline + visibility

## Blockers
- LangFuse precisa Docker
- DSPy tem learning curve (mas bom tutorial)
