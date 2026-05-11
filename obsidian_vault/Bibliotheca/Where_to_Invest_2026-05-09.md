---
title: Where to Invest — 2026-05-09 (post-fix definitivo)
date: 2026-05-09
type: investment_recommendation
trigger: pós-bug-sweep 2026-05-09; system test 5-fase + 5 commits a fechar gaps materiais
data_state: fair_value recomputed universe (172 rows), conviction holdings re-run, IC dossiers regen para 6 tickers material
related: [[System_Test_2026-05-09]], [[Extension_Run_2026-05-09]]
---

# Where to Invest 2026-05-09

Dados pós-fix dos 5 bugs estruturais. Antes desta session, o motor estava
a gritar SELL em PG/JNJ/KO (false), AVOID em ITSA4/BBDC4 (false), e a routear
JPM por buffett_ceiling em vez de bank multiple. Agora a leitura é confiável.

NAV: ~$87k (US $22.8k + BR R$355k @ 6.10 ≈ $58k). HHI 825 (bem-diversificado).

---

## US — single material BUY: **O (Realty Income)**

| | Value |
|---|---|
| Current | $61.92 |
| our_fair | $72.40 |
| Action | **STRONG_BUY** |
| Upside | +16.9% |
| Method | reit_pb_proxy |
| DivSafety | 75 (HOLD) |
| Confidence | cross_validated |
| Position actual | 30 sh × $61.92 = $1,858 (8.1% NAV US) |
| Allocate target | 6.5% — drift +$374 (already at target) |

**Rationale**: REIT correctly handled by sector (BVPS × 2 = $86, our_fair=$72). Monthly aristocrat, 33y dividend streak. The IC committee was AVOID this morning — let me re-IC it post-fix to see if that changes (likely Klarman tail risk concern still valid, but Buffett+Druck+Dalio probably BUY).

**Actionable**: O já está overweight ligeiro. Não adicionar agora porque o drift está positivo. Mas é o único nome US com sinal BUY genuíno. Se chegar cash novo, considerar add.

## US — strongly held, **don't trim**

| Ticker | Action | Reason | Position |
|---|---|---|---|
| **KO** | HOLD (was false SELL) | intangible_warning gate fired (ipa 26.7%); KO é o canonical Buffett brand. IC committee post-fix BUY (medium) — Buffett+Druck+Dalio convergem 8/7/8 conv. | 11 sh × $78.42 = $860 |
| **PG** | HOLD (was false SELL) | tbv −$12B, gate firing. IC HOLD (high). Klarman AVOID conv 8 mas 4/5 HOLD. | 10 sh × $146.42 = $1,464 |
| **JNJ** | HOLD (was false SELL) | tbv −$17B, gate firing. IC HOLD (medium). Taleb+Klarman AVOID, others HOLD. Moat 8.75 STRONG (de smoke). | 10 sh × $221.32 = $2,213 |
| **BRK-B** | HOLD | upside +10.1%, fair $524 vs cur $475. Buffett core, no-action. | 1 sh × $475.94 |

## US — strict valuations say SELL but **review philosophy**

Estes têm SELL porque criteria Graham/Buffett strict são impossíveis para
megacap modernas. Não é bug do gate — é fundamental limitation da fórmula
ceiling. Decide manualmente, não acionar SELL automaticamente.

| Ticker | Action | our_fair vs cur | Position | Comment |
|---|---|---|---|---|
| **AAPL** | SELL | $16.61 vs $293 | 5 sh × $293 = $1,467 | Brand off-balance + organic growth. Modern compounder, P/E ~30. |
| **MSFT** | SELL | $130 vs $415 | $0 (target $2,146 short) | Cloud dominance + ROE >35%. Modern compounder. |
| **TSM** | SELL | $15.30 vs $411 | 5 sh × $411 = $2,058 | Tech foundry leader. Cyclical but moat strong. |
| **JPM** | SELL | $198 vs $302 | 7 sh × $302 = $2,114 | Bank multiple correct (EPS×12); JPM at 14.5 P/E above mid-cycle 12. **Trim consider** if cycle peak risk. |
| **GS** | SELL | $532 vs $936 | 1 sh × $936 = $936 | Bank multiple. GS at 9.4 P/E roughly mid-cycle, but absolute price above ceiling.|
| **PLD** | SELL | $94 vs $144 | 2 sh × $144 = $288 | REIT pb_proxy. Industrial REIT premium baked in. |

**Recommendation US**: Não trade automatic. Single action material:
- **Add ACN to drift target**: ACN currently $777 vs target 10.4% × NAV = $2,374. Drift −$1,598. Conviction 90, action HOLD (gate fired ipa 38%), no veto. Most underallocated quality name.
- **Consider IBM/HD adds**: target 7.7% / 5.9% but currently 0% / 1.4% positions. Both HOLD (gate fired). Lower-conviction picks vs ACN.

## BR — material BUYs: **POMO3, PVBI11**

| Ticker | Action | Detail |
|---|---|---|
| **POMO3** | BUY | Graham our_fair R$6.09 vs current R$6.00, +1.4% upside. Allocate top BR target (9.6%). Currently NÃO holding. |
| **PVBI11** | BUY | FII NAV R$80.89 vs cur R$77.45, +4.4%. **Memory rule: turnaround thesis deliberada — manter, não vender.** Already hold 217 cotas. |

