# TSLA — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://ir.tesla.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=3.0 · entry=186.40333333333334 · date=2020-11-24

- Total events na DB: **168**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=445.0
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.04901 · DY=None · P/E=415.88782
- Score (último run): score=0.0 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-23 | 10-Q | sec | 10-Q |
| 2026-04-22 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-02 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-01-29 | 10-K | sec | 10-K |
| 2026-01-28 | 8-K | sec | 8-K \| 2.02,9.01 |

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
