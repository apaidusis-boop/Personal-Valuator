---
title: Cloud Memory & Remote-Engine Architecture — Decision Memo
date: 2026-05-04
status: AWAITING_DECISION
author: claude
---

# Cloud Memory + Remote-Engine Architecture

## Problema

> "Quero ver sobre a possibilidade de conseguir manter algo em Cloud para que eu
> possa acessar a memória de outro lugar para continuar editando e usando outras
> máquinas como motores, quando estiver trabalhando fora."

Três coisas distintas, fáceis de confundir:

1. **Memória do Claude Code** (`~/.claude/memory/*.md`) — preferências, feedback, projecto. Hoje vive só na máquina local.
2. **Estado do projecto** (`investment-intelligence/` — código, vault, DBs, configs). Hoje está em git mas nem tudo é commitado (DBs, logs, .env).
3. **Motor LLM** (Ollama em `localhost:11434`). Hoje exclusivamente local na máquina principal. Quando estás fora com o laptop pequeno → não tens 14B/32B.

Cada uma destas três precisa de uma solução diferente. A pergunta certa não é "como ponho na cloud" — é "qual destas três vale a pena?".

---

## 4 Opções

### A — GitHub privado como single source of truth (sem Ollama remoto)

```
[máquina principal]  →  git push  →  [GitHub repo privado]  ←  git pull  ←  [laptop]
   Ollama local                                                                Ollama local (ou Claude API)
```

- **O que vai para o repo**: `~/.claude/memory/` + `obsidian_vault/` + código (já está). DBs **não** (binárias, grandes).
- **Acesso à memória**: `git pull` antes de começar a sessão; `git push` no fim. Pode ser automatizado num hook `Stop` do Claude Code.
- **Motor**: cada máquina precisa do próprio Ollama OU usa Claude API (queima budget).
- **Custo**: 0
- **Setup**: 30 min
- **Risco**: nenhum significativo. Standard.
- **Limitação real**: laptop pequeno sem GPU → corre só 7B com qualidade fraca, ou paga Claude API.

**Perfeito para**: trabalhar de outra máquina forte (segundo desktop, hotel com workstation).
**Mau para**: laptop em viagem.

---

### B — Tailscale + máquina principal sempre ligada como engine remoto

```
[laptop em viagem]                    [máquina principal sempre ON]
  Claude Code                            Ollama 14B/32B em :11434
  $env:OLLAMA_URL = http://100.x.x.x:11434
       └──────── Tailscale VPN privada (ZeroTier alternativo) ────────┘
```

- **Tailscale**: VPN P2P encriptada, free tier para uso pessoal. Instalação `winget install tailscale.tailscale`. Gera IPs `100.x.x.x` que só os teus dispositivos vêem.
- **Configurar**: na máquina principal abrir o porto 11434 só para Tailscale (não para a internet pública). Editar `agents/_llm.py:24` para ler `OLLAMA_URL` do env.
- **Memória**: continua a precisar de sync — Tailscale resolve o motor mas não a memória. Combinar com **A** (GitHub) ou Syncthing.
- **Motor**: laptop usa o 32B que vive na principal. Latência ~100-300ms em vez de 2-5s (porque é só a network round-trip; o compute é igual).
- **Custo**: 0
- **Setup**: 1-2h
- **Risco**: principal desliga → laptop fica sem motor (fallback para Claude API ou Ollama 7B local).

**Perfeito para**: viagens curtas onde a principal fica em casa ligada.
**Mau para**: principal em casa com cortes de luz / wi-fi instável.

---

### C — Cloudflare Tunnel + R2 + Workers AI (mais cloud-native)

```
[qualquer máquina]  →  Cloudflare Worker (auth) →  Tunnel  →  Ollama na principal
                       R2 storage                ←  sync   ←  ~/.claude/memory/
                       Workers AI (Llama 3.1 70B)  ← fallback se principal off
```

- **Cloudflare Tunnel**: expoe `localhost:11434` publicamente com auth Cloudflare Access (Google SSO).
- **R2**: storage S3-compatible, 10 GB grátis. Sync de memory + vault.
- **Workers AI**: 10K neurons/dia grátis (~Llama 3.1 70B chamadas).
- **Custo**: 0 dentro do free tier; depois $5/mês por GB-mês.
- **Setup**: 2-3h
- **Vantagem sobre B**: redundância — se a principal cair, Workers AI cobre.
- **Desvantagem**: mais infra para manter; depende da Cloudflare.

**Perfeito para**: ficares 100% independente da máquina principal.
**Mau para**: complexidade. Vale só se a principal for unreliable.

---

### D — Hybrid pragmatic (recomendação)

```
                         GitHub privado (memory + vault + código)
                              ↑                ↓
[máquina principal]      git push/pull    [laptop / outra máquina]
  Ollama 32B/14B                              Claude Code
  Tailscale node                              Tailscale node (OLLAMA_URL → 100.x.x.x principal)
       │
       └──── DBs grandes em Backblaze B2 (10GB free) via rclone ────┐
                                                                     ↓
                                                          [laptop precisa de DB? `rclone sync`]
```

