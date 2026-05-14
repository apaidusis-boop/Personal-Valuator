---
type: memorandum
tags: [research, simplywall.st, buffett, drip, value, dividend, shortlist]
created: 2026-05-13
audience: o chefe — decisão de watchlist
related: ["[[SWS_Consensus_Memorandum_2026-05-11_overnight]]", "[[DRIP_Shortlist_2026-05-11]]", "[[Manual_de_Direcao]]"]
data: data/sws_buffett_drip_shortlist.json (41 nomes ranked)
filter: "div >= 1 SWS list AND (quality + value) >= 1 SWS list, depois Buffett US screen"
---

# MEMO — SWS através da lente Buffett+DRIP (intersecção)

> Pediste o cruzamento certo: **Value Investing (Buffett) ∩ Dividend Investing (DRIP)**.
> Cruzei as 47 listas SWS (p1+p2): **41 nomes** aparecem em **pelo menos 1 lista de dividendos** *E* **pelo menos 1 lista de qualidade/valor**. Depois apliquei a régua Buffett US da Constitution (P/E fwd ≤ 20, DY ≥ 2,5%, ROE ≥ 15%, streak ≥ 10 ou Aristocrat) com yfinance live.
> Output: 4 nomes claros para adicionar à watchlist, 5 para investigar com cautela, 3 buckets a descartar para o nosso perfil.
> Ficheiro: `data/sws_buffett_drip_shortlist.json`.

---

## 1. TL;DR — o que faço agora

1. **3 nomes já estão na nossa watchlist e a SWS confirma a tese — não toco:** **IBM, PPG, AOS** (todos Aristocrats, todos passam a régua Buffett, todos com presença SWS em listas de dividendo + qualidade). Nada para fazer — já estão no radar.
2. **2 nomes novos a adicionar à watchlist agora**: **RPM** (Aristocrat 40 anos, qualidade industrial, fwd P/E 17, ROE 23%) e **MRK** (pharma de qualidade com desconto, fwd P/E 12, DY 3%, mas com cliff Keytruda 2028 explicitamente como risco da tese).
3. **3 nomes para `ii deepdive` antes de qualquer adição**: **GILD** (biotech barata e ~justa), **BMY** (high-yield 4,5% + ROE 39% mas Bristol corta dividendos historicamente — não é DRIP-clean), **BKE** (cash-cow sem dívida com specials que levam o all-in yield a 8% — não cresce, mas é bucket UVV/HRL).
4. **Descartado para o nosso perfil**: bancos regionais small/mid (11 nomes, "outro jogo"), shipping/fertilizer cíclicos (DHT/GSL/CF — payout do lucro, não DRIP), ADRs China/micro-caps (JFIN/HTHT/HEOL/FBAK).

---

## 2. A régua aplicada

Régua Buffett US da `CLAUDE.md`:

- **P/E fwd ≤ 20** (qualidade não é caro)
- **DY ≥ 2,5%** (Buffett não exige isto, mas a tua filosofia DRIP exige)
- **ROE ≥ 15%** (qualidade do negócio)
- **Streak ≥ 10 anos** *OU* **Dividend Aristocrat** (constância)
- (P/B ≤ 3 não aplicado aqui — não tinha o campo limpo para todos)

Considero **"passa Buffett+DRIP"** quem cumpre **4 de 5**. A relaxação está sempre no streak (porque nem toda a Buffett-name é Aristocrat — GILD/BMY/MRK por exemplo).

---

## 3. TIER A — passa a régua, é DRIP-clean

