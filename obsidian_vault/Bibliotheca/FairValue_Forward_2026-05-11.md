# Fair Value Forward — leitura quality-aware (US)  ·  2026-05-11

> **EXPERIMENTAL** — `analytics.fair_value_forward`. NÃO está no engine nem no daily_run.
> Mostra o que um DCF conservador que *dá crédito ao prémio de qualidade* diz, lado a lado
> com o teto Buffett-Graham (`our_fair`) que continua a ser o número oficial persistido.
> Método em `analytics/fair_value_forward.py` (docstring). Decisão A/B de fusão pendente —
> ver [[Sessions/FairValue_Forward_Audit_2026-05-11]] e [[Bibliotheca/Manual_de_Direcao]].

| Ticker | Sector | Preço | Engine `our_fair` / action | **Forward fair** (impl. mult.) | Margem | Analistas PT (n) | **Leitura fwd** |
|---|---|---|---|---|---|---|---|
| ★ **ACN** | Technology | $180.42 | $115.48 / HOLD | $238.51 (16.0×) | +32.2% | $249.19 (26) | **ADD** |
| ★ **BLK** | Financials | $1,084.83 | $606.58 / HOLD | $970.53 (16.0×) | -10.5% | $1,254.12 (16) | **RICH** · *street mais bull (PT ≫ fwd)* |
| ★ **HD** | Consumer Disc. | $317.45 | $213.41 / HOLD | $260.94 (16.0×) | -17.8% | $406.58 (33) | **EXPENSIVE** · *street mais bull (PT ≫ fwd)* |
| ★ **JNJ** | Healthcare | $221.32 | $142.03 / HOLD | $251.47 (19.8×) | +13.6% | $252.42 (24) | **ADD** |
| ★ **JPM** | Financials | $302.10 | $198.20 / SELL | $284.33 (14.0×) | -5.9% | $342.32 (22) | **RICH** · *street mais bull (PT ≫ fwd)* |
| ★ **KO** | Consumer Staples | $78.42 | $52.10 / HOLD | $68.82 (19.8×) | -12.2% | $85.80 (23) | **RICH** · *street mais bull (PT ≫ fwd)* |
| ★ **O** | REIT | $61.92 | $72.40 / STRONG_BUY | $67.52 (16.0×) ⚠️ | +9.0% | $68.50 (20) | **FAIR** |
| ★ **PG** | Consumer Staples | $146.42 | $107.83 / HOLD | $122.21 (17.2×) | -16.5% | $163.77 (22) | **RICH** · *street mais bull (PT ≫ fwd)* |
| ★ **AAPL** | Technology | $293.32 | $121.44 / SELL | $152.96 (16.0×) | -47.9% | $305.28 (42) | **EXPENSIVE** · *street mais bull (PT ≫ fwd)* |
|   **ABBV** | Healthcare | $201.55 | — | $294.95 (18.2×) | +46.3% | $252.23 (30) | **ADD** · *street mais bear (PT ≪ fwd)* |
| ★ **BN** | Financials | $47.08 | $7.35 / SELL | — ⚠️ | — | — | **—** |
| ★ **BRK-B** | Holding | $475.94 | $524.16 / HOLD | — ⚠️ | — | — | **—** |
| ★ **GREK** | ETF | $71.82 | — | — ⚠️ | — | — | **—** |
| ★ **GS** | Financials | $936.48 | $532.48 / SELL | $556.32 (13.0×) | -40.6% | $947.60 (20) | **EXPENSIVE** · *street mais bull (PT ≫ fwd)* |
| ★ **NU** | Financials | $13.80 | $5.44 / SELL | — ⚠️ | — | — | **—** |
| ★ **PLD** | REIT | $144.09 | $93.94 / SELL | $88.96 (16.0×) ⚠️ | -38.3% | $150.65 (20) | **EXPENSIVE** · *street mais bull (PT ≫ fwd)* |
| ★ **PLTR** | Technology | $137.80 | $7.71 / SELL | — ⚠️ | — | — | **—** |
| ★ **TEN** | Energy | $43.80 | $52.82 / SELL | $46.96 (16.0×) ⚠️ | +7.2% | $46.00 (2) | **FAIR** |
| ★ **TSLA** | Consumer Disc. | $428.35 | $16.42 / SELL | — ⚠️ | — | — | **—** |
| ★ **TSM** | Technology | $411.68 | $182.36 / SELL | — ⚠️ | — | — | **—** |
| ★ **XP** | Financials | $19.17 | $21.25 / BUY | — ⚠️ | — | — | **—** |

`Margem` = quanto o forward fair está acima(+)/abaixo(−) do preço atual. Vocab `Leitura fwd` (sobre o **forward fair puro**, não misturado com o PT dos analistas): **ADD** = preço ≤ 90% do forward fair (margem ≥ ~10%) · **FAIR** = ±5% · **RICH** = 5-20% acima · **EXPENSIVE** = >20% acima. ⚠️ = baixa confiança (holdco/ETF/REIT sem AFFO calibrado/distressed). O PT dos analistas é mostrado só como referência — *não* entra na leitura (disciplina: não confiar no número que adoramos).

## Notas por ticker

