# Fair Value Engine — Audit + Forward Overlay (US compounders)

> Sessão 2026-05-11. Pedido do user: auditar `scoring/fair_value.py`, montar uma
> camada *forward-aware* / *quality-aware* para os compounders DRIP US, corrigir
> o bug do intangible gate (KO a sair SELL), e re-emitir recomendações de aporte.
> Carteiras BR/US isoladas — este doc é **só US**.

Relacionado: [[ROADMAP]] · [[CONSTITUTION_Pessoal]] · `scoring/fair_value.py` ·
`scoring/_safety.py` · `config/safety_margins.yaml` · `scoring/moat.py` ·
memory `moat_engine_shipped` / `session_2026-05-09_bug_sweep`.

---

## 1. Como o engine funciona hoje (audit)

`scoring.fair_value.compute(ticker, market)` produz um **tecto Buffett-Graham**, não
uma avaliação intrínseca. Pipeline:

### 1.1 Consensus fair (`fair_price`)

| Caso (market × sector) | Fórmula | Comentário |
|---|---|---|
| BR não-banco, não-FII | `√(22.5 · EPS · BVPS)` (Graham Number) | clássico Graham |
| BR banco | `min(EPS×10, BVPS×1.5)` | os dois tectos do screen BR bank |
| BR FII | `VPA` (NAV anchor) | lê `fii_fundamentals.vpa` |
| US REIT | `BVPS × 2` (proxy) | **crude** — devia ser P/AFFO |
| US banco (whitelist `_US_BANK_TICKERS`) | `EPS × 12` | mid-cycle multiple |
| US não-banco "modern compounder" (ROE≥25% **e** streak≥10y) | `EPS × 20` | larga a perna BVPS×3 |
| US não-banco resto | `min(EPS×20, BVPS×3)` (Buffett ceiling) | a perna BVPS×3 domina nomes com buyback |

Inputs: `eps` e `bvps` do snapshot `fundamentals` mais recente (preferindo
`fundamentals_from_filings` quando existe; com override para mediana yf+Fundamentus
se `data_confidence` flag `cvm_outlier_eps`). **100% backward-looking** — TTM / último
snapshot. Zero forward estimates, zero consenso de analistas, zero owner-earnings,
zero crescimento terminal explícito, zero cenários.

### 1.2 Safety triplet (`scoring._safety.build_triplet`)

`our_fair = consensus_fair × (1 − margin)`, onde `margin` vem de
`config/safety_margins.yaml` por sector (Compounders staples/health 18%, Bancos
top-tier 25-27%, Cyclicals 35-42%, REITs US 16%, FIIs 10-14%). `sell_above =
consensus × 1.15`. Action vocab 6-stance: STRONG_BUY ≤ our_fair×0.90 < BUY ≤ our_fair
< HOLD ≤ consensus < TRIM ≤ sell_above < SELL.

### 1.3 Gates aplicados ao action (depois do triplet)

1. **Confidence** — `disputed` rebaixa BUY/STRONG_BUY→HOLD; `single_source` rebaixa STRONG_BUY→BUY.
2. **Intangible warning** — se `intangible_pct_assets ≥ 0.25` *ou* `tangible_book_value < 0`:
   SELL/TRIM→HOLD, STRONG_BUY→BUY, confidence -1 notch. (Rationale: brand off-balance ⇒
   o tecto sobre BVPS é enviesado *baixo* ⇒ o sinal SELL é não-fiável. PG/JNJ/KO são os
   casos canónicos.)
3. **Distress vetoes** — Altman Z distress ⇒ força SELL; Piotroski F fraco ⇒ rebaixa BUY→HOLD.
   (Excl. bancos/REITs/FIIs.)
4. **Macro overlay** — `analytics.regime` + `config/macro_sector_fit.yaml`: `hard_hold`
   força HOLD, `downgrade` rebaixa um notch, `reinforce` só anota.

### 1.4 Onde falha para os compounders DRIP

