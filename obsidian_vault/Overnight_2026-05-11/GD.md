# GD — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://www.generaldynamics.com/investors
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=346.5299987792969
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.17974001 · DY=0.01757423605879123 · P/E=21.780642
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.0s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.generaldynamics.com/investors | ✅ | 12.0s | 10,191 |
- Filings extraídos do RI: **1**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **1**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| March 09, 2026 | General Dynamics Board Declares Dividend |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Audio / Video disponível (markitdown pode ler)

- [General Dynamics to Webcast 2026 First-Quarter Financial Results Conference Call](https://www.generaldynamics.com/Articles/2026/04/general-dynamics-to-webcast-2026-first-quarter-financial-results-Conference-Call)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 0 | = |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 fontes audio/video** disponíveis (markitdown pode transcrever)

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
