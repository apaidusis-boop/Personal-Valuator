# ENGI11 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Utilities
- **RI URLs scraped** (1):
  - https://ri.energisa.com.br/
- **Pilot rationale**: heuristic (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **21**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=51.79999923706055
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.14495 · DY=0.02985530932003462 · P/E=37.536232
- Score (último run): score=0.0 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-24 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Boletim de Relações com I |
| 2026-04-22 | fato_relevante | cvm | Assinatura de memorando de entendimentos para subscrição e integralização de açõ |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Aneel homologa reajuste t |
| 2026-04-22 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Aneel homologa reajuste t |
| 2026-04-22 | fato_relevante | cvm | Assinatura de memorando de entendimentos para subscrição e integralização de açõ |

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
