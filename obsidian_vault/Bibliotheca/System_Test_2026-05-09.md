---
title: System Test 2026-05-09 — bateria 5 fases
date: 2026-05-09
type: system_test
trigger: pós-calibration noturna 2026-05-09; user: "testar a fundo o sistema"
related: [[Extension_Run_2026-05-09]], [[Postmortem_2026-05-09_synthetic_ic]]
---

# System Test 2026-05-09

Bateria de 5 fases, exercendo cada camada do sistema com a baseline calibrada hoje cedo.
Foco: **encontrar disagreements e gaps**, não validar.

---

## Phase 1 — Data freshness baseline

| Check | Resultado |
|---|---|
| US fundamentals/prices/scores | ✅ latest 2026-05-08 |
| BR fundamentals/prices/scores | ✅ latest 2026-05-08 |
| 103 IC dossiers do calibration | ✅ touched 12:15→12:18 |
| `us/prices/yfinance` | 90% (1 fail "No module named 'yfinance'") |
| `us/analyst/fmp` | 100% |
| **BR `strategy_runs` table** | ❌ **NÃO EXISTE** (US tem 112 rows com `run_ts`) |
| BR `events` latest | ⚠️ 2026-05-01 (8 dias stale — CVM monitor não rodou esta semana) |

**Action item P1**: investigar porque CVM monitor parou. Criar tabela `strategy_runs` no BR DB (ou usar mesmo schema US) — evita silent persistence loss.

---

## Phase 2 — 5-ticker cross-validation matrix

5 tickers escolhidos para spannar o universo: dividend king US, banco US, REIT US, holding BR, FII pós-merger BR.

| Ticker | Gra | Buf | DRIP | Macro | Hedge | IC | Variant | Moat | Quality |
|---|---|---|---|---|---|---|---|---|---|
| **JNJ** | – | H 0.67 | **B 0.80** | H 0.67 | H 1.00 | HOLD | mid_var | **8.75 STRONG** | Altman 4.3, Pio 4/9 |
| **JPM** | – | **A 0.40** | H 1.00 | H 0.67 | H 1.00 | HOLD | low_cons | n/a (bank) | **None / None** ❌ |
| **O** | – | **B 0.86** | H 0.75 | H 0.67 | H 1.00 | **AVOID** | unmeas | n/a (REIT) | None / None |
| **ITSA4** | B 1.00 | – | **A 0.55** | H 0.67 | H 1.00 | BUY | low_cons | n/a (Holding) | Altman 6.9, Pio 5/9 |
| **KNHF11** | H 0.80 | – | **A 0.25** | H 0.67 | H 1.00 | HOLD | – | n/a (FII) | DivSafety 25 |

### Disagreements reais (3 com material divergence)

1. **JPM | Buffett-engine AVOID 0.40 vs DRIP HOLD 1.00 vs IC HOLD vs FairValue BUY**
   Root cause: Auditor schema não tem campos para bancos (Altman/Piotroski/Moat = None). Buffett engine genérico aplica P/E≤20 + ROE≥15% sem o overlay novo de US Banks (P/TBV≤1.8, ROTCE≥15%, CET1≥11%). FairValue calcula por TBV+EPS direto e dá BUY firme — esse é o canal correcto para bancos.
   **Conclusão**: Trust FairValue, descartar Buffett engine output em bancos.

2. **O | Buffett BUY 0.86 vs IC AVOID**
   Buffett screen passa O fácilmente (REIT, dividend monthly aristocrat). IC AVOID provavelmente puxado por Klarman/Taleb (preocupação com tail risk de cuts ou refinancing em high-rate regime). DivSafety 75 confirma sólido. **Tensão entre métrica fundamental e narrativa qualitativa.** IC tem razão para flagar mas screening tem razão para passar.

