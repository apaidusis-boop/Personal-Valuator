# PSSA3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Insurance
- **RI URLs scraped** (1):
  - https://ri.portoseguro.com.br/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=51.4900016784668
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.25159 · DY=0.05793425719089674 · P/E=9.065142
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.portoseguro.com.br/ | ✅ | 12.8s | 17,193 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **4**
- Audio/video: **0**
- Headers detectados (structure): **34**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (4 total, top 4)

- [Apresentação da Companhia](https://ri.portoseguro.com.br/a-companhia/apresentacao-da-companhia/)
- [Demonstrações Financeiras por Empresa](https://ri.portoseguro.com.br/informacoes-aos-acionistas/demonstracoes-financeiras-por-empresa/)
- [Relatórios do Conglomerado Prudencial](https://ri.portoseguro.com.br/informacoes-aos-acionistas/conglomerado-prudencial/)
- [Apresentação - Porto Day 2026](https://api.mziq.com/mzfilemanager/v2/d/b77a3922-d280-4451-b3ee-0afec4577834/29a53a81-d7ed-afa4-0ce8-f3c59682b29e?origin=2)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 4 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **4 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 4 releases/relatórios — podemos auditar se ROE=0.25159, DY=0.05793425719089674 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
