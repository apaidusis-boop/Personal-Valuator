# ABBV — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Healthcare
- **RI URLs scraped** (1):
  - https://investors.abbvie.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: qty=7.46602 · entry=200.91025740622177 · date=2026-04-23

- Total events na DB: **183**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=202.77999877929688
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.03323799211250479 · P/E=99.40196
- Score (último run): score=0.8 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 10-Q | sec | 10-Q |
| 2026-04-29 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-04-03 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-23 | proxy | sec | DEF 14A |
| 2026-03-04 | 8-K | sec | 8-K \| 8.01,9.01 |

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
