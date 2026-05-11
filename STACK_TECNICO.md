# Stack Técnico — Sistema de Inteligência de Investimentos Pessoal

> Documento para partilha. Foca o **porquê** das escolhas, não o **como** detalhado.
> Núcleo do sistema: rodar 90%+ do trabalho **localmente, sem queimar tokens** de LLM pago,
> e ter **memória persistente** entre conversas para o assistente não recomeçar do zero.

---

## 1. Filosofia central — "In-house first"

A regra-mãe que governa toda a arquitectura:

> **Tudo que possa rodar localmente (SQL, Ollama, scripts existentes) NÃO usa tokens Claude.
> Claude API é último recurso, não primeiro.**

Operacionalmente:
- **L1 — Determinístico** (SQL, regras, fórmulas): sem LLM, custo zero, output reproduzível.
- **L2 — Ollama local** (Qwen 2.5 14B, nomic-embed): LLM grátis, custo só de electricidade.
- **L3 — Claude API** (Sonnet/Opus): só para tarefas que exigem raciocínio multi-domínio profundo
  ou síntese que o local não dá conta.

Cada camada tem que **falhar a tentar** antes da próxima ser invocada. O assistente é treinado
(via memória — ver §3) para escalar conscientemente.

---

## 2. Runtime local — o que substitui APIs pagas

| Necessidade | Solução local | Substitui |
|---|---|---|
| LLM geral (síntese, classificação, parsing) | **Ollama + Qwen 2.5 14B** | Claude / GPT-4 |
| Embeddings semânticos | **nomic-embed-text** (Ollama) | OpenAI ada-002 |
| Vector store / RAG | **SQLite + cosine sim em Python** | Pinecone / Weaviate |
| Transcrição de vídeo | **Whisper** (faster-whisper local) | Whisper API |
| Database | **SQLite** (2 ficheiros: BR + US) | Postgres / Snowflake |
| Scheduling | **Windows Scheduled Tasks** (cron-like) | Airflow / Temporal |
| Search (web, fallback) | **Tavily** (cache 7d + rate-limit gate) | Google / Bing API |
| UI dashboard | **Streamlit local** (`localhost:8501`) | hosted SaaS |
| "Vault" / docs | **Obsidian** (markdown plain, git) | Notion / Confluence |

**Stack Python** mínimo: `yfinance`, `requests`, `sqlite3`, `pyyaml`, `pandas`, `streamlit`,
`ollama-python`. Sem framework de agentes pesado — agentes são scripts Python normais que partilham
um `agents/_llm.py::ollama_call` canónico.

---

## 3. Memória — 3 camadas, persistente entre sessões

O assistente (Claude Code) tem memória **persistente em ficheiros**. Cada conversa nova
arranca já com o estado mental anterior.

### Estrutura
```
~/.claude/projects/<projeto>/memory/
├── MEMORY.md                  # índice (~30 linhas, sempre carregado)
├── feedback_inhouse_first.md  # regras aprendidas
├── portfolio_loaded.md        # facts sobre dados
├── phase_x_perpetuum.md       # estado de iniciativas
└── ...                        # uma memória por tópico
```

### Tipos de memória
1. **`user`** — quem é o utilizador, role, expertise.
2. **`feedback`** — correcções e validações ("não faças X", "sim, esta abordagem é a certa").
   Sempre com **Why** + **How to apply** para julgar edge cases.
3. **`project`** — facts sobre o trabalho em curso (deadlines, decisões, constraints).
4. **`reference`** — pointers para sistemas externos (DBs, dashboards, channels).

### Padrão de gravação
- Ficheiro próprio com frontmatter (`name`, `description`, `type`).
- Pointer de 1 linha em `MEMORY.md`.
- **Nunca** escrever conteúdo directamente no índice.

### O que **não** vai para memória
- Código, arquitectura, file paths → derivável do repo.
- Git history → `git log`/`git blame` é canónico.
- Conversas em curso → isso é contexto, não memória.

**Resultado prático**: o assistente lembra-se de regras como "PVBI11 é tese contrarian, não sugerir
venda", "carteiras BR/US isoladas, não cruzar moeda", "TEN está em distress signal" — sem o
utilizador ter de re-explicar.

---

## 4. Token economy — padrões concretos