| TK | Empresa | Status | Fwd P/E | DY | ROE | Streak | Sector | Tese curta |
|---|---|---|---:|---:|---:|---:|---|---|
| **IBM** | International Business Machines | watchlist (4 listas SWS) | 15,9× | 3,2% | 36% | **65 (Aristo)** | Technology | Pivot p/ AI/hybrid cloud + balanço sólido + dividend streak inquestionável. Já passou a régua antes do SWS. |
| **PPG** | PPG Industries | watchlist (2 listas SWS) | 12,2× | 2,7% | 21% | **44 (Aristo)** | Materials | Tintas industriais; ciclo recovering; alvo $123 vs $106. |
| **AOS** | A. O. Smith | watchlist (2 listas SWS) | 13,6× | 2,5% | 28% | **41 (Aristo)** | Industrials | Aquecedores de água; China overhang real mas USA core estável; alvo $71 vs $57. |
| **RPM** | RPM International | — (2 listas SWS) | 16,7× | 2,2% | 23% | **40 (Aristo)** | Materials | Coatings/sealants (Rust-Oleum, DAP, Tremco); estável; alvo $128 vs $98 = **+31% upside**. **DY um pouco abaixo do nosso mínimo 2,5%** — mas tudo o resto bate caixa. |

**Veredito TIER A**: IBM/PPG/AOS já no radar — confirma a tese, não é descoberta. **RPM é a única descoberta nova clara**. Adicionar à watchlist.

---

## 4. TIER B — Buffett-friendly, DRIP precisa qualificação

Nomes onde a régua passa quase toda, mas há **uma pedra** que precisa ser pesada na tese antes de tratar como DRIP.

| TK | Fwd P/E | DY | ROE | Streak | Upside | A pedra na tese |
|---|---:|---:|---:|---:|---:|---|
| **MRK** | 11,9× | 3,0% | 19% | (não-aristo) | +15% | **Cliff Keytruda 2028** — 50%+ das vendas. Pipeline pós-Keytruda (Winrevair, ADCs com Daiichi) é credível mas não comprovado. Buffett-quality, mas pesar como "compra do desconto com clock". |
| **GILD** | 13,7× | 2,5% | 43% | (não-aristo) | +19% | **Sem LOE major próximo** = pedra menor. Lenacapavir (HIV prevenção) + oncologia Trodelvy; ~justa-a-barata; pharma honesta, dividendo crescente mas streak curto. |
| **BMY** | 9,2× | **4,5%** | 39% | (não-aristo) | +12% | **Bristol historicamente corta dividendos** (faz parte da cultura de M&A pesado). Yield 4,5% atractivo, ROE 39% alto — mas isto **não é o KO/PG do dividendo**. Trata como "high-yield value play" não como DRIP-compound. |
| **BKE** | 10,5× | 2,9% | **49%** | (cash-cow) | +10% | **Não cresce.** Buckle é jeans-store de teenagers que paga **specials anuais de $3+** levando o all-in yield a 8%. Sem dívida. Bucket "cash-cow estagnado" (tipo UVV/HRL). O risco é serem o último Sears: declínio retalho. |
| **AMP** | 9,8× | **1,5%** | **67%** | (não-aristo) | +15% | **DY abaixo do nosso mínimo.** Ameriprise é compounder de wealth-mgmt (~10× lucro fwd para ROE 67% é barato). Buffett-quality clara, mas o yield é low — vira "value compounder" não "DRIP". |

**Veredito TIER B**: dos cinco, **MRK e GILD** são as duas que mais facilmente entram na watchlist DRIP (pharma de qualidade com desconto, dividendo a crescer). **BMY** entra como "income play tactical, não DRIP compound". **AMP** é Buffett puro sem DRIP. **BKE** é nicho cash-cow — só se quiseres mais um nome do bucket UVV/HRL.

---

## 5. TIER C — descartar para o nosso perfil

### 5a. Cíclicos disfarçados de DRIP (shipping/fertilizer)

| TK | DY aparente | Por que não é DRIP |
|---|---:|---|
| **DHT** | 14% | Tanker VLCC; payout = 100% do lucro spot. Dividendo swinga 5×-15× com tarifas. Não é renda — é um *cyclical kicker*. |
| **GSL** | 6% | Containership de mid-size; preços de afretamento elevados a normalizar. Mesmo problema. |
| **CF** | 1,6% | Fertilizante azoto; upcycle terminando, buybacks > dividendos. Não é renda recorrente. |

