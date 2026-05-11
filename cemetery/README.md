# 🪦 Cemetery — Quarantine Area

Files and folders enterrados pelo `agents/mega_auditor.py --bury` aguardam aqui antes
de delete definitivo. Princípio: **reversível por default**.

## Estrutura

```
cemetery/
├── README.md             # este ficheiro
├── <DATE>/               # data do enterro (run_date do audit)
│   ├── manifest.md       # o que foi enterrado, porquê, como restaurar
│   └── <CATEGORY>/       # CODE-DEAD, VAULT-EMPTY, etc.
│       └── <orig_path>   # estrutura original preservada
```

## Restaurar

Cada entrada no `manifest.md` tem comando `git mv` para restaurar para localização
original. Ou usa `python -m agents.mega_auditor --exhume <ID>` (futuro).

## Truly delete

Após N dias (recomendado 30+) sem regressão observada, podes apagar a pasta de
data inteira: `rm -rf cemetery/<DATE>`. Se algo dependia daquele código, já saberias
neste ponto.

## Política

- Burial é registado em git (move, não delete)
- Cada burial tem manifest com reason
- FOLDER-EMPTY são apenas registadas (não há content para mover)
- VAULT-EMPTY e VAULT-DEPRECATED preservam path completo dentro de `vault/`
