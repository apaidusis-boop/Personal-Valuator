# AFL — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investors.aflac.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=113.0999984741211
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.16469 · DY=0.02077807278253601 · P/E=12.9257145
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 9.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.aflac.com/ | ✅ | 9.2s | 20,810 |
- Filings extraídos do RI: **4**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **5**
- Headers detectados (structure): **16**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 05/01/2026 | Aflac opens new South Portland office to support Maine Paid Family and Medical L |
| 04/29/2026 | Aflac Incorporated Announces First Quarter 2026 Results |
| 04/29/2026 | Aflac recognizes 6 leaders as Check for Cancer Champions |
| 08/06/2026 | Second quarter earnings release |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Events & Presentations](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
- [Presentations](https://investors.aflac.com/events-and-presentations/presentations/default.aspx)

### Audio / Video disponível (markitdown pode ler)

- [First quarter teleconference (webcast event)](https://investors.aflac.com/events-and-presentations/events-calendar/event-details/2026/First-quarter-teleconference-webcast-event/default.aspx)
- [Webcast (opens in new window)](https://events.q4inc.com/attendee/563301778)
- [Year-end teleconference (webcast event)](https://investors.aflac.com/events-and-presentations/events-calendar/event-details/2026/Year-end-teleconference-webcast-event/default.aspx)
- [Webcast (opens in new window)](https://events.q4inc.com/attendee/356672156)
- [Second quarter teleconference (webcast event)](https://investors.aflac.com/events-and-presentations/events-calendar/event-details/2026/Second-quarter-teleconference-webcast-event/default.aspx)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 4 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 5 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**4 filings detectados como novos vs DB.**

### 1. 04/29/2026 — Aflac Incorporated Announces First Quarter 2026 Results

URL: https://investors.aflac.com/press-releases/press-release-details/2026/Aflac-Incorporated-Announces-First-Quarter-2026-Results/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

High ContrastOFFON

[![AFLAC Incorporated logo](//s24.q4cdn.com/367535798/files/design/aflaclogo.png)](https://www.aflac.com/)

* [Home](https://investors.aflac.com/home/default.aspx)
  + [Financials](https://investors.aflac.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://investors.aflac.com/financials/quarterly-results/default.aspx)
    - [Annual Reports and Proxy](https://investors.aflac.com/financials/annual-reports-and-proxy/default.aspx)
    - [SEC Filings](https://investors.aflac.com/financials/sec-filings/default.aspx)
    - [Statutory Filings](https://investors.aflac.com/financials/statutory-filings/us-entities/default.aspx)
      * [US Entities](https://investors.aflac.com/financials/statutory-filings/us-entities/default.aspx)
    - [Investment Details](https://investors.aflac.com/financials/investment-details/default.aspx)
    - [Financial Analysts Briefings](https://investors.aflac.com/financials/Financial-Analysts-Briefings/default.aspx)
  + [Press Releases](https://investors.aflac.com/press-releases/default.aspx)
  + [Events & Presentations](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
    - [Events Calendar](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
    - [Presentations](https://investors.aflac.com/events-and-presentations/presentations/default.aspx)
  + [Sustainability](https
```

### 2. 04/29/2026 — Aflac recognizes 6 leaders as Check for Cancer Champions

URL: https://investors.aflac.com/press-releases/press-release-details/2026/Aflac-recognizes-6-leaders-as-Check-for-Cancer-Champions/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

High ContrastOFFON

[![AFLAC Incorporated logo](//s24.q4cdn.com/367535798/files/design/aflaclogo.png)](https://www.aflac.com/)

* [Home](https://investors.aflac.com/home/default.aspx)
  + [Financials](https://investors.aflac.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://investors.aflac.com/financials/quarterly-results/default.aspx)
    - [Annual Reports and Proxy](https://investors.aflac.com/financials/annual-reports-and-proxy/default.aspx)
    - [SEC Filings](https://investors.aflac.com/financials/sec-filings/default.aspx)
    - [Statutory Filings](https://investors.aflac.com/financials/statutory-filings/us-entities/default.aspx)
      * [US Entities](https://investors.aflac.com/financials/statutory-filings/us-entities/default.aspx)
    - [Investment Details](https://investors.aflac.com/financials/investment-details/default.aspx)
    - [Financial Analysts Briefings](https://investors.aflac.com/financials/Financial-Analysts-Briefings/default.aspx)
  + [Press Releases](https://investors.aflac.com/press-releases/default.aspx)
  + [Events & Presentations](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
    - [Events Calendar](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
    - [Presentations](https://investors.aflac.com/events-and-presentations/presentations/default.aspx)
  + [Sustainability](https
```

### 3. 08/06/2026 — Second quarter earnings release

URL: https://investors.aflac.com/events-and-presentations/events-calendar/event-details/2026/Second-quarter-earnings-release/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

High ContrastOFFON

[![AFLAC Incorporated logo](//s24.q4cdn.com/367535798/files/design/aflaclogo.png)](https://www.aflac.com/)

* [Home](https://investors.aflac.com/home/default.aspx)
  + [Financials](https://investors.aflac.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://investors.aflac.com/financials/quarterly-results/default.aspx)
    - [Annual Reports and Proxy](https://investors.aflac.com/financials/annual-reports-and-proxy/default.aspx)
    - [SEC Filings](https://investors.aflac.com/financials/sec-filings/default.aspx)
    - [Statutory Filings](https://investors.aflac.com/financials/statutory-filings/us-entities/default.aspx)
      * [US Entities](https://investors.aflac.com/financials/statutory-filings/us-entities/default.aspx)
    - [Investment Details](https://investors.aflac.com/financials/investment-details/default.aspx)
    - [Financial Analysts Briefings](https://investors.aflac.com/financials/Financial-Analysts-Briefings/default.aspx)
  + [Press Releases](https://investors.aflac.com/press-releases/default.aspx)
  + [Events & Presentations](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
    - [Events Calendar](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
    - [Presentations](https://investors.aflac.com/events-and-presentations/presentations/default.aspx)
  + [Sustainability](https
```

### 4. 05/01/2026 — Aflac opens new South Portland office to support Maine Paid Family and Medical Leave Progr...

URL: https://investors.aflac.com/press-releases/press-release-details/2026/Aflac-opens-new-South-Portland-office-to-support-Maine-Paid-Family-and-Medical-Leave-Program/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

High ContrastOFFON

[![AFLAC Incorporated logo](//s24.q4cdn.com/367535798/files/design/aflaclogo.png)](https://www.aflac.com/)

* [Home](https://investors.aflac.com/home/default.aspx)
  + [Financials](https://investors.aflac.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://investors.aflac.com/financials/quarterly-results/default.aspx)
    - [Annual Reports and Proxy](https://investors.aflac.com/financials/annual-reports-and-proxy/default.aspx)
    - [SEC Filings](https://investors.aflac.com/financials/sec-filings/default.aspx)
    - [Statutory Filings](https://investors.aflac.com/financials/statutory-filings/us-entities/default.aspx)
      * [US Entities](https://investors.aflac.com/financials/statutory-filings/us-entities/default.aspx)
    - [Investment Details](https://investors.aflac.com/financials/investment-details/default.aspx)
    - [Financial Analysts Briefings](https://investors.aflac.com/financials/Financial-Analysts-Briefings/default.aspx)
  + [Press Releases](https://investors.aflac.com/press-releases/default.aspx)
  + [Events & Presentations](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
    - [Events Calendar](https://investors.aflac.com/events-and-presentations/events-calendar/default.aspx)
    - [Presentations](https://investors.aflac.com/events-and-presentations/presentations/default.aspx)
  + [Sustainability](https
```


## Sinais / observações

- **4 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **5 fontes audio/video** disponíveis (markitdown pode transcrever)
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **5 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.16469, DY=0.02077807278253601 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
