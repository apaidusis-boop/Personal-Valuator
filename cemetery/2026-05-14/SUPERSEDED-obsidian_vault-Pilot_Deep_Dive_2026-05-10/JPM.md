# JPM — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Bank
- **RI URLs scraped** (3):
  - https://www.jpmorganchase.com/ir
  - https://www.jpmorganchase.com/ir/news
  - https://www.jpmorganchase.com/ir/quarterly-earnings
- **Pilot rationale**: Large US corporate IR (multi-page)

## Antes (estado da DB)

**Posição activa**: qty=7.0 · entry=306.55571428571426 · date=2025-09-25

- Total events na DB: **28**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=302.1000061035156
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.16465001 · DY=0.019529956573315476 · P/E=14.468391
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-07 | 8-K | sec | 8-K \| 3.03,5.03,8.01,9.01 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-24 | 8-K | sec | 8-K \| 5.03 |
| 2026-04-23 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-04-14 | 8-K | sec | 8-K \| 2.02,9.01 |

## Agora (RI scrape live)

- Scrape: ✅ **3/3 URLs OK** · total 0.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.jpmorganchase.com/ir | ✅ | 0.1s | 23,741 |
| https://www.jpmorganchase.com/ir/news | ✅ | 0.1s | 15,838 |
| https://www.jpmorganchase.com/ir/quarterly-earnings | ✅ | 0.1s | 75,973 |
- Filings extraídos do RI: **15**
- Eventos calendário: **0**
- Apresentações/releases: **312**
- Audio/video: **16**
- Headers detectados (structure): **91**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 19, 2026 | Press release |
| May 27, 2026 | Press release |
| Jul 14, 2026 | Press release |
| 2026-04-27 | JPMorganChase to Present at the Bernstein Strategic Decisions Conference |
| 2026-04-15 | JPMorganChase 2026 Annual Meeting of Shareholders |
| 2026-04-15 | JPMorganChase Declares Preferred Stock Dividends |
| 2026-03-17 | JPMorganChase Declares Common Stock Dividend |
| 2026-03-17 | JPMorganChase to Host First-Quarter 2026 Earnings Call |
| 2026-03-13 | JPMorganChase Declares Preferred Stock Dividends |
| 2026-03-04 | JPMorganChase Announces Conference Calls to Review First-Quarter, Second-Quarter |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (312 total, top 12)

