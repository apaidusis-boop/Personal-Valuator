# Manual de Direção — falar com o sistema em linguagem de investidor

> 2026-05-11. Pedido teu: *"uma linguagem não coder, mais investimentos e fundamentos, para poder te direcionar melhor."*
> Este doc é a **ponte**. O código vive onde vive — tu diriges a partir daqui. Nenhum termo técnico fica sem tradução.
>
> Companheiros: [[Bibliotheca/Disciplina_de_Investidor]] (a régua de mentalidade) · [[Bibliotheca/_Index]] (hub) · `obsidian_vault/Glossary/` (glossário a sério) · [[CONSTITUTION_Pessoal]] (os não-negociáveis).

---

## 1. O que este sistema é, numa frase

É um **analista de research pessoal**, sempre ligado, que segue ~130 empresas (a tua carteira real BR+US + uma watchlist), lê os resultados e os fatos relevantes mal saem, mede a qualidade e o preço justo de cada uma, e te diz **onde a margem de segurança está** — na filosofia Buffett/Graham, com viés para dividendos consistentes e reinvestimento (DRIP). Não negoceia sozinho. Não converte moeda entre as tuas contas. Propõe; tu decides.

## 2. As três perguntas que ele responde

| Pergunta de investidor | Como pedir | O que recebes |
|---|---|---|
| *"Quanto vale esta empresa?"* | `ii fv TICKER` ou está dentro do deepdive | Preço justo conservador (nosso) + preço atual + consenso de analistas |
| *"Compro, seguro ou vendo?"* | `ii verdict TICKER` (rápido) · `ii deepdive TICKER` (dossiê 5 mil palavras) | Veredito BUY/HOLD/SELL com o raciocínio e os "portões" aplicados |
| *"Para onde vai o próximo aporte?"* | `ii rebalance --cash-add 5000` (BR) · `ii rebalance --cash-add 500` lado US | Trades concretos respeitando a tua alocação-alvo, o macro, e a saúde de cada tese |

(Tudo isto também responde no chat livre do Antonio Carlos — Telegram ou o widget 🐙 no Mission Control. Falas como falarias a um analista; ele chama as ferramentas certas.)

---

## 3. O vocabulário das decisões — o que cada coisa quer dizer

> Cada termo: **o que é** (1 frase de investidor) · **porque te importa**.

- **Preço justo / fair value (conservador)** — o teto Buffett-Graham: para um compounder de qualidade, ~20× lucros; para um banco, ~12× lucros; para uma empresa BR, o Número de Graham; para um FII, o valor patrimonial. *Porque te importa*: é deliberadamente exigente — grita "estás a pagar múltiplo rico" muito antes de a empresa estar realmente cara. Não é o valor intrínseco; é a fronteira da disciplina de preço.
- **Preço justo forward (qualidade-aware)** — *novo, 2026-05-11, ainda experimental*: um fluxo de caixa descontado conservador (cresce o lucro 10 anos, desacelera, desconta a ~8,5-9,5%) que **dá crédito ao prémio de qualidade** — um negócio de fosso largo e ROIC durável merece 22-28× porque o fluxo é mais certo *e* cresce. Corre `python -m analytics.fair_value_forward`. *Porque te importa*: é a resposta ao teu desconforto com "KO = SELL −33%" — esse número vinha do teto conservador a ignorar o prémio de marca.
- **Margem de segurança** — o desconto que exigimos sobre o preço justo antes de chamar "compra": 18% para staples/saúde de qualidade, 25-27% para bancos top, 35-42% para cíclicas (mineração/petróleo). Vive em `config/safety_margins.yaml`. *Porque te importa*: é a tua alavanca de "quão exigente quero ser" por sector — sobe a margem e o sistema fica mais paciente.
- **Veredito (BUY / HOLD / SELL / STRONG_BUY / TRIM / N/A)** — onde o preço atual cai vs as faixas: abaixo do "compra com margem" → BUY; entre a margem e o preço justo → HOLD; entre o preço justo e ~15% acima → TRIM; acima disso → SELL; sem fair value aplicável (ETF, tactical) → N/A. *Porque te importa*: **SELL não quer dizer "vende já"** — quer dizer "a este preço a margem de segurança não está aqui; um aporte novo vai para outro lado". Ver §5.
- **Fosso / moat (0-10)** — durabilidade da vantagem competitiva, em quatro sub-notas: poder de preço (margem bruta alta e estável), eficiência de capital (ROIC alto e persistente), pista de reinvestimento (crescimento + conversão de lucro em caixa), durabilidade de escala (margem operacional e recompras). ≥7 forte, 5-7 neutro, <5 fraco. Não se aplica a bancos/holdings/REITs/FIIs. *Porque te importa*: é o que separa "barata" de "barata por uma razão". Se achas que o sistema subestima o fosso de uma empresa, é uma das poucas alavancas que muda o veredito de verdade (§6).
- **Qualidade contábil — três detectores**:
  - **Piotroski F (0-9)** — nove sinais binários de saúde financeira (lucro positivo, caixa positivo, dívida a cair, margem a subir…). ≤3 = fraco → o sistema rebaixa qualquer "compra" para "espera". *Porque te importa*: barata + livros a deteriorar = armadilha.
  - **Altman Z** — probabilidade de aflição financeira. Z baixo = distress → força SELL mesmo que o preço grite compra (foi o que apanhou a TEN). Não se aplica a bancos/REITs.
  - **Beneish M** — oito índices que farejam manipulação de resultados. M ≥ -1,78 = RISCO. Não se aplica a bancos/REITs.
