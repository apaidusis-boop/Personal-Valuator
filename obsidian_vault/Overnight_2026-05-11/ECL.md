# ECL — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://investor.ecolab.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=254.22000122070312
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.22427 · DY=0.010856738206070119 · P/E=34.354053
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 14.7s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.ecolab.com/ | ✅ | 14.7s | 24,885 |
- Filings extraídos do RI: **4**
- Eventos calendário: **0**
- Apresentações/releases: **4**
- Audio/video: **3**
- Headers detectados (structure): **43**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 7, 2026 | Ecolab Declares Cash Dividend |
| May 7, 2026 | Ecolab to Webcast Annual Meeting on May 7, 2026 |
| April 28, 2026 | Ecolab Delivers Accelerated Sales Growth and Double-Digit EPS Growth; Reported D |
| April 28, 2026 | Ecolab Q1 2026 Earnings Release Call |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (4 total, top 4)

- [Events & Presentations](https://investor.ecolab.com/events-and-presentations/default.aspx)
- [Earnings Release(opens in new window)](https://s204.q4cdn.com/218790897/files/doc_financials/2026/q1/Q1-2026-Earnings-Release.pdf)
- [Earnings Slides(opens in new window)](https://s204.q4cdn.com/218790897/files/doc_financials/2026/q1/Q1-2026-Earnings-Presentation-2.pdf)
- [Download Presentation(opens in new window)](https://s204.q4cdn.com/218790897/files/doc_financials/2026/q1/Investor-Presentation.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://virtualshareholdermeeting.com/ECL2026)
- [Webcast(opens in new window)](https://events.q4inc.com/attendee/688092333)
- [Webcast(opens in new window)](https://events.q4inc.com/attendee/786432902)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 4 | + |
| Audio/video acessível | 0 (era cego) | 3 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **3 fontes audio/video** disponíveis (markitdown pode transcrever)
- **4 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **3 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 4 releases/relatórios — podemos auditar se ROE=0.22427, DY=0.010856738206070119 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
