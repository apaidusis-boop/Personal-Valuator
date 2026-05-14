# BTLG11 — Pilot Deep Dive (2026-05-10)

- **Market**: BR
- **Sector**: Logística
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/btlg11/
- **Pilot rationale**: fii_heuristic (holding)

## Antes (estado da DB)

**Posição activa**: qty=166.0 · entry=103.3 · date=2026-05-07

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-08 → close=103.75
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.08615 · DY=0.09116068433734939 · P/E=95.79871
- Score (último run): score=0.8 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 36.0s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.fiis.com.br/btlg11/ | ✅ | 36.0s | 12,152 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **0**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 0 | = |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

_(sem sinais accionáveis — RI sem novidades vs DB)_

## Interpretação para a tese

_(sem sinais accionáveis materiais)_

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
