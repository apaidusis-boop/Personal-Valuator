# Disciplina de Investidor — a régua por trás dos plugins FSI

> Origem: 2026-05-11. Destilado dos plugins **Claude for Financial Services** (`anthropics/financial-services`), depois de ler o conteúdo real das skills (não os READMEs). Tirando o software, aquilo é o *modus operandi de um analista institucional sério*. Este doc é a versão "mentalidade", não a versão "código".
>
> **Função**: régua para os agentes de research (council, synthetic_ic, deepdive, thesis_manager, earnings_prep, verdict). Quando uma análise nossa não respeita um destes pontos, é trabalho por acabar — não opinião pronta.
> Relacionado: [[Comercial/Personal_Investment_OS_Blueprint]] · memória `anthropic_fsi_plugins.md` · `CONSTITUTION.md`

---

## Os 10 hábitos

### 1. Nunca confies na tua memória sobre o último resultado
Antes de escrever uma linha: data de hoje → procurar ativamente o último resultado → confirmar filing < 90 dias → se não, procurar outra vez. O erro nº1 é raciocinar sobre o que *achas* que sabes ("a ITSA reportou, foi assim") — a empresa mudou, o guidance mudou, o teu cérebro tem a versão de há 6 meses. **Fonte primária recente, sempre, ou não opinas.** Onde somos frouxos: deixamos o raciocínio correr sobre "o último trimestre" sem confirmar qual é.

### 2. Desconfia do modelo quando ele te dá a resposta que adoras
Flags de auditoria: terminal value > 75% do EV (estás a pagar pelo ano 10, não pelos próximos 3)? Projeções em "taco de hóquei" (plano até ano 3, milagre no 4–10)? Crescimento de lucro projetado >> histórico? Dividendo > lucro gerado? Cada flag é o som de um investidor a justificar uma conclusão já feita — o modelo erra *na direção do que querias*. **Número bonito → primeiro instinto é procurar o erro, não celebrar.**

### 3. Mostra o trabalho — o que mudou e *porquê*
Mudança de estimativa = valor antigo → novo → variação → uma linha de razão. Não "revi as estimativas". *Porquê.* Daqui a um ano queres saber o *caminho* de como mudaste de ideias, não só o destino — senão reescreves a história a teu favor. **O registo de decisão tem o "porquê", não só o "o quê".**

### 4. ⭐ Uma tese tem de ter como morrer
*Se nada pudesse desmentir a tese, não é tese — é religião.* Ao criar: 3–5 pilares, 3–5 riscos que a invalidam, gatilho de saída ("o que me faria sair"). Depois: rastrear evidência *contra* com o mesmo apetite que a evidência a favor; rever o scorecard todos os trimestres mesmo "sem nada dramático". A única coisa desta lista que muda mesmo retornos. Onde somos frouxos: temos teses para todas as holdings mas a maioria não tem gatilho de saída escrito, e quando temos um sinal de venda ele vive separado da tese — em vez de a tese dizer "morro se X".

### 5. "Não houve nada" é uma resposta legítima
Nota matinal = a única coisa que importa / overnight (uma linha cada) / eventos hoje / ideias + o que as tornaria erradas. Regras: tem uma opinião (resumo sem *view* é lixo), não enterres o headline, e — a melhor — "se erraste, assume na nota seguinte; credibilidade vale mais do que acertar sempre". A maior parte do fluxo diário é ruído; a disciplina é distinguir acionável (resultados, M&A) de barulho (downgrade menor, não-evento) e levar registo dos próprios erros.

### 6. Anota o que esperas — e depois anota se aconteceu
Calendário de catalisadores = data / evento / empresa / impacto esperado (A/M/B) / posicionamento — e depois **arquivar o resultado real**. Era alto impacto e foi não-evento? Bateu como esperavas? É assim que constróis reconhecimento de padrão *sobre ti*: descobres que sobrestimas earnings, ou que os teus "catalisadores" raramente movem preço, ou que erras sempre na mesma direção. Sem arquivo de outcomes não há aprendizagem — só palpites esquecidos.

### 7. Quando sai um resultado, há um interrogatório fixo
Bateu ou falhou? (vs o que *eu* esperava **e** vs consenso — coisas diferentes). Porquê — que segmento/geografia puxou? Margem subiu/desceu, porquê? Guidance novo vs antigo vs Street, e o que penso dele? Reforça/enfraquece cada pilar da tese? Estimativas mudam — para quê e porquê? Preço-alvo muda? (regra: estimativas mudam >5% → alvo normalmente também). Rating muda? Checklist contra o esquecimento — sem ela lês o press release, sentes um *vibe* e segues. Força a separar one-time de estrutural, onde está o dinheiro.

### 8. O imposto é parte do retorno
Uma perda existente vale dinheiro se realizada na altura certa — abate ganhos, e mantém-se a exposição comprando algo *parecido mas não idêntico*. Vendes pela tese **e** pelo calendário fiscal. Caso nosso é muito BR-específico: isenção R$20k/mês em ações, 20% em FII, prejuízo compensável, day-trade vs swing em buckets separados. Rebalanceamento e colheita de prejuízos andam juntos; antes de "vende X" → "qual o custo fiscal e há substituto que mantém a exposição?".

