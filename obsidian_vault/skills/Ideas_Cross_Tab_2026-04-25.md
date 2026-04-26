---
type: cross_tab_audit
tags: [audit, ideas, gap_analysis, autocrítica]
date: 2026-04-25
phase: AA (audit + critical-thinking stack)
---

# 🔍 Cross-tab — ~100 ideias propostas vs estado actual

> Resposta honesta ao input do user. Cada categoria mapeada contra o que o sistema **realmente tem** vs **realmente falta**. Auto-crítica explícita.

## Sumário executivo

- **JÁ TEMOS**: ~45% das ideias já implementadas (algumas só parcialmente usadas).
- **GENUINAMENTE NOVO**: ~30% — alto valor, build agora.
- **OVERKILL/SKIP**: ~25% (voice, fine-tuning, family office, satellite data).

## 1. Estrutura/Automação Vault

| # | Ideia | Status | Note |
|---|---|---|---|
| 1.1 | Vault structure raw/wiki/reports | ✅ | tickers/, briefings/, reports/, wiki/, skills/, agents/ |
| 1.2 | Templates company analysis YAML | ✅ | obsidian_bridge.py gera com frontmatter rico |
| 1.3 | Daily digest auto-generated | ✅ | morning_briefing.py + scheduled 23:30 |
| 1.4 | Smart Connections / Copilot Ollama | ✅ | user já tem BMO + Smart Connections (memória) |
| 1.5 | Graph view personalizado | ✅ | Obsidian native + Home.md links agressivos |
| 1.6 | Workflow compilação semanal | ⚠️ Partial | weekly_report.py existe; não corre auto |
| 1.7 | Web Clipper estruturado | ❌ | não wired |
| 1.8 | Canvas dashboard | ⚠️ Partial | 4 .canvas files no vault, vazios |

## 2. RAG Local Documentos Financeiros

| # | Ideia | Status | Note |
|---|---|---|---|
| 2.1 | RAG simples LlamaIndex+Ollama | ✅ | library/rag.py — 1704 chunks indexed |
| 2.2 | Hierarchical chunking tabelas | ❌ | usamos chunks de 2000 chars flat |
| 2.3 | Citações fontes exatas | ✅ | rag.ask devolve [book:chunk N] |
| 2.4 | Earnings call transcripts RAG | ❌ | sem transcripts ingeridos |
| 2.5 | Embeddings nomic-embed | ✅ | 768-dim local |
| 2.6 | Reranking | ❌ | só cosine similarity flat |
| 2.7 | Agentic RAG (decide RAG vs cálculo) | ⚠️ Partial | research_scout.py existe |
| 2.8 | Multi-doc comparison RAG | ✅ | rag.ask cross-book testado (Dalio+Damodaran) |
| 2.9 | Tabelas → CSVs | ❌ | quarterly_history vem de CVM CSVs, não PDFs |
| 2.10 | Quantization tradeoff test | ⚠️ | usamos só Q4_K_M; sem benchmark vs full |

## 3. Agentes / Multi-Agent

| # | Ideia | Status | Note |
|---|---|---|---|
| 3.1 | Financial Agent básico | ✅ | 12 agents + 9 perpetuums |
| 3.2 | Multi-agent investment advisor | ⚠️ Partial | meta_agent.py existe; falta personality debate |
| 3.3 | AI Investment Team (Buffett+Druck+Taleb) | ❌ **GAP** | **AA.2 build now** |
| 3.4 | Tool-decision agent | ✅ | research_scout.py + agentic dispatch |
| 3.5 | Portfolio Manager Agent rebalance | ✅ | rebalance-advisor skill + portfolio_matcher.py |
| 3.6 | Trading Agent backtest | ⚠️ Partial | analytics/backtest_*; sem agent wrapper |
| 3.7 | Screening agent custom | ✅ | scoring/engine.py + library/matcher.py |
| 3.8 | Warp integration | ✅ | ii CLI + dashboard; user usa Warp |
| 3.9 | Supervisor agent revisa outputs | ⚠️ | meta_perpetuum faz audit posterior, não inline |
| 3.10 | Diferentes architectures (debate) | ❌ **GAP** | AA.2 cobre |

## 4. Análise Portfólio / Personal Finance

