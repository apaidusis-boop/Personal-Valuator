# TEN — Pilot Deep Dive (2026-05-10)

- **Market**: US
- **Sector**: Energy
- **RI URLs scraped** (1):
  - https://investors.tsakoshellenicgroup.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=35.0 · entry=23.928 · date=2025-11-12

- Total events na DB: **204**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-08 → close=43.79999923706055
- Último fundamentals snapshot: period_end=2026-05-09 · ROE=0.09087 · DY=0.013698630375598757 · P/E=9.842697
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-17 | 6-K | sec | 6-K |
| 2026-04-06 | 20-F | sec | 20-F |
| 2026-03-06 | 6-K | sec | 6-K |
| 2025-11-21 | 6-K | sec | 6-K |
| 2025-10-30 | 6-K | sec | 6-K |

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
