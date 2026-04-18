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

-- ============================================================================
-- Narrativa de mercado (sector-level). Pipeline:
--   scrapers -> narrative_items (raw + classified)
--             -> sector_sentiment (rolling agregado)
--   series macro -> macro_regime (4D: rate/growth/fx/risk)
--   join histórico -> sector_base_rates
-- A combinação final (matriz fundamentals × sentiment × regime) vive em código,
-- não em SQL — ver narrative/rules.py.
-- ============================================================================

-- Item bruto capturado (artigo, vídeo, transcript). Após classificação por LLM
-- ganha sector/subsector/direction/thesis_tag. classified_at NULL = pendente.
CREATE TABLE IF NOT EXISTS narrative_items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at    TEXT NOT NULL,
    source        TEXT NOT NULL,          -- ex: 'rss:infomoney' | 'youtube:thiago_nigro' | 'transcript:JPM'
    source_url    TEXT,
    published_at  TEXT,                   -- timestamp original do conteúdo
    raw_title     TEXT,
    raw_text      TEXT,                   -- corpo do artigo ou transcript
    lang          TEXT,
    market        TEXT,                   -- 'br' | 'us' | 'global'
    classified_at TEXT,
    sector        TEXT,                   -- output classifier; NULL se pendente
    subsector     TEXT,
    direction     REAL,                   -- [-1, +1]
    magnitude     INTEGER,                -- 1..3
    thesis_tag    TEXT,                   -- macro|credit|governance|regulatory|earnings|panic|...
    thesis_action TEXT,                   -- 'contrarian_ok' | 'pause' | 'neutral' (derivado de thesis_tag)
    confidence    REAL,                   -- [0,1]
    extra_json    TEXT
);
CREATE INDEX IF NOT EXISTS idx_narrative_published ON narrative_items(published_at);
CREATE INDEX IF NOT EXISTS idx_narrative_sector ON narrative_items(sector, published_at);
CREATE INDEX IF NOT EXISTS idx_narrative_pending ON narrative_items(classified_at) WHERE classified_at IS NULL;

-- Agregado rolling por (mercado, sector, subsector, janela). subsector NULL =
-- rollup ao nível do sector.
CREATE TABLE IF NOT EXISTS sector_sentiment (
    as_of_date      TEXT NOT NULL,
    market          TEXT NOT NULL,
    sector          TEXT NOT NULL,
    subsector       TEXT NOT NULL DEFAULT '',  -- '' = rollup do sector inteiro
    window_days     INTEGER NOT NULL,          -- 7 | 30 | 90
    score           REAL NOT NULL,              -- [-1, +1] médio ponderado por confiança
    n_items         INTEGER NOT NULL,
    confidence      REAL NOT NULL,
    top_theses_json TEXT,                       -- {"credit": 12, "macro": 8, ...}
    PRIMARY KEY (as_of_date, market, sector, subsector, window_days)
);

-- Regime macro 4D derivado de `series` (SELIC, IPCA, USDBRL, IBOV, VIX, etc).
-- Recomputado diariamente. Histórico fica para join de base rates.
CREATE TABLE IF NOT EXISTS macro_regime (
    date            TEXT NOT NULL,
    market          TEXT NOT NULL,              -- 'br' | 'us'
    rate_regime     TEXT NOT NULL,              -- 'tightening' | 'easing' | 'hold'
    growth_regime   TEXT NOT NULL,              -- 'expansion' | 'slowdown' | 'recession' | 'recovery'
    fx_regime       TEXT NOT NULL,              -- 'strong_local' | 'weak_local' | 'neutral'
    risk_regime     TEXT NOT NULL,              -- 'risk_on' | 'risk_off' | 'neutral'
    details_json    TEXT,                       -- valores brutos que produziram a classificação
    PRIMARY KEY (date, market)
);

-- Retorno forward histórico do sector dado (regime macro × regime narrativa).
-- Em BR limitar lookback a 2010+ para evitar quebras estruturais (ver
-- narrative/base_rates.py). n_obs é o sinal de confiança.
CREATE TABLE IF NOT EXISTS sector_base_rates (
    market              TEXT NOT NULL,
    sector              TEXT NOT NULL,
    subsector           TEXT NOT NULL DEFAULT '',
    rate_regime         TEXT NOT NULL,
    growth_regime       TEXT NOT NULL,
    narrative_regime    TEXT NOT NULL,          -- 'very_neg' | 'neg' | 'neutral' | 'pos' | 'very_pos'
    forward_horizon     TEXT NOT NULL,          -- '3m' | '6m' | '12m'
    median_return       REAL NOT NULL,
    p25_return          REAL,
    p75_return          REAL,
    n_obs               INTEGER NOT NULL,
    last_computed_at    TEXT NOT NULL,
    PRIMARY KEY (market, sector, subsector, rate_regime, growth_regime, narrative_regime, forward_horizon)
);
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


def _add_column_if_missing(conn: sqlite3.Connection, table: str, col: str, decl: str) -> bool:
    """ALTER TABLE idempotente. Devolve True se adicionou a coluna."""
    existing = {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
    if col in existing:
        return False
    conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {decl}")
    return True


def _migrate(conn: sqlite3.Connection) -> None:
    """Migrations aditivas que CREATE TABLE IF NOT EXISTS não cobre.

    Idempotente — seguro correr em cada invocação.
    """
    # narrative_items: colunas adicionadas após o scaffold inicial
    _add_column_if_missing(conn, "narrative_items", "embedding_blob",   "BLOB")
    _add_column_if_missing(conn, "narrative_items", "retry_after",      "TEXT")
    _add_column_if_missing(conn, "narrative_items", "dedup_group_id",   "TEXT")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_narrative_dedup "
        "ON narrative_items(dedup_group_id, published_at)"
    )


def init(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
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
