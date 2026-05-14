# BTLG11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Logística
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/btlg11/
- **Pilot rationale**: fii_heuristic (holding)

## Antes (estado da DB)

**Posição activa**: qty=166.0 · entry=103.3 · date=2026-05-07

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-11 → close=103.0999984741211
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.08615 · DY=0.09173541357882765 · P/E=95.198524
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
