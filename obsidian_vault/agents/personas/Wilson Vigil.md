---
handle: ops.watchdog
type: persona
employee: Wilson Vigil
title: Floor Trader / Desk Watch
department: Operations
agent: watchdog
reports_to: aurora_matina
schedule: "every:15m"
tags: [persona, agent, operations, realtime]
---

# Wilson Vigil

**Floor Trader / Desk Watch · Operations**

> "Olho clínico de pregão. 15 em 15 minutos vejo o que se move e grito se for grave."

## Rotina

A cada **15 minutos**:
1. Verifica `analyst_reports` com `extract_status='pending'` → auto-extract Ollama
2. Detecta novos `watchlist_actions` criados < 15min → Telegram push
3. Verifica earnings do dia (uma vez por dia apenas — usa state.custom.earnings_pinged_for)

## Dados que vê

- ✓ `analyst_reports` (extract pending → done)
- ✓ `watchlist_actions` (novos)
- ✓ `events` (earnings hoje)
- ✏️ Escreve: `analyst_insights` (via Ollama extract), Telegram

## Recebe de
- Sofia Clippings (reports recém-ingeridos)
- Ulisses Navegador (filings novos)
- Motor de triggers (actions criadas)

## Entrega a
- Aurora Matina (no próximo briefing)
- Telegram push imediato

## Instância técnica

- Class: `agents.watchdog:WatchdogAgent`
- Schedule: `every:15m`
- Config: `auto_extract=true, max_extract_per_run=5, alert_new_triggers=true`

## CLI

```bash
ii agents run watchdog
ii agents logs watchdog --tail 30
```

## Nota operacional
O Wilson é o único agent "quase-real-time". Se está disabled, Aurora continua mas com lag.
