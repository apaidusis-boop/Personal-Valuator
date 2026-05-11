---
type: postmortem-followup
parent: Postmortem_2026-05-09_synthetic_ic.md
date: 2026-05-10
component: Ollama infra hardening
status: in-progress
---

# Follow-up — 2026-05-10 — Ollama infra hardening

> Continuação do postmortem 2026-05-09. Verifica persistência das fixes,
> fecha o item P3 (gemma corruption check), e endereça o TODO de restaurar
> diversidade multi-family no synthetic IC.

## Verificação — fixes do postmortem persistiram?

| Item | Estado actual | Verificado |
|---|---|---|
| `CUDA_VISIBLE_DEVICES=0` | **Set (User)** | env var read 2026-05-10 |
| `OLLAMA_FLASH_ATTENTION=1` | **Set (User)** | env var read 2026-05-10 |
| `OLLAMA_KEEP_ALIVE=30m` | **Set (User)** | env var read 2026-05-10 |
| `MODEL_TALEB = qwen14b` | **Set + committed** | `dff6c2a` 2026-05-10 |
| `--majority 3` removed | **Done in postmortem** | git log midnight script |
| Smoke test gate | **Done in postmortem** | git log midnight script |

**Probe re-run 2026-05-10**:

| Modelo | t/s 2026-05-09 (após fix) | t/s 2026-05-10 (hoje) | Status |
|---|---:|---:|---|
| qwen2.5:14b-instruct-q4_K_M | 170 | **186** | ✅ +9% (margin de jitter) |
| qwen2.5:32b-instruct-q4_K_M | 13.1 | **14.1** | ✅ +8% |

Conclusão: **GPU offload sobreviveu reboot/restart** sem regressão. Probe script
guardado em `scripts/_ollama_probe.py` para health check on demand.

## P3 — Gemma corruption check (CONCLUÍDO)

Confirmação directa via `scripts/_gemma_corruption_check.py`:

| Regime | Resultado |
|---|---|
| Generic prompt, temp=0.0 | 250 tok contados, **output vazio** (`''`) |
| synthetic_ic prompt, temp=0.3 | 400 tok contados, **output vazio** (`''`) |
| synthetic_ic prompt, format=json | **0 tok**, degeneração `'own own own...'` |

**Diagnóstico**: gemma4:31b está **funcionalmente quebrado** neste install.
Não é prompt sensitivity (testado em 3 regimes); não é sampling param (temp=0
deveria ser determinístico mas continua vazio). Causa provável: incompat
entre **Ollama 0.23.2 + gemma4 31B Q4_K_M tokenizer** em Windows. O modelo
incrementa `eval_count` mas emite tokens que decodificam para string vazia
ou repetições de 1-token.

**Decisão**: não tentar `ollama pull gemma4:31b` para refresh (19GB de risco
sem garantia). Pular para substituto de família diferente.

## Substituto não-Qwen para Taleb persona — em progresso

**Critérios**:
- Família distinta de Qwen (anti latent-space-echo-chamber)
- Cabe em <16GB VRAM (margem com qwen32B já carregado)
- JSON-mode estável

**Candidatos avaliados**:

| Modelo | Tamanho | Família | Decisão |
|---|---:|---|---|
| llama3.3:70b-instruct | 40GB | Meta | ❌ não cabe (32GB VRAM) |
| **mistral-small:22b** | **13GB** | **Mistral AI** | ✅ **escolhido** — fits, estável, JSON OK |
| gemma3:27b | 16GB | Google | ⚠ risco herdar bug família gemma |
| phi-4:14b | 9GB | Microsoft | candidato secundário se mistral falhar |

**Acção 2026-05-10**: `ollama pull mistral-small:22b` em background.

## VRAM accounting com mistral juntando-se

Stack pós-mistral (síncrono, com `MAX_LOADED_MODELS=1`):
- qwen2.5:14b-instruct-q4_K_M: 8.4 GB
- qwen2.5:32b-instruct-q4_K_M: 19 GB
- mistral-small:22b: 13 GB
- **Total se carregassem em paralelo**: 40.4 GB > 32 GB → swap thrashing

**Mitigação aplicada 2026-05-10**:
```
OLLAMA_MAX_LOADED_MODELS = 1  (User)
OLLAMA_NUM_PARALLEL      = 1  (User)
```

Com isto, Ollama força evict do modelo anterior antes de carregar o próximo.
Custo: ~10-15s overhead por troca de modelo (load_duration medido). Para
synthetic_ic com 3 modelos distintos × 5 personas (sequencial): ~30-45s
overhead total por ticker. Aceitável vs 600s timeout cap.

> ⚠ **Pendente**: estes env vars só fazem efeito quando Ollama service for
> restartado. Aplicar quando o pull do mistral acabar (evita interromper
> download).

## TODO restantes

- [ ] Aguardar pull mistral-small completar (~1h em 3.1 MB/s)
- [ ] Probe mistral-small:22b — confirmar t/s razoável + JSON estável
- [ ] Restart Ollama service (aplica MAX_LOADED_MODELS=1)
- [ ] Wire `MODEL_TALEB = "mistral-small:22b"` em `agents/synthetic_ic.py`
- [ ] Smoke test: `python -m agents.synthetic_ic ACN --majority 1` →
      esperado <120s, 5/5 personas com JSON válido
- [ ] Commit + atualizar este doc com resultado final

## Referências

- Postmortem original: `obsidian_vault/Postmortem_2026-05-09_synthetic_ic.md`
- Probe script: `scripts/_ollama_probe.py`
- Gemma check script: `scripts/_gemma_corruption_check.py`
- Commit Taleb fallback: `dff6c2a` (2026-05-10)
