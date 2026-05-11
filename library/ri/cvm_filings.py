"""CVM filings downloader — DFP/ITR/IPE/FCA via dados.cvm.gov.br.

Política:
  - Cache local em library/ri/cache/<source>/<year>.zip
  - TTL configurável (default 30 days para DFP/ITR; 1 day para IPE)
  - Filter agressivo: só extrai linhas para tickers em catalog.yaml
  - User-Agent identificável (não-anonymous)

Schema gerado:
  ri_documents (id, ticker, source, doc_kind, doc_date, period_end,
                filename, hash, ingested_at)
  cvm_dre, cvm_bpa, cvm_bpp, cvm_dfc — normalized financial statements per ticker

Uso:
    python -m library.ri.cvm_filings sources         # list available
    python -m library.ri.cvm_filings download dfp --year 2024
    python -m library.ri.cvm_filings download itr --year 2025
    python -m library.ri.cvm_filings ingest dfp --year 2024 --ticker VALE3
    python -m library.ri.cvm_filings ingest dfp --year 2024 --all-catalog
"""
from __future__ import annotations

import argparse
import csv
import io
import sqlite3
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

from . import CACHE_DIR

USER_AGENT = "investment-intelligence-bot/1.0 (personal-research; non-commercial)"

ROOT = Path(__file__).resolve().parent.parent.parent
DB_BR = ROOT / "data" / "br_investments.db"

