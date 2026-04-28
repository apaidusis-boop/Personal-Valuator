---
type: playbook
name: Verdict Engine — BUY/HOLD/SELL/AVOID aggregator
tags: [playbook, verdict, decision_engine]
related: ["[[Buy_checklist]]", "[[Sell_triggers]]", "[[Critical_Thinking_Stack]]", "[[Token_discipline]]"]
---

# Verdict Engine — agregador de decisão por ticker

> Motor que destila quality + valuation + momentum + narrativa em **uma acção** (`AVOID|SELL|HOLD|WATCH|ADD|BUY`) por ticker. Substitui o vai-e-vem entre `screen`, `altman`, `piotroski`, `safety`, `triggers` — single source of truth para decisão. Acoplado a `verdict_history` para backtest forward-only (Phase R).

## Princípio

**Score composto, vetos absolutos, persistência forward-only.** Nenhuma das 4 dimensões manda sozinha — o engine pondera e aplica vetos de distress (Altman/Piotroski). História é gravada **antes** de saber se a decisão foi boa: backtest mede accuracy real, não fitada.

## Arquitectura (quem chama quem)

```
ii verdict <TK>                       ii vh record (cron 23:30)
        ↓                                       ↓
scripts/verdict.py                  scripts/verdict_history.py
   compute_verdict(ticker)              record_all(holdings)
        ↓                                       ↓
        └── scripts/research.py::evaluate(tk, mkt)
                ├── scoring/engine.py        → screen_score
                ├── scoring/altman.py        → Altman Z
                ├── scoring/piotroski.py     → Piotroski F
                ├── scoring/dividend_safety  → safety 0-100
                └── prices table             → 1d/30d/YTD momentum
        ↓
   Verdict dataclass  → render_markdown() → vault note (--write)
                      → synthesize_narrative() (Qwen 14B, --narrate)
                      → INSERT verdict_history (vh record)
```

`scripts/panorama.py` consome o verdict como bloco principal do super-command.

## Pesos e dimensões

`compute_verdict()` em `scripts/verdict.py` produz um `Verdict` dataclass (ver Schemas) com 4 dimensões 0-10 ponderadas:

| Dimensão | Peso | Inputs |
|---|---:|---|
| **Quality** | 35% | Altman Z + Piotroski F + Dividend Safety (média simples) |
| **Valuation** | 30% | Screen score (BR/US engine) × 10 + DY-percentile adjustment ±2 |
| **Momentum** | 20% | Média de 1d / 30d / YTD price-change pontuados em tiers |
| **Narrativa** | 15% | User note + YT insights ≤60d (base 4.0 + bumps) |

Total `= Q*0.35 + V*0.30 + M*0.20 + N*0.15`.

### Quality (peso 35%)
- **Altman pts**: Z≥3.0 → 10; Z≥1.81 → 5; Z<1.81 → 0; N/A → 5 neutral
- **Piotroski pts**: F≥7 → 10; F≥5 → 6; F≥3 → 3; F<3 → 0; N/A → 5
- **Safety pts**: 80+ → 10; 60+ → 6; 40+ → 3; <40 → 0; None → 5

### Valuation (peso 30%)
- `screen_pts = screen_score × 10` (screen vem de `scoring.engine` aplicando critérios BR / US / Banks BR / Banks US)
- Adjustment DY-percentile: P75+ → +2 (CHEAP histórico); P25- → −2 (EXPENSIVE)
- Clamp `[0, 10]`

### Momentum (peso 20%)
Tiers em `_MOMENTUM_TIERS = [(3.0, 8.0), (0.0, 6.0), (-3.0, 4.0), (-10.0, 2.0)]` para 1d/30d e tiers próprios YTD `[(10.0, 8.0), (0.0, 6.0), (-10.0, 4.0), (-25.0, 2.0)]`. Score = média dos 3.

### Narrativa (peso 15%)
Base 4.0 + 3.0 se `notes_cli` tem nota não-vazia para o ticker + 3.0 se ≥3 `video_insights` em 60d (1.5 se 1-2). Tags da nota são propagadas mas não somam.

## Acção — vetos e thresholds

A acção final **não é só** total score. Vetos passam à frente:

```python
if altman_applicable and Z < 1.81:                  → AVOID (distress veto)
elif piotroski_applicable and F ≤ 3:                → AVOID (quality veto)
elif is_holding and total < 4:                      → SELL  (holding deteriorou)
elif total ≥ 7.5:                                   → BUY (não-holding) | ADD (holding)
elif total ≥ 6.0 and valuation_score ≥ 7:           → WATCH (barato mas qualidade fraca)
else:                                               → HOLD (holding) | SKIP (não-holding)
```

