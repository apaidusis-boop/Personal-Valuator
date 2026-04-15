# Padrões Arquiteturais a Portar

Sumário dos padrões do `vendor/skill-financial-analyst/` que vale a pena
reutilizar quando se construir o lado US. Cada padrão tem exemplo de onde
vive no repo deles e sugestão de onde encaixa no nosso stack.

## 1. Resilient fetch com fallback chain

**No repo deles:** `scripts/api_caller.py` (117 linhas)

Função `call_api(source_list, endpoint, params)` tenta cada fonte por ordem,
captura exceções, regista no log qual fonte respondeu, e devolve o primeiro
resultado válido. Se todas falharem, devolve `None` e regista o erro composto.

**Onde encaixa no nosso stack:** `fetchers/_resilient.py` (novo).

Já fazemos fallback manual em `fetchers/fiis_fetcher.py` (fiis.com.br →
Status Invest). Ao portar, extraímos a lógica para um helper genérico:

```python
# Pseudocódigo alvo
from fetchers._resilient import resilient_fetch

result = resilient_fetch(
    sources=[fetch_yfinance, fetch_finnhub, fetch_fmp],
    ticker="KO",
    field="dividend_yield",
    log_event="us_div_yield_fetch",
)
```

Ganhos: uniformidade de logging, eliminação de código duplicado, facilidade
de adicionar fontes novas.

## 2. Confidence score

**No repo deles:** `scripts/scoring.py` (846 linhas, função `calculate_confidence`)

Cada análise devolve não só um score mas também um nível de confiança
(HIGH/MEDIUM/LOW) baseado na **fração de dados disponíveis sobre o total
esperado**. Ex: se 9/10 inputs vieram, confidence=HIGH; se 5/10, MEDIUM.

**Onde encaixa no nosso stack:** estender `scoring/engine.py aggregate()`.

Hoje devolvemos `(score: float, passes_screen: bool)`. Podemos estender:

```python
def aggregate(details: dict) -> dict:
    verdicts = [c["verdict"] for c in details.values()]
    applicable = [v for v in verdicts if v != "n/a"]
    passes = sum(1 for v in applicable if v == "pass")
    total = len(verdicts)
    score = passes / len(applicable) if applicable else 0.0
    coverage = len(applicable) / total if total else 0.0
    confidence = "HIGH" if coverage >= 0.8 else "MEDIUM" if coverage >= 0.5 else "LOW"
    return {
        "score": round(score, 4),
        "passes_screen": all(v == "pass" for v in applicable),
        "coverage": round(coverage, 2),
        "confidence": confidence,
    }
```

Isso previne o caso falso-positivo que vimos com PMLL11 — score 1.0 com só
2 critérios aplicáveis (coverage 40% → confidence LOW → avisa para não
confiar cegamente).

## 3. Composite score ponderado (Fundamental + Technical + Sentiment)

**No repo deles:** `scripts/scoring.py` — composite 40/30/30.

Combinam 10 fatores fundamentais, 8 técnicos, 5 de sentimento, cada um
normalizado para 0–10, e agregam com pesos.

**Para nós:** **não portar cegamente.** A filosofia Graham/Buffett/DRIP é
explicitamente fundamentalista de longo prazo. Indicadores técnicos são
contexto de *entrada*, não de decisão de compra/venda.

**Compromisso útil:** fundamental continua a ser `pass/fail/n/a` (binário e
honesto). Camada técnica entra como **score informativo separado**, não
como parte do screen. Ex: relatório diz "ITSA4 passa o screen Graham
(score 1.0) e indicadores técnicos sugerem oversold (RSI=28) → bom timing
para entrada gradual".

## 4. TTL cache por tipo de dado

**No repo deles:** `scripts/data_cache.py` (783 linhas)

SQLite-like com TTLs diferentes por categoria:
- Preços intraday: 5 min
- Preços daily: 1 dia
- Fundamentals: 1 dia
- News: 30 min
- Analyst ratings: 1 dia

