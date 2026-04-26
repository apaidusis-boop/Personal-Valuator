---
type: roadmap
phase: Z
title: UI Friendly Layer
created: 2026-04-25
status: in_progress
---

# 🎨 Phase Z — UI Friendly Layer

> Eliminar comandos terminal do flow normal. Tudo visível, navegável, com clique.

## 🎯 Objectivo

Transformar o sistema de "CLI com side outputs em vault" para "dashboard navegável com vault como knowledge base". O backend (perpetuums, fetchers, RAG, scoring) **não muda**. Só wrappar.

## 🧭 Decisão arquitectural — Opção D (Mix), pesada em Streamlit

| Camada | Tech | Para quê |
|---|---|---|
| **Interactive** | Streamlit (`scripts/dashboard_app.py`) | Approve actions, ask library, screener live, deep dive |
| **Read flow normal** | Obsidian + Dataview + Charts | Ticker notes, wiki, briefings, RI timelines |
| **Deliverables** | (futuro) HTML/Jinja2 | Weekly/quarterly reports portáveis |

**Porquê não rewrite em React/Next**: Streamlit já tem 5 páginas funcionais (~420 LOC), gráficos plotly, cache, sidebar nav. 80% feito. Reescrever em React custa semanas e zero benefício para single-user local.

**Porquê não Obsidian-only**: Dataview é poderoso mas não corre subprocess (não consegue approve actions, não consegue chamar RAG).

**Porquê não Static HTML**: bom para deliverables (weekly), mas não para o flow diário interactive.

## 📋 Sprints

### Z.0 — Scope freeze + roadmap (este doc) ✅
Decisão arquitectural + plano + commit.

### Z.1 — T2 Actions queue page 🔄
**Página nova** no Streamlit: `🎯 Actions Queue`.
- Lista `watchlist_actions WHERE status='open'` (BR + US)
- Por linha: ticker, kind, action_hint, opened_at, notes
- Botões **✅ Approve / ❌ Ignore / 📝 Note**
- Approve: chama `python scripts/perpetuum_action_run.py <id>` se whitelisted, senão `action_cli.py resolve`
- Confirma com modal antes de executar (anti-clique-acidental)

**Critério de sucesso**: Conseguir resolver os 20 triggers abertos hoje sem terminal.

### Z.2 — Ask Library page
**Página nova**: `📚 Ask Library`.
- Text input PT
- Botão "Ask"
- Spinner enquanto roda `python -m library.rag ask "..." --k 6` (subprocess)
- Mostra resposta formatada + chunks fonte expansíveis
- Histórico das últimas 10 perguntas em sidebar

**Critério de sucesso**: Conseguir perguntar "Qual a melhor empresa BR pelos critérios Damodaran?" e ler resposta sem touch terminal.

### Z.3 — Perpetuum Health dashboard
**Página nova**: `🩺 Perpetuum Health`.
- Tabela: 9 perpetuums × (last_run, rows, top_flagged_subject, score_delta_7d)
- Line chart: `perpetuum_health` rows ao longo de 30d (multi-line per perpetuum)
- Click num perpetuum → drill-down: top 10 flagged subjects com action_hint

**Critério de sucesso**: Detectar visualmente quando um perpetuum começa a degradar (rows estagnadas, last_run > 24h).

### Z.4 — Paper Signals viewer
**Página nova**: `📈 Paper Signals`.
- Filtros: market, method_id, ticker, status, opened_after
- Highlight especial: tickers com **≥2 methods convergentes** (mesmo signal)
- KPIs: open / closed / win_rate / avg_holding_days
- Tabela ordenável

**Critério de sucesso**: Identificar convergent signals (ex: ITSA4 com 3 methods em ADD) sem SQL.

### Z.5 — RI Timeline page
**Página nova**: `📊 RI Timeline`.
- Selectbox ticker BR (5 com CVM data: VALE3, ITSA4, BBDC4, PRIO3, +1)
- Charts: revenue, EBIT, net_income, equity (yoy + qoq)
- Tabela `quarterly_history` últimos 11 trimestres
- Link para `_RI.md` no vault

**Critério de sucesso**: Ver deterioração trimestral de VALE3 (memo: YoY EBIT −25%) num gráfico.

### Z.6 — Obsidian Home.md como morning landing
**Re-escrever** `obsidian_vault/Home.md`:
- Top: Dataview query "decisões pendentes" (open actions resumo)
- Mid: link rápido para latest briefing + dashboard URL
- Charts inline (Charts plugin) com health score por sector
- Sidebar links: Constitution / Tickers / Wiki / Skills

**Critério de sucesso**: Abrir Obsidian de manhã e ter tudo num scroll sem clicar nada.

### Z.7 — One-click launcher
- `start_dashboard.bat` (Windows): activa venv → roda streamlit → abre browser
- Shortcut Desktop com ícone (💼)
- Optional: tray icon que mostra "X actions pending" (deferred se complexo)

**Critério de sucesso**: Double-click no ícone Desktop → dashboard abre sozinho.

## 🛡️ Constraints (não-negociáveis Phase Z)

1. **Zero rewrite backend** — só wrappar `scripts/`, `agents/`, `library/` via subprocess.
2. **Local-first** — Streamlit corre em localhost. Sem cloud, sem auth complexa.
3. **Ollama, não Claude** — RAG via Qwen 14B (já é). Frontend não introduz tokens.
4. **Cada sprint = 1 commit** com changelog na Constitution.
5. **Não criar dependências novas** sem justificar (Streamlit, plotly, pandas já existem).
6. **Não tocar perpetuums** — só consumir o que escrevem em SQLite.

## 📊 Success metrics (fim Phase Z)

- [ ] 7 páginas Streamlit funcionais
- [ ] 0 comandos terminal no workflow matinal típico
- [ ] Home.md Obsidian é landing usável standalone
- [ ] Launcher 1-click funciona
- [ ] Constitution updated com Phase Z section
- [ ] 20 triggers abertos hoje resolvidos via UI (smoke test)

## 🔗 Skills aplicáveis (Phase W catalog)

- **Frontend Design** (Anthropic) — para Z.6 Home.md polish
- **Canvas Design** — opcional para Z.5 charts SVG export
- **Web Artifacts Builder** — não usar; Streamlit já cobre

## 📝 Decision log

| Data | Decisão | Razão |
|---|---|---|
| 2026-04-25 | Opção D (mix), Streamlit pesado | 80% scaffold já existe; Obsidian read-only não cobre interactive |
| 2026-04-25 | Sem React/Next rewrite | Single-user local, custo ≫ benefício |
| 2026-04-25 | Subprocess para chamar CLI tools | Não duplicar lógica; CLI continua canónico |

## ⏭️ Next

Z.1 arranca já. Estimativa: ~30min para T2 Actions page funcional.
