# LOW — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://ir.lowes.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=229.1999969482422
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=None · DY=0.020942408655807848 · P/E=19.341772
- Score (último run): score=0.75 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 30.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ir.lowes.com/ | ✅ | 30.4s | 12,880 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **4**
- Audio/video: **0**
- Headers detectados (structure): **4**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (4 total, top 4)

- [Events & Presentations](https://ir.lowes.com/investors/news-events/events-presentations)
- [Contact Investor Relations](https://ir.lowes.com/investors/shareholder-services/contact-investor-relations)
- [Contact Media Relations](https://ir.lowes.com/newsroom/contact-media-relations)
- [Annual Report 2024](https://ir.lowes.com/sites/lowes-corp/files/2025-04/Lowes_2024_Annual_Report_Website.pdf)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 4 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **4 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 4 releases/relatórios — podemos auditar se ROE=None, DY=0.020942408655807848 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
