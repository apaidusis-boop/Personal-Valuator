# Memorandum — próxima sessão
**Criado**: 21/04/2026
**Propósito**: rever quando voltar a casa.

---

## 1. Transcrição verbatim do pedido do user (21/04 fim-de-sessão)

> Quero que faça o seguinte. Busque maneiras de ser mais optimal, ainda mais no
> número de tolkens (Quero eles registados para termos parametors de melhora).
>
> Me demorou 10 minuitos para termos essas informações. Precisamos verificar
> toda as Watchlists, por exemplo, ABBV é uma solução viável para esse momento,
> E Visa? PG é o melhor? GREK para DRIP é difícil, dividendos são regulares??
>
> Precisamos pesquisar sobre Divided King + Aristocrats para o caso USA e
> salvar isso tambémm para que os preços possam ser acompanhados ao longo
> prazo para surgir buys e tudo mais.
>
> SALVE ISSO TUDO O QUE ESCREVI COMO MEMORADUM PARA SER REVISTO QUANDO EU
> VOLTAR PARA CASA.

---

## 2. Decomposição em tarefas accionáveis

### T1 — Instrumentação de tokens / latência
- **Problema**: sessão de 10 min para chegar à recomendação $3k sem métricas de custo.
- **Propor**: hook de logging por turn (tool-call count, output-size approximation, wall-time). Tabela CSV em `logs/session_metrics.csv`. Baseline desta sessão: estimar a posteriori e registar como linha 1.
- **Potenciais ganhos** (antes de implementar, já identificados):
  - Batch scan corre `_ensure_deep_fundamentals` sequencialmente para 32 tickers → paralelizar via ThreadPool (5–10× em runs com fetch).
  - `portfolio_report.py` corre `dy_percentile` por holding no tempo de render → cache diária em tabela `analytics_cache`.
  - `research.py --holdings` recomputa altman/piotroski já persistidos → considerar persistir score com TTL (1 dia).
  - Respostas longas em markdown devem ir para ficheiro em `reports/` + apontar ao user; só mostrar summary no chat.

### T2 — Verificar watchlists com tickers específicos levantados pelo user
- **ABBV** — watchlist US (já aparece como near-miss no briefing, fail: P/E). Rodar `scripts/research.py ABBV --md`, avaliar se faz sentido em substituição/complemento de JNJ (ambos pharma, mas ABBV tem yield mais alto normalmente).
- **V (Visa)** — não está na watchlist. Adicionar a `config/universe.yaml` (sector Financials / Payments), fetch fundamentals, scoring. Historicamente: aristocrat 16y+ (2008 IPO, streak short mas perfeito), ROE ~50%, DY baixo (~0.7%). Avaliar se fit DRIP ou growth.
- **PG é o melhor?** — comparar PG vs outros Kings via `scripts/compare_tickers.py PG KO JNJ ...`. Pergunta operacional: o trigger PG ADD é solid ou há alternativas com DY pct mais baixo (i.e. ainda mais cheap vs histórico)?

### T3 — GREK: regularidade de dividendos
- GREK é MSCI Greece ETF. Dividendos dependem dos constituintes (Banco Nacional da Grécia, OPAP, etc.) → **distribuição é tipicamente semestral ou anual, não trimestral**. Confirmar na DB:
  ```
  SELECT ex_date, amount FROM dividends WHERE ticker='GREK' ORDER BY ex_date DESC LIMIT 20
  ```
  Avaliar se é compatível com DRIP filosofia (que assume fluxo regular).
- Se irregular, reclassificar intent GREK de `drip` para `tactical` e retirar da pool DRIP.

### T4 — Construir tabela canónica de Dividend Kings + Aristocrats US
- **Dividend Kings**: ≥50 anos de aumento consecutivo de dividendo. ~45 nomes (PG, JNJ, KO, EMR, 3M, CINF, DOV, GPC, HRL, LOW, NDSN, NWN, PH, SWK, SYY, WMT, BDX, ABBV-pre-split, ...).
- **Dividend Aristocrats**: S&P 500 + ≥25 anos de aumento consecutivo. ~68 nomes.
- **Salvar em**: novo `config/kings_aristocrats.yaml` com `ticker, name, sector, streak_years, kind (king|aristocrat)`. Importar em `config/universe.yaml` como watchlist US expandida.
- **Loop longo-prazo**: cron diário já corre `daily_update.py` → vai automaticamente popular prices + fundamentals destes nomes. Trigger engine vai flagar entry windows (DY P75+ próprio, price drop ≥-15%, etc.) sem intervenção manual.
- **Fonte**: Wikipedia Dividend Kings + S&P 500 Dividend Aristocrats (lista curada, actualizada 1× ano pela S&P).

### T5 — Decisão pendente sobre os $3k USD (da análise desta sessão)
- Recomendação em vigor foi **Opção A**:
  ```
  ACN  4 sh × $195.59 = $  782
  GREK 11 sh × $ 71.27 = $  784   ← REVISITAR após T3 (regularidade div)
  TFC  12 sh × $ 50.58 = $  607
  HD    2 sh × $347.83 = $  696
  PG    1 sh × $144.27 = $  144
                          ------
                        ~$3013
  ```
- **Não executar até**: (a) T3 responder sobre GREK; (b) T2 responder se ABBV/V são melhores alternativas; (c) T4 alargar a watchlist para garantir que não há Dividend King cheap fora do radar actual.

---

## 3. Ordem de execução sugerida na próxima sessão

1. **T1 primeiro** (5 min): add hook de métricas. Toda a próxima sessão já é medida.
2. **T4 segundo** (15 min): popular lista Kings/Aristocrats em yaml, carregar fundamentals. Dá-nos o universe completo *antes* de decidir onde aplicar os $3k.
3. **T3** (2 min): query SQL para GREK div history.
4. **T2** (10 min): research.py em ABBV + V (V ainda precisa fetch inicial) + compare_tickers.py nos Kings.
5. **T5 revisar** (5 min): opção A ainda válida? Ou substituir GREK por Dividend King cheap descoberto em T4?

Total estimado: ~40 min. Se T1 instrumentar bem, medimos e iteramos.

---

## 4. Baseline aproximado da sessão 21/04 (para comparar)

- **Wall time**: ~10 min (percepção do user).
- **Tool calls**: ~50+ (Bash, Read, Edit, TaskCreate/Update, Grep).
- **Commits**: 2 (Phase K, Phase L).
- **Output artifacts**: 1 research_batch, 1 weekly report, 1 memo (este).
- **Limitação conhecida**: sem métrica de tokens; instrumentar em T1.

---

**Status**: aguardar regresso do user. Nenhuma acção pendente do meu lado antes da próxima sessão.
