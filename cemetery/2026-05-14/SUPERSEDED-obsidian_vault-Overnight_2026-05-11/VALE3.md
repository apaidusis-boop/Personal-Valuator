# VALE3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Mining
- **RI URLs scraped** (1):
  - https://vale.com/pt/investidores
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=501.0 · entry=61.84 · date=2026-05-07

- Total events na DB: **42**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=80.80000305175781
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.068390004 · DY=0.06778660635063978 · P/E=24.996931
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Vale esclarece sobre notí |
| 2026-04-29 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Desempenho da Vale no 1T26 |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atualização sobre negocia |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atualização sobre negocia |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Relatório de produção e v |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 20.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://vale.com/pt/investidores | ✅ | 20.2s | 82,319 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **14**
- Audio/video: **2**
- Headers detectados (structure): **29**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (14 total, top 12)

- [Comunicados, resultados, apresentações e relatórios](https://vale.com/pt/comunicados-resultados-apresentacoes-e-relatorios)
- [Acesse o relatório de desempenho do 1T26 aqui.](https://api.mziq.com/mzfilemanager/v2/d/53207d1c-63b4-48f1-96b7-19869fae19fe/07ad1ae4-205c-7457-ad91-a9d53f1b5147?origin=2)
- [Acesse o relatório Produção e Vendas](https://api.mziq.com/mzfilemanager/v2/d/53207d1c-63b4-48f1-96b7-19869fae19fe/cf0ed600-42cd-8013-998a-6dbf39c5e146?origin=2)
- [Apresentação Institucional](https://api.mziq.com/mzfilemanager/v2/d/53207d1c-63b4-48f1-96b7-19869fae19fe/980ced1c-fff8-4853-c7e8-6fb5b7b9395f?origin=1)
- [Apresentação Institucional](https://api.mziq.com/mzfilemanager/v2/d/53207d1c-63b4-48f1-96b7-19869fae19fe/d06b73db-5a28-88a4-a7ea-593521d70cb9?origin=2)
- [Relatórios e Apresentações](https://vale.com/pt/comunicados-resultados-apresentacoes-e-relatorios#comunicados-relevantes)
- [Relatório de Produção 4T22](https://vale.com/pt/relatorio-de-producao-4t22)
- [Museu Vale apresenta exposição sobre Leonardo Da Vinci](https://vale.com/pt/museu-vale-apresenta-exposi%C3%A7%C3%A3o-sobre-leonardo-da-vinci)
- [Relatório de Vendas e Produção 1T23](https://vale.com/pt/confira-os-resultados-de-vendas-e-producao-do-1t23%E2%80%8B)
- [Relatório de Vendas e Produção 2T23](https://vale.com/pt/relatorio-de-vendas-e-producao-2t23)
- [Relatório de Vendas e Produção 3T23](https://vale.com/pt/relatorio-de-vendas-e-producao-do-3t23)
- [Relatório de Vendas e Produção 4T23](https://vale.com/pt/relatorio-de-vendas-e-producao-4t23)
- _… e mais 2 no MD raw (`data/portal_cache/`)_

### Audio / Video disponível (markitdown pode ler)

- [Reinaldo Duarte Castanheira Filho](https://vale.com/pt/reinaldo-duarte)
- [Vale é destaque em eficiência energética em podcast do MIT Technology Review](https://vale.com/pt/vale-e-destaque-em-eficiencia-energetica-em-podcast-do-mit-technology-review)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 42 | 42 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 14 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **14 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 14 releases/relatórios — podemos auditar se ROE=0.068390004, DY=0.06778660635063978 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
