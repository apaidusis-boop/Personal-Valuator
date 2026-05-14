# CHD — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://investor.churchdwight.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=93.44000244140625
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.16779 · DY=0.01276755103627163 · P/E=30.736843
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 9.2s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investor.churchdwight.com/ | ✅ | 9.2s | 20,885 |
- Filings extraídos do RI: **4**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **1**
- Headers detectados (structure): **9**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 1, 2026 | Church & Dwight Reports Q1 2026 Results |
| April 29, 2026 | Church & Dwight Co., Inc. Declares 501st Regular Quarterly Dividend |
| March 25, 2026 | Church & Dwight to Webcast Discussion of First Quarter 2026 Earnings Results on  |
| May 1, 2026 | Q1 2026 Church & Dwight Co., Inc. Earnings Conference Call |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Events & Presentations](https://investor.churchdwight.com/Investors/events-and-presentations/default.aspx)
- [Church & Dwight Reports Q1 2026 Results](https://investor.churchdwight.com/files/doc_earnings/2026/q1/earnings-result/PressRelease.pdf)
- [Press Release for the latest quarter(opens in new window)](https://s203.q4cdn.com/233583214/files/doc_earnings/2026/q1/earnings-result/PressRelease.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast for the latest quarter(opens in new window)](https://events.q4inc.com/attendee/339105132)

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
- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.16779, DY=0.01276755103627163 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
