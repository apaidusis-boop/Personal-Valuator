# V — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investor.visa.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **229**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=323.8599853515625
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.60349 · DY=0.007781140350711876 · P/E=28.210802
- Score (último run): score=0.4 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-11 | 8-K | sec | 8-K \| 7.01,9.01 |
| 2026-04-29 | 10-Q | sec | 10-Q |
| 2026-04-28 | 8-K | sec | 8-K \| 2.02,8.01,9.01 |
| 2026-02-27 | 8-K | sec | 8-K \| 8.01 |
| 2026-02-13 | 8-K | sec | 8-K \| 7.01 |

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