Confidence heurístico (`confidence_pct`, base 50, capped 95): +10 por dimensão Altman/Piotroski aplicável, +10 se ≥3 YT insights, +10 se user_note, +10 se total nos extremos (<2 ou >8).

> ❓ verify — thresholds **6.0 + valuation≥7 → WATCH** e o limite **total<4 → SELL** estão hard-coded no `verdict.py`; não há config externo. Se mudarem critérios BR/US no `scoring/engine.py`, o screen_score muda mas estes cortes ficam fixos.

## Modos de output

### Markdown (default)
`render_markdown(v)` produz secção `## 🎯 Verdict — <icon> <ACTION>` com:
- Score total + confidence + timestamp
- Tabela 4 linhas (Quality/Valuation/Momentum/Narrativa) com bar visual `█████░░░░░`
- Detalhes inline (Altman Z, Piotroski F, DivSafety, screen, DY pctl, 1d/30d/YTD)
- Lista de razões (geradas heuristicamente das dimensões)

Ícones: BUY/ADD 🟢, WATCH 🟡, HOLD 🟠, SELL 🔴, AVOID ⛔, SKIP ⚪.

### `--narrate` (Qwen 14B local)
Liga `synthesize_narrative(v)` que faz POST a `http://localhost:11434/api/chat` com modelo `qwen2.5:14b-instruct-q4_K_M`, `temperature=0.2`, `num_ctx=4096`. Gera 2-3 frases PT explicando o verdict. **System prompt impõe**: Buffett-Graham persona, NÃO inventar dados, foco na lógica de decisão. Se Ollama down → retorna `_(Qwen indisponível: <err>)_` (graceful).

### `--write` (vault inject)
Chama `write_into_vault(v, md)` que:
1. Lê `obsidian_vault/tickers/<TICKER>.md` (FileNotFoundError se vault não está populado → correr `ii obsidian --refresh` primeiro)
2. Preserva frontmatter
3. Remove bloco `## 🎯 Verdict ...` anterior (regex DOTALL, count=1)
4. Insere o novo bloco logo abaixo do frontmatter

Idempotente — re-run substitui in-place.

### `--json`
`json.dumps(asdict(v))` raw. Para consumo programático (panorama, agents, dashboards Streamlit).

## Histórico + Backtest (Phase R)

`verdict_history` é uma tabela espelhada nas 2 DBs. Snapshot diário tipicamente disparado pelo cron 23:30 via `ii vh record`.

### Schema `verdict_history` (idêntica BR + US)

| Coluna | Tipo | Notas |
|---|---|---|
| ticker | TEXT | PK1 |
| date | TEXT | PK2, ISO `YYYY-MM-DD` |
| action | TEXT | AVOID/SELL/HOLD/WATCH/ADD/BUY/SKIP |
| total_score | REAL | 0-10 |
| confidence_pct | INTEGER | 50-95 |
| quality_score / valuation_score / momentum_score / narrative_score | REAL | dimensões |
| price_at_verdict | REAL | snapshot do `momentum_detail.price_latest` |
| recorded_at | TEXT | UTC ISO timestamp |

PK `(ticker, date)` → idempotente; `INSERT` segundo no mesmo dia retorna `already_recorded_today`.

### `record_all()` (default = só holdings)
Itera `portfolio_positions WHERE active=1` em ambas as DBs e chama `record_verdict()` por ticker. `--all` extende a `companies` (universe completo, lento ~2-3min/100 tickers).

### `backtest()`
Itera linhas gravadas, para cada `(ticker, date, action)` calcula `forward_return(price_at_verdict → price em date+30d, +90d, +180d)`. Bucketiza por action e devolve `n / mean / median / win_rate / min / max` por janela. Útil só **depois** de existirem ≥30 dias de history (caso contrário todas as janelas vêm `None`).

### `show_history(ticker)`
Lista cronologia decrescente: data, action, scores, price. Permite ver verdict drift (ex: HOLD → WATCH → BUY conforme valuation comprime).

## Comandos

| Caso | Comando |
|---|---|
| Verdict só (stdout markdown) | `ii verdict ACN` |
| + narrativa Qwen local | `ii verdict ACN --narrate` |
| Inject no vault note | `ii verdict ACN --write` |
| JSON puro | `ii verdict ACN --json` |
| Batch holdings | `ii verdict --all-holdings --write` |
| Snapshot diário (cron) | `ii vh record` |
| Snapshot universe inteiro | `ii vh record --all` |
| Backtest accuracy | `ii vh backtest` |
| Histórico de 1 ticker | `ii vh show ACN` |

`ii panorama ACN` consome `scripts/verdict.py` internamente como primeira secção.

## Schemas

