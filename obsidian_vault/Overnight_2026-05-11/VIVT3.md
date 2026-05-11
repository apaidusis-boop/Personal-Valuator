# VIVT3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Telecom
- **RI URLs scraped** (1):
  - https://ri.telefonica.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=38.36000061035156
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.08901 · DY=0.029573044367832278 · P/E=20.08377
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 27.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.telefonica.com.br/ | ✅ | 27.8s | 15,163 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **0**
- Headers detectados (structure): **19**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Relatórios de Sustentabilidade](https://ri.telefonica.com.br/esg/relatorios-de-sustentabilidade/)
- [Apresentações e Eventos](https://ri.telefonica.com.br/resultados-e-comunicados/apresentacoes-e-eventos/)
- [Relatórios](https://ri.telefonica.com.br/resultados-e-comunicados/relatorios/)

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

- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.08901, DY=0.029573044367832278 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
