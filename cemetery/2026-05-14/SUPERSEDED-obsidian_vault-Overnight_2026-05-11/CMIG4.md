# CMIG4 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.cemig.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=11.770000457763672
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.1751 · DY=0.1078195370130954 · P/E=6.803468
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 6.5s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.cemig.com.br/ | ✅ | 6.5s | 15,641 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **1**
- Headers detectados (structure): **7**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Relatórios SEC](https://ri.cemig.com.br/informacoes-financeiras/relatorios-sec)
- [Relatórios](https://novoportal.cemig.com.br/relatorios/)
- [Relatórios](https://www.cemig.com.br/programa-sustentabilidade/relatorios-de-sustentabilidade-da-cemig/)

### Audio / Video disponível (markitdown pode ler)

- [Apresentações e Teleconferências](https://ri.cemig.com.br/divulgacao-e-resultados/apresentacoes-e-teleconferencias)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.1751, DY=0.1078195370130954 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
