# O — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: REIT
- **RI URLs scraped** (1):
  - https://www.realtyincome.com/investors
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=30.0 · entry=63.56333333333334 · date=2026-04-13

- Total events na DB: **276**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=62.36000061035156
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.02831 · DY=0.05192430994720842 · P/E=51.114754
- Score (último run): score=1.0 · passes_screen=1
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-05-07 | 10-Q | sec | 10-Q |
| 2026-05-06 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |
| 2026-04-07 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-03-31 | 8-K | sec | 8-K \| 8.01,9.01 |

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
