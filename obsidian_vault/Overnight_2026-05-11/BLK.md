# BLK — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://ir.blackrock.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=2.0 · entry=897.695 · date=2024-01-29

- Total events na DB: **15**
- deep_fundamentals (rows anuais): **4**
- Última cotação DB: 2026-05-08 → close=1084.8299560546875
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=None · DY=0.019689721767715655 · P/E=27.325691
- Score (último run): score=0.2 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-06 | 10-Q | sec | 10-Q |
| 2026-04-14 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |
| 2026-04-10 | proxy | sec | DEF 14A |
| 2026-04-03 | 8-K | sec | 8-K \| 1.01,2.03,9.01 |
| 2026-02-25 | 10-K | sec | 10-K |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 28.9s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ir.blackrock.com/ | ✅ | 28.9s | 14,438 |
- Filings extraídos do RI: **4**
- Eventos calendário: **0**
- Apresentações/releases: **5**
- Audio/video: **1**
- Headers detectados (structure): **23**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| Apr 14, 2026 | BlackRock Reports First Quarter 2026 Diluted EPS of $14.06, or $12.53 as adjuste |
| Mar 31, 2026 | BlackRock to Report First Quarter 2026 Earnings on April 14th |
| Feb 2, 2026 | BlackRock’s Martin S. Small to Present at the 2026 Bank of America Securities Fi |
| Jun 12, 2025 | Shareholder Value Presentation(opens in new window) |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (5 total, top 5)

- [Events & Presentations](https://ir.blackrock.com/news-and-events/events-and-presentations/default.aspx)
- [2025 Annual Report](https://ir.blackrock.com//s24.q4cdn.com/856567660/files/doc_financials/2026/ar/BLK_AR25.pdf)
- [Full presentation](https://ir.blackrock.com//s24.q4cdn.com/856567660/files/doc_presentations/2025/BLK-Investor-Day-2025-WEB.pdf)
- [Earnings Release(opens in new window)](https://s24.q4cdn.com/856567660/files/doc_financials/2026/Q1/BLK-1Q26-Earnings-Release.pdf)
- [Earnings Supplement(opens in new window)](https://s24.q4cdn.com/856567660/files/doc_financials/2026/Q1/BLK-1Q26-Earnings-Supplement.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://events.q4inc.com/attendee/426255190)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 15 | 15 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 5 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **5 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 5 releases/relatórios — podemos auditar se ROE=None, DY=0.019689721767715655 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
