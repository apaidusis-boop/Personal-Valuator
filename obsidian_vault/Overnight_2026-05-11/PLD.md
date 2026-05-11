# PLD — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: REIT
- **RI URLs scraped** (1):
  - https://ir.prologis.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=2.0 · entry=109.22 · date=2023-10-17

- Total events na DB: **158**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=144.08999633789062
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.06844 · DY=0.03588035346934401 · P/E=36.203518
- Score (último run): score=0.6667 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | 10-Q | sec | 10-Q |
| 2026-04-30 | 8-K | sec | 8-K \| 5.07,9.01 |
| 2026-04-27 | 8-K | sec | 8-K \| 2.03,8.01,9.01 |
| 2026-04-23 | 8-K | sec | 8-K \| 2.03,8.01,9.01 |
| 2026-04-16 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 16.9s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://ir.prologis.com/ | ✅ | 16.9s | 15,835 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **1**
- Headers detectados (structure): **33**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| Apr 28, 2026 | PROLOGIS DECLARES QUARTERLY DIVIDEND |
| Apr 16, 2026 | View Press Release |
| Apr 9, 2026 | View Press Release |
| Mar 31, 2026 | Earnings Release |
| 2025-12-31 | Latest Annual Report |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Events & Presentations](https://ir.prologis.com/events-presentations)
- [PLD Investor Presentation March 2026](https://d1io3yog0oux5.cloudfront.net/_df2103e45c988946122009b01faa2e6c/prologis/db/2224/21676/pdf/Prologis_Investor%2BPresentation_March_2026.pdf)
- [Supplemental Financial Report](https://d1io3yog0oux5.cloudfront.net/_df2103e45c988946122009b01faa2e6c/prologis/db/2317/21681/file/Q1_2026_Prologis_Earnings_Supplemental.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Earnings Webcast](https://event.choruscall.com/mediaframe/webcast.html?webcastid=E3y2wRMN)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 158 | 158 + 1 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**1 filings detectados como novos vs DB.**

### 1. 2025-12-31 — Latest Annual Report

URL: https://www.prologis.com/annual-report-2024
Após data máxima DB: (título não match em DB)


## Sinais / observações

- **1 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 💼 **Posição activa**: qty=2.0, entry=109.22. 1 filings novos → revisitar tese se houver signal material acima.
- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.06844, DY=0.03588035346934401 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
