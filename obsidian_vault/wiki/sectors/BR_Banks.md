---
type: sector
name: BR Banks
region: BR
tags: [sector, banks, financials, br]
related: ["[[Graham_Number]]", "[[P_E_interpretation]]", "[[P_B_interpretation]]", "[[Selic]]", "[[CDI]]"]
holdings: ["[[BBAS3]]", "[[ITUB4]]", "[[SANB11]]", "[[BPAC11]]", "[[BBSE3]]"]
---

# 🏦 Setor: Bancos BR

## Por que Bancos precisam de scoring separado

Estrutura de capital **incomparável** com uma empresa industrial:

- Ativo = depósitos + funding → alavancagem 8-12× é normal (vs ≤2× industrial).
- Receita = NII (spread ativos-passivos) + tarifas + seguros — não comparável a "margem EBITDA".
- Valor contábil é o cerne da tese (equity é colchão contra default).

Por isso em `scoring/engine.py::score_br_bank`:
- ❌ Graham Number (EPS × BVPS não aplica — equity alavancado)
- ❌ Net Debt / EBITDA (bancos têm liability, não debt operacional)
- ✅ P/E ≤ 10, P/B ≤ 1.5, DY ≥ 6%, ROE ≥ 12%, dividend streak ≥ 5y

## Taxonomia competitiva (2026)

| Tier | Nome | Foco | ROE típico |
|---|---|---|---|
| Big 5 | [[ITUB4]], BBDC4, [[BBAS3]], [[SANB11]], CAIXA | varejo massivo + corporate | 15-20% |
| Boutique | [[BPAC11]] (BTG), XP | investment banking + wealth | 18-25% |
| Digital | Nubank, Inter | retail low-cost, tech | 12-25% (escala recente) |
| Regional | ABCB4 (Daycoval), Banrisul | nicho / estado | 8-14% |
| Seguradora | [[BBSE3]], Caixa Seguridade, [[PSSA3]] | insurance float | 18-22% |

## Drivers de resultado

### 1. [[Selic]] (mais importante)
- Selic ↑ → spread ↑ (primeiro movimento) → mas inadimplência ↑ 12-18m depois → créditos provisionados → lucro ↓.
- **Peak bank earnings tipicamente ocorre ~12m depois do pico Selic** (efeito 2023 → 2024).
- Selic ↓ → spread ↓ imediato → inadimplência ↓ com delay → lucro neutro-a-positivo se crescimento carteira suficiente.

### 2. Inadimplência (NPL)
- Ciclos 3-5 anos. NPL > 90d é o indicador-chave.
- Cartão de crédito é o primeiro a quebrar (unsecured, juros 300%+).
- **Watch**: provisões crescendo enquanto inadimplência estável = banco a "limpar" o balanço (preparar ciclo).

### 3. Competição fintech
- Nubank (NU @ NYSE) + Inter roubaram CDB e cartão de pessoa física.
- Big 5 respondeu com franchising + buy (ITUB → ITI, BB → Digio).
- **BPAC11** é imune (foca alta renda + institucional).

### 4. [[IPCA]] / regulação
- Basel III/IV capital requirements — Bacen conservador.
- JCP (Juros sobre Capital Próprio) é vantagem fiscal BR-only — bancos pagam via JCP, dedutível no lucro (economia IR 34%).

## Métricas-chave

| Métrica | Fórmula | Bom |
|---|---|---|
| ROE | Lucro líq / PL médio | ≥ 15% |
| P/B | Preço / BVPS | ≤ 1.5 (Graham) |
| P/E | Preço / EPS | ≤ 10 |
| Cost-to-income | Opex / (NII + tarifas) | ≤ 45% |
| NPL 90d | Créditos vencidos > 90d / Carteira | ≤ 3% |
| Basel ratio | Capital / RWA | ≥ 11% |
| NIM | Net Interest Margin | ≥ 4.5% BR |

## Tese actual BR bancos (2026)

- **Selic ciclo**: terminal alta 2024 → início corte 2025 → 2026 janela favorável a DY (preços reflectem receio margin squeeze, mas inadimplência estabilizando).
- **BBAS3** segue o trade mais clássico (DY 8%+, P/E 5-6, estatal desconto). Risco: interferência política.
- **ITUB4** é o quality (ROE 22%, cobertura 200%). Pagou P/B ~1.8 historicamente justificado.
- **BPAC11** é growth-within-financial (BTG wealth management explodindo BRL AUM).
- **SANB11** recuperou após 2023, spread comprimido mas dividendo de volta.
- **BBSE11** não é banco técnico (holding BB Seguridade) — DY extraordinário mas dependência 100% BB distribution.

## Red flags

- Provisões caem enquanto NPL sobe → balanço a mascarar.
- Banco que para de dar JCP — estrutura fiscal comprometida.
- Payout > 70% consecutivo sem retenção para RWA growth.
- Exposição desproporcional a um setor (agro, real estate, consumo).

## Como integrar ao scoring

```bash
python scoring/engine.py BBAS3 --market br  # aplica score_br_bank automaticamente
```

Universe.yaml classifica `sector: Banks` → engine enrota para bank scoring.

---

> Ver também: [[markets/BR]], [[P_B_interpretation]], [[Dividend_Safety]], [[Selic_history]].
