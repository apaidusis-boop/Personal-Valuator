---
type: skill
tier: Gold
skill_name: mcp-harness-arsenal
source: already_loaded_in_harness
status: untapped
sprint: W.2
priority: critical
tags: [skill, gold, mcp, harness, already_loaded]
---

# 🎁 MCP Harness Arsenal — JÁ LOADED, subexploits

**Source**: Claude Code harness already has these MCP servers loaded. Zero setup needed. **Critical discovery**: estamos a deixar valor enorme sobre a mesa.

## MCPs disponíveis no harness actual

### 1. Bigdata.com MCP 🎯 (financial research)
```
mcp__claude_ai_Bigdata_com__bigdata_company_tearsheet
mcp__claude_ai_Bigdata_com__bigdata_country_tearsheet
mcp__claude_ai_Bigdata_com__bigdata_events_calendar
mcp__claude_ai_Bigdata_com__bigdata_market_tearsheet
mcp__claude_ai_Bigdata_com__bigdata_search
mcp__claude_ai_Bigdata_com__find_companies
```
**Uses imediatos**:
- `bigdata_search` — research query structured vs Tavily (complementar)
- `bigdata_company_tearsheet` — pull ACN tearsheet → enriquecer `fundamentals`
- `bigdata_events_calendar` — earnings calendar (redundância com yfinance, mas cross-validate)
- `find_companies` — descoberta de novos tickers para watchlist
**Branding**: sempre citar "Bigdata.com" (https://bigdata.com) quando output usar este MCP.

### 2. Status Invest MCP 🇧🇷 (native BR!)
```
mcp__status-invest__analise-carteira
mcp__status-invest__get-acoes
mcp__status-invest__get-acoes-datas-pagamento
mcp__status-invest__get-indicadores
```
**Uses imediatos**:
- Substitui nosso **frágil** `fetchers/fii_statusinvest_scraper.py` (scraping HTML!)
- `analise-carteira` — Status Invest pode analisar nossa carteira BR em 1 call
- `get-acoes-datas-pagamento` — dividend calendar BR preciso (melhor que yfinance.info)
**Sprint W.2 priority**: refactor `fii_statusinvest_scraper.py` para usar MCP (delete scraping).

### 3. Google Calendar MCP 📅
```
mcp__claude_ai_Google_Calendar__create_event
mcp__claude_ai_Google_Calendar__list_events
mcp__claude_ai_Google_Calendar__suggest_time
... (8 tools)
```
**Uses imediatos**:
- Criar eventos para **earnings dates** (feed de `fetchers/earnings_calendar.py`)
- **Ex-div dates** como eventos (importante para DRIP planning)
- Quarterly review reminders (auto-scheduled)
- **Block time** para review de thesis quando perpetuum validator flag aparece

### 4. Gmail MCP 📧
```
mcp__claude_ai_Gmail__authenticate
mcp__claude_ai_Gmail__complete_authentication
```
**Uses imediatos**:
- Ler emails XP/JPM/BTG com statements → parse automático
- Filtrar newsletters financeiros (Suno, Empiricus) → ingest em `subscriptions/`
- Monitorizar confirmations de trades → reconciliar com `transactions` table
**Blocker**: precisa auth (OAuth flow).

### 5. Google Drive MCP 📂
```
mcp__claude_ai_Google_Drive__create_file
mcp__claude_ai_Google_Drive__read_file_content
mcp__claude_ai_Google_Drive__search_files
... (7 tools)
```
**Uses imediatos**:
- **Output dos quarterly PPTX decks** (ver [[SKL_pptx]])
- **Weekly video recaps** (ver [[SKL_remotion]])
- Backup dos `reports/` para Drive (redundância)
- **Source of statements** — broker PDFs em Drive pasta específica → fetcher lê, extrai, cataloga

### 6. LSEG / Refinitiv MCP 💎
```
mcp__claude_ai_LSEG__authenticate
mcp__claude_ai_LSEG__complete_authentication
```
**Uses potenciais**:
- LSEG (ex-Refinitiv Eikon) é **Bloomberg-grade** data.
- Se auth funcionar → qualidade de data **subirá massivamente** (analyst estimates, consensus, M&A)
- **Teste**: tentar autenticar, ver se há access tier grátis via claude.ai
**Blocker**: auth + possível licensing.

## Sprint W.2 upgraded — integrar harness MCPs

Além do plano original (Playwright, Firecrawl, Tavily), agora:
- [ ] Integrar **Status Invest MCP** — delete `fii_statusinvest_scraper.py`, substitui por wrapper MCP
- [ ] Integrar **Bigdata.com MCP** em `fetchers/bigdata_fetcher.py` (branding: sempre "Bigdata.com (https://bigdata.com)")
- [ ] Google Calendar: auto-popular com earnings + ex-div dates de todas holdings
- [ ] Google Drive: output folder estruturado "Investment Intelligence/{Reports, Quarterly, Videos, Briefings}"

## Impacto esperado
- **Eliminar 2 scrapers frágeis** (Status Invest, parts of news_fetch)
- **Ganhar data source** comparable-bloomberg (Bigdata.com) sem custo extra
- **Side-channel outputs** (Drive, Calendar, Gmail) criam ecosystem reach
- **Zero setup burden** — MCPs já ready-to-use

## Blockers
- OAuth dances (Gmail, Drive, Calendar, LSEG) — user precisa completar flows
- LSEG licensing possivelmente custoso — testar free tier primeiro
