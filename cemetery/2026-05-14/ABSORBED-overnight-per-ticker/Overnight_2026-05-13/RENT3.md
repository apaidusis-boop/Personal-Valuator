# RENT3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Industrials
- **RI URLs scraped** (1):
  - https://ri.localiza.com/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **14**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=47.02000045776367
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.0853 · DY=0.04379319395901885 · P/E=22.714977
- Score (último run): score=0.2 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-29 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-04-22 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-28 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Juros sobre o capital pró |
| 2026-03-25 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-03-24 | fato_relevante | cvm | Juros sobre o Capital Próprio |

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
