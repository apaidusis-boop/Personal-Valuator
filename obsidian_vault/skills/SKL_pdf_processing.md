---
type: skill
tier: S
skill_name: pdf-processing
source: anthropics/skills
status: backlog
sprint: W.1
tags: [skill, tier_s, pdf, document]
---

# 📄 PDF Processing (Anthropic Skills)

**Repo**: https://github.com/anthropics/skills (subfolder `document-skills/pdf`)
**Fit**: 🎯 **Altíssimo** — temos pipeline PDF existente via Ollama que falha em tabelas complexas.

## O que faz
Skill oficial Anthropic que usa Claude para extrair conteúdo estruturado de PDFs: texto, tabelas, figuras, layout multi-coluna. Retorna JSON estruturado pronto para consumo.

## Onde integra no nosso projeto
- **Primário**: `fetchers/subscriptions/_pdf_extract.py` — hoje faz `pypdf → Ollama Qwen 14B`. PDFs da Suno/XP/WSJ/BTG com tabelas de recomendações (ex: "Carteira Top Div" com 10 tickers + pesos + preços-teto) frequentemente perdem structure.
- **Secundário**: fatos relevantes CVM que vêm em PDF (`monitors/cvm_monitor.py`)
- **Terciário**: 10-K/20-F filings SEC (`monitors/sec_monitor.py`)

## Fluxo proposto (W.1)
```
PDF → pypdf extract (local, grátis) ─ sucesso? → Ollama Qwen (in-house, grátis)
                                    └─ falha/tabela complexa → Claude PDF skill (pago, só em fallback)
```

**Flag**: `--use-claude-pdf` em `_pdf_extract.py::extract_insights()`. Default OFF (respeita [[../_MOC|in-house first]]).

## Benchmark a correr (W.1)
1 relatório real de cada subscription (Suno BDRs, XP Top Div, BTG PS, WSJ):
- Ollama: N insights extraídos, tempo, custo = $0
- Claude PDF skill: N' insights, tempo, custo em tokens
- Diff qualitativo: quais insights só Claude pegou?

## Instalação
```bash
# Clone do repo oficial
git clone https://github.com/anthropics/skills ~/.claude/anthropic-skills
cp -r ~/.claude/anthropic-skills/document-skills/pdf ~/.claude/skills/
```

## Riscos / watch-outs
- **Tokens**: PDFs de 50+ páginas custam $ sério. Cap `max_pages` agressivo.
- **Duplicação**: se Ollama já extrai bem, não repetir. A/B test antes.
- **Cache**: armazenar output em `data/pdf_cache/<hash>.json` — mesmo PDF nunca re-processado.

## Blockers
Nenhum. Pipeline existe; skill só adiciona 1 branch de fallback.