### 9. Antes de uma decisão grande, escreve-a como se a fosses defender perante céticos
Memo de comité: resumo executivo + retorno headline + top-3 riscos e como os mitigas; depois empresa / indústria / financeiros / plano de criação de valor / retornos base-alta-baixa. Escrever formalmente *força rigor* — o óbvio na cabeça desfaz-se no papel perante um leitor hostil. Para compra/venda material não chega "acho que sim".

### 10. Sabe onde cada empresa tua se senta no mapa
Enquadramentos 2×2 por sector (varejo: preço × amplitude de gama; serviços financeiros: escala × especialização; etc.). Não basta "boa empresa" — precisas da posição relativa no campo competitivo: quem é barato, quem é nicho, quem tem escala — e *se a empresa se está a mover no mapa*.

---

## Síntese
Cinco hábitos: **(1)** trabalha sempre da fonte primária recente, nunca da memória; **(2)** desconfia do modelo quando ele te agrada; **(3)** define como a tese morre *antes* de comprar e persegue a evidência contra ti; **(4)** leva registo dos teus erros e dos outcomes que previste; **(5)** imposto e calendário fazem parte da decisão de vender. Temos mais máquina do que eles — o que falta é parte desta disciplina *por escrito*.

---

## Eficiência & possibilidade de comercialização

> Nota do user (2026-05-11): além do uso pessoal, vale pensar nisto (a) de forma mais eficiente e (b) com a hipótese de comercializar o sistema lá adiante. Ver [[Comercial/Personal_Investment_OS_Blueprint]] (já tem MVP/telas/pricing/SaaS).

**O "teatro" sell-side inverte-se de anti-padrão para feature.** Para *nós como PF*, a regra é verdade comprimida — meia página com um gráfico se for isso que basta; volume não é rigor. Mas se o sistema virar produto, o que hoje descartamos passa a ser **uma camada de entrega (tier), não a substância**:

- **Outputs em camadas**: (1) o nosso default — denso, acionável, "compra/mantém/vende?"; (2) tier "relatório" — initiating-coverage / earnings-update no formato institucional (8–12 págs, charts, tabelas old→new, secção de fontes com links), que clientes *querem* ver mesmo quando a substância cabe numa página. A disciplina #1–#10 garante que o tier longo não é encher chouriços — é a mesma análise, embrulhada.
- **Os 11 MCPs de data providers** (FactSet/Daloopa/Morningstar/Moody's/S&P/PitchBook…) que hoje ficam não-autenticados deixam de ser ruído: num produto pago, ou se integra (caro, com conta) ou se substitui por camadas equivalentes. Hoje: yfinance + SEC EDGAR + CVM + Status Invest + fiis.com.br já cobrem o essencial — o gap é *cobertura premium*, não *cobertura*.
- **Multi-user / auth / Postgres**: o Blueprint já marca SQLite → Postgres "só se SaaS". A arquitetura BR/US isolada e o "in-house first" (Ollama) são vantagens de custo num SaaS — margem melhor que concorrentes que queimam OpenAI/Claude API por request.
- **Eficiência (vale para ambos os cenários)**: menos scripts one-shot, perpetuums em vez de re-runs manuais, cache TTL agressivo, Ollama antes de API. Já é a filosofia; comercializar só aperta a régua (cada request de cliente que toca API tem custo marginal real).
- **O moat do produto não é o screening** (qualquer um faz P/E < 20) — **é a disciplina embutida**: o sistema que te obriga a escrever como a tese morre, que arquiva os teus erros, que te mostra que sobrestimas earnings. Isso é difícil de copiar e é o que falta no mercado retail (TipRanks/Finviz/Simply Wall St dão números, não disciplina).

**Não decidir nada agora** — isto é só para não perder o fio. Próximo passo natural quando se quiser avançar: fundir esta secção com o [[Comercial/Personal_Investment_OS_Blueprint]] e decidir se os 10 hábitos viram (a) régua interna dos agentes, (b) feature de produto ("o teu Constitution pessoal"), ou ambos.

---

## Como isto vira régua (quando se quiser implementar)
Picks baratos, in-house-first, idempotentes (detalhe na conversa de 2026-05-11):
1. **Freshness gate** — verificar o trimestre / abortar se filing > 90d stale (deepdive Scout + earnings_prep). Candidato a perpetuum check.
2. **Model-sanity flags** — TV ≥ WACC, implied > 3× preço, EPS CAGR >> hist, dividendo > NI, sinal de net-debt (dentro de `ii anomalies` / reusa `derive_scenarios`).
3. **Thesis scorecard + falsificabilidade** — coluna/secção por pilar + trend; auto-emitir trigger de stop-loss ao criar tese; regra "rastrear desconfirmação" nos prompts do council/synthetic_ic.
4. **Template de earnings-update** para `ii deepdive --post-earnings` (beat/miss lidera → segmentos → bridge de margem → guidance vs old/Street → impacto por pilar → estimativas old→new c/ razões → fair-value walk → lógica de rating).
5. **Catalyst outcome archive** — estender `decision_journal_intel` / `predictions_evaluate` para registar "a catalisador jogou?" com tags A/M/B.
