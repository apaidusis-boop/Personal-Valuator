# ADM — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://investors.adm.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=77.66000366210938
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.047659997 · DY=0.02639711438746948 · P/E=34.669643
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.7s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.adm.com/ | ✅ | 11.7s | 14,105 |
- Filings extraídos do RI: **3**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **0**
- Headers detectados (structure): **24**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 05/06/2026 | ADM Declares Cash Dividend |
| 05/05/2026 | ADM Reports First Quarter 2026 Results |
| May 5, 2026 | ADM to Release First Quarter Financial Results on May 5, 2026 |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Events & Presentations](https://investors.adm.com/events-and-presentations/default.aspx)
- [Read our latest Corporate Sustainability Report](https://www.adm.com/globalassets/sustainability/sustainability-reports/archer_daniels_2024_corporate_sustainability_report.pdf)
- [2025 Regenerative Agriculture Report](https://investors.adm.com//s1.q4cdn.com/365366812/files/doc_presentations/2026/01/adm_regen-ag-report-2025_final.pdf)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 2 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**2 filings detectados como novos vs DB.**

### 1. 05/06/2026 — ADM Declares Cash Dividend

URL: https://investors.adm.com/news/news-details/2026/ADM-Declares-Cash-Dividend/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

[![Archer Daniels Midland Company logo](//s1.q4cdn.com/365366812/files/design/logo.svg)](https://www.adm.com/)

* [Home](https://investors.adm.com/home/default.aspx)
  + [Overview](https://investors.adm.com/home/default.aspx)
  + [Governance](https://investors.adm.com/governance/board-of-directors/default.aspx)
    - [Board of Directors](https://investors.adm.com/governance/board-of-directors/default.aspx)
    - [Board Committees](https://investors.adm.com/governance/board-committees/default.aspx)
    - [Governance Documents](https://investors.adm.com/governance/corporate-governance/default.aspx)
  + [Events & Presentations](https://investors.adm.com/events-and-presentations/default.aspx)
  + [News](https://investors.adm.com/news/default.aspx)
  + [Stock Information](https://investors.adm.com/stock-information/default.aspx)
    - [Stock Quote](/stock-information/default.aspx#stock-quote)
    - [Stock Chart](/stock-information/default.aspx#stock-chart)
    - [Historical Stock Quote](/stock-information/default.aspx#stock-historical)
    - [Investment Calculator](/stock-information/default.aspx#calculator)
    - [Stockholder Information](/stock-information/default.aspx#stockholder-information)
    - [Analyst Coverage](https://investors.adm.com/stock-information/analyst-coverage/default.aspx)
  + [Financials](https://investors.adm.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](h
```

### 2. 05/05/2026 — ADM Reports First Quarter 2026 Results

URL: https://investors.adm.com/news/news-details/2026/ADM-Reports-First-Quarter-2026-Results/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

[![Archer Daniels Midland Company logo](//s1.q4cdn.com/365366812/files/design/logo.svg)](https://www.adm.com/)

* [Home](https://investors.adm.com/home/default.aspx)
  + [Overview](https://investors.adm.com/home/default.aspx)
  + [Governance](https://investors.adm.com/governance/board-of-directors/default.aspx)
    - [Board of Directors](https://investors.adm.com/governance/board-of-directors/default.aspx)
    - [Board Committees](https://investors.adm.com/governance/board-committees/default.aspx)
    - [Governance Documents](https://investors.adm.com/governance/corporate-governance/default.aspx)
  + [Events & Presentations](https://investors.adm.com/events-and-presentations/default.aspx)
  + [News](https://investors.adm.com/news/default.aspx)
  + [Stock Information](https://investors.adm.com/stock-information/default.aspx)
    - [Stock Quote](/stock-information/default.aspx#stock-quote)
    - [Stock Chart](/stock-information/default.aspx#stock-chart)
    - [Historical Stock Quote](/stock-information/default.aspx#stock-historical)
    - [Investment Calculator](/stock-information/default.aspx#calculator)
    - [Stockholder Information](/stock-information/default.aspx#stockholder-information)
    - [Analyst Coverage](https://investors.adm.com/stock-information/analyst-coverage/default.aspx)
  + [Financials](https://investors.adm.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](h
```


## Sinais / observações

- **2 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-06-05** matched `dividend` → Dividend declaration: _ADM Declares Cash Dividend_
- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.047659997, DY=0.02639711438746948 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
