# PETR4 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Oil & Gas
- **RI URLs scraped** (1):
  - https://www.investidorpetrobras.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **49**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=45.66999816894531
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.28176 · DY=0.06917992394727883 · P/E=6.073138
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Petrobras antecipa início |
| 2026-04-30 | fato_relevante | cvm | Relatório de Produção e Vendas 1T26 |
| 2026-04-28 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Investor Tour 2026 |
| 2026-04-27 | fato_relevante | cvm | Petrobras amplia presença na Bacia de Campos com a aquisição de parte do ring-fe |
| 2026-04-23 | fato_relevante | cvm | Petrobras assina novo Acordo de Acionistas da Braskem |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.investidorpetrobras.com.br/ | ✅ | 11.2s | 25,676 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **4**
- Audio/video: **0**
- Headers detectados (structure): **14**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (4 total, top 4)

- [Apresentações e Webinars](https://www.investidorpetrobras.com.br/esg-meio-ambiente-social-e-governanca/apresentacoes-e-webinars/)
- [Apresentações](https://www.investidorpetrobras.com.br/apresentacoes-relatorios-e-eventos/apresentacoes/)
- [Relatórios Anuais](https://www.investidorpetrobras.com.br/apresentacoes-relatorios-e-eventos/relatorios-anuais/)
- [Eventos](https://www.investidorpetrobras.com.br/apresentacoes-relatorios-e-eventos/eventos/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 49 | 49 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 4 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **4 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 4 releases/relatórios — podemos auditar se ROE=0.28176, DY=0.06917992394727883 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
