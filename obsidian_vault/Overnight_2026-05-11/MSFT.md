# MSFT — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://www.microsoft.com/en-us/investor
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **98**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=415.1199951171875
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.34013999 · DY=0.008383118233121012 · P/E=24.753725
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-29 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-29 | 10-Q | sec | 10-Q |
| 2026-01-28 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-01-28 | 10-Q | sec | 10-Q |
| 2025-12-08 | 8-K | sec | 8-K \| 5.02,5.07 |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 8.9s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.microsoft.com/en-us/investor | ✅ | 8.9s | 20,063 |
- Filings extraídos do RI: **2**
- Eventos calendário: **0**
- Apresentações/releases: **1**
- Audio/video: **1**
- Headers detectados (structure): **15**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 2026-04-29 | Microsoft FY26 Q3 Earnings |
| 2026-04-28 | Microsoft announces quarterly dividend |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (1 total, top 1)

- [Investor Relations](https://www.microsoft.com/en-us/investor/default)

### Audio / Video disponível (markitdown pode ler)

- [Press Release & Webcast](https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q3/press-release-webcast)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 98 | 98 + 2 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 1 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**2 filings detectados como novos vs DB.**

### 1. 2026-04-29 — Microsoft FY26 Q3 Earnings

URL: https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/press-release-webcast
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
This is the Trace Id: 7a3f68057fcbf980b31042ede0efce45

![]()

Skip to main content

[![](https://uhf.microsoft.com/images/microsoft/RE1Mu3b.png)
Microsoft](https://www.microsoft.com)

Investor Relations

[Investor Relations](/en-us/Investor/default)

Investor Relations

* [Home](/en-us/Investor/default)
* Investor Relations
  + [Home](/en-us/Investor/default)
  + [Board & ESG](/en-us/Investor/corporate-governance/overview)
  + [Annual Reports](/en-us/Investor/annual-reports)
  + [SEC Filings](/en-us/Investor/sec-filings)
  + [Events](/en-us/Investor/events/default)
  + [Investor Information](/en-us/Investor/investor-information)
  + [Contacts](/en-us/Investor/contact-information)
* Earnings Releases
  + [Press Release & Webcast](/en-us/Investor/earnings/FY-2026-Q3/press-release-webcast)
  + Financial Statements
    Financial Statements
    - [Income Statements](/en-us/Investor/earnings/FY-2026-Q3/income-statements)
    - [Comprehensive Income](/en-us/Investor/earnings/FY-2026-Q3/comprehensive-income)
    - [Balance Sheets](/en-us/Investor/earnings/FY-2026-Q3/balance-sheets)
    - [Cash Flows](/en-us/Investor/earnings/FY-2026-Q3/cash-flows)
    - [Segment Results](/en-us/Investor/earnings/FY-2026-Q3/segment-revenues)
  + [Performance](/en-us/Investor/earnings/FY-2026-Q3/performance)
  + [Metrics](/en-us/Investor/earnings/FY-2026-Q3/metrics)
  + Segment Performance
    Segment Performance
    - [Productivity and Business Processes](/en-us/Investor/earnings/FY-2026-Q3/productiv
```

### 2. 2026-04-28 — Microsoft announces quarterly dividend

URL: https://www.microsoft.com/content/dam/microsoft/invst/general/images/icons/fileiconsvg.svg
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<!-- Uploaded to: SVG Repo, www.svgrepo.com, Transformed by: SVG Repo Mixer Tools -->
<svg width="64px" height="64px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="SVGRepo_bgCarrier" stroke-width="0"/>
<g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"/>
<g id="SVGRepo_iconCarrier"> <path d="M19 9V17.8C19 18.9201 19 19.4802 18.782 19.908C18.5903 20.2843 18.2843 20.5903 17.908 20.782C17.4802 21 16.9201 21 15.8 21H8.2C7.07989 21 6.51984 21 6.09202 20.782C5.71569 20.5903 5.40973 20.2843 5.21799 19.908C5 19.4802 5 18.9201 5 17.8V6.2C5 5.07989 5 4.51984 5.21799 4.09202C5.40973 3.71569 5.71569 3.40973 6.09202 3.21799C6.51984 3 7.0799 3 8.2 3H13M19 9L13 3M19 9H14C13.4477 9 13 8.55228 13 8V3" stroke="#0067B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/> </g>
</svg>
```


## Sinais / observações

- **2 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **1 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🚨 **2026-04-28** matched `dividend` → Dividend declaration: _Microsoft announces quarterly dividend_
- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 📊 **Cross-check fundamentals**: RI tem 1 releases/relatórios — podemos auditar se ROE=0.34013999, DY=0.008383118233121012 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
