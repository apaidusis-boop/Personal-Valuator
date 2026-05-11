---
type: spec
scope: commercial
roadmap_block: B4
status: spec-only (build bloqueado — ver Dependências)
created: 2026-05-11
---

# 📄 Spec — Report Tier (o "relatório institucional")

> Bloco B4 de [[Comercial/00_Roadmap]]. Constituições: [[CONSTITUTION_Comercial]] (nº3: o "teatro" é um *tier de entrega*, não a substância) + [[CONSTITUTION_Pessoal]] (nº6: para mim, verdade comprimida — esta regra **inverte-se** aqui). Disciplina por baixo: [[Bibliotheca/Disciplina_de_Investidor]]. Segue o padrão `obsidian_vault/specs/<component>.spec.md` (spec-first).

## Purpose
Pegar no **output analítico que o sistema já produz** (deep-dive dossier, verdict, tese, fair value, peers, consensus) e **renderizá-lo num formato de relatório de nível institucional** — sem nova análise. É uma **camada de apresentação**, determinística a partir dos dados já calculados. O cliente Pro (ver [[Comercial/Pricing]]) quer ver "um relatório"; a substância por baixo é a disciplina que nenhum concorrente tem (ver [[Comercial/Competitive_Landscape]]).

**Mantra**: *a mesma verdade comprimida do núcleo, embrulhada* — não enchimento. Se a análise por baixo é rasa (ex: deepdive `--no-llm`), o relatório **di-lo**, não enche páginas.

## Dois tipos de relatório
Esqueleto destilado dos plugins FSI (ver [[Bibliotheca/Disciplina_de_Investidor]] §7 + memória `anthropic_fsi_plugins.md`), com thresholds *sãos* (não os 30-50 págs de teatro sell-side):