3. **ITSA4 | Graham BUY 1.00 + IC BUY vs DRIP AVOID 0.55 / **KNHF11 / BBDC4 / KNCR11 / MCCI11 mesmo padrão**
   Padrão sistemático em BR: DRIP engine penaliza holdings + bancos + FIIs com track record curto. Não é bug local de 1 ticker, é estrutural. **Investigar `strategies/drip.py` — DY threshold ou trajetória pode estar mal calibrada para BR (Selic alta = bond-like yields ≠ DRIP US 2.5% floor).**

---

## Phase 3 — Allocate proposals

### US (top 15) — universo 28, candidatos 14

```
ACN     10.4%   | AAPL  9.4%  | MSFT  9.4%  | TSM  9.4%  | IBM   7.7%
TTD      7.5%   | GREK  7.2%  | O     6.5%  | PLTR 6.4%  | MCD   6.0%
HD       5.9%   | JNJ   5.9%  | PLD   5.5%  | PG    2.8%
```

**Drift vs portfolio actual** (NAV US $22.8k):

| Ticker | Atual | Atual % | Target % | Drift $ |
|---|---|---|---|---|
| ACN | $777 | 3.4% | 10.4% | **−$1,598** |
| AAPL | $1,467 | 6.4% | 9.4% | −$680 |
| MSFT | $0 | 0% | 9.4% | **−$2,146** |
| TSM | $2,058 | 9.0% | 9.4% | −$88 ✓ |
| IBM | $0 | 0% | 7.7% | −$1,758 |
| TTD | $0 | 0% | 7.5% | −$1,712 |
| MCD | $0 | 0% | 6.0% | −$1,370 |
| HD | $317 | 1.4% | 5.9% | −$1,030 |
| **JNJ** | $2,213 | 9.7% | 5.9% | **+$866 (overweight)** |
| **PG** | $1,464 | 6.4% | 2.8% | **+$825 (overweight)** |

**8 conflicts** (engines disagree). Pattern dominante: Buffett AVOID em AAPL/IBM/MSFT/PLD (P/E acima do threshold 20 — criteria-correct mas filtra megacaps modernas que o próprio Buffett detém).

### BR (top 15) — universo 47, candidatos 23, regime expansion (low confidence)

```
POMO3   9.6%  | PLPL3  9.0%  | TTEN3  8.7%  | MULT3  8.6%  | ALOS3 7.6%
SUZB3   7.6%  | MOTV3  6.5%  | PETR4  5.9%  | POMO4  5.9%  | BBDC4 5.5%
ITSA4   5.4%  | RECR11 5.0%  | KNCR11 4.9%  | PGMN3  4.9%  | RBRY11 4.8%
```

**Critical observation**: Apenas 2/15 dos targets allocate (BBDC4, ITSA4) estão na carteira BR actual. As outras 10 holdings (LFTB11, VALE3, PRIO3, KLBN11, BTLG11, KNHF11, VGIR11, XPML11, PVBI11, IVVB11) **não aparecem** no top-15. Allocate recomendaria reshuffle quase total. **NÃO accionar wholesale.** Use como pool de candidatos para deploy de cash, não como sell-list.

**16 conflicts BR** (dobro do US). Pattern: Graham BUY vs DRIP AVOID em todo holdings/bancos/FIIs — confirma o gap estrutural identificado em Phase 2.

### Bug fix shipped durante Phase 3

`strategies/drip.py:40,42` — `(snap or {}).get("fundamentals", {}).get(...)` falhava com NoneType quando `fundamentals` existia mas valor era None. Corrigido para `((snap or {}).get("fundamentals") or {}).get(...)`. Sem isso, BR allocate crashava antes de produzir output.

---

## Phase 4 — Portfolio stress test

NAV total implícito ~$87k (US $22.8k + BR R$355k ≈ $58k @ 6.10). HHI 825 = bem diversificado.

| Stress scenario | DD% | Loss $ |
|---|---|---|
| 2008 GFC | −53.7% | −$46,904 |
| 2020 COVID | −42.1% | −$36,798 |
| BR Selic 15% | −23.5% | −$20,499 |
| 2022 Bear | −13.9% | −$12,160 |

