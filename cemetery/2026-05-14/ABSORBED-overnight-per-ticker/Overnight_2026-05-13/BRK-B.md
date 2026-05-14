# BRK-B — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Holding
- **RI URLs scraped** (1):
  - https://www.berkshirehathaway.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1.0 · entry=417.99 · date=2024-03-28

- Total events na DB: **124**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=479.54998779296875
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.10499 · DY=None · P/E=14.272322
- Score (último run): score=0.5 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-07 | 8-K | sec | 8-K \| 2.02,5.02,5.03,5.07,9.01 |
| 2026-05-04 | 10-Q | sec | 10-Q |
| 2026-04-16 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-03-13 | proxy | sec | DEF 14A |
| 2026-03-05 | 8-K | sec | 8-K \| 8.01,9.01 |

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