### 4.1 Caches em todo lado, com TTL explícito
- **Transcript cache** (YouTube): re-extracção custa só Ollama, zero rede/tokens.
- **Autoresearch cache** (Tavily): 7 dias TTL, rate-limit 100/dia + 50/hora, fallback gracioso.
- **Embedding cache**: chunks já embedados não re-processam.
- **Verdict history**: snapshots diários permitem backtest sem recomputar.

### 4.2 Gating antes de invocar LLM
Padrão típico em código:
```python
# 1. Tenta DB
local_data = query_sqlite(...)
if local_data and len(local_data) >= 3:
    return synthesize_local(local_data)

# 2. Tenta Tavily com cache
cached = tavily_cache.get(key, max_age_days=7)
if cached:
    return cached

# 3. Só agora chama Tavily ao vivo (rate-limited)
if rate_limiter.allow():
    return tavily_search(...)

# 4. Falha graciosa, NÃO escala para Claude
return None
```

Resultado: **Claude API só vê o que realmente precisa de Claude API.**

### 4.3 Routing por tier de tarefa
- Síntese textual simples (resumir filing, extrair insight) → **Ollama Qwen 14B**.
- Classificação rule-based → **Python puro**.
- Decisão de IC ("comprar/segurar/vender com 5 personas a debater") → **Ollama** com prompt
  estruturado por persona, output JSON.
- Síntese multi-domínio com julgamento (este chat) → **Claude API** (manual, pelo utilizador).

### 4.4 Silent batch mode
Pipelines longos correm como `Bash run_in_background` **sem** Monitor a stream-ar output.
Monitor só para debug. Poupa ~10× tokens em conversas com pipelines de horas.

### 4.5 Single-pass extraction
Quando se processa biblioteca de PDFs (livros), o pipeline corre **uma vez** com Ollama,
guarda os insights em `library/methods/*.yaml`, e nunca mais re-processa. Re-runs são
idempotentes e baratos.

---

## 5. Autonomia — "Perpetuums" e tiers

Em vez de scripts one-shot, o sistema tem **agentes contínuos** (perpetuums) que correm
diariamente via cron e propõem melhorias.

### Autonomy tiers
- **T1 — Observer**: detecta sinal, escreve no log/vault. **Não toca em nada**.
- **T2 — Proposer**: escreve `action_hint` com critério verificável. Utilizador aprova.
- **T3 — Whitelisted executor**: executa só comandos numa whitelist (ex: `ii panorama X`).
- **T4 — Bounded autonomous**: cria PRs, escreve em vault auto. Não toca em `data/`.
- **T5 — Full**: reservado, não usado.

### Perpetuums activos (12)
`thesis`, `vault`, `data_coverage`, `bibliotheca`, `code_health`, `content_quality`,
`token_economy`, `methods`, `library`, `meta`, `ri_freshness`, `autoresearch`.

Cada um tem domínio próprio, sinais nomeados (`CH001`, `BIB003`, etc.), e cooldowns para
não spammar.

### Cron diário
Um ficheiro `daily_run.bat` (Windows Scheduled Task, 23:30 local) corre:
1. Fetchers (preços, fundamentals, FX).
2. Scoring engine.
3. Triggers monitor.
4. Perpetuum master (todos os 12).
5. Captain's log → push Telegram (~1160 chars, mobile-friendly).

Tudo offline-friendly: PC tem que estar acordado, mas não precisa de internet contínua.

---

## 6. Arquitectura "3-layer brain"

```
┌──────────────────────────────────────────────────────────────┐
│  L3 — Vault humano (Obsidian)                                │
│       wiki, notas, decision log, Constitution                │
│       fonte de verdade qualitativa                           │
├──────────────────────────────────────────────────────────────┤
│  L2 — Vault auto-gerado (markdown via scripts)               │
│       holdings/, sectors/, timelines/, dossiers/             │
│       regenerável a partir de L1                             │
├──────────────────────────────────────────────────────────────┤
│  L1 — SQLite (data/{br,us}_investments.db)                   │
│       fundamentals, prices, scores, events, paper_trades     │
│       fonte de verdade quantitativa                          │
└──────────────────────────────────────────────────────────────┘
```

