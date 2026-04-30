---
type: playbook
name: Critical Thinking Stack (Phase AA)
tags: [playbook, critical_thinking, synthetic_ic, variant, ollama]
related: ["[[Token_discipline]]", "[[Perpetuum_Engine]]", "[[Tavily_Integration]]", "[[Agents_layer]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 🧠 Critical Thinking Stack — anti-groupthink layer

> 5 módulos shipped juntos em **Phase AA** (2026-04-25). Cada um ataca um vector específico de groupthink/bias na nossa análise. **100% Ollama local (Qwen 14B); zero tokens Claude no pipeline.** Cumpre [[Token_discipline]] (REGRA #1).

## Porquê este stack existe

A Constitution tinha 1 open issue persistente: **theses auto-populadas via Ollama overnight** (Phase G/J) tendem a ser monolíticas — refletem o framework que escreveu, não múltiplos ângulos. Sem contra-pressão, o sistema *acredita em si próprio*.

O stack ataca isso em 5 frentes complementares:

| Frente | Módulo | Pergunta que responde |
|---|---|---|
| 🏛️ **Multi-framework** | `synthetic_ic` | "5 lendas com frameworks diferentes concordam ou divergem nesta tese?" |
| 🎯 **Crowd-vs-us** | `variant_perception` | "Onde a nossa tese DIVERGE do consenso analyst (e quem tem razão)?" |
| 🧠 **Auto-crítica** | `decision_journal_intel` | "Que padrões de erro repetimos? Que actions ignoramos sempre?" |
| 📞 **Pré-evento** | `library/earnings_prep` | "Que perguntas/métricas devo procurar em earnings amanhã?" |
| 💥 **Cenário extremo** | `portfolio_stress` | "Que perdemos se 2008/COVID/2022 repetir hoje?" |

> **Anti-padrão que isto previne**: fazer uma única chamada Ollama, receber output coerente, aceitar como verdade. Múltiplos prompts com frameworks contraditórios + dados crowd + histórico de decisões = vetos cruzados.

## Princípios de design partilhados

1. **Ollama local Qwen 14B** (`qwen2.5:14b-instruct-q4_K_M`) é o modelo único — todos os módulos chamam via `agents._llm.ollama_call` ou `ollama_call_typed` (Pydantic schemas).
2. **Tavily quando há gap** — variant_perception, earnings_prep e synthetic_ic têm wires Tavily mas com **gating** (só chama quando DB é insuficiente). Cache 7d via `agents.autoresearch`.
3. **Output é vault markdown** com frontmatter — futuro Claude lê o `.md`, não re-corre o LLM.
4. **Skip resumability** — `--skip-existing` em batch para não regenerar trabalho.

---

## 🏛️ 1. Synthetic IC — debate multi-persona

`agents/synthetic_ic.py` — 5 personas com frameworks contrastantes debatem o ticker. Cada uma vota `BUY/HOLD/AVOID` + conviction + key_risk.

### As 5 personas

| Persona | Framework chave | O que vai *flagar primeiro* |
|---|---|---|
| **Buffett** | Quality + moat + simplicity, horizonte forever | Falta de moat, complexity, leverage cíclica |
| **Druckenmiller** | Macro liquidity + concentration + asymmetric bets | Liquidity regime errado, no asymmetric upside |
| **Taleb** | Tail risk + barbell + anti-fragility | Hidden leverage, fragility, opacidade, optimism |
| **Klarman** | Margin of safety ≥30% + cash patience | Sem desconto sobre intrínseco, leverage interno |
| **Dalio** | Big debt cycles + diversification + regime | Ciclo dívida tóxico, single-country concentration |

> **Função de cada uma**: ser o veto cruzado. Se 5/5 dizem BUY → consensus. Se Taleb sozinho diz AVOID, a tese pode estar a ignorar tail risk (foi exactamente o caso VALE3 — ver findings AA.2).

### Context que recebe (build_context)

- `fundamentals` latest (PE/PB/DY/ROE/ND-EBITDA/mcap/current_ratio/beta)
- `quarterly_single` últimos 6 trimestres (revenue/ebit/margem/debt/fcf)
- `thesis_health` latest (score, contradições, risk_flags, regime_shift)
- `vault_thesis` via `agents._common.read_vault_thesis` (lê tanto `## Thesis` legacy como `## N. Thesis` em `<TK>_DOSSIE.md`)
- **Tavily news 14d** (`_tavily_recent_news`, 1 call serve as 5 personas — não multiplica)

### Comandos

```bash
# Single ticker
python -m agents.synthetic_ic ITSA4

# Single ticker com majority voting (3 seeds, fixa flips ~85%)
python -m agents.synthetic_ic ITSA4 --majority 3

# Todo o portfolio activo
python -m agents.synthetic_ic --all-holdings

# Watchlist (companies is_holding=0)
python -m agents.synthetic_ic --watchlist

# Holdings + watchlist (universe-wide)
python -m agents.synthetic_ic --all --skip-existing --limit 50
```

### `--majority N` (default 1)

Cada persona corre N vezes com seeds diferentes (`[42, 137, 314, 271, 1729]`); verdict por maioria; conviction = mean dos winners. **N=3 é sweet-spot** (3× custo, fixa ~85% dos flips entre runs). Custo: 5 personas × N runs ≈ 15 chamadas Ollama / ticker no N=3 (~3-5 min).

### Synthesizer (consensus calculation)

- ≥80% mesma verdict → `high confidence`
- 60-79% → `medium confidence`
- <60% → `MIXED` (`low confidence`)

### Output

`obsidian_vault/tickers/<TICKER>_IC_DEBATE.md` — frontmatter `type: synthetic_ic_debate`, committee_verdict, consensus_pct, votes, cada persona com emoji + rationale + key_risk + context provided.

---

## 🎯 2. Variant Perception — we vs consensus

`agents/variant_perception.py` — onde divergimos do crowd; *edge identification = where you disagree, with evidence*.

### Pipeline

1. **Stance interno**: classifica `## Thesis` do vault como `bullish/bearish/neutral` via keyword matching (BULLISH_HINTS / BEARISH_HINTS) — **só** sobre Core thesis + Intent (não Disconfirmation triggers, que listam keywords bearish por design).
2. **Stance analyst (DB)**: `analyst_insights` últimos 90d, agregados `bull/bear/neutral` + `weighted_consensus` (source weighting via `predictions` win-rate, fallback 0.5).
3. **Stance web (Tavily)**: `_tavily_consensus` — quando DB tem `<3` insights, faz 1 Tavily call (`topic="downgrade"`, 30d), classifica hits via `_TAVILY_BULL` / `_TAVILY_BEAR` keyword lists. Cache 7d.
4. **Variance matrix** (3×3 = 9 cells) — converte par `(thesis_stance, consensus)` em label + magnitude 0-5:
   - `HIGH_VARIANCE_LONG` (we bull, market bear, mag 5) → "we see something market misses (or wrong)"
   - `HIGH_VARIANCE_SHORT` (we bear, market bull, mag 5) → "contrarian sell"
   - `low_consensus_long` / `low_consensus_short` (mag 1) → "no edge"
   - etc.
5. **Specific divergence** (LLM, só se mag ≥2): pede ao Ollama 3 frases identificando o ponto contestado.

### Bug history — substring → word-boundary (Phase FIX, 2026-04-25)

> 🚨 **Bug crítico fixed**: classifier antigo usava `if hint in text` — `"trim"` matchava `"patrimonial"`, `"risk"` matchava `"asterisko"`. **4 falsos HIGH variance** (IVVB11/RBRX11/VGIR11/VALE3) confundiram análise. **Fix**: word-boundary regex `\b" + re.escape(word) + r"\b`. **Resultado**: HIGH variance falsos 4 → 0. ❓ verify se a regra anti-Disconfirmation-Triggers continua a aplicar a todas as theses recentes.

### Open issue exposto pelo módulo

- **Theses auto-populadas overnight via Ollama (Phase G/J) podem ter bias sistémico**. VALE3 foi confirmado como genuíno (CVM single-Q margin compression -10pp YoY). **IVVB11/RBRX11/VGIR11**: provavelmente artefacto da pop overnight, precisa review humana. Documentado como Constitution open issue.

### Comandos

```bash
# Single ticker
python -m agents.variant_perception ACN

# Single ticker — writes vault by default (não há flag --write)
python -m agents.variant_perception ACN

# Todo o portfolio
python -m agents.variant_perception --all-holdings

# A/B legacy mode (uniform consensus, sem source weighting)
python -m agents.variant_perception --all-holdings --no-weighting
```

### Output

`obsidian_vault/tickers/<TICKER>_VARIANT.md` — frontmatter `type: variant_perception`, variance label + magnitude, weighted vs raw consensus, weight_skew flag, Tavily web consensus block (com hits classificados), source weights table.

---

## 🧠 3. Decision Journal Intelligence — pattern mining

`agents/decision_journal_intel.py` — varre histórico interno e detecta 5 padrões P1-P5. **Pure SQL + filesystem; zero LLM, zero rede.**

### Sources mined

- `watchlist_actions` (resolved/ignored history) — quais propostas foram aceites
- `paper_trade_signals` com `closed_*` outcomes — win/loss
- `thesis_health` trajectory — quem teve decay
- `perpetuum_health` flags — quem é mais flagado
- `obsidian_vault/tickers/<X>.md` — notas humanas

### Os 5 padrões

| # | Padrão | Pergunta |
|---|---|---|
| **P1** | Auto-ignored kinds | Que tipos de action ignoramos sempre? (high ignore rate por kind) |
| **P2** | Action latency | Quanto demoramos a actuar nas que aceitamos? |
| **P3** | Thesis decay → outcome | Tickers com decay maior tiveram pior performance? |
| **P4** | Dominant ticker concerns | Quais tickers aparecem mais em flags? |
| **P5** | Sector concentration in flags | Que sector concentra mais alarmes? |

### Insights actionable auto-derivados

- Se um `kind` tem ≥70% ignore rate e n≥3 → "considera silenciar este perpetuum ou ajustar threshold"
- Se ticker top-1 tem >5 flags → "re-avaliar position size ou exit"
- Se sector top-1 tem >10 flags → "concentration risk a observar"

### Auto-crítica embutida

> "Decision journal só fica útil após 30+ days de operação com action resolutions. Paper signals win-rate só significant após 30+ closed signals/method. Pattern detection é honesto sobre amostra pequena."

### Comando

```bash
python -m agents.decision_journal_intel
```

### Output

`obsidian_vault/briefings/decision_journal_intel_<DATE>.md` — frontmatter `type: decision_journal_intelligence`, 5 secções (uma por pattern) + insights actionable + auto-crítica.

---

## 📞 4. Earnings Prep — pre-call brief automático

`library/earnings_prep.py` — para cada `earnings_calendar` event nos próximos N dias, gera memo Ollama-grounded.

### Context fed to LLM (build_context)

- `fundamentals` latest (PE/PB/DY/ROE/ND-EBITDA/mcap/cur_ratio)
- `quarterly_single` últimos 6 quarters (rev/ebit/margem/ni/fcf)
- `thesis_health` latest (score + contradictions + risk_flags)
- `analyst_insights` últimos 60d (stance + claim)
- `vault_thesis` (`## Thesis` extraído)
- **Tavily 2 calls/event**:
  - `topic="guidance"` 60d → expectations
  - `topic="earnings"` 90d → last quarter notes
  - Cache 7d → re-runs no mesmo event = 0 calls

### LLM prompt (PREP_PROMPT)

Pede markdown estruturado em PT:
- 🔥 **Top 3 things to watch** (com número-alvo)
- ❓ **5 specific questions** to listen for management
- 📊 **Trajectory check** (confirmar trend Y / reverter Z)
- 🚨 **Red flags potenciais**
- 🎯 **Decision framework** BUY MORE / HOLD / TRIM com condições quantitativas

### Comandos

```bash
# Próximos N dias (todos earnings em earnings_calendar)
python -m library.earnings_prep --upcoming 30

# Single ticker (data manual ou hoje)
python -m library.earnings_prep --ticker AAPL --date 2026-05-30

# Confirmado 2026-04-28: argparse só tem --upcoming N + --ticker/--date/--market.
# Não existe --days. CLAUDE.md actualizado.
```

### Output

`obsidian_vault/briefings/earnings_prep_<TICKER>_<DATE>.md` — frontmatter `type: earnings_prep_brief`, brief markdown gerado + context provided to LLM (debug). Auto-stamp "X days before call".

### Smoke (Phase AA findings)

11 briefs gerados em ~1min para próximos 30d (VALE3, KO, AAPL, BRK-B, PRIO3, PLTR, O, BN, NU, HD, XP).

---

## 💥 5. Portfolio Stress — concentration + factor + drawdown

`analytics/portfolio_stress.py` — 3 sub-reports independentes, cada um aborda uma fragilidade.

### Sub-reports

#### A. `concentration` — onde estás concentrado

- **HHI** (Herfindahl-Hirschman) em basis-points; interpretação: <1500 well-diversified, 1500-2500 moderate, 2500-4000 concentrated, >4000 highly
- Top-3 / Top-5 / Top-10 % do portfolio
- Largest single position
- Sector breakdown
- Market split (BR vs US %, USD-normalized via FX rough ~5.5)

#### B. `factor` — que tilts implícitos tens

- Weighted-by-MV: PE / PB / DY / ROE / Beta levered
- Tilts auto-detected: `VALUE_TILT` (PE<12) / `GROWTH_TILT` (PE>25) / `INCOME_TILT` (DY>5%) / `DEFENSIVE` (β<0.8) / `AGGRESSIVE` (β>1.2)
- Size buckets: large (>$50B) / mid ($5-50B) / small (<$5B) / unknown

#### C. `drawdown` — guerra histórica re-jogada

Aplica 4 cenários a tua mix BR/US actual:

| Scenario | SPX dd | IBOV dd | Duration | Recovery |
|---|---:|---:|---:|---:|
| **2008_GFC** | -50% | -55% | 18m | 24m |
| **2020_COVID** | -34% | -45% | 1m | 4m |
| **2022_Bear** | -25% | -10% | 9m | 12m |
| **BR_Selic_15pct** | -5% | -30% | 6m | 18m |

Computa portfolio DD como `br_pct × ibov_dd + us_pct × spx_dd` + USD loss estimado.

### Caveats honestos (escritos no próprio output)

- Modelo simples: aplica só market drawdown × peso geográfico
- Não inclui beta individual nem sector covariance
- Recovery times são médias históricas — outliers podem ser muito piores
- FII liquidity risk não modelado (gates possíveis)

### Comandos

```bash
python -m analytics.portfolio_stress concentration   # só concentration
python -m analytics.portfolio_stress factor          # só factor
python -m analytics.portfolio_stress drawdown        # só drawdown war-game
python -m analytics.portfolio_stress all             # todos os 3

# Confirmado 2026-04-28: kind é argumento POSICIONAL ∈ {concentration, factor, drawdown, all}.
# Não há flag --shock. CLAUDE.md actualizado.
```

### Output

`obsidian_vault/briefings/portfolio_<KIND>_<DATE>.md` — frontmatter `type: portfolio_<concentration|factor_exposure|drawdown_wargame>`.

### Phase AA smoke findings (2026-04-25)

- **HHI 828** overall (well-diversified) **mas LFTB11 sozinho = 21.8%** (Tesouro Selic ETF — defensive cash sleeve)
- Top-5 = 52% do portfolio
- Tilts simultâneos `GROWTH + INCOME + DEFENSIVE` (US tech + BR div + defensives) — perfil dual
- 2008 repeat estimado: portfolio -53.7% / -$47k (recovery 24m hist)

---

## Token economics — zero Claude

| Operação | Custo |
|---|---|
| Synthetic IC 1 ticker, default | 5 calls Ollama qwen 14b (~30s) |
| Synthetic IC 1 ticker, `--majority 3` | 15 calls Ollama (~2-3 min) |
| Synthetic IC universe (--all) | ~150-180 tickers × 5 calls (~2-3h overnight) |
| Variant Perception 1 ticker | 1 LLM call (só se mag≥2) + 0-1 Tavily call (cached 7d) |
| Variant Perception --all-holdings | ≤30 LLM calls + ≤10 Tavily |
| Decision Journal Intel | **0 LLM, 0 rede** (pure SQL) |
| Earnings Prep 1 brief | 1 Ollama + 2 Tavily (cached 7d) |
| Earnings Prep --upcoming 30 (full month) | ~10-15 events × (1 Ollama + 2 Tavily) |
| Portfolio Stress (any/all) | **0 LLM, 0 rede** (pure SQL + math) |

**Total Claude tokens consumidos pelo pipeline: 0.** Tudo Ollama local + Tavily cached.

## Open issues do stack (de memory + Constitution)

1. **Bias em theses auto-populated overnight** — variant_perception expôs falsos HIGH variance em IVVB11/RBRX11/VGIR11. Hipótese: Ollama overnight escreve theses muito bullish (default-long bias do classifier também ajuda). **Acção**: review humana das theses auto-draft + considerar prompt anti-bias na próxima reroda.
2. **Decision journal precisa runway** — só fica útil após 30+ days de operação. Não tirar conclusões antes.
3. **Paper signals win-rate** — só significant após **30+ closed signals/method** (regra do user em `library_and_paper_trade.md`). Antes disso, decision_journal_intel.P3 é placebo.
4. ❓ **CLAUDE.md script catalog desalinhado em 2 pontos**:
   - `portfolio_stress --shock pe_compress|recession` (não existe; argparse usa positional `kind`)
   - `earnings_prep --days 60` (argparse só tem `--upcoming N`)
5. **Tavily quota** — Dodo Key dev tier 1000/dia. Stack consome ≤10/dia em uso normal; spike só se rodar `synthetic_ic --all` + `earnings_prep --upcoming 30` no mesmo dia.

## Workflow recomendado (cadência)

| Quando | Comando |
|---|---|
| **Diário** (cron 23:30 wired em `daily_run.bat`) | nada deste stack ainda — todos manual / weekly |
| **Semanal** (Sunday review) | `python -m agents.decision_journal_intel` + `python -m analytics.portfolio_stress all` |
| **Antes de earnings** (auto, 7d before) | `python -m library.earnings_prep --upcoming 30` |
| **Quando dúvida em ticker** | `python -m agents.synthetic_ic <TK> --majority 3` |
| **Após nova compra** | `python -m agents.variant_perception <TK>` (sanity check vs crowd) |
| **Mensal** (full sweep) | `python -m agents.synthetic_ic --all --skip-existing --limit 50` |

## Ver também

- [[Token_discipline]] — porque 100% Ollama local
- [[Perpetuum_Engine]] — engine que pode promover synthetic_ic / variant a perpetuum diário (T2+) quando tiver runway suficiente
- [[Tavily_Integration]] — wires usados por 3 destes módulos (cache + rate-limit + gating)
- [[Agents_layer]] — framework `agents/` que hosting estes módulos
- `obsidian_vault/CONSTITUTION.md` — open issue "bias em theses auto-populated"
- `reports/_phases/PHASE_AA_REPORT.md` — design rationale + smoke findings originais
- `reports/_phases/PHASE_FIX_REPORT.md` — bug history variant_perception (substring → word-boundary)
