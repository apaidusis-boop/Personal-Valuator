# PLTR — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investors.palantir.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1.8673199999999999 · entry=80.32902769744875 · date=2024-11-15

- Total events na DB: **72**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=137.8000030517578
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.32587 · DY=None · P/E=153.11111
- Score (último run): score=0.25 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-05 | 10-Q | sec | 10-Q |
| 2026-05-04 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |
| 2026-04-24 | proxy | sec | DEF 14A |
| 2026-02-17 | 10-K | sec | 10-K |
| 2026-02-02 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.palantir.com/ | ✅ | 12.4s | 4,563 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **0**
- Headers detectados (structure): **6**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 72 | 72 + 0 novos no RI | = |
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
