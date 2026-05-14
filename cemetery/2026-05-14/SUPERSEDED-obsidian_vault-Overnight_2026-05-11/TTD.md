# TTD — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Communication
- **RI URLs scraped** (1):
  - https://investors.thetradedesk.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **134**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=23.079999923706055
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.16317 · DY=None · P/E=26.227272
- Score (último run): score=0.25 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 8-K | sec | 8-K \| 5.02 |
| 2026-05-08 | 8-K | sec | 8-K \| 5.07 |
| 2026-05-07 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-05-07 | 10-Q | sec | 10-Q |
| 2026-04-20 | 8-K | sec | 8-K \| 1.01,2.03 |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 19.1s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.thetradedesk.com/ | ✅ | 19.1s | 11,122 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **4**
- Audio/video: **1**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 07, 2026 | The Trade Desk Reports First Quarter 2026 Financial Results |
| May 07, 2026 | The Trade Desk, Pacvue, and Skai Unlock Unified Activation and Measurement Acros |
| April 28, 2026 | The Trade Desk Announces Date of First Quarter 2026 Financial Results and Confer |
| 2026-05-07 | The latest press releases |
| 2026-05-07 | Q1 2026 The Trade Desk Earnings Conference Call |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (4 total, top 4)

- [Presentations](https://investors.thetradedesk.com/news-and-events/presentations/default.aspx)
- [Download PDF(opens in new window)](https://s205.q4cdn.com/467402606/files/doc_earnings/2026/q1/presentation/TheTradeDesk_Q126_Investor_Presentation.pdf)
- [Transcript(opens in new window)](https://s205.q4cdn.com/467402606/files/doc_earnings/2026/q1/transcript/The-Trade-Desk-First-Quarter-2026-Conference-Call-Prepared-Remarks.pdf)
- [Investor relations](https://investors.thetradedesk.com/resources/contact-ir/default.aspx)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://events.q4inc.com/attendee/185538199)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 134 | 134 + 2 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 4 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**2 filings detectados como novos vs DB.**

### 1. 2026-05-07 — The latest press releases

URL: https://investors.thetradedesk.com/news-and-events/news/default.aspx
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

* [Overview](https://investors.thetradedesk.com/overview/default.aspx)
  + [News & Events](https://investors.thetradedesk.com/news-and-events/news/default.aspx)
    - [News](https://investors.thetradedesk.com/news-and-events/news/default.aspx)
    - [Events](https://investors.thetradedesk.com/news-and-events/events/default.aspx)
    - [Presentations](https://investors.thetradedesk.com/news-and-events/presentations/default.aspx)
  + [Financials](https://investors.thetradedesk.com/financials/quarterly-results/default.aspx)
    - [Quarterly results](https://investors.thetradedesk.com/financials/quarterly-results/default.aspx)
    - [Annual reports](https://investors.thetradedesk.com/financials/annual-reports/default.aspx)
    - [SEC filings](https://investors.thetradedesk.com/financials/sec-filings/default.aspx)
  + [Stock Info](https://investors.thetradedesk.com/stock-info/stock-quote-chart/default.aspx)
    - [Stock quote & chart](https://investors.thetradedesk.com/stock-info/stock-quote-chart/default.aspx)
    - [Analyst coverage](https://investors.thetradedesk.com/stock-info/analyst-coverage/default.aspx)
  + [Governance](https://investors.thetradedesk.com/governance/governance-documents/default.aspx)
    - [Governance documents](https://investors.thetradedesk.com/governance/governance-documents/default.aspx)
    - [Executive management](https://www.thetradedesk.com/us/about-us/our-leadership)
    -
```

### 2. 2026-05-07 — Q1 2026 The Trade Desk Earnings Conference Call

URL: https://investors.thetradedesk.com/news-and-events/events/event-details/2026/Q1-2026-The-Trade-Desk-Earnings-Conference-Call/default.aspx
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

* [Overview](https://investors.thetradedesk.com/overview/default.aspx)
  + [News & Events](https://investors.thetradedesk.com/news-and-events/news/default.aspx)
    - [News](https://investors.thetradedesk.com/news-and-events/news/default.aspx)
    - [Events](https://investors.thetradedesk.com/news-and-events/events/default.aspx)
    - [Presentations](https://investors.thetradedesk.com/news-and-events/presentations/default.aspx)
  + [Financials](https://investors.thetradedesk.com/financials/quarterly-results/default.aspx)
    - [Quarterly results](https://investors.thetradedesk.com/financials/quarterly-results/default.aspx)
    - [Annual reports](https://investors.thetradedesk.com/financials/annual-reports/default.aspx)
    - [SEC filings](https://investors.thetradedesk.com/financials/sec-filings/default.aspx)
  + [Stock Info](https://investors.thetradedesk.com/stock-info/stock-quote-chart/default.aspx)
    - [Stock quote & chart](https://investors.thetradedesk.com/stock-info/stock-quote-chart/default.aspx)
    - [Analyst coverage](https://investors.thetradedesk.com/stock-info/analyst-coverage/default.aspx)
  + [Governance](https://investors.thetradedesk.com/governance/governance-documents/default.aspx)
    - [Governance documents](https://investors.thetradedesk.com/governance/governance-documents/default.aspx)
    - [Executive management](https://www.thetradedesk.com/us/about-us/our-leadership)
    -
```


## Sinais / observações

- **2 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **4 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 4 releases/relatórios — podemos auditar se ROE=0.16317, DY=None batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
