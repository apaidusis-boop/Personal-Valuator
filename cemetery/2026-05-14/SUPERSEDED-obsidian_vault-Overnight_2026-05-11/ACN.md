# ACN — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investor.accenture.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=4.30506 · entry=213.70666146348714 · date=2023-09-28

- Total events na DB: **44**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=180.4199981689453
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.24763 · DY=0.017237556986824682 · P/E=14.788525
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-24 | 8-K | sec | 8-K \| 1.01,1.02,2.03,9.01 |
| 2026-03-19 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-19 | 10-Q | sec | 10-Q |
| 2026-01-28 | 8-K | sec | 8-K \| 5.02,5.07,9.01 |
| 2025-12-18 | 8-K | sec | 8-K \| 2.02,9.01 |

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
