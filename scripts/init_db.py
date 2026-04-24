"""Cria/migra as duas bases SQLite (BR e US) com schema idêntico.

Idempotente: pode correr quantas vezes for preciso. Não destrói dados.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

SCHEMA = """
CREATE TABLE IF NOT EXISTS companies (
    ticker      TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    sector      TEXT,
    is_holding  INTEGER NOT NULL DEFAULT 0,
    currency    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prices (
    ticker  TEXT NOT NULL,
    date    TEXT NOT NULL,
    close   REAL NOT NULL,
    volume  INTEGER,
    PRIMARY KEY (ticker, date),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);
CREATE INDEX IF NOT EXISTS idx_prices_date ON prices(date);

CREATE TABLE IF NOT EXISTS fundamentals (
    ticker                 TEXT NOT NULL,
    period_end             TEXT NOT NULL,
    eps                    REAL,
    bvps                   REAL,
    roe                    REAL,
    pe                     REAL,
    pb                     REAL,
    dy                     REAL,
    net_debt_ebitda        REAL,
    dividend_streak_years  INTEGER,
    is_aristocrat          INTEGER,
    PRIMARY KEY (ticker, period_end),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS fii_fundamentals (
    ticker                      TEXT NOT NULL,
    period_end                  TEXT NOT NULL,
    price                       REAL,
    vpa                          REAL,
    pvp                          REAL,
    dy_12m                       REAL,
    last_monthly_rendimento      REAL,
    avg_monthly_rendimento_24m   REAL,
    physical_vacancy             REAL,
    financial_vacancy            REAL,
    adtv_daily                   REAL,
    distribution_streak_months   INTEGER,
    segment_anbima               TEXT,
    management_type              TEXT,
    source                       TEXT NOT NULL,
    fetched_at                   TEXT NOT NULL,
    PRIMARY KEY (ticker, period_end),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS scores (
    ticker         TEXT NOT NULL,
    run_date       TEXT NOT NULL,
    score          REAL NOT NULL,
    passes_screen  INTEGER NOT NULL,
    details_json   TEXT,
    PRIMARY KEY (ticker, run_date),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS portfolio_positions (
    ticker       TEXT NOT NULL,
    weight       REAL NOT NULL,
    entry_date   TEXT NOT NULL,
    entry_price  REAL NOT NULL,
    active       INTEGER NOT NULL DEFAULT 1,
    quantity     REAL,
    notes        TEXT,
    exit_date    TEXT,
    exit_price   REAL,
    PRIMARY KEY (ticker, entry_date),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS dividends_annual (
    ticker  TEXT NOT NULL,
    year    INTEGER NOT NULL,
    amount  REAL NOT NULL,
    PRIMARY KEY (ticker, year),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS valuations (
    ticker       TEXT NOT NULL,
    run_date     TEXT NOT NULL,
    model        TEXT NOT NULL,
    fair_value   REAL,
    entry_price  REAL,
    details_json TEXT,
    PRIMARY KEY (ticker, run_date, model),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS income_statements (
    ticker       TEXT NOT NULL,
    period_end   TEXT NOT NULL,
    period_type  TEXT NOT NULL,
    revenue      REAL,
    gross_profit REAL,
    ebit         REAL,
    ebitda       REAL,
    net_income   REAL,
    source       TEXT NOT NULL,
    fetched_at   TEXT NOT NULL,
    PRIMARY KEY (ticker, period_end, period_type),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS balance_sheets (
    ticker              TEXT NOT NULL,
    period_end          TEXT NOT NULL,
    period_type         TEXT NOT NULL,
    total_assets        REAL,
    current_assets      REAL,
    cash_equivalents    REAL,
    total_liabilities   REAL,
    current_liabilities REAL,
    long_term_debt      REAL,
    total_equity        REAL,
    source              TEXT NOT NULL,
    fetched_at          TEXT NOT NULL,
    PRIMARY KEY (ticker, period_end, period_type),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

CREATE TABLE IF NOT EXISTS cash_flow_statements (
    ticker              TEXT NOT NULL,
    period_end          TEXT NOT NULL,
    period_type         TEXT NOT NULL,
    operating_cash_flow REAL,
    investing_cash_flow REAL,
    financing_cash_flow REAL,
    capex               REAL,
    free_cash_flow      REAL,
    source              TEXT NOT NULL,
    fetched_at          TEXT NOT NULL,
    PRIMARY KEY (ticker, period_end, period_type),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

-- séries temporais universais: macro, benchmarks, FX.
-- Um único armazém para SELIC, CDI, IPCA, IBOV, USD/BRL, IFIX, etc.
CREATE TABLE IF NOT EXISTS series (
    series_id  TEXT NOT NULL,
    date       TEXT NOT NULL,
    value      REAL NOT NULL,
    source     TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (series_id, date)
);
CREATE INDEX IF NOT EXISTS idx_series_date ON series(date);

CREATE TABLE IF NOT EXISTS series_meta (
    series_id        TEXT PRIMARY KEY,
    description      TEXT,
    unit             TEXT,
    frequency        TEXT,
    source_primary   TEXT,
    source_fallback  TEXT
);

-- eventos de dividendos (inclui JCP) por acção/FII.
-- kind: 'dividend' | 'jcp' | 'rendimento'. Todos contam para total return.
CREATE TABLE IF NOT EXISTS dividends (
    ticker     TEXT NOT NULL,
    ex_date    TEXT NOT NULL,
    pay_date   TEXT,
    amount     REAL NOT NULL,
    currency   TEXT NOT NULL,
    kind       TEXT NOT NULL DEFAULT 'dividend',
    source     TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (ticker, ex_date, kind),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);
CREATE INDEX IF NOT EXISTS idx_dividends_ticker_date ON dividends(ticker, ex_date);

CREATE TABLE IF NOT EXISTS events (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker              TEXT NOT NULL,
    event_date          TEXT NOT NULL,
    source              TEXT NOT NULL,
    kind                TEXT NOT NULL,
    url                 TEXT,
    summary             TEXT,
    full_text           TEXT,
    pdf_path            TEXT,
    classification_json TEXT,
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);
CREATE INDEX IF NOT EXISTS idx_events_ticker_date ON events(ticker, event_date);

-- Caixa livre: aportes pendentes, proceeds de vendas, dividendos em cash
-- que ainda não foram reinvestidos. Permite tracking do "dry powder".
CREATE TABLE IF NOT EXISTS cash_balance (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT NOT NULL,          -- quando entrou no caixa
    amount      REAL NOT NULL,          -- valor em moeda local (positivo = entrada)
    currency    TEXT NOT NULL DEFAULT 'BRL',
    source      TEXT NOT NULL,          -- 'sale_proceeds' | 'dividend' | 'aporte' | 'rebalance'
    related_ticker TEXT,                -- ticker que originou (se aplicável)
    notes       TEXT
);
CREATE INDEX IF NOT EXISTS idx_cash_date ON cash_balance(date);

-- Posições de renda fixa: Tesouro Direto, debêntures, CRAs, LCAs, CRIs.
-- Modelagem mínima orientada a DRIP/consolidado: o que mete juros/cupons
-- é separado das equities para não contaminar scoring ou dividendo history.
CREATE TABLE IF NOT EXISTS fixed_income_positions (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT NOT NULL,
    kind              TEXT NOT NULL,         -- tesouro|debenture|cra|lca|cri
    indexador         TEXT,                   -- IPCA|CDI|PREFIXADO|SELIC
    spread_taxa       REAL,                   -- 0.0709 p/ IPCA+7.09%
    cdi_pct           REAL,                   -- 0.87 p/ 87% CDI
    entry_date        TEXT,
    maturity_date     TEXT,
    quantity          REAL,
    entry_unit_price  REAL,
    valor_aplicado    REAL,
    valor_atual       REAL NOT NULL,
    currency          TEXT NOT NULL DEFAULT 'BRL',
    source            TEXT,                   -- XP|manual
    fetched_at        TEXT NOT NULL,
    notes             TEXT
);
CREATE INDEX IF NOT EXISTS idx_fi_maturity ON fixed_income_positions(maturity_date);

-- Decision journal: cada vez que um trigger dispara, abre-se uma row aqui.
-- O user resolve explicitamente ("bought 10 @ X", "ignored: wait Q earnings").
-- Em 6 meses temos o track record das nossas decisões de compra/venda/trim.
--   kind            : mesmo vocabulário do triggers.yaml
--                     (price_drop_from_high | dy_above_pct | dy_percentile_vs_own_history | ...)
--   trigger_id      : slug opcional (stable id) da entry em triggers.yaml
--                     para dedupe por (ticker, trigger_id, status=open)
--   action_hint     : BUY | SELL | TRIM | ADD | REVIEW  — sugestão, não execução
--   trigger_snapshot_json : snapshot do que estava true no momento do fire
--                           (price, dy, reference, threshold, etc.)
--   status          : open | resolved | ignored
CREATE TABLE IF NOT EXISTS watchlist_actions (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker                TEXT NOT NULL,
    market                TEXT NOT NULL,               -- 'br' | 'us'
    kind                  TEXT NOT NULL,
    trigger_id            TEXT,
    action_hint           TEXT,
    trigger_snapshot_json TEXT,
    status                TEXT NOT NULL DEFAULT 'open',
    opened_at             TEXT NOT NULL,               -- ISO 8601 UTC
    resolved_at           TEXT,
    notes                 TEXT,
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);
CREATE INDEX IF NOT EXISTS idx_wa_ticker_status ON watchlist_actions(ticker, status);
CREATE INDEX IF NOT EXISTS idx_wa_opened_at    ON watchlist_actions(opened_at);
-- Idempotência por dia: não reabrir 2 vezes o mesmo trigger aberto para o mesmo ticker no mesmo dia.
CREATE UNIQUE INDEX IF NOT EXISTS ux_wa_open_daily
    ON watchlist_actions(ticker, kind, trigger_id, substr(opened_at,1,10))
    WHERE status='open';

-- Fundamentals profundos (Phase I): balance sheet + income + cashflow anuais.
-- Necessário para Altman Z-Score (5 rácios) e Piotroski F-Score (9 critérios
-- comparando 2 anos consecutivos). Fetched on-demand por research.py ou em
-- batch. Fonte: yfinance .balance_sheet / .financials / .cashflow.
CREATE TABLE IF NOT EXISTS deep_fundamentals (
    ticker                TEXT NOT NULL,
    period_end            TEXT NOT NULL,     -- ISO date (fim do ano fiscal)
    period_type           TEXT NOT NULL,     -- 'annual' | 'quarterly'
    -- balance sheet
    total_assets          REAL,
    current_assets        REAL,
    current_liabilities   REAL,
    total_liabilities     REAL,
    long_term_debt        REAL,
    total_debt            REAL,
    stockholders_equity   REAL,
    retained_earnings     REAL,
    working_capital       REAL,
    shares_outstanding    REAL,
    -- income statement
    total_revenue         REAL,
    gross_profit          REAL,
    ebit                  REAL,
    net_income            REAL,
    diluted_avg_shares    REAL,
    -- cash flow
    operating_cashflow    REAL,
    capital_expenditure   REAL,
    free_cash_flow        REAL,
    -- meta
    market_cap_at_fetch   REAL,              -- só preenchido na row mais recente
    fetched_at            TEXT NOT NULL,
    source                TEXT NOT NULL DEFAULT 'yfinance',
    PRIMARY KEY (ticker, period_end, period_type),
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);
CREATE INDEX IF NOT EXISTS idx_deep_fund_ticker_period
    ON deep_fundamentals(ticker, period_end DESC);

-- YouTube ingestion (Phase Q): metadata + transcript cache + structured facts.
-- Áudio NÃO é persistido. Transcript É — permite re-correr extractor/validator
-- sem re-descarregar/re-transcrever (ganho ~30s GPU/vídeo por iteração).
-- Ver scripts/yt_ingest.py, scripts/yt_reextract.py.
CREATE TABLE IF NOT EXISTS videos (
    video_id              TEXT PRIMARY KEY,  -- YouTube video id (11 chars)
    url                   TEXT NOT NULL,
    title                 TEXT,
    channel               TEXT,
    channel_id            TEXT,
    published_at          TEXT,              -- ISO 8601
    duration_sec          INTEGER,
    lang                  TEXT,              -- detected by Whisper
    processed_at          TEXT NOT NULL,     -- ISO 8601 UTC
    status                TEXT NOT NULL,     -- pending|completed|skipped_no_relevance|error
    error_msg             TEXT,
    tickers_seen          TEXT,              -- JSON array of matched tickers
    transcript_text       TEXT,              -- full transcript (Whisper)
    transcript_chunks_json TEXT              -- JSON [[text, ts_start, ts_end], ...]
);
CREATE INDEX IF NOT EXISTS idx_videos_processed_at ON videos(processed_at);
CREATE INDEX IF NOT EXISTS idx_videos_status       ON videos(status);

-- Factos extraídos ligados a um ticker do universo.
-- kind ∈ guidance|capex|dividend|balance_sheet|thesis_bull|thesis_bear|
--        catalyst|risk|operational|management|valuation
CREATE TABLE IF NOT EXISTS video_insights (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id        TEXT NOT NULL,
    ticker          TEXT NOT NULL,
    kind            TEXT NOT NULL,
    claim           TEXT NOT NULL,
    claim_norm      TEXT NOT NULL,         -- lowercased, stripped, for dedup
    evidence_quote  TEXT NOT NULL,         -- verbatim transcript substring ≤300 chars
    ts_seconds      INTEGER,               -- timestamp dentro do vídeo
    confidence      REAL NOT NULL,         -- 0-1
    created_at      TEXT NOT NULL,
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    FOREIGN KEY (ticker)   REFERENCES companies(ticker)
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_insights_dedup
    ON video_insights(video_id, ticker, kind, claim_norm);
CREATE INDEX IF NOT EXISTS idx_insights_ticker_created
    ON video_insights(ticker, created_at DESC);

-- Factos macro/sector sem ticker (theme ∈ selic_cycle|fed_path|usdbrl|
-- pulp_cycle|real_estate_cycle|oil_cycle|semis_cycle|...)
CREATE TABLE IF NOT EXISTS video_themes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id        TEXT NOT NULL,
    theme           TEXT NOT NULL,
    stance          TEXT,                  -- bullish|bearish|neutral
    summary         TEXT NOT NULL,
    summary_norm    TEXT NOT NULL,         -- for dedup
    evidence_quote  TEXT NOT NULL,
    ts_seconds      INTEGER,
    confidence      REAL NOT NULL,
    created_at      TEXT NOT NULL,
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_themes_dedup
    ON video_themes(video_id, theme, summary_norm);
CREATE INDEX IF NOT EXISTS idx_themes_theme_created
    ON video_themes(theme, created_at DESC);

-- Analyst reports ingested from paid subscriptions (Suno, XP, WSJ, Finclass, etc).
-- Each row = one document (article or PDF). Insights extracted by Ollama are
-- stored in analyst_insights (linked by report_id). Cookies stored externally
-- in data/subscriptions/cookies/ (gitignored).
CREATE TABLE IF NOT EXISTS analyst_reports (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source          TEXT NOT NULL,                -- suno|xp|wsj|finclass|other
    source_id       TEXT NOT NULL,                -- site-specific ID (slug, url hash)
    url             TEXT,
    title           TEXT NOT NULL,
    author          TEXT,
    published_at    TEXT NOT NULL,                -- ISO date
    fetched_at      TEXT NOT NULL,
    content_type    TEXT NOT NULL,                -- html|pdf|rss_item
    local_path      TEXT,                         -- file path if downloaded (PDF/HTML snapshot)
    raw_text        TEXT,                         -- extracted plain text (limited size)
    language        TEXT DEFAULT 'pt',
    tags_json       TEXT,                         -- ["br-equity", "sector:banks", ...]
    summary         TEXT,                         -- Ollama 2-3 sentence summary
    extracted_at    TEXT,                         -- when Ollama processed (null = pending)
    extract_status  TEXT DEFAULT 'pending'        -- pending|done|failed|skipped
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_reports_source_sid
    ON analyst_reports(source, source_id);
CREATE INDEX IF NOT EXISTS idx_reports_pub ON analyst_reports(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_reports_source_pub ON analyst_reports(source, published_at DESC);

-- Structured insights extracted from analyst_reports.
-- kind taxonomy aligns with video_insights for unified queries:
--   thesis|catalyst|risk|numerical|rating|price_target|sector_view
CREATE TABLE IF NOT EXISTS analyst_insights (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id       INTEGER NOT NULL,
    ticker          TEXT,                         -- null se view sectorial/macro
    kind            TEXT NOT NULL,
    claim           TEXT NOT NULL,
    stance          TEXT,                         -- bull|bear|neutral (quando aplicável)
    price_target    REAL,                         -- se rating/PT
    confidence      REAL NOT NULL DEFAULT 0.5,    -- 0-1 (Ollama self-report)
    evidence_quote  TEXT,
    created_at      TEXT NOT NULL,
    FOREIGN KEY (report_id) REFERENCES analyst_reports(id)
);
CREATE INDEX IF NOT EXISTS idx_ainsights_ticker ON analyst_insights(ticker, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ainsights_report ON analyst_insights(report_id);

-- Predictions log — para learning loop (Phase V.backlog analyst_backtest).
-- Grava cada prediction (analyst insight OR verdict OR YouTube claim) com
-- price-at-prediction; agent backtest compara com preço N dias depois
-- e computa accuracy por source. Feeds back em source credibility weights.
CREATE TABLE IF NOT EXISTS predictions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    source           TEXT NOT NULL,                -- 'analyst:xp' | 'analyst:fool' | 'youtube:channel' | 'verdict'
    source_ref       TEXT,                         -- report_id | video_id | run_id
    ticker           TEXT NOT NULL,
    prediction_date  TEXT NOT NULL,                -- ISO date when prediction was made
    price_at_pred    REAL,                         -- from prices table at pred date
    predicted_stance TEXT NOT NULL,                -- bull | bear | neutral
    price_target     REAL,                         -- nullable
    horizon_days     INTEGER DEFAULT 90,           -- when to evaluate
    confidence       REAL DEFAULT 0.5,             -- source confidence 0-1
    claim            TEXT,                         -- original claim text (short)
    evaluated_at     TEXT,                         -- when backtest agent ran
    price_at_eval    REAL,                         -- price N days later
    outcome          TEXT,                         -- 'correct' | 'wrong' | 'neutral' | 'pending'
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);
CREATE INDEX IF NOT EXISTS idx_pred_ticker_date ON predictions(ticker, prediction_date DESC);
CREATE INDEX IF NOT EXISTS idx_pred_eval_pending ON predictions(evaluated_at) WHERE evaluated_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_pred_source ON predictions(source);

-- Agent audit trail — cada run de agent registado persistentemente
-- (vai além do agent state JSON; permite queries históricas cross-agent).
CREATE TABLE IF NOT EXISTS agent_runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    agent           TEXT NOT NULL,
    status          TEXT NOT NULL,                 -- ok|no_action|failed|skipped
    started_at      TEXT NOT NULL,
    finished_at     TEXT,
    duration_sec    REAL,
    summary         TEXT,
    actions_json    TEXT,                          -- JSON array de actions
    errors_json     TEXT,                          -- JSON array de errors
    data_json       TEXT,                          -- JSON payload agent-specific
    reason          TEXT                           -- scheduled|manual|triggered
);
CREATE INDEX IF NOT EXISTS idx_agent_runs_agent ON agent_runs(agent, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_agent_runs_status ON agent_runs(status);
"""


SERIES_META_SEED = [
    ("SELIC_DAILY",  "SELIC efetiva diária (fator)",         "pct_daily",   "daily",   "bcb_sgs:11",  None),
    ("SELIC_META",   "Meta SELIC (a.a.)",                    "pct_annual",  "daily",   "bcb_sgs:432", None),
    ("CDI_DAILY",    "CDI diário",                           "pct_daily",   "daily",   "bcb_sgs:12",  None),
    ("IPCA_MONTHLY", "IPCA mensal",                          "pct_monthly", "monthly", "bcb_sgs:433", None),
    ("USDBRL_PTAX",  "PTAX venda USD/BRL",                   "brl",         "daily",   "bcb_sgs:1",   "yfinance:BRL=X"),
    ("IBOV",         "Índice Bovespa",                       "index",       "daily",   "yfinance:^BVSP", "brapi:^BVSP"),
    ("IFIX",         "Índice FII",                           "index",       "daily",   "statusinvest", "b3"),
]


def _add_column_if_missing(conn: sqlite3.Connection, table: str, col: str, ddl: str) -> None:
    """Idempotent ALTER TABLE ... ADD COLUMN (SQLite não tem IF NOT EXISTS em ADD)."""
    cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    if col not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {ddl}")


def _migrate(conn: sqlite3.Connection) -> None:
    """Migrações pontuais para DBs existentes."""
    # Phase Q v2: transcript cache em videos
    _add_column_if_missing(conn, "videos", "transcript_text", "TEXT")
    _add_column_if_missing(conn, "videos", "transcript_chunks_json", "TEXT")

    # Phase R (2026-04-23): portfolio_snapshots + fundamentals_history + earnings_calendar
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS portfolio_snapshots (
        date          TEXT NOT NULL,
        ticker        TEXT NOT NULL,
        quantity      REAL NOT NULL,
        price_close   REAL NOT NULL,
        mv_native     REAL NOT NULL,
        mv_brl        REAL NOT NULL,
        fx_rate       REAL NOT NULL,
        created_at    TEXT NOT NULL,
        PRIMARY KEY (date, ticker)
    );
    CREATE INDEX IF NOT EXISTS idx_snap_date ON portfolio_snapshots(date);
    CREATE INDEX IF NOT EXISTS idx_snap_ticker ON portfolio_snapshots(ticker);

    CREATE TABLE IF NOT EXISTS fundamentals_history (
        ticker         TEXT NOT NULL,
        period_end     TEXT NOT NULL,
        altman_z       REAL,
        altman_zone    TEXT,
        piotroski_f    INTEGER,
        div_safety     REAL,
        screen_score   REAL,
        screen_passes  INTEGER,
        pe             REAL,
        pb             REAL,
        dy             REAL,
        roe            REAL,
        source_event   TEXT,
        recorded_at    TEXT NOT NULL,
        PRIMARY KEY (ticker, period_end, recorded_at)
    );
    CREATE INDEX IF NOT EXISTS idx_fh_ticker ON fundamentals_history(ticker, recorded_at DESC);

    CREATE TABLE IF NOT EXISTS verdict_history (
        ticker          TEXT NOT NULL,
        date            TEXT NOT NULL,
        action          TEXT NOT NULL,
        total_score     REAL NOT NULL,
        confidence_pct  INTEGER NOT NULL,
        quality_score   REAL,
        valuation_score REAL,
        momentum_score  REAL,
        narrative_score REAL,
        price_at_verdict REAL,
        recorded_at     TEXT NOT NULL,
        PRIMARY KEY (ticker, date)
    );
    CREATE INDEX IF NOT EXISTS idx_vh_date ON verdict_history(date);
    CREATE INDEX IF NOT EXISTS idx_vh_action ON verdict_history(action);

    -- Tax lots (FIFO-ready); cada row = 1 compra individual.
    CREATE TABLE IF NOT EXISTS tax_lots (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker            TEXT NOT NULL,
        acquisition_date  TEXT NOT NULL,
        quantity          REAL NOT NULL,
        unit_cost         REAL NOT NULL,
        total_cost        REAL NOT NULL,
        tax_term          TEXT,        -- Short | Long
        days_held         INTEGER,
        source            TEXT NOT NULL DEFAULT 'jpm_import',
        imported_at       TEXT NOT NULL,
        active            INTEGER NOT NULL DEFAULT 1,
        sold_date         TEXT,
        sold_price        REAL,
        notes             TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_lots_ticker ON tax_lots(ticker);
    CREATE INDEX IF NOT EXISTS idx_lots_acq ON tax_lots(acquisition_date);

    -- Cash balance por broker/moeda (JPM Chase Sweep, XP, etc.)
    CREATE TABLE IF NOT EXISTS broker_cash (
        broker      TEXT NOT NULL,
        currency    TEXT NOT NULL,
        amount      REAL NOT NULL,
        as_of       TEXT NOT NULL,
        PRIMARY KEY (broker, currency)
    );
    """)


def init(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        # WAL mode — permite multi-agent concurrent writes sem lock contention.
        # Persistente no DB file (só precisa setar 1×).
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")  # WAL + normal = safe + fast
        conn.executescript(SCHEMA)
        _migrate(conn)
        if "br_investments" in db_path.name:
            conn.executemany(
                """INSERT INTO series_meta
                     (series_id, description, unit, frequency, source_primary, source_fallback)
                   VALUES (?,?,?,?,?,?)
                   ON CONFLICT(series_id) DO UPDATE SET
                     description=excluded.description, unit=excluded.unit,
                     frequency=excluded.frequency,
                     source_primary=excluded.source_primary,
                     source_fallback=excluded.source_fallback""",
                SERIES_META_SEED,
            )
        conn.commit()
    print(f"[ok] {db_path}")


def main() -> None:
    init(DATA_DIR / "br_investments.db")
    init(DATA_DIR / "us_investments.db")


if __name__ == "__main__":
    main()
