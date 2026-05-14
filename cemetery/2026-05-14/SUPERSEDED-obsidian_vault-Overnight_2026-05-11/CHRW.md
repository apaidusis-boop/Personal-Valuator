# CHRW — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://investor.chrobinson.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=171.38999938964844
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.34838 · DY=0.014586615373726375 · P/E=34.764706
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 5.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.chrobinson.com/ | ✅ | 5.8s | 9,581 |
- Filings extraídos do RI: **3**
- Eventos calendário: **0**
- Apresentações/releases: **6**
- Audio/video: **4**
- Headers detectados (structure): **10**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| April 29, 2026 | 05/07/26C.H. Robinson Declares Quarterly Cash Dividend |
| April 29, 2026 | 04/29/26C.H. Robinson Reports 2026 First Quarter Results |
| April 29, 2026 | 04/07/26C.H. Robinson First Quarter 2026 Earnings Release and Conference Call Sc |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (6 total, top 6)

- [Presentations](https://investor.chrobinson.com/News-and-Events/Presentations/default.aspx)
- [Press Release](https://investor.chrobinson.com//s21.q4cdn.com/950981335/files/doc_financials/2026/q1/Q1-2026-Earnings-Release.pdf)
- [Presentation](https://investor.chrobinson.com//s21.q4cdn.com/950981335/files/doc_financials/2026/q1/Q1-2026-Earnings-Deck.pdf)
- [Presentation](https://investor.chrobinson.com//s21.q4cdn.com/950981335/files/doc_presentations/2024/Dec/12/Full_Presentation/CHRW-ID_Presentation-FINAL.pdf)
- [Q1 2026 Press Release](https://s21.q4cdn.com/950981335/files/doc_financials/2026/q1/Q1-2026-Earnings-Release.pdf)
- [Q1 2026 Presentation](https://s21.q4cdn.com/950981335/files/doc_financials/2026/q1/Q1-2026-Earnings-Deck.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast](https://events.q4inc.com/attendee/156877459)
- [C.H. Robinson Q1 2026 Earnings Conference Call](https://investor.chrobinson.com/News-and-Events/Events/Events-details/2026/CH-Robinson-Q1-2026-Earnings-Conference-Call/default.aspx)
- [Webcast](https://event.webcasts.com/starthere.jsp?ei=1754361&tp_key=292dec8c43&tp_special=8)
- [Webcast](https://event.summitcast.com/view/VSr8zRPFYu9jT7Rm69ptdC/GF5zNibHvnDwGLWrKkpJ2Y)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 6 | + |
| Audio/video acessível | 0 (era cego) | 4 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **4 fontes audio/video** disponíveis (markitdown pode transcrever)
- **6 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **4 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 6 releases/relatórios — podemos auditar se ROE=0.34838, DY=0.014586615373726375 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