- [Investor Relations](https://www.jpmorganchase.com/ir)
- [Events and presentations](https://www.jpmorganchase.com/ir/events)
- [2025 Complete Annual Report](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/annualreport-2025.pdf)
- [Consolidated financial statements and Notes and Supplementary information](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/audited-financial-statements-2025.pdf)
- [2026 Proxy Supplemental Presentation](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/2026-proxy-supplement.pdf)
- [Response to Glass Lewis Report](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/gl-response-letter2026.pdf)
- [Response to ISS Report](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/iss-response-letter-2026.pdf)
- [1Q26 Earnings Press Release](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2026/1st-quarter/a5fd2d13-877b-43b2-8b58-81bad4399c87.pdf)
- [1Q26 Earnings Presentation](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2026/1st-quarter/ba305358-f754-4f76-a59d-5278b3bcf99a.pdf)
- [1Q26 Earnings Supplement](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2026/1st-quarter/ea70ca6c-a0d5-4596-94f5-52f1722cd704.pdf)
- [1Q26 Earnings Supplement (xls)](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2026/1st-quarter/1q26-earnings-supplement.xlsx)
- [1Q26 Earnings Transcript](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2026/1st-quarter/1q26-earnings-transcript.pdf)
- _… e mais 300 no MD raw (`data/portal_cache/`)_

### Audio / Video disponível (markitdown pode ler)

- [1Q26 Conference Call](https://event.webcasts.com/starthere.jsp?ei=1755596&tp_key=bcddbd4b9b&tp_special=8)
- [4Q25 Conference Call](https://event.webcasts.com/starthere.jsp?ei=1746461&tp_key=a6439a82cd&tp_special=8)
- [3Q25 Conference Call](https://event.webcasts.com/starthere.jsp?ei=1735121&tp_key=7976a418ef&tp_special=8)
- [2Q25 Conference Call](https://event.webcasts.com/starthere.jsp?ei=1723895&tp_key=4ff3289e48&tp_special=8)
- [1Q25 Conference Call](https://event.webcasts.com/starthere.jsp?ei=1711813&tp_key=a937c13dcb&tp_special=8)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 28 | 28 + 12 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 312 | + |
| Audio/video acessível | 0 (era cego) | 16 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**12 filings detectados como novos vs DB.**

### 1. 2026-04-27 — JPMorganChase to Present at the Bernstein Strategic Decisions Conference

URL: https://www.jpmorganchase.com/ir/news/2026/jpmorganchase-to-present-at-the-bernstein-strategic-decisions-conference
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main)

[![JPMorganChase logo](/content/dam/jpmorganchase/images/logos/jpmc-logo.svg)](/)

[Join our team](https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions)

Search JPMorganChase

* About us

  + ### [About us](/about)

  + ### [How we do business](/about/business-principles)

  + ### [Leadership](/about/leadership)

  + ### [Awards and recognition](/about/awards-and-recognition)

  + ### [Technology](/about/technology)

  + ### [Governance](/about/governance)

  + ### [Suppliers](/about/suppliers)

  + ### [Diversity, opportunity & inclusion](/about/diversity-opportunity-and-inclusion)

  Read more

  ![](/content/dam/jpmorganchase/images/ir/ceo-letters/2025/chairman-and-ceo/dimon-1440x810.jpg)

  Chairman and CEO Letter to Shareholders

  Annual Report 2025

  [Learn more](/ir/annual-report/2025/ar-ceo-letters)
* Impact

  + ### [Impact](/impact)
  + [Business growth and entrepreneurship](/impact/business-growth-and-entrepreneurship)
  + [Careers and skills](/impact/careers-and-skills)
  + [Community development](/impact/community-development)
  + [Environmental sustainability](/impact/environmental-sustainability)
  + [Financial health and wealth creation](/impact/financial-health-wealth-creation)

  Latest news

  ![](/content/dam/jpmorganchase/images/newsroom/stories/fire-dex-jpmcr-banner.jpg)

  An Ohio-based company is protecting first responders around the world

  With support from JPMorganChase, Fire-Dex 
```

### 2. 2026-04-15 — JPMorganChase 2026 Annual Meeting of Shareholders

URL: https://www.jpmorganchase.com/ir/news/2026/jpmc-2026-annual-meeting-of-shareholders
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main)

[![JPMorganChase logo](/content/dam/jpmorganchase/images/logos/jpmc-logo.svg)](/)

[Join our team](https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions)

Search JPMorganChase

* About us

  + ### [About us](/about)

  + ### [How we do business](/about/business-principles)

  + ### [Leadership](/about/leadership)

  + ### [Awards and recognition](/about/awards-and-recognition)

  + ### [Technology](/about/technology)

  + ### [Governance](/about/governance)

  + ### [Suppliers](/about/suppliers)

  + ### [Diversity, opportunity & inclusion](/about/diversity-opportunity-and-inclusion)

  Read more

  ![](/content/dam/jpmorganchase/images/ir/ceo-letters/2025/chairman-and-ceo/dimon-1440x810.jpg)

  Chairman and CEO Letter to Shareholders

  Annual Report 2025

  [Learn more](/ir/annual-report/2025/ar-ceo-letters)
* Impact

  + ### [Impact](/impact)
  + [Business growth and entrepreneurship](/impact/business-growth-and-entrepreneurship)
  + [Careers and skills](/impact/careers-and-skills)
  + [Community development](/impact/community-development)
  + [Environmental sustainability](/impact/environmental-sustainability)
  + [Financial health and wealth creation](/impact/financial-health-wealth-creation)

  Latest news

  ![](/content/dam/jpmorganchase/images/newsroom/stories/fire-dex-jpmcr-banner.jpg)

  An Ohio-based company is protecting first responders around the world

  With support from JPMorganChase, Fire-Dex 
```

### 3. 2026-04-15 — JPMorganChase Declares Preferred Stock Dividends

URL: https://www.jpmorganchase.com/ir/news/2026/jpmc-declares-preferred-stock-dividends-4-15
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main)

[![JPMorganChase logo](/content/dam/jpmorganchase/images/logos/jpmc-logo.svg)](/)

[Join our team](https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions)

Search JPMorganChase

* About us

  + ### [About us](/about)

  + ### [How we do business](/about/business-principles)

  + ### [Leadership](/about/leadership)

  + ### [Awards and recognition](/about/awards-and-recognition)

  + ### [Technology](/about/technology)

  + ### [Governance](/about/governance)

  + ### [Suppliers](/about/suppliers)

  + ### [Diversity, opportunity & inclusion](/about/diversity-opportunity-and-inclusion)

  Read more

  ![](/content/dam/jpmorganchase/images/ir/ceo-letters/2025/chairman-and-ceo/dimon-1440x810.jpg)

  Chairman and CEO Letter to Shareholders

  Annual Report 2025

  [Learn more](/ir/annual-report/2025/ar-ceo-letters)
* Impact

  + ### [Impact](/impact)
  + [Business growth and entrepreneurship](/impact/business-growth-and-entrepreneurship)
  + [Careers and skills](/impact/careers-and-skills)
  + [Community development](/impact/community-development)
  + [Environmental sustainability](/impact/environmental-sustainability)
  + [Financial health and wealth creation](/impact/financial-health-wealth-creation)

  Latest news

  ![](/content/dam/jpmorganchase/images/newsroom/stories/fire-dex-jpmcr-banner.jpg)

  An Ohio-based company is protecting first responders around the world

  With support from JPMorganChase, Fire-Dex 
```

### 4. 2026-03-17 — JPMorganChase Declares Common Stock Dividend

URL: https://www.jpmorganchase.com/ir/news/2026/jpmc-declares-common-stock-dividend-3-17
Após data máxima DB: (título não match em DB)

### 5. 2026-03-17 — JPMorganChase to Host First-Quarter 2026 Earnings Call

URL: https://www.jpmorganchase.com/ir/news/2026/jpmc-to-host-first-quarter-2026-earnings-call
Após data máxima DB: (título não match em DB)


## Sinais / observações

- **12 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **16 fontes audio/video** disponíveis (markitdown pode transcrever)
- **312 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-04-15** matched `dividend` → Dividend declaration: _JPMorganChase Declares Preferred Stock Dividends_
- 🚨 **2026-03-17** matched `dividend` → Dividend declaration: _JPMorganChase Declares Common Stock Dividend_
- 🚨 **2026-03-13** matched `dividend` → Dividend declaration: _JPMorganChase Declares Preferred Stock Dividends_
- 🚨 **2026-02-13** matched `dividend` → Dividend declaration: _JPMorganChase Declares Preferred Stock Dividends_
- 🎙️ **16 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 💼 **Posição activa**: qty=7.0, entry=306.55571428571426. 12 filings novos → revisitar tese se houver signal material acima.
- 📊 **Cross-check fundamentals**: RI tem 312 releases/relatórios — podemos auditar se ROE=0.16465001, DY=0.019529956573315476 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
