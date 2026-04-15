"""Monitor de fatos relevantes da CVM (IPE) — piloto ITSA4.

Fonte: CVM Dados Abertos — ficheiro anual IPE (Informações Periódicas
e Eventuais) em
  https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_<YYYY>.zip

O ficheiro traz TODAS as entregas do ano para todas as empresas abertas.
Filtramos pelo nome da companhia (piloto usa 'ITAUSA' para ITSA4) e
escrevemos em events:
    source='cvm', kind=Categoria (ou 'fato_relevante'), event_date=Data_Entrega.

Idempotente: desduplica pelo Protocolo_Entrega (guardado no campo url
depois do '#' como âncora — ou preferencialmente via chave natural).
Para simplificar e não mexer no schema, fazemos DELETE + INSERT das
linhas do ticker com kind a começar por 'fato' antes de reinserir
as de interesse — só para a janela corrente.

Uso:
    python monitors/cvm_monitor.py              # ITSA4, ano corrente
    python monitors/cvm_monitor.py PRIO3
    python monitors/cvm_monitor.py ITSA4 --year 2025
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

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"

CVM_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_{year}.zip"

# Mapeamento ticker -> substring a procurar em Nome_Companhia (UPPER).
# Generalizar depois movendo para universe.yaml (campo `cvm_name`).
TICKER_NAME = {
    "ITSA4": "ITAUSA",
    "PRIO3": "PETRORIO",
    "VALE3": "VALE",
    "BBDC4": "BRADESCO",
}

# Categorias IPE que consideramos "fatos relevantes" para o monitor.
# O ficheiro IPE inclui muitas categorias (Assembleia, Aviso, etc.);
# para o piloto foca-se em Fato Relevante e Comunicado ao Mercado.
WATCHED_CATEGORIES = {"Fato Relevante", "Comunicado ao Mercado"}


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with (LOG_DIR / "cvm_monitor.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


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


def filter_for_ticker(rows: list[dict], ticker: str) -> list[dict]:
    needle = TICKER_NAME.get(ticker.upper())
    if not needle:
        raise SystemExit(f"Sem mapeamento CVM para {ticker} em TICKER_NAME.")
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
    # Desduplica por (ticker, source, event_date, url). Schema não tem UNIQUE,
    # fazemos check manual antes de inserir.
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


def run(ticker: str, year: int | None = None) -> None:
    year = year or datetime.now().year
    _log({"event": "cvm_fetch_start", "ticker": ticker, "year": year})
    rows = download_ipe(year)
    matches = filter_for_ticker(rows, ticker)
    _log({"event": "cvm_filtered", "ticker": ticker, "total_rows": len(rows), "matches": len(matches)})

    with sqlite3.connect(DB_PATH) as conn:
        inserted = persist(conn, ticker, matches)
        conn.commit()

    _log({"event": "cvm_persisted", "ticker": ticker, "inserted": inserted, "already_in_db": len(matches) - inserted})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default="ITSA4")
    ap.add_argument("--year", type=int, default=None)
    args = ap.parse_args()
    run(args.ticker, args.year)


if __name__ == "__main__":
    main()
