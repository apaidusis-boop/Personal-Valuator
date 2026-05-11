---
type: postmortem
date: 2026-05-09
severity: high
component: agents.synthetic_ic + Ollama infra
duration_lost: 7.5h overnight
data_lost: zero (no destructive ops); only compute time wasted
---

# Postmortem — 2026-05-09 — synthetic_ic Phase 5 wasted 7.5h

## TL;DR

A phase 5 do `scripts/midnight_2026-05-09.py` (multi-agent validation chain)
correu durante ~7.5h e **produziu zero output útil** — 24/24 calls a
`agents.synthetic_ic` deram timeout. A causa não é um bug, são **três bugs
em camadas que se amplificam mutuamente**:

| # | Bug | Magnitude | Camada |
|---|---|---|---|
| 1 | **Ollama não está a usar GPU como devia** | 6-10× mais lento que esperado | infra |
| 2 | **Gemma 31B produz output degenerado** (`"ownable ownable..."`) | Taleb sempre falha | model |
| 3 | **VRAM 32 GB < 45 GB modelos combinados** | swap forçado entre personas | config |
| 4 (multiplicador) | **`--majority 3`** triplica o custo total | 3× wall-clock | orchestrator |
| 5 (multiplicador) | **Orchestrator timeout 600s** matava cada call antes de acabar | kill garantido | orchestrator |

## Evidência colhida (não especulação)

### Evidência 1 — GPU está praticamente parada

```
nvidia-smi: RTX 5090, 3930 MiB / 32607 MiB used (12%), 8% utilization
```

Para qwen2.5:14b (8.4 GB) deveria estar **8400+ MiB** em VRAM e **>50%**
utilização durante inferência. **Está a usar 12% da VRAM**. Diagnóstico:
Ollama está a fazer offload mínimo de layers para GPU (provável CPU-heavy).

### Evidência 2 — Tokens por segundo brutalmente baixos

Probe directo a cada modelo (ver `_tmp_ollama_probe.py` corrido às 09:xx):

| Modelo | Tokens/sec medido | Esperado em RTX 5090 | Razão |
|---|---:|---:|---:|
| qwen2.5:14b-instruct-q4_K_M | **4.9** | 30-50 | **6-10× lento** |
| qwen2.5:32b-instruct-q4_K_M | **2.3** | 15-25 | **6-10× lento** |
| gemma4:31b | 2.7 | 12-18 | **5-7× lento** |

Em RTX 5090 com GPU offload correcto, qwen14b deveria correr em ~5s para
500 tokens. Está a correr em 27s. Cada chamada do synthetic_ic faz 5 personas
× 1 chamada (single mode) = ~135s mínimo. Com `--majority 3` = ~405s mínimo.
O timeout do orchestrator era **600s**, então ficou no fio da navalha mesmo
no melhor caso.

### Evidência 3 — Gemma 31B output degenerado

Probe directo:

```json
{"verdict": "BUY", "conviction": 9, "rationale": ["High ownable ownable
ownable ownable ownable ownable ownable ownable ownable ownable ownable
ownable ownable ownable ownable ownable ownable ownable ownable ownable
[...continua até 500 tokens]
```

JSON inválido. Pydantic schema `PersonaVerdict` rejeita. `ollama_call_typed`
devolve None. `ask_persona` regista `_error: "ollama_or_validation_failed"`.
A persona Taleb (atribuída a `gemma4:31b` por design — diversidade de family
para anti-echo-chamber) **falha sempre**.

Possíveis causas para a degeneração:
- Modelo corrompido (verificar com `ollama show gemma4:31b`)
- Template de prompt incompatível com o que `ollama_call` envia
- Quantização agressiva
- Tag `gemma4:31b` errada (talvez user quis `gemma2:27b` ou similar)

### Evidência 4 — VRAM thrashing forçado

```
qwen2.5:32b   18.5 GB
qwen2.5:14b    8.4 GB
gemma4:31b    18.5 GB
nomic-embed    0.3 GB
TOTAL         45.7 GB

VRAM disponível: 32 GB

Excesso: 13.7 GB → impossível ter 32B + 31B carregados ao mesmo tempo.
```

Sequência típica de uma chamada synthetic_ic (5 personas serial):

| Step | Persona | Modelo | VRAM action | Cost |
|---|---|---|---|---|
| 1 | Buffett | qwen32b | load cold | +30s |
| 2 | Druck | qwen14b | load (fits side-by-side) | +15s |
| 3 | Taleb | gemma31b | **evict qwen32b**, load gemma | +30s + 185s gen + fail |
| 4 | Klarman | qwen32b | **evict gemma**, **reload** qwen32b | +30s + 47s gen |
| 5 | Dalio | qwen14b | reuses se ainda em VRAM | +27s |

