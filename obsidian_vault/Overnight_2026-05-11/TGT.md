# TGT — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://investors.target.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=125.25
- Último fundamentals snapshot: period_end=2026-05-10 · ROE=0.24034001 · DY=0.03624750499001996 · P/E=15.405904
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 11.4s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://investors.target.com/ | ✅ | 11.4s | 6,376 |
- Filings extraídos do RI: **5**
- Eventos calendário: **0**
- Apresentações/releases: **0**
- Audio/video: **1**
- Headers detectados (structure): **22**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| Mar 11, 2026 | Target Corporation Declares Regular Quarterly Dividend |
| Mar 3, 2026 | Target Corporation Reports Fourth Quarter and Full-Year 2025 Earnings |
| Jan 22, 2026 | Target Corporation Declares Regular Quarterly Dividend |
| Nov 19, 2025 | Target Corporation Reports Third Quarter Earnings |
| 2026-03-03 | [Target Corporation Declares Regular Quarterly Dividend](/press/release/2026/03/ |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Audio / Video disponível (markitdown pode ler)

- [Target Corporation to Webcast Presentation to Investors on March 3](https://investors.target.com/press/release/2026/03/target-corporation-to-webcast-presentation-to-investors-on-march-3)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 0 | 0 + 1 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 0 | = |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**1 filings detectados como novos vs DB.**

### 1. 2026-03-03 — [Target Corporation Declares Regular Quarterly Dividend](/press/release/2026/03/target-corporation-declares-regular-quarterly-dividend)

URL: https://investors.target.com/press/release/2026/03/target-outlines-strategic-plan-for-a-new-chapter-of-growth-in-2026-and-beyond
Após data máxima DB: **SIM (após max DB date)**

**Extracção markitdown (preview 1500 chars):**

```
* [Skip to main navigation](#site-nav-toggle)
* [Skip to main navigation](#site-nav-logo)
* [Skip to content](#site-content)
* [Skip to footer](#site-footer)

Open menu
[Target Corporate Home](/)

* [About](/about)
  + [Leadership & Team](/about/leadership-team)
    - [Human Capital Management](/about/leadership-team/human-capital-management)
  + [Purpose & History](/about/purpose-history)
    - [Serving & Strengthening Communities](/about/purpose-history/communities)
      * [Target Foundation](/about/purpose-history/communities/target-foundation)
        + [Hometown](/about/purpose-history/communities/target-foundation/hometown)
        + [National](/about/purpose-history/communities/target-foundation/national)
        + [Global](/about/purpose-history/communities/target-foundation/global)
        + [Charter](/about/purpose-history/communities/target-foundation/charter)
      * [Disaster Preparedness & Response](/about/purpose-history/communities/disasters)
      * [Volunteerism](/about/purpose-history/communities/volunteerism)
      * [Grants & Corporate Giving](/about/purpose-history/communities/grants-corporate-giving)
        + [Community Engagement Funds](/about/purpose-history/communities/grants-corporate-giving/community-engagement-funds)
        + [Target Circle Community Giving](/about/purpose-history/communities/grants-corporate-giving/target-circle-community-giving)
      * [Twin Cities Market](/about/purpose-history/communities/twin-cities-market)
    - [Our Cor
```


## Sinais / observações

- **1 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)

## Interpretação para a tese

- 🚨 **2026-03-03** matched `dividend` → Dividend declaration: _[Target Corporation Declares Regular Quarterly Dividend](/press/release/2026/03/_
- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
