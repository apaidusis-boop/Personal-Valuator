# VIVA3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://ri.vivara.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=24.770000457763672
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.22749001 · DY=0.028165481917919483 · P/E=9.947791
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 14.7s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.vivara.com.br/ | ✅ | 14.7s | 16,935 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **0**
- Headers detectados (structure): **17**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Apresentações](https://ri.vivara.com.br/informacoes-financeiras/apresentacoes/)
- [Relatório de Sustentabilidade](https://api.mziq.com/mzfilemanager/v2/d/61a4df2d-a461-44d6-9128-da74058019db/ef60d08a-20c8-d332-10c1-ed75c96e7e73?origin=2)
- [Apresentação Institucional](https://api.mziq.com/mzfilemanager/v2/d/61a4df2d-a461-44d6-9128-da74058019db/178e6784-4655-698e-0c70-9f181b5f7927?origin=2)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.22749001, DY=0.028165481917919483 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
