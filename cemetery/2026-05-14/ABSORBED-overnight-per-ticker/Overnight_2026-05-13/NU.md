# NU — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Financials
- **RI URLs scraped** (1):
  - https://investors.nu/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=13.0 · entry=8.25923076923077 · date=2023-12-18

- Total events na DB: **152**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=13.5
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.30278 · DY=None · P/E=22.881357
- Score (último run): score=0.25 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-09 | 6-K | sec | 6-K |
| 2026-04-08 | 20-F | sec | 20-F |
| 2026-02-25 | 6-K | sec | 6-K |
| 2026-02-25 | 6-K | sec | 6-K |
| 2026-02-25 | 6-K | sec | 6-K |

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
