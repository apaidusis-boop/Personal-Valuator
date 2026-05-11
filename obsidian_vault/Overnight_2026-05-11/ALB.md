# ALB — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://investors.albemarle.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=203.52000427246094
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=-0.0182 · DY=0.007959905493276409 · P/E=None
- Score (último run): score=0.25 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.7s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.albemarle.com/ | ✅ | 11.7s | 14,270 |
- Filings extraídos do RI: **1**
- Eventos calendário: **0**
- Apresentações/releases: **6**
- Audio/video: **1**
- Headers detectados (structure): **11**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| May 6, 2026 | Albemarle Reports First Quarter 2026 Results |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (6 total, top 6)

- [Earnings Release(opens in new window)](https://s201.q4cdn.com/960975307/files/doc_earnings/2026/q1/earnings-result/Q12026_pressrelease.pdf)
- [Presentation(opens in new window)](https://s201.q4cdn.com/960975307/files/doc_earnings/2026/q1/presentation/Q12026_presentation.pdf)
- [2024 Sustainability Report Key Highlights](https://s201.q4cdn.com/960975307/files/doc_downloads/2025/07/2024-Sustainability-Report-Highlights.pdf)
- [2024 Sustainability Report](https://s201.q4cdn.com/960975307/files/doc_downloads/2025/2024-Sustainability-Report-vWeb.pdf)
- [Albemarle 2023 Strategic Update News Release](https://s201.q4cdn.com/960975307/files/doc_events/2023/Jan/24/2023_01_ALB_Strategic_Update_NR_Web.pdf)
- [Albemarle 2023 Strategic Update Presentation](https://s201.q4cdn.com/960975307/files/doc_events/2023/Jan/24/2023_01_ALB_Strategic_Update_PPT_Web.pdf)

### Audio / Video disponível (markitdown pode ler)

- [Webcast(opens in new window)](https://albemarle-q1-2026-earnings-call.open-exchange.net/)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 0 novos no RI | = |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 6 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

_(nenhum filing novo — DB está sincronizada com RI)_

## Sinais / observações

- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **6 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 6 releases/relatórios — podemos auditar se ROE=-0.0182, DY=0.007959905493276409 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
