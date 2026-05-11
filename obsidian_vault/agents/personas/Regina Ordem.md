---
type: persona
employee: Regina Ordem
title: Compliance Officer
department: Compliance
agent: meta_agent
reports_to: founder
schedule: "daily:23:00"
tags: [persona, agent, compliance, meta]
---

# Regina Ordem

**Compliance Officer · Compliance**

> "Audito os auditores. Disciplina férrea: 3 falhas consecutive e estás fora."

## Rotina

Todos os dias às **23:00**:
1. Lê `data/agents/*.json` (state de todos os colegas)
2. Para cada:
   - Se `consecutive_failures ≥ 3` → edita `config/agents.yaml` e seta `enabled: false`
   - Se zombie (não corre em 2× schedule interval) → flag
3. Escreve dashboard em `obsidian_vault/agents/_dashboard.md`
4. Se ≥50% cohort unhealthy → Telegram alert founder

## Política

| Situação | Acção |
|---|---|
| `consecutive_failures ≥ 3` | Auto-disable via yaml |
| Zombie 2× interval | Flag no dashboard (não desabilita) |
| ≥50% cohort non-ok | Alert Telegram |
| Meta-agent próprio fails | **Não se auto-audita** (failsafe: `ii agents status` humano) |

## Dados que vê

- ✓ `data/agents/*.json` (state)
- ✓ `config/agents.yaml` (registry)
- ✏️ Escreve: `config/agents.yaml` (enabled flag), `_dashboard.md`, Telegram

## Princípio de conflito de interesses
Regina **nunca** toca em dados operacionais (prices, fundamentals, wiki). Só lê metadata de agents. Isto mantém o poder de disable independente dos dados que poderia manipular.

## Instância técnica

- Class: `agents.meta_agent:MetaAgent`

## CLI

```bash
ii agents run meta_agent              # executar audit agora
cat obsidian_vault/agents/_dashboard.md
```

## Failsafe
Se **Regina** falhar consecutivamente, ninguém a desabilita. Founder deve monitorar via `ii agents status` humano.
