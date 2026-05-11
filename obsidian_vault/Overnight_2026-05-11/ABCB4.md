# ABCB4 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Banks
- **RI URLs scraped** (1):
  - https://ri.abcbrasil.com.br/
- **Pilot rationale**: manual (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-04-24 → close=25.280000686645508
- Último fundamentals snapshot: period_end=2026-04-25 · ROE=0.15463 · DY=0.10298176144335587 · P/E=4.725234

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.abcbrasil.com.br/ | ✅ | 12.2s | 15,911 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **1**
- Audio/video: **0**
- Headers detectados (structure): **11**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (1 total, top 1)

- [Relatório Anual Integrado](https://ri.abcbrasil.com.br/esg/relatorio-anual-integrado/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 1 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 1 releases/relatórios — podemos auditar se ROE=0.15463, DY=0.10298176144335587 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
