---
type: playbook
name: Agents layer — autonomy framework
tags: [playbook, agents, autonomy, meta]
related: ["[[Token_discipline]]", "[[Analysis_workflow]]", "[[Web_scraping_subscriptions]]"]
---

# 🤖 Agents Layer — autonomy framework

> Sistema de agentes autónomos que trabalham em cron + event-driven, respeitando REGRA #1 [[Token_discipline]] (Ollama 95%, Claude só via budget-cap escalation).

## Arquitectura

```
config/agents.yaml    ←  declarative registry (enable/schedule/config)
       │
       ▼
agents/                 ←  Python package
   ├─ _base.py          BaseAgent abstract + AgentResult + AgentContext
   ├─ _state.py         JSON state per agent (data/agents/<name>.json)
   ├─ _registry.py      carrega + instancia a partir de yaml
   ├─ _runner.py        decide schedule match + execute
   ├─ _llm.py           Ollama default + Claude escalation w/ budget
   ├─ templates/        para `ii agents create <name>`
   │  └─ periodic.py.tpl
   ├─ morning_briefing.py    ← 4 production agents
   ├─ watchdog.py
   ├─ thesis_refresh.py
   └─ subscription_fetch.py

scripts/
   ├─ agents_cli.py     CLI principal — `ii agents <cmd>`
   └─ agent_runner.py   cron entry every minute → run_all_due()
```

## Production agents

| Agent | Schedule | Purpose |
|---|---|---|
| [[agents/morning_briefing\|morning_briefing]] | `daily:07:00` | Briefing matinal via Ollama + Telegram push |
| [[agents/watchdog\|watchdog]] | `every:15m` | Auto-extract new reports + trigger alerts + earnings reminders |
| [[agents/thesis_refresh\|thesis_refresh]] | `weekly:sun:22:00` | Re-run thesis_refresh + obsidian_bridge |
| [[agents/subscription_fetch\|subscription_fetch]] | `weekly:mon:09:00` | Fetch new Fool/XP/WSJ reports |

## Schedule formats

- `manual` — só via `ii agents run <name>`
- `daily:HH:MM` — uma vez ao dia
- `every:Nm` / `every:Nh` — a cada N min/horas
- `weekly:DOW:HH:MM` — DOW em mon/tue/wed/thu/fri/sat/sun

## CLI (`ii agents`)

```bash
ii agents list                        # todos registered com last run
ii agents status                      # dashboard detalhado
ii agents run morning_briefing        # trigger manual
ii agents run-due                     # executar todos schedule-due agora
ii agents enable <name>
ii agents disable <name>
ii agents create <name>               # scaffold novo agent from template
     --schedule "daily:08:00"
     --desc "Monitora Y e faz Z"
ii agents show <name>                 # config + state + status
ii agents logs <name> [--tail 100]    # log output
ii agent-runner                       # entry para cron
```

## Budget discipline (Claude escalation)

- Default: Ollama local, zero tokens.
- Agents podem pedir Claude via `llm_summarise(prompt, prefer='claude')` MAS:
  - `LLMBudget` em `data/agents/_llm_budget.json` tracks tokens spent/day
  - Default cap: **50,000 tokens/day**
  - Quando excede: fallback automático a Ollama
- Escalation só faz sense para: decisões estratégicas multi-dimensional
- Default sempre Ollama

## Setup cron (Windows)

```powershell
schtasks /create /tn "ii-agent-runner" /sc minute /mo 1 `
  /tr "C:\Users\paidu\investment-intelligence\.venv\Scripts\python.exe C:\Users\paidu\investment-intelligence\scripts\agent_runner.py"
```

## Setup cron (Linux / WSL)

```bash
* * * * * cd ~/investment-intelligence && python scripts/agent_runner.py >> logs/agent_runner.log 2>&1
```

## Como criar novo agent

### Path fácil (template-based)

```bash
ii agents create my_agent --schedule "daily:10:00" --desc "O que este agent faz"
```

1. Scaffolda `agents/my_agent.py` a partir de `agents/templates/periodic.py.tpl`.
2. Auto-registra em `config/agents.yaml`.
3. Editas `execute_impl()` no ficheiro gerado.
4. Testas: `ii agents run my_agent --dry-run`.
5. Habilita: já habilitado por default.

### Path manual (custom)

1. Cria `agents/<name>.py` herdando de `BaseAgent`.
2. Implementa `execute_impl(ctx) -> AgentResult`.
3. Adiciona entry em `config/agents.yaml`:
   ```yaml
   - name: my_agent
     class: agents.my_agent:MyAgent
     enabled: true
     schedule: "daily:10:00"
     description: "..."
     config: {}
   ```

## AgentResult contract

Agents devolvem `AgentResult` com:
- `status` — `ok` | `no_action` | `failed` | `skipped`
- `summary` — 1-3 linhas humano-legível
- `actions` — lista de efeitos (journal)
- `errors` — lista de strings (fail-soft)
- `data` — dict agent-specific (estrutural para futuro LLM review)

## Observability

- **State file** (`data/agents/<name>.json`): run_count, last_run, last_status, last_error
- **Status MD** (`obsidian_vault/agents/<name>.md`): última execução formatada
- **Logs** (`logs/agents/<name>_YYYY-MM-DD.log`): output rotado diário

## Integration com Obsidian

- `obsidian_vault/agents/<name>.md` atualiza a cada run
- [[_MOC]] tem secção "Agents" com links live
- Dataview query possível:

```dataview
TABLE status, last_run, duration_sec
FROM "agents"
WHERE type = "agent_status"
SORT last_run DESC
```

## Próximos agents planeados (backlog)

- **analyst_backtest** — `weekly:wed:20:00` — tracks analyst predictions vs price moves 30/90/180d depois
- **wiki_curator** — `monthly:1:18:00` — detecta topics recurring em reports sem wiki note, draft via Ollama
- **news_digest** — `daily:18:00` — scan news_fetch + Ollama resume market close BR+US
- **cash_reminder** — `daily:09:00` — alerta cash idle > target threshold (opportunity cost)

## Related

- 🚨 [[Token_discipline]] — meta-regra
- [[Analysis_workflow]] — fluxo ideal; agents eliminam fricção "⚠️ manual"
- [[Web_scraping_subscriptions]] — scraping infra que watchdog + subscription_fetch usam
- [[Buy_checklist]] / [[Sell_triggers]] — decisões que agents apoiam (não substituem)

## Memory refs

- Fase V+ do roadmap
- Complementa Phase U (scraping infra) com layer autonomy
