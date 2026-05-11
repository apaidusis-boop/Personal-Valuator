# RDOR3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Healthcare
- **RI URLs scraped** (1):
  - https://ri.rededorsaoluiz.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **5**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=38.310001373291016
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.19188 · DY=0.11147898321344073 · P/E=18.242859
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-16 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-23 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Distribuição de Juros Sob |
| 2026-03-06 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Habilitação Medicina |
| 2026-02-26 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação da Teleconferência d |
| 2026-01-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Fechamento do Acordo Atlâ |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.9s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.rededorsaoluiz.com.br/ | ✅ | 12.9s | 8,713 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **0**
- Headers detectados (structure): **2**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Apresentações](https://ri.rededorsaoluiz.com.br/documentos-publicados/apresentacoes/)
- [Relatório Anual](https://ri.rededorsaoluiz.com.br/documentos-publicados/relatorio-anual/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 5 | 5 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.19188, DY=0.11147898321344073 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
