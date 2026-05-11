# FUL — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://investors.hbfuller.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=61.25
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.083179995 · DY=0.015510204081632652 · P/E=21.193771
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.0s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.hbfuller.com/ | ✅ | 12.0s | 24,810 |
- Filings extraídos do RI: **6**
- Eventos calendário: **0**
- Apresentações/releases: **4**
- Audio/video: **2**
- Headers detectados (structure): **36**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 06, 2026 | H.B. Fuller Announces Aerospace Manufacturing Center of Excellence |
| April 16, 2026 | H.B. Fuller Increases Quarterly Dividend by 4.3 Percent |
| March 25, 2026 | H.B. Fuller Reports First Quarter 2026 Results |
| March 26, 2026 | H.B. Fuller Q1 2026 Earnings Conference Call |
| January 15, 2026 | H.B. Fuller Q4 2025 Earnings Conference Call |
| 03-25-2026 | Earnings Release (PDF)(opens in new window) |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (4 total, top 4)

- [Events & Presentations](https://investors.hbfuller.com/events-and-presentations/default.aspx)
- [Presentations](https://investors.hbfuller.com/events-and-presentations/presentations/default.aspx)
- [Download PDF(opens in new window)](https://s26.q4cdn.com/617714526/files/doc_financials/2026/q1/2026-Q1-Earnings-Presentation-3-24-2026.pdf)
- [Transcript(opens in new window)](https://s26.q4cdn.com/617714526/files/doc_financials/2026/q1/FUL-USQ_Transcript_2026-03-26-1.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://events.q4inc.com/attendee/622880009)
- [Webcast(opens in new window)](https://events.q4inc.com/attendee/293325089)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 1 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 4 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**1 filings detectados como novos vs DB.**

### 1. 03-25-2026 — Earnings Release (PDF)(opens in new window)

URL: https://s26.q4cdn.com/617714526/files/doc_financials/2026/q1/v2/2026-Q1-Earnings-Release-03-25-2026-FINAL-V2.pdf
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
`cGross
Worldwide Headquarters Scott Jensen
1200 Willow Lake Boulevard Investor Relations Contact
St. Paul, Minnesota 55110-5101 investors@hbfuller.com
NEWS
March 25, 2026
H.B. Fuller Reports First Quarter 2026 Results
Reported EPS (diluted) of $0.38; Adjusted EPS (diluted) of $0.57, up 6% year-on-year
Net income of $21 million; Adjusted EBITDA of $119 million, up 4% year-on-year
Adjusted EBITDA margin of 15.4%, up 90 basis points year-on-year
Increases full-year revenue, adjusted EBITDA, and adjusted EPS guidance
ST. PAUL, Minn. – H.B. Fuller Company (NYSE: FUL) today reported financial results for its first quarter that
ended February 28, 2026.
First Quarter 2026 Noteworthy Items:
▪ Net revenue was $771 million; organic revenue was down 6.6% year-on-year;
▪ Gross margin was 30.6%; adjusted gross margin of 31.3% increased 170 basis points year-on-year driven by
restructuring savings from Quantum Leap, the impact of acquisitions, and targeted price and raw material cost
actions;
▪ Net income was $21 million; adjusted EBITDA was $119 million, up 4% versus last year, with pricing and raw
material cost actions more than offsetting the impact of lower volumes;
▪ Adjusted EBITDA margin was 15.4%, up 90 basis points year-on-year;
▪ Reported EPS (diluted) was $0.38; adjusted EPS (diluted) was $0.57, up 6% year-on-year, driven by higher
adjusted net income and lower shares outstanding.
Summary of First Quarter 2026 Results:
The Company’s net revenue for the first quarter of fiscal 20
```


## Sinais / observações

- **1 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **4 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 4 releases/relatórios — podemos auditar se ROE=0.083179995, DY=0.015510204081632652 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
