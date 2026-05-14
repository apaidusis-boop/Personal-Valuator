# VRTA11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Papel (CRI)
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/vrta11/
- **Pilot rationale**: fii_heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-11 → close=76.04000091552734
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.081949994 · DY=0.1341399247394954 · P/E=11.291951
- Score (último run): score=1.0 · passes_screen=1

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
