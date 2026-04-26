---
type: skill
tier: Gold
skill_name: autoresearch
source: karpathy/autoresearch
status: in_design
sprint: W.5
priority: critical
tags: [skill, gold, autoresearch, perpetuum, heart_of_gold]
---

# 🔬 autoresearch + Ad Perpetuum Validator — HEART OF GOLD

**Repos**:
- https://github.com/karpathy/autoresearch (research engine)
- https://github.com/assafelovic/gpt-researcher (alternativa production)

**Fit**: 🎯 **CRÍTICO** — este é o coração da Phase W Gold. Sem isto, não temos validação contínua; só temos snapshots.

## 🎯 A visão (quote do user)

> "Eu quero autoresearch para sempre fazer esse ad perpetuum validation para que possamos melhorar todos os dias"

Traduzido: não basta gerar research memo pontual. Quero um **loop que roda todos os dias** e questiona cada thesis da carteira contra evidência nova. Se uma thesis decai, eu quero saber ANTES de perder capital.

## 🏗️ Arquitectura — Ad Perpetuum Validator

### Nova tabela DB
```sql
-- data/br_investments.db + us_investments.db
CREATE TABLE thesis_health (
    ticker         TEXT NOT NULL,
    run_date       TEXT NOT NULL,  -- ISO YYYY-MM-DD
    thesis_score   INTEGER,        -- 0-100 (100 = thesis intact)
    new_evidence   INTEGER,        -- # novos data points desde última run
    contradictions INTEGER,        -- # sinais que contradizem thesis
    regime_shift   INTEGER,        -- 1 se macro regime mudou vs thesis origin
    devils_flags   INTEGER,        -- # flags do devils_advocate agent
    risk_flags     INTEGER,        -- # flags do risk_auditor
    details_json   TEXT,           -- full reasoning + evidence URLs
    PRIMARY KEY (ticker, run_date)
);

CREATE INDEX idx_thesis_health_date ON thesis_health(run_date);
CREATE INDEX idx_thesis_health_ticker ON thesis_health(ticker);
```

### Loop diário
```
[23:30 cron daily]
  ↓
agents/perpetuum_validator.py
  ↓
For each holding (BR + US):
  1. Pull thesis from obsidian_vault/tickers/<TICKER>.md (secção ## Thesis)
  2. Pull latest fundamentals (fundamentals table)
  3. Pull news from last 24h (fetchers/news_fetch.py + Tavily MCP)
  4. Pull analyst diffs (fetchers/subscriptions/ deltas)
  5. Pull macro regime (analytics/regime.py)
  6. Run autoresearch query: "Has <thesis> been contradicted by <new_evidence>?"
  7. Run agents/devils_advocate.py against thesis + new_evidence
  8. Run agents/risk_auditor.py against current state
  9. Compute thesis_score (composite — details below)
  10. INSERT into thesis_health
  11. If Δscore < -10 (daily drop) → Telegram alert + action in open_actions
  ↓
Weekly (Sunday):
  12. agents/meta_agent.py consolida semana
  13. Output: obsidian_vault/briefings/weekly_thesis_review_YYYY-WW.md
```

### thesis_score composite (0-100)
```python
score = 100
score -= contradictions * 5         # cada contradição tira 5 pts
score -= regime_shift * 15          # macro shift tira 15 pts
score -= devils_flags * 3           # cada devil's flag tira 3
score -= risk_flags * 4             # cada risk flag tira 4
score += min(new_evidence_pro, 10)  # confirmações dão até 10 pts
score = max(0, min(100, score))
```

Tiers interpretativos:
- **90-100**: Thesis intact, no action
- **70-89**: Minor erosion, watch
- **50-69**: Material drift, revisit thesis this week
- **30-49**: Thesis broken, rebalance or exit
- **0-29**: Capital preservation, exit now

## 🔄 Como isto nos faz melhorar TODOS OS DIAS

1. **Hoje**: thesis é manual, actualizada quando lembramos (mensalmente talvez).
2. **Com perpetuum**: thesis revalidada 24/7. Decay detectado no dia em que aparece, não no mês seguinte.
3. **Métricas crescem**: sabemos *quantitativamente* se tomamos melhores decisões:
   - Quantas thesis morreram? (contadores mensais)
   - Quanto capital salvamos por saída antecipada?
   - Qual é a latência média de detecção de regime shift?
   - Quantas contradições em média por thesis?

## Integração com skills vizinhas
- **[[SKL_tavily]]** — search engine para evidência nova
- **[[SKL_firecrawl]]** — scrape sites que Tavily não indexa
- **[[SKL_playwright_mcp]]** — Investidor10, Fundamentus data
- **[[SKL_mcp_harness_arsenal|Bigdata.com MCP]]** — structured data on-demand
- **[[SKL_observability_stack|LangFuse]]** — trace cada decisão do validator
- **[[SKL_pptx]]** — weekly review deck auto-gerado
- **[[SKL_canvas_design]]** — heatmap visual diário

## Sprint W.5 — entregáveis concretos

- [ ] Migration `scripts/migrate_thesis_health.py` — cria tabelas nas 2 DBs
- [ ] `agents/perpetuum_validator.py` — loop principal (~400 LOC)
- [ ] Integrar em cron 23:30 (já existente) — segundo stage após `daily_update`
- [ ] Dashboard widget: thesis health history line chart por ticker
- [ ] Telegram alert template: "⚠️ THESIS DECAY: TICKER dropped X points. Run `ii panorama TICKER`."
- [ ] Weekly report `agents/thesis_weekly_review.py` → markdown + PPTX

## Decisão: autoresearch (Karpathy) vs GPT Researcher

| Critério | autoresearch | GPT Researcher |
|---|---|---|
| Maturidade | Novo (Karpathy experimental) | Production-grade 2+ anos |
| Docs | Minimal | Extensivo |
| LLM-agnostic | Sim | Sim (via LangChain) |
| Performance | Leve (Karpathy style) | Heavier stack |
| Community | Alto buzz | Estabelecida |

**Recomendação**: usar **GPT Researcher como default** + **autoresearch como exploratory** em paralelo. A/B medir qual dá melhor thesis_score accuracy em 30 dias.

## Blockers
- Nenhum bloqueante técnico
- Precisa thesis explícita por ticker no vault (secção `## Thesis` em `tickers/<X>.md`). Hoje ~15 de 35 tickers têm. Sprint W.3 (obsidian) tem esta cleanup.

## Links
- [[Metrics]] — KPIs que medem o ganho deste sistema
- [[Roadmap]] — W.5 é o sprint
- [[../agents/_MOC|Agents framework]] — Phase V base que perpetuum expande
