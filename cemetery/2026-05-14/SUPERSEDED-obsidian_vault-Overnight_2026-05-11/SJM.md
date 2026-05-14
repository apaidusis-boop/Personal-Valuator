# SJM — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://investors.jmsmucker.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **4**
- Última cotação DB: 2026-05-08 → close=99.25
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=-0.20683001 · DY=0.04413098236775819 · P/E=None
- Score (último run): score=0.75 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.6s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.jmsmucker.com/ | ✅ | 11.6s | 22,911 |
- Filings extraídos do RI: **3**
- Eventos calendário: **0**
- Apresentações/releases: **6**
- Audio/video: **2**
- Headers detectados (structure): **26**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| April 16, 2026 | The J.M. Smucker Co. Declares Dividend and Announces Annual Shareholder Meeting  |
| February 26, 2026 | The J.M. Smucker Co. Appoints Two New Independent Directors |
| February 26, 2026 | The J.M. Smucker Co. Announces Fiscal 2026 Third Quarter Results |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (6 total, top 6)

- [Events & Presentations](https://investors.jmsmucker.com/events-and-presentations/default.aspx)
- [Learn More about CAGNY 2026 Presentation](https://investors.jmsmucker.com/events-and-presentations/events/event-details/2026/CAGNY-2026-Presentation/default.aspx)
- [Press Release(opens in new window)](https://s203.q4cdn.com/703080298/files/doc_financials/2026/q3/The-J-M-Smucker-Co-Announces-Fiscal-2026-Third-Quarter-Results.pdf)
- [Supplemental Information(opens in new window)](https://s203.q4cdn.com/703080298/files/doc_financials/2026/q3/The-J-M-Smucker-Co-FY26-Q3-Earnings-Supplement.pdf)
- [Download(opens in new window)](https://s203.q4cdn.com/703080298/files/doc_events/2026/02/The-J-M-Smucker-Co-2026-CAGNY-Presentation.pdf)
- [Events & Presentations](https://investors.jmsmucker.com/events-and-presentations)

### Audio / Video disponível (markitdown pode ler)

- [Learn More about Q3 FY26 The J.M. Smucker Co. Earnings Q&A Webcast](https://investors.jmsmucker.com/events-and-presentations/events/event-details/2026/Q3-FY26-The-JM-Smucker-Co-Earnings-QA-Webcast-2026-daKC529OK3/default.aspx)
- [Q&A Webcast(opens in new window)](https://event.choruscall.com/mediaframe/webcast.html?webcastid=M2G5y2Rq)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 6 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **6 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 6 releases/relatórios — podemos auditar se ROE=-0.20683001, DY=0.04413098236775819 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
