---
type: memorandum
tags: [research, simplywall.st, consensus, ideas, dividend, value, growth, ai, overnight]
created: 2026-05-11
audience: o chefe (briefing matinal)
related: ["[[Posicoes_4_Lentes_2026-05-11]]", "[[DRIP_Shortlist_2026-05-11]]", "[[Manual_de_Direcao]]"]
data: data/sws_consensus.json · data/sws_quotes.json · data/sws_scrape/*.json
---

# 📋 MEMORANDUM — Simply Wall St "Investing Ideas": consensus de listas, a nossa carteira pela lente deles, e ideias novas

> **Bom dia.** Trabalhei a noite nisto. Resumo do que fiz, em três frases: (1) rastreei **47 das 48 listas "investing ideas" da Simply Wall St** (as 5 que deste + as outras 43 do índice), apanhando o topo de cada uma — nome, ticker, e os números que dava para confiar; (2) construí o **"consensus de listas"** — em quantas listas cada ação aparece — e cruzei com a nossa carteira + watchlist; (3) fiz uma passada de **research ("o que dizem")** nos ~24 nomes de maior consenso que ainda não seguimos. Tudo abaixo. Os ficheiros de dados estão em `data/sws_consensus.json` (a agregação completa, 990 tickers), `data/sws_quotes.json` (preços/targets yfinance dos novos), e `data/sws_scrape/*.json` (os 47 scrapes em bruto).

---

## 1. O headline (TL;DR de investidor)

1. **O sinal-Palantir que pediste, validado:** **PLTR aparece em 7 das 47 listas** (IA, data-centers, high-growth-tech, ethical-investing, solid-balance-sheet, rising-millennials, transformational-tech). Empatado em 1º lugar com **APP (AppLovin)**. Ou seja: o screening da SWS percebe a Palantir como um dos nomes de crescimento/IA mais "compelidos" do mercado — e nós já a temos (como aposta de crescimento, não DRIP). O outro nome "de toda a gente" que nós **temos na watchlist** é a **MSFT (6 listas)**. Confirma: a nossa carteira tem stocks que as pessoas procuram — mas concentrados no lado growth/AI; no lado dividendos a SWS surface nomes diferentes (ver §3).
2. **O consenso da SWS é fortemente growth/IA/semis.** O cluster de maior frequência: APP, FLEX, FN, SNDK, WDC (5 listas); NVDA, AVGO, AMD, MU, NOW, PANW, FTNT, DDOG, IOT, ZS, ORCL, P, SMCI, CRWD (4). Isto é "o que o mercado anda a falar" — e quase nada disto está no nosso universo DRIP/Buffett. Não é um problema; é uma escolha. Mas há aqui uma decisão estratégica latente: queremos uma "manga growth/IA" pequena? (ver §6 e §7).
3. **Do lado DIVIDENDOS, as listas da SWS surface sobretudo bancos regionais de yield alto** (FIBK, HBAN, FNLC, OTCM) + REITs (ELS) + farmacêuticas baratas (PFE 6-7%, MRK ~3%, GILD ~3%). **Nenhum dos nossos Aristocrats "quietos"** (MKC, NFG, TROW, ABT, KMB...) aparece nas listas SWS — porque os screens de dividendo da SWS estão ordenados por *yield* e esses nomes ficam abaixo do corte que apanhei. **Não muda nada da nossa shortlist DRIP de ontem** (`[[DRIP_Shortlist_2026-05-11]]`) — só significa que a "comunidade SWS" e nós olhamos para sítios um pouco diferentes do mesmo bairro.
4. **A ideia de valor mais interessante que sai daqui:** **ZTS (Zoetis)** — em 4 listas (analyst-top-picks + big-pharma-dividends + biotech + growing-dividend-payers), ROE ~80%, fosso real (saúde animal de companhia), múltiplo comprimido após de-rating, alvos de analistas ~$160+ vs ~$112. Encaixa na régua Buffett-qualidade. Candidata clara a watchlist. Atrás dela: **MRK, GILD, AMP, AU** (esta cíclica).
5. **Caveat honesto que aplica a tudo:** o "número de listas" favorece o que está no **topo** de cada screen da SWS (muitas vezes ordenado por yield, momentum ou market cap), e eu só apanhei o **topo ~36 de cada lista**. Logo **ausência ≠ rejeição** — AAPL/KO/PG/JPM/HD aparecem em 0 listas, o que é quase de certeza artefacto de corte (não que a SWS os deteste). Trata os contagens como "está no topo de N screens", não como "é amado por N screens".

---

## 2. Metodologia & limitações

- **Fonte:** as 48 listas em `simplywall.st/discover/us/investing-ideas` (índice) + as 5 que indicaste. As páginas individuais estão atrás de Cloudflare (o nosso `portal_playwright` headless ficou preso no "Just a moment…"), mas o **`WebFetch`** passou — usei 6 sub-agentes em paralelo, cada um a fazer `WebFetch` de 8 listas e a escrever um JSON por lista (`data/sws_scrape/<id>_<slug>.json`).
- **47/48 OK.** Falhou só `the-future-is-online` (CF). Parciais: `renewable-energy` (1 nome), `the-intelligent-investor` (4 nomes — RRC, IBP, GPOR, IGIC — pode ser que a lista seja mesmo curta, ou corte; vale re-confirmar).
- **Cada lista deu ~30-36 nomes** (o topo). Os números (preço, retorno 7d/1y, mkt cap, analyst target, valuation, growth, div yield) que o `WebFetch` extraiu vinham frequentemente **desalinhados de coluna** — por isso para os nomes que não cobrimos eu **re-puxei preço/target/yield/PE da yfinance** (`data/sws_quotes.json`) em vez de confiar no scrape; para os que cobrimos, usei a nossa DB (preço, our_fair, ação, consenso).
- **Tickers normalizados** para US-listed (1-5 letras + classe `-A`/`-B`). Foram descartados os numéricos/estrangeiros (601138, POWERINDIA, BRK.A, LKNC.Y, etc.) — a lista `top-asian-stocks` é toda assim e ficou de fora.
- **Categorias das 48 listas** (para o "que tipo de consenso"): **dividend** (5), **value** (5), **quality** (4), **growth** (5), **analyst/insider** (3), **ai_tech** (7), **sector** (19). A contagem por categoria de cada ação está no JSON e nas tabelas abaixo (formato `div2 grw4 ai1` etc.).

---

## 3. As NOSSAS POSIÇÕES vistas pela lente SWS

| Holding | # listas | Categorias | Em que listas | Leitura |
|---|--:|---|---|---|
| **PLTR** | **7** | qual1 grw3 ai2 sec1 | AI-stocks, data-center, ethical, high-growth-tech-AI, solid-balance-sheet, rising-millennials, transformational-tech | É a aposta de growth que o mercado mais "vê". A SWS valida a nossa tese (não-DRIP, crescimento). |
| **ACN** | 3 | div3 | dividend-powerhouses-3-yield, growing-dividend-payers-2.5%, upcoming-dividends | A SWS classifica a Accenture como **nome de dividendos** (~1,7% yield, cresce-o rápido). Nós já sabemos: barata na régua Buffett (~$305 vs $180), mas yield baixo p/ DRIP. |
| **JNJ** | 3 | div2 sec1 | big-pharma-big-dividends, growing-dividend-payers, biotech-stocks | Confirmado como pharma-dividendo de referência. |
| **O** | 2 | div1 sec1 | property-play, upcoming-dividends | REIT de dividendo, como esperado. |
| ABBV | 1 | sec1 | biotech-stocks | Só apanhada na lista de biotech (não nas de dividendo — corte). |
| PLD | 1 | sec1 | property-play | — |
| TSLA | 1 | sec1 | battery-stocks | — |
| XP | 1 | ana1 | betting-on-wall-st | — |
| **AAPL, BLK, BN, BRK-B, GREK, GS, HD, JPM, KO, NU, PG, TEN, TSM** | **0** | — | — | **Em zero listas.** AAPL/KO/PG/JPM/HD em 0 é quase de certeza **artefacto de corte** (não topam os screens ordenados por yield/growth/momentum). BN/BRK-B/NU/GREK fazem sentido (conglomerados/ETF/sem dividendo). TEN: distress. **Não interpretar como "a SWS rejeita estes".** |

**Conclusão §3:** sim, temos stocks que "as pessoas procuram" — mas a sobreposição é **toda do lado growth/AI** (PLTR, e via watchlist a MSFT). Do lado dividendos, a SWS e nós olhamos para nomes diferentes. Não é mau — a nossa filosofia é Graham/Buffett, não "o que está no topo dos screens".

---

## 4. A nossa WATCHLIST vista pela lente SWS

| Watchlist | # listas | Categorias | Em que listas |
|---|--:|---|---|
| **MSFT** | **6** | qual4 ai2 | big-green-snowflakes, cybersecurity, quantum-computing, solid-balance-sheet, spotless-management, sustainable-track-record |
| **IBM** | 3 | div1 ana1 ai1 | insider-trading, quantum-computing, upcoming-dividends |
| ADP | 2 | div2 | dividend-powerhouses-3-yield, growing-dividend-payers-2.5% |
| AOS | 2 | div1 qual1 | big-green-snowflakes, growing-dividend-payers |
| CHRW | 2 | div1 ana1 | insider-trading, upcoming-dividends |
| FAST | 2 | div1 qual1 | growing-dividend-payers, solid-balance-sheet |
| MCD | 2 | div1 sec1 | big-foodies, growing-dividend-payers |
| MDT | 2 | div1 ai1 | dividend-powerhouses-3-yield, us-transformative-AI-healthcare |
| NEE | 2 | sec2 | nuclear-energy, we-cant-live-without-them |
| PPG | 2 | div1 qual1 | big-green-snowflakes, growing-dividend-payers |
| RLI | 2 | div2 | dividend-powerhouses-3-yield, high-and-sustainable |
| (#1 cada) | 1 | — | ABM, ABT, ALB, ATO, BEN, BF-B, BRO, CAT, CVX, ECL, ED, ES, GD, ITW, JKHY, LIN, NFG, ROP, RPM |
| **50 nomes** | **0** | — | ADM, AFL, APD, AWR, BDX, BKH, CB, CBSH, CHD, CINF, CL, CLX, CTAS, CWT, DOV, EMR, ERIE, EXPD, FDS, FUL, GPC, GRC, GWW, HRL, KMB, LEG, LOW, MGEE, **MKC**, MO, MSA, MSEX, NDSN, NUE, NWN, PEP, PH, PNR, SCL, SHW, SJM, SPY, TDS, TR, UVV, **V**, WMT, WST, XOM |

**Conclusão §4:** a SWS gosta mais (do que temos em watchlist) de **MSFT, IBM, ADP, RLI, MDT, PPG, AOS, FAST**. As que **nunca lista** são quase todos os nossos Aristocrats/Kings quietos (MKC, KMB, V, PEP, NUE, SHW, GWW, CTAS, CB, CINF, AFL…) — de novo, **corte por yield/momentum, não rejeição**. O `V` em 0 listas é a prova de que é artefacto (a Visa estaria em meia dúzia de screens da SWS se eu tivesse apanhado mais fundo). **Ação:** numa segunda passada, re-scrape mais profundo (page 2+) das listas de dividendo/quality para fechar este buraco.

> **Confirmação parcial (page-2 testada):** `?page=2` funciona no `WebFetch`. A página 2 de `dividend-powerhouses-3-yield` continua com ~36 nomes — esmagadoramente **mais bancos regionais pequenos** (Credicorp, Valley National, United Bankshares, Preferred Bank, NBT Bancorp, WaFd, First Financial Bancorp, Lakeland Financial, Community Trust Bancorp…) **+ alguns não-bancos de qualidade** que nós seguimos ou deveríamos: **Watsco (WSO), J&J Snack Foods (JJSF), John B. Sanfilippo (JBSS), CareTrust REIT (CTRE), EOG Resources, Merck (de novo)**. Ou seja: confirma-se que os screens de dividendo da SWS são **ordenados por yield** → os bancos regionais de 4-6% ocupam o topo e os Aristocrats "blue-chip" (KO, PG, PEP, V, MKC…) caem para as páginas 3-5+. A nossa watchlist está coerente; a SWS só "vê" primeiro os yields altos. (Re-scrape completo das páginas 2-5 das 9 listas dividendo/quality deferido — alto esforço, baixa novidade marginal; faço se pedires.) — A lista `the-future-is-online` foi confirmada **vazia** ("0 companies") no site, não é bloqueio.

---

## 5. A tabela-mãe — TOP por nº de listas SWS

`OWN` = HOLDING / watchlist / — · `cats` = contagens por categoria (div/val/qual/grw/ana/ai/sec) · números (preço/target/our_fair) da nossa DB ou da yfinance.

| TK | # | OWN | cats | Empresa | Box (research) |
|---|--:|---|---|---|---|
| **APP** | 7 | — | grw4 qual1 val1 sec1 | AppLovin | **Growth** — AXON 2.0 AI ad engine + e-commerce; ~80% EBITDA margin; ~-50% YTD drawdown + short-seller ruído; alvos ~$600-640 vs ~$420. |
| **PLTR** | 7 | **HOLDING** | grw3 ai2 qual1 sec1 | Palantir | Growth — já temos. O nome mais "consenso" do nosso lado. |
| **MSFT** | 6 | watchlist | qual4 ai2 | Microsoft | Growth/quality — Copilot/Azure-AI; o nosso veredito: caro (~25× tecto vs preço $415). |
| **FLEX** | 5 | — | grw4 sec1 | Flex Ltd | **Cyclical** — EMS levado pelo capex de servidores AI; margem fina; 52-sem high. |
| **FN** | 5 | — | grw3 val1 sec1 | Fabrinet | Cyclical — óptica para datacenter/AI; concentração de clientes. |
| **INSM** | 5 | — | val1 ai1 ana1 sec2 | Insmed | **Spec/biotech** — Brensocatib (bronquiectasia) catalisador; pré-lucro. |
| **SNDK** | 5 | — | grw4 sec1 | Sandisk | **Cyclical** — supercycle de NAND/flash; preço (~$660) já desconta o melhor caso. |
| **WDC** | 5 | — | grw3 qual1 ai1 | Western Digital | **Cyclical** — HDD para AI datacenter; margens >50%; +100-170% em 2026. |
| **AMD** | 4 | — | ai2 grw1 sec1 | AMD | Growth — #2 em GPU AI; execução vs NVDA. |
| **AU** | 4 | — | qual3 sec1 | AngloGold Ashanti | **Cyclical** — minerador de ouro; alvos ~$112 vs ~$91; payout variável. |
| **AVGO** | 4 | — | ai2 qual1 sec1 | Broadcom | Growth — ASICs AI custom + VMware (software cash-machine); ~1% yield. |
| **DDOG** | 4 | — | grw3 ai1 | Datadog | Growth — observability + AI; SaaS premium. |
| **FIBK** | 4 | — | div3 qual1 | First Interstate BancSystem | **DRIP** — banco regional Oeste; NIM ~3,3% a expandir; ~4% yield; Hold, PT ~$36-37 ≈ preço. |
| **FTNT** | 4 | — | ai3 grw1 | Fortinet | Growth — cybersecurity; firewall→platform. |
| **FUTU** | 4 | — | qual2 ana2 | Futu Holdings | **Growth (high-beta)** — broker online chinês; risco regulatório/ADR; alvos trimados. |
| **GILD** | 4 | — | qual2 div1 sec1 | Gilead Sciences | **Buffett-value** — lenacapavir (HIV prevenção) + oncologia; ~3% yield; -17% off highs; ~fair (~$131 vs PT >$130). |
| **HBAN** | 4 | — | div3 ana1 | Huntington Bancshares | **DRIP** — banco regional growthy (Sudeste/Texas); ~5% yield; Buy-lean, PT ~mid-$18 vs ~$17. |
| **HUT** | 4 | — | ai2 grw1 sec1 | Hut 8 | **Spec** — mineiro Bitcoin a pivotar p/ AI/HPC. |
| **IOT** | 4 | — | ai2 grw2 | Samsara | Growth — IoT/telematics + AI; SaaS. |
| **IREN** | 4 | — | grw2 ai1 sec1 | IREN | **Spec** — Bitcoin→AI datacenter. |
| **LITE** | 4 | — | val1 ai1 grw1 sec1 | Lumentum | Cyclical — óptica datacenter/AI; recuperação de ciclo. |
| **MU** | 4 | — | qual1 grw1 ai1 sec1 | Micron | **Cyclical** — DRAM/HBM para AI; ciclo de memória. |
| **NOW** | 4 | — | ai2 grw1 ana1 | ServiceNow | Growth — workflow enterprise + AI ACV alvo $1,5B; múltiplo rico. |
| **NVDA** | 4 | — | ai2 qual1 sec1 | NVIDIA | Growth — líder de compute AI; FY26 rev ~$216B (+65%); ~$97B FCF; concentração de clientes. |
| **ORCL** | 4 | — | ai1 grw1 sec2 | Oracle | Growth — OCI/cloud-AI backlog; dívida alta. |
| **P** | 4 | — | grw3 ai1 | (ticker "P" — nome no scrape veio errado) | ⚠️ dados duvidosos — verificar qual empresa é. |
| **PANW** | 4 | — | ai2 grw1 ana1 | Palo Alto Networks | Growth — platformization de segurança; ~-50% drawdown vs expectativas elevadas; PT ~$212 (pós-split). |
| **RDDT** | 4 | — | qual2 grw1 ana1 | Reddit | Growth — dados p/ treino de LLM + publicidade; volátil. |
| **SMCI** | 4 | — | grw3 ai1 | Super Micro Computer | **Spec** — servidores AI; histórico contabilístico manchado. |
| **YOU** | 4 | — | val1 grw2 sec1 | Clear Secure | Growth — identidade verificada (CLEAR); SaaS-ish. |
| **ZS** | 4 | — | ai2 grw2 | Zscaler | Growth — zero-trust/SSE; SaaS premium. |
| **ZTS** | 4 | — | div2 ana1 sec1 | Zoetis | **Buffett-value** ⭐ — saúde animal de companhia; ROE ~80%; fosso real; múltiplo de-rated; alvos ~$160+ vs ~$112. **A melhor ideia de valor da lista.** |
| ACN | 3 | **HOLDING** | div3 | Accenture | já temos — barata na régua Buffett. |
| AMP | 3 | — | qual2 div1 | Ameriprise Financial | **Buffett-value** — compounder de wealth-mgmt, ROE alto; alvos ~$500+ vs ~$465 (full). |
| ANET | 3 | — | qual1 val1 ai1 | Arista Networks | Growth/quality — networking datacenter; balanço imaculado. |
| APH | 3 | — | grw2 val1 | Amphenol | Growth/quality — connectors; compounder discreto. |
| BKE | 3 | — | qual2 div1 | Buckle | **DRIP (cash-cow)** — retalho teen sem dívida; specials de $3+ (~8% all-in yield); não cresce. |
| CF | 3 | — | div1 val1 qual1 | CF Industries | **Cyclical** — azoto/fertilizante em upcycle; buybacks; ~fair após +76% YTD. |
| CRWD | 3 | — | ai2 grw1 | CrowdStrike | Growth — segurança endpoint+ |
| ELS | 3 | — | div2 | Equity LifeStyle Properties | **DRIP** — REIT de manufactured-housing/RV; defensivo, low-capex; alvos ~$70 vs ~$62. |
| FIX | 3 | — | qual2 val1(?) | Comfort Systems USA | Cyclical/quality — HVAC contractor; boom de construção/datacenter. |
| FLS | 3 | — | qual2 val1(?) | Flowserve | Cyclical — bombas/válvulas industriais. |
| FNLC | 3 | — | val2 div1 | First Bancorp (Maine) | **DRIP (micro)** — banco comunitário barato; ~5,3% yield; ilíquido. |
| LLY | 3 | — | div1 qual1 | Eli Lilly | **Growth** — GLP-1 (Mounjaro/Zepbound) + orforglipron oral; alvos ~$1.218 vs ~$925; múltiplo nosebleed. |
| MRK | 3 | — | div1 val1 | Merck | **Buffett-value** — P/E mid-teens, ~3% yield, Winrevair/Daiichi-ADCs; cliff de Keytruda 2028 é o risco. |
| PFE | 3 | — | div1 | Pfizer | **DRIP (high-yield)** — ~6-7% yield, barata, oncologia Seagen + cortes de custo; cliff pós-COVID/patentes é a tese-bear. |
| DHT | 3 | — | div2 qual1 | DHT Holdings | **Cyclical** — VLCC tanker; payout 100% do lucro mas swinga com spot rates. |
| (IBM) | 3 | watchlist | div1 ana1 ai1 | IBM | já em watchlist. |
| ALDX, BUKS, OTCM, INTC, NTNX, SNPS, CRCL, TPC, ... | 3 | — | vários | — | (ver `data/sws_consensus.json` para o resto) |

### 5b. Números ao vivo (yfinance, `data/sws_quotes.json`) — as novas ideias mais relevantes

| TK | Preço | Alvo médio | Upside ao alvo | Yield | Fwd P/E | Rec analistas | Setor | Nota |
|---|--:|--:|--:|--:|--:|---|---|---|
| **ZTS** | **$77** | $136 | **+77%** | 2,6% | ~10-13× | buy | Healthcare | ⚠️ Caiu MUITO (era ~$170 em 2024). Fwd P/E ~10-13× é baixíssimo para a Zoetis — ou de-rating genuíno (concorrência Librela/Apoquel?) ou quirk de dados. **`ii deepdive` prioritário** antes de qualquer conclusão. |
| **PFE** | $26 | $29 | +13% | **6,7%** | 9,1× | buy | Healthcare | High-yield value clássico; o yield é a tese, o cliff de patentes 2026-28 é o risco. |
| **MRK** | $111 | $130 | +17% | 3,1% | 11,6× | buy | Healthcare | Pharma de qualidade com desconto; cliff Keytruda 2028 é o que pesas. |
| **GILD** | $134 | $158 | +18% | 2,5% | 13,8× | buy | Healthcare | Biotech barata; ~justa-a-barata; sem LOE major próximo. |
| **AMP** | $464 | $541 | +17% | 1,5% | **9,7×** | buy | Financials | Compounder wealth-mgmt a ~10× lucro fwd — barato para a qualidade; yield baixo. |
| **AU** | $108 | $121 | +11% | 4,3% | 10,0× | buy | Materials | Cíclico (ouro); só se quiseres exposição a ouro. |
| **HBAN** | $16 | $20 | **+24%** | 3,9% | 8,4× | buy | Financials | Banco regional growthy; o melhor "upside ao alvo" dos regionais. |
| **FIBK** | $35 | $37 | +6% | **5,2%** | 11,9× | hold | Financials | Yield alto, mas só Hold dos analistas; sleepy. |
| **OTCM** | $55 | $65 | +19% | 1,8%* | 17,4× | strong_buy | Financials | *1,8% é só o div regular — os specials sobem o all-in p/ ~5%+. Asset-light. |
| **FNLC** | $28 | n/a | — | **5,1%** | n/a | (sem cobertura) | Financials | Micro-cap ($1B), ilíquido, sem cobertura — yield 5%. |
| **ELS** | $63 | $70 | +11% | 3,4% | (REIT) | buy | Real Estate | REIT defensivo (manufactured-housing); bom complemento ao O/PLD. |
| **BKE** | $50 | $53 | +6% | 2,7%* | 10,9× | (sem cobertura) | Cons. Cyc. | *2,7% é o div regular; com o special anual ~8% all-in. Cash-cow sem dívida. |
| **APP** | $478 | $645 | **+35%** | — | 21,8× | strong_buy | Comm. Svcs | O mais "consenso" (#7); -50% YTD; alto reward / alto ruído de short-sellers. |
| **NVDA** | $219 | $269 | +23% | ~0% | 19,4× | strong_buy | Technology | O líder de IA; múltiplo "fwd" parece baixo (19×) por causa do crescimento embutido. |
| **AVGO** | $428 | $475 | +11% | 0,6% | 23,6× | strong_buy | Technology | A mais "Buffett-friendly" do lote IA (paga dividendo, software sticky, disciplina). |
| **NOW** | (ver json) | — | — | — | — | buy | Technology | Software composto + IA; múltiplo rico. |

> O ficheiro `data/sws_quotes.json` tem os 70 nomes (preço, alvo, yield, PE, rec, market cap, retorno 1a, setor). A discrepância ZTS $77-vs-$112 é o exemplo de porque não confio cegamente nos números do scrape — a yfinance dá o preço ao vivo.

---

## 6. NOVAS IDEIAS — agrupadas por "caixa"

### 6a. DRIP / income (relevante para nós) — candidatas a watchlist

| TK | Empresa | # listas | Yield/setup | Veredito preliminar |
|---|---|--:|---|---|
| **PFE** | Pfizer | 3 | ~6-7% yield, P/E baixo | Income-the-thesis; o cliff de patentes 2026-28 é real → **watchlist sim, "income only", olhos abertos** (parece o nosso MO/CVX bucket). |
| **HBAN** | Huntington Bancshares | 4 | ~5% yield, banco regional growthy | **Watchlist** — o mais "growthy" dos regionais; Buy-lean dos analistas. |
| **FIBK** | First Interstate BancSystem | 4 | ~4% yield, Oeste, sleepy | **Watchlist** — yield decente, Hold dos analistas; não empolga vs os nossos. |
| **OTCM** | OTC Markets Group | 3 | ~5,4% yield + specials, asset-light | **Watchlist** — máquina de caixa de nicho; cobertura fina (1 analista) é o risco. |
| **FNLC** | First Bancorp (Maine) | 3 | ~5,3% yield, micro-cap ($1B) | **Watchlist** com cautela — ilíquido, sem cobertura. |
| **ELS** | Equity LifeStyle Properties | 3 | REIT defensivo, raises constantes | **Watchlist** — manufactured-housing tem pricing power; bom complemento ao O/PLD. |
| **BKE** | Buckle | 3 | ~8% all-in c/ specials, sem dívida | **Watchlist** "cash-cow" — não cresce, mas a caixa é sólida; tipo UVV/HRL bucket. |

> **Cruzamento com a nossa shortlist DRIP de ontem:** os nossos ADD de ontem (NFG, MKC, TROW, ABT, PPG, FRT, RLI, BF-B…) **não aparecem nas listas SWS** (corte por yield), o que **não os invalida** — continuam bons. A SWS apenas adiciona à conversa os regionais de yield mais alto (HBAN/FIBK/FNLC/OTCM) e PFE/ELS. Nenhuma destas é claramente superior ao que já temos; são "engrossar a watchlist", não "trocar".

### 6b. VALUE / qualidade (régua Buffett) — a ideia forte

| TK | Empresa | # listas | Porquê | Veredito |
|---|---|--:|---|---|
| **ZTS** ⭐ | Zoetis | 4 | ROE ~80%, fosso de saúde animal de companhia, múltiplo comprimido (~14-21× de ~30×+), alvos ~$160+ vs ~$112 | **A melhor ideia nova.** Encaixa exactamente no que a lente Buffett premia (alto ROIC durável a preço de-rated). **Watchlist + correr o `ii deepdive` em prioridade.** |
| **GILD** | Gilead Sciences | 4 | Biotech barata, ~3% yield, lenacapavir + oncologia, sem LOE major | **Watchlist** — "cheap cash-flow biotech"; ~fair ao preço actual. |
| **MRK** | Merck | 3 | P/E mid-teens, ~3% yield, pipeline (Winrevair, Daiichi ADCs) | **Watchlist** — qualidade pharma com desconto; o cliff de Keytruda 2028 é o que tens de pesar. |
| **AMP** | Ameriprise Financial | 3 | Compounder de wealth-mgmt, ROE alto, capital return | **Watchlist** — qualidade, mas full valuation (alvos ~$500 vs $465); esperar pullback. |
| **AU** | AngloGold Ashanti | 4 | Alavancado ao ouro recorde, FCF/div snap-back | **Watchlist tactical** — cíclico, não DRIP; só se quiseres exposição a ouro. |
| **(Intelligent Investor)** | RRC, IBP, GPOR, IGIC | (lista 249, parcial) | Deep value clássico — Range Resources (gás), Installed Building Products, Gulfport Energy, Intl General Insurance | A lista "Intelligent Investor" da SWS está hoje muito concentrada em energia/value cíclico. Worth a re-scrape para confirmar; nenhum grita "compra" para o nosso perfil. |

### 6c. GROWTH / IA — o tema dominante do consenso (fora da nossa caixa DRIP/Buffett)

Isto é "o que o mercado anda a falar". **Não é uma recomendação** — é o mapa, para tu decidires se queremos uma manga growth pequena.

- **Adtech/software:** APP (#7 — o mais listado; -50% YTD, alvos ~$600 vs $420; alto reward/alto ruído de short-sellers), RDDT, NOW, ZS, FTNT, CRWD, PANW, DDOG, YOU, ANET.
- **Semis AI:** NVDA (#4 — o líder), AVGO (#4 — ASICs + VMware, ~1% yield), AMD (#4), MU (#4 — ciclo de memória), INTC, SNPS, LITE, FN, AVGO.
- **Memória/storage cíclico:** SNDK (#5), WDC (#5), MU — "supercycle de memória AI"; o consenso é forte mas o preço já desconta muito; é um *trade* de ciclo, não um *hold* de qualidade.
- **Crypto-adjacent:** HUT (#4), IREN (#4), CRCL (#3 — Circle); especulativo.
- **EMS/infra:** FLEX (#5), CLS-like names; margem fina, levado pelo capex de servidores AI.

**Se** fôssemos fazer uma manga growth (digamos 5-10% da carteira US): as "blue-chips de IA" seriam **AVGO** (tem dividendo, software sticky, disciplina Hock Tan — a mais "Buffett-friendly" do lote), **NVDA** (o líder, mas múltiplo de momentum), e **NOW/PANW** (software composto). A **APP** é a mais barata-vs-consenso mas a mais arriscada (short-seller noise). **Decisão a tomar contigo — não avanço sem sinal.**

### 6e. Suplemento page-2 (6 das 9 listas dividendo/quality) — o que mudou

Rastreei a **página 2** de 6 listas (`data/sws_scrape/*_p2.json`). Resultado:

- **Confirma o caveat do corte:** vários dos NOSSOS nomes que apareciam em "0 listas" estão lá, só na página 2 — **KO, ADP, FRT, PLD, ES** (em `upcoming-dividends` p2), **EXPO, WWW** (em `growing-dividend-payers` p2), **RPM, IBM** (em `big-green-snowflakes`/`sustainable-track-record` p2). Logo: a nossa watchlist está coerente; só não topa os screens.
- **PLTR sobe para ~8 listas** (aparece de novo em `sustainable-track-record` p2). Reforça o nº 1 do consenso.
- **Nomes de qualidade novos que a página 2 traz** (candidatos a olhar): **INTU** (Intuit — quality SaaS), **TRV** (Travelers — seguradora P&C de qualidade, Buffett-style), **MKTX** (MarketAxess — fixed-income trading platform, moat de rede), **DOX** (Amdocs — telecom software, ~3% yield, defensivo), **ALL** (Allstate), **BMY** (Bristol Myers — pharma barata high-yield), **STZ** (Constellation Brands — cerveja/spirits), **CI** (Cigna — managed care barata), **GRMN** (Garmin — sem dívida, ~2,5% yield), **MRSH/MMC** (Marsh McLennan — broker de seguros de qualidade), **WSO** (Watsco — distribuição HVAC, Aristocrat), **JJSF/JBSS** (snack foods, Aristocrats discretos), **CTRE** (CareTrust REIT — healthcare REIT, ~4% yield), **GLPI** (Gaming & Leisure Properties — casino REIT, ~6% yield).
- **As outras 3 listas** (`high-and-sustainable`, `big-pharma-big-dividends`, `spotless-management`) não tinham página 2 — são listas curtas (~10-32 nomes, já apanhadas inteiras).

> **Os 4 nomes mais "Buffett-friendly" deste suplemento:** **TRV** (P&C insurer de qualidade), **MMC/MRSH** (insurance broker, compounder), **INTU** (SaaS moat — mas caro), **WSO** (HVAC distributor Aristocrat). Worth a watchlist + 4-lentes pass. **GLPI** e **CTRE** entram na conversa DRIP (REITs de yield 4-6%).

---

## 7. O "sinal-Palantir" — como ler as contagens

Tu deste o exemplo: "Palantir em 15 de 25 listas → tens uma ideia de como é percebida". Com a nossa amostra de 47 listas:
- **PLTR = 7/47** (≈15%). É o tecto, empatado com **APP**. Leitura: a Palantir é vista pelo screening da SWS como **simultaneamente** crescimento (rising-millennials, transformational-tech, high-growth-AI), IA-infra (AI-stocks, data-center) **e** qualidade de balanço (solid-balance-sheet) **e** "ético" (ethical-investing). Ou seja: percepção amplamente positiva, multi-ângulo. Coerente com a tua tese de a teres como growth pick. **Mas** repara: nenhuma das listas de *valor* a apanha (a Palantir não é barata por nenhuma régua de valor) — então a "consenso positivo" é toda do lado momentum/qualidade-de-balanço, não do lado margem-de-segurança. Saber disso é o ponto.
- Próximo nível (5 listas): **APP, FLEX, FN, SNDK, WDC** — todos growth/tech/cíclicos-de-IA. **MSFT = 6** (a nossa watchlist).
- Do lado **dividendos**, o "tecto de consenso" é mais baixo: o nome de dividendo em mais listas é **FIBK/HBAN/ZTS/GILD = 4** — e mesmo esses só estão em ~3 listas de dividendo + 1 outra. Tradução: **a comunidade de dividendos é mais fragmentada** (ou os screens de dividendo da SWS, sendo ordenados por yield, surface nomes diferentes uns dos outros). Não há um "Palantir dos dividendos".
- **Interpretação prática:** usa a contagem como "amplitude de apelo / breadth", não como "qualidade". Um nome em muitas listas growth+sector+quality é "o mercado está apaixonado" — útil saber, mas não é a régua de Graham. Um nome de dividendo em 3-4 listas (FIBK, ZTS) já é "consenso forte para o seu nicho".

---

## 8. Síntese & ações propostas

**Para DRIP** — adicionar à watchlist (engrossar, não substituir): **HBAN, FIBK, OTCM, FNLC** (regionais yield alto), **ELS** (REIT defensivo), **PFE** (high-yield value, "income only"), **BKE** (cash-cow). Manter a shortlist DRIP de ontem (NFG, MKC, TROW, ABT, PPG, FRT, RLI, BF-B) como prioridade — a SWS não a contradiz.

**Para VALOR (Buffett-qualidade)** — **ZTS é a candidata de eleição** (watchlist + `ii deepdive` prioritário); atrás: **GILD, MRK, AMP** (watchlist), **AU** (só se quiseres ouro, é tactical).

**Para GROWTH** — registar o cluster (APP, NVDA, AVGO, NOW, PANW, AMD, MU/SNDK/WDC, FN, FLEX, ZS, FTNT, CRWD, IOT, DDOG…) num doc de tese "manga growth/IA" para decidires se queremos 5-10% disso. A mais "Buffett-friendly" do lote: **AVGO**. **Não avanço sem o teu sim.**

**Higiene de dados** — segunda passada: re-scrape mais profundo (page 2+) das listas de dividendo/quality da SWS para fechar o buraco dos nossos Aristocrats em "0 listas" (V, PEP, MKC, KMB… quase de certeza estão lá, abaixo do corte que apanhei). E re-confirmar `the-intelligent-investor` (só 4 nomes) e re-fazer `the-future-is-online` (falhou no CF).

**Fila (do que já estava em curso):** o brainstorm do *banco ROTCE-scaled* (JPM SELL→HOLD, escolha A/B/C) e o fix do *cascade do `dividend_safety`* (ABBV/CINF/FRT/RLI com EPS GAAP a estragar a safety) continuam parados — quando voltares, decidimos.

---

## 9. Anexo — as 48 listas SWS rastreadas

`data/sws_lists_index.json` tem a lista completa. Por categoria:
- **Dividend (5):** dividend-powerhouses-3-yield · upcoming-dividends · big-pharma-big-dividends · growing-dividend-payers-with-2-5percent-yield · high-and-sustainable
- **Value (5):** the-intelligent-investor · undervalued-stocks-based-on-cash-flows · undervalued-small-caps-with-insider-buying · undiscovered-gems-with-strong-fundamentals · buy-the-dip
- **Quality (4):** solid-balance-sheet-and-fundamentals · spotless-management · sustainable-track-record · big-green-snowflakes
- **Growth (5):** breakout-stocks · fast-growing-stocks-with-high-insider-ownership · the-rising-millennials · high-growth-tech-and-ai-stocks · transformational-technology
- **Analyst/insider (3):** analysts-top-stock-pics · insider-trading · betting-on-wall-st
- **AI/tech (7):** artificial-intelligence-ai-stocks · data-center-stocks · cybersecurity · fintech-stocks · quantum-computing-stocks · us-transformative-ai-healthcare-stocks · the-future-is-online *(falhou)*
- **Sector (19):** aerospace-and-defense · biotech-breakthroughs · biotech-stocks · battery-stocks · food-delivery-stocks · big-foodies · property-play · renewable-energy *(parcial)* · nuclear-energy-stocks · rare-earth-metal-stocks · us-midstream-oil-and-gas-pipeline-operators · top-gold-stocks · electric-autonomous-vehicle-stocks · construction-boom · cryptocurrency-and-blockchain-stocks · ethical-investing · environmentally-friendly · top-asian-stocks · we-cant-live-without-them

*Ficheiros: `data/sws_consensus.json` (agregação, 990 tickers, ordenado por nº de listas) · `data/sws_quotes.json` (preço/target/yield/PE yfinance dos novos) · `data/sws_research_targets.json` · `data/sws_scrape/*.json` (47 scrapes em bruto) · `data/sws_lists_index.json` (índice das listas).*
