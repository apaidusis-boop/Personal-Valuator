# RBRX11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Híbrido
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/rbrx11/
- **Pilot rationale**: fii_heuristic (holding)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **4**
- Última cotação DB: 2026-05-11 → close=8.670000076293945
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.1252790069713922 · P/E=33.346157
- Score (último run): score=1.0 · passes_screen=1
- Thesis health: status=- (-)

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