| Falha | Efeito | Quem é vítima |
|---|---|---|
| **EPS×20 é um *tecto de disciplina de preço*, não valor intrínseco** | Não capta ROIC durável, moat de marca, pricing power, owner-earnings vs EPS GAAP, redução de share count, crescimento terminal. Um compounder de moat largo merece 22-28× porque o fluxo é mais certo *e* cresce — o modelo trata isso como "caro". | KO, PG, JNJ, HD, ACN |
| **Perna BVPS×3 domina o `min()` em nomes com buyback / goodwill** | BVPS artificialmente baixo ⇒ `buffett_ceiling` cospe um número absurdo. ACN: `min(EPS×20=$244, BVPS×3=$152)` → $152, quando o nome negocia a 12× fwd (barato). | ACN, BLK, IBM, V, MA |
| **Gate `modern_compounder` com threshold ROE ≥ 25% binário** | ACN ROE 24.8% — falha por 0.2pp ⇒ apanha a perna BVPS×3. Cliff edge. | ACN (e qualquer 23-25% ROE) |
| **`reit_pb_proxy = BVPS×2` ignora AFFO** | Para net-lease (O) sobrestima — O a P/AFFO ~14.7× já está "fairish/cheapish", mas o engine diz STRONG_BUY a partir de um BVPS×2 = $86 sem fundamento. | O e todos REITs |
| **`us_bank_pe12` usa o *screen ceiling* (P/E ≤ 12) como *fair value*** | Para um banco best-in-class (JPM, ROE 16.5%, ~13× histórico normal) o fair devia ser ~13-14× EPS normalizado, não 12×. ⇒ SELL espúrio a $302. | JPM (e BAC/WFC top-tier) |
| **Backward-looking total** | Para JNJ o P/E trailing 25.6× é distorcido pelos charges de talco/litígio; fwd P/E 17.4×. O engine vê o trailing. | JNJ (e qualquer nome pós-charge) |

---

## 2. Bug do intangible gate — diagnóstico e fix (✅ feito, commit `2abbb59`)

**Sintoma**: KO a sair `SELL` (consensus $63.5, sell_above $73, preço $78) apesar do
fix de 2026-05-09 que era suposto rebaixar SELL→HOLD para nomes brand-heavy.

**Causa raiz**: o gate só dispara quando `fundamentals.intangible_pct_assets` /
`tangible_book_value` estão preenchidos — e só `scripts/backfill_intangibles.py` os
preenche. O refresh diário de fundamentals (`daily_run`) **insere linhas novas sem
essas colunas** ⇒ entre backfills o gate fica silenciosamente morto. Foi exactamente
assim que KO/PG/JNJ regrediram para SELL/TRIM em 2026-05-10.

**Fix aplicado** (`scoring/fair_value.py`):
- Re-corrido `backfill_intangibles.py --us-only` (107 tickers re-enriquecidos; usa o
  `.venv` que tem `yfinance`, não o Python311 global).
- Adicionado `_HIGH_INTANGIBLE_TICKERS` (frozenset, mirror de `_US_BANK_TICKERS`):
  KO/PEP/PG/CL/KMB/MDLZ/KHC/GIS/HSY/K/SJM/MO/PM/MCD/SBUX/YUM/NKE/EL/CLX/CHD/JNJ/ABT/
  MMM/HON/V/MA/ACN/IBM/HD/LOW. Quando as colunas medidas estão NULL e o ticker está
  nessa lista, o gate dispara na mesma. Só rebaixa SELL/TRIM→HOLD (direcção conservadora).
- Verificado: `KO` com intangibles reais → HOLD (gate medido, ipa 27%); `KO` com
  intangibles removidos via monkeypatch → HOLD (fallback); `TSM` (não na lista, baixos
  intangibles) → SELL inalterado.

**Resultado pós-fix** (recomputado 2026-05-11):

