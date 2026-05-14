---
type: migration_analysis
held_before: RBRX11
held_now: KNHF11
market: br
date: 2026-05-08
stance: EXECUTED
confidence: medium
executed_at: 2026-05-08T10:48
tags: [migration, fii, kinea, patria, rbr, executed]
---

# RBRX11 (Pátria) → KNHF11 (Kinea) — migração EXECUTADA

**Status**: ✅ **EXECUTADA** — 2026-05-08 10h48 (full swap, não faseado)
**Decisão do user**: full migration em vez do faseamento 50/50 que eu havia recomendado
**Confiança ex-ante**: média (LEAN MIGRATE) — registado para retrospectiva

## Execução real (broker print)

| | Operação | Preço | Qty | Total |
|---|---|---|---|---|
| RBRX11 | **Venda** | R$ 8.70 | 2,000 | R$ 17,400.40 |
| KNHF11 | **Compra** | R$ 98.56 | 175 | R$ 17,247.62 |
| **Cash residual** | | | | **R$ 152.78** (pre-IR) |

### Realized P&L RBRX11 (após 2026-04-24 entry @ R$8.48)

- Cost basis: R$ 16,960.00 (2,000 × R$8.48)
- Proceeds:   R$ 17,400.00 (2,000 × R$8.70)
- Gross gain: **+R$ 440.00**
- IR FII 20%: R$ 88.00 (devida — FII tributa ganho de capital a 20%)
- **Net gain: +R$ 352.00**
- Cash net (após IR): R$ 152.78 − R$ 88.00 = **R$ 64.78**

> Plus 12 meses × R$0.09 × 2,000 = R$ 2,160 de proventos isentos colhidos durante o holding period (não entram no cálculo de P&L de capital).

### DB updates aplicados (`data/br_investments.db`)

- `portfolio_positions` RBRX11 (entry 2026-05-07): `active=0, exit_date=2026-05-08, exit_price=8.70`
- `portfolio_positions` KNHF11: nova linha `entry_date=2026-05-08, entry_price=98.56, qty=175, active=1`
- `companies.is_holding`: KNHF11 → 1, RBRX11 → 0

---

## Análise ex-ante (preservada para retrospectiva)

**Stance que dei**: 🟢 **LEAN MIGRATE faseado** (50% agora, 50% em 8 semanas)
**O que o user fez**: full migration imediata
**Diff**: o user removeu optionality que eu sugeri preservar. Razoável se a convicção era alta — no extremo o faseamento é só uma regra de "não vendas no fundo" que pesa pouco quando a tese qualitativa é forte. Registar e medir nos próximos 8 semanas qual foi a melhor escolha.

---

## Resumo executivo (1 parágrafo)

Mantemos RBRX11 desde antes da venda da divisão FIIs da RBR à Pátria (Dez/2025). O fundo já foi formalmente renomeado **Pátria Plus Multiestratégia Real Estate FII**, e a Pátria comunicou um *reposicionamento estratégico* — redução de tijolo performado, prioridade a CRIs. O fundo passa portanto a competir, na prática, num espaço onde o **KNHF11 (Kinea Hedge Fund)** já está estabelecido, com gestor mais sénior, *track record* mais longo, e mandato híbrido análogo (CRI + tijolo + cotas FII). Para mesmo capital deployed, ambos pagam DY ~12% mensal isento; a renda mensal ficaria praticamente igual (~R$2,124 vs R$2,160). **A migração troca risco de transição de gestor por exposição a um fundo já estabilizado**, com modesto sacrifício de yield.

---

## Side-by-side

| | **RBRX11** (held) | **KNHF11** (candidate) |
|---|---|---|
| Nome legal (2026) | Pátria Plus Multiestratégia Real Estate FII | Kinea Hedge Fund FII |
| Gestor | **Pátria Investments** (post-Dez/25) | **Kinea** (Itaú Unibanco) |
| Mandato | Híbrido — pivotando p/ CRI | Híbrido multi-strategy |
| Sector na DB | Híbrido | Híbrido |
| Preço (2026-05-07) | R$ 8.70 | R$ 98.39 |
| Market cap | R$ 989M | R$ 1,935M (~2× maior) |
| DY trailing 12m | ~12.5% | ~11.2–12.0% |
| Distribuição | R$ 0.09/cota/mês (9 meses estável) | R$ 1.00/cota/mês (12 meses estável) |
| Carry alvo | ~1.05% mensal | ~91–99% CDI bruto isento |
| P/VP | n/d (DB sem book) | ~0.93–0.94 (~6–8% deságio) |
| Streak dividendos | 5 anos | 4 anos |
| Alocação CRI | em transição (subindo) | 63.6% (Jun/25) |
| Alocação tijolo | em redução | 29.2% (prime SP) |
| Alocação FII | parte mantida | 13.5% |
| Duration crédito | n/d | ~2.9 anos (positivo p/ ciclo de corte Selic) |
| Risco material 2026 | mudança regulamento, possível troca ticker, integração Pátria; cotistas −8% Jul→Dez/25 | resgates secundário; CRI inadimplência idiossincrática |

