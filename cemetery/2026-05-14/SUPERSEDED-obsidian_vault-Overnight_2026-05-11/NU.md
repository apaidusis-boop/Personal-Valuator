# NU — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investors.nu/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=13.0 · entry=8.25923076923077 · date=2023-12-18

- Total events na DB: **152**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=13.800000190734863
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.30278 · DY=None · P/E=23.389832
- Score (último run): score=0.25 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-09 | 6-K | sec | 6-K |
| 2026-04-08 | 20-F | sec | 20-F |
| 2026-02-25 | 6-K | sec | 6-K |
| 2026-02-25 | 6-K | sec | 6-K |
| 2026-02-25 | 6-K | sec | 6-K |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 29.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.nu/ | ✅ | 29.8s | 10,079 |
- Filings extraídos do RI: **0**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **0**
- Headers detectados (structure): **10**

### Filings detectados no RI (top 10)

_(nenhum filing parseado — heuristic falhou ou layout diferente)_

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 152 | 152 + 0 novos no RI | = |
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
