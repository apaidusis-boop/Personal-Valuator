---
title: HEARTBEAT
purpose: Checklist editável de tarefas ad-hoc para perpetuum_master executar além do schedule YAML.
edit: humano-editável; vazio = skip; cada bullet é uma instrução em PT-BR.
---

# HEARTBEAT — Checklist de heartbeat

Vazio (sem bullets) = perpetuum_master usa só o schedule de `config/agents.yaml`.

## Como funciona

- `perpetuum_master.py` lê este ficheiro a cada invocação (cron 23:30 ou manual).
- Cada bullet `- [ ] <comando ou descrição>` é executado uma vez. Marca `- [x]` quando feito.
- Items `- ` (sem checkbox) são notas/lembretes — não executados, só lidos.
- Items com prefixo `>>` são comandos exactos para shell (corre como subprocess).

## Comandos suportados

- `>> python -m library.ri.cvm_parser build` — qualquer script do catalog.
- `>> ii panorama X` — qualquer ii sub-command.
- Texto livre `- [ ] verificar X` é registado no daily log mas não executado automaticamente.

## Examples (markdown, dentro de fenced block — não executa)

```markdown
- [ ] >> python scripts/perpetuum_action_run.py list-open
- [ ] verificar se PVBI11 publicou fato relevante esta semana
- nota: founder pediu para reduzir cadence do RI parser de daily para weekly
```

## Active items

<!-- Adiciona items abaixo desta linha. -->
