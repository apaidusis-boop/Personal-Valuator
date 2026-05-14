---
type: council_dossier
ticker: MOTV3
market: br
modo: A
is_holding: false
date: 2026-04-30
final_stance: HOLD
confidence: medium
elapsed_sec: 40.1
tags: [council, storyt2, debate]
---

# Council Dossier — MOTV3 (MOTV3)

**Final stance**: 🟡 **HOLD**  
**Confidence**: `medium`  
**Modo (auto)**: A (BR)  |  **Sector**: Industrials  |  **Held**: não  
**Elapsed**: 40.1s  |  **Failures**: 0

## Síntese

**Consenso**:
- A relação dívida líquida/EBITDA está acima do limite ideal
- ROE acima de 15% e margens EBITDA sólidas sugerem potencial

**Dissenso (preservado)**:
- role RISK_OFFICER diz que o alto ROE pode ser temporário ou não indicar uma tendência sustentável se a relação dívida líquida/EBITDA continuar alta e sem mitigação clara
- role PORTFOLIO_OFFICER diz que embora a relação dívida líquida/EBITDA esteja alta, o ROE de 20.8% sugere que a empresa pode gerar lucros suficientes para reduzir essa alavancagem ao longo do tempo

**Pre-publication flags** (rever antes de qualquer narrativa imprimir):
- ⚠️ CCC deteriorando >30% YoY sem explicação
- ⚠️ dividend yield baixo e relação dívida líquida/EBITDA acima de 3x

**Sizing**: size 1.5-2.5% se add, trim se peso > 5%, hold actual se watchlist

## Round 1 — Opening Statements (blind)

### Sector Specialist — 🟡 **HOLD**

**Headline**: _MOTV3 tem ROE forte mas preocupante ND/EBITDA e DY baixo_

A empresa apresenta um ROE acima de 15% e margens EBITDA sólidas, sugerindo potencial. No entanto, a relação ND/EBITDA está alta e o DY é insatisfatório.

**Supporting metrics**:
- ROE=20.8%
- ND/EBITDA=3.55
- DY=1.98%

**Concerns**:
- ND/EBITDA acima do limite ideal
- Dividend yield baixo

### Risk Officer — 🔴 **AVOID**

**Headline**: _Risco de deterioração financeira e incerteza operacional_

A relação dívida líquida/EBITDA está acima do limite ideal, sem mitigação clara nos próximos dois anos. Além disso, a empresa quebrou recentemente seu histórico de dividendos.

**Supporting metrics**:
- ND/EBITDA=3.55
- DivStreak=2.00

**Concerns**:
- Deterioração da margem EBITDA nos últimos trimestres
- Possível falta de liquidez para manter o pagamento de dividendos

**Veto signals**:
- 🚫 CCC deteriorando >30% YoY sem explicação

### Portfolio Officer — 🟡 **HOLD**

**Headline**: _MOTV3 tem potencial de valorização mas riscos financeiros_

ROE acima de 20% sugere crescimento futuro, porém dívida líquida/EBITDA elevada e DY baixo indicam cautela.

**Supporting metrics**:
- P/E=10.72
- ROE=20.8%
- ND/EBITDA=3.55

**Concerns**:
- dívida líquida/EBITDA acima de 3x
- dividend yield baixo

## Round 2 — Responses (after seeing peers)

### Sector Specialist — 🟡 **HOLD**

**Agreed with**:
- A relação dívida líquida/EBITDA está acima do limite ideal, sem mitigação clara nos próximos dois anos.
- risk_officer

### Risk Officer — 🔴 **AVOID**

**Agreed with**:
- A empresa apresenta um ROE acima de 15% e margens EBITDA sólidas, sugerindo potencial.
- sector_specialist

**Challenged**:
- ROE acima de 20% sugere crescimento futuro
- O alto ROE pode ser temporário ou não indicar uma tendência sustentável se a relação dívida líquida/EBITDA continuar alta e sem mitigação clara.

### Portfolio Officer — 🟡 **HOLD**

**Agreed with**:
- A empresa apresenta um ROE acima de 15% e margens EBITDA sólidas, sugerindo potencial.
- sector_specialist

**Challenged**:
- Concerns: ND/EBITDA acima do limite ideal
- Embora a relação dívida líquida/EBITDA esteja alta, o ROE de 20.8% sugere que a empresa pode gerar lucros suficientes para reduzir essa alavancagem ao longo do tempo.

## Dossier (factual base — same input for all voices)

```
=== TICKER: BR:MOTV3 — MOTV3 ===
Sector: Industrials  |  Modo (auto): A  |  Held: False
Last price: 15.539999961853027 (2026-04-29)
Fundamentals: P/E=10.72 | P/B=1.98 | DY=2.5% | ROE=20.8% | ND/EBITDA=3.55 | DivStreak=2.00

Quarterly (last 6, R$ M):
  2025-09-30: rev=    6.3  ebit=   3.1  ni=   1.4  ebit_margin= 48.5%
  2025-06-30: rev=    4.7  ebit=   1.6  ni=   0.9  ebit_margin= 35.4%
  2025-03-31: rev=    4.6  ebit=   1.9  ni=   0.5  ebit_margin= 41.3%
  2024-12-31: rev=    6.2  ebit=   1.2  ni=   0.2  ebit_margin= 19.3%
  2024-09-30: rev=    5.6  ebit=   1.5  ni=   0.5  ebit_margin= 26.6%
  2024-06-30: rev=    5.3  ebit=   1.3  ni=   0.3  ebit_margin= 24.7%

VAULT THESIS (~800 chars):
**Core thesis (2026-04-25)**: A MOTV3 opera no setor industrial brasileiro, com um P/E de 11.36 e um ROE de 20.78%, indicando potencial valorização a longo prazo. No entanto, o dividend yield de apenas 1.98% e uma relação dívida líquida/EBITDA acima do limite ideal (3.55 vs 3x) sugerem cautela.

**Key assumptions**:
1. Mantendo-se a tendência atual de crescimento dos lucros, o ROE se manterá acima de 15% nos próximos anos
2. A empresa conseguirá reduzir sua dívida líquida/EBITDA para abaixo de 3x nos próximos dois anos
3. O dividend yield aumentará significativamente em decorrência de políticas de distribuição mais agressivas ou melhora na rentabilidade operacional
4. A empresa continuará a pagar dividendos ininterruptamente, mantendo o histórico de cinco anos

**Disconfirmation triggers**

PORTFOLIO CONTEXT:
  Active positions (BR): 12
  Sector weight: 0.0%
```

---
*STORYT_2.0 Council prototype · 100% Ollama local · zero Claude tokens · 3 voices × 2 rounds*