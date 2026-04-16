"""Monitor de fatos relevantes da CVM (IPE).

Fonte: CVM Dados Abertos — ficheiro anual IPE (Informações Periódicas
e Eventuais) em
  https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_<YYYY>.zip

O ficheiro traz TODAS as entregas do ano para todas as empresas abertas.
Mapeamos ticker -> nome_CVM via config/universe.yaml (campo `cvm_name`).

Categorias filtradas: Fato Relevante, Comunicado ao Mercado.
Idempotente: desduplica por (ticker, source, event_date, url).

Uso:
    python monitors/cvm_monitor.py                    # todos os stocks BR do universo
    python monitors/cvm_monitor.py ITSA4              # só um ticker
    python monitors/cvm_monitor.py --year 2025        # outro ano
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sqlite3
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"

CVM_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_{year}.zip"

WATCHED_CATEGORIES = {"Fato Relevante", "Comunicado ao Mercado"}


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with (LOG_DIR / "cvm_monitor.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def load_ticker_map() -> dict[str, str]:
    """Devolve {ticker: cvm_name_substring} lido de universe.yaml.
    Só inclui entries com campo `cvm_name` (ignora FIIs e entries sem
    mapeamento)."""
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    br = data.get("br", {})
    for bucket in ("holdings", "watchlist", "research_pool"):
        g = br.get(bucket) or {}
        for e in (g.get("stocks") or []):
            name = e.get("cvm_name")
            if name:
                out[e["ticker"]] = str(name).upper()
    return out


def _session_with_retries() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=5, backoff_factor=2,
                  status_forcelist=(500, 502, 503, 504),
                  allowed_methods=("GET",))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({
        "User-Agent": "investment-intelligence/1.0 (apaidusis@gmail.com)",
        "Accept": "application/zip, */*",
    })
    return s


def download_ipe(year: int) -> list[dict]:
    url = CVM_URL.format(year=year)
    sess = _session_with_retries()
    r = sess.get(url, timeout=180)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = next(n for n in z.namelist() if n.endswith(".csv"))
        with z.open(name) as f:
            text = io.TextIOWrapper(f, encoding="latin-1", newline="")
            reader = csv.DictReader(text, delimiter=";")
            return list(reader)


def filter_rows(rows: list[dict], needle: str) -> list[dict]:
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


def run_all(year: int | None = None, only: str | None = None) -> dict:
    """Corre CVM monitor para todos os tickers em universe.yaml com cvm_name.
    Download único do ZIP do ano. Devolve dict {ticker: inserted_count}."""
    year = year or datetime.now().year
    ticker_map = load_ticker_map()
    if only:
        ticker_map = {only: ticker_map[only]} if only in ticker_map else {}
        if not ticker_map:
            raise SystemExit(f"{only} sem cvm_name em universe.yaml")

    _log({"event": "cvm_fetch_start", "year": year, "tickers": list(ticker_map)})
    rows = download_ipe(year)
    _log({"event": "cvm_download_done", "year": year, "total_rows": len(rows)})

    results: dict[str, int] = {}
    with sqlite3.connect(DB_PATH) as conn:
        for ticker, needle in ticker_map.items():
            matches = filter_rows(rows, needle)
            inserted = persist(conn, ticker, matches)
            results[ticker] = inserted
            if matches:
                _log({"event": "cvm_ticker_done", "ticker": ticker,
                      "matches": len(matches), "inserted": inserted})
        conn.commit()

    total_inserted = sum(results.values())
    _log({"event": "cvm_all_done", "year": year, "tickers": len(ticker_map),
          "total_inserted": total_inserted})
    return results


def run(ticker: str, year: int | None = None) -> None:
    """Compat — single ticker mode."""
    results = run_all(year=year, only=ticker)
    print(json.dumps(results, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default=None,
                    help="ticker específico (omitir corre para todos)")
    ap.add_argument("--year", type=int, default=None)
    args = ap.parse_args()

    if args.ticker:
        run(args.ticker, args.year)
    else:
        results = run_all(year=args.year)
        new_events = {k: v for k, v in results.items() if v > 0}
        print(f"\n=== CVM monitor ===")
        print(f"Tickers processados: {len(results)}")
        print(f"Novos eventos inseridos: {sum(results.values())}")
        if new_events:
            print("Por ticker com novidades:")
            for t, n in sorted(new_events.items(), key=lambda x: x[1], reverse=True):
                print(f"  {t}: {n}")


if __name__ == "__main__":
    main()
