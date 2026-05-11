"""earnings_react — reage a novos filings SEC/CVM: refetch + quality recompute + alert.

Pipeline:
  1. Para cada holding, lista eventos (SEC 8-K/10-Q/10-K, CVM fato relevante)
     mais recentes em DB.
  2. Compara com último snapshot em `fundamentals_history` — se há filing
     mais novo: triga refetch.
  3. Refetch: `yf_deep_fundamentals.py <ticker>` (para US) ou `brapi_fetcher`
     (para BR). Recompute Altman/Piotroski/DivSafety/Screen.
  4. Persiste novo snapshot em `fundamentals_history`.
  5. Detecta quality drift — alerta se:
     • Altman Δ < -0.5
     • Piotroski Δ ≤ -1
     • DivSafety Δ < -10
     • Screen passa → não passa (ou vice-versa)

Idempotente — pode correr múltiplas vezes sem duplicar.

Uso:
    python scripts/earnings_react.py               # todos os holdings
    python scripts/earnings_react.py ACN           # 1 ticker
    python scripts/earnings_react.py --dry-run     # não refetches
"""
from __future__ import annotations

import argparse
import sqlite3
import subprocess
import sys
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"


RELEVANT_KINDS = {"8-K", "10-Q", "10-K", "20-F", "6-K", "fato_relevante"}


def _latest_filing(db: sqlite3.Connection, ticker: str) -> tuple | None:
    r = db.execute(
        """SELECT event_date, kind FROM events
           WHERE ticker=? AND kind IN ({}) ORDER BY event_date DESC LIMIT 1""".format(
            ",".join(f"'{k}'" for k in RELEVANT_KINDS)
        ),
        (ticker,),
    ).fetchone()
    return r


def _last_recorded_history(db: sqlite3.Connection, ticker: str) -> tuple | None:
    try:
        return db.execute(
            """SELECT altman_z, piotroski_f, div_safety, screen_score, screen_passes,
                      period_end, recorded_at, source_event
               FROM fundamentals_history WHERE ticker=?
               ORDER BY recorded_at DESC LIMIT 1""",
            (ticker,),
        ).fetchone()
    except sqlite3.OperationalError:
        return None


def _recompute_quality(ticker: str, market: str) -> dict:
    """Calcula Altman + Piotroski + DivSafety + Screen actual."""
    result = {}
    try:
        from scoring import altman, piotroski, dividend_safety
        a = altman.compute(ticker, market)
        result["altman_z"] = round(a.z, 3) if a and a.applicable else None
        result["altman_zone"] = (
            "SAFE" if a and a.is_safe else
            "DISTRESS" if a and a.is_distress else
            "GREY" if a and a.applicable else None
        )
    except Exception as e:  # noqa: BLE001
        result["altman_err"] = str(e)[:80]

    try:
        from scoring import piotroski
        p = piotroski.compute(ticker, market)
        result["piotroski_f"] = p.f_score if p and p.applicable else None
    except Exception as e:  # noqa: BLE001
        result["piotroski_err"] = str(e)[:80]

    try:
        from scoring import dividend_safety
        d = dividend_safety.compute(ticker, market)
        result["div_safety"] = getattr(d, "total", None) if d else None
    except Exception as e:  # noqa: BLE001
        result["divsafety_err"] = str(e)[:80]

    # Screen
    try:
        from scoring import engine
        score_fn = getattr(engine, f"score_{market}", None)
        if score_fn:
            db_path = DB_BR if market == "br" else DB_US
            with sqlite3.connect(db_path) as conn:
                r = conn.execute(
                    "SELECT score, passes_screen, details_json FROM scores "
                    "WHERE ticker=? ORDER BY run_date DESC LIMIT 1", (ticker,)
                ).fetchone()
                if r:
                    result["screen_score"] = r[0]
                    result["screen_passes"] = int(r[1])
    except Exception as e:  # noqa: BLE001
        result["screen_err"] = str(e)[:80]

    # Fundamentals snapshot
    try:
        db_path = DB_BR if market == "br" else DB_US
        with sqlite3.connect(db_path) as conn:
            r = conn.execute(
                """SELECT period_end, pe, pb, dy, roe FROM fundamentals
                   WHERE ticker=? ORDER BY period_end DESC LIMIT 1""",
                (ticker,),
            ).fetchone()
            if r:
                result["period_end"] = r[0]
                result["pe"] = r[1]; result["pb"] = r[2]
                result["dy"] = r[3]; result["roe"] = r[4]
    except Exception:  # noqa: BLE001
        pass

    return result


