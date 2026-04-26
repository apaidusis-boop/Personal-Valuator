---
type: strategic_doc
tags: [library, books, options, paper_trade, strategy]
date: 2026-04-24
---

# 📚 Library + Options Calls — honest strategy

> User pediu: "se eu salvar livros de investimentos e métodos avançados, achas que seríamos capazes de criar calls (Put/Call curtos) como 5% em período curto?"
>
> Resposta: **parcialmente sim, mas com staged trust**. Esta nota é o plano honesto — o que construí hoje, o que precisaria de mais, o que **nunca** deveríamos fazer sem backtest rigoroso.

---

## ✅ O que JÁ temos (shipped hoje)

| Componente | Purpose |
|---|---|
| `library/__init__.py` | estrutura: books/, methods/, chunks/ |
| `library/ingest.py` | PDF/EPUB/MD → chunks 2000 chars + metadata |
| `library/methods/*.yaml` | 2 seeds: Graham Defensive, Dalio All Weather |
| `library/matcher.py` | aplica rules YAML a fundamentals dos holdings |
| `library/paper_trade.py` | `paper_trade_signals` table — signal log SEM capital |
| `agents/perpetuum/library_signals.py` | perpetuum diário que corre matcher |

**Pipeline completo funcional**: user adiciona PDF → ingest → extrai chunks → matcher aplica método → se pass → log signal paper → perpetuum tracks.

---

## ⚠️ Onde tem que fazer paper-trade ANTES de real capital

### Value investing (Graham, Buffett) — SIM, seguro de expandir
- Horizon longo (3-5 anos)
- Critérios já parcialmente no CLAUDE.md
- Backtest possível com data histórica que temos
- **Risco**: low. Mesmo se método errar, perdas graduais, não catastróficas
- **Action**: **pode fazer já** — expand methods YAML + matcher enriquece variáveis

### Macro investing (Dalio) — SIM mas com paper-trade de 6 meses
- Horizon medium (3-12 meses)
- Baseia-se em regime classification — nós já temos `analytics/regime.py`
- **Risco**: médio. Regime misclassified → wrong tilt, mas tilts são pequenos
- **Action**: paper trade os tilts por 6 meses; medir hit rate; só depois aplicar ao portfolio real

### Options / directional short-term calls — **NÃO AINDA**. Honestamente.

Você perguntou: _"Put da Ação tal para ganhar 5% em período mais curto"_. Aqui está a verdade honesta:

| Por que NÃO já | Razão |
|---|---|
| **Expected value negativo** para plays directionais baseados em signals untested. 5% em período curto = vol play, não value play |
| **Nós não temos data de options**: vol surface, IV percentile, DTE structure, open interest — nada. Sem isto, options pricing é chute |
| **Short-term moves são quase random** para ticker individual. Edge vem de volatility read, não de fundamentals |
| **Um único bad call wipes profits** de 10 good calls. Asymmetry do lado errado |
| **O CLAUDE.md + MEMORY.md** são optimizados para **DRIP + long-term compounding**. Directional short-term é direcção diferente — precisaria philosophy change, não só método adicionado |

### O caminho responsável (staged)

```
NOW (2026-04) → paper-trade signals of Graham/Dalio methods
                 log hit rate + avg return per method (library.paper_trade.performance_by_method)

+3 months    → if ≥30 closed signals per method, statistical significance possible
                 measure: win rate, avg return, worst drawdown, Sharpe-like ratio

+6 months    → if methods prove positive expected value, scale to small real allocation
                 max 2% portfolio per signal, hard stops

+12 months   → consider options overlays ONLY for methods with IC > 0.05 (statistically meaningful)
                 start with covered calls on existing holdings (sell premium, not buy)
                 never buy puts/calls speculatively without vol data infrastructure

NEVER        → blind "Put XYZ for 5% gain" based solely on book heuristics
                 these are effectively lottery tickets with narrative attached
```

---

## 📋 Para avançar, adicione os PDFs abaixo em `library/books/`:

Estes são os livros que maximizam o valor do pipeline actual:

**Core (high fit com CLAUDE.md philosophy)**:
- ✅ Graham, _The Intelligent Investor_ (4th/5th ed)
- ✅ Graham & Dodd, _Security Analysis_
- ✅ Buffett, _The Essays of Warren Buffett_
- ✅ Dalio, _Principles for Navigating Big Debt Crises_
- ✅ Dalio, _The Changing World Order_

**Augment methodology**:
- Klarman, _Margin of Safety_ — risk framework
- Marks, _The Most Important Thing_ — cycle awareness
- Greenwald, _Value Investing from Graham to Buffett_ — modern take
- Asness et al., _Quality Minus Junk_ (paper) — factor validation

**Do NOT need** (tempting mas low-fit):
- Any options/derivatives textbook until after 12m paper-trade track record
- Technical analysis books (philosophy conflicts com DRIP+value)
- Crypto/trading system books (different mental model)

---

## 🔧 Próximos passos técnicos (para methods funcionarem melhor)

Actualmente os matcher rules falham porque faltam algumas variables. Para eles realmente gerarem signals, precisamos:

1. **Enriquecer `fundamentals` schema**:
   - `market_cap_usd` (computed via price × shares_outstanding)
   - `current_ratio` (from financials)
   - `ltd` (long-term debt) + `working_capital`
   - `positive_earnings_years_10` (aggregate de 40 quarters)
   - `eps_3y_avg_growth_10y` (window calc)

2. **Scripts de backfill**:
   - `scripts/enrich_fundamentals_for_methods.py` — popula as colunas acima dos dados já existentes

3. **Resolver expressions mais ricas no matcher**:
   - actualmente `_safe_eval_check` faz eval restrito. Pode ser ampliado para aceitar funções simples (min, max, abs)

Sem estes, `library_signals` perpetuum vai sempre scorear 0 (rules falham por missing vars). Depois disto, scores meaningful.

---

## 📊 Quando saberemos se funciona

Após 90 dias:
```sql
SELECT method_id,
       COUNT(*) as total,
       SUM(CASE WHEN status='closed_win' THEN 1 ELSE 0 END) as wins,
       AVG(realized_return_pct) as avg_return
FROM paper_trade_signals
WHERE status LIKE 'closed%'
GROUP BY method_id
HAVING total >= 20;
```

Se **win_rate > 60% AND avg_return > 0** para um método → vale considerar real capital.
Se **win_rate ~50%** → method é aleatório, não use.
Se **win_rate > 70% mas avg_return negativo** → wins pequenos, losses grandes (worst case).

**Critical**: número mínimo de closed signals para significance. 20 é o floor. 50+ é confortável.

---

## 🛡️ Risk-management hardcoded no paper_trade

Mesmo paper, o schema força:
- `expected_move_pct` explicit por signal
- `horizon` explícito (não pode ser "indefinite")
- `thesis` obrigatório — por que este método disparou
- `status` transições auditáveis

Isto é disciplina **antes** de haver capital envolvido. Quando houver, a disciplina já está inbuilt.

---

## Links

- [[_MOC]] — Gold index
- [[Phase_X_Perpetuum_Engine]] — engine arquitectural
- `library/` — book ingest + methods + matcher
- `library/methods/graham_defensive.yaml` — seed 1
- `library/methods/dalio_all_weather_tilt.yaml` — seed 2
