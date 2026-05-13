---
type: inventory
tags: [audit, inventory, skills, agents, capabilities]
date: 2026-05-13
---

# Inventário Completo — Skills / Agents / Capabilities

> Cada linha tem uma explicação curta (5-8 palavras) do que faz.
> Marca o que queres podar, consolidar ou promover.

## Sumário numérico

| Camada | Total |
|---|---:|
| Skills (`.claude/skills/`) | 124 |
| Slash commands (`.claude/commands/`) | 52 |
| Subagents (`.claude/agents/`) | 4 |
| Python agents top-level | 28 |
| Perpetuum modules | 15 |
| Council modules | 14 |
| Helena modules | 4 |
| Council personas (vault) | 10 |
| Plugins activos | 17 |
| MCP servers loaded | ~18 |
| `ii` catalog entries | 131 |
| **TOTAL items** | **~410** |

---

## SKILLS (`.claude/skills/`, 124)

### bigdata-com (1) — workflows do MCP Bigdata.com
- `bigdata-com-financial-research-analyst` — Guia: como usar o MCP da Bigdata.

### chrome-devtools-mcp (6) — debug web/Mission Control
- `chrome-devtools-mcp-a11y-debugging` — Auditoria de acessibilidade (a11y) numa página.
- `chrome-devtools-mcp-chrome-devtools` — Debug geral via Chrome DevTools MCP.
- `chrome-devtools-mcp-chrome-devtools-cli` — Automatizar Chrome via shell.
- `chrome-devtools-mcp-debug-optimize-lcp` — Otimizar Largest Contentful Paint (LCP).
- `chrome-devtools-mcp-memory-leak-debugging` — Diagnosticar memory leaks em JS/Node.
- `chrome-devtools-mcp-troubleshooting` — Resolver falhas de conexão do DevTools MCP.

### claude-md-management (1) — manutenção de CLAUDE.md
- `claude-md-management-claude-md-improver` — Auditar e melhorar ficheiros CLAUDE.md.

### data (20) — Astronomer/Airflow (NÃO usamos)
- `data-airflow` — Comandos básicos de Apache Airflow.
- `data-airflow-hitl` — Workflows com aprovação humana em Airflow.
- `data-analyzing-data` — Consultar warehouse e responder perguntas.
- `data-annotating-task-lineage` — Adicionar inlets/outlets a tasks Airflow.
- `data-authoring-dags` — Escrever DAGs novos em Airflow.
- `data-checking-freshness` — Verificar se dados estão actualizados.
- `data-cosmos-dbt-core` — Integrar dbt Core via Astronomer Cosmos.
- `data-cosmos-dbt-fusion` — Integrar dbt Fusion via Astronomer Cosmos.
- `data-creating-openlineage-extractors` — Criar extractors de lineage customizados.
- `data-debugging-dags` — Diagnóstico profundo de falhas em DAGs.
- `data-deploying-airflow` — Fazer deploy de DAGs/projectos.
- `data-managing-astro-deployments` — Gerir deployments Astronomer.
- `data-managing-astro-local-env` — Gerir Airflow local com Astro CLI.
- `data-migrating-airflow-2-to-3` — Migrar projectos Airflow 2 → 3.
- `data-profiling-tables` — Profiling profundo duma tabela.
- `data-setting-up-astro-project` — Iniciar projecto Astro novo.
- `data-testing-dags` — Workflow test-debug-fix de DAGs.
- `data-tracing-downstream-lineage` — Quem depende destes dados?
- `data-tracing-upstream-lineage` — De onde vêm estes dados?
- `data-troubleshooting-astro-deployments` — Investigar problemas em prod Astronomer.
- `data-warehouse-init` — Inicializar discovery do warehouse.

### drip-analyst (1) — nosso, projecções DRIP
- `drip-analyst` — Projecção DRIP de ticker via Ollama.

### earnings-reviewer (6) — pacote earnings sell-side
- `earnings-reviewer-audit-xls` — Auditar fórmulas duma sheet.
- `earnings-reviewer-earnings-analysis` — Earnings update formal (8-12 pp).
- `earnings-reviewer-earnings-preview` — Preview pré-earnings com cenários.
- `earnings-reviewer-model-update` — Actualizar modelo com novos dados.
- `earnings-reviewer-morning-note` — Draft de morning note.
- `earnings-reviewer-xlsx-author` — Criar ficheiro .xlsx headless.