### 5b. Bancos regionais small/mid (11 nomes — outro jogo)

A SWS surface estes porque ordena dividend-screens por yield, e bancos regionais pequenos rendem 4-6%. Mas isto é uma **classe de activo separada** da nossa tese (BR já tem ITUB4/BBDC4 + US já tem JPM como banco global). Lista para arquivo: **BAC, FIBK, HBAN, COLB, ASB, CTBI, FRME, PB, FMNB, INDB, COFS, PNFP, UNB, FNLC, FBAK**.

**Excepção possível: BAC** (Bank of America) — fwd P/E 10, DY 2,2%, strong_buy dos analistas. É blue-chip, não regional. Mas já temos JPM como aposta-banco-US. **Não adicionar sem trocar JPM por BAC** (não recomendo — JPM é melhor compounder).

### 5c. ADRs china / micro-caps esotéricos

**JFIN** (Jiayin — peer-lending China), **HTHT** (H World — hoteleiro China), **CMCL** (Caledonia Mining — micro gold), **HEOL** (Highwater Ethanol — OTC pink sheet, preço $15.750 é provavelmente artefacto de quote), **FBAK** (First National Bank Alaska — ilíquido, sem cobertura), **OPRA** (Opera Norway — browser de nicho), **OSPN** (OneSpan — segurança autenticação, micro-cap a recuperar). **Pular tudo.**

### 5d. Cíclicos de mid-cap mediana

**LEA** (Lear — autopeças), **WWW** (Wolverine — sapatos), **EXPO** (Exponent — consultoria forense, fwd P/E 19 é caro para o crescimento), **MKTX** (MarketAxess — fintech bond trading, fwd P/E 16, ROE 24% — esta é interessante mas yield 2,2% baixo), **FAST** (Fastenal — já watchlist; fwd P/E **32×** é caro para 34% ROE). **LLY** já é Growth, não DRIP. **CTRE** (CareTrust REIT — sénior housing; fwd P/E 25 caro mas REIT-justified; vale considerar como ELS-alternative no lado REIT). **BBY** (Best Buy — fwd P/E 8, DY 7%, ROE 37% — **value-trap clássico** ou pivot real? deepdive opcional).

---

## 6. Cruzamento com a nossa shortlist DRIP de 2026-05-11

A shortlist DRIP de ontem (MKC/NFG/TROW/ABT/PPG/FRT/BF-B/RLI) sobrevive intacta — **nenhum destes 41 nomes substitui qualquer um deles**. O SWS adiciona à conversa, não troca:

| Bucket | Nosso nome (ontem) | SWS nome (hoje) | Comparação |
|---|---|---|---|
| Healthcare quality | ABT (Aristo, ROE 30%, fwd P/E 23) | MRK / GILD / BMY | Os SWS são mais baratos mas **menos clean** (cliff/cuts). ABT continua superior. |
| Industrial Aristo | (já: AOS) | RPM | RPM é peer de qualidade — **adicionar como complemento, não substituir**. |
| Cash-cow nicho | (já: BF-B, RLI) | BKE | BKE é mais nichado/risk; BF-B/RLI continuam superiores. |
| REIT DRIP | (já: FRT, O na carteira) | CTRE | CTRE é sénior-housing (mais defensivo); FRT é shopping (mais cíclico). **Complemento, não substituto**. |

---

## 7. Acções concretas

