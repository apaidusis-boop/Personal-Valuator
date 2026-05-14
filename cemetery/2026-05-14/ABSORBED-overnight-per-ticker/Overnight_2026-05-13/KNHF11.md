# KNHF11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Híbrido
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/knhf11/
- **Pilot rationale**: fii_heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: qty=175.0 · entry=98.56 · date=2026-05-08

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **2**
- Última cotação DB: 2026-05-11 → close=97.25
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.11311053984575835 · P/E=7.6214733
- Score (último run): score=0.8 · passes_screen=0
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
