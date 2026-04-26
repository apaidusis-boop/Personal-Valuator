"""SEC EDGAR Company Facts — validação autoritativa do streak de dividendos US.

O yfinance tem histórico de dividendos desde 1962 (floor do Yahoo), o que
para a maioria das empresas é mais longo do que o SEC XBRL (que só começa
em ~2007, quando o XBRL foi mandatado). Por isso a *substituição* simples
pioraria o streak.

Estratégia final: **cross-validation + máximo**.
  - Calcula o streak SEC (unbroken desde 2007+) a partir do Company Facts XBRL.
  - Lê o streak yfinance já persistido em `fundamentals`.
  - Novo streak = max(yf, sec). SEC nunca piora; se coincide ou excede, a
    série yf é "vouched for" pela SEC no período coberto.
  - `is_aristocrat=1` quando o streak final ≥ 25 (aproximação S&P Aristocrats).
  - `dividend_streak_source` regista qual fonte ditou o valor:
      * `sec_edgar_validated` — SEC cobriu integralmente os últimos N anos
        (validação cruzada com yf)
      * `yfinance`            — SEC sem CIK/facts (ADR/ETF estrangeiro), yf só
      * `sec_edgar`           — raro, SEC excedeu yf

Endpoint: https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json

Conceitos XBRL (us-gaap) varridos — união dos anos com valor > 0:
  - CommonStockDividendsPerShareDeclared
  - CommonStockDividendsPerShareCashPaid
  - PaymentsOfDividendsCommonStock
  - Dividends

Cache 7 dias em data/sec_cache/facts/.

Uso:
    python fetchers/sec_edgar_fetcher.py            # todos os tickers US
    python fetchers/sec_edgar_fetcher.py JNJ        # só JNJ
    python fetchers/sec_edgar_fetcher.py --dry-run  # não escreve na DB
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import time
from datetime import datetime, timezone
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
FACTS_CACHE = CACHE_DIR / "facts"

TICKER_MAP_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
USER_AGENT = "investment-intelligence apaidusis@gmail.com"

DIVIDEND_CONCEPTS_GAAP = [
    "CommonStockDividendsPerShareDeclared",
    "CommonStockDividendsPerShareCashPaid",
    "PaymentsOfDividendsCommonStock",
    "Dividends",
]

# Foreign private issuers (20-F) usam IFRS — TSM, NU, BN, etc.
DIVIDEND_CONCEPTS_IFRS = [
    "DividendsPaid",
    "DividendsPaidClassifiedAsFinancingActivities",
    "DividendsPaidOrdinarySharesPerShare",
    "DividendsRecognisedAsDistributionsToOwnersOfParent",
    "DividendsRecognisedAsDistributionsToOwnersPerShare",
]

ARISTOCRAT_STREAK_THRESHOLD = 25


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(event: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    line = json.dumps({"ts": _now_iso(), **event}, ensure_ascii=False, default=str)
    with (LOG_DIR / "sec_edgar_fetcher.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _session() -> requests.Session:
    s = requests.Session()
    retry = Retry(total=5, backoff_factor=2,
                  status_forcelist=(429, 500, 502, 503, 504),
                  allowed_methods=("GET",))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"})
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


def fetch_company_facts(sess: requests.Session, cik10: str) -> dict | None:
    """Company Facts JSON — cache 7 dias. Devolve None em 404 (companhia
    sem XBRL, tipicamente ADR estrangeiro)."""
    FACTS_CACHE.mkdir(parents=True, exist_ok=True)
    cache = FACTS_CACHE / f"CIK{cik10}.json"
    if cache.exists() and (time.time() - cache.stat().st_mtime) < 7 * 86400:
        return json.loads(cache.read_text(encoding="utf-8"))
    sess.headers["Host"] = "data.sec.gov"
    url = FACTS_URL.format(cik10=cik10)
    r = sess.get(url, timeout=60)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    data = r.json()
    cache.write_text(json.dumps(data), encoding="utf-8")
    return data


def extract_dividend_years(facts: dict) -> set[int]:
    """Devolve o conjunto de anos calendário com pelo menos um registo de
    dividendo > 0. Varre us-gaap (domestic filers) e ifrs-full (20-F filers:
    TSM, NU, BN, etc.)."""
    ns_block = facts.get("facts") or {}
    years: set[int] = set()
    for ns, concepts in [("us-gaap", DIVIDEND_CONCEPTS_GAAP),
                         ("ifrs-full", DIVIDEND_CONCEPTS_IFRS)]:
        scope = ns_block.get(ns) or {}
        for concept in concepts:
            c = scope.get(concept)
            if not c:
                continue
            for entries in (c.get("units") or {}).values():
                for e in entries:
                    val = e.get("val")
                    end = e.get("end")
                    if val and val > 0 and end and len(end) >= 4:
                        try:
                            years.add(int(end[:4]))
                        except ValueError:
                            continue
    return years


def consecutive_streak(years: set[int], as_of_year: int | None = None) -> int:
    """Anos consecutivos terminando no mais recente (≤ as_of_year).
    Tolera um gap de 1 ano no topo: se o último ano calendário ainda não
    reportou (ex.: 2026 em Abril antes do 10-K), verifica a partir do
    anterior. Isto evita falsos zeros em Jan-Abr."""
    if not years:
        return 0
    ys = sorted(years, reverse=True)
    if as_of_year is not None:
        ys = [y for y in ys if y <= as_of_year]
        if not ys:
            return 0
    streak = 1
    for i in range(1, len(ys)):
        if ys[i - 1] - ys[i] == 1:
            streak += 1
        else:
            break
    return streak


def compute_streak(facts: dict) -> tuple[int, int | None]:
    """Devolve (streak, last_year). Tolera o ano corrente incompleto."""
    years = extract_dividend_years(facts)
    if not years:
        return 0, None
    current_year = datetime.now(timezone.utc).year
    last = max(years)
    # Se o último ano é o corrente, usa-o; se falta (ex: Jan-Abr 2026 e
    # o último registo é 2025), conta a partir do ano anterior sem penalizar.
    anchor = current_year if current_year in years else current_year - 1
    streak = consecutive_streak(years, as_of_year=anchor)
    return streak, last


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Adiciona `dividend_streak_source` se não existir (idempotente)."""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(fundamentals)").fetchall()}
    if "dividend_streak_source" not in cols:
        conn.execute("ALTER TABLE fundamentals ADD COLUMN dividend_streak_source TEXT")
        _log({"event": "sec_schema_migration", "added": "dividend_streak_source"})


