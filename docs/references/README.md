# Research References

PDFs de research profissional que servem como *anchors* de estilo, estrutura
analítica e ideias de *tickers* para o sistema.

**IMPORTANTE:** estes documentos são de distribuição restrita das respectivas
casas (Suno, XP, BTG Pactual). Mantêm-se aqui apenas para uso pessoal como
fonte de consulta. Não redistribuir.

## Conteúdo

| Ficheiro | Casa | Tipo | Valor analítico |
|---|---|---|---|
| `2026-04-02_suno_tese_itsa4.pdf` | Suno Research | Tese profunda (28pp) | **Padrão-ouro de deep dive.** Estrutura: Opinião → Resultados → História → Modelo → Setor → Financeira → Governança → Perspectivas → Valuation (SOTP) → Riscos → Conclusão. Ancorado em preço-teto. |
| `2026-04-02_suno_dividendos_ed23.pdf` | Suno Research | Update mensal (5pp) | Formato de comunicação de *mudança de preço-teto*. Estrutura de 3 argumentos numerados com números concretos. |
| `2026-04-02_suno_carteiras.pdf` | Suno Research | Listas de carteiras | Fonte das recomendações Suno Dividendos / Suno Ações / Suno FIIs usadas no `research_pool` do `universe.yaml`. |
| `2026-04-02_xp_top_dividendos.pdf` | XP Research | Brief mensal (7pp) | Estrutura de *relatório executivo* — cover + performance + comentários. Inspirou `executive_report.py`. |
| `2025-xx_btg_portfolio_solutions_fias.pdf` | BTG Pactual | Institucional (33pp) | Mostra múltiplas estratégias (Dividendos / Equity Brazil / Value) com *screening criteria* explícitos. Fonte para consenso cruzado. |

## Como estes PDFs influenciam o sistema

1. **Estrutura dos outputs**: o `executive_report.py` e o futuro *deep-dive*
   replicam as secções destes documentos.
2. **Watchlist consenso**: o `universe.yaml` tem um campo `sources` em cada
   ticker documentando quais casas o recomendam. Consenso entre casas
   (3+) é tratado como sinal forte.
3. **Preço-teto como âncora**: o conceito de *preço-teto* da Suno substitui
   pills "BUY/HOLD/SELL" nos outputs.
4. **SOTP para holdings**: a metodologia de *Soma das Partes* da tese de
   ITSA4 é o template para qualquer holding futura.

## Log

- 2026-04-15: arquivo inicial criado com os 5 PDFs acima.
