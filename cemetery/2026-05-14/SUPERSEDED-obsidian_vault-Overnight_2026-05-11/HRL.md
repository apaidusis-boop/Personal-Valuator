# HRL — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://investor.hormelfoods.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=20.440000534057617
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.061160002 · DY=0.057045008294260215 · P/E=22.966293
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.hormelfoods.com/ | ✅ | 11.8s | 28,985 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **5**
- Audio/video: **2**
- Headers detectados (structure): **23**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 28, 2026 | Hormel Foods Corporation Second Quarter Earnings Conference Call |
| May 04, 2026 | Hormel Foods Corporation Announces Second Quarter Earnings Call |
| April 28, 2026 | Hormel Foods Announces 2026 Call for 10 Under 20 Food Heroes Nominations |
| April 24, 2026 | Hormel Foods Completes Sale of Whole-Bird Turkey Business to Life-Science Innova |
| February 26, 2026 | Hormel Foods Corporation First Quarter Earnings Conference Call |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (5 total, top 5)

- [Events & Presentations](https://investor.hormelfoods.com/news-and-events/events-and-presentations/default.aspx)
- [Global Impact Report](https://investor.hormelfoods.com//s204.q4cdn.com/636391999/files/doc_downloads/2025/09/Hormel-Foods-2024-Global-Impact-Report.pdf)
- [Press Release(opens in new window)](https://s204.q4cdn.com/636391999/files/doc_earnings/2026/q1/earnings-result/hormel-earnings-release-q1-2026.pdf)
- [Presentation(opens in new window)](https://s204.q4cdn.com/636391999/files/doc_earnings/2026/q1/supplemental-info/q1-earnings-supplemental-deck.pdf)
- [Transcript(opens in new window)](https://s204.q4cdn.com/636391999/files/doc_earnings/2026/q1/transcript/corrected-transcript-hormel-foods-corp-q1-2026-earnings-call.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://events.q4inc.com/attendee/627833424)
- [Webcast(opens in new window)](https://events.q4inc.com/attendee/399622419)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 5 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **5 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 5 releases/relatórios — podemos auditar se ROE=0.061160002, DY=0.057045008294260215 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