**Onde encaixa no nosso stack:** `fetchers/cache_policy.py` (já existe).

Confirmar se o nosso cache_policy tem a granularidade necessária. Os valores
deles são um bom sanity check.

## 5. Position sizing & risk management

**No repo deles:** `scripts/entry_exit.py` (448 linhas)

Calcula:
- **Stop loss** baseado em ATR(14), swing low, Bollinger inferior — usa o
  mais apertado dos três
- **Position size** a partir de: `capital × risk% / (entry - stop)`
- **Risk/reward ratio** para cada par entry/target

**Onde encaixa no nosso stack:** `analytics/entry_exit.py` (novo).

Vale portar *adaptado ao DRIP*:
- Entries: agressivo (preço actual) / moderado (pullback para SMA50) /
  conservador (preço Graham, margem 20%)
- Stop loss: BVPS ou preço Graham × 0.85 (não ATR — DRIP não usa stops
  técnicos, usa thesis breaks)
- Targets: não aplicável (hold forever); substituído por "zone de sobrevalue"
  onde pode-se considerar trim

## 6. Sector rotation com relative strength

**No repo deles:** `scripts/sector_rotation.py` (415 linhas)

Tracks 11 ETFs sectoriais vs SPY, calcula RS over 1w/1m/3m, aplica modifier
ao composite score (ações em sectores *momentum forte* ganham +0.3, sectores
*weakening* levam -0.3).

**Onde encaixa no nosso stack:** `analytics/sector_rotation.py` (novo).

Para US é port directo. Para BR precisa mapeamento setorial próprio (B3 não
tem ETFs setoriais tão limpos — há alguns iShares tipo BOVA11 / DIVO11 mas
setores específicos requerem agregação manual de tickers).

## 7. Estrutura de output estruturado (JSON + markdown)

**No repo deles:** `scripts/run_deep_dive.py`, `run_portfolio_review.py`

Cada análise devolve um dict aninhado completo (raw data), **e
paralelamente** gera uma versão markdown para leitura humana.

**Onde encaixa no nosso stack:** já fazemos. `scoring/engine.py` devolve
`details: dict` JSON-persistido. Podemos alinhar o formato deles para
facilitar composição futura de relatórios multi-ticker.

## 8. Macro calendar integrado

**No repo deles:** `scripts/macro_calendar.py` (408 linhas)

Lista próximos eventos macro (FOMC, CPI, jobs, earnings dates) e injeta
contexto no topo dos relatórios.

**Onde encaixa no nosso stack:** `analytics/calendar.py` (novo).

Para BR é trivial: COPOM dates (já temos SELIC decisions no BCB), IPCA
release dates, calendário de earnings da watchlist. Para US é direto do
código deles (fonte: Finnhub earnings calendar, FOMC dates hardcoded).

## 9. Usage tracking para rate limits

**No repo deles:** `scripts/usage_tracker.py`

Conta chamadas por API, por dia. Avisa quando aproxima do limite. Persiste
em ficheiro local.

**Onde encaixa no nosso stack:** `fetchers/_usage.py` (novo, opcional).

Só relevante quando se começa a usar APIs com tiers (Alpha Vantage tem
25/dia, é apertado). Enquanto for só yfinance + SEC EDGAR, não é crítico.

## O que **não** portar

- **Sentiment social (ApeWisdom, StockTwits)** — ruído para estratégia
  de longo prazo. Mantém-se fora da filosofia.
- **Congress trades** — gimmick interessante mas não determinante para
  Buffett. Skip.
- **Trading swing (entries próximos, stops técnicos)** — conflitua com DRIP.
- **Print-based CLI output** — nós usamos HTML Plotly + SQLite, melhor.
- **pandas-ta dependência** — podemos reimplementar os 5–6 indicadores
  que interessam (SMA, EMA, RSI, MACD, ATR, Bollinger) em pandas puro.
  Evita dependência pesada.
