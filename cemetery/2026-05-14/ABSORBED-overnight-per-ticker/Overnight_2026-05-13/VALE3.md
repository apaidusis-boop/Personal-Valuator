# VALE3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Mining
- **RI URLs scraped** (1):
  - https://vale.com/pt/investidores
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=501.0 · entry=61.84 · date=2026-05-07

- Total events na DB: **42**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=83.44999694824219
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.068390004 · DY=0.06563401078848538 · P/E=25.598158
- Score (último run): score=0.6 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-30 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Vale esclarece sobre notí |
| 2026-04-29 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Desempenho da Vale no 1T26 |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atualização sobre negocia |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Atualização sobre negocia |
| 2026-04-16 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Relatório de produção e v |

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
