# CB — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investors.chubb.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=319.6400146484375
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.15433 · DY=0.006069327715848555 · P/E=11.310687
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 14.0s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.chubb.com/ | ✅ | 14.0s | 20,955 |
- Filings extraídos do RI: **6**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **0**
- Headers detectados (structure): **12**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| April 21, 2026 | Chubb Reports First Quarter Per Share Net Income and Core Operating Income of $5 |
| April 22, 2026 | Chubb Limited to Hold its First Quarter Earnings Conference Call on Wednesday, A |
| February 26, 2026 | Chubb Limited Board Will Recommend 33rd Consecutive Annual Dividend Increase to  |
| February 03, 2026 | Chubb Reports Fourth Quarter Net Income of $3.21 Billion, Up 24.7%, and Core Ope |
| February 4, 2026 | Chubb Limited to Hold its Fourth Quarter Earnings Conference Call on Wednesday,  |
| November 20, 2025 | Chubb Limited Board Declares Quarterly Dividend |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Events & Presentations](https://investors.chubb.com/News--Events/news-presentations/default.aspx)
- [Press Release(opens in new window)](https://s201.q4cdn.com/471466897/files/doc_financials/2026/q1/1st-Quarter-2026-Earnings-Press-Release.pdf)
- [Financial Supplement(opens in new window)](https://s201.q4cdn.com/471466897/files/doc_financials/2026/q1/Q1-2026-Chubb-Limited-Financial-Supplement.xlsm)

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

- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.15433, DY=0.006069327715848555 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
