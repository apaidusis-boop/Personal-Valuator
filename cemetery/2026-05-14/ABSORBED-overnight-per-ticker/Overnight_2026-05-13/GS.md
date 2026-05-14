# GS — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://www.goldmansachs.com/investor-relations/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1.0 · entry=318.83 · date=2023-07-11

- Total events na DB: **20**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=944.8599853515625
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.14548 · DY=0.021167157367298628 · P/E=17.248266
- Score (último run): score=0.4 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.07 |
| 2026-05-01 | 10-Q | sec | 10-Q |
| 2026-04-20 | 8-K | sec | 8-K \| 9.01 |
| 2026-04-13 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |
| 2026-03-20 | proxy | sec | DEF 14A |

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
