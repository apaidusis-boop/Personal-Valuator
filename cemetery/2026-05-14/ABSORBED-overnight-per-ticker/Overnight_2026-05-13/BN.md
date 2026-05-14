# BN — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://bn.brookfield.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=7.0 · entry=25.56142857142857 · date=2023-07-19

- Total events na DB: **343**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=46.34000015258789
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.01951 · DY=0.005394907189831733 · P/E=94.57143
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-04 | 6-K | sec | 6-K |
| 2026-04-22 | 6-K | sec | 6-K |
| 2026-04-17 | 6-K | sec | 6-K |
| 2026-04-14 | 6-K | sec | 6-K |
| 2026-03-18 | 6-K | sec | 6-K |

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
