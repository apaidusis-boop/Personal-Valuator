# RBRY11 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Papel (CRI)
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/rbry11/
- **Pilot rationale**: fii_heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=93.12000274658203
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=None · DY=0.15114905052466424 · P/E=None
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 32.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.fiis.com.br/rbry11/ | ✅ | 32.8s | 17,408 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **6**
- Audio/video: **0**
- Headers detectados (structure): **10**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (6 total, top 6)

- [Relatórios, Relatório Gerencial](https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=1126043&cvm=true)
- [Relatórios, Relatório Gerencial](https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=1101997&cvm=true)
- [Relatórios, Outros Relatórios](https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=1093223&cvm=true)
- [Relatórios, Relatório Gerencial](https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=1072499&cvm=true)
- [Relatórios, Outros Relatórios](https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=1059506&cvm=true)
- [Relatórios, Relatório Gerencial](https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=1050834&cvm=true)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 6 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **6 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 6 releases/relatórios — podemos auditar se ROE=None, DY=0.15114905052466424 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