- **Os "portões" (gates)** — ajustes ao veredito *depois* de ele ser calculado, sempre na direção conservadora:
  - **Portão dos intangíveis** — quando >25% dos ativos são goodwill/intangíveis, ou o patrimônio tangível é negativo (KO, PG, JNJ, HD…), o teto sobre o valor patrimonial é pouco fiável → rebaixa SELL/TRIM → HOLD. *(O bug que arranjámos hoje: este portão estava a falhar silenciosamente porque os dados de intangíveis caducavam entre atualizações — agora tem uma lista de salvaguarda + re-popula-se todo dia.)*
  - **Portão de aflição** — Altman/Piotroski como veto (acima).
  - **Portão macro** — consulta o regime económico (expansão/late-cycle/recessão) e o ajuste do sector: numa cíclica no pico, força HOLD.
  - **Portão de confiança de dados** — se as fontes discordam, rebaixa a convicção.
- **Confiança de dados (cross-validated / single-source / disputed)** — quantas fontes independentes concordam no número. *Porque te importa*: um veredito "cross_validated" pesa mais do que um "single_source"; um "disputed" leva caveat no dossiê.
- **Dividend safety score (0-100, forward)** — quão seguro é o dividendo daqui para a frente (payout, FCF cobre, dívida, histórico). *Porque te importa*: numa estratégia DRIP, um corte de dividendo é o pior cenário.
- **Conviction score (0-100)** — nota composta de "quanto deveríamos gostar disto" cruzando qualidade, preço, momentum de tese e dados. Calculada para todo o universo. *Porque te importa*: ranking rápido de candidatos.
- **Payback DRIP** — quantos anos para os dividendos reinvestidos duplicarem o nº de ações, e quantos para recuperares o investido só em caixa de dividendos. `python scripts/drip_projection.py --ticker X --payback`. *Porque te importa*: é a métrica que importa para a tese de longo prazo, mais do que o preço de amanhã.
- **Paper trade vs capital real** — todos os sinais nascem "paper" (simulados). Só viram capital real depois de 30+ sinais fechados com >60% de acerto. *Porque te importa*: o sistema ganha o direito de mexer em dinheiro a sério, não o assume.

---

## 4. Como me dares direção — o que dizes e o que acontece

> A coluna do meio é o que escreves (CLI) **ou** o que dizes ao Antonio Carlos em português corrente. Não precisas de decorar comandos — diz a intenção.