def _refetch(ticker: str, market: str) -> bool:
    """Chama fetcher apropriado para refresh fundamentals."""
    cmd: list[str] | None = None
    if market == "us":
        cmd = [sys.executable, "-X", "utf8", str(ROOT / "fetchers" / "yf_deep_fundamentals.py"), ticker]
    elif market == "br":
        # brapi tem fundamentals anuais — usamos yf_deep como genérico se suportar .SA
        cmd = [sys.executable, "-X", "utf8", str(ROOT / "fetchers" / "yf_deep_fundamentals.py"), ticker]
    if not cmd:
        return False
    r = subprocess.call(cmd, timeout=180)
    return r == 0


def _persist_history(conn: sqlite3.Connection, ticker: str, snap: dict,
                     source_event: str) -> None:
    now = datetime.now(UTC).isoformat()
    conn.execute(
        """INSERT OR REPLACE INTO fundamentals_history
             (ticker, period_end, altman_z, altman_zone, piotroski_f, div_safety,
              screen_score, screen_passes, pe, pb, dy, roe, source_event, recorded_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (ticker, snap.get("period_end", now[:10]),
         snap.get("altman_z"), snap.get("altman_zone"),
         snap.get("piotroski_f"), snap.get("div_safety"),
         snap.get("screen_score"), snap.get("screen_passes"),
         snap.get("pe"), snap.get("pb"), snap.get("dy"), snap.get("roe"),
         source_event, now),
    )
    conn.commit()


def _check_drift(prev: tuple | None, now: dict) -> list[str]:
    if not prev:
        return []
    alerts = []
    prev_alt = prev[0]; prev_piot = prev[1]; prev_safe = prev[2]
    prev_scr = prev[3]; prev_pass = prev[4]
    if prev_alt is not None and now.get("altman_z") is not None:
        da = now["altman_z"] - prev_alt
        if da <= -0.5:
            alerts.append(f"Altman Δ {da:+.2f} (de {prev_alt:.2f} para {now['altman_z']:.2f})")
    if prev_piot is not None and now.get("piotroski_f") is not None:
        dp = now["piotroski_f"] - prev_piot
        if dp <= -1:
            alerts.append(f"Piotroski Δ {dp} (de {prev_piot} para {now['piotroski_f']}/9)")
    if prev_safe is not None and now.get("div_safety") is not None:
        ds = now["div_safety"] - prev_safe
        if ds <= -10:
            alerts.append(f"DivSafety Δ {ds:+.0f} (de {prev_safe:.0f} para {now['div_safety']:.0f})")
    if prev_pass is not None and now.get("screen_passes") is not None:
        if prev_pass == 1 and now["screen_passes"] == 0:
            alerts.append("screen perdeu PASS")
        elif prev_pass == 0 and now["screen_passes"] == 1:
            alerts.append("screen passou a PASS")
    return alerts


def react(ticker: str, market: str, dry_run: bool = False) -> dict:
    db_path = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db_path) as c:
        filing = _latest_filing(c, ticker)
        prev = _last_recorded_history(c, ticker)

    if not filing:
        return {"ticker": ticker, "status": "no_filing"}

    filing_date, filing_kind = filing
    filing_tag = f"{filing_kind}@{filing_date}"

    prev_event = prev[7] if prev else None
    if prev_event == filing_tag:
        return {"ticker": ticker, "status": "up_to_date", "filing": filing_tag}

    if dry_run:
        return {"ticker": ticker, "status": "would_refetch", "filing": filing_tag,
                "prev_event": prev_event}

    refetched = _refetch(ticker, market)
    snap = _recompute_quality(ticker, market)
    alerts = _check_drift(prev, snap)

    with sqlite3.connect(db_path) as c:
        _persist_history(c, ticker, snap, source_event=filing_tag)

    return {
        "ticker": ticker, "status": "refetched",
        "filing": filing_tag,
        "refetch_ok": refetched,
        "snapshot": snap,
        "drift_alerts": alerts,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    from scripts.init_db import init
    init(DB_BR); init(DB_US)

    if args.ticker:
        from scripts.refresh_ticker import _market_of
        tickers = [(args.ticker.upper(), _market_of(args.ticker.upper()))]
    else:
        tickers = []
        for market, db in (("br", DB_BR), ("us", DB_US)):
            with sqlite3.connect(db) as c:
                for (t,) in c.execute(
                    "SELECT DISTINCT ticker FROM portfolio_positions WHERE active=1"
                ):
                    tickers.append((t, market))

    drifts = []
    for t, mk in tickers:
        r = react(t, mk, dry_run=args.dry_run)
        status = r["status"]
        marker = ""
        if r.get("drift_alerts"):
            drifts.append((t, r["drift_alerts"]))
            marker = " 🚩 DRIFT"
        print(f"  {t:<8} {mk}  {status}  {r.get('filing','')}{marker}")

    if drifts:
        print("\n=== Drift alerts ===")
        for t, a in drifts:
            print(f"\n{t}:")
            for msg in a:
                print(f"  - {msg}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
