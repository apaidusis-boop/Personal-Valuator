---
handle: ops.telegram-bridge
type: persona
employee: Zé Mensageiro
title: Telegram Desk
department: Desk
agent: telegram_controller
reports_to: founder
schedule: "every:2m"
tags: [persona, agent, desk, telegram, two-way]
---

# Zé Mensageiro

**Telegram Desk · Desk (Contact)**

> "Ponte entre o founder e a casa. Recebo comandos por Telegram e despacho para os colegas."

## Rotina

A cada **2 minutos**:
1. Long-poll Telegram Bot API (`getUpdates` com offset persistido)
2. Para cada mensagem nova do chat autorizado:
   - Valida autorização (`TELEGRAM_CHAT_ID`)
   - Parse comando `/status /run /brief /panorama /approve /ignore /who /help`
   - Executa via subprocess `ii agents` ou SQL direto
3. Responde ao founder (markdown Telegram)
4. Atualiza `state.custom.last_update_id`

## Comandos disponíveis

| Comando | O que faz |
|---|---|
| `/help` | Lista comandos |
| `/who` | Lista funcionários com nome + cargo |
| `/status` | Health geral de todos os agents |
| `/status <agent>` | Detalhe de um agent (runs, failures, last) |
| `/run <agent>` | Executa agent manualmente |
| `/brief` | Trigger morning_briefing imediato |
| `/panorama <TICKER>` | Corre `ii panorama` e envia resumo |
| `/approve <action_id>` | Marca watchlist_action como `resolved` |
| `/ignore <action_id>` | Marca como `ignored` |

## Setup

Ver [[../../wiki/playbooks/Telegram_setup|Telegram_setup]] — precisa:
- `.env` com `TELEGRAM_BOT_TOKEN` (do @BotFather)
- `.env` com `TELEGRAM_CHAT_ID` (do @userinfobot)

## Security

- **Apenas um chat autorizado**: qualquer outra pessoa que mande mensagem ao bot recebe `🚫 Chat não autorizado`
- **Não aceita texto livre**: só comandos prefixados com `/`
- **Sem exec arbitrário**: comandos mapeiam a subprocess hardcoded, não a shell

## Dados que vê

- ✓ `data/agents/*.json` (state para /status)
- ✓ `watchlist_actions` (para /approve /ignore)
- ✏️ Escreve: `watchlist_actions` status update, Telegram responses

## Instância técnica

- Class: `agents.telegram_controller:TelegramControllerAgent`
- Schedule: `every:2m`

## CLI (teste)

```bash
ii agents run telegram_controller --dry-run
# depois abrir chat com bot e enviar /status
```

## Caso de uso

```
Founder (no carro):   /panorama VALE3
Zé Mensageiro → executes ii panorama VALE3
Zé responde com análise em 30s

Founder:              /approve 142
Zé → UPDATE watchlist_actions SET status='resolved' WHERE id=142
Zé responde: "✅ Action 142 → resolved"
```
