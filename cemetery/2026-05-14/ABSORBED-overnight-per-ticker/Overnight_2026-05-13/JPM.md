# JPM — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (2):
  - https://www.jpmorganchase.com/ir
  - https://www.jpmorganchase.com/ir/quarterly-earnings
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=7.0 · entry=306.55571428571426 · date=2025-09-25

- Total events na DB: **28**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=300.0
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.16465001 · DY=0.01966666666666667 · P/E=14.367817
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-07 | 8-K | sec | 8-K \| 3.03,5.03,8.01,9.01 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-24 | 8-K | sec | 8-K \| 5.03 |
| 2026-04-23 | 8-K | sec | 8-K \| 8.01,9.01 |
| 2026-04-14 | 8-K | sec | 8-K \| 2.02,9.01 |

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
