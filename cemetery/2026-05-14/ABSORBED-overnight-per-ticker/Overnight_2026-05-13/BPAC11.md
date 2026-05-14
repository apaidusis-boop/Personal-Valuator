# BPAC11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Banks
- **RI URLs scraped** (1):
  - https://ri.btgpactual.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-04-24 → close=60.880001068115234
- Último fundamentals snapshot: period_end=2026-04-25 · ROE=0.23868 · DY=0.020489585711477683 · P/E=99.15309

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
