# KLBN11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Materials
- **RI URLs scraped** (1):
  - https://ri.klabin.com.br/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1059.0 · entry=18.29 · date=2026-05-07

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=17.0
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.05465 · DY=0.09624211764705881 · P/E=25.718607
- Score (último run): score=0.0 · passes_screen=0
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
