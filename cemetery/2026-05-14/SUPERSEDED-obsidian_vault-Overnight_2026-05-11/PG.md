# PG — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://www.pginvestor.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=10.0 · entry=142.76 · date=2026-04-13

- Total events na DB: **111**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=146.4199981689453
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.31112 · DY=0.0290943863766795 · P/E=21.406431
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-24 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-24 | 8-K | sec | 8-K \| 7.01,9.01 |
| 2026-04-24 | 10-Q | sec | 10-Q |
| 2026-04-14 | 8-K | sec | 8-K \| 7.01,9.01 |
| 2026-01-23 | 10-Q | sec | 10-Q |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 17.9s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.pginvestor.com/ | ✅ | 17.9s | 19,567 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **2**
- Audio/video: **0**
- Headers detectados (structure): **13**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| April 24, 2026 | P&G Announces Fiscal Year 2026 Third Quarter Results |
| April 16, 2026 | P&G Recommends Stockholders Reject April 7 Mini-Tender Offer by Potemkin Limited |
| April 14, 2026 | P&G Declares Dividend Increase for April 2026 |
| July 29, 2026 | Q4 2026 The Procter & Gamble Earnings Conference Call (Anticipated) |
| April 24, 2026 | Q3 2026 The Procter & Gamble Earnings Conference Call |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (2 total, top 2)

- [Events & Presentations](https://www.pginvestor.com/events-and-presentations/default.aspx)
- [Investor Relations Sitemap opens in new window](https://www.pginvestor.com/site-map/default.aspx)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 111 | 111 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 2 | + |
| Audio/video acessível | 0 (era cego) | 0 | = |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **2 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 📊 **Cross-check fundamentals**: RI tem 2 releases/relatórios — podemos auditar se ROE=0.31112, DY=0.0290943863766795 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