**Tilts contraditórios detectados**:
- `GROWTH_TILT` (weighted P/E > 25) — puxado por PLTR / TSM / AAPL / TTD-target / MSFT-target
- `INCOME_TILT` (DY > 5%) — puxado por LFTB11 / VGIR11 / KNCR11 / ITSA4 / O

Estes dois tilts em simultâneo significam **portfolio bimodal** — não é Buffett-Graham puro nem income-DRIP puro. Está em tensão com a filosofia declarada em CLAUDE.md.

Top single-position concentration: LFTB11 22% (Tesouro Selic ETF — cash-equivalent, OK).

---

## Phase 5 — Respostas às 3 perguntas pendentes

### P1: PG / JNJ / KO bands

| | PG | JNJ | KO |
|---|---|---|---|
| Current | $146.42 | $221.32 | $78.42 |
| our_fair | $54.86 | $82.21 | $19.18 |
| sell_above | $76.93 | $115.29 | $26.90 |
| **action** | **SELL** | **SELL** | **SELL** |
| upside | −62.5% | −62.9% | −75.5% |
| Tangible BV | **−$12B** | **−$17B** | +$4B |
| Intangible % assets | 50.8% | 49.8% | 26.7% |
| inputs_json warning | ✓ | ✓ | – |

**SINAL FALSO em PG e JNJ**. `inputs_json` literalmente diz:
> `"intangible_warning": "high_intangibles_brand_off_balance — Buffett ceiling on BVPS unreliable for this name"`.

A fórmula Graham ceiling = √(22.5 × EPS × BVPS) assume BVPS reflecte valor económico. Para marcas (PG soap brands, JNJ Listerine/Tylenol, KO formula) o brand value está **off-balance-sheet** — BVPS é deceptivamente baixo (PG/JNJ até negativo em tangible terms). Resultado: o motor recomenda vender exactamente as empresas que Buffett detém na vida real. KO é o caso canónico — Buffett owns desde 1988 com cost basis ~$3.

**Recommendação prática**:
- PG/JNJ/KO ações dentro dos planos: **manter, não accionar SELL**
- KO: tangible BV positivo (+$4B) mas ainda overstated; sinal SELL menos errado mas warning deveria estar lá também
- Bug a fixar: motor `scoring/fair_value.py` precisa downgrade de `confidence` ou de `action=HOLD` quando `intangible_warning` presente. Hoje o warning está em inputs_json mas a action ignora.

### P2: JPM deep dive

```
Auditor    | Piotroski: -/9 (-)   Altman: - (-)   Moat: -/10 (N/A bank)
Scout      | yfinance consensus: 0 analysts (FMP free-tier rate-limit)
FairValue  | our_fair $306.26   sell_above $451.53   action BUY @ $302.10
            | TBV $277.9B (real backing), intangible 1.5% — Buffett ceiling VÁLIDO
Strategist | qwen2.5:32b dossier 432 palavras
```

**Resolução do disagreement Phase 2**:
Buffett-engine genérico → AVOID 0.40 (porque Altman/Piotroski None). É falso negativo. Os critérios novos US Banks (P/E ≤ 12, P/TBV ≤ 1.8, ROTCE ≥ 15%, CET1 ≥ 11%, dividend streak pós-2009 ≥ 10y) **ainda não estão wired no engine genérico** — só existem em `scoring/engine.py::score_us_bank` e em texto no CLAUDE.md. FairValue é o único canal correcto para bancos hoje.

JPM hoje:
- Price $302.10 vs our_fair $306.26 → margin 22% até $451 ceiling
- Action BUY com `confidence_label: cross_validated`
- Posição actual: 7 shares = $2,114.70 (9.3% NAV US, vs target allocate "não-listada" — JPM nem aparece no top-15 do allocate, evidência de outro gap entre engines)

