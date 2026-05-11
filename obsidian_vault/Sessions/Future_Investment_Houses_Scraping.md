---
date: 2026-05-10
status: deferred — note for future session
trigger: user ask after Phase MCP-5 — "como vais buscar recomendações em Motley Fool, WSJ, etc."
related: [[2026-05-10_5MCPs_Sweep]]
---

# Future session — Investment Houses Recommendation Scraping

> Goal: turn the project into a **multi-house recommendation aggregator**.
> For every ticker we hold or watch, we want to know what the public-facing
> recommendation pages of major investment houses / financial media are
> saying — collected, structured, deduped, dated. This lets us compare our
> internal verdict (Synthetic IC, Variant Perception, Moat, deepdive) against
> the broader analyst landscape automatically.

## Two tiers, two channels

### Tier A — Already authed (cookies via Cookie-Editor)
Already wired in `fetchers/subscriptions/` with `PlaywrightSession`. Just needs maintenance + the Suno-PDF-is-image fix from the MCP-5 session.

| House | Status | Auth | Output |
|---|---|---|---|
| Motley Fool (premium) | adapter exists (`fool.py`) | cookies | PDFs/HTML scraped, not always parsed cleanly |
| WSJ | adapter exists (`wsj.py`) | cookies | similar |
| Suno | adapter exists, **PDF extract empty** (image-based PDFs — known gap) | cookies | needs HTML route or OCR |
| XP | adapter exists | cookies | works, text-based PDFs |
| Finclass | adapter exists | cookies | works |

### Tier B — Free public pages (no auth) — **what's NEW**
This is the gap we want to close. Build `fetchers/research_houses.py` that, given a ticker, hits the public recommendation pages and returns a structured list of `Recommendation` records.

Targets (public, non-authed, JS-rendered → use `fetchers/portal_playwright.py`):

| House / Source | URL pattern | What we get |
|---|---|---|
| Motley Fool free articles | `https://www.fool.com/quote/<exch>/<ticker>/` | recent free coverage, sometimes ratings |
| Motley Fool stock recommendations index | `https://www.fool.com/investing-news/` (filter by ticker) | latest news/picks |
| MarketWatch analyst ratings | `https://www.marketwatch.com/investing/stock/<ticker>/analystestimates` | consensus, # of analysts |
| Yahoo Finance analyst | `https://finance.yahoo.com/quote/<ticker>/analysis` | EPS estimates, recos breakdown |
| TipRanks free | `https://www.tipranks.com/stocks/<ticker>/forecast` | 12mo target, smart-score |
| Zacks free | `https://www.zacks.com/stock/quote/<ticker>` | Zacks rank 1-5, ESP |
| Finviz | `https://finviz.com/quote.ashx?t=<ticker>` | analyst consensus, target, ratings table |
| CNBC quote page | `https://www.cnbc.com/quotes/<ticker>` | news + analyst snapshot |
| Seeking Alpha free | `https://seekingalpha.com/symbol/<ticker>` | quant rating, factor grades |
| Bloomberg free quote | `https://www.bloomberg.com/quote/<ticker>:US` | summary + recent stories |
| WSJ free quote | `https://www.wsj.com/market-data/quotes/<ticker>` | analyst ratings table (free) |
| Reuters free | `https://www.reuters.com/markets/companies/<ticker>` | recent stories |
| Investor.com analyst | `https://www.investors.com/research/stock-of-the-day/<ticker>/` | IBD ratings (some free) |
| StockAnalysis.com | `https://stockanalysis.com/stocks/<ticker>/forecast/` | analyst forecast detail |

For each: `python fetchers/portal_playwright.py <url> --md` already lands a clean Markdown rendering → Qwen 14B extracts structured records.

## Architecture I'd build

### Schema (new table per market DB)
```sql
CREATE TABLE house_recommendations (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker      TEXT    NOT NULL,
  house       TEXT    NOT NULL,        -- 'motley_fool' / 'wsj' / 'tipranks' / ...
  rec_date    TEXT    NOT NULL,        -- ISO date when the rec was published
  fetched_at  TEXT    NOT NULL,        -- ISO when we scraped it
  action      TEXT,                    -- BUY / HOLD / SELL / OVERWEIGHT / etc
  rating      TEXT,                    -- house-native rating string (e.g. "Zacks #2")
  price_target REAL,
  currency    TEXT,
  analyst     TEXT,                    -- if named
  summary     TEXT,                    -- 1-3 sentence digest from Qwen
  url         TEXT    UNIQUE,          -- canonical page url (UNIQUE prevents dup)
  raw_md_path TEXT                     -- pointer to data/portal_cache/<sha>.md
);
CREATE INDEX idx_hr_ticker_date ON house_recommendations (ticker, rec_date DESC);
CREATE INDEX idx_hr_house_date  ON house_recommendations (house, rec_date DESC);
```

