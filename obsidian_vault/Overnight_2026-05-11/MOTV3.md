# MOTV3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.motiva.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **15**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=15.869999885559082
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.20401 · DY=0.024411216307097798 · P/E=10.795918
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Divulgação 1T26 |
| 2026-04-29 | fato_relevante | cvm | ABERTURA DO 4º PROGRAMA DE RECOMPRA DE AÇÕES |
| 2026-04-29 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Divulgação 1T26 |
| 2026-04-27 | fato_relevante | cvm | Intenção de Alienação de Participação Acionária - Grupo Mover. |
| 2026-04-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Movimentação Mensal - Mar |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 13.1s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.motiva.com.br/ | ✅ | 13.1s | 43,000 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **1**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Apresentações e Eventos](https://ri.motiva.com.br/esg/apresentacoes-e-eventos/)
- [Relatórios Anuais e Sustentabilidade](https://www.grupoccr.com.br/esg/nossas-praticas/#5eafe6095e63f6463e433d716522af25)

### Audio / Video disponível (markitdown pode ler)

- [Apresentações e Teleconferências](https://ri.motiva.com.br/resultados/apresentacoes-e-teleconferencias/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 15 | 15 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.20401, DY=0.024411216307097798 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
