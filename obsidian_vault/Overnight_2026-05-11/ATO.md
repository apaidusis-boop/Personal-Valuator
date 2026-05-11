# ATO — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://investors.atmosenergy.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=180.8699951171875
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.096 · DY=0.020677835467274804 · P/E=22.27463
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 9.7s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.atmosenergy.com/ | ✅ | 9.7s | 13,840 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **2**
- Headers detectados (structure): **21**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 06, 2026 | Atmos Energy Corporation Reports Earnings for Fiscal 2026 Second Quarter; Raises |
| May 06, 2026 | Atmos Energy Declares Regular Quarterly Dividend |
| May 7, 2026 | Atmos Energy Corporation to Host Fiscal 2026 Second Quarter Earnings Conference  |
| 05/07/2026 | Second Quarter Earnings Conference Call |
| 02/04/2026 | First Quarter Earnings Conference Call |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Events & Presentations](https://www.investors.atmosenergy.com/events-and-presentations/default.aspx)
- [Download PDF(opens in new window)](https://s201.q4cdn.com/158157484/files/doc_financials/2026/q2/ATO-2Q26-Earnings-Presentation.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://events.q4inc.com/attendee/269105194)
- [Webcast(opens in new window)](https://events.q4inc.com/attendee/349622805)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 2 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**2 filings detectados como novos vs DB.**

### 1. 05/07/2026 — Second Quarter Earnings Conference Call

URL: https://investors.atmosenergy.com/events-and-presentations/events/event-details/2026/Second-Quarter-Earnings-Conference-Call/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

* [Overview](https://www.investors.atmosenergy.com/overview/default.aspx)
  + [Why Invest](https://www.investors.atmosenergy.com/why-invest/default.aspx)
  + [News](https://www.investors.atmosenergy.com/news/default.aspx)
  + [Events & Presentations](https://www.investors.atmosenergy.com/events-and-presentations/default.aspx)
  + [Stock Info](https://www.investors.atmosenergy.com/stock-info/default.aspx)
    - [Stock Quote](/stock-info/default.aspx#stock-quote)
    - [Stock Chart](/stock-info/default.aspx#stock-chart)
    - [Historical Stock Quote](/stock-info/default.aspx#stock-historical)
    - [Investment Calculator](/stock-info/default.aspx#calculator)
    - [Dividend History](https://www.investors.atmosenergy.com/stock-info/dividend-history/default.aspx)
    - [Analyst Coverage](https://www.investors.atmosenergy.com/stock-info/analyst-coverage/default.aspx)
  + [Financials](https://www.investors.atmosenergy.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://www.investors.atmosenergy.com/financials/quarterly-results/default.aspx)
    - [Annual Reports](https://www.investors.atmosenergy.com/financials/annual-reports/default.aspx)
    - [SEC Filings](https://www.investors.atmosenergy.com/financials/sec-filings/default.aspx)
    - [Additional Information](https://www.investors.atmosenergy.com/financials/Additional-Information/default.aspx)
    - [Kansas Securitization](
```

### 2. 02/04/2026 — First Quarter Earnings Conference Call

URL: https://investors.atmosenergy.com/events-and-presentations/events/event-details/2026/First-Quarter-Earnings-Conference-Call/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

[Skip to main content](#maincontent)

* [Overview](https://www.investors.atmosenergy.com/overview/default.aspx)
  + [Why Invest](https://www.investors.atmosenergy.com/why-invest/default.aspx)
  + [News](https://www.investors.atmosenergy.com/news/default.aspx)
  + [Events & Presentations](https://www.investors.atmosenergy.com/events-and-presentations/default.aspx)
  + [Stock Info](https://www.investors.atmosenergy.com/stock-info/default.aspx)
    - [Stock Quote](/stock-info/default.aspx#stock-quote)
    - [Stock Chart](/stock-info/default.aspx#stock-chart)
    - [Historical Stock Quote](/stock-info/default.aspx#stock-historical)
    - [Investment Calculator](/stock-info/default.aspx#calculator)
    - [Dividend History](https://www.investors.atmosenergy.com/stock-info/dividend-history/default.aspx)
    - [Analyst Coverage](https://www.investors.atmosenergy.com/stock-info/analyst-coverage/default.aspx)
  + [Financials](https://www.investors.atmosenergy.com/financials/quarterly-results/default.aspx)
    - [Quarterly Results](https://www.investors.atmosenergy.com/financials/quarterly-results/default.aspx)
    - [Annual Reports](https://www.investors.atmosenergy.com/financials/annual-reports/default.aspx)
    - [SEC Filings](https://www.investors.atmosenergy.com/financials/sec-filings/default.aspx)
    - [Additional Information](https://www.investors.atmosenergy.com/financials/Additional-Information/default.aspx)
    - [Kansas Securitization](
```


## Sinais / observações

- **2 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.096, DY=0.020677835467274804 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