- **L1** é o ground truth numérico. Tudo o resto deriva.
- **L2** é cache renderizado para humanos (Obsidian) e RAG (chunks indexados).
- **L3** é o que o utilizador escreve à mão — teses, contraméricas, decisões.

A regra: **L1 nunca é editado à mão**. L2 nunca é editado à mão (regenera). L3 é sagrado.

---

## 7. Quando Claude API entra (e quando não)

### Entra quando…
- Síntese exige julgamento multi-domínio (macro + sector + ticker + memória do utilizador).
- O utilizador inicia uma conversa exploratória ("o que achas de X?").
- Tarefa é one-shot rara e o setup local custaria mais que o token.
- Code review / refactor que beneficia de raciocínio sobre intent.

### **Não** entra quando…
- Pipeline batch (qualquer coisa que corra >1× ou em loop).
- Extracção/parsing estruturado (regex, BeautifulSoup, ou Ollama dão conta).
- Síntese de relatório curto (Ollama Qwen 14B é suficiente).
- Cron jobs (custo recorrente proibitivo).

**Rule of thumb**: se a tarefa cabe num prompt de 2k tokens e o output é estruturado,
**Ollama**. Se exige contexto >10k tokens **+ julgamento**, **Claude**.

---

## 8. Padrões de coding (autonomia segura)

Adoptados dos [Karpathy guidelines](https://github.com/forrestchang/andrej-karpathy-skills),
porque sessões autónomas sem utilizador a corrigir queimam tokens em loops:

1. **Think before coding** — declarar assumptions explicitamente; se algo é unclear,
   parar e nomear o que confunde em vez de inventar.
2. **Simplicity first** — mínimo código que resolve. Antes de adicionar abstracção, perguntar:
   "passa review de senior engineer?"
3. **Surgical changes** — tocar só no que o pedido exige. Cleanup separado → commit separado.
4. **Goal-driven execution** — transformar pedidos vagos em critérios verificáveis *upfront*.
   Critério de done numa linha **antes** de codar.

Operacionalizado via:
- `simplify` skill (review changed code).
- `code_health` perpetuum (linter contra anti-patterns CH001-CH007).
- 1 commit por preocupação (não commit-monstro).

---

## 9. Métricas que importam acompanhar

- **Token usage Claude/dia** — meta: tendência decrescente.
- **Tavily quota usado/1000** — meta: <30% em rotina, ramp em deep research.
- **Ollama calls/dia** — sobe → bom (significa trabalho a sair de Claude).
- **Cron success rate** — meta >95%.
- **Memory entries staleness** — `memory_cleanup --fix` mensal.
- **Coverage**: `% holdings com thesis populated`, `% universe com conviction score`,
  `% sectors com wiki`. Meta: 100% nas três.

---

## 10. Stack visual rápido (TL;DR)

```
┌─────────────────────── INTERFACE ───────────────────────┐
│  CLI (`ii ...`)  │  Streamlit  │  Obsidian  │  Telegram │
└──────────────────┴─────────────┴────────────┴───────────┘
            │            │            │            │
            ▼            ▼            ▼            ▼
┌────────────────── ORQUESTRAÇÃO ─────────────────────────┐
│   Scripts Python · Perpetuums · Cron (Scheduled Task)   │
└─────────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────── COMPUTE ────────────────────────────┐
│   Ollama (Qwen 14B + nomic-embed) · SQLite · Whisper    │
└─────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────── EXTERNAL (rate-limited, cached) ─────────────┐
│   yfinance · brapi · CVM · SEC EDGAR · Tavily · YouTube │
└─────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────── ESCALATION (manual) ─────────────────────┐
│         Claude API — só para o que exige julgamento     │
└─────────────────────────────────────────────────────────┘
```

---

## Resumo em 3 frases

1. **Local-first absoluto**: Ollama + SQLite + cron resolvem 90%+; Claude só para o resto.
2. **Memória em ficheiros**: o assistente persiste regras, contexto e correcções entre sessões,
   nunca recomeça do zero.
3. **Autonomia em tiers**: agentes contínuos propõem (T1-T2), nunca executam destrutivo sem
   aprovação; tudo idempotente e reversível.

---

*Sistema pessoal, não comercial. Para um investidor pessoa física a operar B3 + NYSE/NASDAQ
em estratégia DRIP de longo prazo.*