### Config: `config/research_houses.yaml`
```yaml
houses:
  motley_fool:
    type: public
    url_template: "https://www.fool.com/quote/{exchange}/{ticker}/"
    market_supports: [us]
    extract_prompt: "fool"          # Qwen prompt template name
    rate_limit_sec: 10
    refresh_hours: 24

  tipranks:
    type: public
    url_template: "https://www.tipranks.com/stocks/{ticker}/forecast"
    market_supports: [us]
    extract_prompt: "tipranks"
    rate_limit_sec: 5
    refresh_hours: 12

  # ... per source
  fool_premium:
    type: authed
    adapter: fetchers.subscriptions.fool.FoolAdapter
    rate_limit_sec: 30
```

### Fetcher: `fetchers/research_houses.py`
1. Load `config/research_houses.yaml`
2. For each (ticker, house) in cartesian × universe holdings:
   - If house is `public`: render via `portal_playwright.fetch(url, md=True)` — caching applies (24h)
   - If house is `authed`: use existing subscriptions `PlaywrightSession`
3. Extract structured Recommendation via Qwen 14B prompt template
4. UPSERT into `house_recommendations` keyed on `url`
5. Idempotent: skip if cached MD is fresh & DB row exists

### Extraction: `library/houses/extract.py`
Per-house Qwen prompt templates that read the MD and return JSON matching the schema. Examples:

```python
SYSTEM_FOOL = """You read a Motley Fool article in Markdown and extract all
ticker recommendations. Return JSON: {recommendations: [{ticker, action,
analyst, price_target_usd, summary, rec_date}]}. action ∈ {BUY, HOLD, SELL,
WATCH, NEUTRAL}. If no clear rec, action=null."""
```

### CLI surface: `ii houses <TICKER>`
Wraps `scripts/houses_cli.py`:
- `ii houses ACN` — show latest reco from each house, colored by stance
- `ii houses ACN --history` — full timeline
- `ii houses --fetch all` — refresh all holdings × all sources (cron-friendly)
- `ii houses --diff` — what changed since yesterday (downgrade/upgrade alerts)

### Mission Control surface
New `/research/<TICKER>` panel showing:
- Bar chart: # of houses BUY / HOLD / SELL
- Median price target with our vs consensus delta
- List of recent recos with stance + 1-line summary
- Click → opens raw MD scraped page

### Cron wire-up
- Daily 06:30 cron: `ii houses --fetch all` for holdings (90 cells/day worst case = ~15min Playwright budget)
- Weekly Sunday: `ii houses --fetch all --include-watchlist` (heavier)

### Anti-bot defenses we already have
`PlaywrightSession` already sets:
- Persistent profile (mimics returning user)
- Real Chromium (`--disable-blink-features=AutomationControlled`)
- pt-BR locale + São Paulo TZ
- Realistic UA + viewport
- networkidle wait + selector wait

For Tier B public scrape, my new `portal_playwright.fetch()` inherits these but uses fresh context per call. Could share the persistent-profile pattern to look less bot-y across sites.

### Robots / ToS hygiene
- 5-30s rate-limit between requests per house
- Cache 24h to avoid hammering
- Honor robots.txt (add explicit check before first scrape per host)
- User-Agent identifies as a researcher (not impersonating a browser if site bans bots)
- **No re-distribution**: we read into our own SQLite + private vault. If we ever surface this in a public app, that's a different ToS conversation.

## Effort estimate (rough)

- Skeleton + schema + 1 source (Finviz, easiest) ............... 2-3h
- 5 free sources × prompt templates ............................. 6-8h
- CLI + Mission Control panel ................................... 4-6h
- Cron wire + smoke tests ....................................... 2h
- Suno PDF→HTML fix (separate, from MCP-5 follow-up) ............ 2-3h
- **Total realistic first delivery** ............................ ~3-4 sessions of ~5h

## Why this matters

- Variant Perception (`agents/variant_perception.py`) currently computes "we vs consensus" using a single feed. Multi-house gives **dispersion** — when houses disagree, that's a more interesting signal than the average.
- Synthetic IC (`agents/synthetic_ic.py`) gets richer evidence ledger to argue with — Buffett/Druck/Taleb/Klarman/Dalio personas can quote real recent positions of real houses.
- Decision journal can track "we said BUY on date X when houses were Y%" → calibration over time.
- Earnings prep gets a "what house just changed" pre-call sweep automatically.

## Open questions for the live session

1. Which houses are highest priority? (My guess: Motley Fool free + TipRanks + Finviz + WSJ free + Yahoo, in that order — easy → harder.)
2. Should we add **paid Tier A** sources to the same table or keep them in `subscriptions_*` schema as-is and only union at query time? (Probably the latter — preserves provenance.)
3. Mission Control panel mockup — pixel layout to match v5 JPM theme. (Helena pass before code.)
4. ToS — if any house has clear "no scraping" language, swap to RSS or skip.

## Tooling already in place that this builds on

- `fetchers/portal_playwright.py` (Phase MCP-5) — public site renderer
- `fetchers/subscriptions/_session.py::PlaywrightSession` — authed flow
- `library/_md_extract.py` (Phase MCP-5) — universal HTML→MD
- `agents/_llm.ollama_call` — Qwen 14B in-house extraction
- `agents/autoresearch` (Tavily) — could find URLs we don't know about
- `data/portal_cache/` — already wired for caching renders
