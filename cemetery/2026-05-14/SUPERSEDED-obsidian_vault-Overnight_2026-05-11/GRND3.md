# GRND3 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://ri.grendene.com.br/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=4.190000057220459
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.17924 · DY=0.36749307374030493 · P/E=5.9014087
- Score (último run): score=1.0 · passes_screen=1

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.5s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.grendene.com.br/ | ✅ | 11.5s | 10,796 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **5**
- Audio/video: **2**
- Headers detectados (structure): **8**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (5 total, top 5)

- [Relatório de Sustentabilidade](https://grendene.com.br/sustentabilidade/wp-content/uploads/2025/10/relatorio_sustentabilidade_Grendene_2024-1.pdf)
- [Apresentações](https://ri.grendene.com.br/PT/Apresentacoes-e-Videoconferencias/Apresentacoes)
- [Demonstrações Financeiras](https://ri.grendene.com.br/PT/Informacoes-Financeiras/Demonstracoes-Financeiras)
- [Relatório da Administração](https://ri.grendene.com.br/PT/Informacoes-Financeiras/Relatorio-da-Administracao)
- [Releases de Resultados](https://ri.grendene.com.br/Arquivos/releases/2564_1T26.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Videoconferências](https://ri.grendene.com.br/PT/Apresentacoes-e-Videoconferencias/Videoconferencias)
- [Videoconferências](https://youtu.be/rWvfl3WP3Fk)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 5 | + |
| Audio/video acessível | 0 (era cego) | 2 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 fontes audio/video** disponíveis (markitdown pode transcrever)
- **5 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **2 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 5 releases/relatórios — podemos auditar se ROE=0.17924, DY=0.36749307374030493 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
