# Bugs & Limitations descobertos no overnight 2026-05-11

> Inventory honesto de problemas encontrados durante a sessão.
> Para corrigir amanhã quando o user voltar.

## 🐛 Bugs identificados

### B1. FII heuristic gera falsos positivos para units não-FII
**Onde**: `scripts/seed_br_watchlist.py::main()` e `scripts/ri_url_resolver.py::resolve_one()`
**Sintoma**: Tickers terminados em "11" que NÃO são FIIs (ex: ENGI11 = Energisa units, ALUP11 = Alupar units, KLBN11 = Klabin units, TAEE11 = Taesa units) recebem URL `https://www.fiis.com.br/<ticker>/`. Esse URL retorna 200 mas o conteúdo é geralmente irrelevante (página genérica de "ticker não encontrado" ou de outro fundo).
**Resultado**: Dossier criado com "Scrape: ❌ FALHOU" ou conteúdo inútil.
**Fix sugerido**: Validar se ticker é FII pela `companies.sector` (== 'FII' / 'REIT-Like' / similar) antes de aplicar fii_heuristic. Se não for FII, fallback para outras heurísticas.
**Severidade**: Médio (~5-10 tickers afectados, mas dossiers ainda úteis pelo DB context).

### B2. Novelty detection over-counts em providers com prefixos longos
**Onde**: `scripts/pilot_deep_dive.py::detect_novel_filings()`
**Sintoma**: BBDC4 detecta 27 filings "novos" mas ~12 são duplicados de DB events que diferem só em prefixo ("Outros Comunicados Não Considerados Fatos Relevantes | Fechamento" vs "Comunicado ao Mercado - Fechamento").
**Fix sugerido**: Tokenization com stopwords expandida + lower threshold para fuzzy match (≥1 shared content token em vez de ≥2 quando datas iguais).
**Severidade**: Baixo (todas as filings reais são apanhadas — over-detection é só ruído visual).

### B3. AAPL dossier reporta ROE=141% (suspicious)
**Onde**: `data/us_investments.db` — fundamentals table
**Sintoma**: Apple negative equity (recompra agressiva) → ROE = NetIncome / negative equity = artificial high. Pipeline mostra "1.4147" no dossier sem flag.
**Fix sugerido**: Em compose_dossier, flagar ROE > 100% como suspicious + checar BVPS sign.
**Severidade**: Baixo (dado correctamente reportado, só falta context).

### B4. JPM tem 312 "presentations" — heuristic muito permissive
**Onde**: `scripts/pilot_deep_dive.py::parse_ri_content()` parsing presentations
**Sintoma**: Em /ir/quarterly-earnings, cada PDF link com keyword "earnings/release/report" classificado como presentation. JPM mantém 5+ anos de filings nessa página.
**Fix sugerido**: Filtrar por data — só presentations dos últimos 12 meses por default.
**Severidade**: Baixo (cap display ao top 12 já mitigou. No master report: relevância ≠ número).

### B5. URLs com SSL errors em scripts probe
**Onde**: `scripts/ri_url_resolver.py::probe_url()` — alguns sites retornam SSL errors (ALUP11, AURA33).
**Sintoma**: Falsos negativos — URL existe mas SSL handshake falha.
**Fix sugerido**: Tentar `verify=False` como fallback (com warning) para sites com cert mismatch.
**Severidade**: Baixo (afecta ~3-5 tickers, manualmente mapável).

### B6. Subprocess timing reportado como 0.07s quando cache hit
**Onde**: `scripts/pilot_deep_dive.py::scrape_ri()`
**Sintoma**: Quando portal_playwright cache hit, retorna instantaneamente. Subprocess elapsed mostra 0.07s. Mas isto NÃO é o tempo real de network/render que tomaria sem cache.
**Fix sugerido**: Já fix in subprocess_elapsed_s + parsed['elapsed_s']. Verificar se compose_dossier usa o certo.
**Severidade**: Baixo (cosmético).

### B7. Falsos TODO no code_health audit
**Onde**: `scripts/overnight_code_health.py::find_todos()`
**Sintoma**: Regex `# TODO|FIXME|...` apanha strings em código onde "TODO" aparece em contexto não-comentário (ex: `# TODOs neste módulo...`).
**Fix sugerido**: Match só `#\s*TODO\b` no início de linha (ignorando docstrings). Ou pular linhas dentro de strings tripla.
**Severidade**: Baixo (só 3-4 falsos positivos, fácil de revisar).

## 📋 Limitações conhecidas (não bugs, apenas escopo)

### L1. ETFs não cobertos
ETFs (LFTB11, IVVB11, GREK, ARKK, etc) não têm RI corporativo. Skip explícito.
**Para o user**: usar dados do gestor (BlackRock, Vanguard, etc) directamente se quiser deep-dive.

### L2. ~25-30% dos BR mid-caps falharam URL discovery
Tickers como ABCB4, ALOS3, BRKM5, ENGI11, EZTC3, GMAT3, ISAE4, PGMN3, PLPL3, PNVL3 não match heurísticas (`ri.<base>.com.br` pattern).
**Workaround**: 8 já validados manualmente em `scripts/patch_failed_urls.py::MANUAL_PATCH`. Correr o patch script após discovery completar.
**Para o user**: para ticker específico, mapear URL e adicionar a `KNOWN` em `scripts/ri_url_resolver.py`.

### L3. Cobertura US watchlist (Kings/Aristocrats) baixa
Só 7/87 Kings/Aristocrats em KNOWN dict. Discovery vai apanhar mais via heurística (~30-40% taxa de sucesso esperada).
**Para o user**: Quando overnight terminar, ver lista de failed em `config/ri_urls.yaml` (`status: failed`) e mapear críticos.

### L4. Sites com anti-bot bloqueiam Playwright
TipRanks, Morningstar, Seeking Alpha, MarketBeat tipicamente bloqueiam. Não aplicável a este overnight (só RI directo) mas relevante para "Investment Houses scraping" futuro.

### L5. Audio/video extraction não automatizado neste run
Nos dossiers vejo links para conference calls, podcasts (Itaúsa Cast, JPM 1Q26 Conference Call). Markitdown PODE extraí-los, mas não corremos extracção (cada audio = ~5-15min processing time). Ficam disponíveis para extracção manual.

### L6. Auto-flagged signals usam keyword matching, não LLM
"🚨 Mudança executiva" detection é regex puro (`alteração na diretoria`). Falha em variantes ("renúncia do CEO", "novo CFO anunciado"). Para precisão maior, precisaria LLM pass.

## 🎯 Acções recomendadas (priorizado)

| # | Acção | Esforço | Impacto |
|---|---|---|---|
| 1 | Aplicar `patch_failed_urls.py` para 8 BR mid-caps confirmados | 5min | Alto — adiciona ~8 dossiers |
| 2 | Re-correr Phase D BR com novos URLs | 5min | Alto — mais coverage BR |
| 3 | Fix B1 (FII heuristic só para FIIs reais) | 30min | Médio — limpa falsos positivos |
| 4 | Map mais 20-30 BR mid-caps em KNOWN dict | 1h | Médio — coverage longa |
| 5 | Fix B2 (novelty fuzzy threshold) | 30min | Baixo — só afecta ruído visual |
| 6 | Schedule daily overnight (cron) | 30min | Alto — production value |
| 7 | Wire para `events` table | 1-2h | Alto — perpetuums beneficiam |

---
_Inventory criado durante overnight run, à medida que bugs eram identificados._
_Last updated: $(date)_
