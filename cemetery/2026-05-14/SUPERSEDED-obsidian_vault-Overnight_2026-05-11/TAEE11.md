# TAEE11 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.taesa.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=40.959999084472656
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.21719 · DY=0.07966096369462379 · P/E=39.384617
- Score (último run): score=0.0 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 12.6s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.taesa.com.br/ | ✅ | 12.6s | 30,295 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **10**
- Audio/video: **0**
- Headers detectados (structure): **55**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (10 total, top 10)

- [Release de Resultados 1T26](https://ri.taesa.com.br/wp-content/uploads/2026/05/TAESA_Release-1T26.pdf)
- [Apresentação de Resultados 1T26](https://ri.taesa.com.br/wp-content/uploads/2026/05/Apresentacao-1T26_TAESA.pdf)
- [Demonstrações Financeiras (ITR/DFP) 1T26](https://ri.taesa.com.br/wp-content/uploads/2018/11/1TRI-2026-Versao-final.pdf)
- [Relatório de Sustentabilidade 2025](https://ri.taesa.com.br/wp-content/uploads/2018/11/Relatorio-de-Sustentabilidade-da-TAESA-2025.pdf)
- [Release de Resultados 4T25 e 2025](https://ri.taesa.com.br/wp-content/uploads/2026/03/Release-4T25.pdf)
- [Apresentação de Resultados 4T25 e 2025](https://ri.taesa.com.br/wp-content/uploads/2026/03/Apresentacao-4T25.pdf)
- [Demonstrações Financeiras (ITR/DFP) 4T25 e 2025](https://ri.taesa.com.br/wp-content/uploads/2026/03/TAESA-DFs-31.12.2025.pdf)
- [Apresentações](https://ri.taesa.com.br/divulgacao-ao-mercado/apresentacoes/)
- [Relatório de Sustentabilidade](https://ri.taesa.com.br/sustentabilidade/visao-geral/#relatorios)
- [Download Apresentação](https://youtu.be/SUkTuTP05AY)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 10 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **10 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 10 releases/relatórios — podemos auditar se ROE=0.21719, DY=0.07966096369462379 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
