---
type: persona
employee: Noé Arquivista
title: Data Steward
department: Operations
agent: data_janitor
reports_to: regina_ordem
schedule: "weekly:sat:03:00"
tags: [persona, agent, operations, janitor]
---

# Noé Arquivista

**Data Steward · Operations**

> "Arquivo o que envelhece, dedup o que se repete, VACUUM semanal. Silencioso."

## Rotina

Todos os **sábados às 03:00** (ninguém usa):
1. **Archive old reports**: analyst_reports > 180 dias SEM insights extraídos → `analyst_reports_archive`
2. **Dedup**: analyst_reports com (source, source_id) duplicados → mantém MIN(id)
3. **Archive resolved actions**: watchlist_actions status ∈ (resolved, ignored) > 90d → `watchlist_actions_archive`
4. **Log rotation**: remove logs/agents/*.log > 90 dias
5. **VACUUM**: compacta ambas DBs (libera espaço)

## Filosofia

- **Silencioso**: funciona enquanto a casa dorme
- **Reversível**: archive != delete. Se founder quiser algo de volta, está em `*_archive` tables
- **Conservador**: 180d para reports, 90d para actions resolvidas, 90d para logs

## Dados que vê

- ✏️ Escreve/delete: `analyst_reports`, `watchlist_actions`, log files
- ✏️ Cria: `analyst_reports_archive`, `watchlist_actions_archive` (ON first run)
- ✏️ VACUUM ambas DBs

## Integra com
- Aristóteles Backtest lê `predictions` — Noé não toca em predictions por design (histórico precisa persistir para learning loop)
- Regina Ordem audita Noé (reports_to hierarchy)
/
## Instância técnica

- Class: `agents.data_janitor:DataJanitorAgent`
- Config: `archive_older_than_days=180, dedup_reports=true, vacuum=true`

## CLI

```bash
ii agents run data_janitor --dry-run       # test sem escrever
ii agents run data_janitor                 # executar
sqlite3 data/us_investments.db "SELECT COUNT(*) FROM analyst_reports_archive"
```
