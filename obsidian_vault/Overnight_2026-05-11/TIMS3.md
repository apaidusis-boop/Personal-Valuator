# TIMS3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Telecom
- **RI URLs scraped** (1):
  - https://ri.tim.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=23.329999923706055
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.17724001 · DY=0.06617775418126712 · P/E=13.03352
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 13.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.tim.com.br/ | ✅ | 13.4s | 27,580 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **10**
- Audio/video: **0**
- Headers detectados (structure): **27**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (10 total, top 10)

- [Relatórios ESG](https://ri.tim.com.br/esg/relatorios-esg/)
- [Apresentações](https://ri.tim.com.br/informacoes-ao-mercado/apresentacoes/)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/4c4aa51f-1235-4aa1-8b83-adc92e8dacc3/e20a2bb8-2971-e29d-e6fd-7d61e00629e9?origin=2)
- [Demonstrações Financeiras](https://api.mziq.com/mzfilemanager/v2/d/4c4aa51f-1235-4aa1-8b83-adc92e8dacc3/17d86534-4a1b-2293-5585-05efd1539623?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/4c4aa51f-1235-4aa1-8b83-adc92e8dacc3/a6430a5a-53e3-b264-9a18-262e01e56baa?origin=2)
- [Demonstrações Financeiras](https://api.mziq.com/mzfilemanager/v2/d/4c4aa51f-1235-4aa1-8b83-adc92e8dacc3/197553f9-c229-4f09-b201-bcf48f2026d6?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/4c4aa51f-1235-4aa1-8b83-adc92e8dacc3/72184409-e58f-5e16-a2c4-8126a571b6db?origin=1)
- [Demonstrações Financeiras](https://api.mziq.com/mzfilemanager/v2/d/4c4aa51f-1235-4aa1-8b83-adc92e8dacc3/c67e134a-e017-769a-65b6-34397cb71c2e?origin=1)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/4c4aa51f-1235-4aa1-8b83-adc92e8dacc3/4d468ff6-b297-cee6-644b-9db10e6f3a7c?origin=1)
- [Demonstrações Financeiras](https://api.mziq.com/mzfilemanager/v2/d/4c4aa51f-1235-4aa1-8b83-adc92e8dacc3/49fe829b-408b-7bbf-bd63-a0a87d2f83a4?origin=1)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 10 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **10 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 10 releases/relatórios — podemos auditar se ROE=0.17724001, DY=0.06617775418126712 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
