# TFC — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://ir.truist.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **117**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=49.11000061035156
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.08579001 · DY=0.04235389888310388 · P/E=12.155941
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.02,5.07,9.01 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-23 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-04-17 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-16 | proxy | sec | DEF 14A |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 16.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ir.truist.com/ | ✅ | 16.8s | 5,368 |
- Filings extraídos do RI: **4**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **0**
- Headers detectados (structure): **11**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 2026-04-28 | Truist declares common and preferred stock dividends |
| 2026-04-17 | Truist reports first quarter 2026 results |
| 2026-03-18 | Truist announces first quarter 2026 earnings call details |
| 2026-03-12 | Truist expands open banking capabilities with Plaid |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Events & Presentations](https://ir.truist.com/events-and-presentation)
- [Fixed Income Presentation](https://ir.truist.com/image/2Q25_fixed_income.pdf)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 117 | 117 + 4 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**4 filings detectados como novos vs DB.**

### 1. 2026-04-28 — Truist declares common and preferred stock dividends

URL: https://ir.truist.com/2026-04-28-Truist-declares-common-and-preferred-stock-dividends
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
![](https://imaginativeastute.com/816715.png)

[Skip to main content](#wd_main_content)

## Header

[![Truist Logo](images/truist-logo.svg)
 Homepage](index.php)

Menu

* [Home](index.php)
* [Financial Information](sec-filings)

  [Annual Report & Proxy Statement](https://ir.truist.com/annual-reports)
  [Earnings](https://ir.truist.com/earnings)
  [Regulatory Disclosures](https://ir.truist.com/regulatory-disclosures)
  [SEC Filings](https://ir.truist.com/sec-filings)
  [Legacy Documents](https://ir.truist.com/legacy-documents)
* [Events & Presentations](https://ir.truist.com/events-and-presentation)
* [Shareholder Information](shareholder-information)

  [Shareholder Information](https://ir.truist.com/shareholder-information)
  [Dividend & Stock Split History](https://ir.truist.com/dividend-and-stock-split)
  [Stock Price Information](https://ir.truist.com/stock-price-information)
  [Investor Alerts](https://ir.truist.com/investor-alerts)
  [Analyst Coverage](https://ir.truist.com/analyst-coverage)
* [Fixed Income](credit-ratings)

  [Credit Ratings](https://ir.truist.com/credit-ratings)
  [Preferred Stock](https://ir.truist.com/preferred-stock)
  [Fixed Income Presentation](https://ir.truist.com/image/2Q25_fixed_income.pdf)
* [Governance & Responsibility](board-of-directors)

  [Corporate Governance](https://ir.truist.com/corporate-governance)
  [Board of Directors](https://ir.truist.com/board-of-directors)
  [Board Committees](https://ir.truist.com/Board-Committees)
  [Oper
```

### 2. 2026-04-17 — Truist reports first quarter 2026 results

URL: https://ir.truist.com/2026-04-17-Truist-reports-first-quarter-2026-results
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
![](https://imaginativeastute.com/816715.png)

[Skip to main content](#wd_main_content)

## Header

[![Truist Logo](images/truist-logo.svg)
 Homepage](index.php)

Menu

* [Home](index.php)
* [Financial Information](sec-filings)

  [Annual Report & Proxy Statement](https://ir.truist.com/annual-reports)
  [Earnings](https://ir.truist.com/earnings)
  [Regulatory Disclosures](https://ir.truist.com/regulatory-disclosures)
  [SEC Filings](https://ir.truist.com/sec-filings)
  [Legacy Documents](https://ir.truist.com/legacy-documents)
* [Events & Presentations](https://ir.truist.com/events-and-presentation)
* [Shareholder Information](shareholder-information)

  [Shareholder Information](https://ir.truist.com/shareholder-information)
  [Dividend & Stock Split History](https://ir.truist.com/dividend-and-stock-split)
  [Stock Price Information](https://ir.truist.com/stock-price-information)
  [Investor Alerts](https://ir.truist.com/investor-alerts)
  [Analyst Coverage](https://ir.truist.com/analyst-coverage)
* [Fixed Income](credit-ratings)

  [Credit Ratings](https://ir.truist.com/credit-ratings)
  [Preferred Stock](https://ir.truist.com/preferred-stock)
  [Fixed Income Presentation](https://ir.truist.com/image/2Q25_fixed_income.pdf)
* [Governance & Responsibility](board-of-directors)

  [Corporate Governance](https://ir.truist.com/corporate-governance)
  [Board of Directors](https://ir.truist.com/board-of-directors)
  [Board Committees](https://ir.truist.com/Board-Committees)
  [Oper
```

### 3. 2026-03-18 — Truist announces first quarter 2026 earnings call details

URL: https://ir.truist.com/2026-03-18-Truist-announces-first-quarter-2026-earnings-call-details
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
![](https://imaginativeastute.com/816715.png)

[Skip to main content](#wd_main_content)

## Header

[![Truist Logo](images/truist-logo.svg)
 Homepage](index.php)

Menu

* [Home](index.php)
* [Financial Information](sec-filings)

  [Annual Report & Proxy Statement](https://ir.truist.com/annual-reports)
  [Earnings](https://ir.truist.com/earnings)
  [Regulatory Disclosures](https://ir.truist.com/regulatory-disclosures)
  [SEC Filings](https://ir.truist.com/sec-filings)
  [Legacy Documents](https://ir.truist.com/legacy-documents)
* [Events & Presentations](https://ir.truist.com/events-and-presentation)
* [Shareholder Information](shareholder-information)

  [Shareholder Information](https://ir.truist.com/shareholder-information)
  [Dividend & Stock Split History](https://ir.truist.com/dividend-and-stock-split)
  [Stock Price Information](https://ir.truist.com/stock-price-information)
  [Investor Alerts](https://ir.truist.com/investor-alerts)
  [Analyst Coverage](https://ir.truist.com/analyst-coverage)
* [Fixed Income](credit-ratings)

  [Credit Ratings](https://ir.truist.com/credit-ratings)
  [Preferred Stock](https://ir.truist.com/preferred-stock)
  [Fixed Income Presentation](https://ir.truist.com/image/2Q25_fixed_income.pdf)
* [Governance & Responsibility](board-of-directors)

  [Corporate Governance](https://ir.truist.com/corporate-governance)
  [Board of Directors](https://ir.truist.com/board-of-directors)
  [Board Committees](https://ir.truist.com/Board-Committees)
  [Oper
```

### 4. 2026-03-12 — Truist expands open banking capabilities with Plaid

URL: https://ir.truist.com/2026-03-12-Truist-expands-open-banking-capabilities-with-Plaid
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
![](https://imaginativeastute.com/816715.png)

[Skip to main content](#wd_main_content)

## Header

[![Truist Logo](images/truist-logo.svg)
 Homepage](index.php)

Menu

* [Home](index.php)
* [Financial Information](sec-filings)

  [Annual Report & Proxy Statement](https://ir.truist.com/annual-reports)
  [Earnings](https://ir.truist.com/earnings)
  [Regulatory Disclosures](https://ir.truist.com/regulatory-disclosures)
  [SEC Filings](https://ir.truist.com/sec-filings)
  [Legacy Documents](https://ir.truist.com/legacy-documents)
* [Events & Presentations](https://ir.truist.com/events-and-presentation)
* [Shareholder Information](shareholder-information)

  [Shareholder Information](https://ir.truist.com/shareholder-information)
  [Dividend & Stock Split History](https://ir.truist.com/dividend-and-stock-split)
  [Stock Price Information](https://ir.truist.com/stock-price-information)
  [Investor Alerts](https://ir.truist.com/investor-alerts)
  [Analyst Coverage](https://ir.truist.com/analyst-coverage)
* [Fixed Income](credit-ratings)

  [Credit Ratings](https://ir.truist.com/credit-ratings)
  [Preferred Stock](https://ir.truist.com/preferred-stock)
  [Fixed Income Presentation](https://ir.truist.com/image/2Q25_fixed_income.pdf)
* [Governance & Responsibility](board-of-directors)

  [Corporate Governance](https://ir.truist.com/corporate-governance)
  [Board of Directors](https://ir.truist.com/board-of-directors)
  [Board Committees](https://ir.truist.com/Board-Committees)
  [Oper
```


## Sinais / observações

- **4 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-04-28** matched `dividend` → Dividend declaration: _Truist declares common and preferred stock dividends_
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.08579001, DY=0.04235389888310388 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