| Ticker | Antes | Depois | Porquê |
|---|---|---|---|
| KO | SELL | **HOLD** | intangible_pct_assets 26.7% ≥ 0.25 |
| PG | TRIM | **HOLD** | intangibles / tbv backfilled |
| JNJ | SELL | **HOLD** | ipa 49.8%, tbv −$17.6B |
| ACN | SELL | **HOLD** | ipa 38.2% |
| HD | TRIM | **HOLD** | ipa 31.1%, tbv −$19.9B |
| BLK | SELL | **HOLD** | ipa 37.2%, tbv −$7.4B |
| JPM | SELL | SELL | banco — sem intangible gate (ver §1.4; precisa de fix de multiple) |
| O | STRONG_BUY | STRONG_BUY | REIT — sem intangible gate (precisa de fix AFFO) |

**Dívida residual** (não corrigida aqui — concern separado): o `daily_run.bat` devia
re-correr `backfill_intangibles.py` depois do refresh de fundamentals, senão a lista
fallback é o único safety net. Sugerido como passo de manutenção, não bloqueante.

---

## 3. Overlay forward-aware — 8 compounders DRIP (passo 2)

Metodologia (honest-conservative, memory `feedback_honest_projections`): DCF 2-estágios
sobre **forward EPS** como proxy de owner-earnings, crescimento explícito 10a com fade
linear para `g2`, terminal Gordon. Discount rate por perfil de risco. Cruzado com (a) o
nosso engine, (b) consenso de analistas (yfinance, n=16-33), (c) o DCF da FMP onde
disponível (free tier só serviu KO/JNJ/JPM; o DCF da FMP é agressivo e em bancos é lixo).

| TK | Preço | Engine `our_fair` / consensus / action | DCF conserv. (impl. P/E) | Consenso analistas (n) | FMP DCF | Leitura |
|---|---|---|---|---|---|---|
| **KO** | $78.4 | $52.1 / $63.5 / **HOLD** | **$66** (19.4×) | $85.8 (23) buy | $106.9 | Ligeiramente rico (22.5× fwd p/ 5-6% growth). HOLD correto. Não é "add now". |
| **PG** | $146.4 | $107.8 / $131.5 / **HOLD** | **$130** (18.6×) | $163.8 (22) buy | — | Rico (20.6× fwd p/ ~4-5%). HOLD. Esperar <$130. |
| **JNJ** | $221.3 | $142.0 / $173.2 / **HOLD** | **$195–236** (≈18.6×) | $252.4 (24) buy | $346.8 | Trailing P/E 25.6× distorcido por charges; **fwd 17.4× é razoável**. Fair→ligeiramente barato. Add em fraqueza. |
| **ACN** | $180.4 | $115.5 / $148.1 / **HOLD** | **$245** (16.9×) | $249.2 (26) buy | — | **Barato** — 12.1× fwd p/ compounder capital-light ROE 25%. Engine enviesado baixo (perna BVPS×3 + falhou modern_compounder por 0.2pp). **Top "add now".** |
| **HD** | $317.5 | $213.4 / $284.5 / **HOLD** | **$260** (16.2×) | $406.6 (33) buy | — | ~18% rico no meu DCF; vento contra de housing (EPS −14%). PT $407 dos analistas assume recuperação cíclica — optimista demais. HOLD. |
| **BLK** | $1085 | $606.6 / $777.7 / **HOLD** | **$1090** (19.5×) | $1254 (16) | — | ≈ fairly valued. 17.9× fwd p/ ~8-12% (pivot GIP/HPS private markets). HOLD; intangible gate resgatou-o do SELL. |
| **JPM** | $302.1 | $198.2 / $254.1 / **SELL** | ~$280–310 (≈13× EPS norm. ~$22) | $342.3 (22) buy | $750 (lixo) | Não está barato (~13× é o topo do range histórico 10-13×) **mas SELL a $302 é exagero**. Fair ≈ HOLD. Engine usa o screen ceiling (×12) como fair — devia ser ×13-14 p/ best-in-class. |
| **O** | $61.9 | $72.4 / $86.2 / **STRONG_BUY** | ~$65–72 (15.5-17× AFFO ~$4.2) | $68.5 (20) hold | — | Barato-ish mas não "STRONG BUY". Engine sobrestima via BVPS×2. Leitura honesta: **BUY/accumulate** para sleeve income. |