### equity-research (10) — pacote equity research
- `equity-research-catalyst-calendar` — Calendário de catalisadores.
- `equity-research-earnings-analysis` — Earnings update formal (8-12 pp).
- `equity-research-earnings-preview` — Preview pré-earnings.
- `equity-research-idea-generation` — Stock screen / ideas novas.
- `equity-research-initiating-coverage` — Initiation report (5-task workflow).
- `equity-research-model-update` — Actualizar modelo financeiro.
- `equity-research-morning-note` — Draft morning meeting note.
- `equity-research-sector-overview` — Overview formal de sector.
- `equity-research-thesis-tracker` — Criar/actualizar tese de investimento.

### exa (1) — busca semântica
- `exa-search` — Deep research via Exa MCP.

### figma (9) — design system (NÃO usamos)
- `figma-figma-code-connect` — Mapear componentes Figma↔código.
- `figma-figma-create-design-system-rules` — Gerar regras de design system.
- `figma-figma-create-new-file` — Criar ficheiro Figma novo.
- `figma-figma-generate-design` — App → Figma (página/modal/sidebar).
- `figma-figma-generate-diagram` — Diagrama flowchart/architecture.
- `figma-figma-generate-library` — Construir design system completo.
- `figma-figma-implement-design` — Figma → código UI 1:1.
- `figma-figma-use` — Pré-requisito para usar Figma MCP.
- `figma-figma-use-figjam` — Pré-requisito Figma MCP em FigJam.

### financial-analysis (14) — modelagem financeira
- `financial-analysis-3-statement-model` — Preencher modelo 3-statement (IS/BS/CF).
- `financial-analysis-audit-xls` — Auditar fórmulas dum modelo Excel.
- `financial-analysis-clean-data-xls` — Limpar dados sujos numa sheet.
- `financial-analysis-competitive-analysis` — Deck de landscape competitivo.
- `financial-analysis-comps-analysis` — Comparable company analysis institucional.
- `financial-analysis-dcf-model` — DCF formal (SEC filings + WACC).
- `financial-analysis-deck-refresh` — Refresh dum deck com novos números.
- `financial-analysis-ib-check-deck` — QC de deck IB antes do envio.
- `financial-analysis-lbo-model` — LBO model (PE acquisition).
- `financial-analysis-ppt-template-creator` — Criar skill PPT reutilizável.
- `financial-analysis-pptx-author` — Criar ficheiro .pptx headless.
- `financial-analysis-skill-creator` — Guia para criar skills novas.
- `financial-analysis-xlsx-author` — Criar ficheiro .xlsx headless.

### hookify (1) — anti-padrão prevention
- `hookify-writing-rules` — Sintaxe/padrões para hooks Claude Code.

### legalzoom (1) — contratos legais (irrelevante)
- `legalzoom-attorney-assist` — Conectar com advogado LegalZoom.

### macro-regime (1) — nosso, regime macro
- `macro-regime` — Classificador regime macro BR+US.

### market-researcher (5) — sector/comps decks
- `market-researcher-competitive-analysis` — Deck de landscape competitivo.
- `market-researcher-comps-analysis` — Comparable companies de um sector.
- `market-researcher-idea-generation` — Ideas novas de um sector/tema.
- `market-researcher-pptx-author` — Criar .pptx headless.
- `market-researcher-sector-overview` — Sector overview report.

### model-builder (6) — Excel headless
- `model-builder-3-statement-model` — Preencher modelo 3-statement.
- `model-builder-audit-xls` — Auditar fórmulas Excel.
- `model-builder-comps-analysis` — Comparable companies em Excel.
- `model-builder-dcf-model` — DCF model em Excel.
- `model-builder-lbo-model` — LBO model em Excel.
- `model-builder-xlsx-author` — Criar .xlsx headless.

### panorama-ticker (1) — nosso, super-command
- `panorama-ticker` — Vista 360° dum ticker (verdict+peers+triggers+vídeos).

### perpetuum-review (1) — nosso, T2 actions
- `perpetuum-review` — Aprovar/rejeitar acções perpetuum.

### private-equity (10) — PE deals (não usamos directamente)
- `private-equity-ai-readiness` — Scan da carteira por AI opportunities.
- `private-equity-dd-checklist` — Due diligence checklist.
- `private-equity-dd-meeting-prep` — Prep para reunião de diligence.
- `private-equity-deal-screening` — Triagem dum deal (CIM/teaser).
- `private-equity-deal-sourcing` — Descobrir companies + draft outreach.
- `private-equity-ic-memo` — Draft IC memo.
- `private-equity-portfolio-monitoring` — Review da performance da carteira PE.
- `private-equity-returns-analysis` — Tabelas IRR/MOIC sensitivity.
- `private-equity-unit-economics` — Análise unit economics (ARR/LTV/CAC).
- `private-equity-value-creation-plan` — Plano value creation pós-aquisição.

