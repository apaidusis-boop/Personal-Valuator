# ABEV3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://ri.ambev.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=16.31999969482422
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.17251 · DY=0.05318627550436049 · P/E=16.484848
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 14.3s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.ambev.com.br/ | ✅ | 14.3s | 39,073 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **26**
- Headers detectados (structure): **66**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Apresentações](https://ri.ambev.com.br/apresentacoes/apresentacoes/)
- [Apresentação de Resultados 1T26](https://api.mziq.com/mzfilemanager/v2/d/c8182463-4b7e-408c-9d0f-42797662435e/226e19cf-e7a9-e9db-d65b-93e1dd576b8f?origin=2)

### Audio / Video disponível (markitdown pode ler)

- [Teleconferência de Resultados 2T19](https://apicatalog.mziq.com/filemanager/d/c8182463-4b7e-408c-9d0f-42797662435e/fd4e8bc1-efd8-4765-b041-c511d1187900?origin=2)
- [Teleconferência de Resultados 3T25](https://api.mziq.com/mzfilemanager/v2/d/c8182463-4b7e-408c-9d0f-42797662435e/5e20f1e5-2515-189f-5937-dc0a14d16af1?origin=2)
- [Teleconferência de Resultados 2T25](https://api.mziq.com/mzfilemanager/v2/d/c8182463-4b7e-408c-9d0f-42797662435e/6232816d-2220-fcca-d971-e660679220b1?origin=2)
- [Teleconferência de Resultados 1T25](https://api.mziq.com/mzfilemanager/v2/d/c8182463-4b7e-408c-9d0f-42797662435e/1de9ac1a-a823-5f73-4a7e-c60321e8c5aa?origin=2)
- [Teleconferência de Resultados 4T24](https://api.mziq.com/mzfilemanager/v2/d/c8182463-4b7e-408c-9d0f-42797662435e/5eafc823-3329-45a4-aafb-8a5e57e5b1f2?origin=2)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 26 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **26 fontes audio/video** disponíveis (markitdown pode transcrever)
- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **26 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.17251, DY=0.05318627550436049 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
