---
type: skill
tier: S
skill_name: playwright-mcp
source: executeautomation/playwright-mcp-server
status: backlog
sprint: W.2
tags: [skill, tier_s, mcp, scraping, browser_automation]
---

# 🎭 Playwright MCP

**Repo**: https://github.com/executeautomation/mcp-playwright (também existe microsoft/playwright-mcp)
**Fit**: 🎯 **Alto** — scraping fiável para sites dinâmicos (React/JS).

## O que faz
MCP server que expõe Playwright (Chromium headless) ao Claude. Pode: navegar páginas, preencher forms, screenshot, extrair HTML pós-render, lidar com JS-heavy sites.

## Onde integra
- **Substituir** `fetchers/fii_statusinvest_scraper.py` (hoje quebra quando Status Invest muda HTML)
- **Novo** `fetchers/investidor10_scraper.py` — site tem DY histórico 10y que brapi não tem
- **Novo** `fetchers/fundamentus_scraper.py` — data gratuita complementar
- **Broker portals** (XP, BTG, JPM) — login-gated, precisa browser real
- **Screenshots** de charts para vault: `scripts/obsidian_bridge.py` poderia incluir PNG de gráficos

## Por que Playwright > simples HTTP?
- Status Invest carrega tabelas via JS depois do load → `requests` só apanha skeleton
- Investidor10 tem paywall soft (detect bot) → Playwright com user-agent real passa
- Broker portals têm OAuth/2FA → só browser real funciona

## Sprint W.2 — plano concreto
```yaml
# .claude/mcp.json (adicionar)
mcpServers:
  playwright:
    command: npx
    args: ["-y", "@executeautomation/playwright-mcp-server"]
```

Depois, CLI tests:
1. Extrair DY 10y de 1 ticker BR via Investidor10
2. Carregar em `fundamentals` (novo campo `dy_history_json`)
3. Validar vs dados brapi actuais (sanity check)

## Riscos
- **Detecção anti-bot**: rotate UA, rate limit, não hammer
- **Fragilidade**: Playwright selectors quebram quando site muda. **Wrapping em função com retry + log** obrigatório
- **Complexity creep**: usar APENAS para dados que não temos via API. Nunca replace brapi/yfinance.

## Blockers
Nenhum. Node.js precisa estar instalado (provável que já esteja).
