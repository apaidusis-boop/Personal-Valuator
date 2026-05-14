# XOM — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Energy
- **RI URLs scraped** (1):
  - https://investor.exxonmobil.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=144.57000732421875
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.09873 · DY=0.027944938751643878 · P/E=24.338385
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 5.5s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.exxonmobil.com/ | ✅ | 5.5s | 21,989 |
- Filings extraídos do RI: **3**
- Eventos calendário: **0**
- Apresentações/releases: **7**
- Audio/video: **2**
- Headers detectados (structure): **43**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| April 16, 2026 | View press release |
| March 10, 2026 | View press release |
| February 17, 2026 | View press release |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (7 total, top 7)

- [Events and presentations](https://investor.exxonmobil.com/news-events)
- [Events and presentations](https://investor.exxonmobil.com/news-events/ir-calendar)
- [Investor Presentation](https://investor.exxonmobil.com/news-events/investor-presentation)
- [Factors affecting future results](https://d1io3yog0oux5.cloudfront.net/_049f4bfce466226b8dbc5ba1fa8aa005/exxonmobil/files/553890/2024_FAFRs_-_Final.pdf)
- [Transcript](https://d1io3yog0oux5.cloudfront.net/_b406718d47f3d06e5bf884007e928789/exxonmobil/db/2288/22639/webcast_transcript/ExxonMobil%2B1Q26%2BEarnings%2BTranscript.pdf)
- [Presentation](https://d1io3yog0oux5.cloudfront.net/_b406718d47f3d06e5bf884007e928789/exxonmobil/db/2288/22639/presentation/1Q26%2BEarnings%2Bpresentation.pdf)
- [Supplement](https://d1io3yog0oux5.cloudfront.net/_b406718d47f3d06e5bf884007e928789/exxonmobil/db/2288/22639/supplement/1Q26%2BSupplement%2BWebsite.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast Replay](https://event.webcasts.com/starthere.jsp?ei=1743195&tp_key=6eb72ee1e7)
- [Webcast](https://event.webcasts.com/starthere.jsp?ei=1757821&tp_key=a161f92d44)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 7 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **7 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 7 releases/relatórios — podemos auditar se ROE=0.09873, DY=0.027944938751643878 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
