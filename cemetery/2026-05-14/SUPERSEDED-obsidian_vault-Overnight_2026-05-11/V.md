# V — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investor.visa.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **228**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=318.7900085449219
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.60349 · DY=0.007904890154814553 · P/E=27.769165
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-29 | 10-Q | sec | 10-Q |
| 2026-04-28 | 8-K | sec | 8-K \| 2.02,8.01,9.01 |
| 2026-02-27 | 8-K | sec | 8-K \| 8.01 |
| 2026-02-13 | 8-K | sec | 8-K \| 7.01 |
| 2026-02-12 | 8-K | sec | 8-K \| 8.01,9.01 |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 9.7s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.visa.com/ | ✅ | 9.7s | 23,978 |
- Filings extraídos do RI: **4**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **1**
- Headers detectados (structure): **20**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 04/28/2026 | Q2 2026 Visa Earnings Conference Call |
| 01/29/2026 | Q1 2026 Visa Earnings Conference Call |
| 10/28/2025 | Q4 and Full-Year 2025 Visa Earnings Conference Call |
| May 5, 2026 | Visa to Participate in Upcoming Investor Conferences |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Investor Relations](https://investor.visa.com/investor-relations/default.aspx)
- [Investor Relations](http://investor.visa.com/)

### Audio / Video disponível (markitdown pode ler)

- [Listen to webcast](https://events.q4inc.com/attendee/111708618)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 228 | 228 + 3 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**3 filings detectados como novos vs DB.**

### 1. 01/29/2026 — Q1 2026 Visa Earnings Conference Call

URL: https://investor.visa.com/events-calendar/Event-Details/2026/Q1-2026-Visa-Earnings-Conference-Call/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Investor Relations](https://investor.visa.com/investor-relations/default.aspx)> [Events Calendar](https://investor.visa.com/events-calendar/default.aspx)> Event Details

* [News](https://investor.visa.com/news/default.aspx)
* [Stock Information](https://investor.visa.com/stock-information/quote-chart/default.aspx)
  + [Dividends](https://investor.visa.com/stock-information/dividends/default.aspx)
  + [Analyst Coverage](https://investor.visa.com/stock-information/analyst-coverage/default.aspx)
  + [Class B/C Stock Info](https://investor.visa.com/stock-information/class-b-c-stock-info/default.aspx)
  + [Preferred Stock Info](https://investor.visa.com/stock-information/Preferred-Stock/default.aspx)
  + [Quote & Chart](https://investor.visa.com/stock-information/quote-chart/default.aspx)
* [Financial Information](https://investor.visa.com/financial-information/quarterly-earnings/default.aspx)
  + [Quarterly Earnings](https://investor.visa.com/financial-information/quarterly-earnings/default.aspx)
  + [Fixed Income](https://investor.visa.com/financial-information/Fixed-Income/default.aspx)
* [Corporate Governance](https://investor.visa.com/corporate-governance/default.aspx)
  + [Management Team](https://investor.visa.com/corporate-governance/management-team/default.aspx)
  + [Board of Directors](https://investor.visa.com/corporate-governance/board-of-directors/default.aspx)
  + [Committee Composition](https://investor.visa.com/corporate-gove
```

### 2. 04/28/2026 — Q2 2026 Visa Earnings Conference Call

URL: https://investor.visa.com/events-calendar/Event-Details/2026/Q2-2026-Visa-Earnings-Conference-Call/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Investor Relations](https://investor.visa.com/investor-relations/default.aspx)> [Events Calendar](https://investor.visa.com/events-calendar/default.aspx)> Event Details

* [News](https://investor.visa.com/news/default.aspx)
* [Stock Information](https://investor.visa.com/stock-information/quote-chart/default.aspx)
  + [Dividends](https://investor.visa.com/stock-information/dividends/default.aspx)
  + [Analyst Coverage](https://investor.visa.com/stock-information/analyst-coverage/default.aspx)
  + [Class B/C Stock Info](https://investor.visa.com/stock-information/class-b-c-stock-info/default.aspx)
  + [Preferred Stock Info](https://investor.visa.com/stock-information/Preferred-Stock/default.aspx)
  + [Quote & Chart](https://investor.visa.com/stock-information/quote-chart/default.aspx)
* [Financial Information](https://investor.visa.com/financial-information/quarterly-earnings/default.aspx)
  + [Quarterly Earnings](https://investor.visa.com/financial-information/quarterly-earnings/default.aspx)
  + [Fixed Income](https://investor.visa.com/financial-information/Fixed-Income/default.aspx)
* [Corporate Governance](https://investor.visa.com/corporate-governance/default.aspx)
  + [Management Team](https://investor.visa.com/corporate-governance/management-team/default.aspx)
  + [Board of Directors](https://investor.visa.com/corporate-governance/board-of-directors/default.aspx)
  + [Committee Composition](https://investor.visa.com/corporate-gove
```

### 3. 10/28/2025 — Q4 and Full-Year 2025 Visa Earnings Conference Call

URL: https://investor.visa.com/events-calendar/Event-Details/2025/Q4-and-Full-Year-2025-Visa-Earnings-Conference-Call/default.aspx
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Investor Relations](https://investor.visa.com/investor-relations/default.aspx)> [Events Calendar](https://investor.visa.com/events-calendar/default.aspx)> Event Details

* [News](https://investor.visa.com/news/default.aspx)
* [Stock Information](https://investor.visa.com/stock-information/quote-chart/default.aspx)
  + [Dividends](https://investor.visa.com/stock-information/dividends/default.aspx)
  + [Analyst Coverage](https://investor.visa.com/stock-information/analyst-coverage/default.aspx)
  + [Class B/C Stock Info](https://investor.visa.com/stock-information/class-b-c-stock-info/default.aspx)
  + [Preferred Stock Info](https://investor.visa.com/stock-information/Preferred-Stock/default.aspx)
  + [Quote & Chart](https://investor.visa.com/stock-information/quote-chart/default.aspx)
* [Financial Information](https://investor.visa.com/financial-information/quarterly-earnings/default.aspx)
  + [Quarterly Earnings](https://investor.visa.com/financial-information/quarterly-earnings/default.aspx)
  + [Fixed Income](https://investor.visa.com/financial-information/Fixed-Income/default.aspx)
* [Corporate Governance](https://investor.visa.com/corporate-governance/default.aspx)
  + [Management Team](https://investor.visa.com/corporate-governance/management-team/default.aspx)
  + [Board of Directors](https://investor.visa.com/corporate-governance/board-of-directors/default.aspx)
  + [Committee Composition](https://investor.visa.com/corporate-gove
```


## Sinais / observações

- **3 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.60349, DY=0.007904890154814553 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