### rebalance-advisor (1) — nosso, allocation
- `rebalance-advisor` — Rebalance da carteira (drift + cash).

### session-report (1) — telemetria de sessão
- `session-report-session-report` — Report HTML de uso de Claude.

### superpowers (14) — engenharia meta-skills
- `superpowers-brainstorming` — Explorar requisitos antes de codar.
- `superpowers-dispatching-parallel-agents` — Despachar agentes em paralelo.
- `superpowers-executing-plans` — Executar plan implementation com checkpoints.
- `superpowers-finishing-a-development-branch` — Decidir como integrar branch (merge/PR).
- `superpowers-receiving-code-review` — Como receber code review feedback.
- `superpowers-requesting-code-review` — Pedir code review antes de mergear.
- `superpowers-subagent-driven-development` — Implementação via subagentes paralelos.
- `superpowers-systematic-debugging` — Debug com root cause analysis.
- `superpowers-test-driven-development` — Escrever testes antes do código.
- `superpowers-using-git-worktrees` — Isolar workspace via git worktrees.
- `superpowers-using-superpowers` — Como descobrir/usar skills no início.
- `superpowers-verification-before-completion` — Verificar com evidência antes de "done".
- `superpowers-writing-plans` — Escrever plan antes de codar.
- `superpowers-writing-skills` — Criar/editar skills.

### tavily (8) — pesquisa web
- `tavily-best-practices` — Boas práticas de integração Tavily.
- `tavily-cli` — Interface CLI do Tavily.
- `tavily-crawl` — Crawl recursivo de website.
- `tavily-dynamic-search` — Search programática com filtros.
- `tavily-extract` — Extrair markdown dum URL.
- `tavily-map` — Listar URLs dum site (sem conteúdo).
- `tavily-research` — Deep research com citations.
- `tavily-search` — Search simples web.

### wealth-management (6) — gestão patrimonial
- `wealth-management-client-report` — Performance report do cliente.
- `wealth-management-client-review` — Prep de reunião com cliente.
- `wealth-management-financial-plan` — Construir/actualizar plano financeiro.
- `wealth-management-investment-proposal` — Proposta de investimento prospect.
- `wealth-management-portfolio-rebalance` — Drift + trades de rebalance.
- `wealth-management-tax-loss-harvesting` — Identificar oportunidades TLH.

---

## SLASH COMMANDS (`.claude/commands/`, 52)

### bigdata-com (10) — wrappers MCP Bigdata
- `/bigdata-com-company-brief` — Summary 30 dias duma empresa.
- `/bigdata-com-country-analysis` — Análise económica dum país.
- `/bigdata-com-country-sector-analysis` — Sector × país combinado.
- `/bigdata-com-cross-sector` — Comparar sectores (rotação).
- `/bigdata-com-earnings-digest` — Análise pós-earnings detalhada.
- `/bigdata-com-earnings-preview` — Análise pré-earnings forward.
- `/bigdata-com-regional-comparison` — Comparar regiões económicas.
- `/bigdata-com-risk-assessment` — Análise de riscos completa.
- `/bigdata-com-sector-analysis` — Performance/valuations de sector.
- `/bigdata-com-thematic-research` — Pesquisar tema de investimento.

### claude-md-management (1)
- `/claude-md-management-revise-claude-md` — Actualizar CLAUDE.md com aprendizagens.

### equity-research (9) — workflows sell-side
- `/equity-research-catalysts` — Calendário de catalisadores.
- `/equity-research-earnings-preview` — Preview com cenários.
- `/equity-research-earnings` — Earnings update report.
- `/equity-research-initiate` — Initiation report.
- `/equity-research-model-update` — Update do modelo.
- `/equity-research-morning-note` — Morning meeting note.
- `/equity-research-screen` — Stock screen / ideas.
- `/equity-research-sector` — Sector overview report.
- `/equity-research-thesis` — Criar/actualizar tese.

### financial-analysis (7) — modelagem
- `/financial-analysis-3-statement-model` — Preencher 3-statement model.
- `/financial-analysis-competitive-analysis` — Landscape competitivo.
- `/financial-analysis-comps` — Comparable company analysis.
- `/financial-analysis-dcf` — DCF valuation model.
- `/financial-analysis-debug-model` — Debug/auditar modelo financeiro.
- `/financial-analysis-lbo` — LBO model.
- `/financial-analysis-ppt-template` — Criar template PPT reutilizável.

