# ITW — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://investor.itw.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=254.75999450683594
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.96848 · DY=0.02484691527903981 · P/E=23.632652
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 9.3s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.itw.com/ | ✅ | 9.3s | 13,630 |
- Filings extraídos do RI: **3**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **1**
- Headers detectados (structure): **6**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 05/08/2026 | ITW Board Of Directors Declares Quarterly Dividend |
| 04/30/2026 | ITW Reports First Quarter 2026 Results |
| 04/10/2026 | ITW Schedules First Quarter 2026 Earnings Webcast |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Events & Presentations](https://investor.itw.com/news-and-events/events-and-presentations/default.aspx)
- [PresentationView More(opens in new window)](https://s204.q4cdn.com/218186261/files/doc_financials/2026/q1/ITW-Slide-Presentation-Q1-2026-Earnings-Call.pdf)
- [Earnings ReleaseView More(opens in new window)](https://s204.q4cdn.com/218186261/files/doc_financials/2026/q1/ITW-Reports-First-Quarter-2026-Results.pdf)

### Audio / Video disponível (markitdown pode ler)

- [WebcastView More(opens in new window)](https://events.q4inc.com/attendee/502016216)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 3 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**3 filings detectados como novos vs DB.**

### 1. 04/30/2026 — ITW Reports First Quarter 2026 Results

URL: https://investor.itw.com/news-and-events/news/news-details/2026/ITW-Reports-First-Quarter-2026-Results/default.aspx
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
[Skip to main content](#main-content)

* [Overview](https://investor.itw.com/overview/default.aspx)
  + [Why Invest](https://investor.itw.com/why-invest/default.aspx)
  + [Financials](https://investor.itw.com/default.aspx)
    - [Earnings](https://investor.itw.com/financials/earnings/default.aspx)
    - [Annual Reports](https://investor.itw.com/financials/annual-reports/default.aspx)
    - [SEC Filings](https://investor.itw.com/financials/SEC-Filings/default.aspx)
  + [News & Events](https://investor.itw.com/news-and-events/default.aspx)
    - [News](https://investor.itw.com/news-and-events/news/default.aspx)
    - [Events & Presentations](https://investor.itw.com/news-and-events/events-and-presentations/default.aspx)
  + [Stock Info](https://investor.itw.com/stock-info/default.aspx)
    - [Stock Quote](/stock-info/default.aspx#stock-quote)
    - [Stock Chart](/stock-info/default.aspx#stock-chart)
    - [Historical Stock Quote](/stock-info/default.aspx#stock-historical)
    - [Investment Calculator](/stock-info/default.aspx#calculator)
    - [Dividend History](https://investor.itw.com/stock-info/dividend-history/default.aspx)
    - [Analyst Coverage](https://investor.itw.com/stock-info/analyst-coverage/default.aspx)
  + [Governance](https://investor.itw.com/governance/governance-documents/default.aspx)
    - [Governance Documents](https://investor.itw.com/governance/governance-documents/default.aspx)
    - [Leadership](https://www.itw.com/about-itw/leadership/)
    - [Board o
```

### 2. 04/10/2026 — ITW Schedules First Quarter 2026 Earnings Webcast

URL: https://investor.itw.com/files/doc_news/2026/Apr/10/ITW-Schedules-First-Quarter-2026-Earnings-Webcast.pdf
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
PRESS RELEASE

155 Harlem Avenue
Glenview, Illinois 60025

ITW SCHEDULES FIRST QUARTER 2026 EARNINGS WEBCAST

GLENVIEW, IL., April 10, 2026 - Illinois Tool Works Inc. (NYSE: ITW) will issue its first quarter 2026

results on Thursday, April 30, 2026, at 7:00 a.m. CDT. Following the release, ITW will hold its first quarter

2026 earnings webcast at 9:00 a.m. CDT.

To access the webcast for the event, please click on the following link:

ITW Q1 2026 Earnings Webcast

If you are a participant on the conference call, please dial 1-888-660-6652 (domestic) or 1-646-960-

0554 (international) 10 minutes prior to the 9:00 a.m. CDT start time. The passcode is “ITW.”

Following  the  webcast,  presentation  materials  and  an  audio  webcast  replay  will  be  available  at

http://investor.itw.com. An audio-only replay will be available from April 30 through May 7 by dialing 1-

800-770-2030 (domestic) or 1-609-800-9909 (international). The passcode is 2756156.

About Illinois Tool Works

ITW (NYSE: ITW) is a Fortune 300 global multi-industrial manufacturing leader with revenue of $16 billion in 2025. The company’s seven industry-

leading segments leverage the unique ITW Business Model to drive solid growth with best-in-class margins and returns in markets where highly

innovative, customer-focused solutions are required. ITW’s approximately 43,000 dedicated colleagues around the world thrive in the company’s

decentralized and entrepreneurial culture. www.itw.com.

Investor Relation
```

### 3. 05/08/2026 — ITW Board Of Directors Declares Quarterly Dividend

URL: https://investor.itw.com/files/doc_news/2026/May/ITW-Declares-Quarterly-Dividend-May-2026.pdf
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
PRESS RELEASE

155 Harlem Avenue
Glenview, Illinois 60025

ITW BOARD OF DIRECTORS DECLARES QUARTERLY DIVIDEND

GLENVIEW, IL., May 8, 2026 (GLOBE NEWSWIRE) – The Board of Directors of Illinois Tool Works Inc.

(NYSE:  ITW)  declared  a  dividend  on  the  company's  common  stock  of  $1.61  per  share  for  the  second

quarter of 2026. The dividend equates to $6.44 per share on a full-year basis. The dividend will be paid on

July 10, 2026 to shareholders of record as of June 30, 2026.

About Illinois Tool Works

ITW (NYSE: ITW) is a Fortune 300 global multi-industrial manufacturing leader with revenue of $16 billion in 2025. The company’s seven industry-leading

segments leverage the unique ITW Business  Model to drive solid growth with best-in-class margins  and returns in markets where highly innovative,

customer-focused solutions are required. ITW’s approximately 43,000 dedicated colleagues around the world thrive in the company’s decentralized and

entrepreneurial culture. www.itw.com.

Investor Relations & Media Contact:
Erin Linnihan
Tel: 224.661.7431
investorrelations@itw.com | mediarelations@itw.com


```


## Sinais / observações

- **3 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-08-05** matched `dividend` → Dividend declaration: _ITW Board Of Directors Declares Quarterly Dividend_
- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.96848, DY=0.02484691527903981 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