## BR — strongly held HOLD, **não rebalance**

| Ticker | Action | Reason | Position |
|---|---|---|---|
| **ITSA4** | HOLD (was false AVOID) | DRIP HOLD post-fix; IC BUY (high) 4/5 personas; Graham HOLD margin -3.8% (close-to-fair). Conviction 90. | 2,485 × R$13.50 = R$33,547 |
| **BBDC4** | HOLD (was false AVOID) | DRIP HOLD post-fix (ROE fallback fix); IC HOLD (medium); br_bank_mult fair R$14.72, cur R$18.59 = -20.8% upside (slight overvalued). | 1,837 × R$18.59 = R$34,150 |
| **PETR4** | HOLD | Graham R$42.82 vs R$45.67 = -6.2%. Close to fair. | (not in current portfolio) |

## BR — distress vetoes / SELL signals (review manually)

| Ticker | Action | Why |
|---|---|---|
| **VALE3** | SELL | Outlier-median override + Graham R$33 vs R$81. CVM disputed signal. (Memory: deteriorating quality.) | 501 × R$81.49 = R$40,826 — **largest BR position after LFTB11**. |
| **PRIO3** | SELL | Altman distress veto. | 503 × R$63.27 = R$31,825 |
| **SUZB3** | SELL | Altman Z=1.66 distress (forced BUY→SELL despite +21% Graham upside). |
| **ITUB4** | SELL | br_bank_mult R$20 vs R$41. Strict bank multiple. ITSA4 owns ITUB4 — already exposed via ITSA4. |
| **KLBN11** | SELL | Graham R$6 vs R$17 = -64.7%. Way above ceiling. |
| **MULT3** | SELL | Graham R$23 vs R$32 = -26.8%. |

**VALE3/PRIO3** são as posições problemáticas no portfolio actual — combined R$72.6k (20%+ of BR NAV). Antes de qualquer action, validar a tese de SELL com sources independentes. VALE3 outlier_median fired por CVM disagree com yf+Fundamentus — é confidence "disputed".

## Action items recomendados

### Imediato (high conviction)
1. **Add ACN para target** — cash USD $1,598 → ACN. Conviction 90, drift maior do portfolio US. Não há flags negativos.
2. **NÃO acionar PG/JNJ/KO SELL** — bug fix confirmou false signal.
3. **NÃO acionar ITSA4/BBDC4 AVOID** — DRIP false signal corrigido.

### Review (medium conviction)
4. **Considerar add PG/JNJ até target** — ambos overweight vs allocate. Mas conviction 84/manhã sugere manter.
5. **VALE3 review thesis** — disputed signal + outlier flag. R$40.8k posição. Antes de SELL real, ler dossier mais recente + checking Altman/Piotroski drivers.
6. **JPM trim consideration** — 9.3% NAV US, criteria-strict acima do mid-cycle 12 P/E. Não acionar SELL automatic mas size review faz sentido.
7. **POMO3 small new position?** — BUY signal, small allocate target 9.6%. Consider R$2-5k toehold.

### Não acionar
- AAPL/MSFT/TSM SELL signals: Buffett ceiling fundamentally inadequate for modern compounders. Bug pendente F1 (modern overlay) — não trade até decidir.
- BR FII allocations: KNHF11/BTLG11/XPML11/VGIR11 todos HOLD/TRIM perto de NAV. Cargo cycling não ganha nada.
- TEN: memory rule, distress signal. Não adicionar.

## Open issues identified this session

1. **AAPL/MSFT eternal SELL** — fundamental Graham strict limitation. Pendente Phase F1 modern compounder overlay.
2. **JPM strict bank criteria** — score_us_bank P/E ≤ 12, P/TBV ≤ 1.8, DY ≥ 2.5%. JPM at 14.5/2.35/1.95 fails 3/5. Conservative-correct but produces SELL/AVOID on a name in regulated post-GFC equilibrium. Re-evaluate threshold or add tier (e.g. ≤14 for top-quartile bank).
3. **VALE3 outlier disputed** — CVM parser may be undercounting Q4'24 settlement loss. Worth investigating before confirming SELL.
4. **CVM events 8d stale** — external network outage to dados.cvm.gov.br. Auto-reset em 6h (was 24h).
5. **Perpetuum thesis scoring −1 universe-wide** — separate bug. Caused conviction --universe to return 0. Holdings-only conviction works.
6. **AAPL/MSFT positions vs allocate** — MSFT target 9.4% × $22.8k = $2.1k mas posição 0. Significa missed allocate signal? Or deliberate skip?

## Confidence map

| Recommendation | Confidence | Why |
|---|---|---|
| Add ACN to target | High | Conviction 90 + no flags + biggest drift |
| Don't sell PG/JNJ/KO | High | Gate fix verified + IC supportive (KO BUY explicitly) |
| ITSA4/BBDC4 hold | High | DRIP fix verified + IC consensus |
| O is BUY | Medium | REIT engine confidence cross_validated, IC AVOID this morning (re-IC pendente) |
| JPM trim | Low | Criteria-strict signal, but bank methodology debatable |
| VALE3 SELL | Low | Disputed confidence — needs independent verification |

---

*Report grounded em: 172 fair_value rows post-fix · 33 conviction scores holdings · 6 IC dossiers regenerated post-fix · 5 commits a fechar bugs estruturais. NÃO accionar trades sem cross-check final manual.*
