# JKHY — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investor.jkhy.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=145.83999633789062
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.24892001 · DY=0.016113549499517144 · P/E=20.368715
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.9s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.jkhy.com/ | ✅ | 12.9s | 53,005 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **1**
- Headers detectados (structure): **28**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Customer & Member Relationships](https://www.jackhenry.com/what-we-offer/customer-member-relationship)
- [Investor Relations](https://ir.jackhenry.com/)
- [Investor Relations](https://ir.jackhenry.com)

### Audio / Video disponível (markitdown pode ler)

- [Listen to the Podcast](https://www.jackhenry.com/resources/podcasts/greg-adelson-featured-on-fintech-cowboys-podcast)

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
- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.24892001, DY=0.016113549499517144 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
