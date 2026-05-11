# Midnight Work 2026-05-09 — Plan (Data Fortification Night)

## Mission

**Não produzir recomendações novas. Provar a firmeza dos dados.**

O teste de manhã: o user reabre as mesmas perguntas de ontem (PG/JNJ/KO bandas, JPM deep dive, "onde investir $1.5k US e ~R$100k BR"). As respostas têm de citar linhas de DB ou estar marcadas explicitamente como `extrapolation:true`. Hoje 7 números importantes foram extrapolados pelo Claude — esses são os 7 gaps que esta noite ataca.

## Anti-hallucination contract

1. Toda inserção numérica em `fundamentals` / `fair_value` / `dividends_annual` / `events` deve ter um source identificável (provenance row OU confidence_label OU inputs_json).
2. Nada de produção de "fair add zones intermédias" inventadas — só bandas computadas pelos engines.
3. Multi-agent: o output de qualquer LLM (synthetic_ic, variant_perception, critic) é registado com `agent.role` + `model` + `temperature` em `agent_runs`.
4. Audit no fim: `data/provenance_scorecard_2026-05-09.json` quantifica % de campos com source vs sem source.

## Constraints

- **In-house first**: Ollama local, scripts existentes, free APIs (SEC, CVM, FRED, BCB, yfinance). Zero tokens Claude.
- **Carteiras isoladas**: BR e US correm em silos separados. Dois relatórios paralelos no fim.
- **Sem destruição**: só leituras + inserts/updates idempotentes. Sem deletes. Sem schtasks novos.
- **Logins de subscritores**: ficam para amanhã (user pediu explicitamente).
- **Tavily budget**: máx 100 calls esta noite, só para gaps onde SEC/CVM/FRED/yfinance não chegam.

## Phases

| # | Nome | O que faz | Engine/Script | Timeout |
|---|---|---|---|---|
| 1 | inventory | Conta nulls per ticker × campo, listas de stale fundamentals/dividends | SQL inline | 60s |
| 2a | dividends | yfinance 25y div history para holdings + watchlist; computa CAGRs | `fetchers/yf_deep_fundamentals.py --holdings` | 20m |
| 2b | macro | FRED 30y + BCB SGS 20y | `fetchers/fred_fetcher.py` + `scripts/export_macro_csv.py` | 15m |
| 2c | sec_cvm | SEC EDGAR 10-K/10-Q/8-K + CVM DFP/ITR + PDF extractor | `monitors.sec_monitor` + `monitors.cvm_monitor` + `cvm_pdf_extractor.py` | 90m |
| 3 | engines | Re-run scoring + fair_value + dividend_safety + regime para todo o universo | `daily_update.py` + `daily_update_us.py` + `dividend_safety --all` | 80m |
| 4 | perpetuums | Roda os 10 perpetuums T1 (observadores) | `agents/perpetuum_master.py` | 60m |
| 5 | multi_agent | synthetic_ic + variant_perception em todos os holdings | `agents.synthetic_ic --all` + `agents.variant_perception --all-holdings` | 180m |
| 6 | provenance | Audit per-field source coverage; produz scorecard JSON | SQL inline | 5m |
| 7 | master_report | Consolida tudo em markdown navegável | inline | 5m |

**Total estimado**: 5–8h. Cabe na noite.

## Outputs (ler de manhã, por ordem)

1. **`obsidian_vault/Midnight_Work_2026-05-09.md`** — live status (cresce em tempo real)
2. **`obsidian_vault/Bibliotheca/Midnight_Work_2026-05-09.md`** — relatório master executivo
3. **`logs/midnight_2026-05-09.log`** — log linear cronológico
4. **`data/midnight_inventory_2026-05-09.json`** — gaps de cobertura no início da noite
5. **`data/provenance_scorecard_2026-05-09.json`** — qualidade de provenance no fim
6. **`obsidian_vault/dossiers/<TK>.md`** — dossiers actualizados com synthetic_ic + variant

## Kill switch

Se quiseres parar a meio: criar ficheiro `STOP_MIDNIGHT` na raiz do repo. O orchestrator detecta no boundary entre fases e faz exit limpo.

## NÃO fica em scope esta noite

- Construção de novos engines (CET1 parser, intangibles, litigation flags, fair_zone).
  Estes são features novas — exigem design + testes que não cabem numa noite. Vão para
  a "design conversation de manhã" como prioridades de follow-up.
- Migração de SQLite para DuckDB/Parquet — análise tradeoff vai amanhã, sem migração agora.
- Captura/storage de credenciais (WSJ, FT, Moody's pro) — explicitly tomorrow.
- Recomendação de "onde investir $1500" / "onde colocar R$100k LFTB11" — user disse para focar em data quality, não em decision.

## Como auditar de manhã

Sequência sugerida:
1. Ler `Bibliotheca/Midnight_Work_2026-05-09.md` (5 min)
2. Reabrir conversa de ontem; pedir as mesmas tabelas (PG/JNJ/KO bands, JPM deep dive)
3. Verificar que cada número agora tem citação ou flag `extrapolation:true`
4. Comparar `provenance_scorecard.json` antes/depois — % cross_validated subiu?
5. Decidir o que vale evoluir em features novas (gap-fillers de Phase 5 que ficou de fora)
