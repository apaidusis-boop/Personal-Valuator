# XPML11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Shopping
- **RI URLs scraped** (1):
  - https://www.fiis.com.br/xpml11/
- **Pilot rationale**: fii_heuristic (holding)

## Antes (estado da DB)

**Posição activa**: qty=159.0 · entry=108.73 · date=2026-05-07

- Total events na DB: **1**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=106.26000213623047
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=None · DY=0.10388255014194364 · P/E=None
- Score (último run): score=0.8 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-27 | data_repair | manual | Removed 3 corrupt price rows (Jan 14-16, 2026) from yfinance — close was R$1.07  |

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