### hookify (4)
- `/hookify-configure` — Activar/desactivar regras.
- `/hookify-help` — Ajuda do plugin.
- `/hookify-hookify` — Criar hooks da conversa.
- `/hookify-list` — Listar regras configuradas.

### legalzoom (1)
- `/legalzoom-review-contract` — Análise profunda de contrato.

### private-equity (10) — wrappers PE
- `/private-equity-ai-readiness` — Scan AI opportunities.
- `/private-equity-dd-checklist` — Due diligence checklist.
- `/private-equity-dd-prep` — Prep diligence meeting.
- `/private-equity-ic-memo` — IC memo.
- `/private-equity-portfolio` — Review performance carteira PE.
- `/private-equity-returns` — IRR/MOIC sensitivity.
- `/private-equity-screen-deal` — Triagem dum deal.
- `/private-equity-source` — Sourcing + outreach.
- `/private-equity-unit-economics` — Unit economics.
- `/private-equity-value-creation` — Value creation plan.

### Engineering meta (4 native)
- `/security-review` — Review de segurança do branch.
- `/systematic-debugging` — Debug com root cause primeiro.
- `/verification-before-completion` — Verificar antes de claim "done".
- `/writing-plans` — Escrever plan implementation antes de codar.

### wealth-management (6) — wrappers
- `/wealth-management-client-report` — Client performance report.
- `/wealth-management-client-review` — Prep client review.
- `/wealth-management-financial-plan` — Financial plan.
- `/wealth-management-proposal` — Investment proposal.
- `/wealth-management-rebalance` — Drift + trades rebalance.
- `/wealth-management-tlh` — Tax-loss harvesting.

---

## SUBAGENTS (`.claude/agents/`, 4)
- `earnings-reviewer-earnings-reviewer` — Processa earnings end-to-end: transcript+filings → nota.
- `hookify-conversation-analyzer` — Analisa transcript da conversa e propõe hooks.
- `market-researcher-market-researcher` — Sector primer + competitive landscape + comps.
- `model-builder-model-builder` — Construir DCF/LBO/3-statement do zero em Excel.

---

## COUNCIL PERSONAS (`obsidian_vault/agents/`, 10)
- **Aderbaldo Cíclico** — Commodities / ciclos (2 reviews: PRIO3, VALE3).
- **Charlie Compounder** — Quality compounders Buffett/Munger (12 reviews).
- **Diego Bancário** — Bancos BR (2: BBDC4, ITSA4).
- **Hank Tier-One** — Bancos US/global (6: BLK, BN, GS, JPM, NU, XP).
- **Lourdes Aluguel** — FIIs aluguel / tijolo (7 reviews).
- **Mariana Macro** — Macro overlay (regime, Selic, USD) (32 reviews).
- **Pedro Alocação** — Allocator / portfolio constructor (32 reviews).
- **Tião Galpão** — FIIs logística / galpões (2 reviews).
- **Valentina Prudente** — Risk / due diligence (32 reviews).
- **Walter Triple-Net** — NNN REITs tipo O, ADC (2 reviews).

---

## PLUGINS ACTIVOS (17)

### `claude-for-financial-services` (7) — pacote FSI Anthropic
- `financial-analysis` — Modelagem financeira (DCF/LBO/3-statement/comps/PPT).
- `equity-research` — Equity research formal (initiation/earnings/morning-note).
- `earnings-reviewer` — Post-earnings updates rápidos.
- `wealth-management` — Gestão patrimonial (rebalance/TLH/plan).
- `private-equity` — PE workflows (IC memo, DD, value creation).
- `market-researcher` — Sector/thematic decks.
- `model-builder` — Excel headless (DCF/LBO/3-statement).

### `claude-plugins-official` (10)
- `superpowers` — Engenharia meta-skills (TDD, debugging, plans).
- `data` — Astronomer Airflow toolkit (não usamos).
- `figma` — Design system tooling (não usamos).
- `bigdata-com` — Bigdata.com MCP (news/tearsheets/themes).
- `chrome-devtools-mcp` — Browser debugging via MCP.
- `hookify` — Hooks de anti-padrões.
- `claude-md-management` — Manutenção de CLAUDE.md.
- `legalzoom` — Revisão contractos legais (irrelevante).
- `exa` — Search semântica via MCP.
- `session-report` — Report HTML uso de Claude.
- Plus: `playwright`, `pyright-lsp`, `typescript-lsp` — só MCPs/LSPs, sem skills.

---

## MCP SERVERS LOADED (~18)

