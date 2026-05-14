# WIZC3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Insurance
- **RI URLs scraped** (2):
  - https://ri.wizsolucoes.com.br/
  - https://ri.wizco.com.br/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **0**
- deep_fundamentals (rows anuais): **0**
- Última cotação DB: 2026-05-11 → close=7.940000057220459
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.29974002 · DY=0.0791848860792197 · P/E=6.3015876
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
