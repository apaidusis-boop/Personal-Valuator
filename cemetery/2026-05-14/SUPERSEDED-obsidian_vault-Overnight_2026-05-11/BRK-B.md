# BRK-B — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Holding
- **RI URLs scraped** (1):
  - https://www.berkshirehathaway.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1.0 · entry=417.99 · date=2024-03-28

- Total events na DB: **124**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=475.94000244140625
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.10499 · DY=None · P/E=14.164882
- Score (último run): score=0.5 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-07 | 8-K | sec | 8-K \| 2.02,5.02,5.03,5.07,9.01 |
| 2026-05-04 | 10-Q | sec | 10-Q |
| 2026-04-16 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-03-13 | proxy | sec | DEF 14A |
| 2026-03-05 | 8-K | sec | 8-K \| 8.01,9.01 |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.0s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.berkshirehathaway.com/ | ✅ | 11.0s | 2,101 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **0**
- Headers detectados (structure): **0**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 124 | 124 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 0 | = |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

_(sem sinais accionáveis — RI sem novidades vs DB)_

## Interpretação para a tese

_(sem sinais accionáveis materiais)_

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
