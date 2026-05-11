---
type: backlog
created: 2026-05-09
last_updated: 2026-05-09
owner: founder + claude
---

# A Fazer

Backlog actualizado a partir da sessão 2026-05-08 → 2026-05-09 (Midnight Work).
Os itens estão ordenados por **alavancagem sobre a qualidade dos dados** —
não por urgência operacional.

## P0 — Investigação imediata (esta sessão)

- [x] **Root cause: `synthetic_ic` perdeu 7.5h de overnight** — RESOLVED 2026-05-09
  - RCA: `obsidian_vault/Postmortem_2026-05-09_synthetic_ic.md`
  - 3 bugs em camadas confirmados e fixados:
    1. Ollama 0.23.2 não fazia auto-discovery da RTX 5090 com driver 595.79 — fix: `CUDA_VISIBLE_DEVICES=0` ao nível user
    2. `gemma4:31b` produz output degenerado (`"ownable ownable..."`) — fix: Taleb persona migrada para qwen2.5:14b
    3. `--majority 3` triplicava o cost — fix: removido do orchestrator default; reservado para decision moments explícitos
  - Verificação: synthetic_ic JPM passou de **491s + 3/5 fails** para **76s + 0 fails** (6.5× speedup)
  - Smoke test obrigatório adicionado ao orchestrator antes de phase 5

## P1 — Engineering follow-ups (gaps que ficaram não fechados de ontem)

Estes são os 7 gaps que tu e eu identificámos quando auditei a minha própria
resposta de "PG/JNJ/KO + JPM deep dive". Todos são features novas que precisam
de design + testes — não são quick fixes.

- [ ] **CET1 / Tier 1 / leverage parser para US banks**
  - Hoje `fundamentals` não tem coluna CET1. CLAUDE.md tem critério ≥11% para US banks.
  - Source: SEC 10-Q exhibit 99.x ("Selected Capital Ratios") por bank.
  - Output esperado: nova coluna em `fundamentals` ou tabela `bank_capital_ratios`.

- [ ] **Brand / intangible premium estimator para staples**
  - Hoje a fórmula Buffett-ceiling pune KO (P/B 10) e PG (P/B 6) como SELL severos.
  - Source: balance sheet `Goodwill + Intangibles` ÷ market cap = `intangible_premium_pct`.
  - Output: nova métrica que ajusta o fair_value para staples high-quality.

- [ ] **Litigation overhang flags** (ex. JNJ talc, BMY entresto)
  - Hoje não há sinal estruturado.
  - Source: SEC 10-K Item 3 "Legal Proceedings" parsing + 8-K filings filter.
  - Output: tabela `litigation_overhang(ticker, jurisdiction, est_exposure_usd, status, source_url)`.

- [ ] **Fair-value "add zones" intermédias**
  - Hoje só temos BUY-below / HOLD / SELL-above estritas (Buffett ceiling).
  - Eu inventei "PG abaixo de $120, JNJ abaixo de $160, KO abaixo de $60" — extrapolation.
  - Output: novo engine `scoring/fair_zone.py` que combina:
    - Buffett ceiling estrito
    - Sector P/E reversal point (z-score do peer set)
    - Dividend yield band (±1σ histórico)
    - DCF se disponível

- [ ] **REIT-aware `dividend_safety` calibration audit**
  - Memory diz que foi shipped 2026-04-27, mas O continua WATCH 60 (payout 84%, ROE 2.7%, ND/EBITDA 5.68x).
  - Esses 3 são *normais* para REIT (FFO ≠ EPS, mandatory 90% payout, capital-intensive).
  - Verificação: confirmar se o engine actual está realmente aplicando lógica REIT-specific ou se a lógica falha.

- [ ] **CVM monitor `download_ipe` fix** (BR side)
  - Backfill 2c falhou (`monitors/cvm_monitor.py:88`). SEC US correu clean — só BR está partido.
  - Stack trace truncated no log; precisa de leitura completa.

- [ ] **Dividend CAGR — current-year partial bias** (já corrigido, mas merece teste)
  - Bug original: o CAGR usava `dividends[2026]` partial-year vs `dividends[2021]` full-year → CAGRs negativos absurdos.
  - Fix aplicado: anchor no último ano completo (`2025` em vez de `2026`).
  - To-do: adicionar teste em `tests/` para evitar regressão.

## P2 — Storage & infra (tomorrow conversation)

- [ ] **Decisão SQLite vs DuckDB vs Parquet** — análise de trade-offs com números
  - Volume actual: 7M rows estimado (precisa medir)
  - Bottleneck actual: completude de dados (não query speed)
  - Critério para migrar: > 50M rows OR queries multi-table > 5s

- [ ] **Captura de credenciais** (WSJ, FT, Moody's pro)
  - Storage: `data/credentials.enc` com Fernet (lib `cryptography`), key em `.env` (já gitignored)
  - Per-domain login sequence em `config/auth_flows.yaml`
  - Browser via `playwright` (já listado no skill arsenal)

## P3 — Multi-agent system (a "back and forth" que não aconteceu)

- [ ] **Senior-validator → junior-researcher loop**
  - Memory note (skill: `synthetic_ic`) diz que tens 5 personas com models diferentes
  - Agora precisas de um meta-loop: critic agent gera challenge questions; junior agent responde; arbiter decide
  - Já existe `agents/critic.py`? — precisa verificar

- [ ] **Per-ticker "dossier delta engine"**
  - Hoje o synthetic_ic regenera tudo cada vez. Devíamos só re-run quando há **mudança material** (filing, price spike, earnings, analyst rating shift)
  - Output: `agents/dossier_freshness.py` que decide qual regenerar

## P4 — Data sources que ainda não tocámos

- [ ] **Moody's / S&P / Fitch credit ratings** — sem API gratuito, scraping risky; precisa de credential storage primeiro
- [ ] **WSJ / Financial Times** — paywall, depende de captura de credenciais
- [ ] **Bloomberg Open Symbology** — algumas APIs free para mapping, vale explorar

## P5 — UI / presentation (ficaram a ressonar mas baixa prioridade)

- [ ] **Mission Control "data confidence" widget** — mostra cross_validated count em tempo real na home
- [ ] **`/dossier/<TK>` route polished** — merge IC_DEBATE + variant + fair_value + recent events numa página

---

## Como usar este ficheiro

Convenção: marcar `[x]` quando done; mover P0→P1→P2 conforme prioridade muda.
Ler `obsidian_vault/Postmortem_2026-05-09_synthetic_ic.md` antes de tentar
re-correr o orchestrator overnight (ou vai perder 7.5h outra vez).
