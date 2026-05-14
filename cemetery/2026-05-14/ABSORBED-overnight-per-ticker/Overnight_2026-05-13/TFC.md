# TFC — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://ir.truist.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **117**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=47.970001220703125
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.08579001 · DY=0.0433604325009336 · P/E=11.873763
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.02,5.07,9.01 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-23 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-04-17 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-16 | proxy | sec | DEF 14A |

## Agora (RI scrape live)

- Scrape: ❌ FALHOU — Traceback (most recent call last):
  File "C:\Users\paidu\investment-intelligence\fetchers\portal_playwright.py", line 233, in <module>
    main()
    ~~~~^^
  File "C:\Users\paidu\investment-intelligence\fetchers\portal_playwright.py", line 220, in main
    result = fetch(
        args.url,
    ...<5 lines>...
        headless=not args.no_headless,
    )
  File "C:\Users\paidu\investment-intellig
