---
type: skill
tier: S
skill_name: tavily-mcp
source: tavily-ai/tavily-mcp
status: backlog
sprint: W.2
tags: [skill, tier_s, mcp, search, news]
---

# 🔍 Tavily MCP

**Repo**: https://github.com/tavily-ai/tavily-mcp
**Homepage**: https://tavily.com
**Fit**: 🎯 **Médio-alto** — search qualificada para research/news. Paid tier (mas free quota decente).

## O que faz
MCP server que expõe Tavily Search API — search otimizada para LLMs. Retorna resultados filtrados, summarizados, com scoring de relevância. Melhor que WebFetch genérico para:
- "Últimas notícias sobre ITSA4"
- "Analyst views on JPM Q1 2026"
- "Has the Fed signaled rate cut?"

## Onde integra
- **`fetchers/news_fetch.py`** — hoje usa feeds RSS simples. Tavily dá search em tempo real
- **`scripts/research.py`** — secção "analyst views" hoje é manual; Tavily + agente pode automatizar
- **`agents/research_scout.py`** — agent que já existe; Tavily é natural fit

## Por que Tavily vs WebFetch?
| | WebFetch | Tavily |
|---|---|---|
| Query semântica | ❌ precisa URL | ✅ natural language |
| Ranking | — | LLM-optimizado |
| Noise | alto | filtrado |
| Custo | $0 | free 1000 searches/mo, depois $ |

## Alternativa in-house
Existe? Não temos search engine próprio. Ollama + Qwen não faz web search. **Tavily é único caminho** para search on-demand, excepto:
- Scraping manual de feeds específicos (RSS Bloomberg, Reuters, Valor, InfoMoney)
- Brave Search API (similar, tem MCP também)

## Decisão
Adoptar Tavily em W.2. **Wrap em cache agressivo** (`data/tavily_cache/<query_hash>.json`, TTL 24h para news, 7d para analyst views) para não queimar quota.

## Instalação
```yaml
# .claude/mcp.json
mcpServers:
  tavily:
    command: npx
    args: ["-y", "@tavily-ai/tavily-mcp"]
    env:
      TAVILY_API_KEY: ${TAVILY_API_KEY}  # no .env
```

## Blockers
Precisa signup + API key em https://tavily.com. Free tier suficiente para começar.
