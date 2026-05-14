# SLCE3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://slc.com.br/ri/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-11 → close=17.389999389648438
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.11582 · DY=0.04630046165954912 · P/E=15.526785
- Score (último run): score=0.2 · passes_screen=0

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
