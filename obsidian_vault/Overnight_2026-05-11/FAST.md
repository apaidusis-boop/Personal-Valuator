# FAST — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://investor.fastenal.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=44.16999816894531
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.33842 · DY=0.020828617571617337 · P/E=39.088493
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.3s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.fastenal.com/ | ✅ | 11.3s | 13,082 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **0**
- Headers detectados (structure): **17**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 05/06/2026 | April 2026 Sales Information (opens in new window) |
| 04/13/2026 | Fastenal Company Reports 2026 First Quarter Earnings |
| 04/13/2026 | Q1 2026 Investor Teleconference Presentation (opens in new window) |
| 06/04/2026 | May 2026 Sales Release |
| 08/06/2026 | July 2026 Sales Release |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Events & Presentations](https://investor.fastenal.com/events-and-presentations/default.aspx)
- [Tax Reporting Info](https://investor.fastenal.com//s23.q4cdn.com/591718779/files/doc_downloads/gov_documents/Fastenal_Form-8937_May2025-Final.pdf)
- [Conflict Minerals Report](https://investor.fastenal.com//s23.q4cdn.com/591718779/files/doc_downloads/2025/05/Exhibit-1-01-Conflict-Minerals-Report-2024-5-14-R5_no-Footers.pdf)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 5 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**5 filings detectados como novos vs DB.**

### 1. 04/13/2026 — Fastenal Company Reports 2026 First Quarter Earnings

URL: https://investor.fastenal.com/news-releases/news-details/2026/Fastenal-Company-Reports-2026-First-Quarter-Earnings/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

[![Fastenal Company](//s23.q4cdn.com/591718779/files/design/fastenal-logo.png)](https://www.fastenal.com/)

* [Investor Overview](https://investor.fastenal.com/investor-overview/default.aspx)
  + [News Releases](https://investor.fastenal.com/news-releases/default.aspx)
  + [Events & Presentations](https://investor.fastenal.com/events-and-presentations/default.aspx)
  + [Stock Info](https://investor.fastenal.com/stock-info/default.aspx)
    - [Stock Quote](/stock-info/default.aspx#stock-quote)
    - [Stock Chart](/stock-info/default.aspx#stock-chart)
    - [Historical Stock Quote](/stock-info/default.aspx#stock-historical)
    - [Investment Calculator](/stock-info/default.aspx#calculator)
    - [Dividend History](https://investor.fastenal.com/stock-info/dividend-history/default.aspx)
    - [Analyst Coverage](https://investor.fastenal.com/stock-info/analyst-coverage/default.aspx)
    - [Tax Reporting Info](//s23.q4cdn.com/591718779/files/doc_downloads/gov_documents/Fastenal_Form-8937_May2025-Final.pdf)
  + [Financial Results](https://investor.fastenal.com/financial-results/quarterly-results/default.aspx)
    - [Quarterly Results](https://investor.fastenal.com/financial-results/quarterly-results/default.aspx)
    - [Annual Reports](https://investor.fastenal.com/financial-results/annual-reports/default.aspx)
    - [SEC Filings](https://investor.fastenal.com/financial-results/sec-filings/default.aspx)
  +
```

### 2. 04/13/2026 — Q1 2026 Investor Teleconference Presentation (opens in new window)

URL: https://investor.fastenal.com/files/doc_financials/2026/Q1/Q1-2026-Investor-Presentation-R7-Milestone-April-10-0204-pm.pdf
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
2026

First Quarter

Investor
Teleconference
April 13, 2026

1

  Safe Harbor Statement

All statements made herein that are not historical facts (e.g., future operating results, net sales growth,
long-term share gains, and business activity, as well as expectations regarding operations, including
gross and operating income margin, eBusiness DSR sales growth, weighted FMI technology signings,
operating  costs  (including  SG&A),  capital  expenditures,  sales  through  our  digital  footprint,  cash  flow
generation,  our  anticipated  progress  on  our  strategic  objectives,  our  ability  to  grow  large  customer
sites  and  sales,  the  declaration  and  payment  of  dividends  and  any  future  share  repurchases,  the
impact  of  tariffs  and  any  pricing  actions)  are  "forward-looking  statements"  within  the  meaning  of  the
Private Securities Litigation Reform Act of 1995. Such statements involve known and unknown risks,
uncertainties,  and  other  factors  that  may  cause  actual  results  to  differ  materially.  More  information
regarding  such  risks  can  be  found  in  the  most  recent  annual  and  quarterly  reports  of  Fastenal
Company  (the  'Company,'  'Fastenal,'  'we,'  'our,'  or  'us')  filed  with  the  Securities  and  Exchange
Commission. Any numerical or other representations in this presentation do not represent guidance by
management  and  should  not  be  construed  as  such.  The  appendix  to  the  following  presentation
includes  
```

### 3. 08/06/2026 — July 2026 Sales Release

URL: https://investor.fastenal.com/events-and-presentations/event-details/2026/July-2026-Sales-Release/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

[![Fastenal Company](//s23.q4cdn.com/591718779/files/design/fastenal-logo.png)](https://www.fastenal.com/)

* [Investor Overview](https://investor.fastenal.com/investor-overview/default.aspx)
  + [News Releases](https://investor.fastenal.com/news-releases/default.aspx)
  + [Events & Presentations](https://investor.fastenal.com/events-and-presentations/default.aspx)
  + [Stock Info](https://investor.fastenal.com/stock-info/default.aspx)
    - [Stock Quote](/stock-info/default.aspx#stock-quote)
    - [Stock Chart](/stock-info/default.aspx#stock-chart)
    - [Historical Stock Quote](/stock-info/default.aspx#stock-historical)
    - [Investment Calculator](/stock-info/default.aspx#calculator)
    - [Dividend History](https://investor.fastenal.com/stock-info/dividend-history/default.aspx)
    - [Analyst Coverage](https://investor.fastenal.com/stock-info/analyst-coverage/default.aspx)
    - [Tax Reporting Info](//s23.q4cdn.com/591718779/files/doc_downloads/gov_documents/Fastenal_Form-8937_May2025-Final.pdf)
  + [Financial Results](https://investor.fastenal.com/financial-results/quarterly-results/default.aspx)
    - [Quarterly Results](https://investor.fastenal.com/financial-results/quarterly-results/default.aspx)
    - [Annual Reports](https://investor.fastenal.com/financial-results/annual-reports/default.aspx)
    - [SEC Filings](https://investor.fastenal.com/financial-results/sec-filings/default.aspx)
  +
```

### 4. 05/06/2026 — April 2026 Sales Information (opens in new window)

URL: https://investor.fastenal.com/files/doc_financials/2026/Q2/04-2026-sales-numbers-v3.pdf
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
APRIL 2026 INFORMATION WEB RELEASE
Release date: 5/6/26
Fastenal Company and Subsidiaries
| (Dollar amounts in thousands) | 2026 | 2025 | Change |     |     |
| ----------------------------- | ---- | ---- | ------ | --- | --- |
Daily sales - Net sales divided by the number of business
| Net sales | $790,483 | $691,674 | 14.3% |     |     |
| --------- | -------- | -------- | ----- | --- | --- |
days in the US.
| Business days                   | 22      | 22      | 0.0%  |     |     |
| ------------------------------- | ------- | ------- | ----- | --- | --- |
| Daily sales                     | $35,931 | $31,440 | 14.3% |     |     |
| Impact of currency fluctuations | 0.3%    | (0.0%)  |       |     |     |
Historical
Historical figures are an average from 2021 - 2025.
| Daily sales in January                 | $33,194 | 29,647  |      |     |     |
| -------------------------------------- | ------- | ------- | ---- | --- | --- |
|    Change in daily sales since January | 8.2%    | 6.0%    | 3.3% |     |     |
| Daily sales last month                 | $36,093 | $32,384 |      |     |     |
   Change in daily sales since last month (0.4%) (2.9%) (1.6%)
Current Month
| Daily sales growth by geography |     |     | % of Sales |     |     |
| ------------------------------- | --- | --- | ---------- | --- | --- |
Calculated using US days and US dollars.
| United States | 13.2% | 7.0%  | 82.9% |     |     |
| ------------- | ----- | ----- | ----- | --- | --- |
| Canada/Mexico | 1
```

### 5. 06/04/2026 — May 2026 Sales Release

URL: https://investor.fastenal.com/events-and-presentations/event-details/2026/May-2026-Sales-Release/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

[![Fastenal Company](//s23.q4cdn.com/591718779/files/design/fastenal-logo.png)](https://www.fastenal.com/)

* [Investor Overview](https://investor.fastenal.com/investor-overview/default.aspx)
  + [News Releases](https://investor.fastenal.com/news-releases/default.aspx)
  + [Events & Presentations](https://investor.fastenal.com/events-and-presentations/default.aspx)
  + [Stock Info](https://investor.fastenal.com/stock-info/default.aspx)
    - [Stock Quote](/stock-info/default.aspx#stock-quote)
    - [Stock Chart](/stock-info/default.aspx#stock-chart)
    - [Historical Stock Quote](/stock-info/default.aspx#stock-historical)
    - [Investment Calculator](/stock-info/default.aspx#calculator)
    - [Dividend History](https://investor.fastenal.com/stock-info/dividend-history/default.aspx)
    - [Analyst Coverage](https://investor.fastenal.com/stock-info/analyst-coverage/default.aspx)
    - [Tax Reporting Info](//s23.q4cdn.com/591718779/files/doc_downloads/gov_documents/Fastenal_Form-8937_May2025-Final.pdf)
  + [Financial Results](https://investor.fastenal.com/financial-results/quarterly-results/default.aspx)
    - [Quarterly Results](https://investor.fastenal.com/financial-results/quarterly-results/default.aspx)
    - [Annual Reports](https://investor.fastenal.com/financial-results/annual-reports/default.aspx)
    - [SEC Filings](https://investor.fastenal.com/financial-results/sec-filings/default.aspx)
  +
```


## Sinais / observações

- **5 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.33842, DY=0.020828617571617337 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
