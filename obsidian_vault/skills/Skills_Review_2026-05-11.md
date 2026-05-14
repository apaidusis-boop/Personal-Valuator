---
type: session_prep
tags: [skills, review, agenda]
created: 2026-05-11
status: agenda — para revisão conjunta
---

# Skills — inventário & agenda de revisão (2026-05-11)

> Preparado enquanto estavas fora, para irmos por aqui **juntos**. Não decidi nada — só
> organizei o que temos em camadas e deixei as decisões marcadas com 🟨.
> O brainstorm do "ROTCE-scaled bank multiple" (JPM SELL→HOLD) fica **parado** no ponto da
> escolha A/B/C — retomamos depois deste.

## O que "skills que temos" significa — 3 camadas

1. **Plugins/skills instalados no Claude Code** (`~/.claude/settings.json` → `enabledPlugins`) — 21 plugins activos.
2. **Skills nossas, project-scoped** (`.claude/skills/`) — 5 custom + 8 da família tavily.
3. **"Arsenal" no vault** (`obsidian_vault/skills/`, Phase W Gold) — ~33 skills *avaliadas*, a **maioria NÃO instalada** (era wishlist; entretanto várias passaram a estar cobertas por plugins oficiais — ver §G).

---

## A. Superpowers — disciplina de trabalho (como EU trabalho)

`brainstorming` · `writing-plans` · `test-driven-development` · `systematic-debugging` · `verification-before-completion` · `requesting-code-review` · `receiving-code-review` · `subagent-driven-development` · `executing-plans` · `finishing-a-development-branch` · `dispatching-parallel-agents` · `using-git-worktrees` · `writing-skills` · `using-superpowers`

Estas mudam *o meu processo*, não o produto. Hoje uso `brainstorming` (estou nele agora).
🟨 **Decisão**: quais viram prática-padrão? Candidatas fortes para o nosso contexto (edits autónomos overnight): `verification-before-completion` (evidência antes de "done" — alinha com os princípios Karpathy do CLAUDE.md), `systematic-debugging` (root-cause antes de fix), `writing-plans` (já implícito no "goal-driven execution"). TDD é mais pesado — ver se vale para o motor de scoring.

## B. Família FSI (`claude-for-financial-services`) — kit de sell-side / PE