- **ACN** — DCF abaixo de 16× owner earnings — elevado ao piso da banda de sanidade (de-rate abaixo disto só em crise) · base = forward EPS consenso ≈ 14.91; g1=3.7% fade→2.5%; desconto r=9.5%; banda 16-25× OE
- **BLK** — DCF abaixo de 16× owner earnings — elevado ao piso da banda de sanidade (de-rate abaixo disto só em crise) · base = forward EPS consenso ≈ 60.66; g1=2.4% fade→3.0%; desconto r=9.5%; banda 16-25× OE
- **HD** — CAGR histórico de lucro negativo/indisponível (charges one-off / ciclo?) → g1=4% por defeito conservador · DCF abaixo de 16× owner earnings — elevado ao piso da banda de sanidade (de-rate abaixo disto só em crise) · base = forward EPS consenso ≈ 16.31; g1=4.0% fade→2.5%; desconto r=9.5%; banda 16-25× OE
- **JNJ** — CAGR histórico 14.3% cortado para o cap sectorial de 6% · base = forward EPS consenso ≈ 12.71; g1=6.0% fade→2.5%; desconto r=8.5%; banda 16-25× OE
- **JPM** — EPS norm. (mediana 3y) = 20.31; multiple 14× (engine usa us_bank_pe12 = ×12, que é o *screen ceiling*)
- **KO** — CAGR histórico 11.2% cortado para o cap sectorial de 6% · base = forward EPS consenso ≈ 3.48; g1=6.0% fade→2.5%; desconto r=8.5%; banda 16-25× OE
- **O** — AFFO/share ≈ 4.22 (hand-maintained); P/AFFO 16× (engine usa BVPS×2, sem base AFFO). Calibrar P/AFFO por sub-sector.
- **PG** — base = forward EPS consenso ≈ 7.09; g1=2.7% fade→2.5%; desconto r=8.5%; banda 16-25× OE
- **AAPL** — DCF abaixo de 16× owner earnings — elevado ao piso da banda de sanidade (de-rate abaixo disto só em crise) · base = forward EPS consenso ≈ 9.56; g1=3.9% fade→2.5%; desconto r=9.5%; banda 16-25× OE
- **ABBV** — CAGR histórico de lucro negativo/indisponível (charges one-off / ciclo?) → g1=4% por defeito conservador · base = forward EPS consenso ≈ 16.21; g1=4.0% fade→2.5%; desconto r=8.5%; banda 16-25× OE
- **BN** — holdco / ETF — economia por ação não mapeia para um DCF simples; ver dossiê / NAV
- **BRK-B** — holdco / ETF — economia por ação não mapeia para um DCF simples; ver dossiê / NAV
- **GREK** — holdco / ETF — economia por ação não mapeia para um DCF simples; ver dossiê / NAV
- **GS** — EPS norm. (mediana 3y) = 42.79; multiple 13× (engine usa us_bank_pe12 = ×12, que é o *screen ceiling*)
- **NU** — growth pick (>20%/ano) — DCF com cap de crescimento 8% não tem sentido; valorizar por outra lente (memory user_investment_intents)
- **PLD** — AFFO/share ≈ 5.56 (hand-maintained); P/AFFO 16× (engine usa BVPS×2, sem base AFFO). Calibrar P/AFFO por sub-sector.
- **PLTR** — growth pick (>20%/ano) — DCF com cap de crescimento 8% não tem sentido; valorizar por outra lente (memory user_investment_intents)
- **TEN** — CAGR histórico de lucro negativo/indisponível (charges one-off / ciclo?) → g1=4% por defeito conservador · DCF abaixo de 16× owner earnings — elevado ao piso da banda de sanidade (de-rate abaixo disto só em crise) · base = forward EPS consenso ≈ 2.94; g1=4.0% fade→2.5%; desconto r=10.5%; banda 16-25× OE
- **TSLA** — growth pick (>20%/ano) — DCF com cap de crescimento 8% não tem sentido; valorizar por outra lente (memory user_investment_intents)
- **TSM** — reporta em moeda ≠ USD — owner earnings de deep_fundamentals não comparáveis ao preço em USD; usar valuation nativa
- **XP** — reporta em moeda ≠ USD — owner earnings de deep_fundamentals não comparáveis ao preço em USD; usar valuation nativa

## Como ler isto vs o engine

- `our_fair` (engine) = teto Buffett-Graham menos margem de segurança — **disciplina de preço**, deliberadamente exigente. Grita 'múltiplo rico' cedo.
- `Forward fair` (este módulo) = DCF 2-estágios sobre owner earnings (conservador: g cortado, fade para 2,5-3%, desconto 8,5-9,5%, teto 25× OE) — **dá crédito ao prémio de qualidade** de um negócio de fosso largo e ROIC durável.
- A verdade está entre os dois. Quando o engine diz SELL e o forward diz FAIR, a leitura humana é 'não está barato mas SELL é exagero' (KO/JNJ). Quando ambos dizem ADD/cheap, é sinal forte (ACN).
- Bancos: o forward usa EPS normalizado × 13-14× (best-in-class), não o ×12 do screen ceiling. REITs: P/AFFO, não BVPS×2 — mas precisa de AFFO calibrado por sub-sector.

_Gerado por `python -m analytics.fair_value_forward` em 2026-05-11. Fontes: `data/us_investments.db` (deep_fundamentals annual, fair_value, prices) + yfinance analyst targets (se disponível)._