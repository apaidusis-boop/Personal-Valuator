# PRIO3 — Pilot Deep Dive (2026-05-12)

- **Market**: BR
- **Sector**: Oil & Gas
- **RI URLs scraped** (2):
  - https://ri.prio3.com.br/
  - https://ri.prio3.com.br/servicos-aos-investidores/comunicados-e-fatos-relevantes/
- **Pilot rationale**: known (holding)

## Antes (estado da DB)

**Posição activa**: qty=503.0 · entry=39.85 · date=2026-05-07

- Total events na DB: **33**
- deep_fundamentals (rows anuais): **5**
- Última cotação DB: 2026-05-11 → close=63.630001068115234
- Último fundamentals snapshot: period_end=2026-05-11 · ROE=0.09729999 · DY=None · P/E=20.199999
- Score (último run): score=0.25 · passes_screen=0
- Thesis health: status=- (-)

**Últimos 5 events em DB**:

| Data | Kind | Source | Summary |
|---|---|---|---|
| 2026-04-13 | comunicado | cvm | Aquisição/Alienação de Participação Acionária (art. 12 da Instr. CVM nº 358) \| D |
| 2026-04-08 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - Març |
| 2026-04-07 | comunicado | cvm | Apresentações a analistas/agentes do mercado \| Apresentação Institucional - Març |
| 2026-04-06 | fato_relevante | cvm | Produção do Terceiro Poço de Wahoo |
| 2026-04-01 | comunicado | cvm | Outros Comunicados Não Considerados Fatos Relevantes \| Dados Operacionais - Març |

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
