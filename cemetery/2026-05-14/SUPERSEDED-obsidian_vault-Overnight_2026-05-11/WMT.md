# WMT — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://stock.walmart.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=130.42999267578125
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.21847 · DY=0.007406271979185433 · P/E=47.776554
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://stock.walmart.com/ | ✅ | 11.8s | 17,566 |
- Filings extraídos do RI: **1**
- Eventos calendário: **0**
- Apresentações/releases: **7**
- Audio/video: **0**
- Headers detectados (structure): **23**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| Jan 31, 2026 | Earnings ReleasePDF |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (7 total, top 7)

- [Contact Media Relations](https://corporate.walmart.com/news/contact-media-relations)
- [PresentationPDF](https://stock.walmart.com/_assets/_5bb4b0137bcb7c329b4b74e982c643dd/walmart/db/938/9972/presentation/Earnings%2BPresentation%2B%28FY26%2BQ4%29.pdf)
- [Transcript - Management CallPDF](https://stock.walmart.com/_assets/_5bb4b0137bcb7c329b4b74e982c643dd/walmart/db/938/9972/transcript_management_call/Earnings%2BTranscript%2B%28FY26%2BQ4%29.pdf)
- [Transcript - Buy Side Follow Up CallPDF](https://stock.walmart.com/_assets/_5bb4b0137bcb7c329b4b74e982c643dd/walmart/db/938/9972/transcript_buy_side_follow_up_call/Buy%2BSide%2BFollow-Up%2BCall%2BTranscript%2BFY26%2BQ4.pdf)
- [Earnings TerminologyPDF](https://stock.walmart.com/_assets/_5bb4b0137bcb7c329b4b74e982c643dd/walmart/db/938/9972/earnings_terminology/Earnings%2BTerminology%2B%28FY26%2BQ4%29.pdf)
- [HTML Release and Related PhotosHTML](https://corporate.walmart.com/news/2026/02/19/walmart-releases-q4-fy26-earnings)
- [Annual Report](https://stock.walmart.com/_assets/_5bb4b0137bcb7c329b4b74e982c643dd/walmart/db/950/9988/annual_report/Walmart%2B2026%2BAnnual%2BReport.pdf)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 7 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **7 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 7 releases/relatórios — podemos auditar se ROE=0.21847, DY=0.007406271979185433 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
