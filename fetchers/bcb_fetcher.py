"""BCB SGS fetcher — séries macro e FX (SELIC, CDI, IPCA, PTAX).

API pública, sem autenticação:
    https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?
        formato=json&dataInicial=dd/MM/yyyy&dataFinal=dd/MM/yyyy

Devolve JSON: [{"data": "15/04/2026", "valor": "14.75"}, ...]

Persiste em data/br_investments.db, tabela `series`. Idempotente.

Uso:
    python fetchers/bcb_fetcher.py SELIC_DAILY --days 365
    python fetchers/bcb_fetcher.py --all --days 365
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"

BCB_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"

# series_id → (bcb_code, scale)
# scale: 1.0 = valor directo; 0.01 = valor vem em % e queremos fracção
SGS_MAP: dict[str, tuple[int, float]] = {
    "SELIC_DAILY":  (11,  0.01),   # % a.d. → fracção diária
    "SELIC_META":   (432, 1.0),    # % a.a. mantém-se em % a.a.
    "CDI_DAILY":    (12,  0.01),
    "IPCA_MONTHLY": (433, 0.01),
    "USDBRL_PTAX":  (1,   1.0),
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False)
    with (LOG_DIR / "bcb_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _parse_br_date(s: str) -> str:
    """`15/04/2026` → `2026-04-15`."""
    d, m, y = s.split("/")
    return f"{y}-{m.zfill(2)}-{d.zfill(2)}"


def fetch_sgs(code: int, start: str, end: str) -> list[dict]:
    """start/end em formato dd/MM/yyyy."""
    url = BCB_BASE.format(code=code)
    params = {"formato": "json", "dataInicial": start, "dataFinal": end}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def persist(series_id: str, rows: list[dict], scale: float, source: str) -> int:
    now = _now_iso()
    count = 0
    with sqlite3.connect(DB_PATH) as conn:
        for row in rows:
            try:
                date = _parse_br_date(row["data"])
                value = float(row["valor"]) * scale
            except (KeyError, ValueError):
                continue
            conn.execute(
                """INSERT INTO series (series_id, date, value, source, fetched_at)
                   VALUES (?,?,?,?,?)
                   ON CONFLICT(series_id, date) DO UPDATE SET
                     value=excluded.value, source=excluded.source,
                     fetched_at=excluded.fetched_at""",
                (series_id, date, value, source, now),
            )
            count += 1
        conn.commit()
    return count


def run(series_id: str, days: int = 365) -> int:
    if series_id not in SGS_MAP:
        raise SystemExit(f"série desconhecida: {series_id}. Conhecidas: {list(SGS_MAP)}")
    code, scale = SGS_MAP[series_id]
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=days)
    start = start_dt.strftime("%d/%m/%Y")
    end = end_dt.strftime("%d/%m/%Y")

    _log({"event": "bcb_fetch_start", "series_id": series_id, "code": code, "start": start, "end": end})
    rows = fetch_sgs(code, start, end)
    n = persist(series_id, rows, scale, source=f"bcb_sgs:{code}")
    _log({"event": "bcb_fetch_done", "series_id": series_id, "rows": n,
          "first": rows[0] if rows else None, "last": rows[-1] if rows else None})
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("series_id", nargs="?")
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--all", action="store_true", help="corre todas as séries conhecidas")
    args = ap.parse_args()

    if args.all:
        for sid in SGS_MAP:
            try:
                run(sid, days=args.days)
            except Exception as e:
                _log({"event": "bcb_fetch_error", "series_id": sid, "error": str(e)})
    else:
        if not args.series_id:
            ap.error("indicar series_id ou --all")
        run(args.series_id, days=args.days)


if __name__ == "__main__":
    main()