SOURCES = {
    "dfp": "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{year}.zip",
    "itr": "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{year}.zip",
    "ipe": "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_{year}.zip",
    "fca": "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FCA/DADOS/fca_cia_aberta_{year}.zip",
    "fre": "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FRE/DADOS/fre_cia_aberta_{year}.zip",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS ri_documents (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    source          TEXT NOT NULL,        -- 'CVM_DFP', 'CVM_ITR', 'CVM_IPE', ...
    doc_kind        TEXT,                 -- 'DRE', 'BPA', 'BPP', 'DFC_MD', ...
    doc_date        TEXT,                 -- DT_REFER ou DT_RECEB
    period_end      TEXT,                 -- DT_FIM_EXERC
    filename        TEXT,
    hash            TEXT UNIQUE,
    ingested_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ri_docs_ticker ON ri_documents(ticker, source, period_end);

-- DRE rows (consolidated financial statements)
CREATE TABLE IF NOT EXISTS cvm_dre (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    source          TEXT NOT NULL,        -- 'DFP' or 'ITR'
    period_end      TEXT NOT NULL,
    grupo_dfp       TEXT,                 -- e.g. 'DF Consolidado - Demonstração do Resultado'
    cd_conta        TEXT,
    ds_conta        TEXT,
    vl_conta        REAL,
    escala          TEXT,                 -- 'MIL' or 'UNIDADE'
    moeda           TEXT,
    UNIQUE(ticker, source, period_end, cd_conta, grupo_dfp)
);

CREATE INDEX IF NOT EXISTS idx_cvm_dre ON cvm_dre(ticker, period_end);

CREATE TABLE IF NOT EXISTS cvm_bpa (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    source          TEXT NOT NULL,
    period_end      TEXT NOT NULL,
    grupo_dfp       TEXT,
    cd_conta        TEXT,
    ds_conta        TEXT,
    vl_conta        REAL,
    escala          TEXT,
    moeda           TEXT,
    UNIQUE(ticker, source, period_end, cd_conta, grupo_dfp)
);

CREATE INDEX IF NOT EXISTS idx_cvm_bpa ON cvm_bpa(ticker, period_end);

CREATE TABLE IF NOT EXISTS cvm_bpp (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    source          TEXT NOT NULL,
    period_end      TEXT NOT NULL,
    grupo_dfp       TEXT,
    cd_conta        TEXT,
    ds_conta        TEXT,
    vl_conta        REAL,
    escala          TEXT,
    moeda           TEXT,
    UNIQUE(ticker, source, period_end, cd_conta, grupo_dfp)
);

CREATE INDEX IF NOT EXISTS idx_cvm_bpp ON cvm_bpp(ticker, period_end);

CREATE TABLE IF NOT EXISTS cvm_dfc (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    source          TEXT NOT NULL,
    period_end      TEXT NOT NULL,
    grupo_dfp       TEXT,                 -- 'DFC_MD' or 'DFC_MI'
    cd_conta        TEXT,
    ds_conta        TEXT,
    vl_conta        REAL,
    escala          TEXT,
    moeda           TEXT,
    UNIQUE(ticker, source, period_end, cd_conta, grupo_dfp)
);

CREATE INDEX IF NOT EXISTS idx_cvm_dfc ON cvm_dfc(ticker, period_end);

CREATE TABLE IF NOT EXISTS cvm_ipe (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker          TEXT NOT NULL,
    cnpj            TEXT,
    dt_referencia   TEXT,
    categoria       TEXT,                 -- e.g. 'Fato Relevante', 'Aviso aos Acionistas'
    tipo            TEXT,
    especie         TEXT,
    assunto         TEXT,
    protocolo       TEXT,
    url             TEXT,
    ingested_at     TEXT NOT NULL,
    UNIQUE(ticker, protocolo)
);

CREATE INDEX IF NOT EXISTS idx_cvm_ipe ON cvm_ipe(ticker, dt_referencia);
"""


def ensure_schema() -> None:
    with sqlite3.connect(DB_BR) as c:
        c.executescript(SCHEMA)
        c.commit()


def cache_path_for(source: str, year: int) -> Path:
    d = CACHE_DIR / source.upper()
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{source}_cia_aberta_{year}.zip"


def download(source: str, year: int, force: bool = False, ttl_days: int = 30) -> Path:
    if source not in SOURCES:
        raise ValueError(f"Unknown source: {source}. Use one of {list(SOURCES)}")
    cache = cache_path_for(source, year)
    if cache.exists() and not force:
        age_days = (time.time() - cache.stat().st_mtime) / 86400
        if age_days < ttl_days:
            return cache
    url = SOURCES[source].format(year=year)
    print(f"[cvm_filings] downloading {url}")
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=120, stream=True)
    r.raise_for_status()
    cache.write_bytes(r.content)
    print(f"  saved {len(r.content)/1024/1024:.1f}MB to {cache.relative_to(ROOT)}")
    return cache


def _read_csv_in_zip(zip_path: Path, name: str) -> list[dict]:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(name) as f:
            text = io.TextIOWrapper(f, encoding="latin-1", newline="")
            return list(csv.DictReader(text, delimiter=";"))


def _list_csvs(zip_path: Path) -> list[str]:
    with zipfile.ZipFile(zip_path) as zf:
        return [n for n in zf.namelist() if n.lower().endswith(".csv")]


def load_catalog_codes() -> dict[str, dict]:
    """Use canonical catalog accessor (avoids "watchlist not in loop" recurring bug)."""
    from library.ri.catalog import by_codigo_cvm_index, by_cnpj_index
    return {
        "by_codigo": by_codigo_cvm_index(include_watchlist=True),
        "by_cnpj":   by_cnpj_index(include_watchlist=True, include_fiis=False),  # stocks only for ITR/DFP
    }


def ingest_dfp_or_itr(source: str, year: int, ticker_filter: str | None = None) -> dict:
    """Read all CSVs in zip, filter to catalog, insert into cvm_dre/bpa/bpp/dfc."""
    if source not in ("dfp", "itr"):
        raise ValueError("Use ingest_ipe for IPE")
    cache = download(source, year)
    csvs = _list_csvs(cache)
    catalog = load_catalog_codes()
    by_cnpj = catalog["by_cnpj"]

    table_map = {
        "DRE_con": "cvm_dre", "DRE_ind": "cvm_dre",
        "BPA_con": "cvm_bpa", "BPA_ind": "cvm_bpa",
        "BPP_con": "cvm_bpp", "BPP_ind": "cvm_bpp",
        "DFC_MD_con": "cvm_dfc", "DFC_MD_ind": "cvm_dfc",
        "DFC_MI_con": "cvm_dfc", "DFC_MI_ind": "cvm_dfc",
    }

    ensure_schema()
    counts = {"docs": 0, "rows": 0, "skipped_csvs": 0}

    for csv_name in csvs:
        # csv name pattern: dfp_cia_aberta_DRE_con_2024.csv
        # we extract the kind: DRE_con
        parts = csv_name.replace(".csv", "").split("_")
        kind = None
        for k in table_map:
            if k in csv_name:
                kind = k
                break
        if not kind:
            counts["skipped_csvs"] += 1
            continue
        target_table = table_map[kind]
        grupo_label = "DF Consolidado" if "_con" in kind else "DF Individual"

        rows = _read_csv_in_zip(cache, csv_name)
        per_table_inserts = 0
        with sqlite3.connect(DB_BR) as c:
            for row in rows:
                row_cnpj = "".join(ch for ch in row.get("CNPJ_CIA", "") if ch.isdigit())
                if row_cnpj not in by_cnpj:
                    continue
                entry = by_cnpj[row_cnpj]
                ticker = entry["ticker"]
                if ticker_filter and ticker != ticker_filter:
                    continue
                period_end = row.get("DT_FIM_EXERC") or row.get("DT_REFER")
                vl = row.get("VL_CONTA")
                try:
                    vl_f = float(vl) if vl else None
                except ValueError:
                    vl_f = None
                try:
                    c.execute(
                        f"""INSERT OR IGNORE INTO {target_table}
                            (ticker, source, period_end, grupo_dfp, cd_conta, ds_conta,
                             vl_conta, escala, moeda)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            ticker, source.upper(), period_end,
                            row.get("GRUPO_DFP", grupo_label),
                            row.get("CD_CONTA"), row.get("DS_CONTA"),
                            vl_f, row.get("ESCALA_MOEDA"), row.get("MOEDA"),
                        ),
                    )
                    per_table_inserts += 1
                except Exception:
                    pass
            c.commit()
        counts["rows"] += per_table_inserts
        if per_table_inserts:
            counts["docs"] += 1
            print(f"  {csv_name:<55} -> {target_table:<8}  rows={per_table_inserts}")

    return counts


