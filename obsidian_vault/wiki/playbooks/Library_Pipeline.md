---
type: playbook
name: Library + Paper Trade pipeline
tags: [playbook, library, paper_trade, ollama, rag]
related: ["[[Token_discipline]]", "[[Youtube_Pipeline]]", "[[Agents_layer]]", "[[Analyst_Tracking]]", "[[Web_scraping_subscriptions]]"]
---

# 📚 Library Pipeline — books → methods → paper signals, zero tokens

> Pipeline que transforma livros (PDF/EPUB/MD) e clippings web em **métodos de investimento estruturados** (`library/methods/*.yaml`) e **paper-trade signals** (tabela `paper_trade_signals`) — usando só Ollama local + SQLite. Cumpre [[Token_discipline]] (REGRA #1): zero Claude tokens em todo o flow regular.

## Princípio

**Books → chunks persistentes → methods YAML reusáveis → matcher determinístico → paper signals trackable.** O LLM (Qwen) só toca a fase de extracção de methods e RAG; o matcher é eval restrito Python (sem rede, sem LLM). Real capital **nunca** dispara directamente — passa sempre pela tabela `paper_trade_signals` e exige track record antes de promoção.

## Pipeline (5 fases)

```
PDF/EPUB ──► chunker ──► Ollama (extract) ──► YAML methods ──► matcher ──► paper_trade_signals
(books/)    (chunks/)    (Qwen 14B)         (methods/)        (eval)      (BR + US DBs)
                │                                                            │
                └────► nomic-embed ──► chunks_index.db ──► RAG query/ask     └► close (cron 23:30)
                       (768-dim)        (cosine top-K)     (Qwen synth)
```

| # | Fase | Módulo | Modelo / Tool | Output |
|---|---|---|---|---|
| 1 | Ingest book → chunks | `library/ingest.py` | `pypdf` / `ebooklib` | `library/chunks/<slug>/NNNN.txt` + `meta.json` |
| 2 | Ingest clipping → chunks | `library/clippings_ingest.py` | regex frontmatter + chunker | `library/chunks/clip_<slug>/` |
| 3 | Extract methods | `library/extract_insights.py` | `qwen2.5:14b-instruct-q4_K_M` (Ollama) | `library/insights/<slug>.json` (drafts → review → `methods/*.yaml`) |
| 4 | Build RAG index | `library/rag.py build` | `nomic-embed-text:latest` (Ollama, 768-dim) | `library/chunks_index.db` rows |
| 5a | Match methods → signals | `library/matcher.py` | restricted `eval()` over fundamentals | rows em `paper_trade_signals` (status=open) |
| 5b | Close expired signals | `scripts/paper_trade_close.py` | SQL + horizon math | rows com status=closed, win flag, realized_return_pct |

### 1. Ingest (`library/ingest.py`)
PDFs via `pypdf` (concat all pages); EPUB via `ebooklib + bs4`; `.md`/`.txt` directo. Chunks ~2000 chars com overlap 200 (helper em `library/_common.py::chunk_text`). Boundaries de parágrafo respeitados quando possível.

**Idempotente**: `meta.json` guarda `file_hash`. Re-run com mesmo file → `skipped_unchanged`. `--force` re-ingere tudo.

### 2. Clippings (`library/clippings_ingest.py`)
Espelha `ingest.py` para `obsidian_vault/Clippings/*.md` (Web Clipper output: Investopedia / Suno / Motley Fool, etc.). Frontmatter YAML é parseado (title, source URL, author, published, tags) e guardado em `meta.json`. **Namespace separado** via prefixo `book_slug='clip_<slug>'` no chunks_index.

Flag `--rag-build` chama embedding directo após ingest. `--list` mostra inventory + estado de embed.

### 3. Extract methods (`library/extract_insights.py`)
Sample stride-based dos chunks (skip 3 primeiros + 2 últimos = intro/biblio). Para cada chunk amostrado, 1 chamada `ollama.chat` (via `agents._llm.ollama_call`, JSON mode, `temperature=0.2`, `max_tokens=800`).

Schema de resposta (Pydantic-friendly):
```json
{
  "has_substance": bool, "is_filler": bool,
  "methods": [{"name": "...", "description": "...", "rules_or_formula": "..."}],
  "heuristics": [...], "key_concepts": [...],
  "tickers_or_assets": [...], "regime_conditions": [...],
  "one_line_takeaway": "..."
}
```

Aggregate dedup por `name.lower()[:60]`. Output `library/insights/<slug>.json`. Drafts em `library/methods/drafts/` viram YAML production em `library/methods/<id>.yaml` (review manual).

**Modelo default**: `qwen2.5:14b-instruct-q4_K_M`. Override via `--model`. JSON malformado → best-effort regex repair (trailing commas).

### 4. RAG index (`library/rag.py`)
Embed cada chunk via `nomic-embed-text` Ollama (768 dims, 8k context). Storage em `library/chunks_index.db`:

```sql
CREATE TABLE chunk_index (
    book_slug   TEXT NOT NULL,
    chunk_file  TEXT NOT NULL,
    text        TEXT NOT NULL,
    embedding   BLOB NOT NULL,    -- struct.pack('<Nf', *vec)
    n_tokens    INTEGER,
    PRIMARY KEY (book_slug, chunk_file)
);
CREATE INDEX idx_chunk_book ON chunk_index(book_slug);
```

**Estado actual (2026-04-28)**: 2.007 chunks indexados; books cobertos: `investment_valuation_3rd_edition` (1043), `principles_for_navigating_big_debt_crises` (550), `cwo_power_index` (59), `daliochangingworldordercharts` (52); 30+ clippings (`clip_*`).

3 sub-comandos:
- `build` — embed missing chunks (idempotente; skip se já existe row)
- `query "<text>"` — embed query, cosine over all rows in-memory, top-K
- `ask "<question>"` — query + Qwen 14B sintetiza resposta citando `[book:chunk]`. **Ainda zero Claude tokens.** Synthesis prompt: "Use ONLY the sources below. Cite each claim with [book:chunk]. If sources don't answer, say so." `temperature=0.3`, `num_predict=600`, max 400 words.

Cosine cálculo é Python puro (sem numpy required) — adequado para escala actual (2k chunks). Para >50k consideraria `sqlite-vss`.

### 5a. Matcher (`library/matcher.py`)
Para cada method YAML × ticker (holdings + watchlist) × market (BR + US):
1. Pull last `fundamentals` row + last `prices.close`
2. Bag de variables: `pe, pb, dy, roe, eps/lpa, bvps/vpa, net_debt_ebitda, dividend_streak_years, price` + placeholders (`market_cap_usd, current_ratio, ltd, working_capital, positive_earnings_years_10, eps_3y_avg_growth_10y, pe_on_3y_avg_earnings`)
3. Para cada `rule.check` (string Python-like): `_safe_eval_check` faz eval restrito (`__builtins__={}`, blocked tokens: `import|eval|exec|open|__|lambda`)
4. Se **todas** as rules passam → `apply_method` chama `library.paper_trade.log_signal()`

Method YAML schema mínimo:
```yaml
id: graham_defensive
name: "Graham Defensive Investor"
book: "Graham_Intelligent_Investor"
direction: LONG
horizon: long          # short | medium | long
expected_move: {target_pct: 20}
rules:
  - id: r1
    description: "P/E ≤ 15"
    check: "pe <= 15"
  - id: r2
    check: "pb <= 1.5 and dy >= 4"
```

Variáveis com `None` → rule auto-fail com `missing vars: [...]`. Sem isto, expressões partem.

### 5b. Close expired (`scripts/paper_trade_close.py`)
Cron 23:30 (wired em `daily_run.bat`, F1 do T0 cleanup 2026-04-26). Sem este script, signals never close → `win_rate` undefined → real capital nunca liberado.

Horizon → days mapping (hardcoded):
| `horizon` | days | racional |
|---|---|---|
| `short`  | 30  | earnings reaction window |
| `medium` | 90  | 1 quarter (Damodaran/Graham) |
| `long`   | 365 | 1 ano (Buffett/compounder) |
| missing  | 90  | `DEFAULT_HORIZON_DAYS` fallback |

Realized return:
- `LONG`/`NEUTRAL`: `(close - entry) / entry × 100`
- `SHORT`: `(entry - close) / entry × 100`

Win flag (em `notes` JSON):
- `LONG`/`SHORT`: win se `realized ≥ expected_move_pct × 0.5` (50%+ do alvo)
- `NEUTRAL`: win se `abs(realized) < expected_move_pct` (ficou dentro da banda)

Close price: prefere preço **on-or-before** `target_close_date`; fallback latest close.

## Comandos

| Caso | Comando |
|---|---|
| Ingest novos books | `python -m library.ingest` |
| Ingest 1 padrão | `python -m library.ingest --book "Dalio_*"` |
| Re-ingest forçado | `python -m library.ingest --force` |
| Listar books processados | `python -m library.extract_insights --list` |
| Extract methods 1 book | `python -m library.extract_insights --book <slug> --max 40` |
| Extract methods all | `python -m library.extract_insights --all` |
| Ingest clippings vault | `python -m library.clippings_ingest` |
| Clippings + embed | `python -m library.clippings_ingest --rag-build` |
| Inventário clippings | `python -m library.clippings_ingest --list` |
| RAG build (embed all) | `python -m library.rag build` |
| RAG build subset | `python -m library.rag build --book dalio_*` |
| RAG query semantic | `python -m library.rag query "capital flow crisis pre-signals" --k 5` |
| RAG ask (Qwen synth) | `python -m library.rag ask "como o Dalio detecta bubble?" --k 8` |
| RAG status / coverage | `python -m library.rag status` |
| Matcher all methods | `python -m library.matcher` |
| Matcher 1 método | `python -m library.matcher --method graham_defensive` |
| Matcher dry-run | `python -m library.matcher --dry-run` |
| Matcher subset market | `python -m library.matcher --market br` |
| Close expired signals | `python scripts/paper_trade_close.py` |
| Close preview | `python scripts/paper_trade_close.py --dry-run` |
| Close force-all (debug) | `python scripts/paper_trade_close.py --all-now` |
| Listar open signals | `sqlite3 data/us_investments.db 'SELECT * FROM paper_trade_signals WHERE status="open"'` |
| Performance per method | `python -c "from library.paper_trade import performance_by_method; print(performance_by_method(min_closed=5))"` |

## Schemas

### `library/chunks_index.db` (RAG)
1 tabela única (acima). Embedding como BLOB packed `<Nf` (little-endian float32). Cobre books **e** clippings via prefixo `book_slug`.

### `paper_trade_signals` (em **ambas** as DBs `data/{br,us}_investments.db`)
```sql
CREATE TABLE paper_trade_signals (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_date         TEXT NOT NULL,        -- ISO 'YYYY-MM-DD'
    ticker              TEXT NOT NULL,
    market              TEXT NOT NULL,        -- 'br' | 'us'
    method_id           TEXT NOT NULL,        -- ref library/methods/<id>.yaml
    book_slug           TEXT,                 -- which book seeded the method
    direction           TEXT NOT NULL,        -- 'LONG' | 'SHORT' | 'NEUTRAL' | 'PAIR' | ...
    horizon             TEXT,                 -- 'short' | 'medium' | 'long'
    expected_move_pct   REAL,
    entry_price         REAL,
    thesis              TEXT,                 -- narrative (why method fired)
    status              TEXT DEFAULT 'open',  -- 'open' | 'closed' (legacy: 'closed_win'/'closed_loss'/'closed_flat'/'expired')
    closed_at           TEXT,
    closed_price        REAL,
    realized_return_pct REAL,
    notes               TEXT                  -- JSON: {closed_by, win, horizon_days, ...}
);
```
Indexes: `idx_paper_status`, `idx_paper_ticker`, `idx_paper_method`.

❓ verify: docstring de `library/paper_trade.py` lista `closed_win/closed_loss/closed_flat/expired` como valores de `status`, mas `paper_trade_close.py` (F1 cleanup 2026-04-26) escreve apenas `'closed'` com `win` flag dentro do `notes` JSON. Schema convergente é `'open' → 'closed'`; legacy strings podem coexistir em rows antigas via `resolve_signal()` legacy path.

### Estado actual (2026-04-28)
- **956 open** US, **780 open** BR (todos `2026-04-24`/`2026-04-25`) → **0 closed**.
- Top methods por volume: `damodaran_auto_geometric_mean_growth` (206), `damodaran_implied_equity_premium` (172), `damodaran_auto_valuation_method` (160).
- 17 YAMLs em `library/methods/` (4 Dalio + 12 Damodaran auto-extracted + 1 Graham + 1 US bank Buffett seed).
- Daily cron close já wired mas ainda nenhum signal atingiu horizon (medium=90d).

## Memory rule — paper-only default

> **Real capital só após ≥30 closed signals com `win_rate > 60%` E `avg_return_pct > 0`**, por método. Ver memory `library_and_paper_trade.md`.

| Tier | Quando | Acção |
|---|---|---|
| **Paper** (NOW) | Sempre | Toda signal de method/matcher/extract entra em `paper_trade_signals` com `status=open`. NÃO aciona broker. |
| **Stat-significant** (+90d) | ≥30 closed signals/method | Mede `win_rate, avg_return, max DD, range`. Floor: 20; confortável: 50+. |
| **Real capital** (+6m) | win_rate>60% **and** avg_return>0 **per method** | Max 2% portfolio per signal. Hard stops. |
| **Options overlay** (+12m) | IC>0.05 + vol data infra (que não temos) | Covered calls em holdings primeiro (sell premium). Nunca buy puts/calls speculatively. |

**Forbidden**: sugerir put/call de 5% em período curto baseado só em method-match. São lottery tickets com narrativa. Histórico em [[Library_Books_and_Options]].

## Token economics

| Acção | Custo Claude | Custo Ollama / local |
|---|---|---|
| Ingest 1 book PDF | 0 | <30s pypdf |
| Extract methods 40 chunks | 0 | ~5-15min Qwen 14B |
| RAG build 2k chunks | 0 | ~10min nomic-embed |
| RAG query top-K | 0 | <1s embed + cosine in-memory |
| RAG ask (Qwen synth) | 0 | ~10-30s |
| Matcher full universe (BR+US) | 0 | <30s SQL + eval |
| Close expired signals | 0 | <5s SQL |
| **Total pipeline / livro novo** | **0** | ~20min, depois reusable |

**Crítico**: `library/extract_insights.py` usa `agents._llm.ollama_call` (canonical). Quando user pergunta "o que diz Graham sobre X" → `library.rag ask` antes de chamar Claude (poupa ~15k tokens vs ler raw chunks).

## Limitações conhecidas

- **Variables-missing burn**: muitas rules failam com `missing vars: [...]` porque `fundamentals` não tem `current_ratio/ltd/positive_earnings_years_10/eps_3y_avg_growth_10y`. Backfill via `scripts/enrich_fundamentals_for_methods.py` (parcial). Sem isto, scoring degrada para subconjunto pequeno de tickers.
- **Sem cooldown no matcher**: `apply_method` cria signal **toda vez** que rules passam para um (ticker, method) — pode acumular duplicados se cron correr 2× no dia. ❓ verify: nenhum `cooldown` ou unique-on-open enforcement encontrado em `library/matcher.py` ou `library/paper_trade.py`. Mitigação actual: perpetuum `library_signals` está `enabled=False` (frozen 2026-04-26 T0 cleanup) até haver win_rate trackable.
- **Auto-extracted Damodaran methods**: 12 yamls `damodaran_auto_*` foram gerados pelo extractor com nomes-de-fórmula como methods (e.g. `geometric_mean_growth`, `unlevered_beta_quality`). São fórmulas, não estratégias accionáveis — geram muitos signals near-meaningless. Triagem manual pendente.
- **Eval restrito é restrito**: só comparações + `and`/`or`/`not` + numeric. Sem `min/max/abs`. Method que precisa `abs(growth - 0.05) < 0.02` não funciona.
- **Cosine in-memory**: RAG carrega todos os 2k vectors em RAM por query. Linear OK até ~50k; depois precisa `sqlite-vss` ou FAISS.
- **0 closed signals (2026-04-28)**: pipeline de close foi shipped 2026-04-26 mas oldest signals são 2026-04-24 com horizon `medium=90d`. Primeiros closes só ~2026-07-23. Win-rate é literalmente untrackable até lá.
- **Schema drift `status`**: paper_trade.py docstring + `resolve_signal` antigo escrevem `closed_win/loss/flat`, mas `paper_trade_close.py` actual escreve apenas `'closed'` + win em notes JSON. SQL queries de performance precisam acomodar ambos.

## Integrações

- **Perpetuum `library_signals`** (`agents/perpetuum/library_signals.py`) — corre matcher diário; T1 Observer; **frozen** (`enabled=False`) desde 2026-04-26 até ≥30 closed signals com win_rate measurable.
- **Perpetuum `tokens`** — tracks Claude usage; library/RAG operations devem aparecer com custo zero (validation que pipeline está local).
- **Daily cron** (`daily_run.bat`, 23:30) — chama `paper_trade_close.py` antes de Captain's Log Telegram push.
- **`agents._llm.ollama_call`** (canonical, post-workday-2026-04-27 dedup) — usado por `extract_insights.py`. Não criar novos wrappers Ollama; reutilizar.
- **Bibliotheca v2** — clippings ingest popula RAG; `obsidian_vault/Bibliotheca/_Index.md` é hub; `Research_Digest_<DATE>.md` perpetuum consome via `library.rag query`.
- **Tutor injector** (Bibliotheca) — research memos / dossiers fazem `library.rag query "PE ratio explained beginner"` para enriquecer com fontes.
- **Verdict engine + research.py** — secção `[L] LIBRARY` poderia injectar top-3 relevant chunks via RAG para contextualizar verdict (Phase futura).

## Workflow recomendado

1. **Antes** de pedir "explica o que Dalio diz sobre X" → `python -m library.rag ask "..."` primeiro. Feed Claude com a resposta + cites se precisar refinar.
2. Novos books → drop em `library/books/` → `python -m library.ingest` → `python -m library.extract_insights --book <slug> --max 40` → review drafts → promote para `library/methods/<id>.yaml` → `python -m library.rag build`.
3. Antes de promover method para T2 (auto-log signals) → matcher `--dry-run` por 30+ days; medir false-positive rate.
4. Para iterar method YAML rules → `python -m library.matcher --method <id> --dry-run` (sem queimar signals).
5. Diagnóstico paper performance → `paper_trade.performance_by_method(min_closed=5)` (Python helper) ou SQL ad-hoc com `HAVING closed_n >= 20`.

## Ver também

- [[Token_discipline]] — porque tudo Ollama local
- [[Youtube_Pipeline]] — pipeline irmão (vídeo vs texto)
- [[Agents_layer]] — `library_signals` perpetuum vive aqui
- [[Library_Books_and_Options]] — strategic doc histórico (staged-trust → options)
- [[Analyst_Tracking]] — counterpart (analyst predictions ↔ paper signals; ambos closed via cron)
- `library/__init__.py` — package overview
- `library/methods/*.yaml` — YAML schema canónico
- `library/chunks_index.db` — RAG storage
- `data/{br,us}_investments.db::paper_trade_signals` — signal log
