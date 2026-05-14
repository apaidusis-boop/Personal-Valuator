# RI URL Resolver Overhaul — Handoff (2026-05-11)

> Sessão de re-resolução completa dos sites de RI (Relações com Investidores).
> Disparada após o overnight 2026-05-11 ter exposto que só ~112/190 tickers
> tinham o site de RI efetivamente lido (41% do universo era ponto cego).
> **Para outra conversa pegar isto** — esp. se for trabalhar agents/skills:
> partes disto podem virar um perpetuum / skill (ver §6).

## 1. O problema que motivou

- Overnight 2026-05-11 produziu 134 dossiers mas **só ~112 tickers tiveram leitura RI fresca**; 22 tinham URL mas o scrape crashou (incl. holdings: `O`/Realty Income — a recomendação nº1!, `ACN`, `HD`, `XP`, `TSM`, `TSLA`, `TEN`); 54 nunca tiveram URL mapeado.
- Causa-raiz #1: **`companies.name` estava == ao ticker para 37 tickers BR** (`POMO4`→"POMO4" em vez de "Marcopolo"), por isso a heurística por nome do `ri_url_resolver.py` corria cega → ~25-30% dos BR mid-caps falhavam.
- Causa-raiz #2: verificação era só `HTTP 200` → páginas parqueadas, "404", e o `fiis.com.br/<ticker>/` genérico de "fundo não encontrado" passavam como ✅. Falsos positivos silenciosos.
- Insight do user: **o RI mapeia-se pelo nome da empresa, não pelo ticker** (`TEN` ≠ Tenaris; é Tsakos Energy Navigation, e mesmo aí o URL apontava para outra entidade do grupo Tsakos).

## 2. O que foi feito

| Fase | Estado | Detalhe |
|---|---|---|
| 1 | ✅ | `scripts/bibliotheca_autofix.py --apply` → 37 nomes BR corrigidos em `companies`; backfill + de-mojibake de 59 nomes em `config/ri_urls.yaml` ("Itaúsa", "SLC Agrícola", "Rede D'Or" agora bem gravados) |
| 2 | ✅ | `scripts/ri_url_resolver.py` reescrito (ver §3) |
| 2b | ✅ | Passo de limpeza: apertar verificação, corrigir KNOWN partidos, re-resolver ~54 suspeitos |
| **Resultado** | — | **184/190 URLs · 0 falhados · 6 ETFs skip** · 143 verificados, 41 a confirmar (vs ~112 legíveis antes) |
| 3 | ⏳ pendente | Re-mapear 4 URLs genuinamente partidos (404/415): `ERIE`, `MSEX`, `UVV`, `WIZC3` (têm KNOWN errado-ish; precisa fix manual ou remover KNOWN p/ cair em Tavily). Tomorrow's overnight vai produzir dossiers finos para estes 4 até serem corrigidos. |
| 4 | 🟡 **ARMADO para 2026-05-12 02:00** | Scheduled task `ii-overnight-ri-rescrape-20260512` (one-shot, WakeToRun) → `scripts\overnight_ri_rescrape.bat` → `overnight_orchestrator.py` (4 phases, `--deep --force-fresh`, ~4-6h). Output `obsidian_vault/Overnight_2026-05-12/`. Log `logs/overnight_ri_rescrape_2026-05-12.log`. **Não faz wire para `events`** — pilot_deep_dive produz dossiers mas não insere em `events`; gap continua aberto. Cancelar: `Unregister-ScheduledTask -TaskName ii-overnight-ri-rescrape-20260512 -Confirm:$false`. |

## 3. Mudanças no `scripts/ri_url_resolver.py`

- **Candidatos derivados do nome da empresa**, ordenados: slug-do-nome-completo → ticker → primeiro-nome-do-nome (por último — colide com domínios não relacionados, ex: "Archer"-Daniels → archer.com da Archer Aviation).
- **`verify_page(url, name, ticker)`** — uma URL só "ganha" se devolver HTML 200 **e** carregar sinal distintivo: slug completo presente OU token forte (≥5 chars, não palavra-genérica tipo "data"/"black"/"illinois"/"energy") OU ≥2 tokens do nome OU ticker presente + hostname derivado do ticker. Token único genérico **já não conta** → mata `ADM→archer.com`, `ADP→automatic.com`, `ITW→illinois.com`.
- **Marcadores de "página parqueada"** verificados só no `<title>` + primeiros 5KB (não "not found" anywhere nos 120KB → matava MSFT/SYY com falso negativo).
- **FII só para FIIs reais** — `is_fii()` usa lista de **exclusão** por sector (`_NON_FII_SECTORS`: Banks/Utilities/Materials/...), robusta a sectores mojibake. `ENGI11`/`ALUP11`/`KLBN11`/`TAEE11`/`BPAC11` deixam de ir para `fiis.com.br`.
- **Tavily fallback** (`--max-tavily N`, via `agents.autoresearch.search`, cache 7d + rate-limit 100/dia) — exige nome-token ou ticker no **hostname** do resultado → mata agregadores (alphaspread/quartr/statusinvest/fundsexplorer/investidor10/advfn/morningstar/marketbeat/...).
- **KNOWN** (111 entradas): curado, tudo verificado mas **nunca descartado** em mismatch — fica `verified: false` + nota "review". Fixes: `BBAS3→ri.bb.com.br` (era `bb.com.br/site/ri/` 404), `AOS→investor.aosmith.com` (era 404), `BN→bn.brookfield.com` (era `/news-and-events` "page not found"), `TEN→tenn.gr` + `tsakosenergynavigation.com` (era `tsakoshellenicgroup.com` — entidade errada). +30 Aristocratas adicionados (`MDT MKC PNR SWK TROW LEG ED BDX CL CLX APD KMB ABT TUPY3 UNIP6 AXIA7 HGLG11 KNRI11 ABCB4 WIZC3 AWR ...`).
- Output `config/ri_urls.yaml` agora tem campos `name`, `verified` (true/false/null), `last_resolved`. Schema/uso documentado no docstring do ficheiro.
- Flags novas: `--only-failed`, `--no-verify`, `--max-tavily N`. Merge-safe (não destrói entradas não tocadas).
- Log estruturado: `logs/ri_url_resolver.log`.