def ingest_ipe(year: int, ticker_filter: str | None = None) -> dict:
    """IPE = Informe Periódico de Eventos (fatos relevantes etc.). Single CSV per year."""
    cache = download("ipe", year, ttl_days=1)
    catalog = load_catalog_codes()
    by_cnpj = catalog["by_cnpj"]
    ensure_schema()
    counts = {"docs": 0}

    csvs = _list_csvs(cache)
    if not csvs:
        return counts
    rows = _read_csv_in_zip(cache, csvs[0])
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(DB_BR) as c:
        for row in rows:
            row_cnpj = "".join(ch for ch in row.get("CNPJ_Companhia", "") if ch.isdigit())
            if row_cnpj not in by_cnpj:
                continue
            entry = by_cnpj[row_cnpj]
            ticker = entry["ticker"]
            if ticker_filter and ticker != ticker_filter:
                continue
            try:
                c.execute(
                    """INSERT OR IGNORE INTO cvm_ipe
                       (ticker, cnpj, dt_referencia, categoria, tipo, especie,
                        assunto, protocolo, url, ingested_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        ticker, row.get("CNPJ_Companhia"),
                        row.get("Data_Referencia") or row.get("Data_Entrega"),
                        row.get("Categoria"), row.get("Tipo"), row.get("Especie"),
                        row.get("Assunto"), row.get("Protocolo_Entrega"),
                        row.get("Link_Download"), now,
                    ),
                )
                counts["docs"] += 1
            except Exception:
                pass
        c.commit()
    return counts


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("sources")

    p_dl = sub.add_parser("download")
    p_dl.add_argument("source", choices=SOURCES.keys())
    p_dl.add_argument("--year", type=int, required=True)
    p_dl.add_argument("--force", action="store_true")

    p_ing = sub.add_parser("ingest")
    p_ing.add_argument("source", choices=["dfp", "itr", "ipe"])
    p_ing.add_argument("--year", type=int, required=True)
    p_ing.add_argument("--ticker")
    p_ing.add_argument("--all-catalog", action="store_true")

    sub.add_parser("schema")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    if args.cmd == "sources":
        for k, v in SOURCES.items():
            print(f"  {k:<6} {v}")
    elif args.cmd == "download":
        download(args.source, args.year, force=args.force)
    elif args.cmd == "ingest":
        if args.source == "ipe":
            r = ingest_ipe(args.year, args.ticker)
        else:
            r = ingest_dfp_or_itr(args.source, args.year, args.ticker)
        print(f"\nResult: {r}")
    elif args.cmd == "schema":
        ensure_schema()
        print("schema applied to data/br_investments.db")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
