---
type: method
name: Free Cash Flow Yield
category: valuation
tags: [method, valuation, fcf, yield, quality]
related: ["[[P_E_interpretation]]", "[[DCF_simplified]]", "[[Dividend_Safety]]", "[[Buffett_quality]]"]
---

# FCF Yield

## Fórmula

$$
\text{FCF Yield} = \frac{\text{Free Cash Flow}}{\text{Market Cap}} \times 100\%
$$

Ou por acção:
$$
\text{FCF Yield} = \frac{\text{FCF per share}}{\text{Price}} \times 100\%
$$

**FCF = Cash Flow from Operations − Capital Expenditures** (e idealmente − SBC).

## Por que FCF > earnings

1. **Earnings são uma opinião, cash é um facto** (saying Buffett)
2. **Ignora acruais** (receivables, inventory, D&A choices)
3. **Captura capital intensity** — CapEx não está em EPS
4. **Harder to manipulate** (SPE accounting schemes raras com cash)

## FCF yield vs earnings yield (1/PE)

Normalmente **FCF yield < EY** porque:
- D&A > CapEx em companies estabelecidas asset-light (KO, PG)
- Stock-based comp não sai de earnings mas sai de equity dilution

Se **FCF yield > EY**, empresa converte > 100% earnings em cash → quality.

## Thresholds

| FCF Yield | Interpretação |
|:-:|---|
| > 10% | 🟢 Deep value — watch for reason |
| 7-10% | 🟢 Cheap |
| 5-7% | Fair |
| 3-5% | Premium growth |
| < 3% | 🔴 Expensive / growth stock |

## FCF yield vs DY

Para dividend investors:
- **FCF yield > DY = sustentável** (div < FCF, há buffer)
- **FCF yield < DY = distress** (pagando div com debt ou asset sales)

**Coverage ratio**:
$$
\text{FCF/Div coverage} = \frac{FCF}{\text{Dividends paid}}
$$

Safety thresholds:
- \> 2× → SAFE
- 1.5-2× → adequate
- 1-1.5× → thin (watch)
- < 1 → pagando div com dívida = **RED FLAG**

## Ajustes importantes

### 1. Stock-based comp (SBC)
GAAP FCF **não desconta SBC**. Tech companies: SBC é 10-20% do "FCF"
- **"True FCF"** = GAAP FCF − SBC

Exemplo MSFT: reported FCF $70B, SBC $10B → true FCF $60B.

### 2. Acquisition CapEx
M&A cash outflow não está em CapEx regulatorial. Empresa que cresce comprando (UHG, CHD) tem FCF reported = flattering.
- Usar **FCF pós-acquisition** (subtrair cash spent on M&A)

### 3. Working capital seasonal
Q1 vs Q4 — receivables/payables oscillate. Usar TTM (últimos 12m), não Q.

### 4. One-time items
- Tax refund from carry-back
- Litigation settlement
- Asset sale cash

Normalizar com **5y average FCF**.

## FCF vs CFO vs EBITDA

| Métrica | Inclui | Ignora |
|---|---|---|
| **EBITDA** | Operating revenue/expenses | D&A, interest, taxes, **CapEx** |
| **CFO** | Operating cash + working capital Δ | CapEx |
| **FCF** | CFO − CapEx | SBC (if GAAP) |
| **FCF-SBC** | True owner earnings | — |

Buffett prefers **"owner earnings"**:
$$
\text{Owner earnings} = NI + D\&A - \text{maintenance CapEx} - \text{working capital changes}
$$

## No nosso sistema

Actualmente `scoring/engine.py` não usa FCF yield directly (foca P/E, P/B, ROE, DY).

**Pendente implementar**: `scoring/fcf.py` que computa FCF yield + coverage + trend.

Verificações existentes:
- `scoring/piotroski.py`: criterion 2 (FCF > 0), criterion 4 (FCF > NI quality)
- `scoring/dividend_safety.py`: payout usa EPS mas deveria ser FCF

## Exemplo: ACN 2026

- Market cap 2.85 × 10⁷ × $178 ~ $112B
- FCF TTM $10.9B (Piotroski detail data)
- FCF Yield = 10.9 / 112 = **9.7%** → **deep value zone**

ACN tem **melhor FCF yield que peers tech**:
- MSFT ~3%, V ~3.5%, MA ~3%, AAPL ~4%, ORCL ~5%

## Research checklist antes de confiar

1. FCF sustentável ou one-off?
2. SBC já ajustado?
3. CapEx de manutenção vs crescimento separados?
4. Trend FCF últimos 5y
5. Conversão NI → FCF consistente ≥ 80%?

---

> **Fontes**: Buffett 1986 letter ("Owner Earnings"); McKinsey *Valuation*; Michael Mauboussin *Expectations Investing*; Aswath Damodaran free cash flow valuation papers.
