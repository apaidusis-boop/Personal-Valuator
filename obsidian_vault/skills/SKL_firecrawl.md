---
type: skill
tier: S
skill_name: firecrawl
source: mendableai/firecrawl
status: backlog
sprint: W.2
tags: [skill, tier_s, scraping, web]
---

# 🔥 Firecrawl

**Repo**: https://github.com/mendableai/firecrawl
**Homepage**: https://firecrawl.dev
**Fit**: 🎯 **Médio-alto** — crawl + extract structured data. Complementa Playwright.

## O que faz
Crawler/scraper que retorna **markdown** ou **JSON structured** de qualquer site. Handles JS rendering, PDFs, sitemaps. Tem cloud API + self-host option.

## Onde integra
- **CVM fatos relevantes** — `monitors/cvm_monitor.py` hoje faz parsing HTML frágil; Firecrawl retorna markdown limpo
- **SEC filings** (`monitors/sec_monitor.py`) — EDGAR HTML é brutal; Firecrawl simplifica
- **Analyst reports** em websites (não-PDF) — XP site tem research notes em HTML; Firecrawl crawl → markdown → Ollama extract

## Firecrawl vs Playwright — quando usar cada um
| Caso | Ferramenta |
|---|---|
| Site público estático (HTML rendered server-side) | **Firecrawl** — mais simples |
| SPA React/Vue com data via XHR | **Playwright** |
| Login-gated (broker portal) | **Playwright** (controlo fino) |
| Crawl recursivo de secção inteira | **Firecrawl** (sitemap support) |
| Screenshot / form fill | **Playwright** |

## Decisão
Usar em W.2 como **complemento** a Playwright. Firecrawl cloud tem free tier; self-host se preocupação com tokens/privacy de certas consultas.

## Instalação (cloud)
```bash
# .env
FIRECRAWL_API_KEY=fc-xxx
```

MCP opcional: https://github.com/mendableai/firecrawl-mcp-server

## Self-host (mais alinhado com in-house first)
```bash
git clone https://github.com/mendableai/firecrawl
cd firecrawl && docker-compose up -d
# Endpoint local: http://localhost:3002
```

**Recomendação**: começar com cloud free tier; migrar para self-host se hit rate limits.

## Blockers
Signup ou Docker.
