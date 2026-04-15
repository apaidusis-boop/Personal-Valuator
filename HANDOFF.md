# HANDOFF — investment-intelligence

Documento de passagem de contexto. Lê isto primeiro antes de continuar o trabalho noutra ferramenta (Warp, outra sessão de Claude Code, etc.).

---

## 1. O que é o projecto

Sistema pessoal de inteligência de investimentos para um investidor pessoa física. Estratégia **DRIP + Buffett/Graham**, dois mercados: **Brasil (B3)** e **EUA (NYSE/NASDAQ)**. Duas bases SQLite separadas por mercado, schema idêntico. Universo de tickers centralizado em `config/universe.yaml` — nunca hardcoded em Python.

Detalhes completos de filosofia, critérios, fontes e schema estão em **`CLAUDE.md`**. Lê esse ficheiro antes de tocar em código.

## 2. Estado actual (scaffolding concluído)

Já existe e está funcional:

```
investment-intelligence/
├── CLAUDE.md                    ✅ filosofia, critérios BR/US, schema, comandos
├── HANDOFF.md                   ✅ (este ficheiro)
├── .env.example                 ✅ template — BRAPI_TOKEN
├── .gitignore                   ✅ ignora .env, data/*.db, logs/, reports/
├── config/
│   └── universe.yaml            ✅ todos os tickers BR+US (carteiras + watchlists)
├── scripts/
│   └── init_db.py               ✅ cria/migra ambas as DBs (idempotente)
├── data/
│   ├── br_investments.db        ✅ schema aplicado
│   └── us_investments.db        ✅ schema aplicado
├── fetchers/                    ⬜ vazio
├── scoring/                     ⬜ vazio
├── monitors/                    ⬜ vazio
├── reports/                     ⬜ vazio
├── logs/                        ⬜ vazio
└── tests/                       ⬜ vazio
```

**Schema SQLite** (ambas as DBs): tabelas `companies`, `prices`, `fundamentals`, `scores`, `events`. Definição canónica em `scripts/init_db.py`.

## 3. Decisão de estratégia: piloto com UMA empresa

Em vez de implementar fetchers para 21 tickers de uma vez, decidimos **pilotar end-to-end numa única empresa** e só depois generalizar.

**Cobaia escolhida: `ITSA4` (Itaúsa PN)** — escolhida deliberadamente por ser *holding*, o que expõe edge cases logo de início:

- É holding → "Dívida líquida / EBITDA" é conceptualmente estranho (resultado vem de equivalência patrimonial de Itaú, Alpargatas, Dexco, Aegea...). O critério `Dív/EBITDA < 3x` pode não se aplicar — o motor de scoring precisa de saber dizer **`n/a`**, não apenas `pass`/`fail`.
- ROE estruturalmente mais baixo que banco operacional — calibra expectativa.
- DY historicamente alto e estável → bom teste do critério ≥ 6%.
- Graham Number pode enganar se brapi reportar EPS consolidado vs. controlador — **inspeccionar o campo cru antes de confiar**.
- Histórico de dividendos ininterrupto há décadas → valida facilmente o parser de histórico.

### Lição central do piloto

> **O motor de scoring tem de distinguir `pass` / `fail` / `n/a`.** O campo `passes_screen` final calcula-se ignorando os `n/a`. O `details_json` em `scores.details_json` deve registar, por critério, o valor observado E o veredicto.

## 4. Plano de ataque para o piloto ITSA4

Passos, em ordem. Cada passo deve ser validado manualmente antes de avançar para o próximo.

1. **`fetchers/brapi_fetcher.py`** — só ITSA4, todos os campos:
   - cotação actual + histórico diário
   - fundamentals trimestrais (EPS, BVPS, ROE, P/E, P/B, DY, dívida, EBITDA)
   - histórico de dividendos (para calcular `dividend_streak_years`)
   - persiste em `data/br_investments.db` nas tabelas `companies`, `prices`, `fundamentals`
2. **Inspecção manual da DB** — abrir com `sqlite3` ou DB Browser for SQLite, confirmar que cada coluna tem valor real e plausível. Anotar colunas em falta ou suspeitas. **Não avançar** sem isto.
3. **`scoring/engine.py`** — aplicar os 5 critérios BR (ver `CLAUDE.md`) a ITSA4. O output em `scores.details_json` deve ter a forma:
   ```json
   {
     "graham_number":    {"value": 12.3, "threshold": 22.5, "verdict": "pass"},
     "dividend_yield":   {"value": 0.071,"threshold": 0.06, "verdict": "pass"},
     "roe":              {"value": 0.13, "threshold": 0.15, "verdict": "fail"},
     "net_debt_ebitda":  {"value": null, "threshold": 3.0,  "verdict": "n/a", "reason": "holding company"},
     "dividend_streak":  {"value": 25,   "threshold": 5,    "verdict": "pass"}
   }
   ```
   `passes_screen` = todos os verdicts que não são `n/a` são `pass`.
4. **`fetchers/statusinvest_scraper.py`** — *só implementar se* o passo 2 revelar campos em falta na brapi (especialmente histórico longo de dividendos).
5. **`monitors/cvm_monitor.py`** — últimos N fatos relevantes de ITSA4 → tabela `events`.
6. **Mini-relatório markdown** só de ITSA4 — protótipo do futuro `scripts/weekly_report.py`, em `reports/pilot_itsa4.md`.

Só depois de tudo isto funcionar é que generalizamos para o resto do universo BR, e só depois atacamos o lado US (`yfinance_fetcher.py` + `sec_monitor.py`).

## 5. O que é preciso do utilizador antes de prosseguir

Duas coisas bloqueantes:

1. **Token brapi.dev** — obrigatório para aceder a fundamentals. Sem token só há quotes básicas. Criar ficheiro `.env` (local, não commitar) com:
   ```
   BRAPI_TOKEN=<o_teu_token>
   ```
2. **Dependências Python** — ainda não instaladas. Mínimo necessário para o piloto:
   ```
   requests
   pyyaml
   python-dotenv
   ```
   Recomendado: criar `.venv` primeiro.
   ```bash
   cd C:/Users/paidu/investment-intelligence
   python -m venv .venv
   .venv/Scripts/activate      # Windows (bash/Git Bash)
   pip install requests pyyaml python-dotenv
   pip freeze > requirements.txt
   ```

## 6. Comandos úteis

```bash
# (re)criar schema das DBs — idempotente
python scripts/init_db.py

# inspeccionar DB BR
sqlite3 data/br_investments.db ".schema"
sqlite3 data/br_investments.db "SELECT * FROM companies;"
```

## 7. Convenções a respeitar (resumo de CLAUDE.md)

- Datas ISO 8601 (`YYYY-MM-DD`), UTC para timestamps de eventos.
- **Moeda nunca convertida na DB** — BRL fica em `br_investments.db`, USD em `us_investments.db`. Conversão só na camada de relatório.
- Tickers BR **sem** sufixo `.SA` na DB; o fetcher acrescenta-o ao falar com APIs externas se for preciso.
- Fetchers são independentes e idempotentes. O motor de scoring **nunca** chama a rede.
- Logs estruturados (1 linha JSON por evento) em `logs/`.

## 8. Próxima acção concreta

Depois de colocar o token em `.env` e instalar dependências: **implementar `fetchers/brapi_fetcher.py` focado só em ITSA4**, correr, inspeccionar a DB, e reportar o que se encontrou antes de mexer no motor de scoring.
