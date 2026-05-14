# PVBI11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Corporativo
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/pvbi11/
- **Pilot rationale**: fii_heuristic (holding)

## Antes (estado da DB)

**Posição activa**: qty=217.0 · entry=79.04 · date=2026-05-07

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **4**
- Última cotação DB: 2026-05-11 → close=75.05999755859375
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.06128430788195966 · P/E=8.002131
- Score (último run): score=0.4 · passes_screen=0
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
