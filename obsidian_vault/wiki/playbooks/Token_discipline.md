---
type: playbook
name: Token Discipline — In-house First
priority: 1
tags: [playbook, meta_rule, tokens, inhouse]
related: ["[[Buy_checklist]]", "[[Sell_triggers]]", "[[Rebalance_cadence]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 🚨 REGRA #1 — In-house First, Tokens Last

> **TUDO QUE PODE SER RODADO INTERNAMENTE FAREMOS INHOUSE.**

Meta-regra do projeto. Claude/tokens são **último recurso**, não primeiro.

## Por que existe

Projeto tem infra local madura:
- **SQLite** BR+US (preços, fundamentals, scores, events, triggers, dividends).
- **Ollama Qwen 14B** (vault_ask, yt_reextract, research sumarização).
- **60+ scripts** Python (fetchers, scoring, reports, DRIP projection).
- **Obsidian + Dataview** (queries cross-note, dashboards live).

Cada vez que Claude faz trabalho que um destes faria = **desperdício de tokens**.

## Decision tree — antes de responder qualquer pergunta

```
Pergunta chega
   │
   ├─ É dado estruturado (posições, preços, fundamentals, divs)?
   │  └─ SQL ou script → 0 tokens
   │
   ├─ É análise qualitativa sobre ticker/vault?
   │  └─ `ii vault "pergunta"` (Ollama Qwen 14B) → 0 tokens
   │
   ├─ É deep-dive de ticker (memo/verdict/peers)?
   │  └─ `ii verdict X --narrate --write` → 0 tokens
   │
   ├─ É transcript/análise de vídeo YouTube?
   │  └─ `yt_digest.py` (SQL-only) OU `yt_reextract.py` (Ollama) → 0 tokens
   │
   ├─ É daily briefing / diff / briefing matinal?
   │  └─ `ii brief` ou `morning_briefing.py` → 0 tokens
   │
   ├─ É fetch de dado externo?
   │  └─ `fetchers/` (brapi, yfinance, SEC, FRED) — NÃO usar WebFetch
   │
   └─ Escalar para Claude (tokens) APENAS se:
       - Síntese cross-fonte genuína (3+ outputs combinados com insight novo)
       - Código novo (script/função que ainda não existe)
       - Debug de bug específico (logs + stack trace)
       - Decisão estratégica com múltiplos tradeoffs
       - Conteúdo narrativo realmente novo (wiki notes, teses)
```

## Script catalog — consultar ANTES de trabalhar

Ver `CLAUDE.md` secção "Script catalog". Resumo prático por caso de uso:

| Pergunta | Comando existente | Tokens |
|---|---|---|
| "Quantas ações de X?" | `sqlite3` query | 0 |
| "Passa no screen?" | `python scoring/engine.py X` | 0 |
| "Deep-dive completo" | `ii verdict X --narrate --write` | 0 |
| "Compara A vs B vs C" | `compare_tickers.py A B C` | 0 |
| "O que falei sobre X?" | `ii vault "o que disse sobre X"` | 0 |
| "Qual o digest do canal Y?" | `yt_digest.py --channel Y --days 30` | 0 |
| "Panorama matinal" | `ii brief` | 0 |
| "Payback DRIP" | `drip_projection.py --ticker X --payback` | 0 |
| "Rebalance drift" | `ii rebalance` | 0 |
| "Kelly size" | `ii size X --cash N` | 0 |
| "Comparar vs SPY/IBOV" | `compare_ibov.py X` | 0 |

## Guardrails de execução

- **Bash `run_in_background` sem Monitor** — pipelines longos em silent mode. Monitor só para debug. Silent ~10× mais barato.
- **Extensão por flag, não script novo** — se existe script próximo, adicionar flag/modo.
- **`--write` / `--md`** — scripts que suportam export de markdown devem escrever em vault e deixar user ler em Obsidian, em vez de pushar texto para o chat.
- **Nunca reproduzir tabelas** já em CLAUDE.md / memórias / wiki. Remete para fonte.

## Anti-padrões (sempre evitar)

- ❌ "Deixa-me pesquisar os dividendos de X" → use `ii verdict` / SQL.
- ❌ Re-fetch preço em chat quando `refresh_ticker.py` existe.
- ❌ Ler 20 ticker notes para "sentir" carteira → `vault_ask` ou `portfolio_report`.
- ❌ Escrever comparativa à mão → `compare_tickers.py`.
- ❌ WebFetch de dado que temos fetcher.
- ❌ Claude reproduzindo output de script que acabou de correr.

## Quando Claude É apropriado

- Wiki notes novas (sem equivalente computável).
- Debug: "porquê este script falha" (requer raciocínio sobre código + logs).
- Síntese: "olhando 3 scripts acima, qual tese emerge?".
- Strategy: "entre estas 2 alternativas, qual recomendas?".
- Pergunta conversacional sobre decisões passadas que precisa contextualização.

## Reforço de padrões já estabelecidos

Esta regra não inventa — **codifica** práticas já em memória:
- [[Silent batch mode]] — run_in_background default
- [[YouTube pipeline]] — Ollama extract, 0 tokens
- [[Obsidian AI plugins]] — Qwen Ollama primary LLM

É a **meta-regra** — governa todas as outras.

## Aplicação pessoal (user-facing)

Quando pedires panorama sobre ação X:
- **Default esperado**: `ii verdict X --narrate --write` → abre `tickers/X.md` no Obsidian.
- **Não esperes que Claude leia 10 ficheiros para te responder** — é sinal de que script não cobre o caso (oportunidade de estender).

Se respondes e sentes que estás a "fazer trabalho manual repetitivo" → **criar script / comando `ii`** que automatize.

---

> Source memory: `feedback_inhouse_first.md` (2026-04-24).