Moat scores (`scoring/moat.py`, sub-scores pricing/capeff/runway/scale): KO 10/9/6/9
(≈8.5 STRONG) · PG 9/9/6/8 (≈8 STRONG) · JNJ 10/7/8/10 (≈8.75 STRONG) · ACN 8/10/8/6
(≈8 STRONG) · HD 8/10/5/5 (≈7 NEUTRAL-STRONG) · BLK/JPM/O N/A (excl. Banks/REITs).

**Padrão**: o engine acerta o *sinal de disciplina de preço* (KO/PG/HD genuinamente
não estão baratos a 20-22× fwd) mas erra grosseiramente onde a perna BVPS domina (ACN)
ou onde usa o screen ceiling como fair value (JPM, O). A pré-fix dramatização ("SELL
−33%" em KO/JNJ/JPM) está corrigida; o que falta é capturar o *prémio de qualidade legítimo*
≈ 3-5 turns de P/E para os compounders de ROIC durável.

---

## 4. Proposta de fusão (passo 3 — aguarda decisão do user)

Não substituir o engine. Fundir uma lente forward por cima do tecto conservador.

### Opção A — novo método `compounder_dcf` dentro do `min()`/substituindo a perna fraca
- Para US não-banco com `moat_score ≥ 7` **e** `ROIC ≥ 15%` (de `ii roic`): em vez de
  `min(EPS×20, BVPS×3)`, usar `compounder_dcf = 2-stage DCF(fwd EPS, g conserv., r sectorial, g2 2.5-3%)`,
  com `fair = min(compounder_dcf, EPS × 25)` (tecto de sanidade — nunca acima de 25× owner-earnings).
- Resolve ACN (sobe de $148 → ~$240), elimina o cliff edge do threshold ROE binário,
  mantém disciplina (tecto 25×).
- **Contra**: introduz forward estimates (fonte? yfinance `forwardEps` é frágil; precisa
  de fallback). Mais um caminho no `compute()`. Precisa de `g` por nome (config nova).

### Opção B — camada separada `analytics.fair_value_forward` que faz blend ponderado
- O `compute()` actual fica intocado. Nova função emite `forward_fair = w·compounder_dcf
  + (1−w)·analyst_consensus_PT` e o orquestrador/dossier mostra **as duas leituras lado a lado**
  (`our_fair` conservador vs `forward_fair` quality-aware), mais um `blended_action`.
- **Pró**: zero risco de regressão no engine existente; honesto sobre incerteza (mostra
  o range); fácil de A/B testar contra os verdicts.
- **Contra**: duas verdades a conviver — precisa de UI/dossier disciplinado para não confundir.

**Recomendação interna**: Opção B primeiro (camada aditiva, surgical, testável), com a
porta aberta para promover a Opção A se o blend provar estável em ~1-2 meses (calibração
Phase FF/GG). Respeita Karpathy: simplicity first, surgical, goal-driven (critério de
done = `forward_fair` de ACN entre $220-260; KO entre $62-70).

### Estado: Opção B já construída (protótipo, 2026-05-11)

`analytics/fair_value_forward.py` — stand-alone, **não wired** no engine/daily_run/ii.
Emite `obsidian_vault/Bibliotheca/FairValue_Forward_<DATE>.md`. Método: DCF 2-estágios
sobre owner earnings (base = forward EPS consenso, ou mediana NI 3y × conversão de caixa
floored 85%); g cortado por sector (defensivas 6%, resto 8%); fade→2,5-3%; desconto
8,5-9,5%; banda de sanidade 16-25× OE. Bancos: EPS_norm ×13-14 (em vez do ×12 screen
ceiling). REITs: AFFO × P/AFFO (`_AFFO_OVERRIDE` hand-maintained — calibrar por sub-sector).
Salta foreign-ccy reporters (TSM/XP), growth picks (NU/PLTR/TSLA), holdcos/ETFs (BN/BRK-B/GREK).
yfinance opcional (só `.venv` tem) → correr `.venv/Scripts/python.exe -m analytics.fair_value_forward`.

Output 2026-05-11 (forward fair / leitura, vs engine `our_fair`/action):
ACN $238 **ADD** (engine $115/HOLD) · JNJ $251 **ADD** ($142/HOLD) · O $68 FAIR ($72/STRONG_BUY) ·
JPM $284 RICH ($198/SELL) · KO $69 RICH ($52/HOLD) · PG $122 RICH ($108/HOLD) ·
BLK $971 RICH ($607/HOLD) · HD $261 EXPENSIVE ($213/HOLD) · AAPL $153 EXPENSIVE ($121/SELL).
Confirma o padrão: ACN é o "add now"; KO/PG/HD/JPM/BLK não estão baratos a preço corrente.

**Pendente da tua decisão**: promover a Opção A (método `compounder_dcf` dentro do engine,
gated por moat≥7 & ROIC≥15%, tecto 25× OE) — ou ficar na Opção B (lado-a-lado, como está).

---

## 5. Re-emissão de recomendações DRIP US — aporte ~$500 (passo 5)

Com a lente forward + o fix do gate:

| Ticker | Veredito de aporte | Racional |
|---|---|---|
| **ACN** | **ADD NOW** (prioridade 1) | 12.1× fwd p/ compounder capital-light, ROE 25%, FCF forte, moat ≈8. ~25-35% abaixo do fair tanto no meu DCF como no consenso. O sinal SELL do engine era um artefacto da perna BVPS×3. |
| **JNJ** | **ADD on weakness** (<$210; prioridade 2) | 17.4× fwd é razoável; overhang de talco largamente resolvido; moat ≈8.75; DY ~3%. Fair-a-ligeiramente-barato. |
| **O** | **ACCUMULATE** para sleeve income (BUY pequeno OK) | P/AFFO ~14.7× vs histórico 16-19×; DRIP-friendly (mensal). Não é "STRONG BUY" — entrar em tranches. |
| **JPM** | **HOLD** (não adicionar a $302) | ~13× é o topo do range; qualidade excelente mas sem margem. SELL do engine é exagero; mas também não é compra. Esperar <$270. |
| **KO** | **HOLD** (não adicionar) | 22.5× fwd p/ 5-6% growth é prémio cheio. Dividend bulletproof mas o preço já paga isso. <$70 seria interessante. |
| **PG** | **HOLD** (não adicionar) | 20.6× fwd p/ ~4-5%. <$130. |
| **HD** | **HOLD** (não adicionar) | ~18% rico no meu DCF; vento contra de housing. PT $407 dos analistas é optimista. <$280. |
| **BLK** | **HOLD** (não adicionar) | ≈ fairly valued; pivot private-markets interessante mas já no preço. |

**Decisão para o aporte de ~$500**: alocar a **ACN** (principal), com ordem-limite
escalonada em **JNJ <$210** e **O em tranches** como destino secundário se ACN recuperar
antes de executar. Nenhum dos outros 5 justifica entrada a preço corrente.

> ⚠️ Estes vereditos usam o DCF conservador *deste doc* + consenso, não ainda um método
> integrado no engine. A persistência em `fair_value` continua a mostrar `our_fair`
> (tecto conservador) — o overlay forward vive aqui até a Opção A/B ser decidida.

---

## Sources / dados

- Engine: `scoring/fair_value.py`, `scoring/_safety.py`, `config/safety_margins.yaml`, `scoring/moat.py` (lidos 2026-05-11).
- DB: `data/us_investments.db` — `fundamentals` (snapshot 2026-05-10, intangibles re-backfilled 2026-05-11), `fair_value` (recomputado 2026-05-11), `prices` (2026-05-08 close).
- Consenso de analistas: yfinance `.info` (`targetMeanPrice`, `numberOfAnalystOpinions`, `forwardEps`, `forwardPE`) — fetch 2026-05-11.
- FMP MCP (claude.ai): `discountedCashFlow/dcf-advanced` e `analyst/price-target-consensus` — só KO/JNJ/JPM passaram no free tier.
- Commit do fix: `2abbb59` "fair_value: make intangible gate robust to stale balance-sheet columns".