> Fontes: `companies` + `fundamentals` + `prices` + `dividends` (DB local), Kinea, fiis.pro, Funds Explorer, statusinvest, Patria Real Estate, Visão do Mercado (Substack), XP Investimentos. Detalhe nas _Sources_ ao fundo.

---

## Renda anual equivalente (mesmo capital)

Migrar R$17,400 (2,000 cotas RBRX11) → ~177 cotas KNHF11 @ R$98.39:

| Cenário | Renda anual | Yield efectivo |
|---|---|---|
| **Manter RBRX11** | R$ 2,160 | 12.41% |
| **Migrar para KNHF11** | R$ 2,124 | 12.20% |
| Δ | **−R$ 36/ano (−1.7%)** | −0.21 pp |

**Custo da migração em renda é ruído**. Decisão é qualitativa, não numérica.

---

## Argumentos a favor da migração (LEAN MIGRATE)

1. **Gestor superior**. Kinea tem track record de 15+ anos em FIIs (KNRI11, KNCR11, KNHY11), todos referência no segmento. Pátria assume os FIIs RBR em fase de M&A integration onde "consolidar fundos" e "possível troca de ticker" estão em cima da mesa (memory `rbrx11_patria_acquisition.md`).
2. **Cotistas a fugir**. RBRX11 perdeu **−8% de cotistas Jul→Dez/2025** (62.7k → 57.8k segundo CVM `fii_monthly`). Mercado já está votando com os pés. Não é o sinal que se quer estar do lado errado.
3. **KNHF11 tem opcionalidade**. Carteira hoje 63% CRI + 29% tijolo prime SP + 13.5% FII. Kinea pode rotacionar de crédito para tijolo conforme cap rates comprimem no ciclo de corte de Selic — captura ganho de capital além do carry. Pátria está a fazer o movimento *contrário* (saindo de tijolo, entrando em CRI), o que é razoável mas perde a optionality dos dois lados.
4. **Mandato declarado vs em transição**. KNHF11 já está estabilizado na sua estratégia. RBRX11/Pátria está a meio da transição — assembleia, possível regulamento novo, possível troca de ticker. *Risco operacional ≠ zero*.
5. **DY similar, escala 2×**. KNHF11 R$1.93B vs RBRX11 R$989M — fundo maior com mais liquidez, menor risco de bid/ask spread alargado em momentos de stress.

## Argumentos contra (HOLD position)

1. **DY ligeiramente maior em RBRX11** (12.5% vs 12.2%). Marginal mas real.
2. **Streak maior** — RBRX11 com 5 anos de pagamento ininterrupto vs 4 de KNHF11.
3. **Custo fiscal e operacional**. Vender 2,000 RBRX11 e comprar ~177 KNHF11 implica corretagem (provavelmente zero na XP), mas há efeito spread de mercado e o spread bid/ask tende a estar alargado em RBRX11 dado o fluxo de saídas.
4. **A transição já foi precificada**. Cotação RBRX11 caiu durante Jul-Dez/2025; em R$8.70 hoje pode já reflectir maior parte do risco. Migrar agora é "vender no fundo".
5. **Pátria não é gestor mau**. R$38B em real estate AuM pós-aquisição → maior gestora de FIIs do Brasil. A integração pode até melhorar processos.

---

## Sinais para reforçar a decisão (data-driven)

Para virar *LEAN MIGRATE → MIGRATE*, vigiar:
- [ ] Fato relevante CVM RBRX11 com convocatória de assembleia para mudança de regulamento ou troca de ticker → migração imediata.
- [ ] Cotistas RBRX11 continuar caindo no `fii_monthly` Jan-Mai/2026 → tendência confirmada.
- [ ] DY KNHF11 manter R$1.00/cota/mês por +3 meses (até Ago/2026) → carry comprovadamente sustentável no novo regime.
- [ ] P/VP KNHF11 ≤0.95 mantido → entry com colchão de valor.

Para virar *LEAN MIGRATE → HOLD*, vigiar:
- [ ] Pátria publicar carta com plano de gestão claro e *não* mexer em ticker/regulamento.
- [ ] Cotistas RBRX11 estabilizarem ou recuperarem.
- [ ] DY RBRX11 subir acima de R$0.10/cota (sinalizando reposicionamento eficaz).

