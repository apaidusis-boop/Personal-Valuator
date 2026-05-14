# JNJ — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Healthcare
- **RI URLs scraped** (1):
  - https://www.investor.jnj.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=10.0 · entry=238.28000000000003 · date=2026-04-14

- Total events na DB: **142**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=221.42999267578125
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.26416 · DY=0.029354650295804002 · P/E=25.658169
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-28 | 8-K | sec | 8-K \| 5.07,9.01 |
| 2026-04-22 | 10-Q | sec | 10-Q |
| 2026-04-14 | 8-K | sec | 8-K \| 2.02,8.01,9.01 |
| 2026-03-11 | proxy | sec | DEF 14A |
| 2026-02-11 | 10-K | sec | 10-K |

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
