# MULT3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Real Estate
- **RI URLs scraped** (1):
  - https://www.multri.com.br/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=31.799999237060547
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.20018 · DY=0.03406424610028167 · P/E=12.874494
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Data de eficácia da capit |
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Teleconferência de Resultados - 1 |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Participação de executivo |
| 2026-04-20 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Alienação de Participação |
| 2026-04-07 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Reunião Pública Multiplan 2026 -  |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 7.3s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.multri.com.br/ | ✅ | 7.3s | 7,969 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **0**
- Headers detectados (structure): **36**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 13 | 13 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 0 | = |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

_(sem sinais accionáveis — RI sem novidades vs DB)_

## Interpretação para a tese

_(sem sinais accionáveis materiais)_

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
