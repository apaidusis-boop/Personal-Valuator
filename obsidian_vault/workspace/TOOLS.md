---
title: TOOLS
purpose: Notas locais de ferramentas e ambiente. NÃO é o catalog de comandos (esse vive em CLAUDE.md).
edit: humano-editável; só coisas environment-specific.
---

# TOOLS — Notas locais

Skills definem _como_ as tools funcionam. Este ficheiro é para _o nosso_ setup específico.

## Ambiente

- **Working dir**: `C:\Users\paidu\investment-intelligence`
- **Shell**: Git Bash (`/usr/bin/bash`) preferido para POSIX paths; PowerShell disponível via PS tool.
- **Python venv**: `.venv/` (ativado automaticamente pelo `ii.bat`).

## Ollama (LLM local)

- **Base URL**: `http://localhost:11434`
- **Models pulled**: `qwen2.5:32b-instruct-q4_K_M` (Antonio Carlos), `qwen2.5:14b-instruct-q4_K_M` (perpetuums), `mistral:7b` (light tasks), `nomic-embed-text` (embeddings).
- **Llama 3.3 70B**: optional, 40GB. `ollama pull llama3.3:70b` se RTX 5090 livre.

## DBs

- **BR**: `data/br_investments.db` (BRL, B3, tickers sem .SA)
- **US**: `data/us_investments.db` (USD, NYSE/NASDAQ)
- **Library/RAG**: `library/chunks_index.db` (Bibliotheca chunks + embeddings)
- **Chat memory**: `data/chief_memory.db` (Antonio Carlos per-chat history)

## Telegram (Jarbas)

- **Bot**: `@TheJarbas123_bot`
- **Token**: `.env::TELEGRAM_BOT_TOKEN`
- **Chat ID**: `.env::TELEGRAM_CHAT_ID`
- **Push**: `notifiers.telegram.send()` ou `agents._telegram.push()`
- **Long-poll loop**: `python scripts/telegram_loop.py` (substitui cron 2m)

## Tavily (web research)

- **API key**: `.env::TAVILY_API_KEY` (Dodo Key, dev tier)
- **Quota**: 1000/mês (vem com cache 7d + rate-limit 100/dia 50/hora)
- **Wires**: variant_perception, earnings_prep, synthetic_ic, autoresearch perpetuum

## Mission Control (Next.js)

- **URL**: `http://localhost:3000`
- **Mode**: webpack (NÃO turbopack — better-sqlite3 incompatível)
- **Start**: `ii missioncontrol` ou `cd mission-control && npm run dev`
- **Remote**: `npm run dev:remote` (0.0.0.0)

## Tailscale (recomendado, pendente)

- **Install**: `winget install Tailscale.Tailscale`
- **Status**: `tailscale status`
- Não-bloqueante para localhost-only workflows.

## Whisper (YouTube ingest)

- **Model**: `large-v3-turbo` (CPU int8 fallback se cuBLAS dll missing)
- **Cache**: HuggingFace `mobiuslabsgmbh/faster-whisper-large-v3-turbo`

## Cron schedule

- **Daily run**: 23:30 local via Windows Scheduled Task — PC precisa estar acordado.
- **Wired**: daily_run.bat → fetchers + scoring + perpetuum_master + captain's log push.