| # | Ideia | Status | Note |
|---|---|---|---|
| 4.1 | Importar CSVs corretora + categorizar | ✅ | import_portfolio.py, import_taxlots.py |
| 4.2 | Métricas alocação/diversificação | ⚠️ Partial | Allocation.md existe; concentration metric ausente |
| 4.3 | Cenários "se juros sobem 2%" | ❌ **GAP** | falta scenario engine |
| 4.4 | Tracking dividendos + projeção | ✅ | drip_projection.py |
| 4.5 | AI CFO mensal | ❌ | sem flow de personal expenses (não é foco) |
| 4.6 | Teses personalizadas vault-aware | ✅ | overnight populate_thesis usa vault context |
| 4.7 | Rebalance auto sugerido | ✅ | ii rebalance + rebalance-advisor skill |
| 4.8 | Macro overlay | ✅ | analytics/regime.py |
| 4.9 | Drawdown stress test | ❌ **GAP** | falta scenario sim |
| 4.10 | Net worth dashboard | ⚠️ | Streamlit tem básico |

## 5. Dados Frescos / Updates

| # | Ideia | Status | Note |
|---|---|---|---|
| 5.1 | Cron noturno preços/news/filings | ✅ | scheduled task 23:30 |
| 5.2 | Scraper RI brasileiro | ❌ | usamos CVM oficial em vez de scrape |
| 5.3 | Yahoo Finance + Alpha Vantage | ✅ | yfinance + brapi |
| 5.4 | News intelligence agent | ⚠️ | news_fetch.py + classify; sentiment ainda raw |
| 5.5 | SearXNG local | ❌ | usamos Tavily MCP (paid) ou nada |
| 5.6 | Earnings releases auto-takeaways | ❌ **GAP** | AA.4 cobre |
| 5.7 | SEC/CVM monitoring + notify | ✅ | cvm_monitor.py + sec_monitor.py + Telegram |
| 5.8 | Cache inteligente | ⚠️ | TTL fixo; sem delta-trigger |
| 5.9 | Frequência update teste | ❌ | sem A/B |

## 6. Geração Relatórios

| # | Ideia | Status | Note |
|---|---|---|---|
| 6.1 | Equity research auto | ⚠️ | research.py básico; falta riqueza visual |
| 6.2 | DCF model template | ❌ | sem template DCF; methods extraídos do Damodaran têm fórmula |
| 6.3 | Investment memo auto | ⚠️ Partial | research.py + verdict; não segue formato pro |
| 6.4 | Análise comparativa pares | ✅ | peer_compare.py |
| 6.5 | Moat extraction MD&A | ❌ **GAP** | quick win com Ollama |
| 6.6 | Flashcards conceitos | ❌ | overkill |
| 6.7 | Visualizações Mermaid | ❌ | usamos Charts plugin |
| 6.8 | Performance mensal narrativa | ✅ | morning_briefing |
| 6.9 | What-if analysis | ❌ **GAP** | scenario engine missing |
| 6.10 | Refinar teses antigas com new context | ✅ | thesis_refresh.py |

## 7. Warp / Claude Code Integrations

| # | Ideia | Status | Note |
|---|---|---|---|
| 7.1 | Warp Ollama backend | ✅ | user roda Ollama |
| 7.2 | Claude Code itera scripts | ✅ | esta sessão |
| 7.3 | "analyze-ticker" pipeline | ✅ | ii panorama |
| 7.4 | n8n workflows | ❌ | overkill (skip declarado em SKL_tier_B) |
| 7.5 | Fine-tuning local | ❌ | overkill |
| 7.6 | CLI personalizada | ✅ | ii super-CLI |
| 7.7 | Voice input | ❌ | overkill |
| 7.8 | Versionamento análises | ⚠️ | git mas sem diff narrativo |
| 7.9 | Code review auto | ❌ | feature interessante; baixa prioridade |
| 7.10 | Hybrid Claude+Ollama loop | ✅ | é o pattern dominante já |

## 8. Avançadas/Experimentais

| # | Ideia | Status | Note |
|---|---|---|---|
| 8.1 | Knowledge graph | ⚠️ | Obsidian native; sem entity graph cross-file |
| 8.2 | Multi-agent debate bull/bear | ❌ **GAP** | AA.2 cobre |
| 8.3 | Scoring proprietário | ✅ | scoring/engine.py |
| 8.4 | Mic local earnings | ❌ | overkill |
| 8.5 | Backtest LLM strategies | ⚠️ | analytics/backtest_*; sem LLM-generated strategies |
| 8.6 | Bio/química portfolio | ❌ | not applicable |
| 8.7 | AI Hedge Fund $10M virtual | ⚠️ | paper_trade_signals é proxy; falta full virtual book |
| 8.8 | Modelos diferentes Qwen/DeepSeek/Llama | ❌ | só Qwen 14B |
| 8.9 | Memory persistente correções | ✅ | ~/.claude/memory + MEMORY.md |
| 8.10 | Hybrid local+API | ✅ | mas evita API por regra |

