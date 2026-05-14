# CMIG4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.cemig.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-11 → close=11.800000190734863
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.10754542199045243 · P/E=6.8208094
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
