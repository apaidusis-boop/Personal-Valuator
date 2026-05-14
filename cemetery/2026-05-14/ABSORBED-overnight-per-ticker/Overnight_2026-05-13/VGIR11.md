# VGIR11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Papel (CRI)
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/vgir11/
- **Pilot rationale**: fii_heuristic (holding)

## Antes (estado da DB)

**Posição activa**: qty=1776.0 · entry=9.72 · date=2026-05-07

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-11 → close=9.850000381469727
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.15532994322297758 · P/E=None
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
