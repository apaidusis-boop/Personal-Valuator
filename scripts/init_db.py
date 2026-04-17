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


def init(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA)
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