### Claude.ai-hosted (sempre on)
- `Bigdata_com` — Tearsheets, securities, calendar, search.
- `FMP` — Financial Modeling Prep (quotes/statements/calendar).
- `Gmail` — Auth on-demand.
- `Google_Calendar` — Eventos.
- `Google_Drive` — Files.
- `LSEG` — Refinitiv (OAuth).

### Plugin-provided
- `figma_*` — API do Figma.
- `financial-analysis_*` — Aiera/Chronograph/Daloopa/Egnyte/FactSet/LSEG/Moodys/Morningstar/Pitchbook/S&P (OAuth).
- `playwright_*` — Automação de browser.

### Local `.mcp.json`
- `status-invest` — Dados BR (FIIs, ações, indicadores).
- `context7` — Docs de libraries (lookup).
- `task-master-ai` — Gestão de tasks.

---

## CRON SURFACE — o que MESMO corre

### `daily_run.bat` (23:30 diário)
1. `daily_update.py` — Fetcher diário BR (preços + scoring).
2. `auto_import_taxlots.py` — Importa CSV de trades novos.
3. `daily_update_us.py` — Fetcher diário US (preços + scoring).
4. `exa_news_monitor.py` — Varre news para holdings via Exa.
5. `backfill_intangibles.py` — Re-popula goodwill/TBV (US banks).
6. `cross_source_spotcheck.py` — Compara yfinance vs outras fontes.
7. `us_portfolio_report.py` — Briefing US only.
8. `weekly_report.py` — Relatório semanal consolidado.
9. `portfolio_report.py` — Briefing consolidado BR+US markdown.
10. `perpetuum_master.py` — Corre todos os perpetuums (thesis/vault/etc).
11. `paper_trade_close.py` — Fecha paper signals expirados.
12. `predictions_evaluate.py` — Avalia track record de analistas.
13. `build_glossary.py` — Re-build Glossary do vault.
14. `dossier_tutor.py` — Injecta secção Tutor em DOSSIE.md.
15. `inject_ticker_insights.py` — Junta YT+podcast+analyst por ticker.
16. `build_knowledge_cards.py` — Knowledge cards de filosofia (RAG).
17. `research_digest.py` — Digest diário da Bibliotheca.
18. `captains_log_telegram.py` — Push diário Telegram.
19. `export_macro_csv.py` — Exporta Selic/CDI/IPCA/USDBRL → CSV.
20. `rotate_logs.py` — Comprime logs >30 dias.

### `hourly_run.bat`
1. `sec_monitor.py` — Filings SEC (8-K/10-K) última 24h.
2. `cvm_monitor.py` — Fatos relevantes CVM diários.
3. `news_fetch.py` — Fetch + classify news.
4. `notify_events.py` — Toast Windows para eventos críticos.

### `q4h_run.bat` (cada 4h)
1. `cvm_pdf_extractor.py` — Baixar+extrair PDFs CVM pendentes.
2. `dividend_calendar.py` — Próximos pagamentos de dividendos.
3. `earnings_calendar.py` — Próximas datas de earnings.
4. `refresh_benchmarks.py` — Re-fetch SPY/BOVA11 prices.
5. `auto_verdict_on_filing.py` — Trigger verdict em novo filing.
6. `auto_verdict_on_content.py` — Trigger verdict em mismatch content.
7. `trigger_monitor.py` — Monitor de triggers (price drops/etc).
8. `yt_poll.py` — Poll de canais YouTube.
9. `pod_poll.py` — Poll de podcasts financeiros.

**Tudo o resto é on-demand** (CLI manual ou Telegram via Antonio Carlos).

---

## PYTHON AGENTS (`agents/*.py`, 28)