---

## Open questions (não resolvidas neste documento)

1. **Posso vender RBRX11 sem prejuízo fiscal material?** R$8.70 vs entry R$8.48 → ganho de R$440 (R$0.22 × 2000). Como FII, ganho é tributado a 20%, mas se vender em prejuízo (não é o caso) seria carry-forward. Verificar no `portfolio_positions` o histórico exacto de aquisições antes de executar.
2. **KNHF11 está em janela de subscrição em 2026?** Algumas Kineas abrem novas emissões periodicamente. Comprar via primária com desconto vs secundária pode mudar o cálculo.
3. **Existe peer melhor que ambos?** KNHY11 (Kinea High Yield) entregou DY 13.43% últimos 12m e R$1.10/cota Mar/2026 — yield superior a ambos. Worth considering como terceira via, mas mandato é só CRI (sem optionality de tijolo/FII).
4. **Concentração Kinea**. User já tem outras posições Kinea? Verificar no portfolio para evitar concentração no mesmo gestor.

---

## Recomendação operacional (ex-ante, NÃO seguida)

**LEAN MIGRATE com execução faseada**, _não all-in num dia_:

- Sprint 1 (próximas 2 semanas): vender 50% da posição RBRX11 (1,000 cotas → ~R$8,700). Comprar ~88 cotas KNHF11. Manter outras 1,000 RBRX11 para observar a integração Pátria.
- Sprint 2 (8 semanas depois): se sinais de reforço migração persistirem (ver _Sinais_ acima), liquidar restante. Se Pátria estabilizar e dividends manterem, parar e re-avaliar.

Este faseamento limita o risco de "vender no fundo" e dá optionality. Se tudo correr bem com a Pátria, perdemos só ~R$18/ano em renda da metade migrada — perfeitamente comportável.

> **Decisão real do user**: full swap imediato em 2026-05-08 10h48. Ver topo do dossier — registado para retrospectiva.

## Acompanhamento pós-trade (next 8 semanas)

Para validar/invalidar a decisão de full swap:

- [ ] **Renda KNHF11 mantém R$1.00/cota/mês** (Mai/Jun/Jul/Ago) → tese carry confirmada.
- [ ] **Cotação RBRX11 NÃO sobe muito** (>R$9.20) → "vender no fundo" não se materializou.
- [ ] **Pátria publica fato relevante de mudança regulamento/ticker** → migração foi a leitura certa.
- [ ] **KNHF11 P/VP comprime mais** (<0.92) → entrámos um pouco caros, registar para próximas oportunidades.
- [ ] **DY KNHF11 12m mantém ≥11.5%** → carry sustentável no novo regime de Selic.

---

## Sources

- [KNHF11 — Kinea Hedge Fund (página oficial)](https://www.kinea.com.br/fundos/fundo-imobiliario-kinea-hedge-fund-knhf11/)
- [KNHF11 dividendos · statusinvest](https://statusinvest.com.br/fundos-imobiliarios/knhf11)
- [KNHF11 · Investidor10](https://investidor10.com.br/fiis/knhf11/)
- [KNHF11 · Funds Explorer](https://www.fundsexplorer.com.br/funds/knhf11)
- [KNHF11 · fiis.pro](https://www.fiis.pro/funds/KNHF11)
- [KNHF11 · Expert XP](https://conteudos.xpi.com.br/fundos-imobiliarios/kinea-hedge-fund-fii-knhf11/)
- [KNHF11: por que ele é um cavalo certo para o ciclo de queda de juros · Visão do Mercado](https://visaodomercado.substack.com/p/knhf11-kinea-hedge-fund-fii-por-que)
- [Patria assume FIIs RBRX11, RBRY11 e RBRP11 · statusinvest](https://statusinvest.com.br/noticias/patria-assume-gestao-fiis-rbrx11-rbry11-rbrp11/)
- [RBRX11 (Pátria Plus Multiestratégia Real Estate FII) · Patria Real Estate](https://realestate.patria.com/papel/rbrx11/)
- [Próximos passos na incorporação do RBRF11 pelo RBRX11 · XP](https://conteudos.xpi.com.br/fundos-imobiliarios/relatorios/proximos-passos-na-incorporacao-do-rbrf11-pelo-rbrx11/)
- [RBRX11 paga R$ 0,09 e foca CRIs · statusinvest](https://statusinvest.com.br/noticias/rbrx11-paga-0-09-e-foca-cris-abril-2026/)
- Local: `data/br_investments.db` (companies, fundamentals, prices, dividends)
- Memory: `rbrx11_patria_acquisition.md` (timeline canónico Pátria-RBR Dez/2025)
