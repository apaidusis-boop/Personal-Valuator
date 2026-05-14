# PLTR — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Technology
- **RI URLs scraped** (1):
  - https://investors.palantir.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=1.8673199999999999 · entry=80.32902769744875 · date=2024-11-15

- Total events na DB: **72**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=136.88999938964844
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.32587 · DY=None · P/E=152.1
- Score (último run): score=0.25 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-05 | 10-Q | sec | 10-Q |
| 2026-05-04 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |
| 2026-04-24 | proxy | sec | DEF 14A |
| 2026-02-17 | 10-K | sec | 10-K |
| 2026-02-02 | 8-K | sec | 8-K \| 2.02,7.01,9.01 |

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