- `analyst_backtest` — Aristóteles: backtest de performance de analistas.
- `autoresearch` — Tavily web research com cache + rate-limit.
- `chief_of_staff` — Antonio Carlos: orquestrador Telegram + CLI.
- `daily_synthesizer` — Agrega tudo que mudou nas últimas 24-48h.
- `data_janitor` — Noé: limpa/normaliza dados na DB.
- `decision_journal_intel` — Pattern mining em decisões anteriores.
- `devils_advocate` — Anti-confirmation-bias agent.
- `fiel_escudeiro` — Assistente pessoal com acesso total ao repo.
- `helena_mega` — Audit + curate + spike + report (Mission Control).
- `holding_wiki_synthesizer` — Stubs wiki por holding via Ollama.
- `mega_auditor` — Detector de cruft (Karpathy-driven).
- `meta_agent` — Compliance officer: audita outros agents.
- `morning_briefing` — Briefing matinal via Ollama.
- `perpetuum_master` — Runner que executa todos os perpetuums.
- `perpetuum_validator` — LEGACY (substituído por perpetuum.thesis).
- `portfolio_matcher` — Clara: match portfolio vs targets.
- `research_scout` — Ulisses: head of research / discovery.
- `risk_auditor` — Detecta drift de tese em holdings.
- `skill_scout` — Monitor passivo de catálogos de skills.
- `subscription_fetch` — Ingest semanal de Fool/XP/WSJ.
- `synthetic_ic` — Debate multi-persona (Buffett/Druck/Taleb/...).
- `telegram_controller` — Zé Mensageiro: Telegram desk.
- `thesis_refresh` — Re-run thesis_refresh.py em schedule.
- `thesis_synthesizer` — Gera secção Thesis em ticker notes (Ollama).
- `variant_perception` — We vs analyst consensus divergence.
- `voice_input` — Captura voz + Whisper + Qwen intent.
- `voice_output` — TTS via Windows SAPI (local).
- `watchdog` — Event-driven poller cron failures.

---

## PERPETUUM (`agents/perpetuum/*.py`, 15)

- `perpetuum.autoresearch` — Descobre news material não-coberto no vault.
- `perpetuum.bibliotheca` — Librarian proactivo do catálogo de companies.
- `perpetuum.code_health` — Apanha anti-patterns recorrentes no código.
- `perpetuum.content_quality` — Signal-to-noise de briefings/reports.
- `perpetuum.daily_delight` — Build proactivo "wake-up gift".
- `perpetuum.data_coverage` — Score 0-100 completeness por holding.
- `perpetuum.dreaming` — Memory consolidation background.
- `perpetuum.library_signals` — Corre métodos da library contra carteira.
- `perpetuum.meta` — Valida os perpetuums entre si.
- `perpetuum.method_discovery` — Autoresearch sobre nossos critérios.
- `perpetuum.ri_freshness` — Monitor releases CVM + flag overdue.
- `perpetuum.security_audit` — Healthcheck de segurança.
- `perpetuum.thesis` — Valida thesis por ticker (Heart of Phase W).
- `perpetuum.token_economy` — Procura economias de Claude tokens.
- `perpetuum.vault_health` — Valida saúde de cada nota do vault.

---

## COUNCIL (`agents/council/*.py`, 14)

- `council.agent_reviews` — Writer dos reviews por persona.
- `council.cache_policy` — Smart re-run cache STORYT_3.0.
- `council.coordinator` — Coordena debate 2-round entre personas.
- `council.dossier` — Camada factual (sem opiniões).
- `council.evidence` — Evidence Ledger (Sprint 3).
- `council.narrative` — Narrative Engine (números determinísticos).
- `council.peer_engine` — Peer comparison engine (Sprint 2).
- `council.personas` — Prompts Round 1 / Round 2.
- `council.philosophy` — Camada filosofia investimento STORYT_1.
- `council.render` — Transcript renderer com wikilinks.
- `council.research_brief` — ResearchBrief (Camada 1).
- `council.roster` — Modo×Jurisdiction → persona nomeada.
- `council.story` — Pipeline E2E: debate → narrativa.
- `council.valuation` — DCF + múltiplos + evolução financeira.
- `council.versioning` — Versioning + Delta Engine (Sprint 4).

---

## HELENA (`agents/helena/*.py`, 4)

- `helena.audit` — Design system linter (DS001-DS009).
- `helena.curate` — Avaliador go/no-go de skills da comunidade.
- `helena.report` — Consolidador master do Helena Mega.
- `helena.spike` — Feasibility sketches dos 4 platform paths.

---

## CLAUDE.md catalog (131 entries) — comandos `ii` + scripts

### Helena / design
- **Mega Helena** — Orquestrador audit+curate+spike+report.
- **Helena audit** — Linter design system (DS001-DS009).
- **Helena Mega master report** — Consolidador final do output Helena.
- **Helena Linha scout** — Scout semanal (GitHub+RSS+YouTube).

### Panorama / ticker views
- **Panorama completo de ticker** — Vista 360° (verdict+peers+vídeos+notes).
- **Refresh preço intraday** — Re-fetch yfinance live.
- **Notes por ticker** — Adicionar nota livre por ticker.

### Perpetuum
- **Perpetuum Master** — Corre todos os perpetuums diariamente.
- **Perpetuum individual** — Corre só um perpetuum nomeado.
- **Perpetuum review** — Lista acções T2+ abertas para aprovar.
- **Perpetuum run action** — Executa acção whitelisted.

