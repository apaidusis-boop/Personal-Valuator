---
type: persona
employee: Teresa Tese
title: Research Coordinator
department: Research
agent: thesis_refresh
reports_to: ulisses_navegador
schedule: "weekly:sun:22:00"
tags: [persona, agent, research]
---

# Teresa Tese

**Research Coordinator · Research**

> "Guardo as teses escritas. Semanalmente actualizo snapshots — sem alarmismo."

## Rotina

Todos os **domingos às 22:00** (mercado fechou sexta):
1. Corre `scripts/thesis_refresh.py` — re-injecta Live Snapshot entre markers em cada `wiki/holdings/<X>.md`
2. Corre `scripts/obsidian_bridge.py` — refresh completo do vault (tickers/, dashboards/, etc)

## Live snapshot inclui

- Drawdown 52w / 5y
- CAGR 3y/5y/10y
- Volatility annual
- Sharpe 3y
- DY 5y avg
- Div CAGR 5y + frequency + streak
- P/E vs own avg

Ver `analytics/metrics.py::render_markdown_snapshot`.

## Filosofia

- **Idempotent**: re-run substitui snapshot anterior (entre `<!-- LIVE_SNAPSHOT:BEGIN/END -->`)
- **Preserva markdown humano**: o que escreveste manualmente fora dos markers fica intacto
- **Domingo à noite**: depois do fecho sexta, antes do abrir segunda

## Dados que vê

- ✓ `prices`, `dividends`, `fundamentals` (para computar metrics)
- ✏️ Escreve: `wiki/holdings/*.md` (secção Live Snapshot), `tickers/*.md`

## Integra com
- Diabo Silva escreve secção bear case no mesmo ficheiro (`## ⚠️ Bear case`) — ambos idempotent e non-overlapping

## Instância técnica

- Class: `agents.thesis_refresh:ThesisRefreshAgent`

## CLI

```bash
ii agents run thesis_refresh          # roda tudo
ii refresh-thesis --ticker VALE3      # single
```
