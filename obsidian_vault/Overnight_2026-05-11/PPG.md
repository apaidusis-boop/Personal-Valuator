# PPG — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://investor.ppg.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=109.61000061035156
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.20748 · DY=0.025636346905873693 · P/E=15.703439
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.9s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.ppg.com/ | ✅ | 11.9s | 11,739 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **6**
- Audio/video: **1**
- Headers detectados (structure): **19**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| April 30, 2026 | PPG IT team named ‘Tech Team of the Year’ by Pittsburgh... |
| April 28, 2026 | PPG reports first quarter 2026 financial results |
| April 28, 2026 | PPG appoints Jamie Beggs as senior vice president and c... |
| April 20, 2026 | PPG introduces end-to-end protective coatings solutions... |
| April 20, 2026 | PPG launches first aluminum coil-applied PVC-NI coating... |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (6 total, top 6)

- [Presentations](https://investor.ppg.com/presentations/events/default.aspx)
- [Presentations](https://investor.ppg.com/presentations/presentations/default.aspx)
- [Presentation(opens in new window)](https://s25.q4cdn.com/953898558/files/doc_financials/2026/q1/1Q-2026-PPG-Earnings-Presentation.pdf)
- [Transcript(opens in new window)](https://s25.q4cdn.com/953898558/files/doc_financials/2026/q1/PPG-Transcript-1Q2026.pdf)
- [2026 BMO Chemicals at Farm to Market](https://investor.ppg.com/presentations/events/event-details/2026/2026-BMO-Chemicals-at-Farm-to-Market-2026-QEYaD1aCN8/default.aspx)
- [KeyBanc Industrials & Basic Materials Conference](https://investor.ppg.com/presentations/events/event-details/2026/KeyBanc-Industrials--Basic-Materials-Conference-2026-NLA5t495N3/default.aspx)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://events.q4inc.com/attendee/616458242)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 6 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **6 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 6 releases/relatórios — podemos auditar se ROE=0.20748, DY=0.025636346905873693 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
