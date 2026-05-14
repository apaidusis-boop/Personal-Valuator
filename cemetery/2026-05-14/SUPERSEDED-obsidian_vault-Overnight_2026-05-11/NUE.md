# NUE — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://investors.nucor.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=227.5
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.12285 · DY=0.009758241758241758 · P/E=22.569445
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.0s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.nucor.com/ | ✅ | 12.0s | 13,381 |
- Filings extraídos do RI: **9**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **3**
- Headers detectados (structure): **18**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 04/27/2026 | All News |
| 04/27/2026 | Nucor Reports Results for the First Quarter of 2026 |
| 04/14/2026 | Nucor Invites You to Join Its First Quarter of 2026 Conference Call on the Web |
| 03/19/2026 | Nucor Announces Guidance for the First Quarter of 2026 Earnings |
| 03/03/2026 | Nucor Executive Vice President Dan Needham to Retire |
| 04/27/2026 | Q1 2026 Earnings Call Presentation |
| 04/28/2026 | Nucor's First Quarter of 2026 Earnings Call |
| 01/27/2026 | Nucor's Fourth Quarter of 2025 Earnings Call |
| 10/28/2025 | Nucor's Third Quarter of 2025 Earnings Call |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Events & Presentations](https://investors.nucor.com/events-and-presentations/default.aspx)
- [ESG Related Documents](https://nucor.com/esg)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://events.q4inc.com/attendee/129924537)
- [Webcast(opens in new window)](https://events.q4inc.com/attendee/409388477)
- [Webcast(opens in new window)](https://events.q4inc.com/attendee/302160378)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 9 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 3 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**9 filings detectados como novos vs DB.**

### 1. 04/28/2026 — Nucor's First Quarter of 2026 Earnings Call

URL: https://investors.nucor.com/events-and-presentations/events/event-details/2026/Nucors-First-Quarter-of-2026-Earnings-Call/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

* [IR Home](https://investors.nucor.com/overview/default.aspx)
  + [COMPANY OVERVIEW](https://investors.nucor.com/why-invest/default.aspx)
  + [News](https://investors.nucor.com/news/default.aspx)
  + [Events & Presentations](https://investors.nucor.com/events-and-presentations/default.aspx)
  + [Financials](https://investors.nucor.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://investors.nucor.com/financials/quarterly-results/default.aspx)
    - [Annual Reports](https://investors.nucor.com/financials/annual-reports/default.aspx)
    - [Financial and Operating Statistics](https://icrm.indigotools.com/IR/IAC/?Ticker=NUE&Exchange=NYSE)
    - [SEC Filings](https://investors.nucor.com/financials/sec-filings/default.aspx)
  + [Leadership & ESG](https://investors.nucor.com/esg/default.aspx)
    - [Executive Team](https://nucor.com/leadership)
    - [Board of Directors](https://nucor.com/leadership#board-of-directors)
    - [ESG Related Documents](https://nucor.com/esg)
  + [Resources](https://investors.nucor.com/resources/investor-faqs/default.aspx)
    - [Investor FAQs](https://investors.nucor.com/resources/investor-faqs/default.aspx)
    - [Information Request Form](https://investors.nucor.com/resources/information-request-form/default.aspx)
    - [Investor Email Alerts](https://investors.nucor.com/resources/investor-email-alerts/default.aspx)
    - [Stock Quote](https://investors.nucor.com/resources/Stock-Qu
```

### 2. 04/27/2026 — All News

URL: https://investors.nucor.com/news/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

* [IR Home](https://investors.nucor.com/overview/default.aspx)
  + [COMPANY OVERVIEW](https://investors.nucor.com/why-invest/default.aspx)
  + [News](https://investors.nucor.com/news/default.aspx)
  + [Events & Presentations](https://investors.nucor.com/events-and-presentations/default.aspx)
  + [Financials](https://investors.nucor.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://investors.nucor.com/financials/quarterly-results/default.aspx)
    - [Annual Reports](https://investors.nucor.com/financials/annual-reports/default.aspx)
    - [Financial and Operating Statistics](https://icrm.indigotools.com/IR/IAC/?Ticker=NUE&Exchange=NYSE)
    - [SEC Filings](https://investors.nucor.com/financials/sec-filings/default.aspx)
  + [Leadership & ESG](https://investors.nucor.com/esg/default.aspx)
    - [Executive Team](https://nucor.com/leadership)
    - [Board of Directors](https://nucor.com/leadership#board-of-directors)
    - [ESG Related Documents](https://nucor.com/esg)
  + [Resources](https://investors.nucor.com/resources/investor-faqs/default.aspx)
    - [Investor FAQs](https://investors.nucor.com/resources/investor-faqs/default.aspx)
    - [Information Request Form](https://investors.nucor.com/resources/information-request-form/default.aspx)
    - [Investor Email Alerts](https://investors.nucor.com/resources/investor-email-alerts/default.aspx)
    - [Stock Quote](https://investors.nucor.com/resources/Stock-Qu
```

### 3. 04/27/2026 — Nucor Reports Results for the First Quarter of 2026

URL: https://investors.nucor.com/news/news-details/2026/Nucor-Reports-Results-for-the-First-Quarter-of-2026/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

* [IR Home](https://investors.nucor.com/overview/default.aspx)
  + [COMPANY OVERVIEW](https://investors.nucor.com/why-invest/default.aspx)
  + [News](https://investors.nucor.com/news/default.aspx)
  + [Events & Presentations](https://investors.nucor.com/events-and-presentations/default.aspx)
  + [Financials](https://investors.nucor.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://investors.nucor.com/financials/quarterly-results/default.aspx)
    - [Annual Reports](https://investors.nucor.com/financials/annual-reports/default.aspx)
    - [Financial and Operating Statistics](https://icrm.indigotools.com/IR/IAC/?Ticker=NUE&Exchange=NYSE)
    - [SEC Filings](https://investors.nucor.com/financials/sec-filings/default.aspx)
  + [Leadership & ESG](https://investors.nucor.com/esg/default.aspx)
    - [Executive Team](https://nucor.com/leadership)
    - [Board of Directors](https://nucor.com/leadership#board-of-directors)
    - [ESG Related Documents](https://nucor.com/esg)
  + [Resources](https://investors.nucor.com/resources/investor-faqs/default.aspx)
    - [Investor FAQs](https://investors.nucor.com/resources/investor-faqs/default.aspx)
    - [Information Request Form](https://investors.nucor.com/resources/information-request-form/default.aspx)
    - [Investor Email Alerts](https://investors.nucor.com/resources/investor-email-alerts/default.aspx)
    - [Stock Quote](https://investors.nucor.com/resources/Stock-Qu
```

### 4. 04/27/2026 — Q1 2026 Earnings Call Presentation

URL: https://s202.q4cdn.com/531038915/files/doc_financials/2026/q1/v2/Q1-2026-Earnings-Call-Presentation.pdf
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
FIRST QUARTER 2026
EARNINGS CALL
Leon Topalian
Chair and CEO
Steve Laxton
President and COO
Jack Sullivan
CFO
April 28, 2026

FORWARD-LOOKING STATEMENTS
Certain statements made in this presentation may constitute forward-looking statements within the meaning of the Private
Securities Litigation Reform Act of 1995. These statements involve risks and uncertainties. The words “anticipate,” “believe,”
“expect,” “intend,” “may,” “project,” “will,” “should,” “could” and similar expressions are intended to identify forward-looking
statements. These forward-looking statements reflect the Company’s best judgment based on current information, and
although we base these statements on circumstances that we believe to be reasonable when made, there can be no
assurance that future events will not affect the accuracy of such forward-looking information. The Company does not
undertake any obligation to update these statements. The forward-looking statements are not guarantees of future
performance, and actual results may vary materially from the projected results and expectations discussed in this
presentation. Factors that might cause the Company’s actual results to differ materially from those anticipated in forward-
looking statements include, but are not limited to: (1) competitive pressure on sales and pricing, including pressure from
imports and substitute materials; (2) U.S. and foreign trade policies affecting steel imports or exports; (3) the sensitivity of the
results of our operat
```

### 5. 01/27/2026 — Nucor's Fourth Quarter of 2025 Earnings Call

URL: https://investors.nucor.com/events-and-presentations/events/event-details/2026/Nucors-Fourth-Quarter-2025-Earnings-Call/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

* [IR Home](https://investors.nucor.com/overview/default.aspx)
  + [COMPANY OVERVIEW](https://investors.nucor.com/why-invest/default.aspx)
  + [News](https://investors.nucor.com/news/default.aspx)
  + [Events & Presentations](https://investors.nucor.com/events-and-presentations/default.aspx)
  + [Financials](https://investors.nucor.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://investors.nucor.com/financials/quarterly-results/default.aspx)
    - [Annual Reports](https://investors.nucor.com/financials/annual-reports/default.aspx)
    - [Financial and Operating Statistics](https://icrm.indigotools.com/IR/IAC/?Ticker=NUE&Exchange=NYSE)
    - [SEC Filings](https://investors.nucor.com/financials/sec-filings/default.aspx)
  + [Leadership & ESG](https://investors.nucor.com/esg/default.aspx)
    - [Executive Team](https://nucor.com/leadership)
    - [Board of Directors](https://nucor.com/leadership#board-of-directors)
    - [ESG Related Documents](https://nucor.com/esg)
  + [Resources](https://investors.nucor.com/resources/investor-faqs/default.aspx)
    - [Investor FAQs](https://investors.nucor.com/resources/investor-faqs/default.aspx)
    - [Information Request Form](https://investors.nucor.com/resources/information-request-form/default.aspx)
    - [Investor Email Alerts](https://investors.nucor.com/resources/investor-email-alerts/default.aspx)
    - [Stock Quote](https://investors.nucor.com/resources/Stock-Qu
```


## Sinais / observações

- **9 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **3 fontes audio/video** disponíveis (markitdown pode transcrever)
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-19-03** matched `guidance` → Update guidance — material para preço: _Nucor Announces Guidance for the First Quarter of 2026 Earnings_
- 🎙️ **3 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.12285, DY=0.009758241758241758 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
