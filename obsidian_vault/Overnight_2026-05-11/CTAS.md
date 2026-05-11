# CTAS — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://www.cintas.com/investors
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=166.97000122070312
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.41303003 · DY=0.010421033642444821 · P/E=35.22574
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 34.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.cintas.com/investors | ✅ | 34.2s | 20,844 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **1**
- Audio/video: **2**
- Headers detectados (structure): **21**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (1 total, top 1)

- [Investor Relations](https://www.cintas.com/investors)

### Audio / Video disponível (markitdown pode ler)

- [Earnings Webcast](https://www.cintas.com/investors/earnings-webcast/event-details)
- [listen to webcastopens in a new tabopens in a new tab](https://app.webinar.net/vyJaEX6G3VB)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 1 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **1 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 1 releases/relatórios — podemos auditar se ROE=0.41303003, DY=0.010421033642444821 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
