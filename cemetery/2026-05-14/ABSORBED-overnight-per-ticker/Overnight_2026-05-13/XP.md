# XP — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investors.xpinc.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=20.0 · entry=17.355 · date=2026-01-15

- Total events na DB: **140**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=18.665000915527344
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.23715 · DY=0.009643717716094976 · P/E=9.47462
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-06 | 6-K | sec | 6-K |
| 2026-04-29 | 20-F | sec | 20-F |
| 2026-02-23 | 6-K | sec | 6-K |
| 2026-02-12 | 6-K | sec | 6-K |
| 2026-02-12 | 6-K | sec | 6-K |

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
