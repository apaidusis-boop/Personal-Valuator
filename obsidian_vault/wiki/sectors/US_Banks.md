---
type: sector
name: US Banks
region: US
tags: [sector, banks, financials, us]
related: ["[[BR_Banks]]", "[[P_E_interpretation]]", "[[P_B_interpretation]]", "[[Fed_Funds_Rate]]", "[[Yield_Curve]]"]
holdings: ["[[JPM]]", "[[GS]]"]
---

# 🏦 Setor: Bancos US

> Pair com [[BR_Banks]]. Mesma família estrutural (alavancado, equity = colchão), mas a regulação, métricas e ciclo são distintos do lado de cá.

## Por que Bancos US precisam de scoring separado

A diferença vs uma empresa operacional é a mesma de BR (alavancagem natural, EBITDA não aplicável). A diferença vs **bancos BR** é mais subtil mas importante:

1. **Goodwill grande pós-aquisições** (Chase comprou WaMu 2008, BofA comprou Merrill 2008/Countrywide 2007). Por isso **P/TBV** (Tangible Book) é a referência, não P/B raw — sobrestima o capital real disponível para absorção de perdas.
2. **ROTCE substitui ROE** (Return on Tangible Common Equity) — a métrica que o sell-side US usa para comparar. JPM, GS, MS reportam ROTCE no slide 1 do earnings deck.
3. **CET1 ratio é o número regulatório** (Common Equity Tier 1, sob Basel III). Mínimo é 4.5% + buffers (capital conservation 2.5% + GSIB surcharge 1-3.5% para bulge bracket) = ~9-12% mandatório.
4. **Streak de dividendos é uma armadilha**. Quase todos os money-center cortaram em 2009 (JPM de $0.38 → $0.05/quarter; BAC de $0.32 → $0.01; WFC de $0.34 → $0.05). "Aristocrat" strict (25y consecutivos de aumento) é raro em bancos US — só BPOP, CINF, HBAN sobreviveram tipo. **A métrica honesta é "streak pós-2009"** (~16 anos hoje).

Por isso `scoring/engine.py::score_us_bank`:
- ❌ Graham Number (mesma razão que BR)
- ❌ Net Debt / EBITDA
- ❌ Aristocrat strict (excluiria toda a Big 4 US)
- ✅ P/E ≤ 12, P/TBV ≤ 1.8, ROTCE ≥ 15%, DY ≥ 2.5%, CET1 ≥ 11%, Efficiency ≤ 60%, streak pós-2009 ≥ 10y

## Taxonomia competitiva (2026)

| Tier | Nome | Foco | ROTCE típico |
|---|---|---|---|
| Money Center / GSIB | [[JPM]], BAC, C, WFC | universal banking, GSIB surcharge alta | 14-21% |
| Bulge Bracket IB | [[GS]], MS | trading + IB + wealth | 10-22% (volátil) |
| Super-Regional | USB, PNC, TFC | retail + SME, sem IB pesado | 12-15% |
| Regional | KEY, CFG, RF, FITB | depósito local, exposição CRE alta | 8-13% |
| Community | NTRS, BK | trust/custody, low-margin alto-volume | 10-14% |
| Card | COF, AXP, DFS | unsecured credit, ciclo de NPL próprio | 18-30% |
| Insurance/Diversified | BRK.B (não é banco mas float) | float + holdings | 10-15% |

