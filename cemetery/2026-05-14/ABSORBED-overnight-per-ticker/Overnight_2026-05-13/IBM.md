# IBM — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://www.ibm.com/investor
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **148**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=223.5500030517578
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.35772 · DY=0.030105121485692058 · P/E=19.783186
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.02,5.03,5.07 |
| 2026-04-23 | 10-Q | sec | 10-Q |
| 2026-04-22 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-10 | proxy | sec | DEF 14A |
| 2026-03-03 | 8-K | sec | 8-K \| 5.03,9.01 |

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
