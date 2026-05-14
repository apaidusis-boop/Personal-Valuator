# SPGI — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investor.spglobal.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=420.1199951171875
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.13939999 · DY=0.00916404847364165 · P/E=26.589872
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 32.6s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.spglobal.com/ | ✅ | 32.6s | 23,640 |
- Filings extraídos do RI: **4**
- Eventos calendário: **0**
- Apresentações/releases: **14**
- Audio/video: **1**
- Headers detectados (structure): **31**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 05/08/2026 | S&P Global Announces Public Filing of Form 10 Registration Statement for Planned |
| May 5, 2026 | S&P Global to Present at the Barclays 18th Annual Americas Select Conference on  |
| 2026-05-12 | S&P Global’s First Quarter 2026 Earnings Announcement / Conference Call on April |
| 2026-08-05 | -8.56](/stock-dividends/stock-quote/) |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (14 total, top 12)

- [Investor Relations Overview](https://investor.spglobal.com/investor-relations-overview/default.aspx)
- [Investor Presentations](https://investor.spglobal.com/investor-presentations/default.aspx)
- [Related Reports & Policies](https://investor.spglobal.com/corporate-governance/related-reports-policies/default.aspx)
- [Contact Investor Relations](https://investor.spglobal.com/contact-investor-relations/contact-ir/default.aspx)
- [Investor Relations Overview](https://investor.spglobal.com/investor-relations-overview)
- [Presentations](https://investor.spglobal.com/investor-presentations)
- [Investor Relations Overview](https://investor.spglobal.com/investor-relations-overview/default.aspx%20%20)
- [Investor Presentations](https://investor.spglobal.com/investor-presentations/default.aspx%20%20)
- [Contact Investor Relations](https://investor.spglobal.com/contact-investor-relations/contact-ir/)
- [Investor Presentations](https://investor.spglobal.com/investor-presentations/)
- [Earnings Release PDF](https://s29.q4cdn.com/690959130/files/doc_financials/2026/q1/S-P-Global-1Q-2026-Earnings-Release-Exhibits-4-28-2026.pdf)
- [Supplemental](https://s29.q4cdn.com/690959130/files/doc_financials/2026/q1/S-P-Global-1Q-2026-Earnings-Supplemental-Disclosure-4-28-2026.pdf)
- _… e mais 2 no MD raw (`data/portal_cache/`)_

### Audio / Video disponível (markitdown pode ler)

- [Webcast](https://events.q4inc.com/attendee/192322092)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 3 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 14 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**3 filings detectados como novos vs DB.**

### 1. 05/08/2026 — S&P Global Announces Public Filing of Form 10 Registration Statement for Planned Separation of Mobility Global

URL: https://investor.spglobal.com/news-releases/news-details/2026/SP-Global-Announces-Public-Filing-of-Form-10-Registration-Statement-for-Planned-Separation-of-Mobility-Global/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

Corporate
/en/index
content

* [IR Home](https://investor.spglobal.com/ir-home/default.aspx)
  + [Investor Relations Overview](https://investor.spglobal.com/investor-relations-overview/default.aspx)
  + [Investor Presentations](https://investor.spglobal.com/investor-presentations/default.aspx)
  + [Investor Fact Book](https://investor.spglobal.com/investor-fact-book/default.aspx)
  + [News Releases](https://investor.spglobal.com/news-releases/default.aspx)
  + [Quarterly Earnings & Monthly Metrics](https://investor.spglobal.com/quarterly-earnings/default.aspx)
  + [SEC Filings & Reports](https://investor.spglobal.com/sec-filings-reports/overview/default.aspx)
    - [Overview](https://investor.spglobal.com/sec-filings-reports/overview/default.aspx)
    - [10-Qs, 10-Ks & Other Filings](https://investor.spglobal.com/sec-filings-reports/10-qs-10-ks-other-filings/default.aspx)
    - [Annual Reports](https://investor.spglobal.com/sec-filings-reports/annual-reports/default.aspx)
    - [Proxy Statements](https://investor.spglobal.com/sec-filings-reports/proxy-statements/default.aspx)
  + [Our Leadership](/our-leadership/executive-committee)
    - [Executive Leadership Team](https://investor.spglobal.com/our-leadership/executive-committee/default.aspx)
    - [Special Advisors](https://investor.spglobal.com/our-leadership/special-advisors/default.aspx)
  + [Corporate Governance](https://investor.spglobal.com/corporate-governance/overview/default.a
```

### 2. 2026-08-05 — -8.56](/stock-dividends/stock-quote/)

URL: https://investor.spglobal.com/news-releases/news-details/2026/SP-Global-Announces-Board-of-Directors-for-Mobility-Global/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

Corporate
/en/index
content

* [IR Home](https://investor.spglobal.com/ir-home/default.aspx)
  + [Investor Relations Overview](https://investor.spglobal.com/investor-relations-overview/default.aspx)
  + [Investor Presentations](https://investor.spglobal.com/investor-presentations/default.aspx)
  + [Investor Fact Book](https://investor.spglobal.com/investor-fact-book/default.aspx)
  + [News Releases](https://investor.spglobal.com/news-releases/default.aspx)
  + [Quarterly Earnings & Monthly Metrics](https://investor.spglobal.com/quarterly-earnings/default.aspx)
  + [SEC Filings & Reports](https://investor.spglobal.com/sec-filings-reports/overview/default.aspx)
    - [Overview](https://investor.spglobal.com/sec-filings-reports/overview/default.aspx)
    - [10-Qs, 10-Ks & Other Filings](https://investor.spglobal.com/sec-filings-reports/10-qs-10-ks-other-filings/default.aspx)
    - [Annual Reports](https://investor.spglobal.com/sec-filings-reports/annual-reports/default.aspx)
    - [Proxy Statements](https://investor.spglobal.com/sec-filings-reports/proxy-statements/default.aspx)
  + [Our Leadership](/our-leadership/executive-committee)
    - [Executive Leadership Team](https://investor.spglobal.com/our-leadership/executive-committee/default.aspx)
    - [Special Advisors](https://investor.spglobal.com/our-leadership/special-advisors/default.aspx)
  + [Corporate Governance](https://investor.spglobal.com/corporate-governance/overview/default.a
```

### 3. 2026-05-12 — S&P Global’s First Quarter 2026 Earnings Announcement / Conference Call on April 28

URL: https://investor.spglobal.com/investor-presentations/event-details/2026/Earnings-Announcement--SP-Globals-First-Quarter-2026-Earnings-Conference-Call-and-Webcast
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

Corporate
/en/index
content

* [IR Home](https://investor.spglobal.com/ir-home/default.aspx)
  + [Investor Relations Overview](https://investor.spglobal.com/investor-relations-overview/default.aspx)
  + [Investor Presentations](https://investor.spglobal.com/investor-presentations/default.aspx)
  + [Investor Fact Book](https://investor.spglobal.com/investor-fact-book/default.aspx)
  + [News Releases](https://investor.spglobal.com/news-releases/default.aspx)
  + [Quarterly Earnings & Monthly Metrics](https://investor.spglobal.com/quarterly-earnings/default.aspx)
  + [SEC Filings & Reports](https://investor.spglobal.com/sec-filings-reports/overview/default.aspx)
    - [Overview](https://investor.spglobal.com/sec-filings-reports/overview/default.aspx)
    - [10-Qs, 10-Ks & Other Filings](https://investor.spglobal.com/sec-filings-reports/10-qs-10-ks-other-filings/default.aspx)
    - [Annual Reports](https://investor.spglobal.com/sec-filings-reports/annual-reports/default.aspx)
    - [Proxy Statements](https://investor.spglobal.com/sec-filings-reports/proxy-statements/default.aspx)
  + [Our Leadership](/our-leadership/executive-committee)
    - [Executive Leadership Team](https://investor.spglobal.com/our-leadership/executive-committee/default.aspx)
    - [Special Advisors](https://investor.spglobal.com/our-leadership/special-advisors/default.aspx)
  + [Corporate Governance](https://investor.spglobal.com/corporate-governance/overview/default.a
```


## Sinais / observações

- **3 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **14 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-08-05** matched `dividend` → Dividend declaration: _-8.56](/stock-dividends/stock-quote/)_
- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 14 releases/relatórios — podemos auditar se ROE=0.13939999, DY=0.00916404847364165 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
