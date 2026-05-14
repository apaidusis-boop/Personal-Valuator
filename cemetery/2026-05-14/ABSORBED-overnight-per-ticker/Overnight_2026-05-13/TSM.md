# TSM — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investor.tsmc.com/english
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=5.0 · entry=102.47 · date=2020-11-16

- Total events na DB: **864**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=404.5400085449219
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.3621 · DY=0.010750481801893442 · P/E=34.605648
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 6-K | sec | 6-K |
| 2026-05-08 | 6-K | sec | 6-K |
| 2026-04-24 | 6-K | sec | 6-K |
| 2026-04-17 | 6-K | sec | 6-K |
| 2026-04-16 | 20-F | sec | 20-F |

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
