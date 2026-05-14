# NFG — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://investor.nationalfuelgas.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=79.5199966430664
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.20833 · DY=0.026911469948943886 · P/E=10.745945
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 13.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.nationalfuelgas.com/ | ✅ | 13.2s | 30,084 |
- Filings extraídos do RI: **3**
- Eventos calendário: **0**
- Apresentações/releases: **5**
- Audio/video: **0**
- Headers detectados (structure): **35**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 04/29/2026 | National Fuel Reports Second Quarter Fiscal 2026 Earnings |
| 04/09/2026 | National Fuel Schedules Second Quarter Fiscal 2026 Earnings Conference Call |
| 03/12/2026 | National Fuel Declares Quarterly Dividend and Reports Preliminary Voting Results |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (5 total, top 5)

- [Investor Relations](https://investor.nationalfuelgas.com/)
- [Presentations](https://investor.nationalfuelgas.com/news-and-events/presentations/default.aspx)
- [Transcripts](https://investor.nationalfuelgas.com/news-and-events/transcripts/default.aspx)
- [Earnings Report(opens in new window)](https://s1.q4cdn.com/329525430/files/doc_downloads/2026/04/NFG-3-31-2026-Earnings-Release-04292026-V-FINAL.pdf)
- [Transcript(opens in new window)](https://s1.q4cdn.com/329525430/files/doc_financials/2026/q2/NFG-Q2-FY26-Transcript-vFinal.pdf)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 3 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 5 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**3 filings detectados como novos vs DB.**

### 1. 04/29/2026 — National Fuel Reports Second Quarter Fiscal 2026 Earnings

URL: https://investor.nationalfuelgas.com/news-and-events/press-releases/press-releases-details/2026/National-Fuel-Reports-Second-Quarter-Fiscal-2026-Earnings/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

* [Our Responsibility](https://www.nationalfuel.com/corporate/our-guiding-principles/)
* [Careers](https://www.nationalfuel.com/corporate/work-at-national-fuel/)
* [Investor Relations](https://investor.nationalfuelgas.com/)
* [Contact Us](https://www.nationalfuel.com/corporate/contact-us-directory/)

* [Our Company](https://www.nationalfuel.com/)
* [Utility Services](https://www.nationalfuel.com/utility/)
* [Business Partners](https://www.nationalfuel.com/business-partners/)
* [Pipeline & Storage](https://www.nationalfuel.com/pipeline-storage/)
* [Integrated Upstream & Gathering](https://www.nationalfuel.com/integrated-upstream-gathering/)

toggle main menu

* [Home](https://investor.nationalfuelgas.com/home/default.aspx)
  + [News & Events](https://investor.nationalfuelgas.com/news-and-events/press-releases/default.aspx)
    - [Press Releases](https://investor.nationalfuelgas.com/news-and-events/press-releases/default.aspx)
    - [Presentations](https://investor.nationalfuelgas.com/news-and-events/presentations/default.aspx)
    - [Events Calendar](https://investor.nationalfuelgas.com/news-and-events/events-calendar/default.aspx)
    - [Transcripts](https://investor.nationalfuelgas.com/news-and-events/transcripts/default.aspx)
  + [Financials](https://investor.nationalfuelgas.com/financials/sec-filings/default.aspx)
    - [SEC Filings](https://investor.nationalfuelgas.com/financials/sec-filings/defa
```

### 2. 03/12/2026 — National Fuel Declares Quarterly Dividend and Reports Preliminary Voting Results from the Annual Meeting of Stockholders

URL: https://investor.nationalfuelgas.com/news-and-events/press-releases/press-releases-details/2026/National-Fuel-Declares-Quarterly-Dividend-and-Reports-Preliminary-Voting-Results-from-the-Annual-Meeting-of-Stockholders/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

* [Our Responsibility](https://www.nationalfuel.com/corporate/our-guiding-principles/)
* [Careers](https://www.nationalfuel.com/corporate/work-at-national-fuel/)
* [Investor Relations](https://investor.nationalfuelgas.com/)
* [Contact Us](https://www.nationalfuel.com/corporate/contact-us-directory/)

* [Our Company](https://www.nationalfuel.com/)
* [Utility Services](https://www.nationalfuel.com/utility/)
* [Business Partners](https://www.nationalfuel.com/business-partners/)
* [Pipeline & Storage](https://www.nationalfuel.com/pipeline-storage/)
* [Integrated Upstream & Gathering](https://www.nationalfuel.com/integrated-upstream-gathering/)

toggle main menu

* [Home](https://investor.nationalfuelgas.com/home/default.aspx)
  + [News & Events](https://investor.nationalfuelgas.com/news-and-events/press-releases/default.aspx)
    - [Press Releases](https://investor.nationalfuelgas.com/news-and-events/press-releases/default.aspx)
    - [Presentations](https://investor.nationalfuelgas.com/news-and-events/presentations/default.aspx)
    - [Events Calendar](https://investor.nationalfuelgas.com/news-and-events/events-calendar/default.aspx)
    - [Transcripts](https://investor.nationalfuelgas.com/news-and-events/transcripts/default.aspx)
  + [Financials](https://investor.nationalfuelgas.com/financials/sec-filings/default.aspx)
    - [SEC Filings](https://investor.nationalfuelgas.com/financials/sec-filings/defa
```

### 3. 04/09/2026 — National Fuel Schedules Second Quarter Fiscal 2026 Earnings Conference Call

URL: https://investor.nationalfuelgas.com/news-and-events/press-releases/press-releases-details/2026/National-Fuel-Schedules-Second-Quarter-Fiscal-2026-Earnings-Conference-Call/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

* [Our Responsibility](https://www.nationalfuel.com/corporate/our-guiding-principles/)
* [Careers](https://www.nationalfuel.com/corporate/work-at-national-fuel/)
* [Investor Relations](https://investor.nationalfuelgas.com/)
* [Contact Us](https://www.nationalfuel.com/corporate/contact-us-directory/)

* [Our Company](https://www.nationalfuel.com/)
* [Utility Services](https://www.nationalfuel.com/utility/)
* [Business Partners](https://www.nationalfuel.com/business-partners/)
* [Pipeline & Storage](https://www.nationalfuel.com/pipeline-storage/)
* [Integrated Upstream & Gathering](https://www.nationalfuel.com/integrated-upstream-gathering/)

toggle main menu

* [Home](https://investor.nationalfuelgas.com/home/default.aspx)
  + [News & Events](https://investor.nationalfuelgas.com/news-and-events/press-releases/default.aspx)
    - [Press Releases](https://investor.nationalfuelgas.com/news-and-events/press-releases/default.aspx)
    - [Presentations](https://investor.nationalfuelgas.com/news-and-events/presentations/default.aspx)
    - [Events Calendar](https://investor.nationalfuelgas.com/news-and-events/events-calendar/default.aspx)
    - [Transcripts](https://investor.nationalfuelgas.com/news-and-events/transcripts/default.aspx)
  + [Financials](https://investor.nationalfuelgas.com/financials/sec-filings/default.aspx)
    - [SEC Filings](https://investor.nationalfuelgas.com/financials/sec-filings/defa
```


## Sinais / observações

- **3 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **5 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-12-03** matched `dividend` → Dividend declaration: _National Fuel Declares Quarterly Dividend and Reports Preliminary Voting Results_
- 📊 **Cross-check fundamentals**: RI tem 5 releases/relatórios — podemos auditar se ROE=0.20833, DY=0.026911469948943886 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