### A. Initiating Coverage (~8-12 págs) — *thesis-focused*
1. **Página 1 — caixa de rating + verdict**: ticker, nome, sector, market; verdict (BUY/HOLD/AVOID) + score + confiança; preço atual + fair value (banda) + upside/downside; 3-4 bullets paragraph-length com os pilares da tese; disclaimer (ver §Compliance).
2. **Tese de investimento (2-3 págs)**: 3-5 pilares, cada um com quantificação e o **gatilho de saída** ("morro se X" — pick #3 da disciplina). + secção de riscos.
3. **Visão da empresa (1-2 págs)**: descrição, sector positioning (2×2 do sector se existir — ver `wiki/sectors/`), management se relevante.
4. **Análise financeira (2-3 págs)**: 5 anos histórico + projeção, de `quarterly_history`/`deep_fundamentals`; margens, ROE/ROIC, dívida; trends. Tabelas com source line.
5. **Valuation (2 págs)**: fair value v2 (`scoring/fair_value.py`) + método; comps/percentis (`ii peers`); consensus blend (`scoring/consensus_target.py` — our_fair vs Suno/XP/WSJ); football field.
6. **Cenários (1 pág)**: bull/base/bear com parâmetros (reusa `drip_projection.py::derive_scenarios` + damper — não reinventar).
7. **Apêndice + Sources**: tabelas detalhadas; **secção de fontes com links clicáveis** (filings CVM/SEC de `events`, transcripts, etc.).

### B. Earnings Update (~6-8 págs) — *event-driven*
1. **Página 1 — beat/miss lidera**: bateu/falhou vs **a nossa estimativa E o consenso** (são diferentes), quantificado; 3 takeaways; rating mantido/alterado + lógica.
2. **Resultados detalhados (1-2 págs)**: breakdown segmento/geografia; bridge de margem com drivers +/−; progressão trimestral.
3. **Guidance & outlook (1 pág)**: novo vs antigo vs Street + "a nossa leitura".
4. **Impacto na tese (1-2 págs)**: por pilar — `strengthened` / `unchanged` / `weakened` (reusa o thesis scorecard, pick #3).
5. **Estimativas (1 pág)**: old→new com **razão por linha** (pick #4 — o template earnings-update). Fair value walk: old→new (de `fair_value` history, que já tem `trigger`).
6. **Sources** com links.

## Data sources (tudo já existe — ZERO novo fetching)
| Conteúdo | Vem de |
|---|---|
| Verdict + score + breakdown | `verdict_engine_breakdown` table; `ii verdict` |
| Auditor (Piotroski/Altman/Beneish/Moat) + Scout (news/insider/short/consensus) + Strategist dossier | `reports/deepdive/<TK>.json` (`ii deepdive`) |
| Pilares da tese + gatilhos de saída | `thesis_health` + thesis (pós pick #3 com scorecard) |
| Fair value (banda, action, confiança) + walk old→new | `fair_value` table (`our_fair`/`action`/`confidence_label` + history com `trigger`) |
| Financeiros 5y hist + proj | `quarterly_history` / `deep_fundamentals` |
| Peers / percentis | `ii peers` |
| Consensus blend | `scoring/consensus_target.py` |
| Filings (URLs p/ Sources) | `events` (source `cvm`/`sec`, `url`) |
| Cenários bull/base/bear | `drip_projection.py::derive_scenarios` |

## Render engine — decisão
Candidatos: (a) **HTML→PDF reusando o Design System (`design.lint`)** — `reports/*.html` já produz HTML standalone estilado; acrescentar passo de print-to-PDF; (b) Markdown→PDF (pandoc/weasyprint); (c) python-docx (igual aos FSI plugins, mas DOCX é menos web-native).
**Recomendação: (a)**. Consistente com "Escritório = polido, `design.lint` aplica-se" ([[CONSTITUTION_Pessoal]] nº4); produz **vista HTML in-app + PDF descarregável** num só pipeline; zero toolchain nova. DOCX export fica como add-on possível *se* clientes pedirem. Decisão final do toolchain: ao construir, não agora.

## Hierarchy intent
- **Hero** — página 1: verdict + caixa de rating + 3-4 bullets dos pilares. Lê-se em 30 segundos. Lidera *sempre* com a conclusão.
- **Primary** — pilares da tese + análise financeira.
- **Secondary** — valuation + cenários + riscos.
- **Tertiary** — apêndice (tabelas detalhadas, highlights de transcript), Sources.

## Density tradeoff
Este é o **único sítio do sistema onde verbosidade é permitida** — mas a substância tem de ser a análise disciplinada. Regras duras (herança directa dos 10 hábitos):
- Todo número citado tem **source com link clicável**.
- Toda mudança de estimativa mostra **old→new + razão**.
- Todo pilar de tese tem **status** (strengthened/unchanged/weakened) e **gatilho de saída**.
- Nada de "strong performance" sem quantificação.
- Se a análise por baixo é rasa → o relatório di-lo na cara, não enche.

## Anti-patterns (explícito — NÃO fazer)
- ❌ Encher páginas para bater uma contagem mínima (não há contagem mínima — há "cobre os pontos").
- ❌ Nova análise em tempo de render. O relatório é **determinístico a partir do JSON**; regenerar dos mesmos inputs dá output JSON-idêntico.
- ❌ Trimestre alucinado num earnings update — o **freshness gate** (pick #1: verificar o trimestre / abortar se filing > 90d stale) **corre antes** de gerar.
- ❌ URLs em texto plano (sempre hyperlink com display text).
- ❌ Earnings update sem o lead beat/miss; initiating sem a caixa de rating.
- ❌ Relatório sem **disclaimer** (ver §Compliance) — não-negociável.

## Compliance hook (ver [[Comercial/Compliance]])
- **Disclaimer** na página 1 + rodapé de **todas** as páginas: *"ferramenta educacional; não constitui recomendação de investimento; decisões são suas."*
- Linguagem: "verdict do sistema" / "análise" / "cenários" — **não** "recomendação" (especialmente importante no lado BR / CVM).
- Backtests/cenários rotulados como históricos/hipotéticos, nunca preditivos.

## Pricing hook (ver [[Comercial/Pricing]])
Feature do tier **Pro** — **metered** (N relatórios/mês incluídos, depois per-use), porque gerar um corre o Strategist LLM = balde B (custo marginal > 0). UI deve mostrar "X/Y relatórios restantes este mês".

## Success metrics
1. Um utilizador Pro gera **≥1 relatório/mês** (uso real, não vanity).
2. Cada relatório passa um **self-checklist** ao gerar (lead beat/miss presente · ≥1 gráfico · tabela old→new · thesis scorecard · Sources com links · disclaimer · zero trimestre stale) — mecânica emprestada da quality-checklist dos FSI plugins, mas com thresholds sãos. Falha o checklist → não entrega, reporta o que falta.
3. **Zero "nova análise em render"** — regenerar o relatório dos mesmos inputs dá o mesmo conteúdo (proxy: o JSON intermédio é idêntico).

## Dependências (porque o *build* está bloqueado, não a spec)
1. **Pick #1** (freshness gate) e **pick #4** (template earnings-update) de [[Bibliotheca/Disciplina_de_Investidor]] — código partilhado, ainda não implementado. O relatório B reusa o pick #4 directamente.
2. **Pick #3** (thesis scorecard + gatilho de saída) — o relatório A e B reusam para a tabela de pilares.
3. **Validação dos verdicts** (~Ago/2026; mesmo gate da Phase GG) — não vendemos um relatório bonito assente numa metodologia ainda não provada ([[Comercial/GTM]] §sequência).
→ **A spec (este doc) está pronta**. O build entra na fila *depois* dos 3 picks + da janela de validação. Decisão "vale a pena já?" fica para essa altura.

## Out of scope (deste spec)
Código de render; finalização do toolchain PDF (recomendado HTML→PDF, decidir ao construir); UI cliente para disparar o relatório; o protótipo a partir de uma holding real (é o entregável de *build* do B4, não da spec).

---

## O que isto desbloqueia
Antes: "o report tier" era uma linha no roadmap. Agora: está especificado ao ponto de poder ser construído sem re-pensar — sabemos os 2 tipos, de onde vem cada dado (tudo já existe), o motor recomendado, os anti-patterns, os hooks de compliance/pricing, e *exatamente* o que falta para destravar (3 picks de código + validação). Da próxima vez que o tema "vamos construir o relatório?" voltar, não há fase de design — pega-se na spec e implementa-se. E ficou claro que os 5 picks de disciplina **não são opcionais para o produto** — o report tier depende de 3 deles.
