# MCD — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Consumer Disc.
- **RI URLs scraped** (1):
  - https://corporate.mcdonalds.com/corpmcd/investors.html
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **165**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=274.6000061035156
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.026438455348261013 · P/E=22.638088
- Score (último run): score=0.6667 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-07 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-05-07 | 10-Q | sec | 10-Q |
| 2026-04-07 | proxy | sec | DEF 14A |
| 2026-02-24 | 10-K | sec | 10-K |
| 2026-02-11 | 8-K | sec | 8-K \| 2.02,9.01 |

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
