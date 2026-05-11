# BBSE3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Insurance
- **RI URLs scraped** (1):
  - https://www.bbseguridaderi.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=34.52000045776367
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.75649 · DY=0.1317758383452436 · P/E=7.282701
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 14.6s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.bbseguridaderi.com.br/ | ✅ | 14.6s | 28,874 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **17**
- Audio/video: **0**
- Headers detectados (structure): **12**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (17 total, top 12)

- [Relatórios da administração](https://www.bbseguridaderi.com.br/informacoes-ao-mercado/relatorios-da-administracao/)
- [Apresentações](https://www.bbseguridaderi.com.br/informacoes-ao-mercado/apresentacoes/)
- [Demonstrações Contábeis (.pdf)](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/bb0b74dd-7875-1999-9620-fe4a5cc12e0f?origin=2)
- [Demonstrações Contábeis (.doc)](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/f127a3de-5541-3d0a-152f-acf38487aceb?origin=2)
- [Apresentação dos Resultados](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/5c2a9ef9-8a67-5750-b210-9cf99ef55b7b?origin=2)
- [Demonstrações Contábeis (.pdf)](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/15802c72-e8c8-fc9d-a817-54714f203203?origin=2)
- [Demonstrações Contábeis (.doc)](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/fcad26e8-d847-7b54-ac2c-010225fd1e28?origin=2)
- [Apresentação dos Resultados](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/cc0a8ff6-10e9-026c-7412-d43ce1c3d9a3?origin=2)
- [Demonstrações Contábeis (.pdf)](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/7027723f-d52a-e84a-9baf-639602e17bc7?origin=2)
- [Demonstrações Contábeis (.doc)](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/017eea05-3424-de9f-5bff-2723c397d3d2?origin=2)
- [Apresentação dos Resultados](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/754b2e6c-7e2c-888b-f09b-da1f08998a81?origin=2)
- [Demonstrações Contábeis (.pdf)](https://api.mziq.com/mzfilemanager/v2/d/d4ee6df5-1dd8-4fb5-b518-e05397c304e4/9aba38f2-996f-cb37-3267-d0e9d8c4b726?origin=1)
- _… e mais 5 no MD raw (`data/portal_cache/`)_

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 17 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **17 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 17 releases/relatórios — podemos auditar se ROE=0.75649, DY=0.1317758383452436 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