1. **Adicionar `RPM` à watchlist US** — Aristo 40y, qualidade Buffett, P/E fwd 17, DY 2,2% (abaixo do mínimo mas o resto compensa), upside +31% para alvo dos analistas. *Faço já se confirmares*.
2. **Adicionar `MRK` à watchlist US com tag `clock:keytruda_cliff_2028`** — pharma de qualidade com desconto, mas só faz sentido se a tese é "compro o desconto pré-cliff e re-avalio em 2027".
3. **Adicionar `GILD` à watchlist US** — biotech barata, sem cliff próximo, pharma "honesta". DRIP-friendly e barata.
4. **Correr `ii deepdive` em**: BMY (perceber a história de dividend cuts), BKE (perceber sustentabilidade dos specials), CTRE (perceber spread vs FRT/O).
5. **Não adicionar**: BAC (já temos JPM), BBY (deepdive opcional, baixa prioridade), todos os bancos regionais small, todos os cíclicos shipping/fertilizer, todos os ADRs China.

---

## 8. Caveats

- **DY do yfinance é o `dividendRate / price` quando há `dividendRate`** (mais fiável que o campo `dividendYield` directo, que tem bugs a aparecer em alguns nomes — AMP veio 145% e LLY 73% no primeiro pass).
- **Streak vem da nossa DB `fundamentals.dividend_streak_years`** quando existe (PPG/IBM/AOS/RPM/FAST). Para os nomes não-DB usei `t.dividends` da yfinance — não 100% fiável (LLY veio 107 anos, claramente artefacto).
- **A SWS ordena dividend-screens por yield**, por isso este cruzamento favorece naturalmente high-yield + alto ROE simultâneo — o que é exactamente o que tu queres. Mas nem todos os "Buffett quietos" (MKC, KMB, V, NFG) aparecem porque caem no rank das listas SWS.
- **Não recomendo o BAC mesmo passando a régua** porque já temos JPM e ambos não cumprem a tua filosofia DRIP-Buffett tão bem como nomes não-bancários (banks são "outro jogo" — ver `Sectors/US_Banks` no vault).

---

**Bottom line**: O cruzamento Buffett+DRIP **valida fortemente** a tese de **IBM/PPG/AOS** já na watchlist, **adiciona claramente `RPM`** como Aristocrat industrial, e **MRK/GILD** como pharma de qualidade com desconto. **Não há "surprise upgrade"** — não há nome novo escondido que substitua os Aristos clássicos. A SWS confirma o terreno, não muda o mapa.

---

## 9. Links — para verificares directamente

### 9a. As listas SWS que conduziram este cruzamento (14 listas)

