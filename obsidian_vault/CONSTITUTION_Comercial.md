---
type: constitution
scope: commercial
parent: "[[CONSTITUTION]]"
status: blueprint
created: 2026-05-11
---

# 📜 Constituição — Mundo Comercial

> **Herda tudo de [[CONSTITUTION]]** (núcleo partilhado) e de [[Bibliotheca/Disciplina_de_Investidor]] — onde os 10 hábitos deixam de ser "régua interna dos agentes" e passam a ser **promessa de produto**. Aqui ficam as regras que só fazem sentido quando há clientes.
>
> **Estado: `blueprint`** — *nada disto está construído*. É a constituição do produto *quando* (e *se*) ele existir. Workspace: [[Comercial/_Index]]. Mesma filosofia do [[CONSTITUTION_Pessoal|Mundo Pessoal]]; governança separada.

## Identidade
Este mundo = **um produto para investidores pessoa física** (BR + US, longo prazo, DRIP / Buffett). Não é robo-advisor, não é corretora, não dá ordens. É uma **ferramenta de disciplina de research** — a parte que falta no retail: TipRanks / Finviz / Simply Wall St / Seeking Alpha dão *números*; nós damos o *processo que obriga a pensar como investidor* (escrever como a tese morre, arquivar os próprios erros, ver onde se erra sistematicamente).

## Não-negociáveis do Mundo Comercial

1. **Not financial advice** — toda saída para cliente é educacional / ferramenta. Disclaimers obrigatórios e visíveis. Nunca "compra X agora" sem o *porquê* e sem disclaimer. Nunca executar ordens. Nunca prometer ou implicar retorno.

2. **In-house first vira modelo de negócio** — no Pessoal "in-house first" é eficiência; aqui é margem. Cada request de cliente que toca a Claude API tem custo marginal real → SQL puro / Ollama local / cache TTL agressivo são a vantagem de custo sobre concorrentes que queimam API por request. Claude API só onde há texto não-estruturado a interpretar e o valor justifica.

3. **O "teatro" é um *tier de entrega*, não a substância** — relatórios longos no formato institucional (initiating-coverage ~10p, earnings-update ~8p, com tabelas old→new, charts, secção de fontes com links) são uma **camada de apresentação** gerada a partir da mesma análise comprimida do núcleo — não nova análise, não enchimento. A disciplina dos 10 hábitos garante que o tier longo tem substância. **Tier 1** = denso / acionável ("compro/mantenho/vendo?"); **Tier 2** = o mesmo, embrulhado para quem quer ver um relatório.

4. **A disciplina embutida é o moat** — não competimos em "screening" (qualquer um faz P/E < 20). Competimos em obrigar o utilizador a (a) escrever as condições de morte da tese antes de comprar, (b) arquivar decisões e outcomes, (c) ver o seu próprio padrão de erro (sobrestima earnings? "catalisadores" não movem preço?). Features que diluem isto — só dar números, esconder o "porquê", deixar a tese sem gatilho de saída — estão **fora de escopo**.

5. **Paper-trade gate vira feature de confiança** — um signal novo não é apresentado ao cliente como "acionável" sem track record (≥30 closed, win_rate > 60%); até lá é rotulado experimental. Transparência sobre o que ainda não se provou.

6. **Honestidade > marketing** — projecções conservadoras (damper quando histórico >> Gordon) mesmo que "vendam" pior. Mostrar incerteza (bandas de fair value, confiança de dados). Expor o verdict history (incluindo os erros). Backtests nunca apresentados como promessas.

7. **Licenciamento de dados respeitado** — base = público (yfinance / SEC EDGAR / CVM / Status Invest / fiis.com.br). Data providers premium (FactSet / Daloopa / Morningstar / Moody's / S&P / PitchBook / …) só com contrato. Nunca redistribuir dados de terceiros fora dos termos.

8. **Isolamento de tenant + de carteira** — dados de um cliente nunca tocam outro. Dentro de um cliente, BR/US isolados (mesmo princípio nº2 do núcleo). LGPD / GDPR para dados de utilizador.

## O que este mundo NUNCA shipará
- Auto-trading / execução de ordens.
- "Compra / vende isto agora" sem disclaimer e sem o "porquê".
- Garantias ou insinuações de retorno; backtests vendidos como promessas.
- Vender, partilhar ou expor dados de utilizadores.
- Esconder a metodologia — a transparência *é* o produto.

## Onde se decide o resto (roadmap / produto, não constituição)
MVP · telas · IA em camadas · stack (SQLite → Postgres se multi-user) · pricing · GTM · competitive landscape · compliance jurisdicional →
- [[Comercial/Personal_Investment_OS_Blueprint|Investment OS Blueprint]] (movido de Bibliotheca, 2026-05-11)
- [[Comercial/00_Roadmap]] (blocos B1…B6) — B6 (infra multi-tenant) só com decisão explícita de comercializar **+** ≥90d de verdicts validados (~Ago/2026; ver Phase GG em [[ROADMAP]]).

## Cross-links
- Núcleo partilhado: [[CONSTITUTION]] · disciplina (régua → promessa): [[Bibliotheca/Disciplina_de_Investidor]]
- Mundo Pessoal: [[CONSTITUTION_Pessoal]]
- Index do mundo: [[Comercial/_Index]] · roadmap: [[Comercial/00_Roadmap]]
