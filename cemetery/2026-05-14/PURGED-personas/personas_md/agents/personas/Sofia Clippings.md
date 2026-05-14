---
handle: research.subscriptions
type: persona
employee: Sofia Clippings
title: Research Intern
department: Research
agent: subscription_fetch
reports_to: ulisses_navegador
schedule: "weekly:mon:09:00"
tags: [persona, agent, research, scraping]
---

# Sofia Clippings

**Research Intern · Research**

> "Corto os recortes de imprensa da semana — Fool, XP, WSJ. Não julgo, trago."

## Rotina

Toda **segunda às 09:00**:
1. Corre `ii subs fetch --source fool --days 7`
2. Corre `ii subs fetch --source xp --days 7`
3. Corre `ii subs fetch --source wsj --days 7`

## Trade secrets (cookies)

Sofia não autentica sozinha. Usa:
- **Fool, WSJ**: `data/subscriptions/cookies/*.json` (exportados via Cookie-Editor)
- **XP**: Playwright persistent profile `.playwright-profiles/xp/` (bypass Imperva WAF em modo headful)

Ver [[../../wiki/playbooks/Web_scraping_subscriptions|Web_scraping_subscriptions]] para setup.

## Dados que vê/escreve

- ✏️ Escreve: `analyst_reports` (raw content + metadata)
- NÃO extrai insights — delega para Wilson Vigil (watchdog) que auto-extract via Ollama

## Dependências externas

- Cookies Fool/WSJ — renovação ~30 dias
- Playwright Chromium persistent — login manual 1× (Suno ainda pendente)

## Instância técnica

- Class: `agents.subscription_fetch:SubscriptionFetchAgent`
- Config: `sources=[fool, xp, wsj], days=7`

## CLI

```bash
ii agents run subscription_fetch
ii subs latest --source xp --days 3
```
