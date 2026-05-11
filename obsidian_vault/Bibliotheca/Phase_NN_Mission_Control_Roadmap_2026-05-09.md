---
type: design_brief
date: 2026-05-09
phase: NN
status: draft_overnight_synthesis
tags: [phase_nn, mission_control, roadmap, design_brief]
---

# Phase NN · Mission Control Roadmap (overnight synthesis)

> Junta os 3 outputs da noite (audit + Bloomberg research + widget research) 
> num roadmap concreto. Assina-se tudo amanhã com o user antes de codar.

## Estado do mundo (audit)

- Universe seguido: **155** tickers
- Holdings activas: **33**
- Tickers sem prices 10y: **8**
- Tickers sem fundamentals 10y: **119**

Detalhe completo: `Data_Coverage_Audit_2026-05-09.md`

## Insights research (Bloomberg + Widgets)

- Queries Bloomberg/Voila: **15**
- Queries widgets: **10**

Detalhes:
- `Bloomberg_Terminal_Patterns_2026-05-09.md`
- `Compact_Widgets_Patterns_2026-05-09.md`

## Próximos sprints propostos

### Sprint NN.1 · Chart system v2

- Substituir SVG raw por Recharts (já em package.json)
- Hover crosshair vertical + tooltip flutuante com valores de todos os tickers
- Período zoom + pan
- Responsive verdadeiro via `<ResponsiveContainer>`
- Aplicar a: Compare tab + DRIP charts + ticker tearsheet price line

### Sprint NN.2 · Micro-station layout

- Reorganizar o Workbench em 4 panes simultâneos sincronizados pelo focus-ticker
- Top: big chart
- Middle: positions table compacta
- Right rail: mini-cards 'next dividends' + 'next filings'
- Inspirado em padrões Bloomberg detectados na noite (ver research)

### Sprint NN.3 · /stocks watchlist expansion

- Mostrar TODA a watchlist (~108 tickers) e Kings/Aristocrats (~87)
- Não só holdings activas
- Filter chip 'Holdings only / Watchlist / All'

### Sprint NN.4 · Data backfill (carece tua aprovação)

Baseado nos gaps do audit:
- Backfill prices p/ 8 tickers via yfinance --period max
- Backfill fundamentals p/ 119 tickers via yf_deep_fundamentals
- CVM/SEC events para holdings sem cobertura events

**Custo estimado**: 30–60 min de runtime, write ao `data/`. **Precisa tua aprovação.**

## Decisões pendentes para o user

- [ ] Aprovar chart system v2 com Recharts? (alternativa: Visx, Plotly)
- [ ] Aprovar layout micro-station 4-pane? (vou trazer 3 mockups ASCII)
- [ ] Aprovar /stocks watchlist expansion?
- [ ] Aprovar backfill priorities (decidir quais gaps fechar)?
