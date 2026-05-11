---
type: doc
scope: commercial
roadmap_block: B3
created: 2026-05-11
---

# 💰 Pricing — o que cobrar, a quem, e se cobre o custo

> Bloco B3 de [[Comercial/00_Roadmap]]. Constituição: [[CONSTITUTION_Comercial]] (nº2: in-house-first vira modelo de negócio; nº3: o "teatro" é um tier). A pergunta: **o que é grátis, o que é pago, e a margem fecha?**

## A insight central: dois baldes de custo
Cada feature do sistema cai num de dois baldes — e isto **decide** a estrutura de tiers:

**Balde A — custo marginal ≈ 0** (SQL local / Ollama / cache TTL): screening BR+US, ficha de fundamentals do ticker, gráficos de preço, tracking de carteira, drift/rebalance, glossário, regime macro, percentis vs peers, alertas CVM/SEC/preço, dividend calendar. → podem ser **generosos** no tier grátis/barato; servir mais utilizadores destas features quase não custa nada.

**Balde B — custo marginal > 0** (Claude API ou compute pesado por request): o deep-dive dossier (síntese Strategist ~5k palavras), o `report tier` institucional (bloco B4), web research ao vivo (Tavily), debate IC on-demand. → **gated** a tiers pagos e/ou com limite de uso metered.

**Consequência estratégica**: o roadmap de produto = "empurrar features para baixo na pilha de custo". Cada feature que conseguimos servir de SQL/Ollama em vez de Claude API cai direto na margem bruta. *In-house-first não é só uma regra técnica — é o motor de margem.*

## Tiers propostos (ilustrativo — números a calibrar com mercado)

| Tier | Para quem | O que inclui | Custo p/ nós | Função |
|---|---|---|---|---|
| **Free** | quem está a avaliar | screening BR+US · **1 ticker** acompanhado com ficha completa + verdict · glossário · digest semanal por email | ~zero (balde A) | aquisição + provar valor |
| **Plus** (~R$15-25 / ~$8-15/mês) | o investidor disciplinado típico | **carteira completa** (BR+US, moedas isoladas) + drift/rebalance · **todas as fichas de ticker** · **gestor de tese** (a camada de disciplina: escrever como a tese morre, gatilhos de saída, scorecard de pilares) · dividend calendar · alertas (CVM/SEC/preço) · regime macro | ainda balde A na maioria | **o produto core** — o scaffold de disciplina |
| **Pro** (~R$40-60 / ~$25-40/mês) | power users | tudo do Plus **+** deep-dive dossiers IA (N/mês incluídos, depois metered) + `report tier` institucional (B4) + memos com web research + **decision journal + analytics de calibração** ("o teu padrão de erro") + prioridade em features novas | balde B real → **metered** | monetizar a profundidade IA |
| **(futuro) Team/Pro+** | só pós-B6 | multi-carteira, partilha, API | infra multi-tenant | só com "go" comercial |

## Filosofia de pricing
- **Nunca cobrar pelos dados** — são quase todos públicos (yfinance/SEC/CVM/Status Invest). Cobramos pela **disciplina + síntese + a vista consolidada BR+US** que ninguém mais dá.
- **Free generoso, Pro metered** — o tier grátis pode ser generoso *porque* o balde A é barato; o Pro tem limite de dossiers/mês *porque* o balde B custa de verdade.
- **O Plus é onde está o produto** — não é "freemium para empurrar Pro"; o Plus (a camada de disciplina) é a razão de existir. O Pro é o "+IA pesada para quem quer".
- **Transparência de custo** — features que tocam Claude API podem ser rotuladas como tal ("este dossier usa IA avançada — X/Y restantes este mês"); educa o utilizador e gere expectativa.

## Âncoras de mercado
Simply Wall St ~$10/mês · Seeking Alpha Premium ~$240/ano (~$20/mês) · Suno ~R$30-50/mês · Motley Fool ~$199/ano · Finviz Elite ~$40/mês. → o nosso **Plus** senta-se em $8-15/mês (abaixo do SA Premium, na zona do SWS) e o **Pro** em $25-40/mês — competitivo, **com base de custo mais baixa** do que a concorrência API-dependente (essa é a vantagem estrutural).

## Riscos / questões em aberto
- BRL vs USD pricing — o cliente BR não paga preço-US; provavelmente dois price books (consistente com a regra de carteiras isoladas).
- Annual vs monthly — desconto anual padrão (12→10x) para retenção.
- O custo real por dossier (tokens × preço Opus/Sonnet) define o limite do Pro — calcular antes de fixar o número (TODO quando B4 tiver protótipo).
- Free tier abuse (criar contas para 1-ticker × N) — limitar por email/device; não crítico no início.

## O que isto desbloqueia
Antes: não sabíamos se uma feature dava lucro. Agora: cada feature está taggeada por balde de custo → da próxima vez que adicionarmos algo (ex: os 5 picks de disciplina, ou o report tier), sabemos *de imediato* em que tier entra e se precisa de metering. E o [[Comercial/GTM]] pode desenhar o funil (Free → Plus → Pro) com a economia já clara.
