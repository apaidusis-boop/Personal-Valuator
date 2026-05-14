# GS — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://www.goldmansachs.com/investor-relations/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1.0 · entry=318.83 · date=2023-07-11

- Total events na DB: **20**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=936.47998046875
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.14548 · DY=0.021356569726123893 · P/E=17.095291
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.07 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-20 | 8-K | sec | 8-K \| 9.01 |
| 2026-04-13 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |
| 2026-03-20 | proxy | sec | DEF 14A |

## Agora (RI scrape live)

- Scrape: ✅ **1/1 URLs OK** · total 26.8s

| URL | OK | Time | MD chars |
|---|---|---|---|
| https://www.goldmansachs.com/investor-relations/ | ✅ | 26.8s | 17,999 |
- Filings extraídos do RI: **8**
- Eventos calendário: **0**
- Apresentações/releases: **3**
- Audio/video: **1**
- Headers detectados (structure): **7**

### Filings detectados no RI (top 10)

| Data | Título |
|---|---|
| 2026-04-13 | View Press Release |
| 2026-04-13 | 2026 First Quarter Earnings Results |
| Mar 20, 2026 | 2026 Proxy Statement for our Annual Meeting of Shareholders |
| Mar 20, 2026 | 2025 Annual Report |
| Feb 25, 2026 | 2025 Form 10-K |
| 2026-01-15 | Goldman Sachs Reports 2025 Full Year and Fourth Quarter Earnings Results |
| 2025-10-14 | Goldman Sachs Reports 2025 Third Quarter Earnings Per Common Share of $12.25 and |
| 2025-07-16 | Goldman Sachs Reports 2025 Second Quarter Earnings Per Common Share of $10.91 an |

### Próximos eventos (calendário RI)

_(nenhum evento de calendário detectado)_

### Apresentações / releases disponíveis (3 total, top 3)

- [Investor Relations](https://www.goldmansachs.com/investor-relations)
- [2026 First Quarter Earnings Results Presentation](https://www.goldmansachs.com/pressroom/press-releases/current/pdfs/2026-q1-earnings-results-presentation.pdf)
- [Browse All Presentations](https://www.goldmansachs.com/investor-relations/presentations)

### Audio / Video disponível (markitdown pode ler)

- [Access Webcast](https://www.goldmansachs.com/investor-relations/presentations/2026/broadcast-first-quarter-2026)

## Diff: o que mudou (Antes → Agora)

| Dimensão | Antes | Agora | Δ |
|---|---|---|---|
| Filings na DB | 20 | 20 + 5 novos no RI | + |
| Próximos eventos conhecidos | 0 | 0 | = |
| Apresentações .pdf detectadas | 0 | 3 | + |
| Audio/video acessível | 0 (era cego) | 1 | + |
| Cross-check fundamentals com RI | Não disponível | Possível (não automatizado ainda) | + |

## Filings novos detectados (não estavam na DB)

**5 filings detectados como novos vs DB.**

### 1. 2026-04-13 — View Press Release

URL: https://www.goldmansachs.com/pressroom/press-releases/2026/2026-04-13-q1-results
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Alumni](https://www.goldmansachs.com/alumni)
* + [Alumni](https://www.goldmansachs.com/alumni)

* [Client Login](https://www.goldmansachs.com/login)
* [Client Login](https://www.goldmansachs.com/login)

* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Alumni](https://www.goldmansachs.com/alumni)
* + [Alumni](https://www.goldmansachs.com/alumni)

* [Client Login](https://www.goldmansachs.com/login)
* [Client Login](https://www.goldmansachs.com/login)

* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom
```

### 2. 2026-04-13 — 2026 First Quarter Earnings Results

URL: https://www.goldmansachs.com/pressroom/press-releases/current/pdfs/2026-q1-results.pdf
Após data máxima DB: (título não match em DB)

### 3. 2026-01-15 — Goldman Sachs Reports 2025 Full Year and Fourth Quarter Earnings Results

URL: https://www.goldmansachs.com/pressroom/press-releases/2026/2026-01-15-q4-results
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Alumni](https://www.goldmansachs.com/alumni)
* + [Alumni](https://www.goldmansachs.com/alumni)

* [Client Login](https://www.goldmansachs.com/login)
* [Client Login](https://www.goldmansachs.com/login)

* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Alumni](https://www.goldmansachs.com/alumni)
* + [Alumni](https://www.goldmansachs.com/alumni)

* [Client Login](https://www.goldmansachs.com/login)
* [Client Login](https://www.goldmansachs.com/login)

* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom
```

### 4. 2025-10-14 — Goldman Sachs Reports 2025 Third Quarter Earnings Per Common Share of $12.25 and Annualized Return on Common Equity of 14.2%

URL: https://www.goldmansachs.com/pressroom/press-releases/2025/2025-10-14-q3-results
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Alumni](https://www.goldmansachs.com/alumni)
* + [Alumni](https://www.goldmansachs.com/alumni)

* [Client Login](https://www.goldmansachs.com/login)
* [Client Login](https://www.goldmansachs.com/login)

* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Alumni](https://www.goldmansachs.com/alumni)
* + [Alumni](https://www.goldmansachs.com/alumni)

* [Client Login](https://www.goldmansachs.com/login)
* [Client Login](https://www.goldmansachs.com/login)

* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom
```

### 5. 2025-07-16 — Goldman Sachs Reports 2025 Second Quarter Earnings Per Common Share of $10.91 and Annualized Return on Common Equity of 12.8%

URL: https://www.goldmansachs.com/pressroom/press-releases/2025/2025-07-16-q2-results
Após data máxima DB: (título não match em DB)

**Extracção markitdown (preview 1500 chars):**

```
* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Alumni](https://www.goldmansachs.com/alumni)
* + [Alumni](https://www.goldmansachs.com/alumni)

* [Client Login](https://www.goldmansachs.com/login)
* [Client Login](https://www.goldmansachs.com/login)

* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Pressroom](https://www.goldmansachs.com/pressroom)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Worldwide](https://www.goldmansachs.com/worldwide)
* + [Alumni](https://www.goldmansachs.com/alumni)
* + [Alumni](https://www.goldmansachs.com/alumni)

* [Client Login](https://www.goldmansachs.com/login)
* [Client Login](https://www.goldmansachs.com/login)

* What We Do
* Insights
* Our Firm
* Careers

* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Investor Relations](https://www.goldmansachs.com/investor-relations)
* + [Pressroom](https://www.goldmansachs.com/pressroom
```


## Sinais / observações

- **5 filings descobertos** que CVM/SEC monitor ainda não trouxe → vantagem informacional
- **1 fontes audio/video** disponíveis (markitdown pode transcrever)
- **3 apresentações .pdf** disponíveis para extracção fundamentals/tese

## Interpretação para a tese

- 🎙️ **1 fontes audio/video** disponíveis para transcrição — earnings call/podcast pode revelar detalhes não em release escrito.
- 💼 **Posição activa**: qty=1.0, entry=318.83. 5 filings novos → revisitar tese se houver signal material acima.
- 📊 **Cross-check fundamentals**: RI tem 3 releases/relatórios — podemos auditar se ROE=0.14548, DY=0.021356569726123893 batem com último report oficial.

## Próximas perguntas (research-on-gap)

- Wirar `events` table com filings novos detectados?
- Schedule re-scrape no dia/véspera de earnings?
- Cross-check fundamentals do RI vs nossa DB (delta material?)