**Recommendação**: JPM razão para adicionar é forte (FairValue BUY + recente push pós-stress regulatório + TBV crescimento). Mas Buffett-engine + allocate disagree por razões metodológicas (gap, não fundamentals). O canal a confiar para decisão é FairValue + verdict aggregator, não allocate.

### P3: Onde investir agora

**Caveats antes de qualquer trade**:
- Cash idle disponível? Não declarado nesta sessão — [memory: BR/US isoladas, R$ fica em BR account, USD em US].
- Action items metodológicos pendentes (DRIP BR engine, US Banks no Buffett genérico, fair_value intangible_warning gate) **inflectam** o ranking — não tomar decisões definitivas baseado só em allocate output até esses três bugs serem fixados.

**Picks defensáveis com data actual** (US):
- **JPM** — FairValue BUY firme, fundamentals sólidos, TBV growing, intangíveis baixos. Único nome onde o sistema é confiável para banks hoje.
- **ACN** — top do allocate (10.4%), atualmente 3.4% (drift −$1,598). Tech-services, dividend grower. Buffett-engine concorda, sem flag de high-intangible.
- **TSM** — 9.0% atual ≈ 9.4% target, no point. Não trim, não add.

**Picks com cuidado** (US):
- **AAPL/MSFT/IBM** — Buffett AVOID por P/E mecânico. Allocate gosta. Sem moat score (Moat só corre para "STRONG" 8+ em determinados sectors). Decidir com peer comparison + DCF, não allocate puro.
- **PG/JNJ overweight** — system diz SELL mas razão é o bug do intangible warning. Se houver outras razões para trim (concentration, reallocation), sim; mas não baseado em fair_value.

**BR** — recommendação geral: **não rebalance**. Reshuffle indicado pelo allocate é artefacto do engine não creditar holdings. KNHF11 (post-merger) ainda está em fase track-record-builder, dar 6-12m para DRIP engine ter dividends suficientes para julgar. ITSA4/BBDC4 — manter, ignorar DRIP AVOID até bug ser fixado.

**Top action list pós-test**:
1. Fix `scoring/fair_value.py` — gate intangible_warning → action=HOLD ou downgrade confidence
2. Fix `strategies/drip.py` — calibration BR DY threshold (Selic alta vs US 2.5% floor)
3. Wire US Banks new criteria (P/TBV / ROTCE / CET1) no engine genérico ou no allocate combiner
4. Investigar `monitors/cvm_monitor.py` — eventos BR 8d stale
5. Criar tabela `strategy_runs` no BR DB para overnight allocate persistir
6. Considerar trim AAPL/PG/JNJ overweight **só** se rebalance disciplinado, não baseado em sinal SELL falso

---

## Conclusão do system test

**Veredicto sobre o sistema**:
- Pipeline ponta-a-ponta funciona. Smoke test JNJ verde em 3 camadas (synthetic_ic / variant / deepdive).
- 103 dossiers IC do calibration estão fresh, todos os engines correm sem fatal errors após 1 fix em drip.py.
- **Mas**: 3 disagreements estruturais expõem fragilidade nos engines em **bancos / high-intangible names / BR holdings+FIIs**. Sistema não é confiável para decisões binárias nestes 3 buckets sem cross-validation manual.
- **Saída de "testes reais"**: ferramentas estão prontas para o user **investigar**. Não estão prontas para auto-acionar trades sem human review nos 3 buckets identificados.

**Bugs shipped esta sessão**:
1. `strategies/drip.py:40,42` — NoneType .get() crash em BR allocate (1-line fix, deployed)

**Bugs identificados, pendentes**:
1. `scoring/fair_value.py` — intangible_warning não gateia action
2. US Banks criteria não wired no Buffett engine genérico
3. DRIP engine BR — DY floor não calibrado para Selic alta
4. CVM monitor BR — events 8d stale
5. BR DB sem tabela strategy_runs

---

*System test executado em ~25 minutos | 5/5 phases completed | nenhuma trade accionada (system test, não actionable run)*
