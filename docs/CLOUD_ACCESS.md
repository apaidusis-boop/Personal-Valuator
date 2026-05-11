# Acesso remoto ao repo (claude.ai/code + GitHub)

Como aceder ao `investment-intelligence` de qualquer máquina para conversar com o Claude
sobre carteira/fundamentals sem precisar do ambiente local.

---

## 1. Estado actual

- **Repo**: `https://github.com/apaidusis-boop/Personal-Valuator` (privado).
- **DBs**: `data/br_investments.db` (15 MB) + `data/us_investments.db` (17 MB) — pequenas,
  não estão em `.gitignore` (podem ser commitadas).
- **Secrets**: `.env` com `BRAPI_TOKEN` NÃO vai para GitHub (já em `.gitignore`).
- **Owner**: apaidusis-boop.

## 2. Recomendação: claude.ai/code (web)

**Setup (uma vez, na máquina qualquer com browser)**:

1. Ir a https://claude.ai/code (requer subscription Claude Max/Pro).
2. Autorizar GitHub App (Settings → Connectors → GitHub).
3. Escolher repo `apaidusis-boop/Personal-Valuator`.
4. Claude Code abre sessão cloud com o repo montado.

**O que funciona**:
- Ler código, perguntar sobre holdings, deep-dive em tickers.
- Rodar scripts Python se o ambiente cloud do Claude tiver Python + deps.
- Se as DBs estiverem commitadas, queries SQLite funcionam directamente.

**O que NÃO funciona sem push**:
- Mudanças feitas localmente hoje não aparecem na cloud até `git push`.
- Cache fetchers (yf_us, sec_edgar) são regenerados, então OK.

---

## 3. Setup recomendado para começar (5 min)

**No local (este laptop)**:

```bash
cd investment-intelligence
# Confirmar .gitignore não inclui DBs (já verificado)
git add data/br_investments.db data/us_investments.db
git commit -m "Snapshot DBs para acesso remoto via claude.ai/code"
git push origin main
```

**No laptop / outra máquina**:
1. Login em claude.ai/code.
2. Connect repo.
3. Novo chat: "Mostra holdings US e DY actual de cada."

---

## 4. Alternativas

### Opção B — Claude Code Desktop App
- Mac/Windows/Android/iOS app nativa.
- Requer `git pull` manual ou auto-sync via GitHub CLI.
- Mais rápida que web, mesma interface.

### Opção C — GitHub Codespaces (pago)
- VM completa na cloud com Python 3.13 + deps.
- Corre `daily_update_us.py`, `research.py`, etc. no servidor.
- ~$0.18/hora de uso (~$2/mês se uso leve).
- Acesso via VS Code Web ou Claude Code no codespace.

### Opção D — Turso (SQLite cloud, futuro)
- Migrar `br_investments.db` + `us_investments.db` para Turso (dialecto SQLite compatível).
- DB viva na cloud, qualquer máquina lê/escreve.
- ~$0 tier grátis para estas DBs.
- Requer refactor minor em `sqlite3.connect(...)` nos scripts.

---

## 5. Fluxo recomendado para uso diário

**Workflow proposto**:

```
[local laptop] daily_update_us.py rodado diariamente (cron Win)
                     ↓
              git add data/*.db && git commit && git push
                     ↓
[claude.ai/code]  pull automático, Claude lê estado actualizado
                     ↓
[qualquer lugar]  chat sobre carteira, análise, decisões
```

Para automatizar:
- Adicionar `git push` ao fim de `scripts/daily_run.bat` (cron).
- OU rodar manualmente `git push` 1-2× por semana.

---

## 6. Limitações conhecidas

1. **Não mexer em ordens reais via Claude**. Claude vê dados, analisa, recomenda. Execução
   de compras/vendas SEMPRE manual no broker (JPM, XP).
2. **.env stays local**. BRAPI_TOKEN não vai para cloud. Fetchers BR não correm remoto sem
   setar env vars na sessão cloud.
3. **yfinance rate limit**. Se usar Claude cloud para fazer fetch intensivo, pode bater rate
   limit yfinance (sem auth).

---

**TL;DR**: push as DBs para GitHub, abre claude.ai/code, liga o repo, conversa daqui.
