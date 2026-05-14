# AWR — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Utilities
- **RI URLs scraped** (2):
  - https://ir.americanstateswater.com/
  - https://www.aswater.com/investors
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=77.1500015258789
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.13221 · DY=0.02563836631080956 · P/E=22.492712
- Score (último run): score=0.6 · passes_screen=0

**Últimos 5 events em DB**:

_(zero events em DB)_

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
