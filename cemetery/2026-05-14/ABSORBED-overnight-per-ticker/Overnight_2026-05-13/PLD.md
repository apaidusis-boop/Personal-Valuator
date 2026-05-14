# PLD — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: REIT
- **RI URLs scraped** (1):
  - https://ir.prologis.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=2.0 · entry=109.22 · date=2023-10-17

- Total events na DB: **158**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=144.07000732421875
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.06844 · DY=0.03588533169409301 · P/E=36.198494
- Score (último run): score=0.6667 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | 10-Q | sec | 10-Q |
| 2026-04-30 | 8-K | sec | 8-K \| 5.07,9.01 |
| 2026-04-27 | 8-K | sec | 8-K \| 2.03,8.01,9.01 |
| 2026-04-23 | 8-K | sec | 8-K \| 2.03,8.01,9.01 |
| 2026-04-16 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |

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