Best case: ~360s. Worst case (com fails + retries): ~600s. **Timeout
orchestrator: 600s.** Logo, todo o trabalho hit-or-miss em cada ticker.

### Evidência 5 — Run de verificação ao vivo (08:50 hoje)

```
$ python -m agents.synthetic_ic JPM --market us
=== Synthetic IC: US:JPM ===
  asking Warren Buffett... FAIL (ollama_or_validation_failed)
  asking Stan Druckenmiller... BUY (conv 7)         ← qwen14b OK
  asking Nassim Taleb... FAIL (ollama_or_validation_failed)  ← gemma broken
  asking Seth Klarman... FAIL (ollama_or_validation_failed)
  asking Ray Dalio... HOLD (conv 7)                 ← qwen14b OK
  -> committee: MIXED (low)  saved: ...JPM_IC_DEBATE.md  (491.3s)
```

3 de 5 falham. Apenas as 14B passam. Total 491s para 1 ticker single-mode.

## Por que custou exactamente 7.5h e não 30min

```
Phase 5 começou: 01:03:09
Último log de synthetic_ic: 08:40:49 (start de ITSA4)
Process morreu algures entre 08:40:49 e 08:57:49 (quando user pediu "Me abra")

Tempo de phase 5: ≈ 7.5h
Tickers processados: 24 (até ITSA4 inclusive, 9 ainda por fazer)
Tempo médio por ticker: 7.5h / 24 = ~19 min/ticker

Cada ticker fazia:
  - 1× synthetic_ic com --majority 3 → timeout aos 600s = 10min queimados
  - 1× variant_perception → ~3s (skip silencioso)
  - Algum overhead de subprocess + log
  ≈ 11-25min/ticker dependendo de qual persona falhou primeiro

24 tickers × 19min = 456min ≈ 7.6h ✓ confere
```

O custo foi 100% **cap a esperar pelo timeout** (cada ticker queimou 10min
inteiros à espera). O orchestrator não tinha early-exit em "todas as
personas falharam" — esperava o ciclo completo.

## Por que não detectei em smoke test

Eu fiz smoke test apenas da `phase_inventory()`. Não fiz smoke test do
`synthetic_ic` antes de detachar a noite inteira.

**Lesson**: para qualquer phase que use Ollama, fazer dry-run de 1 ticker
e medir tempo + verificar output ≠ "_error". Só depois detachar.

## Fixes recomendados (por prioridade)

### Fix 1 (P0, bloqueante) — Ollama GPU offload
```bash
# Verificar
ollama show qwen2.5:14b-instruct-q4_K_M --modelfile

# Set explicit GPU layers via env
$env:OLLAMA_NUM_GPU = "999"     # all layers
$env:OLLAMA_GPU_OVERHEAD = "0"  # no CPU buffer
$env:OLLAMA_FLASH_ATTENTION = "1"

# Restart Ollama service
Stop-Process -Name ollama* -Force
ollama serve   # ou via service manager Windows
```

Verificar com `nvidia-smi` durante uma chamada — VRAM deveria saltar para
8 GB+ e GPU util para >50%.

**Sem isto, qualquer outro fix é band-aid.**

### Fix 2 (P0) — Substituir Gemma na persona Taleb
Até diagnosticar a degeneração, mapear Taleb para `qwen2.5:14b` (perde
diversidade de family mas não falha sempre).

```python
# em agents/synthetic_ic.py
MODEL_TALEB    = "qwen2.5:14b-instruct-q4_K_M"  # was: "gemma4:31b" (broken)
```

### Fix 3 (P1) — Drop `--majority 3` por default
3× cost por ganho marginal de variância. Único caso onde vale: análise final
única antes de trade. Para overnight observer, single run chega.

```python
# em scripts/midnight_2026-05-09.py
run_cmd(f'... synthetic_ic {tk}', timeout=600)   # was: --majority 3
```

### Fix 4 (P1) — Se VRAM thrashing persistir mesmo com GPU OK
Pin all personas to qwen2.5:14b (homogeniza, perde diversidade mas elimina
swap):

```python
PERSONAS = {
    "buffett": {..., "model": MODEL_QWEN_14B},
    "druckenmiller": {..., "model": MODEL_QWEN_14B},
    "taleb": {..., "model": MODEL_QWEN_14B},
    "klarman": {..., "model": MODEL_QWEN_14B},
    "dalio": {..., "model": MODEL_QWEN_14B},
}
```

