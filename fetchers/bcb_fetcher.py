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
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "br_investments.db"
LOG_DIR = ROOT / "logs"

BCB_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"

# series_id → (bcb_code, scale, inception_date)
# scale: 1.0 = valor directo; 0.01 = valor vem em % e queremos fracção
# inception_date: dd/MM/yyyy — usado com --full para puxar desde o início da série
SGS_MAP: dict[str, tuple[int, float, str]] = {
    "SELIC_DAILY":  (11,  0.01, "04/06/1986"),   # % a.d. → fracção diária
    "SELIC_META":   (432, 1.0,  "05/03/1999"),   # Plano Real + metas
    "CDI_DAILY":    (12,  0.01, "04/03/1986"),
    "IPCA_MONTHLY": (433, 0.01, "01/01/1980"),
    "USDBRL_PTAX":  (1,   1.0,  "28/11/1984"),
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
    try:
        from agents._health import _is_tripped, record as _hb_record
        tripped, why = _is_tripped("bcb")
        if tripped:
            raise RuntimeError(f"bcb circuit breaker tripped: {why}")
    except ImportError:
        _hb_record = None

    url = BCB_BASE.format(code=code)
    params = {"formato": "json", "dataInicial": start, "dataFinal": end}
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        out = r.json()
        if _hb_record:
            _hb_record("bcb", "ok")
        return out
    except Exception as e:
        if _hb_record:
            _hb_record("bcb", "fail", f"{type(e).__name__}: {str(e)[:200]}")
        raise


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


def run(series_id: str, days: int | None = 365, since: str | None = None) -> int:
    """Puxa série. Se `since` (dd/MM/yyyy) for dado, ignora `days`.
    BCB SGS às vezes falha em ranges muito grandes; este wrapper chunka
    em janelas de ~10 anos quando o range ultrapassa isso."""
    if series_id not in SGS_MAP:
        raise SystemExit(f"série desconhecida: {series_id}. Conhecidas: {list(SGS_MAP)}")
    code, scale, _ = SGS_MAP[series_id]
    end_dt = datetime.now()
    start_dt = (datetime.strptime(since, "%d/%m/%Y") if since
                else end_dt - timedelta(days=days or 365))

    # chunking: janelas de 10 anos. SGS aceita ranges maiores para séries
    # pequenas (IPCA mensal), mas diárias longas podem truncar silent.
    chunk_days = 3650
    total = 0
    cur = start_dt
    first_row = None
    last_row = None
    while cur < end_dt:
        chunk_end = min(cur + timedelta(days=chunk_days), end_dt)
        start = cur.strftime("%d/%m/%Y")
        end = chunk_end.strftime("%d/%m/%Y")
        _log({"event": "bcb_fetch_start", "series_id": series_id, "code": code,
              "start": start, "end": end})
        try:
            rows = fetch_sgs(code, start, end)
        except Exception as e:
            _log({"event": "bcb_fetch_chunk_error", "series_id": series_id,
                  "start": start, "end": end, "error": str(e)[:120]})
            rows = []
        if rows:
            if first_row is None:
                first_row = rows[0]
            last_row = rows[-1]
        total += persist(series_id, rows, scale, source=f"bcb_sgs:{code}")
        cur = chunk_end + timedelta(days=1)

    _log({"event": "bcb_fetch_done", "series_id": series_id, "rows": total,
          "first": first_row, "last": last_row})
    return total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("series_id", nargs="?")
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--since", default=None, help="dd/MM/yyyy explícito")
    ap.add_argument("--all", action="store_true", help="corre todas as séries conhecidas")
    ap.add_argument("--full", action="store_true",
                    help="puxa desde inception_date (ignora --days e --since)")
    args = ap.parse_args()

    targets = list(SGS_MAP) if args.all or args.full else ([args.series_id] if args.series_id else [])
    if not targets:
        ap.error("indicar series_id ou --all ou --full")

    for sid in targets:
        try:
            if args.full:
                since = SGS_MAP[sid][2]
                run(sid, since=since)
            else:
                run(sid, days=args.days, since=args.since)
        except Exception as e:
            _log({"event": "bcb_fetch_error", "series_id": sid, "error": str(e)})


if __name__ == "__main__":
    main()
