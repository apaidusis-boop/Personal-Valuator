# KLBN11 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://ri.klabin.com.br/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1059.0 · entry=18.29 · date=2026-05-07

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=17.190000534057617
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.05465 · DY=0.09517835655434984 · P/E=26.006052
- Score (último run): score=0.0 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 19.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.klabin.com.br/ | ✅ | 19.4s | 15,057 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **1**
- Headers detectados (structure): **31**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Relatório de Sustentabilidade](https://rs2024.klabin.com.br/)
- [Apresentações](https://ri.klabin.com.br/divulgacoes-e-resultados/apresentacoes/)

### Audio / Video disponível (markitdown pode ler)

- [Vídeos e Podcasts](https://ri.klabin.com.br/klabininvest/)

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
- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.05465, DY=0.09517835655434984 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
