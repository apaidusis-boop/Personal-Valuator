"""FRED macro fetcher — séries essenciais US via endpoint CSV público.

FRED (Federal Reserve Economic Data) expõe séries via
https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES_ID>
sem autenticação. Usamos isso para não depender de API key.

Persiste em data/us_investments.db -> tabela `series`.
Prefixo `FRED_` no series_id para não colidir com BCB_*.

Séries seed (escolhidas para o briefing + regime classifier):
  FRED_FEDFUNDS      Federal Funds Effective Rate (DFF, daily)
  FRED_DGS10         10-Year Treasury constant maturity (DGS10, daily)
  FRED_DGS2          2-Year Treasury (DGS2, daily)
  FRED_T10Y2Y        10Y-2Y spread (T10Y2Y, daily) — inversion = recession signal
  FRED_CPI_YOY       CPI All Urban YoY (computed from CPIAUCSL monthly)
  FRED_UNRATE        Civilian Unemployment Rate (UNRATE, monthly)
  FRED_VIX           CBOE VIX (VIXCLS, daily)

Uso:
    python fetchers/fred_fetcher.py                # fetch todas as séries
    python fetchers/fred_fetcher.py --series DGS10 # só uma
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DB_US = ROOT / "data" / "us_investments.db"
LOG_DIR = ROOT / "logs"

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"

# (fred_id, our_series_id, description, unit, frequency, transform)
SERIES: list[tuple[str, str, str, str, str, str]] = [
    ("DFF",      "FRED_FEDFUNDS", "Federal Funds Effective Rate",      "pct_annual", "daily",   "raw"),
    ("DGS10",    "FRED_DGS10",    "10-Year Treasury yield (CMT)",       "pct_annual", "daily",   "raw"),
    ("DGS2",     "FRED_DGS2",     "2-Year Treasury yield (CMT)",        "pct_annual", "daily",   "raw"),
    ("T10Y2Y",   "FRED_T10Y2Y",   "10Y-2Y spread (inversion = recession signal)", "pct_annual", "daily", "raw"),
    ("CPIAUCSL", "FRED_CPI_YOY",  "CPI All Urban YoY (computed)",       "pct_annual", "monthly", "yoy_pct"),
    ("UNRATE",   "FRED_UNRATE",   "Civilian Unemployment Rate",         "pct_annual", "monthly", "raw"),
    ("VIXCLS",   "FRED_VIX",      "CBOE VIX (option-implied S&P vol)",  "index",      "daily",   "raw"),
]


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False)
    with (LOG_DIR / "fred_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _fetch_csv(fred_id: str) -> list[tuple[str, float]]:
    """Retorna lista (date_iso, value) a partir do CSV FRED. Skips '.'  (missing)."""
    url = FRED_CSV.format(sid=fred_id)
    r = requests.get(url, timeout=30,
                     headers={"User-Agent": "investment-intelligence/1.0"})
    r.raise_for_status()
    out: list[tuple[str, float]] = []
    reader = csv.reader(io.StringIO(r.text))
    header = next(reader, None)
    if not header:
        return out
    for row in reader:
        if len(row) < 2:
            continue
        d, v = row[0], row[1].strip()
        if not d or v in (".", "", "NA"):
            continue
        try:
            out.append((d, float(v)))
        except ValueError:
            continue
    return out


def _transform_yoy(series: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """Converte série de níveis mensais em YoY %. Requer pelo menos 13 meses."""
    idx = {d: v for d, v in series}
    out: list[tuple[str, float]] = []
    for d, v in series:
        # procura o valor 12 meses atrás
        year, month = int(d[:4]), int(d[5:7])
        prev = f"{year-1:04d}-{month:02d}-{d[8:]}"
        p = idx.get(prev)
        if p and p > 0:
            out.append((d, (v / p - 1) * 100.0))
    return out


def upsert_series(conn: sqlite3.Connection, series_id: str, points: list[tuple[str, float]]) -> int:
    now = _now_iso()
    n = 0
    for d, v in points:
        conn.execute(
            """INSERT INTO series (series_id, date, value, source, fetched_at)
               VALUES (?,?,?,?,?)
               ON CONFLICT(series_id, date) DO UPDATE SET
                 value=excluded.value, fetched_at=excluded.fetched_at""",
            (series_id, d, v, "fred", now),
        )
        n += 1
    return n


def upsert_meta(conn: sqlite3.Connection, series_id: str, description: str,
                unit: str, frequency: str, source: str) -> None:
    conn.execute(
        """INSERT INTO series_meta (series_id, description, unit, frequency,
                                    source_primary, source_fallback)
           VALUES (?,?,?,?,?,?)
           ON CONFLICT(series_id) DO UPDATE SET
             description=excluded.description, unit=excluded.unit,
             frequency=excluded.frequency, source_primary=excluded.source_primary""",
        (series_id, description, unit, frequency, source, None),
    )


def fetch_all(*, only: str | None = None) -> dict:
    results: dict = {"ok": [], "bad": []}
    with sqlite3.connect(DB_US) as conn:
        for fred_id, our_id, desc, unit, freq, transform in SERIES:
            if only and fred_id != only and our_id != only:
                continue
            try:
                raw = _fetch_csv(fred_id)
                if transform == "yoy_pct":
                    pts = _transform_yoy(raw)
                else:
                    pts = raw
                n = upsert_series(conn, our_id, pts)
                upsert_meta(conn, our_id, desc, unit, freq, f"fred:{fred_id}")
                conn.commit()
                _log({"event": "fred_fetch_ok", "fred_id": fred_id,
                      "series_id": our_id, "n_points": n,
                      "range": [pts[0][0], pts[-1][0]] if pts else None})
                results["ok"].append((our_id, n))
            except Exception as e:
                _log({"event": "fred_fetch_fail", "fred_id": fred_id,
                      "error": f"{type(e).__name__}: {e}"})
                results["bad"].append((our_id, str(e)[:60]))
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", help="Fetch uma série só (ID FRED ou nosso series_id)")
    args = ap.parse_args()
    r = fetch_all(only=args.series)
    print(f"\n[fred] ok={len(r['ok'])} bad={len(r['bad'])}")
    for sid, n in r["ok"]:
        print(f"  {sid:<22} {n:>6} pts")
    for sid, err in r["bad"]:
        print(f"  {sid:<22} FAIL {err}")


if __name__ == "__main__":
    main()
