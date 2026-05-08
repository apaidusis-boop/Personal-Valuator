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

### Founder-only — capabilities desbloqueadas se feitas (2026-05-08)

Estas 4 acções activam capacidades inteiras que estão hoje desligadas. Não
são executáveis por agentes (precisam consola admin do user / API keys
pessoais). Quando feitas, marcar `[x]` e remover.

- [ ] **YouTube source no `design.scout`** — Google Cloud Console → New project → Enable "YouTube Data API v3" → Credentials → Create API key → adicionar `YOUTUBE_API_KEY=...` ao `.env`. Free tier: 10k units/dia (~100 search calls). Activa as 3 queries do scout (`claude code design skill`, `claude code dashboard`, `design system tutorial 2026`). Depois: `python scripts/yt_ingest.py <url>` para transcrição local + RAG.
- [ ] **GitHub PAT para o `design.scout` + `discovery.skills`** — github.com/settings/tokens → Generate new (classic) → scope `read:public_repo` → `GITHUB_TOKEN=...` no `.env`. Sobe rate limit 60→5000/h.
- [ ] **Schedule hourly tier no Windows** — `schtasks /Create /SC HOURLY /TN "ii-hourly" /TR "C:\Users\paidu\investment-intelligence\scripts\hourly_run.bat" /F` (admin shell). Phase EE-AOW pendente desde 2026-05-08 manhã.
- [ ] **Schedule q4h tier** — `schtasks /Create /SC HOURLY /MO 4 /TN "ii-q4h" /TR "C:\Users\paidu\investment-intelligence\scripts\q4h_run.bat" /F`. Idem.

## Auto-injected (retry wrapper failures)

<!-- scripts/_retry.py appends rows here when a daily/hourly step fails all attempts. agents._heartbeat replays them on next run. -->
