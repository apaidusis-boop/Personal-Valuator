---
title: Wiki Schema
purpose: Canonical frontmatter spec for vault wiki notes (memory-wiki bridge mode).
edit: humano-editável; loosely enforced via scripts/wiki_lint.py.
---

# Wiki Schema — provenance, confidence, freshness

OpenClaw `memory-wiki` plugin compila durable knowledge num wiki vault com
**claims, evidence, contradiction tracking, freshness**. Fazemos espelho parcial
disso adicionando 3 campos ao frontmatter de cada nota wiki.

## Required frontmatter (todas as notas)

```yaml
---
type: <wiki_index|sector|cycle|method|playbook|holding|macro|tax|history>
name: <human-readable name>
tags: [tag1, tag2]
related: ["[[OtherNote]]"]
---
```

## Recommended (memory-wiki bridge fields)

```yaml
source_class: <cvm|sec|yfinance|brapi|tavily|founder|derived|book:<slug>|video:<channel>>
confidence: <0.0-1.0>          # 1.0 = founder-asserted ou source primária; 0.5 = inferred
freshness_check: <YYYY-MM-DD>  # data da última verificação manual ou auto
```

### `source_class` valores canónicos

- `cvm`        — fonte oficial CVM (filings, fatos relevantes)
- `sec`        — SEC EDGAR
- `yfinance`   — Yahoo Finance scrape
- `brapi`      — brapi.dev
- `tavily`     — autoresearch web (low confidence default)
- `founder`    — founder declarou directamente em conversa/notes
- `derived`    — calculado a partir de outras notas/dados (ex: ratios, scores)
- `book:<slug>`  — livro processado (ex: `book:peter_lynch_one_up`)
- `video:<id>`   — vídeo YouTube ingerido (ex: `video:oOCN30ulVyo`)
- `mixed`      — agregado de múltiplas fontes; especificar em `## Sources` body

### `confidence` rule of thumb

| Range      | Quando usar                                                    |
| ---------- | -------------------------------------------------------------- |
| 0.95-1.00  | source primária + founder confirmado                           |
| 0.80-0.94  | source primária mas não verificado por founder                 |
| 0.60-0.79  | source secundária reputada (Bloomberg, Reuters, broker reports) |
| 0.40-0.59  | inference do agent / Ollama synthesis sem source explícita     |
| 0.20-0.39  | rumor / speculation / contrarian view sem evidence forte       |
| 0.00-0.19  | aspirational / hypothesis a testar                             |

### `freshness_check` cadence

- **Macro/cycle/method notes**: 90d default (raramente mudam).
- **Holding notes**: 30d (fundamentals shift trimestralmente).
- **Sector notes**: 60d.
- **Playbook notes**: 180d (frameworks duráveis).

`scripts/wiki_lint.py --stale` flags notas com `freshness_check` mais antigo que
o cadence default.

## Optional (advanced)

```yaml
claims:
  - claim: "Selic deve cair para 12% até 2027 Q1"
    source_class: derived
    confidence: 0.55
    evidence: "[[Macro_BR_Q3_2025]]"
contradicts: ["[[Note_que_diz_o_oposto]]"]
auto_draft: true        # Ollama-generated, founder ainda não revisou
generated_by: <agent>   # ex: holding_wiki_synthesizer
```

## Validation

```bash
python scripts/wiki_lint.py                    # report all non-conforming
python scripts/wiki_lint.py --stale            # flag stale freshness_check
python scripts/wiki_lint.py --missing-source   # flag notes without source_class
python scripts/wiki_lint.py --apply-defaults   # bulk-add default fields (idempotent)
```