## 4. Os 41 `verified: false` (não estão errados — só não deu p/ confirmar via `requests`)

- **10 = bloqueio HTTP 403** (site real, bloqueia scraping HTTP — Playwright lê na boa): `CAT CVX ITUB4 POMO4 POMO3 TSLA TSM XP UNIP6 TR`
- **~27 = timeout/SSL** (Aristocratas com domínios IR padrão, quase de certeza certos): `ABBV ABT ABM AOS APD AXIA7 BKH CBSH CL CWT ED EGIE3 ES FDS FRT GPC GRC KMB LEG MKC PNR SCL SWK TROW TUPY3 WST`
- **4 = genuinamente partidos (404/415) → Fase 3 re-mapear**:
  - `ERIE` Erie Indemnity — `erie.com/about-erie/investor-relations` → 404 (domínio `erie.com` certo, path errado)
  - `MSEX` Middlesex Water — `middlesexwater.com/category/investors/` → 415
  - `UVV` Universal Corporation — `universalcorp.com/investor-relations/` → 404
  - `WIZC3` Wiz Co — `ri.wizsolucoes.com.br` redireciona p/ `ri.wiz.co`, conteúdo fino

(Lista completa com URLs: ver `config/ri_urls.yaml`, campo `verified: false`.)

## 5. Skipped (6) — ETF/residual, sem RI corporativo

`SPY` `BOVA11` `LFTB11` `IVVB11` `GREK` `BTLG12`(residual/old-class)

## 6. Ideias para virar agent/skill (para a conversa de agents)

- **Skill reutilizável: "verify-company-page"** — dado (url, nome, ticker), confirma que a página é mesmo da empresa (slug/tokens/hostname). Útil para qualquer scraper, não só RI. Já implementado como `verify_page()` em `ri_url_resolver.py`; extrair para `library/_verify.py` ou skill.
- **Perpetuum `ri_url_freshness`** (extende o `ri_freshness` que já existe, Phase Y) — semanal: re-resolver tickers com `verified: false` ou `last_resolved` > 30d; tentar Tavily p/ os ainda failed; flagar mudanças de domínio. T1 (audit-only) → T2 se action_hint claro.
- **Step "playwright-verify-fallback"** — quando `requests` dá 403/timeout num KNOWN, escalar para `fetchers/portal_playwright.py` e re-verificar com browser real (resolve os 41 `verified: false` automaticamente). Pode ser um modo do `pilot_deep_dive.py` ou do resolver.
- **Wire para `events`** — Fase 4 deve persistir filings novos descobertos na tabela `events` (hoje ficam só em markdown no vault → perpetuums não os vêem). Está no plano da Fase 4.
- Relação com a "Future session: Investment houses scraping" (memory `future_session_investment_houses_scraping.md`): este resolver é o precursor — o multi-house aggregator reusa o mesmo padrão (resolver URL → verificar → Playwright → markitdown → Qwen).

## 7. Comandos

```bash
# Re-resolver tudo (verificado, com Tavily fallback)
python scripts/ri_url_resolver.py --max-tavily 30
# Só os que falharam
python scripts/ri_url_resolver.py --only-failed --max-tavily 20
# Tickers específicos
python scripts/ri_url_resolver.py --tickers ERIE MSEX UVV WIZC3 --max-tavily 8
# Sem verificação (rápido, só HTTP 200)
python scripts/ri_url_resolver.py --no-verify
# Re-scrape de um ticker (Playwright)
.venv\Scripts\python.exe scripts/pilot_deep_dive.py --tickers O --force-fresh --deep
```

## 8. Ficheiros tocados

- `scripts/ri_url_resolver.py` — reescrito (não commitado ainda)
- `config/ri_urls.yaml` — regravado (190 entradas, schema novo)
- `data/br_investments.db` — `companies.name` corrigido p/ 37 tickers (via bibliotheca_autofix)
- `logs/ri_url_resolver.log`, `logs/ri_resolve_full_20260511_1103.out`, `logs/ri_resolve_cleanup_*.out` — logs do run
- Nada commitado — o user decide quando.
