"""Monitor de filings SEC para US holdings.

Fontes (SEC EDGAR, públicas, rate limit 10 req/s, User-Agent obrigatório):
  - Ticker -> CIK:   https://www.sec.gov/files/company_tickers.json
  - Submissions:     https://data.sec.gov/submissions/CIK{10d}.json

Para cada ticker em universe.yaml (us.holdings + us.watchlist + us.research_pool),
obtém as submissions recentes e guarda as de interesse em events.

Formulários monitorados por default: 8-K, 10-K, 10-Q, DEF 14A.

Idempotente: desduplica por (ticker, source='sec', event_date, url).

Uso:
    python monitors/sec_monitor.py                     # todos os tickers US
    python monitors/sec_monitor.py JNJ                 # só JNJ
    python monitors/sec_monitor.py --forms 8-K,10-K    # filtrar formulários
    python monitors/sec_monitor.py --lookback-days 30  # só filings recentes
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import yaml
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "us_investments.db"
LOG_DIR = ROOT / "logs"
UNIVERSE = ROOT / "config" / "universe.yaml"
CACHE_DIR = ROOT / "data" / "sec_cache"

TICKER_MAP_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik10}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_nodash}/{primary_doc}"

DEFAULT_FORMS = {"8-K", "10-K", "10-Q", "DEF 14A", "20-F", "6-K"}
USER_AGENT = "investment-intelligence apaidusis@gmail.com"


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = json.dumps({"ts": ts, **event}, ensure_ascii=False)
    with (LOG_DIR / "sec_monitor.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _session() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=5, backoff_factor=2,
                  status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=("GET",))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Encoding": "gzip, deflate",
        "Host": "",
    })
    return s


def load_us_tickers() -> list[str]:
    data = yaml.safe_load(UNIVERSE.read_text(encoding="utf-8"))
    us = data.get("us", {})
    out: list[str] = []
    for bucket in ("holdings", "watchlist", "research_pool"):
        g = us.get(bucket) or {}
        for e in (g.get("stocks") or []):
            out.append(e["ticker"])
    return out


def fetch_ticker_map(sess: requests.Session) -> dict[str, str]:
    """Devolve {TICKER: CIK_10_padded}. Cache 7 dias em data/sec_cache/."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / "company_tickers.json"
    if cache.exists() and (time.time() - cache.stat().st_mtime) < 7 * 86400:
        data = json.loads(cache.read_text(encoding="utf-8"))
    else:
        sess.headers["Host"] = "www.sec.gov"
        r = sess.get(TICKER_MAP_URL, timeout=60)
        r.raise_for_status()
        data = r.json()
        cache.write_text(json.dumps(data), encoding="utf-8")
    out: dict[str, str] = {}
    for entry in data.values():
        tk = str(entry["ticker"]).upper()
        cik = str(entry["cik_str"]).zfill(10)
        out[tk] = cik
    return out


def fetch_submissions(sess: requests.Session, cik10: str) -> dict:
    sess.headers["Host"] = "data.sec.gov"
    url = SUBMISSIONS_URL.format(cik10=cik10)
    r = sess.get(url, timeout=60)
    r.raise_for_status()
    return r.json()


def iter_recent_filings(submissions: dict):
    recent = (submissions.get("filings") or {}).get("recent") or {}
    forms = recent.get("form") or []
    dates = recent.get("filingDate") or []
    accessions = recent.get("accessionNumber") or []
    primary = recent.get("primaryDocument") or []
    items = recent.get("items") or []
    for i, form in enumerate(forms):
        yield {
            "form": form,
            "date": dates[i] if i < len(dates) else None,
            "accession": accessions[i] if i < len(accessions) else None,
            "primary_doc": primary[i] if i < len(primary) else None,
            "items": items[i] if i < len(items) else None,
        }


def build_archive_url(cik10: str, accession: str, primary_doc: str) -> str:
    if not accession or not primary_doc:
        return ""
    cik_int = str(int(cik10))
    accession_nodash = accession.replace("-", "")
    return ARCHIVE_URL.format(cik_int=cik_int, accession_nodash=accession_nodash,
                              primary_doc=primary_doc)


def normalise_kind(form: str) -> str:
    """Mapeia form SEC -> kind DB. 8-K = material event; 10-K = annual;
    10-Q = quarterly; DEF 14A = proxy; 20-F/6-K = foreign private issuer."""
    mapping = {
        "8-K": "8-K",
        "10-K": "10-K",
        "10-Q": "10-Q",
        "DEF 14A": "proxy",
        "20-F": "20-F",
        "6-K": "6-K",
    }
    return mapping.get(form, form)


