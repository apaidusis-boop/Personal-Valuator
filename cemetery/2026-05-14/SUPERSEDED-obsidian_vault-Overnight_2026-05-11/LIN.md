# LIN — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://investors.linde.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=493.1600036621094
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.18229 · DY=0.012369210711944596 · P/E=32.681244
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 5.6s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.linde.com/ | ✅ | 5.6s | 26,421 |
- Filings extraídos do RI: **3**
- Eventos calendário: **0**
- Apresentações/releases: **1**
- Audio/video: **0**
- Headers detectados (structure): **24**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 5, 2026 | ##### Linde Earns Dow Jones Best-in-Class and S&P Global Recognition for Sustain |
| May 1, 2026 | ##### Linde Reports First Quarter 2026 Results |
| April 27, 2026 | ##### Linde Declares Dividend in Second Quarter 2026 |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (1 total, top 1)

- [Download our presentation](https://assets.linde.com/-/media/global/corporate/corporate/documents/investors/events-and-presentations/why-linde-presentation.pdf)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 1 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 1 releases/relatórios — podemos auditar se ROE=0.18229, DY=0.012369210711944596 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
