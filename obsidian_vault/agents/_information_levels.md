---
type: info_levels
tags: [agents, information, access, levels]
---

# 🧠 Níveis de Informação — o que cada funcionário vê

> Clearance de dados por agent. Quem lê o quê, quem escreve o quê.

## Matriz de acesso

| Agent | prices | fundamentals | analyst_insights | watchlist_actions | predictions | wiki | Telegram |
|---|---|---|---|---|---|---|---|
| Aurora Matina | 📖 | 📖 | 📖 | 📖 | 📖 | ✏️ briefings | ✏️ push |
| Wilson Vigil | 📖 | 📖 | ✏️ extract | 📖 | — | — | ✏️ alerts |
| Teresa Tese | 📖 | 📖 | 📖 | — | — | ✏️ holdings | — |
| Sofia Clippings | — | — | — | — | — | — | — |
| Ulisses Navegador | — | — | — | — | — | — | — |
| Valentina Prudente | 📖 | 📖 | — | ✏️ create | — | — | ✏️ push |
| Diabo Silva | — | 📖 | 📖 bear | — | — | ✏️ holdings bear | — |
| Regina Ordem | — | — | — | — | — | ✏️ dashboard | ✏️ alert |
| Aristóteles Backtest | 📖 | — | 📖 | — | ✏️ full | ✏️ ranking | — |
| Clara Fit | 📖 | — | 📖 | ✏️ create | 📖 | — | — |
| Noé Arquivista | — | — | ✏️ delete | ✏️ archive | — | — | — |
| Zé Mensageiro | — | — | — | ✏️ resolve | — | — | ✏️ receive/send |

Legenda:
- 📖 read-only
- ✏️ write
- — sem acesso

## Tabelas adicionais

| Agent | events | portfolio_positions | companies | videos | agent_runs | agents_state |
|---|---|---|---|---|---|---|
| Aurora Matina | 📖 | 📖 | 📖 | — | — | — |
| Wilson Vigil | ✏️ | 📖 | 📖 | 📖 | — | — |
| Ulisses Navegador | ✏️ | — | 📖 | — | — | — |
| Clara Fit | — | 📖 | 📖 | — | — | — |
| Aristóteles Backtest | — | — | 📖 | 📖 | 📖 | — |
| Regina Ordem | — | — | — | — | 📖 | ✏️ disable |
| Noé Arquivista | — | — | — | — | ✏️ VACUUM | — |

## External reach (quem pode tocar em fontes externas)

| Agent | brapi | yfinance | SEC EDGAR | CVM | Websites scraping | Telegram API |
|---|---|---|---|---|---|---|
| Wilson Vigil | — | — | — | — | via subscriptions_cli | — |
| Sofia Clippings | — | — | — | — | ✏️ Fool/XP/WSJ | — |
| Ulisses Navegador | — | — | 📖 monitor | 📖 monitor | — | — |
| Zé Mensageiro | — | — | — | — | — | ✏️ long-poll |
| (fetchers diretos) | 📖 | 📖 | 📖 | 📖 | — | — |

## Princípio de least privilege

Cada funcionário vê **apenas** o que precisa para o trabalho. Exemplos:

- **Teresa Tese** só precisa ler insights + holdings para refrescar teses — não precisa de Telegram nem de triggers
- **Diabo Silva** só precisa ler fundamentals + analyst_insights bear para escrever bear case — não precisa ler holdings table completa
- **Noé Arquivista** só escreve em archive tables; nunca toca em dados ativos
- **Regina Ordem** lê state files mas não toca em dados operacionais (capital preservation — quem audita não tem conflito)

## Kill switches

Se algum agent começa a corromper dados, **Regina Ordem** auto-disabla após 3 failures consecutivos editando `config/agents.yaml::enabled: false`. Founder pode manualmente via:

```bash
ii agents disable <name>        # humano
```

## Budget de escalation Claude

| Tier | Quem pode chamar Claude | Budget cap |
|---|---|---|
| L0 Founder | sempre | N/A (conversacional) |
| L1 Heads | via `escalate_to_claude()` em `_llm.py` | 50K tokens/dia **shared** (global) |
| L2 Specialists | proibido por default | — |
| L3 Janitors | proibido | — |

**Default**: 100% Ollama Qwen 14B local.

Actualmente nenhum agent chama Claude — só o framework prepara o caminho. `LLMBudget` em `data/agents/_llm_budget.json` serve de ledger.

## Secret / credentials access

| Credential | Quem precisa |
|---|---|
| `BRAPI_TOKEN` (.env) | fetchers BR |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (.env) | Zé Mensageiro + notifiers.telegram |
| Subscription cookies | Sofia Clippings (via `data/subscriptions/cookies/`) |
| Playwright profile | Sofia Clippings (`.playwright-profiles/`) |
| SQLite DB files | TODOS (single source of truth) |

Credenciais em `.env` + `data/subscriptions/cookies/` + `.playwright-profiles/` **gitignored** — nunca no repo.

---

*Para fluxo visual, ver [[_flow_diagram]]. Para hierarquia, [[_org_chart]].*
