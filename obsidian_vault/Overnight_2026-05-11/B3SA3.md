# B3SA3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://ri.b3.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **13**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=17.93000030517578
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.26738 · DY=0.03379375291059481 · P/E=19.48913
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Conclusão de Venda de Par |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Cronograma de divulgação  |
| 2026-04-15 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - març |
| 2026-03-19 | fato_relevante | cvm | Alteração na Administração da B3 |
| 2026-03-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - feve |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 14.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.b3.com.br/ | ✅ | 14.2s | 10,126 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **0**
- Headers detectados (structure): **6**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Relatório Anual](https://ri.b3.com.br/pt-br/informacoes-financeiras/relatorio-anual/)
- [Apresentações e Vídeos Corporativos](https://ri.b3.com.br/pt-br/servicos-aos-investidores/apresentacoes-e-videos-corporativos/)
- [Apresentação Institucional](https://apicatalog.mziq.com/filemanager/v2/d/5fd7b7d8-54a1-472d-8426-eb896ad8a3c4/8a9fc7d4-366f-f320-b4ee-ac74042e71e5?origin=2)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 13 | 13 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.26738, DY=0.03379375291059481 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