def persist(conn: sqlite3.Connection, ticker: str, filings: list[dict]) -> int:
    inserted = 0
    for f in filings:
        date = f["date"]
        url = f.get("url") or None
        exists = conn.execute(
            """SELECT 1 FROM events WHERE ticker=? AND source='sec'
               AND event_date=? AND url=?""",
            (ticker, date, url),
        ).fetchone()
        if exists:
            continue
        conn.execute(
            """INSERT INTO events (ticker, event_date, source, kind, url, summary)
               VALUES (?,?,?,?,?,?)""",
            (ticker, date, "sec", f["kind"], url, f.get("summary")),
        )
        inserted += 1
    return inserted


def process_ticker(sess: requests.Session, cik_map: dict[str, str],
                   ticker: str, forms: set[str], since: datetime | None) -> list[dict]:
    """SEC mantém hífen em alguns tickers (BRK-B). Tenta exato, depois sem hífen.
    ETFs (GREK, etc.) não estão em company_tickers.json — falham silent."""
    tk_upper = ticker.upper()
    cik10 = cik_map.get(tk_upper) or cik_map.get(tk_upper.replace("-", ""))
    if not cik10:
        _log({"event": "ticker_not_found", "ticker": ticker})
        return []

    subs = fetch_submissions(sess, cik10)
    time.sleep(0.12)  # rate limit safety: ~8 req/s
    filings: list[dict] = []
    for f in iter_recent_filings(subs):
        if f["form"] not in forms:
            continue
        if since and f["date"] and f["date"] < since.strftime("%Y-%m-%d"):
            continue
        url = build_archive_url(cik10, f["accession"], f["primary_doc"])
        summary_parts = [f["form"]]
        if f.get("items"):
            summary_parts.append(f["items"])
        filings.append({
            "date": f["date"],
            "kind": normalise_kind(f["form"]),
            "url": url or None,
            "summary": " | ".join(p for p in summary_parts if p),
        })
    return filings


def run_all(tickers: list[str] | None = None,
            forms: set[str] | None = None,
            lookback_days: int | None = None) -> dict:
    forms = forms or DEFAULT_FORMS
    since = (datetime.now(timezone.utc) - timedelta(days=lookback_days)) if lookback_days else None

    sess = _session()
    _log({"event": "sec_fetch_start", "tickers": len(tickers) if tickers else "all",
          "forms": sorted(forms), "lookback_days": lookback_days})

    cik_map = fetch_ticker_map(sess)
    _log({"event": "sec_cik_map_loaded", "entries": len(cik_map)})

    universe = tickers or load_us_tickers()
    results: dict[str, int] = {}

    with sqlite3.connect(DB_PATH) as conn:
        for ticker in universe:
            try:
                filings = process_ticker(sess, cik_map, ticker, forms, since)
                inserted = persist(conn, ticker, filings)
                results[ticker] = inserted
                if filings:
                    _log({"event": "sec_ticker_done", "ticker": ticker,
                          "filings": len(filings), "inserted": inserted})
            except Exception as e:
                _log({"event": "sec_ticker_error", "ticker": ticker, "error": str(e)[:120]})
                results[ticker] = -1
        conn.commit()

    total = sum(v for v in results.values() if v > 0)
    _log({"event": "sec_all_done", "tickers": len(universe), "total_inserted": total})
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default=None)
    ap.add_argument("--forms", default=None,
                    help="Lista CSV de formulários (ex: 8-K,10-K). Default: 8-K,10-K,10-Q,DEF 14A,20-F,6-K")
    ap.add_argument("--lookback-days", type=int, default=None,
                    help="Só filings com filingDate >= hoje - N dias")
    args = ap.parse_args()

    forms = set(DEFAULT_FORMS)
    if args.forms:
        forms = {f.strip() for f in args.forms.split(",") if f.strip()}

    tickers = [args.ticker] if args.ticker else None
    results = run_all(tickers=tickers, forms=forms, lookback_days=args.lookback_days)

    new_events = {k: v for k, v in results.items() if v > 0}
    errors = {k: v for k, v in results.items() if v < 0}
    print(f"\n=== SEC monitor ===")
    print(f"Tickers processados: {len(results)}")
    print(f"Novos eventos inseridos: {sum(v for v in results.values() if v > 0)}")
    if new_events:
        print("Por ticker com novidades:")
        for t, n in sorted(new_events.items(), key=lambda x: x[1], reverse=True):
            print(f"  {t}: {n}")
    if errors:
        print(f"Erros: {len(errors)} tickers — ver logs/sec_monitor.log")


if __name__ == "__main__":
    main()
