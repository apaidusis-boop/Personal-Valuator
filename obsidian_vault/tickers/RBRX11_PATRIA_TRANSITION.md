---
type: transition_memo
ticker: RBRX11
market: br
date: 2026-05-08
event: "Pátria acquires RBR Asset FII division (closed 11/Dec/2025)"
status: in_integration
tags: [transition, acquisition, patria, rbr, governance, risk]
related: ["[[RBRX11]]", "[[RBRX11_STORY]]", "[[wiki/holdings/RBRX11]]", "[[KNHF11]]"]
---

# RBRX11 — Memorial da transição Pátria-RBR (Dez/2025)

> Sidecar manual ao auto-gerado [[RBRX11]] (que é reescrito pelo
> `obsidian_bridge` diariamente). Capture de findings 2026-05-08 que **não
> existem na pipeline automática** ainda.

## Timeline canónico

- **11/Dez/2025** — Pátria Investments anuncia compra da divisão FIIs da
  RBR Asset Management. 12 fundos, ~R$ 8B em AuM. Pátria torna-se a
  **maior gestora de FIIs do Brasil** (R$ 38B em real estate).
- Time de gestão RBR é **mantido e integrado** à equipa Pátria.
- **RBRX11 incorpora os activos do RBRF11** (FoF da RBR) ao mesmo tempo da
  transação — não é coincidência.
- Comunicação Pátria sinaliza: "alguns fundos da RBR podem ser incorporados
  a estruturas existentes do Pátria, com possível **troca de ticker, mudança
  de regulamento, ou acesso a estrutura mais robusta**".
- A partir de **2026 o foco passa a ser organizar a casa, consolidar fundos
  e acelerar crescimento orgânico** — fase de M&A integration.

## Sinal de mercado coincidente — saída de cotistas

Da tabela `fii_monthly` (CVM oficial):

| Período (período_end) | Total cotistas | ∆ vs Jun/25 |
|---|---:|---:|
| 2025-06 | 64.199 | (base) |
| 2025-07 | 62.741 | −2,3% |
| 2025-08 | 61.653 | −4,0% |
| 2025-09 | 60.561 | −5,7% |
| 2025-10 | 59.530 | −7,3% |
| 2025-11 | 58.543 | −8,8% |
| 2025-12 | **57.786** | **−9,99%** |

Bleed mensal **consistente** ~1.000 cotistas/mês durante 6 meses. Trigger
[[scripts/trigger_monitor|`fii_cotistas_drop`]] (`rbrx11_cotistas_drop_5_6m`)
**dispara hoje** com este histórico — o evaluator foi adicionado em 2026-05-08
exactamente para fechar esta lacuna.

## Performance recente (XP Lista de FIIs, 2026-04)

- **Mês**: −1,15%
- **3M**: −3,82%
- **12M**: +11,20%

Três meses de retorno negativo coincidentes com o período pós-aquisição.

## Conta a pagar — cotistas + price drift

A questão é se a saída líquida está a **comprimir o preço** ou se o **preço
estável reflete fluxo neutralizado** (gestor recompra, BNDES de FII, etc.).
Dado que P/VP está em ~0.87 (descontado vs VPA R$ 9.86), o mercado parece
estar precificando algum desconto de governança / integração.

## Implicações para a tese de holding

1. A tese auto-gerada do council (BUY high, 30/Abr/2026) **não tinha este
   contexto**. Foi baseada em fundamentals frios (DY 12.5%, P/VP 0.87,
   streak 5y) e ignorou o catalyst negativo recente.
2. Os IC personas do council (Buffett-style) têm bias estrutural de "boa
   tese ao P/VP barato + DY alto" e podem estar a **subestimar risco
   de governança** durante a integração.
3. **Lourdes Aluguel** (FII specialist) também não flagou — provavelmente
   porque o auto_draft synthesizer não tinha acesso ao news angle.

## Próximas acções

- [ ] Vigiar fatos relevantes CVM da RBRX11 nos próximos 6 meses para
      avisos de assembleia, alterações de regulamento ou consolidação
      de fundos. Monitor wired em `monitors/cvm_monitor.py`.
- [ ] Re-correr council story RBRX11 com prompt enriquecido
      ("Pátria-RBR transition Dec/2025") para forçar o debate a considerar
      o catalyst.
- [ ] Adicionar trigger paralelo `rbrx11_price_below_8` se o user decidir
      que P/V abaixo de 8,00 é entry zone (actualmente em 8,70-8,80).
- [ ] Comparar com cohort RBR irmãos: RBRP11, RBRL11, RBRR11 (todos
      transferidos à Pátria) — se os irmãos não tiveram saída de cotistas,
      o RBRX11 é idiosyncratic; se tiveram, é Pátria-effect.

## Decisão actual (não automatizar)

Migração total para [[KNHF11]] **defensável mas prematura** sem:

1. Comparar trajectória de cotistas pós-aquisição entre **RBRX11 e cohort
   RBR irmãos** (isolar idiosyncratic vs sistémico).
2. Ler 1-2 fatos relevantes CVM RBRX11 publicados desde Dez/2025 para
   verificar se há comunicação de mudança de regulamento.
3. Validar `fii_fundamentals` KNHF11 após pipeline incluir.

**Recomendação interim**: manter posição actual (2.000 cotas), **não adicionar
mais**, e considerar migração parcial (50%) se nos próximos 60-90 dias
emergir comunicação concreta de mudança de regulamento ou consolidação.

## Sources

- [Patria compra RBR — fiis.com.br](https://fiis.com.br/noticias/fundos-imobiliarios-patria-compra-rbr/)
- [Pátria compra 12 FIIs e torna-se maior gestora do Brasil — BrFiis](https://brfiis.com.br/artigos/patria-compra-12-fundos-imobiliarios-da-rbr-e-se-torna-a-maior-gestora-de-fiis-do-brasil)
- [Patria adquire fundos listados da RBR — NeoFeed](https://neofeed.com.br/negocios/patria-adquire-fundos-listados-da-rbr-incorpora-r-8-bilhoes-e-chega-a-r-38-bilhoes-em-real-estate-no-brasil/)
- [Patria adquire RBR Gestão — Money Times](https://www.moneytimes.com.br/patria-adquire-rbr-gestao-e-incorpora-12-fundos-imobiliarios-fiis-ao-portfolio-veja-os-detalhes-igdl/)
- `data/br_investments.db::fii_monthly` — total_cotistas Jun-Dez/2025

---
*Sidecar criado 2026-05-08. Não regenerado por bridges automáticos.*

## 🎙️ Recent insights & mentions

_Auto-gerado · 2026-05-10 20:39 UTC · yt=0 · analyst=1 · themes=0_

### 📰 Analyst reports (últimos 120d)

| Data | Fonte | Kind | Stance | PT | Claim |
|---|---|---|---|---:|---|
| 2026-04-24 | XP | thesis | bull | — | RBR Plus Multiestratégia Real Estate é destacado por sua posição em hedge funds. |