JPM é a referência de "fortress balance sheet" (Dimon's term). GS é o IB cíclico dentro da carteira. Para 100% diversificação banca, precisaria adicionar mais 1-2 nomes (BAC ou USB seriam complementos óbvios).

## Drivers de resultado

### 1. Yield curve shape (mais importante)
- **Curve steep** (10y - 2y >100bps) → NIM expands → bank earnings boom (1992-94, 2003-06, 2010-14, 2025-?).
- **Curve flat / inverted** → NIM compress → bancos sofrem (2018-19, 2022-24).
- O **2026 setup**: Fed cut cycle iniciado, curve voltou positivo em 2025. Janela favorável para bancos.

### 2. [[Fed_Funds_Rate]] cycle
- Hike cycle inicial (rates ↑ rapidamente, deposit beta lento) → **NII boom** (2022-Q1 2023).
- Hike cycle late (deposit beta catches up) → NII flat/declining (2023 H2 → 2024).
- Cut cycle inicial → **deposit beta cai mais rápido que asset yields** → margem expand (early 2025).
- Esta dinâmica é a alma do trade "buy banks late in cycle".

### 3. Credit cycle (CRE em foco 2026)
- Office vacancy elevada (post-COVID, ~20% major MSAs) → **CRE write-downs** continuam.
- Bancos regionais com >25% loan book em CRE são os vulneráveis (NYCB 2024 wake-up call).
- **JPM/BAC** são <8% CRE — relativamente imunes.
- **Card delinquencies** já em ciclo alto (2025 peak provavelmente) — COF, DFS reportam.

### 4. Regulação
- Basel III "Endgame" (proposed 2023, water-down em 2024) — capital requirements +9% inicialmente, agora ~3-5% após pushback.
- **GSIB surcharge** (1.0-3.5%): JPM tem 4.5%, BAC 3.0%, C 3.0%, GS 3.0%, MS 3.0%, WFC 1.5%. Custo extra de capital = ROE drag estrutural.
- **CCAR / Stress Tests** — Fed obriga resilience. Banco que falha não pode subir dividendo.

### 5. Buyback discipline
- Buybacks dominam payout em US banks (vs dividendos pesados em BR). Total payout (div + buyback) ~80-100% lucro em ciclo bom.
- **Watch**: bancos a recomprar acima de TBV alto (>2x) destroem valor. JPM ~$200/share era OK; >$300 não tanto.

## Métricas-chave

| Métrica | Fórmula | Bom |
|---|---|---|
| ROTCE | Net income comum / TCE médio | ≥ 15% |
| P/TBV | Preço / TBVPS | ≤ 1.8 (top-tier), ≤ 1.3 (mid-tier) |
| P/E | Preço / EPS | ≤ 12 |
| NIM | NII / Earning assets | ≥ 2.5% (mais comprimido que BR) |
| Efficiency ratio | Non-interest expense / (NII + fee) | ≤ 60% |
| CET1 ratio | CET1 / RWA | ≥ 11% (varia por GSIB tier) |
| NCO ratio | Net charge-offs / loans | ≤ 0.5% (consumer ≤ 4%) |
| Reserve coverage | ALL / NPL | ≥ 200% |
| Loan-to-deposit | Loans / Deposits | 60-80% (sweet spot) |

## Tese actual US bancos (2026)

- **Macro setup favorável**: Fed cut cycle iniciou Q3 2024, curve positivada Q1 2025, deposit beta caindo > asset yields → NIM expansion 2025-26.
- **Credit normalizado**: NCO peaked Q4 2024 em consumer; CRE pressão continua mas isolated nos regionais com concentration alta.
- **Capital flush**: Basel III Endgame water-down libertou ~$30bn de buyback capacity para Big 4 → tailwind 2026.
- **JPM** é o quality compounder. ROTCE 21%, fortress BS, Dimon execution premium. **Mas o preço de $300+ tem opção embutida** — paying for the franchise. Entrada DRIP-friendly só <$240.
- **GS** é o cíclico dentro da banca — IB recovery + asset management growth. ROE volátil (10-22%) mas valuation barato em ciclos baixos. Verificar M&A volumes 2026.
- **BAC** é o trade alternativo a JPM (P/TBV ~1.4, ROTCE ~14%, mais barato mas menos quality). Sensível a rates (hold-to-maturity unrealized losses).
- **WFC** sai finalmente do asset cap (Fed levantou em 2025) — story de unlock. Consensus underweight.

## Red flags

- **Office CRE concentração** > 25% loan book (NYCB-style fragility).
- **Trading revenue** > 35% total receita (volatil — ver GS, MS — não é red flag mas não dá DRIP).
- **OCI hidden losses** (held-to-maturity bonds): se Fed sobe outra vez, mark-to-market re-emerge (SVB lesson).
- **Reserve release** consecutivo enquanto credit deteriorates → balanço a maquilhar earnings.
- **CET1 < 10%** com GSIB surcharge alta (JPM teria que rebuild capital).
- Buyback agressivo em P/TBV >2x (destruction of book value per share).

## Pegadas Buffett em US banks (histórico)

- **Wells Fargo** (1989-2018): clássica. Saiu post-fake accounts scandal 2017-18.
- **Bank of America** (2011-presente): preferred + warrants em 2011 ($5bn at deep discount), depois converteu — uma das melhores arbitragens da era pós-GFC.
- **American Express** (1991-presente): never sold. ~10x money em 35 anos.
- **JPMorgan**: passed deliberadamente em 2008 ("Dimon não precisa do meu dinheiro"). Berkshire só comprou pequena posição em 2018, depois saiu.
- **Goldman Sachs** (2008-2020): preferred + warrants em 2008 ($5bn). Saiu da common totalmente em 2020 (concerns sobre IB volatility).
- **Insight**: Buffett prefere franchise consumer banks (deposit moat) sobre IB-heavy. JPM é híbrido (60% retail/CB, 40% IB/AM) — quality mas não puro.

## Comparação rápida BR vs US bancos

| Dimensão | BR | US |
|---|---|---|
| ROE típico top-tier | 15-22% (era Selic alta) | 14-22% (RoTCE) |
| P/B histórico fair | 1.0-1.8x | 1.4-2.2x P/TBV |
| DY típico holding | 6-10% | 1.5-3% (buybacks dominam) |
| Payout via | dividendo + JCP (fiscal) | dividendo + buyback |
| Streak relevante | 5y+ (2008-2010 não cortaram, BR menos exposto) | pós-2009 (GFC reset) |
| Risco principal | Selic ciclo + inadimplência cartão | yield curve + CRE office |
| Regulação dominante | Bacen + Basel III | Fed + OCC + FDIC + Basel III |

## Como integrar ao scoring

```bash
python scoring/engine.py JPM --market us  # aplica score_us_bank automaticamente
python scoring/engine.py GS  --market us
python scoring/engine.py TFC --market us
```

`engine._is_us_bank` usa whitelist de tickers (`_US_BANK_TICKERS`: JPM, BAC, WFC, C, GS, MS, USB, PNC, TFC, BK, NTRS, STT, regionais, COF/DFS/AXP) + fallback para sector + nome. Mais robusto que só name-matching (TFC = "Truist Financial" não tem "bank" no nome).

### Status do screen (2026-04-26)

| Critério | Implementação | Fonte |
|---|---|---|
| P/E ≤ 12 | ✅ wired | `fundamentals.pe` (yfinance batch) |
| P/TBV ≤ 1.8 | ✅ wired | `fundamentals.tbvps` ← `scripts/backfill_us_bank_tangibles.py` (yfinance `Tangible Book Value`); fallback P/B se NULL |
| ROTCE ≥ 15% | ✅ wired | `fundamentals.rotce` ← mesmo backfill (NI Common / TBV); fallback ROE ≥ 12% se NULL |
| DY ≥ 2.5% | ✅ wired | `fundamentals.dy` |
| CET1 ≥ 11% | ⚠️ NA | Requer 10-Q XBRL parser — TODO |
| Efficiency ≤ 60% | ⚠️ NA | Idem |
| Streak pós-2009 ≥ 10y | ✅ wired (proxy) | `fundamentals.dividend_streak_years` com threshold 16 (sobreviveu 2009 sem cortar) |

### Snapshot holdings 2026-04-26

| Ticker | P/E | P/TBV | DY | ROTCE | Streak | Score | Verdict |
|---|---|---|---|---|---|---|---|
| **JPM** | 14.75 ✗ | 2.99 ✗ | 1.91% ✗ | 20.0% ✓ | 43y ✓ | 0.40 | premium franchise, hold-not-add acima $250 |
| **GS** | 16.92 ✗ | 2.67 ✗ | 1.67% ✗ | 15.8% ✓ | 28y ✓ | 0.40 | IB cíclico — comprar em down-cycle |
| **TFC** | 12.56 ✗ | **1.69 ✓** | **4.10% ✓** | 13.1% ✗ | 40y ✓ | **0.60** | DRIP-friendly hoje; ROTCE-quality é o gap |

**Insight**: das 3 banks da carteira, TFC é a mais alinhada com o screen Buffett US bank hoje. P/TBV barato, DY 4.1%. O ponto fraco é ROTCE 13% (quality menor que JPM/GS). Para DRIP puro, TFC > JPM no preço actual.

## Holdings actuais & gap

Hoje a carteira US tem [[JPM]] (banco) e [[GS]] (banca de investimento). Fica faltando:
- 1 super-regional puro (USB, PNC) — diversificação geográfica + retail mix
- 1 card / consumer credit (DFS, COF) — exposição diferente ao ciclo
- Eventualmente 1 trust (BK, NTRS) — fee-based, low-volatility complemento

Watch list que justifica adição: USB (P/TBV ~1.6, ROTCE 15%, DY 4.5%).

---

> Ver também: [[markets/US]], [[BR_Banks]], [[Dividend_Safety]], [[Yield_Curve_history]].