**5 listas DIVIDEND** (as que filtram por yield/dividend payers):
- [U.S. Dividend Powerhouses (3%+ Yield)](https://simplywall.st/discover/investing-ideas/146/dividend-powerhouses-3-yield/us)
- [Growing Dividend Payers with 2-5% Yield](https://simplywall.st/discover/investing-ideas/458086/growing-dividend-payers-with-2-5percent-yield/us)
- [U.S. High And Sustainable Dividend Stocks](https://simplywall.st/discover/investing-ideas/324/high-and-sustainable/us)
- [Big Pharma, Big Dividends](https://simplywall.st/discover/investing-ideas/10194/big-pharma-big-dividends/us)
- [U.S. Upcoming Dividends](https://simplywall.st/discover/investing-ideas/207/upcoming-dividends/us)

**4 listas QUALITY** (as que filtram por balanço/gestão/track-record — espírito Buffett):
- [Solid Balance Sheet and Fundamentals](https://simplywall.st/discover/investing-ideas/10146/solid-balance-sheet-and-fundamentals/us)
- [U.S. Spotless Management Stocks](https://simplywall.st/discover/investing-ideas/1766/spotless-management/us)
- [Sustainable Track Record](https://simplywall.st/discover/investing-ideas/419982/sustainable-track-record/us)
- [U.S. Big Green Snowflakes](https://simplywall.st/discover/investing-ideas/206/big-green-snowflakes/us)

**5 listas VALUE** (deep value, descontados ao FCF):
- [U.S. Value Investment Stocks: The Intelligent Investor](https://simplywall.st/discover/investing-ideas/249/the-intelligent-investor/us)
- [U.S. Undervalued Stocks Based On Cash Flows](https://simplywall.st/discover/investing-ideas/168/undervalued-stocks-based-on-cash-flows/us)
- [U.S. Undiscovered Gems With Strong Fundamentals](https://simplywall.st/discover/investing-ideas/152/undiscovered-gems-with-strong-fundamentals/us)
- [U.S. Buy the Dip Stocks](https://simplywall.st/discover/investing-ideas/1602/buy-the-dip/us)
- [U.S. Undervalued Small Caps with Insider Buying](https://simplywall.st/discover/investing-ideas/16951/undervalued-small-caps-with-insider-buying/us)

### 9b. As páginas SWS por ticker (TIER A + TIER B)

**TIER A — adicionar/já watchlist:**
- [IBM — Simply Wall St](https://simplywall.st/stocks/us/tech/nyse/ibm) · [IBM — Yahoo Finance](https://finance.yahoo.com/quote/IBM)
- [PPG — Simply Wall St](https://simplywall.st/stocks/us/materials/nyse/ppg) · [PPG — Yahoo Finance](https://finance.yahoo.com/quote/PPG)
- [AOS — Simply Wall St](https://simplywall.st/stocks/us/capital-goods/nyse/aos) · [AOS — Yahoo Finance](https://finance.yahoo.com/quote/AOS)
- [RPM — Simply Wall St](https://simplywall.st/stocks/us/materials/nyse/rpm) · [RPM — Yahoo Finance](https://finance.yahoo.com/quote/RPM)

**TIER B — pharma de qualidade com desconto / cash-cow:**
- [MRK — Simply Wall St](https://simplywall.st/stocks/us/pharmaceuticals-biotech/nyse/mrk) · [MRK — Yahoo Finance](https://finance.yahoo.com/quote/MRK)
- [GILD — Simply Wall St](https://simplywall.st/stocks/us/pharmaceuticals-biotech/nasdaq/gild) · [GILD — Yahoo Finance](https://finance.yahoo.com/quote/GILD)
- [BMY — Simply Wall St](https://simplywall.st/stocks/us/pharmaceuticals-biotech/nyse/bmy) · [BMY — Yahoo Finance](https://finance.yahoo.com/quote/BMY)
- [BKE — Simply Wall St](https://simplywall.st/stocks/us/retail/nyse/bke) · [BKE — Yahoo Finance](https://finance.yahoo.com/quote/BKE)
- [AMP — Simply Wall St](https://simplywall.st/stocks/us/diversified-financials/nyse/amp) · [AMP — Yahoo Finance](https://finance.yahoo.com/quote/AMP)

> Se algum link SWS por ticker der 404 (o slug do path varia), entra pela lista relevante de §9a e clica no nome na tabela — chegas à mesma página. O Yahoo Finance é sempre fallback garantido.

### 9c. Índice completo das 48 listas SWS

`data/sws_lists_index.json` no repositório — todas as 48 URLs. Tudo o que segue está cached em `data/sws_scrape/<id>_<slug>.json` (47 OK; 1 falhou: `the-future-is-online`, confirmado vazio no site).

### 9d. Documentos irmãos no vault

- [[SWS_Consensus_Memorandum_2026-05-11_overnight]] — o memo-mãe (47 listas, 990 tickers, consensus completo)
- [[DRIP_Shortlist_2026-05-11]] — a nossa shortlist DRIP original (sem SWS, só nossa filosofia)
- [[Manual_de_Direcao]] — o "como falar" com o sistema
- `obsidian_vault/Clippings/` — os 4 PDFs SWS que tu trouxeste originalmente:
  - `103 U.S. Stocks - Dividend Powerhouses (3%+ Yield)`
  - `4 U.S. Stocks - Value Investment Stocks The Intelligent Investor`
  - `61 U.S. Stocks - Top High Growth Tech & AI Stocks - Spotless Financials`
  - `68 U.S. Stocks - Growing Dividend Payers with 2-5% yield`
