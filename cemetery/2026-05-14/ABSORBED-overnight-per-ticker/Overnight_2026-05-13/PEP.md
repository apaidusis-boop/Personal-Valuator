# PEP — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://investor.pepsico.com/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **211**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-11 → close=149.41000366210938
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.43879002 · DY=0.03809651201717694 · P/E=23.45526
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-08 | 8-K | sec | 8-K \| 5.07 |
| 2026-04-16 | 10-Q | sec | 10-Q |
| 2026-04-16 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-27 | proxy | sec | DEF 14A |
| 2026-02-11 | 8-K | sec | 8-K \| 8.01,9.01 |

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
