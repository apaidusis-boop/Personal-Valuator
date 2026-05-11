---
type: tax
name: BR Dividend Isenção
region: BR
tags: [tax, br, dividend, jcp, isencao, regulatory]
related: ["[[Dividend_withholding_BR_US]]", "[[CVM_vs_SEC]]", "[[Tax_lot_selection]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 🇧🇷 BR — Isenção de IR sobre dividendos + JCP

## Lei 9.249/1995 — o quadro original

Base atual (válida 1996-presente):

| Provento | IR fonte (PF residente BR) | IR anual (ajuste) |
|---|---|---|
| **Dividendos** | **0% — isento** | Zero, não entra IR anual |
| **JCP (Juros sobre Capital Próprio)** | 15% retenção fonte | Zero mais (tributação definitiva) |
| **Rendimentos FII** | 0% se individual + ≥ 50 cotistas + mercado | Zero |
| **Ganho capital venda ações** | 15% (comum), 20% (day trade) | Com isenção R$ 20k/mês |

## Por que isto importa estruturalmente

BR é uma das **poucas jurisdições do mundo** com dividendo isento de IR pessoa física residente.

### Comparação global
| País | IR dividend PF |
|---|---|
| 🇧🇷 Brasil | **0%** (residente) |
| 🇺🇸 US | 15-37% (qualified vs ordinary) |
| 🇬🇧 UK | 8.75-39.35% (after allowance £500) |
| 🇩🇪 Germany | 26.375% flat |
| 🇫🇷 France | 30% flat (PFU) |
| 🇨🇦 Canada | 15-39% (gross-up + credit) |
| 🇵🇹 Portugal | 28% flat (não residente BR: 25% retido) |
| 🇦🇷 Argentina | 7% |
| 🇨🇱 Chile | 35% integrado |

→ Holder BR paga **zero** em dividendos, enquanto holder US paga 15-20% qualified.

## Impacto em compounding

**DRIP math**: a cada dividendo reinvestido, BR tem **vantagem estrutural de ~20-30% vs US** comparando mesmo DY nominal.

Exemplo: FII [[KNRI11]] a 8% DY, 20 anos de reinvestimento:
- BR: (1.08)^20 = 4.66× cotas acumuladas.
- Se fosse taxado a 15%: (1.068)^20 = 3.72× cotas — 20% menor.

Este é o **single most important structural advantage** para DRIP em BR.

## JCP — o "trick" contábil

**Juros sobre Capital Próprio** (lei 9.249/95 art 9º):
- Empresa paga **juros sobre o PL** (TJLP-indexed) aos acionistas.
- Do ponto de vista da empresa: **dedutível no lucro** → economia IR 34%.
- Do ponto de vista PF: retém 15% na fonte mas é definitivo (não vai pra IR anual).

**Por que empresas usam**:
- Payout total maior — mesmo valor net ao acionista, mas economia IR corporativa que flui como maior lucro distribuível.
- Matematicamente: se empresa pagar R$ 100 dividendo vs R$ 100 JCP, beneficio fiscal empresa é R$ 34 em JCP. 
- Acionista recebe R$ 100 - 15 IR = R$ 85 em JCP vs R$ 100 em dividendo.
- **Mas** empresa guardou R$ 34 em caixa no JCP → pode distribuir ou reinvestir.

**Quem usa**: virtualmente todos bancos (ITUB4, BBDC4, BBAS3 etc), utilities (TAEE11, EGIE3), maduras (ABEV3, VALE3).

**Quem não usa**: FIIs (não têm PL tributável), pequenas com PL baixo (juros inviabilizam).

## Projeto lei tributária 2026 (watch)

### PL 1.087/2025 (em discussão Câmara 2026)
**Propõe**: Tributar dividendos de PF em 15% (fonte) para pagamentos acima de **R$ 50.000/mês**.

**Status (abril 2026)**: em comissão CCJ, provável votação 2º semestre. **Alta probabilidade de aprovação** post-eleições.

**Mitigantes propostos**:
- Threshold R$ 50k/mês (poucos retail atingem).
- Transition period (provável 2027 startup).
- Redução IR corporativo (de 34% para 25-27%) em troca — net-neutral para alguns perfis.

### Impact em retail DRIP
- Quem recebe < R$ 50k/mês dividendos → **continua isento** (maioria retail).
- Impact **alto em high-net-worth** (> R$ 50k/mês = R$ 600k/y dividendos → carteira R$ 7-10M+).
- Para o teu perfil atual (estimativa carteira < R$ 1-2M dividendos < R$ 50k/mês) → **impact próximo de zero**.

### Consequência estrutural
- Se aprovado, **premium BR para DRIP caminha para US** — narrowing gap.
- FIIs devem manter isenção (distinct legal structure — condomínio fechado, lei 11.033/2004).
- JCP pode ser **extinto ou reformulado** (compensação da tributação).

## Efeito prático nos nossos critérios

### CLAUDE.md scoring BR
- **DY ≥ 6%** permanece válido (atualmente isento base).
- Se PL 1.087 aprovado e teu volume < R$ 50k/mês: continua válido.
- Se teu volume crescer muito > R$ 50k/mês: aplicar haircut mental 15% no DY efetivo.

### Rebalanceamento pre-aprovação
- Se PL aprovar 2026: existe janela 2026 para **antecipar dividendos** legitimamente.
- Empresas podem declarar special dividend + JCP pré-transição → retail holders beneficiam.

## Registros necessários

Via DARF ou declaração IR:
- Dividendos isentos: anexo "Rendimentos isentos e não tributáveis" (linha 09 ou outra).
- JCP: anexo "Rendimentos sujeitos à tributação exclusiva/definitiva" (15% já retido).
- Comprovantes emitidos pela corretora/escriturador.

## FIIs — caso especial

- **Lei 11.033/2004** mantém isenção para PF residente em FIIs:
  - Fundo com ≥ 50 cotistas.
  - Cotas negociadas em bolsa.
  - PF detém < 10% do fundo.
- **Ganho capital em FII**: 20% IR (diferente de ação).
- **Watch**: PL 1.087 pode propor mexer em FII também — acompanhar.

## Estratégias tax-aware

1. **Max out tax-free BR**: FIIs + ações dividendo enquanto isento.
2. **JCP cash flow** é melhor que dividendo em payout similar (company tax benefit → reinveste).
3. **Não reinvestir dividendo em AÇÃO com P/E peak** — espere correção mesmo que cash fique parado (tax-free waiting é vantagem).
4. **Isenção R$ 20k/mês ganho capital** — planear rebalance mensal para não exceder.

## Red flags

- Empresa corta JCP sem explicação → structural change.
- Empresa paga dividendo 100% sem JCP → provavelmente tem tax loss carry forward pesado.
- Grande distribuição pre-elections 2026 → pode ser IPO de efeito fiscal.

---

> Ver [[Dividend_withholding_BR_US]] (se houver holdings cross-border). [[Tax_lot_selection]] para optimização ganho capital.
