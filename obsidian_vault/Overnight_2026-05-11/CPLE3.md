# CPLE3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.copel.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=15.470000267028809
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.10787 · DY=0.06868771697856502 · P/E=17.0
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado 08/ |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Comunicado ao Mercado 02/ |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Arquivamento Relatório An |
| 2026-03-18 | fato_relevante | cvm | FR 01/26 - Copel vence leilão de reserva de capacidade com duas usinas hidrelétr |
| 2026-03-18 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação - Leilão de Reserva  |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.7s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.copel.com/ | ✅ | 12.7s | 19,205 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **5**
- Audio/video: **0**
- Headers detectados (structure): **17**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (5 total, top 5)

- [Relatórios Anuais e Socioambientais](https://ri.copel.com/sustentabilidade/relatorios-anuais-e-socioambientais/)
- [Apresentações](https://ri.copel.com/publicacoes-e-documentos/apresentacoes/)
- [Relatórios dos Agentes Fiduciários](https://ri.copel.com/publicacoes-e-documentos/relatorios-dos-agentes-fiduciarios/)
- [Relatório 20-F](https://ri.copel.com/publicacoes-e-documentos/relatorios-20-f/)
- [Relatórios CVM 44 e Section 16-A](https://ri.copel.com/publicacoes-e-documentos/relatorios-cvm-44/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 13 | 13 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 5 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **5 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 5 releases/relatórios — podemos auditar se ROE=0.10787, DY=0.06868771697856502 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