| Se pensas / queres… | Diz / faz | O sistema… |
|---|---|---|
| *"Analisa esta empresa a fundo."* | `ii deepdive TICKER` · ou "faz um deep dive na X" | Roda Auditor (Piotroski+Altman+Beneish+Moat) ‖ Scout (notícias/insiders/short/consenso) → dossiê de ~5 mil palavras em `obsidian_vault/dossiers/TICKER.md` |
| *"Resumo rápido: compro ou não?"* | `ii verdict TICKER` · ou "qual o veredito da X" | Veredito agregado com raciocínio e portões aplicados |
| *"Mostra-me a foto completa."* | `ii panorama TICKER` | Junta veredito + comparação com pares + gatilhos abertos + notas + vídeos + visão de analistas |
| *"Quero seguir uma empresa nova."* | "adiciona TICKER ao universo — watchlist" (ou "para comprar") | Edito `config/universe.yaml` e os fetchers passam a cobri-la. **Edição de tickers nunca é em código — é sempre aí.** |
| *"Acho que o fosso desta empresa é maior do que o sistema vê — porque [marca dominante / rede / custo de troca]."* | Diz-me o porquê | Explico de onde vem a nota de moat; se concordarmos, ajusta-se a nota / abre-se uma nota de tese a registar o argumento. É das poucas coisas que muda o veredito (§6). |
| *"Quero ser mais exigente (ou menos) neste sector."* | "sobe a margem de segurança de [sector] para X%" | Edito `config/safety_margins.yaml`; o "compra com margem" passa a exigir mais desconto. Override por ticker também existe (ex: PVBI11). |
| *"O preço justo desta empresa está errado porque [tem crescimento que vocês não contam / o lucro reportado tem um charge de uma vez]."* | Diz-me o caso concreto | Mostro o método usado (teto conservador) e o forward (DCF). Se o caso for sólido, promove-se o método forward para essa empresa. |
| *"Onde aplico R$ 5.000?"* (BR) / *"… US$ 500?"* (US) | `ii rebalance --cash-add 5000` · ou "tenho 500 dólares, onde meto" | Lê alocação-alvo + drift + macro + saúde das teses → trades concretos. **Respeita o isolamento BR/US — nunca sugere converter entre contas.** |
| *"Quero registar a tese / o motivo de ter esta posição."* | `python scripts/notes_cli.py add TICKER "texto" --tags tese` · ou "anota a tese da X: …" | Grava a nota. **Uma tese a sério tem 3-5 pilares, 3-5 riscos que a invalidam, e um gatilho de saída** ("o que me faria sair") — senão é religião, não tese (Disciplina §4). |
| *"Não quero que vendas X mesmo que o sistema diga SELL."* | "marca X como hold/keep deliberado — motivo: [turnaround / DRIP core]" | Marca-se a posição (override). Já feito para PVBI11 (turnaround) e GREK (tactical). O sistema deixa de sugerir venda. |
| *"O que os agentes propuseram sozinhos enquanto eu não estava?"* | `/perpetuum-review` · ou `python scripts/perpetuum_action_run.py list-open` | Lista as ações que os "perpetuums" (T2+) propuseram com status aberto; aprovas / rejeitas / adias uma a uma. |
| *"Como está o macro? Devo ficar defensivo?"* | `/macro-regime` · ou "em que regime estamos" | Classificador de regime BR+US + implicações sectoriais + notas wiki de macro |
| *"Vamos rebalancear a carteira toda."* | `/rebalance-advisor` · ou `ii rebalance --md` | Drift vs alvo + trades sugeridos, com o relatório legível no vault |
| *"O que mudou desde ontem?"* | `python scripts/daily_diff.py --since 1` · ou "o que mudou hoje" | Diff: novos filings, mudanças de veredito, sinais novos |
| *"Pergunta livre sobre tudo o que sabemos."* | `ii vault "pergunta em PT"` · ou pergunta ao Antonio Carlos | Busca semântica sobre todo o vault + síntese |

**Regra de ouro da direção**: tu dás *direção*, não micro-aprovas. "Avança com X" = ação total — escrevo nas bases de dados, deixo o output no vault para leres depois. Eu não fico bloqueado à espera de "podes?" em coisas que tu já mandaste fazer. (Memória `feedback_dont_block_on_approval`.)

---

## 5. Como ler um output — anatomia de um veredito (exemplo: KO, hoje)

```
KO   modern_compounder_pe20   fair=63.53   our=52.10   cur=78.42   HOLD   [single_source]
     gate: intangibles_ipa=27% — Buffett ceiling unreliable, SELL→HOLD
```

Traduzindo:
- **`fair=63.53`** — o "preço justo consensual" pelo teto Buffett-Graham: lucro por ação × 20. É exigente de propósito.
- **`our=52.10`** — o "compra com margem": preço justo menos 18% (margem de staples). Abaixo disto é compra clara.
- **`cur=78.42`** — preço atual.
- **`HOLD`** — o preço ($78) está acima do preço justo conservador ($63,5), portanto o cálculo cru dizia SELL…
- **`gate: intangibles_ipa=27%...`** — …mas 27% dos ativos da KO são goodwill/marca, e a marca real (~$98B pela Interbrand) **não está no balanço** — então o teto sobre o valor patrimonial está enviesado *baixo* e o sinal SELL não é de confiança. Rebaixou-se para **HOLD**. *Leitura humana*: "a KO não está barata a 22,5× lucros, mas chamar SELL seria forçar; segura-se, não se compra mais a este preço."
- **`[single_source]`** — confiança média (uma fonte). Levaria caveat num dossiê.

