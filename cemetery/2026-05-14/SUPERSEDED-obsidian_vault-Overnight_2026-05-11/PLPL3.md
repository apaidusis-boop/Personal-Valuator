# PLPL3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://ri.planoeplano.com.br/
- **Pilot rationale**: manual (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=10.550000190734863
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.41075 · DY=0.04671374323128536 · P/E=5.861111
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.6s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.planoeplano.com.br/ | ✅ | 11.6s | 9,362 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **1**
- Headers detectados (structure): **1**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Relatório de Sustentabilidade](https://ri.planoeplano.com.br/relatorio-esg/)
- [Relatório de Igualdade Salarial](https://ri.planoeplano.com.br/relatorio-de-igualdade-salarial/)

### Audio / Video disponível (markitdown pode ler)

- [Apresentações e Teleconferências](https://ri.planoeplano.com.br/informacoes-financeiras/apresentacoes-e-teleconferencias/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
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
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.41075, DY=0.04671374323128536 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