## 9. Research/Intelligence (lista grande)

| # | Ideia | Status |
|---|---|---|
| 9.1 | Live SEC copilot | ⚠️ Partial — sec_monitor existe, sem deviation detection |
| 9.2 | Earnings call deviation | ❌ **GAP** |
| 9.3 | Variant perception | ❌ **GAP** — **AA.3 build** |
| 9.4 | Perplexity privado setorial | ✅ — library/rag.py com filtro book |
| 9.5 | Research memo auto-generator | ⚠️ research.py |
| 9.6 | Consensus breaker bot | ❌ — variante de AA.3 |
| 9.7 | Counter-thesis engine | ✅ — devils_advocate.py |
| 9.8 | Expert synthetic panel | ❌ **GAP** — **AA.2** |
| 9.9 | Management credibility tracker | ❌ — high effort |
| 9.10 | Event impact mapper | ❌ — high effort |

## 10. Alternative Data

| # | Ideia | Status |
|---|---|---|
| 10.1-10.10 | Freight, satellite, jobs, patents, supply, insider, credit, estimate revisions, commodity, regulatory | ❌ TODOS — **explicitamente skip** (precisa data sources externos pagos) |

## 11. Portfolio Intelligence

| # | Ideia | Status |
|---|---|---|
| 11.1 | Synthetic risk committee diário | ⚠️ — risk_auditor.py existe, sem diário multi-agent |
| 11.2 | Position kill-switch | ⚠️ — perpetuum_thesis flag mas sem auto-action |
| 11.3 | Conviction scoring engine | ⚠️ — verdict engine existe |
| 11.4 | Portfolio fragility map | ❌ **GAP** |
| 11.5 | Hidden factor exposure | ❌ **GAP** — **AA.5 build** |
| 11.6 | Regime-shift allocator | ⚠️ — analytics/regime.py + alocator overlay falta |
| 11.7 | Drawdown war-game | ❌ **GAP** |
| 11.8 | Concentration stress | ❌ **GAP** — **AA.5 build** |
| 11.9 | Correlation breakdown monitor | ❌ |
| 11.10 | Position sizing co-pilot | ✅ — position_size.py (Kelly-lite) |

## 12. Decision Quality / Meta

| # | Ideia | Status |
|---|---|---|
| 12.1 | Decision journal intelligence | ❌ **GAP** — **AA.6 build** |
| 12.2 | Bias detector | ❌ |
| 12.3 | Premortem generator | ❌ |
| 12.4 | Postmortem engine | ❌ |
| 12.5 | Mistake taxonomy | ❌ |
| 12.6 | Second-order consequence | ❌ |
| 12.7 | Disconfirming evidence hunter | ✅ — devils_advocate é versão disto |
| 12.8 | Narrative vs reality | ⚠️ — perpetuum_thesis tracks |
| 12.9 | Historical analog engine | ❌ — high effort |
| 12.10 | Thesis decay monitor | ✅ — perpetuum_thesis = exatamente isto |

## 13. Quant / Models

| # | Ideia | Status |
|---|---|---|
| 13.1-13.10 | Factor discovery, event-driven, Monte Carlo, Bayesian | ⚠️ Partial — backtest_yield, regime; falta Monte Carlo + Bayesian explícito |

## 14. Knowledge Graph / Obsidian

| # | Ideia | Status |
|---|---|---|
| 14.1-14.10 | Living graph, causal map, thesis genealogy, idea collision | ⚠️ Native Obsidian + Dataview cobre 60%; sem entity-graph cross-file |

## 15. Agentic / Autonomous

| # | Ideia | Status |
|---|---|---|
| 15.1 | Autonomous overnight loop | ✅ — orchestrator.py corre 5 phases |
| 15.2 | Watchlist sentinel | ⚠️ — perpetuum_thesis itera holdings, não watchlist |
| 15.3 | Earnings prep bot | ❌ **GAP** — **AA.4** |
| 15.4 | Sector swarm | ❌ |
| 15.5 | Continuous thesis monitor | ✅ — perpetuum_thesis |
| 15.6 | Idea generation engine | ⚠️ — research_scout |
| 15.7 | Agent debate tournament | ❌ — variant de AA.2 |
| 15.8 | Self-improving prompts | ❌ — DSPy roadmap (W.6) |
| 15.9 | Autonomous red team | ✅ — devils_advocate é isto |
| 15.10 | OS orchestrator | ✅ — perpetuum_master.py é o coordenador |

