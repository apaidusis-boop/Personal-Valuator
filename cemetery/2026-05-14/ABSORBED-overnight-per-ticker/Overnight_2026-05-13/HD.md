# HD — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://ir.homedepot.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1.0 · entry=292.02 · date=2023-10-12

- Total events na DB: **140**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=311.3999938964844
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=1.45541 · DY=0.029640334556551847 · P/E=21.898733
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-07 | proxy | sec | DEF 14A |
| 2026-03-18 | 10-K | sec | 10-K |
| 2026-02-24 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2025-11-25 | 10-Q | sec | 10-Q |
| 2025-11-24 | 8-K | sec | 8-K \| 5.03,8.01,9.01 |

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