OU manter o design mas adicionar warmup explícito + `keep_alive: -1`
no payload Ollama para evitar evictions.

### Fix 5 (P2) — Early-exit no orchestrator quando run inteiro falha
```python
# em scripts/midnight_2026-05-09.py
def phase_multi_agent():
    consecutive_failures = 0
    for tk, mkt in holdings:
        r = run_cmd(...)
        if r is None or r.returncode != 0:
            consecutive_failures += 1
            if consecutive_failures >= 3:
                log("3 consecutive failures — bailing", phase)
                break
        else:
            consecutive_failures = 0
```

### Fix 6 (P2) — Smoke test obrigatório no orchestrator
Antes de entrar em phase 5, corre 1 ticker e verifica que `_error` count < 50%.
Se falhar, skip phase 5 e regista no relatório.

## Custos reais da noite

- **Compute wasted**: 7.5h × ~50% GPU + CPU = electricity + heat sem deliverable
- **Data quality cost**: 0 dossiers IC_DEBATE atualizados (era exactamente
  o que pediste — ter agentes a desafiar entre si)
- **Trust cost**: tu acordaste e perguntaste o que aconteceu — relação
  cliente-sistema fica abalada quando promessa não cumpre

## O que SE SALVOU apesar disto

A phase 5 falhou, mas as outras 8 phases produziram dados reais e
verificáveis. O scorecard de provenance, o CAGR table corrigido, e os
backfills SEC + macro são deliverables válidos. Ver `Bibliotheca/Midnight_Work_2026-05-09.md`
para o que tens em DB hoje vs ontem.

## Action items (estes ficam no `A_FAZER.md` P0)

- [x] **Fix 1: Ollama GPU offload — DONE 2026-05-09**
  - Root cause: Ollama 0.23.2 auto-discovery falhou silenciosamente no driver 595.79
  - Fix: `[Environment]::SetEnvironmentVariable("CUDA_VISIBLE_DEVICES", "0", "User")`
  - Bonus envs: `OLLAMA_FLASH_ATTENTION=1` e `OLLAMA_KEEP_ALIVE=30m` (anti VRAM thrash)
  - Resultado medido: qwen14b 4.9 → **170 tok/s (35×)**, qwen32b 2.3 → **13.1 tok/s (5.7×)**
  - Log de proof: `time=2026-05-09T09:37:57 ... library=CUDA compute=12.0 name=CUDA0 description="NVIDIA GeForce RTX 5090" total=31.8 GiB`

- [x] **Fix 2: Substituir Gemma na Taleb persona — DONE 2026-05-09**
  - `agents/synthetic_ic.py` line 50: `MODEL_TALEB = MODEL_QWEN_14B  # was: gemma4:31b (degenerate)`
  - Comment com link ao postmortem para histórico
  - TODO follow-up: identificar substituto não-Qwen (llama3.3 / mistral) para restaurar diversity

- [x] **Fix 3: Drop --majority 3 default — DONE 2026-05-09**
  - `scripts/midnight_2026-05-09.py` phase_multi_agent: removido `--majority 3`
  - Single run por persona é suficiente para overnight observer mode
  - --majority reservado para decision moments explícitos (CLI manual)

- [x] **Smoke-test obrigatório antes de phase 5 — DONE 2026-05-09**
  - Phase 5 começa por correr 1 ticker (smoke), mede tempo + falhas
  - Bail out se: smoke timeout, returncode != 0, ou ≥3 personas falham
  - Bail out adicional: 3 ticker failures consecutivos durante o loop principal
  - Config: smoke_timeout=300s; per-call timeout=300s (era 600s)

- [ ] Verificar com `ollama show gemma4:31b` se o modelo está corrupto (P3)

- [x] **Verificação final do conjunto de fixes — DONE 2026-05-09**
  - Run: `python -m agents.synthetic_ic JPM --market us`
  - Antes: 491s, 3/5 personas FAIL
  - Depois: **75.8s, 0 personas FAIL** ← 6.5× speedup, JSON válido em todas as 5
  - Output: `obsidian_vault/tickers/JPM_IC_DEBATE.md` regenerado (committee MIXED, 5 votos: HOLD/BUY/AVOID/AVOID/HOLD)

## Lesson learned (para a memória do projecto)

> **Antes de detachar uma phase Ollama-heavy para overnight: corre 1 ticker
> em foreground e verifica (a) tempo < timeout, (b) zero `_error` no
> output, (c) GPU está realmente em uso (`nvidia-smi`).**
>
> O custo de 5min de smoke test poupa 7.5h de wasted compute.
