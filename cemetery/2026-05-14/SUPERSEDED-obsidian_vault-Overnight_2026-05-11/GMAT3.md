# GMAT3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://ri.grupomateus.com.br/
- **Pilot rationale**: manual (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=4.590000152587891
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.17944999 · DY=0.04121938860793474 · P/E=5.5975614
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 10.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.grupomateus.com.br/ | ✅ | 10.4s | 6,439 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **0**
- Headers detectados (structure): **4**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Relatórios Financeiros](https://ri.grupomateus.com.br/relatorios-e-publicacoes/relatorios-financeiros/)
- [Apresentação](https://ri.grupomateus.com.br/relatorios-e-publicacoes/apresentacao/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.17944999, DY=0.04121938860793474 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
