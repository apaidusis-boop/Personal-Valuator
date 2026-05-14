# MGEE — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://www.mgeenergy.com/investor-relations
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=73.6500015258789
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.10948 · DY=0.02545824794506173 · P/E=18.884615
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 14.9s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.mgeenergy.com/investor-relations | ✅ | 14.9s | 6,959 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **0**
- Headers detectados (structure): **2**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Investor Relations](https://www.mgeenergy.com/invest/investor-relations)
- [Investor Presentations](https://www.mgeenergy.com/invest/investor-presentations)
- [Corporate Responsibility and Sustainability Report](https://www.mgeenergy.com/MGEEnergy/media/Library/documents/environmental-reports/2025-corporate-responsibility-sustainability-report-20260116.pdf)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.10948, DY=0.02545824794506173 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
