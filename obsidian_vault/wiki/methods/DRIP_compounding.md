---
type: method
name: DRIP — Dividend Reinvestment Plan
category: income
tags: [method, drip, compound, income, long_term]
related: ["[[DDM_Gordon]]", "[[Aristocrats_Kings]]", "[[Dividend_Safety]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# DRIP — Dividend Reinvestment

## Definição

Reinvestimento automático dos dividendos recebidos de volta em shares da **mesma empresa** (ou outra), multiplicando shares detidas sem novo capital externo.

## A matemática do compound

Dados:
- Shares iniciais S₀
- DY = d (ex: 3%)
- Price growth = p (ex: 4%/y)
- Dividend growth = g (ex: 5%/y)

Após n anos, shares:
$$
S_n = S_0 \cdot \prod_{t=1}^{n} \left(1 + \frac{d(1+g)^{t-1}}{(1+p)^t}\right)
$$

E total return incluindo price:
$$
TR_n = \frac{S_n \cdot P_0 \cdot (1+p)^n}{S_0 \cdot P_0} - 1
$$

## Regra de ouro: **Payback Period**

Número de anos até o dividendo reinvestido dobrar shares:

| DY | g div | Payback (anos) |
|---|---|---|
| 2% | 6% | 28 |
| 3% | 5% | 22 |
| 4% | 5% | 17 |
| 5% | 4% | 14 |
| 6% | 3% | 12 |
| 7% | 3% | 10 |

Inferior payback = compound mais rápido. **Ideal: DY ~4-5% + g ~5%**.

## Exemplo concreto: ITSA4 DRIP

Dados (2026):
- Preço R$14.41
- DY trailing ~7%
- Dividend growth 5y CAGR ~12% (cyclical bank env)
- Se preço subir 4%/y, div subir 8%/y:

| Ano | Shares | Div cash | Novas shares | Total value |
|---|---|---|---|---|
| 0 | 2,472 | — | — | R$35,622 |
| 5 | 3,330 | R$3,800 | +263/y | R$58,000 |
| 10 | 4,480 | R$6,200 | +347/y | R$95,000 |
| 15 | 6,020 | R$10,100 | +457/y | R$155,000 |
| 20 | 8,100 | R$16,500 | +605/y | R$253,000 |

Valor 7× em 20y com **apenas reinvestindo** — sem injectar capital.

## Vantagens

1. **Dollar-cost averaging automático** (preços altos/baixos médios)
2. **Sem taxa de compra** (brokers isentam para DRIP)
3. **Psicologia**: removes temptation to time market
4. **Fractional shares** permitidos na maioria dos brokers US (JPM, Fidelity, Schwab)
5. **Tax-efficient em BR** (dividendos isentos de IRPF até MP)

## Desvantagens

1. **Concentration risk** crescente — 20y DRIP em 1 ticker que quebra = disaster
2. **Tax drag em US** — dividendos tributados ANO do recebimento (mesmo reinvestido); evitar em IRA/401k
3. **Over-valuation buying** — se preço disparar, DRIP compra caro (mitigate com DCA external + DRIP)
4. **Concentração posicional** — em 20y, 1 posição pode ser 50% da carteira

## Quando DRIP faz mais sense

✅ **Aristocrats com 25+ anos streak**
✅ **Carteiras diversificadas 15-25 tickers** (spreads concentration risk)
✅ **Long horizon 15y+**
✅ **Brokerage BR** (dividendos isentos até MP change)
✅ **Growth moderado** (não hyper-growth)

## Quando DRIP falha

✗ **Concentração extrema em 1 ticker** (T DRIP 2000-2022 = −50% real)
✗ **Carteiras pequenas iniciais** (< 20 shares → rounding inefficient sem fractional)
✗ **Horizontes < 10 anos** (compound não materializa)
✗ **Empresas em decline secular** (GE, ATT, Kraft)

## DRIP vs accumulate cash manually

Alternativa: **NÃO DRIP**, acumular cash, fazer compras grandes trimestrais quando há oportunidade.
- Prós: controlas entry, pode entrar noutro ticker cheaper
- Contras: disciplina psicológica; muitos deixam cash estagnar

**Híbrido** (o nosso approach):
- DRIP activo em Aristocrats high-conviction (JNJ, PG, KO, ITSA4, VALE3)
- Cash acumulado trimestral para **opportunistic DCA** em drawdowns (ex: ACN Abril 2026 DCA)

## No nosso sistema

- `scripts/drip_projection.py` calcula 5/10/15/20y scenarios
- `portfolio_positions.notes` regista "DRIP active" vs "cash accumulate"
- [[Intenção por posição]] memory flagga per ticker

---

> **Fontes**: Daniel Peris *The Dividend Connection*; Jeremy Siegel *The Future for Investors* (cap. 10 DRIP); SureDividend tools; nosso código em `scripts/drip_projection.py`.
