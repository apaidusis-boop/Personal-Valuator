---
type: playbook
name: Analysis Workflow — ideal flow
tags: [playbook, workflow, tokens, efficiency]
related: ["[[Token_discipline]]", "[[Buy_checklist]]", "[[Sell_triggers]]"]
---

# 🔀 Analysis Workflow — do sinal à decisão

> **Princípio**: executar o **comando mais curto que responde à pergunta**. Claude só entra para síntese/decisão; nunca para data gathering.

## Fluxo canónico por caso de uso

### 1. "Dá-me panorama sobre X"

```bash
ii panorama X           # TUDO: verdict + peers + triggers + notes + videos + wiki links
```

Ou a forma granular se só queres uma peça:

```bash
ii verdict X --narrate --write   # verdict + narrativa em vault
ii peers X                       # percentil vs sector
ii actions list --ticker X       # triggers abertos
ii notes show X                  # observações tuas
```

**Nunca** pedir a Claude "analisa X" sem correr `ii panorama X` primeiro.

### 2. "Passa no screen?"

```bash
python scoring/engine.py X --market br   # OU us
```

Saída: PASS/FAIL + breakdown por critério.

### 3. "Distress? Quality?"

```bash
ii altman X         # Z-Score
ii piotroski X      # F-Score
ii safety X         # Dividend Safety 0-100
```

### 4. "Comparativa A vs B vs C"

```bash
ii compare A B C [--vs SPY]
```

### 5. "Payback DRIP / projeção"

```bash
ii drip --ticker X --payback         # anos para 2× shares
ii drip --ticker X --horizons 5,10,15 # projeção multi-horizonte
```

### 6. "O que disse sobre X no passado"

```bash
ii notes show X           # notas tuas
ii vault "o que disse sobre X"   # semantic search Ollama Qwen 14B
```

### 7. "Mudanças desde ontem"

```bash
ii diff --since 1          # daily diff
ii brief                   # briefing completo
```

### 8. "Análise de vídeo YouTube"

```bash
ii ingest <url>                          # ingere se novo
ii digest --channel "NomeCanal" --days 30 # digest SQL-only
ii reextract --video <id>                # re-extrair com Ollama
```

### 9. "Análise de relatório analista (subscription)"

```bash
ii subs fetch --source suno              # download PDFs novos
ii subs extract --source all             # Ollama extrai key points
ii subs query X                          # views sobre ticker X
```

Ver [[Web_scraping_subscriptions]] para setup inicial.

### 10. "Rebalance / sizing"

```bash
ii rebalance [--cash-add 5000]
ii size X --cash 10000
```

## Anti-padrões

### ❌ Evitar
- Pedir a Claude para ler 10 ficheiros Obsidian para formar opinião → `ii vault` faz isto via embeddings.
- Re-fetch preço em chat → `ii refresh X` é 1 call, 0 tokens.
- Reproduzir tabelas de CLAUDE.md ou wiki → remeter user para fonte.
- Copiar output de `ii verdict` para chat quando já está gravado em vault.

### ✅ Fazer
- Default reflex: "panorama de X" → `ii panorama X --write` → user lê no Obsidian.
- Se script não existe para o caso: **criar comando `ii`** em vez de repetir work manual.
- Escalar para Claude só quando há síntese não-computável (decisão estratégica com tradeoffs).

## Workflow matinal recomendado

```bash
# 09:00 (cron corre 23:30 night before)
ii brief                           # P&L + moves + triggers + earnings
ii diff --since 1                  # o que mudou
ii panorama <top-move-ticker>      # dig no maior mover
ii actions list                    # triggers pendentes
# abrir Obsidian → _MOC → dashboards
```

## Decisão workflow — "devo comprar/vender?"

1. `ii panorama X` → estado factual actual
2. [[Buy_checklist]] ou [[Sell_triggers]] → verificação por regras
3. **Só** então: Claude para síntese se tradeoff ambíguo → justificação documentada
4. `ii notes add X "decisão + raciocínio" --tags buy,thesis` → journal
5. Trade executado → `ii tx buy X ...`

## Medição

**Token cost** típico por query:

| Query | Inhouse | Claude tokens |
|---|---|---|
| `ii panorama X` | ~8s | ~500 (síntese final) |
| Spelunking manual Claude | 30-60s | **5-10k** |
| `ii brief` | ~5s | 0 |
| `ii vault "pergunta"` | ~15s | 0 (Ollama) |

Ratio esperado: **> 90% das queries inhouse**, Claude só para ~10%.

## Self-test

Antes de responder, pergunta-se:
- [ ] Existe `ii` command que resolve isto?
- [ ] Se não, existe script em `scripts/` ou `fetchers/`?
- [ ] Se não, vault_ask / Ollama resolve semanticamente?
- [ ] Se não, confirmado — Claude é necessário.

Se todas "sim" antes da última → **usar inhouse**, reportar resumo curto.

## Related

- 🚨 [[Token_discipline]] — a meta-regra
- [[Buy_checklist]] · [[Sell_triggers]]
- [[Web_scraping_subscriptions]] — adapters para relatórios externos
