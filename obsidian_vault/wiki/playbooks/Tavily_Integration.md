---
type: playbook
name: Tavily web research integration
tags: [playbook, tavily, web_research, autoresearch]
related: ["[[Token_discipline]]", "[[Perpetuum_Engine]]", "[[Agents_layer]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# Tavily Integration — web research em duas camadas

> Ponte para o mundo exterior do projecto. Tavily é a primeira fonte de dados *vivos* (web actual) que integramos sem queimar tokens Claude no caminho automatico. Phase K (cliente + perpetuum) + Phase K.2 (3 wires) + Phase K.3 (8 skills oficiais + CLI) cobrem o desenho actual.

## Princípio — duas camadas, dois budgets

| Camada | Quem invoca | Custo Claude | Custo Tavily | Quando |
|---|---|---|---|---|
| **L1 — Autoresearch** (in-house) | cron `daily_run.bat` + perpetuums + 3 wires Python | **0** tokens | quota Tavily (cache 7d + rate-limit local) | 24/7 silencioso |
| **L2 — Skills oficiais** | eu (Claude Code) via slash `/tavily-*` ou `tvly` CLI | sim, paga ao consumir resultado | quota Tavily (mesma key) | on-demand quando user pede deep-dive |

**Regra de uso**: tudo que é **recorrente/cron-friendly** entra em L1; tudo que é **one-shot/exploratório** vai por L2. Se uma query L2 começa a repetir-se, promover para L1 (criar perpetuum ou wire).

## Layer 1 — Autoresearch (zero Claude tokens)

### Core client — `agents/autoresearch.py`

Cliente Tavily python custom. Responsabilidades:

| Componente | Detalhe |
|---|---|
| **API endpoint** | `https://api.tavily.com/search` (POST, `requests` library) |
| **Cache** | sha1(`query|search_depth|topic`) → `data/tavily_cache/<key>.json`. **TTL 7d**. Hit ratio esperado 30-50% |
| **Rate-limit local** | `data/tavily_cache/_ratelimit.json` — **100 calls/dia**, **50 calls/hora** burst. Persiste contador entre runs |
| **Fallback gracioso** | Se key missing, daily_limit excedido, ou Tavily down → devolve `TavilyResult(error=..., results=[])`. **Nunca levanta excepção** que interrompa perpetuum downstream |
| **Result shape** | `TavilyResult(query, answer, results: list[TavilyHit], cached, error)`. `TavilyHit(title, url, content, score, published_date)` |

### `search_ticker(ticker, topic, market, days_back)` — convenience helper

Templates curados em `TICKER_TOPICS`:
- `earnings` — "{name} ({ticker}) earnings results last quarter beat miss guidance"
- `guidance` — "{name} ({ticker}) forward guidance fy26 outlook"
- `news` — "{name} ({ticker}) news"
- `regime` — "{name} ({ticker}) regulatory macro risk"
- `downgrade` — "{name} ({ticker}) analyst downgrade upgrade target"
- `scandal` — "{name} ({ticker}) fraud investigation scandal lawsuit"

**BUG FIX crítico (Phase K.2)** — `search_ticker` **auto-injecta company name**. Resolve via `_company_name(ticker, market)` que faz lookup em `companies` table e strip de sufixos (`S.A.`, `Inc`, `Corp`, `Ltd`, `Holdings`, ...). Sem isto, `ACN` retornava news genéricas trending; com isto retorna `Accenture (ACN) earnings ...` e o relevance score sobe ~5×. Para mercado BR adiciona sufixo `" B3 brazil"` para desambiguar.

### Autoresearch perpetuum — `agents/perpetuum/autoresearch.py`

11º perpetuum, **autonomy tier T1 (Observer)** — só alerta, não acciona.

```
[cron 23:30 daily_run.bat] → perpetuum_master → AutoresearchPerpetuum
  ↓
subjects(): top conviction holdings (composite_score >= 70, MAX 30/run)
  ↓
score(subject):
  1. Skip if last_query < 6 days ago (cooldown)
  2. search_ticker(ticker, topic="news", days_back=14)
  3. Para cada hit: filtra por score >= 0.5 + published <= 14d + coverage check
     (3+ keywords do título já no vault → considera coberto)
  4. score = 100 - 15 * len(novel_hits), floor 0
  5. Se novel >= 1 → action_hint "REVIEW autoresearch: N news não-cobertas — <titles>"
```

**Quota math**: 30 subjects/run × 1 run/dia × cooldown 6d ≈ ~5 calls efectivas/dia steady-state (cache absorve repetições). Bem abaixo do limit 100/dia.

### Os 3 wires (Phase K.2)

Tavily está integrada em 3 módulos production. Cada wire tem **gating** próprio para não queimar quota desnecessária.

#### Wire #1 — `agents/variant_perception.py::_tavily_consensus`

| | |
|---|---|
| Tópico | `downgrade` (template captura upgrades/downgrades/targets) |
| Window | 30d |
| Calls | 1 por ticker scan |
| **Gating** | Só dispara quando DB `analyst_insights` tem **n < 3** insights — preenche gap quando coverage local é fraca |
| Output | Conta bull/bear/neutral por keywords (`_TAVILY_BULL` / `_TAVILY_BEAR` lists) sobre title+content. Devolve `consensus` label que pode sobrepor o DB consensus se este for `no_data` |
| Vault | Secção "## Tavily web consensus (last 30d)" no `<TICKER>_VARIANT.md` |

#### Wire #2 — `library/earnings_prep.py::_tavily_pre_call_research`

| | |
|---|---|
| Tópicos | `guidance` (60d) + `earnings` (90d) — **2 calls por ticker** |
| **Gating** | Só corre 7d antes de earnings_date (já é o cadence natural do prep). Re-runs no mesmo evento → 0 calls (cache 7d) |
| Output | `guidance_answer` + `earnings_answer` (Tavily synth) + 3 hits cada → injectados no `context` que vai para Ollama Qwen 14B gerar o pre-call brief |
| Vault | Secção "WEB EARNINGS CONTEXT" + "WEB GUIDANCE CONTEXT" no `briefings/earnings_prep_<TICKER>_<DATE>.md` |

#### Wire #3 — `agents/synthetic_ic.py::_tavily_recent_news`

| | |
|---|---|
| Tópico | `news` |
| Window | 14d |
| Calls | **1 por ticker** — a mesma news lista alimenta as 5 personas (Buffett/Druck/Taleb/Klarman/Dalio). Não multiplica 5× |
| Gating | Sempre on (controlável por flag `use_tavily=True`) — assumimos que recent material news é input crítico mesmo quando há thesis health alta |
| Output | Lista de 4 hits (title + content snippet) appendada ao `context` que vai para cada persona prompt como secção "RECENT MATERIAL NEWS (last 14d via Tavily)" |
| Vault | `<TICKER>_IC_DEBATE.md` (a context block exibe os headlines) |

### Cache + rate-limit em prática

```
data/tavily_cache/
  _ratelimit.json        # {day, day_count, hour, hour_count, total, last_call}
  <sha1-16chars>.json    # 1 file por query (com _cached_at)
```

- **Cache hit** = 0 quota gasta (e 0 chamada HTTP).
- **Cache miss** + dentro de quota → bump rate-limit + POST + grava cache.
- **Cache miss** + over quota → devolve `error="rate_limit: ..."` sem chamar API.

### Quota state ilustrativo (snapshot 2026-04-28)

```json
{ "day": "2026-04-28", "day_count": 15, "hour_count": 15, "total": 162 }
```

163 cache files persistidos. **Nota**: snapshot ilustrativo, não autoritativo — quota Tavily mensal é gerida pela conta dev tier, ler `python -m agents.autoresearch stats` para estado actual.

## Layer 2 — Skills oficiais Tavily (consome Claude tokens)

Instaladas via `npx skills add tavily-ai/skills --all` em `C:/Users/paidu/investment-intelligence/.agents/skills/`. CLI binary `tvly` em `C:/Users/paidu/.local/bin/tvly.exe`. Mesma `TAVILY_API_KEY` é usada pelas duas camadas.

Slash commands disponíveis nesta sessão Claude Code:

| Skill | Slash | Em uma linha |
|---|---|---|
| `tavily-search` | `/tavily-search` | Web search optimizado para LLM (snippets + score), suporta domain filters / time ranges |
| `tavily-extract` | `/tavily-extract` | URL → markdown limpo (até 20 URLs/call, lida com JS-rendered pages) |
| `tavily-crawl` | `/tavily-crawl` | Bulk crawl de site/docs com depth/breadth control + path filters |
| `tavily-map` | `/tavily-map` | Discover URLs num domínio sem extrair conteúdo (rápido, content-free) |
| `tavily-research` | `/tavily-research` | Deep AI research multi-fonte com citations (30-120s, devolve report estruturado) |
| `tavily-best-practices` | `/tavily-best-practices` | Reference doc para construir integrações production-ready |
| `tavily-dynamic-search` | `/tavily-dynamic-search` | Search com context isolation — filtra resultados sem poluir context window |
| `tavily-cli` | `/tavily-cli` | Wrapper das capacidades acima usando o `tvly` binary |

**CLI binary** — `tvly` está no PATH do user (`~/.local/bin/`). Exemplos:

```bash
tvly search "Accenture FY26 guidance"
tvly extract https://example.com/article
tvly research "compare ITSA4 vs BBDC4 dividend safety"
```

## Comandos típicos

```bash
# === Layer 1 (zero Claude tokens) ===
python -m agents.autoresearch query "ITSA4 dividendos 2025"
python -m agents.autoresearch ticker AAPL --topic earnings
python -m agents.autoresearch stats              # cache + rate-limit state
python -m agents.autoresearch test               # smoke test live

# Perpetuum standalone
python -m agents.perpetuum_master --only autoresearch
python -m agents.perpetuum_master --only autoresearch --dry-run

# Trigger explícito dos wires
python -m agents.variant_perception ACN          # usa Tavily se DB n<3
python -m library.earnings_prep --upcoming 30    # Tavily 2× por evento
python -m agents.synthetic_ic ACN                # Tavily 1× recent news

# === Layer 2 (consome Claude tokens) ===
tvly search "Accenture earnings FY26"             # CLI direct
# /tavily-search "..."                             # slash skill
# /tavily-research "compare X vs Y"                # deep multi-source synth
```

## Quando L1 vs quando L2 — rule of thumb

| Sinal | Camada |
|---|---|
| "Já corre nightly, só quero o resultado" | **L1** (perpetuum/wire) |
| "Quero deep-dive numa empresa hoje, irrepetível" | **L2** (`/tavily-research`) |
| "Preciso 1 título de manchete recente para context" | **L1** (`search_ticker(news)`) |
| "User pediu 'pesquisa o que aconteceu hoje no mercado'" | **L2** (`/tavily-search`) |
| Query já cached <7d? | qualquer camada — cache hit é grátis |
| Vai ser repetido amanhã? Promover para L1 | criar perpetuum/wire |

## Histórico de bugs corrigidos

- **Phase K.2 — `search_ticker` retornava trending genérico**. Tickers como `ACN` sozinhos não são únicos no Tavily index → primeiro hit era random news. Fix: `_company_name(ticker, market)` injecta nome real (ACN→Accenture). Improvement de relevance ~5× em smoke tests.
- **`days` param do Tavily API** — payload usa `days` (não `days_back`); o nosso parâmetro python é `days_back` por clareza, traduzido no `payload["days"] = days_back`.

## Limitações conhecidas

- **Quota mensal Tavily dev tier** é finita (~1000/mês ordem de magnitude). Se 11 perpetuums começarem a fazer queries não-cooldown, pode esgotar. Cooldown 6d + cache 7d são as guard-rails actuais.
- **Stance keywords** em `_TAVILY_BULL/BEAR` (variant_perception) são heurísticas básicas — não distinguem ironia/sarcasmo. Confiável só com n>=3 hits.
- **Coverage check** no perpetuum (3 keywords match → considera coberto) tem falsos positivos quando o ticker note é longo. Aceitável: prefere falsos negativos (alertar quando talvez não preciso) ao inverso.
- **`published_date` parsing** — Tavily devolve formato RFC2822-ish; o parse no perpetuum tenta `%a, %d %b %Y %H:%M:%S` e falha silenciosa (mantém hit). Edge case.
- **`.env` `TAVILY_API_KEY`** confirmado presente (não revelado aqui). Se rotaccionada, perpetuums devolvem `error="no_api_key"` sem crashar.

## Ver também

- [[Token_discipline]] — porque L1 é cron-driven e nunca chama Claude
- [[Perpetuum_Engine]] — autoresearch é o 11º perpetuum, T1 Observer
- [[Agents_layer]] — pattern de agents/ que `autoresearch.py` segue
- [[Youtube_Pipeline]] — irmão de fonte externa (vídeo vs web)
- [[Web_scraping_subscriptions]] — outro vector externo (PDFs assinados)