### Bibliotheca / RAG / vault
- **Bibliotheca autofix** — Backfill sector+name em companies.
- **Library ingest books** — PDF→chunks (pypdf ou markitdown).
- **Universal extractor** — Qualquer file (PDF/DOCX/XLSX/PPT/IMG/áudio)→MD.
- **CVM PDF extractor (markitdown)** — Preserva tables em filings CVM.
- **Portal scraper (Playwright)** — Scrape JS-heavy sites (RI/fiis).
- **Library extract methods** — Extrai métodos de livros via Ollama.
- **Library matcher** — Match métodos vs portfolio.
- **Library RAG build** — Embed chunks com nomic local.
- **Library RAG query** — Search semântica nos chunks.
- **Library RAG ask** — RAG + síntese Qwen em PT.
- **Bibliotheca Glossary build** — Re-build Glossary do vault.
- **Bibliotheca Knowledge Cards** — Cards filosofia via RAG synth.
- **Dossier Tutor** — Injecta secção Tutor em DOSSIE.md.
- **Clippings ingest** — Importa clippings Obsidian → chunks RAG.
- **Vault semantic ask** — Pergunta Qwen 14B sobre todo o vault.
- **Vault clean video names** — Renomear videos/<id>.md → date_channel_slug.

### Paper trade / scoring
- **Paper trade signals** — SQL para signals abertos.
- **Paper trade close** — Fecha signals expirados (cron diário).
- **Enrich fundamentals** — Backfill market_cap/cur_ratio/ltd/wc.
- **Dividend safety score** — Score 0-100 forward dividend safety.
- **Altman Z-Score** — Distress score (veto se baixo).
- **Piotroski F-Score** — Quality 0-9 (veto se F≤3).
- **Beneish M-Score** — Manipulação contábil (8 índices).
- **Moat Score** — Durabilidade competitiva 0-10.
- **ROIC compute** — Return on invested capital.

### Fetchers / data
- **Fetch deep fundamentals** — yfinance full fundamentals dump.
- **Fetch Kings/Aristocrats batch** — Popula US dividend kings (87 tickers).
- **Massive.com fetcher** — Fallback US (intraday/options/forex).
- **Exa neural search** — Search semântica via Exa MCP.
- **Atualizar FRED macro** — Update macros US (DGS10/etc).
- **Fetch unificado com fallback** — Cascade BR/US com cache TTL.
- **Data health monitor** — API availability + cache hit + latency.

### Strategy / allocation
- **Strategy engine single** — Corre 1 engine (graham/buffett/drip/macro/hedge).
- **Allocation proposal** — Combina 5 engines + bucket weights.
- **Hedge status** — Status do hedge tactical (regime-based).
- **Quality drift** — Screen a degradar/melhorar.
- **Regime macro classifier** — Classifica regime BR+US.
- **Conviction score engine** — Score 0-100 universe-wide.

### Backtest
- **Backtest yield strategy** — Backtest yield BR/US histórico.
- **Backtest regime overlay** — Phase H (null result).
- **Backtest triggers históricos** — Backtest price_drop/etc.
- **Portfolio stress test** — Concentration/factor/drawdown.
- **Quant smoke tearsheet** — Sharpe/Sortino/MDD HTML.

### Agents / decisions
- **Agent call (role-based)** — Wrapper LLM por role (classification/extraction/...).
- **Agent decisions stats** — Stats 7d agent_decisions.db.
- **Overnight backfill** — Pre-warm + 5 engines × universo.
- **Backfill US bank tangibles** — TBVPS+ROTCE para bancos US.
- **Mega Audit** — Cruft detector (8 categorias, NUNCA apaga).
- **Mega Audit bury** — Quarantine para cemetery (reversível).
- **Synthetic IC debate** — 5 personas Buffett/Druck/Taleb/Klarman/Dalio.
- **Variant perception** — We vs analyst consensus.
- **Decision journal intel** — Pattern mining decisões.
- **Holding wiki synthesizer** — Stubs wiki por holding.
- **Earnings prep brief** — Pre-call brief LLM-grounded.

### YouTube / podcast / news
- **YouTube batch** — Ingest canal/lista YouTube.
- **YouTube re-extract** — Re-extract só Ollama (sem rede).
- **YouTube digest** — Digest SQL-only por canal.
- **News fetch + classify** — Fetch + classify (cron horário).
- **Exa news monitor** — Varre universo → tabela news.

### Subscriptions
- **Ingest relatórios subscriptions** — Suno/XP/WSJ ingest.
- **Views de analistas sobre ticker** — Query analistas por TK.

