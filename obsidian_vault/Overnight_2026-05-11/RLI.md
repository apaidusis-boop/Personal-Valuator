# RLI — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investors.rlicorp.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=49.04999923706055
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.23232001 · DY=0.05382263080659345 · P/E=11.433566
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 10.0s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.rlicorp.com/ | ✅ | 10.0s | 13,049 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **1**
- Audio/video: **1**
- Headers detectados (structure): **11**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| April 22, 2026 | RLI Reports First Quarter 2026 Results |
| April 1, 2026 | RLI Announces Claim Leadership Promotions |
| April 1, 2026 | RLI First Quarter Earnings Release & Teleconference |
| May 14, 2026 | Annual shareholder meeting |
| April 23, 2026 | Q1 earnings conference call |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (1 total, top 1)

- [Events & Presentations](https://investors.rlicorp.com/events-and-presentations/default.aspx)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://events.q4inc.com/attendee/570395995)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 1 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **1 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 1 releases/relatórios — podemos auditar se ROE=0.23232001, DY=0.05382263080659345 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
