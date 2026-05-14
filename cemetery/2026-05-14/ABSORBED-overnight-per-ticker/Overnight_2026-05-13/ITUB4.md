# ITUB4 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Banks
- **RI URLs scraped** (1):
  - https://www.itau.com.br/relacoes-com-investidores/
- **Pilot rationale**: known (watchlist)

## Antes (estado da DB)

**Posição activa**: (nenhuma — watchlist ou holding sem qty)

- Total events na DB: **7**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=40.33000183105469
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.21816 · DY=0.0845453966078045 · P/E=9.788836
- Score (último run): score=0.8 · passes_screen=0

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-14 | fato_relevante | cvm | Ajustes contábeis nas Demonstrações Financeiras auditadas da Aegea |
| 2026-03-25 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Apresentação Instituciona |
| 2026-03-17 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Teleconferência - Resultados em F |
| 2026-03-16 | fato_relevante | cvm | Pagamento de Juros sobre capital próprio |
| 2026-02-10 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Apresentação Instituciona |

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
