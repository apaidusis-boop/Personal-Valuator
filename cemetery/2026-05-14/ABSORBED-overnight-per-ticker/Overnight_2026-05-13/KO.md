# KO — Pilot Deep Dive (2026-05-12)

- **Market**: US
- **Sector**: Consumer Staples
- **RI URLs scraped** (1):
  - https://investors.coca-colacompany.com/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=10.97119 · entry=75.91701538301679 · date=2026-04-13

- Total events na DB: **154**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=78.66000366210938
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.43372002 · DY=0.03292651766360909 · P/E=24.73585
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-05-01 | 8-K | sec | 8-K \| 5.07 |
| 2026-04-30 | 10-Q | sec | 10-Q |
| 2026-04-28 | 8-K | sec | 8-K \| 2.02,9.01 |
| 2026-03-16 | proxy | sec | DEF 14A |
| 2026-02-20 | 10-K | sec | 10-K |

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
