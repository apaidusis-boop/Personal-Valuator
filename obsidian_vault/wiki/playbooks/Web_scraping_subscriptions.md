---
type: playbook
name: Web Scraping — paid subscriptions
tags: [playbook, scraping, subscriptions, inhouse]
related: ["[[Token_discipline]]", "[[Analysis_workflow]]"]
source_class: founder
confidence: 0.7
freshness_check: 2026-04-30
---

# 🕸 Web Scraping — subscriptions

> Ingerir conteúdo das **tuas subscriptions pagas** sem queimar tokens de LLM. Tudo em-house via cookies exportadas + Ollama extract.

## Arquitetura

```
                ┌─ fetchers/subscriptions/
                │      ├─ _base.py              (abstract BaseAdapter)
                │      ├─ _session.py           (cookie jar / Playwright hybrid)
                │      ├─ _pdf_extract.py       (Ollama PDF → structured)
                │      ├─ wsj.py                (WSJ adapter)
                │      ├─ suno.py               (Suno adapter)
                │      ├─ finclass.py           (Finclass adapter)
                │      └─ xp.py                 (XP Conteúdos adapter)
                │
scripts/        ├─ fetch_subscriptions.py       (orchestrator)
                │
data/           ├─ subscriptions/cookies/       (exported cookies *.json)
                ├─ subscriptions/pdfs/          (downloaded reports)
                └─ subscriptions/html/          (raw HTML snapshots)

DB              └─ analyst_reports              (structured extraction)
                     ticker, source, date, title, key_points_json, ...
```

## Setup único (por site)

### 1. Exportar cookies do browser

Instala extensão **Cookie-Editor** (Chrome/Firefox/Edge):
- `https://cookie-editor.com/` → instala.
- Login no site (wsj.com, suno.com.br, etc.) normalmente.
- Cookie-Editor → **Export → JSON format** → copia.
- Guarda em `data/subscriptions/cookies/<site>.json`.

**Alternativa**: extensão "Get cookies.txt LOCALLY" → formato Netscape → converter.

### 2. Testar

```bash
ii subs test --source wsj    # valida cookies + access
```

Se expira: refrescar browser, re-exportar cookies. Esperar ~30 dias entre refreshes (depende do site).

## Per-site approach

### 🟢 **Suno** (suno.com.br) — **ROI mais alto, começar aqui**

- **Conteúdo**: relatórios PDF (Suno Premium, FIIs, Dividendos, Internacional).
- **Login**: email+senha, cookie `__suno_session` estável (~30d).
- **Formato preferido**: PDF direto.
- **URLs-chave**:
  - `/relatorios/` — lista cronológica
  - `/materiais/` — vídeos + artigos
- **Strategy**: fetch page list → extract PDF URLs → download → Ollama extract → DB.
- **TOS**: pessoal tolerado. Não redistribuir.
- **Priority**: **ALTA** (relatórios brasileiros = edge em BR holdings).

### 🟢 **XP Conteúdos** (conteudos.xpi.com.br) — **ROI alto para BR**

- **Conteúdo**: morning call, relatórios sectoriais, reports de empresas.
- **Login**: conta XP (cliente). Cookie pode ter dual-domain (xpi.com.br + conteudos).
- **Formato**: HTML para artigos, PDF para reports formais.
- **URLs-chave**:
  - `/categoria/renda-variavel/` — BR equity research
  - `/categoria/fundos-imobiliarios/`
  - Feed RSS possível: `/feed/` (checar — WordPress pattern).
- **Strategy**: RSS primeiro (se existe) → HTML full scrape com cookies → PDF download.
- **TOS**: cliente-only content, uso pessoal tolerado.
- **Priority**: **ALTA** para BR holdings.

### 🟡 **WSJ** (wsj.com) — **ROI médio, high-volume**

- **Conteúdo**: notícia + analysis + Heard on the Street + editorial.
- **Login**: email+senha, cookie `wsjgdpr` + session + membership.
- **Formato**: HTML article.
- **URLs-chave**:
  - `/news/markets` · `/news/business` · `/opinion/heard-on-the-street`
  - RSS público (headlines only): `https://feeds.a.dj.com/rss/RSSMarketsMain.xml`
- **Strategy**:
  1. Fetch RSS público para descobrir headlines.
  2. User "flags" artigos interessantes (ou auto-filter por keyword/ticker).
  3. Fetch full article HTML com cookies → parse `<article>` body.
  4. Ollama extract → summary + tickers mentioned.
- **TOS**: explicitly prohibit scraping, BUT personal reading via automated fetch é cinza. **Baixo volume, uso pessoal**.
- **Priority**: MÉDIA (muito volume, sinal baixo per article).

### 🔴 **Finclass** (app.finclass.com) — **ROI baixo, deprioritize**

- **Conteúdo**: cursos vídeo + notas.
- **Login**: SPA + JWT em localStorage. Complicated.
- **Formato**: video URLs + some PDF/notes.
- **Strategy**: Playwright + network interception necessário (não vale o esforço para este site).
- **TOS**: normal restricted.
- **Priority**: **BAIXA** (education ≠ actionable intel). **Skeleton only**. Implementar se user quiser indexar curso específico.

## Execução

```bash
# 1. download + cache
ii subs fetch --source suno           # só Suno
ii subs fetch --source all            # todos

# 2. extrair insights (Ollama Qwen, 0 tokens)
ii subs extract --source all

# 3. consultar
ii subs query ITUB4                   # todas views sobre ITUB4
ii subs latest --source xp --days 7   # reports XP últimos 7d
```

## Cadência recomendada

- **Diário** via cron 23:30 (junto com `daily_update`): fetch headlines RSS → flag por keyword.
- **Semanal** manual: download batch PDFs Suno + XP → extract.
- **On-demand**: `ii subs extract --ticker X` quando estás a analisar ticker específico.

## Integration com research workflow

`research.py --intraday` passa a incluir secção "📰 Analyst views" no memo, com últimos 3 reports extraídos que mencionam o ticker.

`ii panorama X` (novo) agrega analyst views junto do verdict + peers + triggers.

## Red flags & warnings

- ❗ **Nunca commitar `data/subscriptions/cookies/`** — contém session tokens. `.gitignore` já exclui.
- ❗ Cookie-export = credential-export. Se partilhares laptop, cifra `data/subscriptions/`.
- ❗ Distribuir conteúdo scrapado = violação explícita TOS + copyright. **Uso pessoal only**.
- ❗ Taxas de request: respeitar `robots.txt`, limit 1 req/3s para não ser banido.
- ❗ Se site implementar Cloudflare challenge → upgradear adapter para Playwright (com headless browser autentico).

## Claude Web API — quando faz sentido

- `WebFetch` do Claude Code: OK para 1-off research ad-hoc ("lê-me este artigo único"). **Não** para cronjob.
- Anthropic "Computer Use" (browser control via Claude): $3-15/hora. **Não recomendo** para scraping regular — Playwright local faz o mesmo por zero recurring tokens.

## Future improvements

- Playwright mode automático fallback se requests falhar (Cloudflare).
- Structured JSON extraction via Ollama tool-calling (Qwen 2.5 suporta function calls).
- Integration com triggers: novo relatório Suno sobre holding → dispara alert + linkar ao memo.
- Cross-source synthesis: "Suno + XP + WSJ concordam em X?" — synthesis em Ollama.

## Related

- 🚨 [[Token_discipline]]
- [[Analysis_workflow]]
- `fetchers/subscriptions/` source code