## 16. Family Office / Mini Fund

| # | Ideia | Status |
|---|---|---|
| 16.1 | IC memo workflow | ⚠️ — verdict é proxy |
| 16.2 | Shadow portfolio | ✅ — paper_trade_signals + watchlist |
| 16.3 | Research CRM | ❌ |
| 16.4 | Opportunity funnel | ❌ |
| 16.5 | PM dashboard | ⚠️ — Streamlit tem ; pode melhorar |
| 16.6 | Synthetic CRO | ✅ — risk_auditor.py |
| 16.7 | Idea incubation | ❌ |
| 16.8 | Portfolio OS | ✅ |
| 16.9 | Private Bloomberg | ⚠️ — Phase Z (UI) é exactly isto |
| 16.10 | Family office stack | ✅ — é o que estamos a construir |

## 17. Frontier/Experimental

| # | Ideia | Status | Recomendação |
|---|---|---|---|
| 17.1 | Market digital twin | ❌ | overkill |
| 17.2 | Agentic macro sim | ❌ | overkill |
| 17.3 | Reflexivity detector | ❌ | overkill |
| 17.4 | Internal prediction market | ❌ | overkill |
| 17.5 | Synthetic channel checks | ❌ | overkill |
| 17.6 | Alpha attribution | ❌ **GAP** | useful, baixo effort |
| 17.7 | Cognitive leverage dashboard | ❌ | depende de tracking explícito |
| 17.8 | Fine-tuned digital twin | ❌ | skip — fine-tuning não vale ROI |
| 17.9 | Self-critiquing copilot | ✅ | meta_perpetuum |
| 17.10 | Sovereign intelligence | ✅ | é a meta-target do projecto |

## 🎯 Construir AGORA (Sprint AA)

Baseado nos GAPs marcados:

1. **AA.2 Synthetic IC** — multi-personality debate (Buffett, Druckenmiller, Taleb, Klarman)
2. **AA.3 Variant Perception** — diff entre analyst_insights consensus vs nossa thesis
3. **AA.4 Earnings Prep Cockpit** — pre-call memo usando quarterly_history + analyst views + thesis
4. **AA.5 Portfolio Stress** — concentration + hidden factor exposure + drawdown war-game
5. **AA.6 Decision Journal Intel** — pattern mining em past notes + actions + outcomes

**Skip por overkill** (documentado): satellite/freight/insider data, voice, fine-tuning, market digital twin, prediction market interno.

**Quick fixes pending** (não são "novos" mas precisam):
- ITRs CVM 2019-2023 backfill (Y.9)
- Watchlist auto-populator matches errados (ITUB4/SUZB3/TTEN3)
- fii_monthly DY display em decimal vs %
- Bank-specific schema BBDC4/ITUB4
- Streamlit dashboard expand (Phase Z)

## 🪞 Auto-crítica honesta

**O que temos que NÃO uso bem**:
- 5 skills custom criados mas nunca confirmei se disparam auto em sessões — falta proof
- Streamlit dashboard existe mas eu próprio não a abri esta sessão
- 12 agents + 9 perpetuums pode ser bloat — meta_perpetuum disse content_quality é "noisy"
- 1,152 methods extraídos mas só 16 viraram YAML — 99% sentado
- 932 paper signals open sem track record yet (precisa tempo)

**O que é genuinamente forte**:
- CVM pipeline (Phase Y) — primary source, deterministic
- RAG cross-book funcional em PT
- Perpetuum engine pattern escala
- Constitution criada hoje resolve "voltar e não saber onde estou"

**O que está perigosamente fofo**:
- Thesis populadas via Ollama (28 holdings) ainda não revistas pelo user — podem ter assumptions ruins encrustadas
- Auto-populator watchlist gerou matches errados que se passados por cima viram dados maus
- Bank schema generic (BBDC4 ITUB4) — números podem estar enviesados

**Onde estou a fugir do trabalho difícil**:
- Bank-specific BACEN schema (chato mas necessário)
- ITRs 2019-2023 backfill (trivial, só não fiz)
- UI friendly (Phase Z handoff existe mas é escape)
- Promover perpetuums além T2 (T3 worktree é onde valor real escala)
