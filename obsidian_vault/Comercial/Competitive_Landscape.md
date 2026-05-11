---
type: doc
scope: commercial
roadmap_block: B3
created: 2026-05-11
---

# 🗺️ Competitive Landscape — há um buraco no mercado?

> Bloco B3 de [[Comercial/00_Roadmap]]. Constituição: [[CONSTITUTION_Comercial]]. A pergunta que este doc responde: **quem já serve o investidor PF disciplinado de longo prazo (DRIP / Buffett / dividendos), e o que é que nenhum deles faz?**

## A leitura curta
Toda a concorrência cai em dois baldes: **dão-te DADOS** (screeners, fundamentals, fair value) ou **dão-te OPINIÕES** (consenso de analistas, artigos, picks). **Ninguém te dá DISCIPLINA** — ninguém te obriga a escrever como a tua tese morre, ninguém arquiva as tuas decisões e os outcomes, ninguém te mostra o teu padrão de erro. Esse é o nosso wedge. (É exactamente o argumento de [[Bibliotheca/Disciplina_de_Investidor]].)

## Quem está no campo

| Player | Forte em | Fraco em (= o nosso espaço) |
|---|---|---|
| **TipRanks** | consenso de analistas, "smart score", insider/hedge-fund tracking | é a opinião da multidão, não o *teu* processo; nada de tese própria/falsificável; pouco para DRIP/longo prazo |
| **Finviz** | screening rápido, heatmaps, market overview visual | zero profundidade de carteira; zero gestão de tese; sem síntese IA; **só US** |
| **Simply Wall St** | "snowflake" visual de fundamentals, fair value (DCF), tracking de carteira, muitos mercados | o fair value é caixa-preta de método único; sem rastreio de falsificabilidade da tese; sem "o teu padrão de erro"; **cobertura B3 fraca**; leve em dividendos/DRIP |
| **Seeking Alpha** | foco em dividendos (Dividend Grades), Quant Ratings, muita opinião | signal-to-noise péssimo (é content farm); sem camada de disciplina pessoal; sem gestão de tese; **US-cêntrico** |
| **Suno / XP / BTG (BR)** | research BR-nativo profissional, carteiras recomendadas | é a tese *deles* num PDF que lês passivamente; sem ferramentas; sem analytics de carteira; **sem US** |
| **Motley Fool** | enquadramento de longo prazo, picks de convicção | são *picks*, não processo; sem ferramentas; tom hype-y; **só US** |
| **Bloomberg / FactSet** | tudo, institucional | $$$$, irrelevante para retail |

## O buraco (o nosso wedge)
Ninguém, hoje, faz **tudo isto junto**:
1. **Obriga a falsificar a tese** — escreves os pilares, os riscos que a invalidam e o **gatilho de saída no momento da compra**, e o sistema persegue a evidência *contra*.
2. **Arquiva decisões + outcomes** — calibração: descobres que sobrestimas sistematicamente o impacto de earnings, ou que os teus "catalisadores" raramente movem o preço.
3. **Mostra o teu padrão de erro** ao longo do tempo — o verdict history exposto, incluindo os erros.
4. **BR + US num só sítio**, moedas isoladas, mesma filosofia, fontes nativas dos dois (CVM/B3/Status Invest/fiis.com.br + SEC EDGAR/yfinance).
5. **In-house** (SQL/Ollama) — a profundidade não custa uma fortuna por query → preço competitivo.

**Posicionamento de uma linha**: *"os outros dizem-te o que está a acontecer; nós tornamos-te um melhor tomador de decisões."* O moat não é o screener (qualquer um faz `P/E < 20`) — é o **scaffold de disciplina**.

## Vantagens injustas que já temos
- Cobertura **BR + US** real, com fontes nativas (a maioria da concorrência é US-only ou BR-only).
- **LLM in-house** (custo marginal ≈ 0 nas features que não tocam Claude API) → margem que a concorrência API-dependente não tem. Ver [[Comercial/Pricing]].
- Arquitectura de **perpetuums / agentes** + 184 tickers já cobertos + knowledge base RAG (Damodaran/Dalio) + RI knowledge base CVM oficial — anos de trabalho que não se replicam num fim-de-semana.
- Os 10 hábitos de [[Bibliotheca/Disciplina_de_Investidor]] já destilados e prontos a virar features.

## Ameaças (honestidade)
- Simply Wall St podia acrescentar gestão de tese; uma startup LLM-native podia atacar o mesmo ângulo; os data providers podiam descer de gama.
- Mitigação: o ângulo "disciplina-como-produto" é genuinamente mal-servido *hoje*, e o nosso BR-depth + in-house cost são difíceis de copiar à pressa. Mas não é um moat eterno — a janela importa.

## O que isto desbloqueia
Com este mapa escrito (em vez de uma intuição), as próximas decisões comerciais argumentam-se a partir de uma posição, não de um palpite: [[Comercial/Pricing]] (o que cobrar e a quem), [[Comercial/GTM]] (como chegar a esse cliente), e o `report tier` do bloco B4 (porque é que um cliente paga pelo "teatro" — porque a substância por baixo é a disciplina que nenhum concorrente tem).