def load_current_streak(conn: sqlite3.Connection, ticker: str) -> tuple[str | None, int | None]:
    """Devolve (period_end, current_streak) da linha mais recente. (None, None) se
    o ticker ainda não tem fundamentals."""
    row = conn.execute(
        "SELECT period_end, dividend_streak_years FROM fundamentals "
        "WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    if not row:
        return None, None
    return row[0], row[1]


def persist_streak(conn: sqlite3.Connection, ticker: str, period_end: str,
                   streak: int, is_aristocrat: bool, source: str) -> None:
    conn.execute(
        """UPDATE fundamentals
           SET dividend_streak_years = ?,
               is_aristocrat = ?,
               dividend_streak_source = ?
           WHERE ticker = ? AND period_end = ?""",
        (streak, 1 if is_aristocrat else 0, source, ticker, period_end),
    )


def process_ticker(sess: requests.Session, cik_map: dict[str, str],
                   ticker: str, conn: sqlite3.Connection | None,
                   dry_run: bool) -> dict:
    tk_upper = ticker.upper()
    cik10 = cik_map.get(tk_upper) or cik_map.get(tk_upper.replace("-", ""))

    period_end, yf_streak = (None, None)
    if conn is not None:
        period_end, yf_streak = load_current_streak(conn, ticker)

    # Sem CIK — ETF/ADR estrangeiro (GREK, TSM, BN, NU): deixa yf sozinho
    # a ditar o streak; só actualiza is_aristocrat + source.
    if not cik10:
        _log({"event": "sec_facts_no_cik", "ticker": ticker})
        final = yf_streak or 0
        result = {"ticker": ticker, "status": "no_cik",
                  "yf_streak": yf_streak, "sec_streak": None,
                  "final_streak": final,
                  "is_aristocrat": final >= ARISTOCRAT_STREAK_THRESHOLD,
                  "source": "yfinance"}
        if not dry_run and conn is not None and period_end is not None:
            persist_streak(conn, ticker, period_end, final,
                           result["is_aristocrat"], "yfinance")
        return result

    facts = fetch_company_facts(sess, cik10)
    time.sleep(0.12)  # ~8 req/s, seguro face ao limite de 10 req/s
    if facts is None:
        _log({"event": "sec_facts_404", "ticker": ticker, "cik": cik10})
        final = yf_streak or 0
        result = {"ticker": ticker, "status": "no_facts",
                  "yf_streak": yf_streak, "sec_streak": None,
                  "final_streak": final,
                  "is_aristocrat": final >= ARISTOCRAT_STREAK_THRESHOLD,
                  "source": "yfinance"}
        if not dry_run and conn is not None and period_end is not None:
            persist_streak(conn, ticker, period_end, final,
                           result["is_aristocrat"], "yfinance")
        return result

    sec_streak, last_year = compute_streak(facts)
    final_streak = max(sec_streak, yf_streak or 0)

    # Source: SEC tem a última palavra só se excedeu yf (raro). Caso contrário,
    # "sec_edgar_validated" sinaliza que SEC cobriu todos os anos que afirma.
    if sec_streak == 0:
        source = "yfinance"
    elif sec_streak >= (yf_streak or 0):
        source = "sec_edgar"
    else:
        source = "sec_edgar_validated"

    is_aristocrat = final_streak >= ARISTOCRAT_STREAK_THRESHOLD

    result = {
        "ticker": ticker, "status": "ok",
        "yf_streak": yf_streak, "sec_streak": sec_streak, "last_year": last_year,
        "final_streak": final_streak,
        "is_aristocrat": is_aristocrat, "source": source,
    }

    if not dry_run and conn is not None:
        if period_end is None:
            result["status"] = "no_fundamentals_row"
        else:
            persist_streak(conn, ticker, period_end, final_streak,
                           is_aristocrat, source)

    _log({"event": "sec_facts_streak", **result})
    return result


def run_all(tickers: list[str] | None = None, dry_run: bool = False) -> list[dict]:
    sess = _session()
    _log({"event": "sec_facts_start", "tickers": len(tickers) if tickers else "all",
          "dry_run": dry_run})

    cik_map = fetch_ticker_map(sess)
    universe = tickers or load_us_tickers()

    results: list[dict] = []
    if dry_run:
        for t in universe:
            try:
                results.append(process_ticker(sess, cik_map, t, None, dry_run=True))
            except Exception as e:  # noqa: BLE001
                _log({"event": "sec_facts_error", "ticker": t, "err": str(e)[:120]})
                results.append({"ticker": t, "status": "error", "err": str(e)[:120]})
        return results

    with sqlite3.connect(DB_PATH) as conn:
        ensure_schema(conn)
        for t in universe:
            try:
                results.append(process_ticker(sess, cik_map, t, conn, dry_run=False))
            except Exception as e:  # noqa: BLE001
                _log({"event": "sec_facts_error", "ticker": t, "err": str(e)[:120]})
                results.append({"ticker": t, "status": "error", "err": str(e)[:120]})
        conn.commit()

    ok = [r for r in results if r["status"] == "ok"]
    _log({"event": "sec_facts_done", "total": len(results), "ok": len(ok),
          "aristocrats": sum(1 for r in ok if r.get("is_aristocrat"))})
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?", default=None)
    ap.add_argument("--dry-run", action="store_true",
                    help="não escreve na DB, só calcula e imprime")
    args = ap.parse_args()

    tickers = [args.ticker] if args.ticker else None
    results = run_all(tickers, dry_run=args.dry_run)

    print(f"\n=== SEC EDGAR Company Facts ===")
    print(f"Tickers processados: {len(results)}")
    ok = [r for r in results if r["status"] == "ok"]
    no_cik = [r for r in results if r["status"] == "no_cik"]
    no_facts = [r for r in results if r["status"] == "no_facts"]
    errors = [r for r in results if r["status"] == "error"]

    print(f"OK: {len(ok)}  |  sem CIK: {len(no_cik)}  |  sem facts: {len(no_facts)}  |  erros: {len(errors)}")
    if ok or no_cik:
        print("\nStreak final por ticker (top 20):")
        rows = ok + no_cik
        for r in sorted(rows, key=lambda r: r.get("final_streak") or 0, reverse=True)[:20]:
            tag = " [ARISTOCRAT]" if r.get("is_aristocrat") else ""
            yf = r.get("yf_streak")
            sec = r.get("sec_streak")
            print(f"  {r['ticker']:7s} final={r.get('final_streak'):>3}  "
                  f"yf={yf if yf is not None else '-':>3}  sec={sec if sec is not None else '-':>3}  "
                  f"src={r.get('source','?'):>22}{tag}")
    if errors:
        print(f"\nErros: {', '.join(r['ticker'] for r in errors)} — ver logs/sec_edgar_fetcher.log")


if __name__ == "__main__":
    main()
