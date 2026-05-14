# PG — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://www.pginvestor.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=10.0 · entry=142.76 · date=2026-04-13

- Total events na DB: **111**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=143.36000061035156
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.31112 · DY=0.029715401659201716 · P/E=20.959064
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
