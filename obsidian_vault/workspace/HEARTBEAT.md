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

### Founder-only — capabilities (2026-05-08, 3/4 fechadas mesmo dia)

- [x] **YouTube source no `design.scout`** — `YOUTUBE_API_KEY=AIzaSyCd...` adicionado ao `.env` 17:08. Confirmed live: 15 vídeos pulled na primeira corrida, design.scout pipeline end-to-end OK.
- [x] **Schedule q4h tier** — `schtasks /Create /SC HOURLY /MO 4 /TN "ii-q4h" /TR "...\q4h_run.bat" /F` executado 18:00. Next run 09/05 01:20.
- [x] **Schedule hourly tier** — `schtasks /Create /SC HOURLY /TN "ii-hourly" /TR "...\hourly_run.bat" /F` executado 18:00. Next run 08/05 22:20.
- [ ] **GitHub PAT para o `design.scout` + `discovery.skills`** — github.com/settings/tokens → Generate new (classic) → scope `read:public_repo` → `GITHUB_TOKEN=...` no `.env`. Sobe rate limit 60→5000/h. Não-bloqueante: design.scout funciona com 60/h, mas com PAT alarga queries.

## Auto-injected (retry wrapper failures)

- [ ] >> C:\Users\paidu\investment-intelligence\.venv\Scripts\python.exe scripts\pod_poll.py --max-per-feed 1  <!-- failed POD-POLL, exit=124 after 3 attempts at 2026-05-09T04:35:32+00:00 -->  <!-- ran 2026-05-09T13:49:57+00:00, exit=1 -->  <!-- ran 2026-05-09T20:38:16+00:00, exit=1 -->  <!-- ran 2026-05-10T20:39:25+00:00, exit=1 -->
<!-- scripts/_retry.py appends rows here when a daily/hourly step fails all attempts. agents._heartbeat replays them on next run. -->