### `Verdict` dataclass (`scripts/verdict.py`)
```
ticker, market, action, total_score, confidence_pct,
quality_score, valuation_score, momentum_score, narrative_score,
quality_detail{altman_z, altman_zone, altman_pts, piotroski_f, piotroski_label, piotroski_pts, div_safety, safety_pts},
valuation_detail{screen_score, screen_pts, dy_percentile, dy_label, dy_adjustment},
momentum_detail{score, change_1d_pct, change_30d_pct, change_ytd_pct, price_latest, price_date},
narrative_detail{score, user_note, tags, yt_insights_60d, reasons},
reasons[], generated_at
```

## Economia de tokens

| Operação | Custo |
|---|---|
| `ii verdict <TK>` (sem `--narrate`) | **0 tokens Claude** — pure SQL + Python |
| `ii verdict <TK> --narrate` | **0 tokens Claude** — Qwen local, ~3-8s |
| `ii vh record` (33 holdings) | **0 tokens Claude** — ~30-60s wall-clock |
| `ii vh backtest` | **0 tokens Claude** — agregação SQL |
| `panorama` (consome verdict) | **0 tokens** — script `subprocess.call` |

Cumpre [[Token_discipline]] (REGRA #1). Claude **só** entra se o user pedir interpretação narrativa de um verdict que não cabe em 2-3 frases Qwen.

## Limitações conhecidas

- **N/A neutral inflation**: tickers sem Altman/Piotroski aplicáveis (FIIs, ETFs) recebem 5/10 nas duas pontas → quality_score sobe artificialmente. ETFs e bancos cuja screen é específica costumam ficar HOLD por default em vez de WATCH/SKIP.
- **Verdict drift**: thresholds (`7.5`, `6.0`, `< 4`) são fixos no código; mudanças aos critérios em `CLAUDE.md` (BR/US/Banks) só afectam o screen_pts indirectamente. Ajustar manualmente quando os critérios de mercado mudam (ex: era Selic alta vs cycle de cortes).
- **Recency bias na narrativa**: `yt_insights_60d` cap de 60 dias significa que um ticker com 1 vídeo viral mês passado pontua igual ao com 5 vídeos sólidos há 90d. Não há decay temporal dentro da janela.
- **Momentum dominado por YTD**: a média simples 1d/30d/YTD dá peso igual a noise (1d) e a tendência (YTD). Em mercados laterais o 1d swing vira ruído puro.
- **`--write` requer vault populado** — se `obsidian_vault/tickers/<TK>.md` não existe, abort. Correr `ii obsidian --refresh --holdings-only` antes.
- **Backtest precisa população**: `verdict_history` actualmente tem ~30 rows num único dia (2026-04-23). Backtest ainda devolve `None` para ≥30d até o cron diário acumular ~30 snapshots → wait period inerente à filosofia forward-only.
- **Confidence é heurístico**, não calibrado vs accuracy real. `confidence_pct=85` ≠ 85% acerto histórico — proxy de "quantos sinais convergem", não probabilidade.
- **Dimensões não-correlacionadas**: ticker pode ter quality 9 + momentum 1 + valuation 5 → total 5.5 = HOLD, mas o conflito entre dimensões é apagado no agregado. Ler sempre `reasons[]` antes de agir.
- **Bug histórico**: `is_holding` lookup vem de `evaluate()`; se `portfolio_positions` está stale, holding novo aparece como BUY em vez de ADD (semântica trocada mas acção idêntica).

## Workflow recomendado

1. **Decisão tactical (single ticker)**: `ii verdict <TK> --narrate` — markdown + Qwen prose, suficiente sem abrir Claude.
2. **Daily snapshot**: cron 23:30 corre `ii vh record` automaticamente; é forward-only, não retro-actuável.
3. **Mensal**: `ii vh backtest` para ver win-rate por action; se BUY tiver win-rate <50% em 90d, recalibrar thresholds.
4. **Pré-rebalance**: `ii verdict --all-holdings --write` injecta verdicts actualizados em todos os ticker notes; depois abrir Obsidian para cross-ref com [[Buy_checklist]] / [[Sell_triggers]].
5. **Antes de pedir Claude para "analisa esse ticker"**: correr `ii verdict --json` e injectar o output — Claude não precisa re-derivar (ver [[Token_discipline]]).

## Ver também
- [[Buy_checklist]] — confirmação manual antes de agir num BUY/ADD
- [[Sell_triggers]] — vetos de SELL fora do verdict (price_drop, thesis_break)
- [[Critical_Thinking_Stack]] — synthetic_ic / variant_perception complementam quando o verdict é HOLD ambíguo
- [[Token_discipline]] — porque `--narrate` é Qwen e não Claude
