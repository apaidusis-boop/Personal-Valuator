# PEP — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://investor.pepsico.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **211**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=154.6199951171875
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.43879002 · DY=0.03681283262029595 · P/E=24.273155
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 8-K | sec | 8-K \| 5.07 |
| 2026-04-16 | 10-Q | sec | 10-Q |
| 2026-04-16 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-27 | proxy | sec | DEF 14A |
| 2026-02-11 | 8-K | sec | 8-K \| 8.01,9.01 |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 3.6s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.pepsico.com/ | ✅ | 3.6s | 24,894 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **4**
- Audio/video: **7**
- Headers detectados (structure): **53**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (4 total, top 4)

- [Events & Presentations](https://www.pepsico.com/investors/events-presentations)
- [Transcript – Pre-Recorded Management Discussion](https://investor.pepsico.com/docs/pepsico-5v9wci20/media/Files/investors/q3-2020-transcript-pre-recorded-management-discussion.pdf)
- [Transcript – Pre-Recorded Management Discussion](https://investor.pepsico.com/docs/pepsico-5v9wci20/media/Files/investors/q2-2020-transcript-pre-recorded-management-discussion.pdf)
- [Transcript – Pre-Recorded Management Discussion](https://investor.pepsico.com/docs/pepsico-5v9wci20/media/Files/investors/q1-2020-transcript-pre-recorded-management-discussion.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast - Investors Q&A](https://edge.media-server.com/mmc/p/fgn5nuso/)
- [Webcast - Investors Q&A](https://edge.media-server.com/mmc/p/bk9s3ib8/)
- [Webcast - Investors Q&A](https://edge.media-server.com/mmc/p/x43xtvfm/)
- [Webcast - Investors Q&A](https://edge.media-server.com/mmc/p/g82fc56t)
- [Webcast - Investors Q&A](https://edge.media-server.com/mmc/p/u5hzyuur/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 211 | 211 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 4 | + |
| Audio/video acessível | 0 (era cego) | 7 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **7 fontes audio/video** disponíveis (markitdown pode transcrever)
- **4 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **7 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 4 releases/relatórios — podemos auditar se ROE=0.43879002, DY=0.03681283262029595 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
