---
type: playbook
name: YouTube ingestion pipeline
tags: [playbook, youtube, ingestion, ollama, whisper, video_insights]
related: ["[[Token_discipline]]", "[[Agents_layer]]", "[[Web_scraping_subscriptions]]", "[[Analysis_workflow]]"]
---

# 📺 YouTube Pipeline — local ingest, zero tokens

> Pipeline que transforma vídeos de YouTube em factos estruturados (`video_insights`, `video_themes`) na DB usando **só compute local**: faster-whisper na 5090 + Ollama Qwen2.5. Cumpre [[Token_discipline]] (REGRA #1).

## Princípio

**Áudio descartável, factos persistentes.** Transcript fica em DB para iteração barata; áudio é apagado; output são factos validados com `evidence_quote` verbatim (anti-alucinação).

## Pipeline (6 fases)

```
URL ──► yt-dlp ──► faster-whisper ──► router ──► Ollama ──► validator ──► SQLite
        (audio)    (transcript)       (aliases)  (Qwen)     (substring)   (BR + US)
                                                                          ↓
                                                              audio apagado
```

| # | Fase | Módulo | Modelo / Tool |
|---|---|---|---|
| 1 | Download áudio | `youtube/downloader.py` | `yt-dlp` |
| 2 | Transcribe | `youtube/transcriber.py` | `faster-whisper` `large-v3-turbo`, CUDA fp16 → CPU int8 fallback |
| 3 | Router (filtra) | `youtube/router.py` | regex sobre `config/aliases.yaml` |
| 4 | Extract (LLM) | `youtube/extractor.py` | `ollama` Qwen2.5-32B-q4 → 14B fallback, JSON mode |
| 5 | Validate | `youtube/validator.py` | substring + dedup + confidence ≥0.5 |
| 6 | Persist | `youtube/persistence.py` | `videos` / `video_insights` / `video_themes` em **ambas** as DBs |

### 1. Download
`yt-dlp` puxa só áudio + metadata (title, channel, channel_id, published_at, duration_sec). Áudio em temp.

### 2. Transcribe
Whisper `large-v3-turbo` na CUDA fp16 (RTX 5090). VAD filter activo (`min_silence_duration_ms=500`). Output: lista de `TranscriptChunk(text, ts_start, ts_end)` + `full_text` + `lang`.

**Cache-first**: se `video_id` já tem `transcript_text` em `videos`, salta esta fase inteira. Re-extract custa só Ollama (~84s/vídeo vs ~2.5min full).

### 3. Router
Carrega `config/aliases.yaml` (estrutura: `tickers: <T>: {names, products, people}`; `themes: <name>: {keywords}`). Faz regex `\b(term|term|...)\b` case-insensitive sobre cada chunk. Para cada hit, expande **±90s** à volta para dar contexto. Junta janelas overlapping.

**Short-circuit**: se 0 tickers e <2 themes → marca vídeo `status='skipped_no_relevance'`, **não chama o LLM** (poupa Ollama).

### 4. Extract
Uma chamada `ollama.chat` por **ticker** (com as suas janelas concatenadas) + uma por **theme**. JSON mode, `temperature=0.1`, `num_ctx=8192`. Pydantic valida o schema.

System prompt impõe 3 regras críticas (anti-bug):
1. **Sujeito principal**: cada insight tem de ter o ticker alvo como sujeito (teste de substituição: "facto sobrevive sem o ticker?").
2. **Brokers proibidos**: GS/JPM/XP/BBI/Itaú BBA/BB Investimentos **não** são sujeito quando recomendam outras empresas. Fix do bug histórico Klabin → BBAS3.
3. **`evidence_quote` literal**: substring verbatim do transcript, ≤400 chars, sem parafrasear.

`kind` ∈ `{guidance, capex, dividend, balance_sheet, thesis_bull, thesis_bear, catalyst, risk, operational, management, valuation}`.

Fallback automático para Qwen 14B se 32B devolver JSON malformado.

### 5. Validate (`youtube/validator.py`)
- **Rule (A) Evidence-only**: `evidence_quote` tem de ser substring literal do `full_text`. Reject se não for.
- **Rule (B) Cross-contamination** (v2 fix): se `claim` menciona OUTRA empresa do universe **e** o ticker alvo está ausente do claim → reject.
- **Rule (C) Confidence**: <0.5 → reject.
- **Dedup**: chave `(video_id, ticker, kind, normalized_claim)`.

### 6. Persist
Escreve em **ambas** as DBs (BR + US, mirror). Tabelas:

| Tabela | PK | Colunas-chave |
|---|---|---|
| `videos` | `video_id` | url, title, channel, channel_id, published_at, duration_sec, lang, status, **transcript_text**, **transcript_chunks_json** |
| `video_insights` | autoincr | video_id, ticker, kind, claim, evidence_quote, ts_seconds, confidence |
| `video_themes` | autoincr | video_id, theme, stance, summary, evidence_quote, ts_seconds, confidence |

`status` ∈ `{pending, completed, skipped_no_relevance, error}`.

Áudio é apagado (`youtube/cleanup.py::remove_audio`).

## Comandos

| Caso | Comando |
|---|---|
| 1 vídeo | `python scripts/yt_ingest.py <url>` |
| 1 vídeo (dry-run) | `python scripts/yt_ingest.py <url> --dry-run` |
| Forçar re-transcribe | `python scripts/yt_ingest.py <url> --force-retranscribe` |
| Skip se já tem facts | `python scripts/yt_ingest.py <url> --skip-if-has-facts` |
| Batch canal | `python scripts/yt_ingest_batch.py --channel-last <id> --count N` |
| Batch lista | `python scripts/yt_ingest_batch.py --file <urls.txt>` |
| Re-extract sem rede/GPU | `python scripts/yt_reextract.py --all` (ou `--video <id>`) |
| Rundown SQL-only | `python scripts/yt_digest.py --channel "<x>" --days 30` |
| Rundown ticker | `python scripts/yt_digest.py --ticker PETR4 --days 60` |
| Rundown holdings | `python scripts/yt_digest.py --holdings-only --days 30` |

## Economia de tokens

| Acção | Custo |
|---|---|
| Iterar prompt/validator (14 vids cached) | ~14min Ollama (zero rede/GPU) |
| Dashboard via `yt_digest` | ~1.5k tokens (vs ~15k raw insights) |
| Pipeline full por vídeo | ~2.5min, **0 tokens Claude** |

## Configs críticas

- **`config/aliases.yaml`** — sem isto, router não funciona em PT. Tickers populares têm `["ITSA 4", "ITSA quatro", …]` para apanhar transcrições Whisper irregulares.
- **`config/youtube_sources.yaml`** — whitelist de canais/playlists curados (não scraping aberto).

## Limitações conhecidas

- **GPU contention**: batches in-process morriam silenciosamente (Whisper segura VRAM, Ollama 32B precisa ~20GB e falha). Fix: `yt_ingest_batch.py` spawna `subprocess.call` fresh por vídeo — Windows liberta a GPU quando o processo sai.
- **Não paralelizar** `yt_ingest_batch` com `yt_reextract` (mesmo Ollama → contention residual).
- **Brand hallucination resid**: casos tipo "Caixa Seguridade, parte do BBAS3" ainda passam mesmo com regra 3 (LLM mistura entities não-broker). Fix futuro: penalizar insights cujo claim tem >50% nomes de outras empresas.
- **Subject-confusion**: ITSA4/ITUB4, CXSE3/BBSE3/BBAS3 — quando transcript discute várias holdings/subsidiárias, atribuição fica ambígua.
- **Price-target regex** (em `yt_digest.py`) é simples — não apanha "alvo em R$X" e variações.

## Estado actual (2026-04-28)

- **23 vídeos** processados (ambas as DBs).
- **109** `video_insights` BR, **9** US.
- **114** `video_themes` BR.

## Integrações

- **Trigger engine** (`scripts/trigger_monitor.py`) pode ler `video_insights` (ex: `kind='dividend'` com `stance='bearish'` → trigger REVIEW).
- **Thesis manager** cross-refs claim vs DB (CEO diz "deleveraging" mas `net_debt_ebitda` sobe → flag).
- **Briefing matinal** (`agents/morning_briefing.py`) pode injectar contexto qualitativo de vídeos recentes.
- **`research.py`** — secção `[V] VIDEO EVIDENCE` (Phase 3 do plano original).

## Workflow recomendado

1. **Antes** de pedir a Claude para "analisar vídeos do canal X" → correr `yt_digest --channel "X"` primeiro. Feed Claude com o digest, não com raw insights.
2. Para iterar prompt/validator → `yt_reextract --all` (zero rede/GPU, só Ollama).
3. Novos canais → adicionar a `config/youtube_sources.yaml`; novos tickers populares em lives → adicionar aliases a `config/aliases.yaml`.

## Ver também
- [[Token_discipline]] — porque 100% local
- [[Agents_layer]] — pode envolver isto num agent cron
- [[Analyst_Tracking]] — analistas em vídeo são uma fonte cross-checkable
- [[Web_scraping_subscriptions]] — pipeline irmão (texto vs áudio)
