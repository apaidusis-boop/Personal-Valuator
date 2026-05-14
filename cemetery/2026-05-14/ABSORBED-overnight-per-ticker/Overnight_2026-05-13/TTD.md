# TTD — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Communication
- **RI URLs scraped** (1):
  - https://investors.thetradedesk.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **134**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=21.520000457763672
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.16735001 · DY=None · P/E=24.454546
- Score (último run): score=0.25 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 8-K | sec | 8-K \| 5.02 |
| 2026-05-08 | 8-K | sec | 8-K \| 5.07 |
| 2026-05-07 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-05-07 | 10-Q | sec | 10-Q |
| 2026-04-20 | 8-K | sec | 8-K \| 1.01,2.03 |

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
