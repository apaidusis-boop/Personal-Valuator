---
type: playbook
name: Telegram Setup — two-way remote control
tags: [playbook, telegram, remote, setup, agents]
related: ["[[Agents_layer]]", "[[Token_discipline]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 📱 Telegram Setup — delegação remota

> Configurar Zé Mensageiro (`telegram_controller`) para enviar briefings **E** receber comandos do founder via Telegram. Permite operar a empresa sintética do carro/férias/telemóvel.

## Overview

```
              ┌─────────────────┐
              │     Founder     │
              │  (Telegram app) │
              └────────┬────────┘
                       │
                       │ /status, /run, /approve ...
                       ▼
              ┌─────────────────┐
              │  Telegram Bot   │  (hosted by Telegram)
              │   (tu crias)    │
              └────────┬────────┘
                       │
                       │ long-poll every 2m
                       ▼
              ┌─────────────────┐
              │  Zé Mensageiro  │
              │ (agent Python)  │
              └────────┬────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │  agents/ + scripts/ │
            └─────────────────────┘
```

## Setup em 5 passos

### 1. Criar o bot (2 minutos)

1. Abre Telegram e procura **@BotFather**
2. Manda `/newbot`
3. Escolhe um nome: `IIInvestmentAgent` (ou o que preferires — visível no chat)
4. Escolhe username único terminado em `bot`: `ii_investment_bot` (se livre)
5. **@BotFather devolve um TOKEN** tipo `7831234567:AAEabcdefg_XYZ...`

**Guarda este token.** É a senha do bot.

### 2. Obter o teu chat_id

1. Abre conversa com **@userinfobot** no Telegram
2. Envia `/start` — responde com o teu ID (ex: `123456789`)
3. Alternativa via API:
   - Envia qualquer mensagem ao teu bot novo
   - Abre no browser: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Procura `"chat":{"id":123456789,...}` → esse é o teu chat_id

### 3. Configurar `.env`

No root do projecto, edita `.env` (cria se não existe — já está no `.gitignore`):

```bash
TELEGRAM_BOT_TOKEN=7831234567:AAEabcdefg_XYZ...
TELEGRAM_CHAT_ID=123456789
```

### 4. Testar send-only (Aurora Matina)

```bash
ii telegram "🌅 Hello from IInv — setup ok"
```

Devias ver a mensagem chegar ao chat. Se sim, Aurora já pode enviar briefings.

### 5. Testar two-way (Zé Mensageiro)

Manualmente corre o agent:

```bash
ii agents run telegram_controller
```

No Telegram, manda ao bot:
```
/help
```

Zé deve responder com lista de comandos em ~10 segundos (delay = long-poll timeout).

Depois experimenta:
```
/who
/status
/brief
/panorama VALE3
```

## 📋 Comandos disponíveis

| Comando | Descrição | Exemplo |
|---|---|---|
| `/help` | Lista comandos | — |
| `/who` | Lista funcionários com nome e cargo | — |
| `/status` | Health geral dos agents | — |
| `/status <agent>` | Detalhe específico | `/status valentina` — **nota**: usa agent name, não employee name |
| `/run <agent>` | Executar manualmente | `/run morning_briefing` |
| `/brief` | Alias para `/run morning_briefing` | — |
| `/panorama <TICKER>` | Análise completa | `/panorama ITUB4` |
| `/approve <id>` | Marca watchlist_action como `resolved` | `/approve 142` |
| `/ignore <id>` | Marca como `ignored` | `/ignore 143` |

## 🕒 Quando a empresa fala contigo (push)

### Aurora Matina — diário 07:00
Briefing matinal com TOP 3 takeaways + P&L + triggers + analyst insights + earnings próximos.

### Wilson Vigil — eventos real-time
- Novos triggers < 15min → push imediato
- Earnings hoje → 1× por dia (dedup)

### Valentina Prudente — diário 21:00 (se há drift)
Flags TRIM/REVIEW/WATCH por holding.

### Regina Ordem — diário 23:00 (se cohort unhealthy)
Alert se ≥50% dos agents estão non-ok.

### Zé Mensageiro — responde a teus comandos
Latência: até 2 min (schedule every:2m).

## 🔒 Segurança

- **Chat ID gate**: só o `TELEGRAM_CHAT_ID` configurado pode enviar comandos. Outros recebem `🚫 Chat não autorizado`.
- **Token em `.env`**: gitignored, nunca no repo
- **Sem exec arbitrário**: `/run foo && rm -rf /` é parsed como comando desconhecido, não shell command
- **Rate limit implícito**: every:2m = no máximo 20 comandos processados por ciclo

## 🚨 Troubleshooting

### Bot não recebe mensagens
- Inicia conversa no Telegram: envia `/start` ao bot
- Verifica token: `curl https://api.telegram.org/bot<TOKEN>/getMe` — deve devolver `"ok": true`

### `/status` não responde
- Verifica se `telegram_controller` está enabled: `ii agents show telegram_controller`
- Corre manual: `ii agents run telegram_controller`
- Verifica logs: `ii agents logs telegram_controller --tail 50`

### `/approve <id>` responde "não encontrada"
- `watchlist_actions` IDs são por DB (BR e US separadas)
- Ver actions abertas: `ii actions list`

### Message truncada
- Telegram limita 4096 chars. `/panorama` resume até 3500.
- Para output completo, corre em terminal: `ii panorama VALE3 --write` e abre no vault.

## 🔄 Auto-arranque em Windows

O agent runner já deve estar em Task Scheduler (cron). Se não:

```powershell
schtasks /create /tn "ii-agent-runner" /sc minute /mo 1 `
  /tr "C:\Users\paidu\investment-intelligence\.venv\Scripts\python.exe C:\Users\paidu\investment-intelligence\scripts\agent_runner.py"
```

Isto corre `agent_runner.py` a cada minuto. O runner verifica schedules e executa Zé (every:2m) automaticamente.

## 🧪 Dev / debug

```bash
# Long-poll manual
curl "https://api.telegram.org/bot<TOKEN>/getUpdates?timeout=30"

# Enviar mensagem sem o agent
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d chat_id=<CHAT_ID> -d text="Teste manual"

# Ver state do Zé
cat data/agents/telegram_controller.json
```

## Extensões futuras

- **Webhook em vez de polling** (instant vs 2min delay) — requer servidor acessível pela internet (ngrok ou VPS)
- **Inline commands** (botões) para `/approve` e `/ignore` — mais UX-friendly
- **Markdown formatado rico** (já usa `parse_mode=Markdown`)
- **Rate limiting per-founder** se partilhares chat com outra pessoa

---

*Para arquitectura agents, ver [[Agents_layer]]. Para Zé Mensageiro especificamente, ver [[ops.telegram-bridge|persona card]].*
