# TEN (Tsakos Energy Navigation) — Review obrigatório

**Gerado**: 21/04/2026
**Razão**: `trigger_monitor` flagou Altman DISTRESS + Piotroski WEAK em posição activa.

---

## 1. Estado da posição

| Campo | Valor |
|---|---|
| Quantidade | 35 sh |
| Preço entrada | $23.93 |
| Preço actual | $38.76 |
| MV actual | $1,357 |
| **P&L unrealized** | **+$519 (+62%)** |
| % do US portfolio | 6.6% |

## 2. Sinais vermelhos (convergentes)

### 2a. Dividend cut -60% em 2025
```
2022:  $0.25 total   (recovery)
2023:  $1.00 total   (cycle ramp)
2024:  $1.50 total   (cycle peak — 2x quarterly)
2025:  $0.60 total   (1 único payment — CUT -60%)
```
Management parou de pagar semestral. Indica pressão em cash flow.

### 2b. Altman Z-Score = 1.02 (DISTRESS)
Zone de insolvência (<1.81). Componentes:
- WC/TA = -0.006 (working capital negativo)
- EBIT/TA = 0.066 (margem operativa a comprimir)
- MC/TL = 0.575 (dívida > equity de mercado × 1.7)

### 2c. Piotroski F-Score = 3/9 (WEAK)
6 dos 9 critérios degradaram vs 2024:
- FCF negativo ✗
- ΔROA negativo ✗
- FCF < Net Income ✗ (earnings de baixa qualidade)
- Leverage subiu ✗
- Liquidity caiu ✗
- Asset turnover caiu ✗

### 2d. Contexto de preço
- Low 2023-2026: $13.81
- **High 2023-2026: $40.71**
- Current: $38.76 (a -4.8% da máxima cíclica)
- DY percentile P17 → DY actual é EXPENSIVE vs histórico (confirma topo)

### 2e. ROE falha screen
- ROE 9.1% < 15% threshold
- Cyclical peak typical

---

## 3. Contexto sectorial — shipping de petróleo

TEN é crude tanker operator (VLCC + Suezmax + Aframax). Sector characteristics:
- Extreme cyclical (rates podem ×5 ou ÷5 em 18 meses)
- Rates 2022-2024 foram artificialmente altos (Russia/Ukraine redirection + IMO 2020 scrubber demand)
- Orderbook global 2025+ está a recuperar → novas entregas = excess supply 2026-2027
- Spot rates VLCC caíram de >$100k/day (Q4 2022) para ~$40k/day (Q1 2026) — pico longe

TEN passou pelos mesmos ciclos anteriormente:
- 2007-2008: peak → dividend cut 2009
- 2014-2015: peak → dividend cut 2016
- 2022-2024: peak → **dividend cut 2025** ← AGORA

Este padrão é o *playbook* do shipping. O veto Altman não é bug, é sinal estrutural.

---

## 4. Opções de acção

### Opção 1 — HOLD (status quo)
- Manter 35 sh.
- **Raciocínio**: posição pequena (6.6%), P&L positivo, cycle pode estender se geopolítica.
- **Risco**: dividend cut futuro, Altman pode piorar para zona de solvência.
- **Valor esperado**: baixo. Cycle reverting significa preço para $20-25 em 12-18m.

### Opção 2 — TRIM 50% (17 sh)
- Vender 17 sh × $38.76 = **$658 cash** colhido.
- Manter 18 sh × $38.76 = $698 exposure.
- **Raciocínio**: lock metade do lucro, mantém opcionalidade no cycle upside.
- **Realiza P&L** parcial de ~$253 (tax considerations apply).

### Opção 3 — SELL full (35 sh)
- Liquidar integralmente → **$1,357 cash**.
- **Realiza P&L** +$519.
- **Redeploy**: MKC (clean pass, $52/sh) ou TROW (clean pass, $99/sh).
- MKC @ $52 = 26 shares; TROW @ $99 = 13 shares; mix possível.
- **Raciocínio**: quality rotation from distress-flagged cycle peak to passing-screen compounder.

---

## 5. Recomendação

**Opção 3 (SELL full + redeploy)**.

**Porquê**:
1. Sinais convergentes nos 4 frameworks (Altman, Piotroski, screen, dividend cut) são unusual fortes. Quando Altman + Piotroski coincidem é sinal de alta confiança.
2. Preço -5% de máxima cíclica. Asimetria péssima (upside 5-10%, downside 30-50%).
3. TEN não se encaixa em nenhuma das tuas intenções: não é DRIP (divs cortados), não é Growth (shipping não cresce), não é Compounder. Só fazia sentido como tactical cycle bet — e o cycle virou.
4. Capital para rotação para MKC/TROW que passam screen **limpo**, estão em drawdown (MKC -33%, TROW -11%) e são Aristocrats há 41 anos.

**Execução sugerida** (quando for decidir):
- Sell 35 TEN @ market ≈ $1,357
- Buy ~$750 MKC (14 sh) + ~$600 TROW (6 sh) = $1,350
- Net cash flow zero; P&L realized +$519.

**Nota importante**: esta análise é determinística baseada em métricas. User deve:
- Confirmar que o cost basis ($23.93) está correto na JPM
- Considerar tax implications (capital gains realized)
- Não executar apenas por este memo — ver tape de abertura US, consultar filings recentes (20-F de 2026-04-06)

---

## 6. Trigger para rotação (se user quiser esperar)

Adicionar a `config/triggers.yaml` se preferires regra automática de venda:

```yaml
- id: ten_sell_altman
  ticker: TEN
  market: us
  kind: altman_distress
  threshold_z: 1.5          # mais estrito que 1.81 default
  action_hint: SELL
  note: "TEN em DISTRESS profundo (<1.5) + posição actual: sair do cycle peak"
```

Mas honestamente: sinais estão todos a dizer SELL agora. O trigger só automatiza o inevitável.
