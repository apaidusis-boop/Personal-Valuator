# BN — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://bn.brookfield.com/news-and-events
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=7.0 · entry=25.56142857142857 · date=2023-07-19

- Total events na DB: **343**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=47.08000183105469
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.01951 · DY=0.005310110243774379 · P/E=96.081635
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-04 | 6-K | sec | 6-K |
| 2026-04-22 | 6-K | sec | 6-K |
| 2026-04-17 | 6-K | sec | 6-K |
| 2026-04-14 | 6-K | sec | 6-K |
| 2026-03-18 | 6-K | sec | 6-K |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 21.0s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://bn.brookfield.com/news-and-events | ✅ | 21.0s | 9,483 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **1**
- Audio/video: **0**
- Headers detectados (structure): **10**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (1 total, top 1)

- [Investor Presentations](https://bn.brookfield.com/events-news/investor-presentations)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 343 | 343 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 1 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 1 releases/relatórios — podemos auditar se ROE=0.01951, DY=0.005310110243774379 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
