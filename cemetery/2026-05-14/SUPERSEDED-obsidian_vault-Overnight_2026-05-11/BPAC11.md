# BPAC11 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Banks
- **RI URLs scraped** (1):
  - https://ri.btgpactual.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-04-24 → close=60.880001068115234
- Último fundamentals snapshot: period_end=2026-04-25 · ROE=0.23868 · DY=0.020489585711477683 · P/E=99.15309

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 13.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ri.btgpactual.com/ | ✅ | 13.2s | 9,524 |
- Filings extraídos do RI: **0**
- Eventos calendário: **7**
- Apresentações/releases: **3**
- Audio/video: **0**
- Headers detectados (structure): **18**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

| Data | Evento |
|---|---|
| 2026-05-11 | Teleconferência de resultados - 1T26 |
| 2026-05-11 | Divulgação de resultados 2T26 |
| 2026-08-11 | Teleconferência de resultados - 2T26 |
| 2026-08-11 | Divulgação de resultados 3T26 |
| 2026-11-10 | Teleconferência de resultados - 3T26 |
| 2026-11-10 | Reunião Pública com Analistas |
| 2026-11-26 | ## Precisa falar com a gente? |

### Apresentações / releases disponíveis (3 total, top 3)

- [Relatórios Anuais](https://ri.btgpactual.com/principais-informacoes/relatorios-anuais)
- [Apresentações e Planilhas](https://ri.btgpactual.com/principais-informacoes/apresentacoes-e-planilhas)
- [Relatório de Transparência e Igualdade Salarial](https://ri.btgpactual.com/principais-informacoes/relatorio-de-transparencia-e-igualdade-salarial)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 7 | + |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 eventos críticos nos próximos 30 dias** — maior risco operacional/oportunidade
- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- ⏰ **Earnings/release iminente**: 2026-05-11 — Teleconferência de resultados - 1T26 (em ~1 dias). Re-scrape no dia + monitorizar Telegram.
- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.23868, DY=0.020489585711477683 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
