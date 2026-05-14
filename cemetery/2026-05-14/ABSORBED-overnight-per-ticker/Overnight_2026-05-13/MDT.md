# MDT — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Healthcare
- **RI URLs scraped** (1):
  - https://investorrelations.medtronic.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **4**
- Última cotação DB: 2026-05-11 → close=74.54000091552734
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.0939 · DY=0.03810034833804788 · P/E=20.82123
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
