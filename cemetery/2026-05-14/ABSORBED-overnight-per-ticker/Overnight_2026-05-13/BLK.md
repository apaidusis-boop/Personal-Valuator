# BLK — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://ir.blackrock.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=2.0 · entry=897.695 · date=2024-01-29

- Total events na DB: **15**
- deep_fundamentals (rows anuais): **4**
- Última cotação DB: 2026-05-11 → close=1081.3199462890625
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.118990004 · DY=0.01975363542798272 · P/E=27.237278
- Score (último run): score=0.2 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-06 | 10-Q | sec | 10-Q |
| 2026-04-14 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |
| 2026-04-10 | proxy | sec | DEF 14A |
| 2026-04-03 | 8-K | sec | 8-K \| 1.01,2.03,9.01 |
| 2026-02-25 | 10-K | sec | 10-K |

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