### Research / memos
- **Research memo unificado** — Phase J (PT/EN).
- **Batch research scan** — Todas as holdings BR+US.
- **Research memo com preço live** — Memo + intraday.
- **Research digest** — Bibliotheca daily report.

### DRIP / dividendos / FX
- **Payback DRIP de X** — Anos para 2× shares + cash payback.
- **Earnings calendar** — Próximas datas earnings holdings.
- **Earnings surprise** — YT targets vs real (Phase H).
- **FX total BR+US em BRL** — Total consolidado em BRL.

### Verdict / dossiers
- **Verdict engine** — BUY/HOLD/SELL agregado.
- **Verdict history + backtest** — Track record dos verdicts.
- **`ii deepdive <TK>`** — Pipeline 4-camadas (V10 Personal Equity Valuator).
- **Fair Value Forward (EXPERIMENTAL)** — DCF 2-estágios sobre owner earnings.

### Reports / briefings / triggers
- **Morning briefing** — Briefing matinal consolidado (Ollama).
- **Daily diff** — O que mudou vs ontem.
- **Streamlit dashboard** — Dashboard localhost:8501.
- **Agent matinal** — `ii agent` (cron 09:30).
- **Snapshot MV diário** — Snapshot market value.
- **Earnings react** — Re-fetch on novo filing.
- **Telegram push** — Mensagem ad-hoc Telegram.
- **Captain's log Telegram push** — Brief diário Telegram (23:30).
- **Gerir open triggers** — List/resolve/ignore triggers.

### Peer / size / rebalance
- **Peer compare** — Percentil vs sector peers.
- **Rebalance assistant** — Drift + sugestões trades.
- **Position size Kelly-lite** — Sizing Kelly conservador.

### Metrics / observability
- **Metrics baseline freeze** — Freeze baseline (Phase W).
- **Metrics daily report** — Delta vs baseline.

### RI / CVM / SEC
- **RI bank quarterly** — Parser bank quarterly.
- **RI CVM filings** — Filings oficiais CVM.
- **RI compare releases** — Itera quarters disponíveis.
- **RI CVM parser** — DRE/BPA/BPP/DFC → quarterly_history.
- **RI CVM bank parser** — Schema BACEN (bancos BR).
- **RI quarterly single** — Resolve YTD artifact (Qn=ITRn-ITRn-1).
- **RI FII filings** — CVM inf_mensal NAV/DY/cotistas.
- **RI catalog autopopulate** — universe.yaml → catalog.
- **CVM PDF extractor** — Download+pdfplumber → events.full_text.
- **CVM monitor** — BR fatos relevantes diários.
- **SEC monitor** — US 8-K/10-K/divs.

### Predictions
- **Predictions evaluate** — Closes predictions (track record).

### Reports US/BR
- **Daily update US** — Cron US side.
- **US portfolio report** — Briefing US-only.

### Mission Control
- **Mission Control Next.js** — Front-end localhost:3000.
- **LocalClaw setup check** — Detecta Ollama/Tailscale/MC/Telegram.
- **Topic Watchlist scorer** — Score 0-100 por tema investing.
- **Crew designer** — Audita org + propõe specialists.
- **Visual Office** — Pixel-art rooms localhost:3000/visual.
- **Mission Control front-end COM ESCRITA** — Chat embedded + action buttons.

### Antonio Carlos (Chief of Staff)
- **Antonio Carlos** — Telegram/CLI orchestrator 16-tools.

### Infra / housekeeping
- **Memory cleanup** — Stale/broken/orphan memories.
- **Absorb plugin skills** — Marketplace → local (idempotente).
- **Macro CSV export** — BCB SGS → CSVs diff-friendly.
- **Notify priority events** — Windows Toast eventos críticos.
- **Rotate / archive logs** — >30d → gz.
- **Telegram long-poll loop** — Jarbas live (getUpdates).
- **CLI unificada** — `ii help` mostra tudo.

### Test / dev
- **Test suite typed agents** — Pytest, ~60s, offline.

### Vault / Obsidian
- **Obsidian vault export** — Refresh vault de DB.
- **Skills arsenal index** — `_MOC.md` (33 skills avaliadas).
- **Phase W Roadmap** — `Roadmap.md` (W.1-W.11).

### Legacy
- **Ad Perpetuum Validator** — Wrappado em perpetuum.thesis (removível).

---

## Próximos passos sugeridos

Após leitura, marca em cada secção:
- ✂️ podar (remover)
- 🔄 consolidar com X (merge)
- ⭐ promover (usar mais)
- ❓ investigar (não sei se uso)

Manda-me a lista e eu faço o corte em batch.
