# EQTL3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.equatorialenergia.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **24**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=42.310001373291016
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.06985 · DY=0.037421246717318314 · P/E=44.072918
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Resultado sobre proposta  |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Release Operacional - 1t2 |
| 2026-04-29 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Reajuste Tarifário - Equa |
| 2026-04-22 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-04-15 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Institucional 4T25 |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.equatorialenergia.com.br/ | ✅ | 12.4s | 19,769 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **6**
- Audio/video: **2**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (6 total, top 6)

- [Relatórios Inventário de Gases do Efeito Estufa](https://ri.equatorialenergia.com.br/esg/relatorios-inventario-gases-estufa/)
- [Relatórios Anuais e de Sustentabilidade](https://ri.equatorialenergia.com.br/esg/relatorios-anuais-e-de-sustentabilidade/)
- [Apresentações Institucionais](https://ri.equatorialenergia.com.br/informacoes-financeiras/apresentacoes-institucionais/)
- [Relatório Anual de Sustentabilidade](https://ri.equatorialenergia.com.br/divulgacao-e-resultados/relatorios-anuais-e-de-sustentabilidade/)
- [Demonstrações Financeiras](https://api.mziq.com/mzfilemanager/v2/d/62b21cba-838c-49a4-aaef-e0fb2350c169/a9e3810b-8033-0242-c4d1-10e5e0282f68?origin=2)
- [Apresentação de Resultados](https://api.mziq.com/mzfilemanager/v2/d/62b21cba-838c-49a4-aaef-e0fb2350c169/47f2f0e4-2422-4ae1-83af-e4420d289b02?origin=2)

### Audio / Video disponível (markitdown pode ler)

- [Áudio Teleconferência](https://api.mziq.com/mzfilemanager/v2/d/62b21cba-838c-49a4-aaef-e0fb2350c169/773f3a34-7752-6610-5205-216ce28e3938?origin=2)
- [Clique aqui para acessar o Webcast](https://mzgroup.zoom.us/webinar/register/WN_BqTavN8WTz2gWbG5nJ7GFw)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 24 | 24 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 6 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **6 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 6 releases/relatórios — podemos auditar se ROE=0.06985, DY=0.037421246717318314 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