E o que falta (porque o teu olho de investidor vê e o engine não, ainda): a KO compõe ~5-6% ao ano com dividendo blindado; um DCF conservador (`fair_value_forward`) dá ~$66 — ainda "ligeiramente rica", mas longe do "SELL −33%". A leitura honesta é **HOLD, esperar abaixo de ~$70**.

---

## 6. As cinco alavancas que mudam o veredito de verdade

Tudo o resto é ruído de afinação. Estas movem o ponteiro:

1. **A nota de fosso (moat)** — se o sistema subestima a vantagem competitiva, sobe a nota → o método forward passa a aplicar-se / a margem efetiva relaxa.
2. **A margem de segurança do sector** (`safety_margins.yaml`) — quão exigente queres ser. Mais margem = mais paciência.
3. **A intenção da posição** (DRIP vs Growth vs Compounder — memória `user_investment_intents`) — o sistema não aplica lógica de DRIP a um growth pick (a XP é growth, a BN é pós-split). Diz-me a intenção e ele para de te incomodar com "o dividendo é baixo".
4. **A tese com gatilho de saída** — uma tese que diz "morro se X" transforma um sinal de venda solto numa decisão. Sem gatilho escrito, o SELL e a tese vivem separados.
5. **A escolha de método de fair value** (a decisão A vs B que está pendente) — teto conservador puro, ou teto + DCF forward lado a lado. Até decidires, o número persistido é o conservador; o forward vive em `analytics.fair_value_forward`.

---

## 7. O que *não* peças (anti-padrões — Disciplina de Investidor)

- Não peças uma opinião sem fonte recente — o sistema confirma o último resultado < 90 dias antes de opinar (Disciplina §1).
- Não celebres um número bonito — se o DCF te dá o que adoras, o primeiro instinto é procurar o erro (terminal value > 75% do EV? crescimento projetado >> histórico? dividendo > lucro?) (Disciplina §2).
- Não peças "uma tese" sem como ela morre — 3-5 pilares, 3-5 riscos, 1 gatilho de saída (Disciplina §4).
- Não confundas "barata" com "barata por uma razão" — sempre cruzar com Piotroski/Altman/moat.
- Não trates o veredito SELL como ordem de venda — é "a margem não está aqui a este preço".

A régua completa: [[Bibliotheca/Disciplina_de_Investidor]].

---

## 8. Glossário relâmpago (os 15 termos que mais aparecem)

| Termo | Em uma linha |
|---|---|
| Fair value (conservador) | Teto Buffett-Graham: ~20× lucros (compounder) / ~12× (banco) / Graham Number (BR) / VPA (FII) |
| Fair value forward | DCF conservador que dá crédito ao prémio de qualidade — *novo, experimental* |
| Margem de segurança | Desconto exigido sobre o fair value antes de "compra" — 18% staples, 25-42% conforme risco |
| Veredito | BUY / HOLD / SELL / STRONG_BUY / TRIM / N/A — onde o preço cai vs as faixas |
| Moat (0-10) | Durabilidade da vantagem competitiva — ≥7 forte |
| Piotroski F (0-9) | Saúde financeira em 9 sinais — ≤3 rebaixa "compra" para "espera" |
| Altman Z | Aflição financeira — Z baixo força SELL |
| Beneish M | Manipulação de resultados — M ≥ -1,78 risco |
| Portão (gate) | Ajuste conservador ao veredito (intangíveis / aflição / macro / confiança) |
| Confiança de dados | cross_validated > single_source > disputed |
| Dividend safety (0-100) | Quão seguro é o dividendo forward |
| Conviction (0-100) | Nota composta qualidade+preço+tese — ranking do universo |
| Payback DRIP | Anos para dividendos reinvestidos duplicarem as ações |
| Paper trade | Sinal simulado; vira capital real só após 30+ fechados com >60% de acerto |
| Perpetuum | Agente autónomo que propõe ações (revês com `/perpetuum-review`) |

Glossário a sério, com thresholds e contraméricas: `obsidian_vault/Glossary/`.

---

*Manutenção: este doc vive no Bibliotheca. Quando um conceito novo entrar no engine (ex.: o método forward sair de experimental), acrescentar aqui a tradução em linguagem de investidor — não só no CLAUDE.md.*
