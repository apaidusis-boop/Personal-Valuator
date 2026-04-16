"""Monitor de fatos relevantes da CVM (IPE).

Fonte: CVM Dados Abertos — ficheiro anual IPE (Informações Periódicas
e Eventuais) em
  https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_<YYYY>.zip

O ficheiro traz TODAS as entregas do ano para todas as empresas abertas.
Filtramos pelo campo `cvm_name` de config/universe.yaml (substring match
em Nome_Companhia) e escrevemos em events:
    source='cvm', kind=Categoria (ou 'fato_relevante'), event_date=Data_Entrega.

Idempotente: desduplica por (ticker, source='cvm', event_date, url).

Uso:
    python monitors/cvm_monitor.py              # ITSA4, ano corrente
    python monitors/cvm_monitor.py PRIO3
    python monitors/cvm_monitor.py ITSA4 --year 2025
    python monitors/cvm_monitor.py --all        # todos os tickers com cvm_name
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sqlite3
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"

CVM_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_{year}.zip"

# Categorias IPE que consideramos relevantes para o monitor.
WATCHED_CATEGORIES = {"Fato Relevante", "Comunicado ao Mercado"}


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with (LOG_DIR / "cvm_monitor.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


# ---------- universe.yaml → cvm_name ----------

def _load_cvm_map() -> dict[str, str]:
    """Devolve {ticker: cvm_name} para todas as entradas BR com cvm_name."""
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    br = data.get("br", {}) or {}
    mapping: dict[str, str] = {}
    for bucket in ("holdings", "watchlist", "research_pool"):
        group = br.get(bucket, {}) or {}
        if isinstance(group, list):
            entries = group
        else:
            entries = []
            for section in group.values():
                entries.extend(section or [])
        for entry in entries:
            cvm = entry.get("cvm_name")
            if cvm:
                mapping[entry["ticker"]] = cvm.upper()
    return mapping


def resolve_cvm_name(ticker: str) -> str:
    """Devolve a substring CVM para um ticker, lendo de universe.yaml."""
    mapping = _load_cvm_map()
    needle = mapping.get(ticker.upper())
    if not needle:
        raise RuntimeError(
            f"Sem campo cvm_name para {ticker} em config/universe.yaml. "
            f"Tickers com cvm_name definido: {sorted(mapping.keys())}"
        )
    return needle


def all_cvm_tickers() -> list[str]:
    """Devolve todos os tickers BR com cvm_name definido."""
    return sorted(_load_cvm_map().keys())


# ---------- fetch + filter + persist ----------

def download_ipe(year: int) -> list[dict]:
    url = CVM_URL.format(year=year)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = next(n for n in z.namelist() if n.endswith(".csv"))
        with z.open(name) as f:
            text = io.TextIOWrapper(f, encoding="latin-1", newline="")
            reader = csv.DictReader(text, delimiter=";")
            return list(reader)


def filter_for_ticker(rows: list[dict], ticker: str, needle: str) -> list[dict]:
    out = []
    for row in rows:
        name = (row.get("Nome_Companhia") or "").upper()
        if needle not in name:
            continue
        if (row.get("Categoria") or "") not in WATCHED_CATEGORIES:
            continue
        out.append(row)
    return out


def normalise(row: dict) -> dict:
    categoria = (row.get("Categoria") or "").strip()
    kind = "fato_relevante" if categoria == "Fato Relevante" else "comunicado"
    summary_parts = [
        row.get("Tipo") or "",
        row.get("Especie") or "",
        row.get("Assunto") or "",
    ]
    summary = " | ".join(p.strip() for p in summary_parts if p and p.strip())
    return {
        "event_date": (row.get("Data_Entrega") or "")[:10],
        "kind": kind,
        "url": row.get("Link_Download") or None,
        "summary": summary or None,
        "protocolo": row.get("Protocolo_Entrega") or "",
    }


def persist(conn: sqlite3.Connection, ticker: str, rows: list[dict]) -> int:
    inserted = 0
    for r in rows:
        n = normalise(r)
        exists = conn.execute(
            """SELECT 1 FROM events
               WHERE ticker=? AND source='cvm' AND event_date=? AND url=?""",
            (ticker, n["event_date"], n["url"]),
        ).fetchone()
        if exists:
            continue
        conn.execute(
            """INSERT INTO events (ticker, event_date, source, kind, url, summary)
               VALUES (?,?,?,?,?,?)""",
            (ticker, n["event_date"], "cvm", n["kind"], n["url"], n["summary"]),
        )
        inserted += 1
    return inserted


def run(ticker: str, year: int | None = None) -> dict:
    year = year or datetime.now().year
    needle = resolve_cvm_name(ticker)
    _log({"event": "cvm_fetch_start", "ticker": ticker, "year": year,
          "cvm_name": needle})
    rows = download_ipe(year)
    matches = filter_for_ticker(rows, ticker, needle)
    _log({"event": "cvm_filtered", "ticker": ticker, "total_rows": len(rows),
          "matches": len(matches)})

    with sqlite3.connect(DB_PATH) as conn:
        inserted = persist(conn, ticker, matches)
        conn.commit()

    result = {"ticker": ticker, "inserted": inserted,
              "already_in_db": len(matches) - inserted}
    _log({"event": "cvm_persisted", **result})
    return result


def run_all(year: int | None = None) -> list[dict]:
    """Corre o monitor para todos os tickers com cvm_name no universe.yaml.
    Descarrega o ZIP uma só vez e filtra para cada ticker."""
    year = year or datetime.now().year
    tickers = all_cvm_tickers()
    cvm_map = _load_cvm_map()
    _log({"event": "cvm_batch_start", "year": year, "tickers": tickers})

    rows = download_ipe(year)
    results = []

    with sqlite3.connect(DB_PATH) as conn:
        for ticker in tickers:
            needle = cvm_map[ticker]
            matches = filter_for_ticker(rows, ticker, needle)
            inserted = persist(conn, ticker, matches)
            r = {"ticker": ticker, "matches": len(matches), "inserted": inserted}
            _log({"event": "cvm_persisted", **r})
            results.append(r)
        conn.commit()

    _log({"event": "cvm_batch_done", "total_tickers": len(tickers),
          "total_inserted": sum(r["inserted"] for r in results)})
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="ITSA4")
    ap.add_argument("--year", type=int, default=None)
    ap.add_argument("--all", action="store_true",
                    help="Correr para todos os tickers BR com cvm_name definido")
    args = ap.parse_args()
    if args.all:
        run_all(args.year)
    else:
        run(args.ticker, args.year)


if __name__ == "__main__":
    main()