**Componentes:**
1. **Memory + Vault → GitHub privado** (Opção A). Hook `Stop` do Claude Code faz `git add memory/ && git commit -m "auto-sync $(date)" && git push` (silencioso).
2. **Motor → Tailscale tunnel** (Opção B). Laptop aponta `OLLAMA_URL` para a principal. Fallback Claude API se principal offline.
3. **DBs SQLite (`data/*.db`) → Backblaze B2** ou R2. `rclone sync` no início/fim de sessão. Não vai para git porque são MBs e mudam constantemente.
4. **`.env` (BRAPI/MASSIVE/Tavily keys) → 1Password CLI** (`op` command). Nunca em git. Pull on demand.

**Custo**: 0 (GitHub free tier privado, Tailscale free, B2 10GB free).
**Setup**: 2-3h.
**Manutenção**: baixa. Tudo automatizado em hooks.

---

## Comparação

| Dimensão               | A (Git only) | B (Tailscale)  | C (Cloudflare) | **D (Hybrid)** |
|------------------------|--------------|----------------|-----------------|----------------|
| Memory acessível       | ✅            | ❌ (só engine) | ✅              | ✅             |
| Engine remoto          | ❌            | ✅             | ✅              | ✅             |
| DBs sincronizadas      | ❌ (gitignored)| ❌            | ✅ (R2)         | ✅ (B2)        |
| Resiliência principal  | n/a          | Falha total   | Workers AI fallback | Claude API fallback |
| Setup time             | 30 min       | 1-2h          | 2-3h            | 2-3h           |
| Custo                  | 0            | 0             | 0 (free tier)   | 0              |
| Complexidade           | Baixa        | Média         | Alta            | Média          |
| Vendor lock-in         | GitHub       | Tailscale     | Cloudflare      | Disperso (bom) |

---

## Recomendação

**Opção D**, mas em fases:

- **Fase 1 (hoje, 30 min)**: Activar **A** sozinha. Cria repo privado `paidu/.claude-memory` (ou similar) e `paidu/investment-intelligence-private` e wire `Stop` hook para `git push`. **Resolve 80% do problema** sem dependências externas.

- **Fase 2 (quando primeira viagem)**: Adicionar **B**. Instalar Tailscale nas duas máquinas, abrir porto, testar com `OLLAMA_URL` env var. **Resolve o engine remoto**.

- **Fase 3 (se sentires falta)**: Adicionar B2/rclone para DBs. **Resolve trabalho data-heavy fora**.

Razão para faseamento: cada componente tem custo de manutenção. Adicionar tudo de uma vez = cerimónia que se desfaz quando algo falhar. Adicionar quando há *pain* concreto = cada peça justifica-se.

---

## Decisão pendente

Antes de tocar em infra, preciso de saber:

1. ~~Já tens conta GitHub?~~ **Sim** — `apaidusis-boop/Personal-Valuator` já é o remote do projecto. Confirmar se é privado e se já abrange `obsidian_vault/` (tem que ver `.gitignore`).
2. **A máquina principal fica ligada quando viajas?** (Decide se B é viável.)
3. **Que tipo de máquina é o laptop fora?** (Laptop com 16GB+ corre 14B local — Tailscale é nice-to-have, não obrigatório.)
4. **Privacidade da memory**: dados pessoais sobre tickers, posições, valor patrimonial. Confirmas que `Personal-Valuator` é repo privado? (Eu não consigo verificar do CLI sem `gh auth`.)
5. **Memory do Claude Code** (`~/.claude/projects/C--Users-paidu/memory/`) — repo separado ou subdir do `Personal-Valuator`? Recomendo separado — mais limpo, e a memory é cross-project.

Com 1+2+3+4 respondidos consigo executar o setup em ~30 min.

---

## Implementação Fase 1 (preview, não correr ainda)

```powershell
# Criar repos no GitHub (web UI)
# 1. paidu/investment-intelligence-vault  (privado)
# 2. paidu/claude-memory                  (privado)

# Local
cd C:\Users\paidu\.claude\projects\C--Users-paidu\memory
git init && git remote add origin git@github.com:paidu/claude-memory.git
git add . && git commit -m "initial memory" && git push -u origin main

# Hook em ~/.claude/settings.json:
# "hooks": {
#   "Stop": [{"command": "cd ~/.claude/projects/C--Users-paidu/memory && git add . && git commit -m \"auto $(date -Iseconds)\" --allow-empty && git push -q || true"}]
# }
```

Vault e investment-intelligence já estão sob git mas o remote é local — confirmar se há remote GitHub.

---

## Próximos passos

Aguardo resposta às 4 perguntas em "Decisão pendente". Sem elas, não avanço infra.
