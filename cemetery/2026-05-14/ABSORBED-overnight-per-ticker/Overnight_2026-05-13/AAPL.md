# AAPL — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investor.apple.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=5.0 · entry=121.89000000000001 · date=2020-11-16

- Total events na DB: **160**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=292.67999267578125
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=1.4147099 · DY=0.004441711194929836 · P/E=35.390564
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-30 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-20 | 8-K | sec | 8-K \| 5.02 |
| 2026-02-24 | 8-K | sec | 8-K \| 5.07,9.01 |
| 2026-01-30 | 10-Q | sec | 10-Q |

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