| Plugin | O que traz | Para nós (investidor pessoal DRIP+Buffett BR/US)? |
|---|---|---|
| `financial-analysis` | DCF, LBO, comps, 3-statement, audit-xls, clean-data-xls, deck-refresh, ib-check-deck, xlsx/pptx-author, skill-creator, ppt-template | DCF/comps/audit-xls = referência útil (espelham o que já fazemos em `analytics/`); LBO/IB-deck = sell-side, **aprender a régua, não usar**. Traz 11 MCP enterprise (FactSet/Daloopa/Moody's/S&P/Pitchbook/Morningstar…) — OAuth-gated, não temos contas. |
| `equity-research` | earnings, earnings-preview, initiate, sector, screen, morning-note, thesis, catalysts, model-update | **Os mais aplicáveis.** earnings/earnings-preview/thesis/catalysts ≈ o que `ii deepdive`/`thesis_manager`/`earnings_prep` já fazem — vale comparar a estrutura. screen/sector = ideias. |
| `wealth-management` | tlh, rebalance, proposal, financial-plan, client-review, client-report | `tlh` (tax-loss harvesting) e `rebalance` = **directamente úteis** (temos `ii rebalance` mas não TLH). proposal/client-* = para o mundo Comercial (blueprint), não o pessoal. |
| `private-equity` | returns, ai-readiness, value-creation, portfolio, unit-economics, ic-memo, dd-prep, source, dd-checklist, screen-deal | Quase tudo fora de escopo. `ic-memo` e `dd-checklist` = disciplina de due-diligence transferível. Resto = ignorar. |
| `market-researcher` | competitive-analysis (+ comps/pptx) | Útil pontualmente (mapa competitivo de um sector). |
| `earnings-reviewer` | managed agent: lê transcript+filings → actualiza modelo → escreve nota | Sobrepõe-se a `ii react` + `library.earnings_prep`. Avaliar se substitui ou complementa. |
| `model-builder` | managed agent: constrói DCF/LBO/3-statement/comps no Excel a partir de ticker | Sobrepõe-se a `analytics/fair_value*` mas em Excel. Provavelmente **learn-not-adopt** (queremos a lógica em código, não em planilha — regra in-house-first). |

🟨 **Decisão**: ficar com `equity-research` + `wealth-management` (`tlh`!) como os "a usar"; os outros como referência/disable.

## C. Design — antes de qualquer UI nova (regra "AI slop UI")

`huashu-design` (花叔 — protótipos HTML hi-fi, demos, slides, vídeo) · `hue` (gera design-language skills) · `ui-ux-pro-max-skill` (DBs de estilos/paletas/fontes/UX) · `figma:*` (8 skills: implement-design, generate-design-system, code-connect, generate-diagram, use-figma…)

🟨 **Decisão**: confirmar o fluxo — para Mission Control / Obsidian Escritório, qual é o "go-to" (huashu-design para variantes paralelas; ui-ux-pro-max para tokens). figma:* só faz sentido se voltarmos a usar Figma.

## D. Research & scraping — há sobreposição a limpar

| Skill/MCP | Job | Sobrepõe-se a… |
|---|---|---|
| `bigdata-com` (+ 9 sub: company-brief, earnings-digest, thematic-research, sector-analysis, risk-assessment, country-analysis, regional-comparison, cross-sector, earnings-preview) + MCP | research estruturado de empresa/sector/macro | `ii deepdive`, `library.earnings_prep`, `analytics.regime` |
| `exa:search` + `fetchers/exa_fetcher.py` + `scripts/exa_news_monitor.py` | busca neural / news / find-similar | `ii news`, Tavily |
| `tavily-*` (search, research, extract, crawl, map, dynamic-search, cli, best-practices) — 8 skills locais | search web / extract / crawl | Exa, `tvly` CLI, `portal_playwright` |
| `chrome-devtools-mcp:*` + `playwright:*` | automação browser, debug web, scraping JS | `fetchers/portal_playwright.py`, `fetchers/ri_url_resolver` |
| `context7` (MCP) | docs actualizadas de libs/frameworks | — (novo, útil para coding) |
| FMP MCP (27 tools) · status-invest MCP | dados financeiros US / FIIs BR | `fetchers/yfinance_fetcher`, `fetchers/statusinvest_scraper` |

🟨 **Decisão**: por cada job (news · deep research · scraping JS · docs de libs) escolher **o primário e o fallback**, e marcar os redundantes como "não usar a menos que X". Hoje temos 3 caminhos para "news" (Exa fetcher, `ii news`, Tavily) e 3 para scraping (portal_playwright, playwright MCP, chrome-devtools MCP).

## E. Skills nossas (`.claude/skills/`) — estão a ser usadas?

`drip-analyst` · `macro-regime` · `panorama-ticker` · `perpetuum-review` · `rebalance-advisor` (+ os 8 `tavily-*` copiados para cá)

🟨 **Decisão**: quais disparam mesmo (via `/nome` ou trigger)? Estão wired aos comandos `ii` certos? Alguma a melhorar (a `drip-analyst` foi o piloto Phase W.4) ou a aposentar?

## F. Ops & housekeeping

`hookify` (+ writing-rules / configure / list / help) — criar hooks de comportamento · `claude-md-management` (revise-claude-md / claude-md-improver) — higiene do CLAUDE.md · `session-report` — relatório HTML de uso da sessão · `update-config` · `keybindings-help` · `simplify` · `fewer-permission-prompts` · `loop` · `schedule` · `claude-api` · `init` · `review` · `security-review` · `statusline-setup`

🟨 **Decisão**: (1) que regras `hookify` valem a pena (ex.: bloquear `.env` commit, lembrar smoke-test antes de detach overnight — temos memórias sobre isto que dariam bons hooks); (2) cadência de `claude-md-management` (mensal?); (3) `fewer-permission-prompts` — correr uma vez para reduzir prompts.

## G. Arsenal Phase W (no vault) — actualizar o estado

Muitas já estão **cobertas por plugins instalados** — riscar:
- ~~SKL_pdf_processing~~ → temos `library/_md_extract` + markitdown + `monitors/cvm_pdf_extractor`
- ~~SKL_xlsx / SKL_pptx~~ → `financial-analysis:xlsx-author` / `pptx-author` / `audit-xls`
- ~~SKL_skill_creator~~ → `financial-analysis:skill-creator`
- ~~SKL_playwright_mcp~~ → plugin `playwright`
- ~~SKL_tavily~~ → família `tavily-*` instalada
- ~~SKL_autoresearch_perpetuum~~ → construído (`agents/perpetuum/autoresearch.py`, `research.autoresearch`)
- ~~SKL_firecrawl~~ → substituído por `portal_playwright` + Tavily/Exa (firecrawl nunca foi wired)

Ainda **não** cobertas (candidatas reais a instalar):
- `SKL_quant_stack` — pyfolio / empyrical / vectorbt / Alphalens / Riskfolio-Lib. Temos `analytics.quant_smoke` (caseiro) e `analytics.backtest_*`; estas libs dariam tearsheets e factor-validation a sério. **Mais provável "sim".**
- `SKL_openbb` — OpenBB como camada peer de research. Avaliar contra o stack que já temos (yfinance+FMP+SEC+Tavily). Possível overkill.
- `SKL_observability_stack` — LangFuse + DSPy + Instructor. Só vale se a complexidade dos agentes Ollama justificar tracing/optimization. Hoje provavelmente "ainda não".
- `SKL_obsidian_kepano` — MOC/evergreen/orphan detection para o vault. Temos `obsidian_bridge` + `memory_cleanup`; isto seria a versão "PKM a sério".
- `SKL_mcp_harness_arsenal` — Bigdata/Status-Invest/Google Drive/Gmail/Calendar "já loaded, untapped". Parte já está (bigdata-com plugin, status-invest MCP); Drive/Gmail/Calendar continuam por explorar.

🟨 **Decisão**: actualizar `_MOC.md` com os "riscados", e escolher 1–2 das não-cobertas para realmente instalar (recomendação prévia: `quant_stack`).

## H. Plugins que talvez não façam sentido para nós

- `data@claude-plugins-official` (Airflow / Astronomer / dbt-cosmos / DAGs) — **não usamos Airflow**. 🟨 disable?
- `legalzoom@claude-plugins-official` (review-contract / attorney-assist) — fora de escopo de investimento. 🟨 disable? (a menos que seja útil no mundo Comercial mais tarde)
- `pyright-lsp` / `typescript-lsp` — úteis se eu editar muito Python/TS; baixo custo, deixar.

---

## Agenda da nossa sessão (ordem sugerida)

1. **§B** — cortar a família FSI ao que serve (provavelmente: usar `equity-research` + `wealth-management:tlh`; resto referência). Maior payoff.
2. **§D** — escolher o primário/fallback de cada job de research/scraping; matar redundâncias.
3. **§E** — auditar as nossas 5 skills custom (usadas? wired? melhorar/aposentar?).
4. **§A** — fixar quais superpowers viram prática-padrão.
5. **§G** — actualizar `_MOC.md` + escolher 1–2 a instalar.
6. **§F + §H** — hooks que valem a pena + disable do que não usamos.
7. (depois) retomar o brainstorm do banco ROTCE-scaled.

> Quando voltares: dizes "vamos pelo ponto N" ou mexes na ordem. Não preciso de aprovação para
> nada disto — é só o mapa.
