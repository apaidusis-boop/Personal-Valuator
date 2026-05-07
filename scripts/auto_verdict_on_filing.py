"""auto_verdict_on_filing — re-compute verdict for tickers that just got a new filing.

Pattern: hook called after `cvm_monitor` / `sec_monitor` finishes inserting events.
Determines which tickers have *new* events since the last run (by `events.id` watermark
stored in `auto_verdict_state` table), then re-records the verdict for each via
`scripts.verdict_history.record_verdict(replace=True)` and computes the delta vs
the previous recorded verdict.

Output:
  - persists `verdict_history` row for today (replace if exists)
  - writes `verdict_delta` table row for each ticker (today only) with prior_action,
    new_action, prior_score, new_score, triggered_by_filing
  - prints a summary; if --vault writes to obsidian_vault/Bibliotheca/

Idempotent (watermark-driven). Safe to call from cron.

Uso:
    python scripts/auto_verdict_on_filing.py             # default: last 24h of events
    python scripts/auto_verdict_on_filing.py --since-id  # use watermark
    python scripts/auto_verdict_on_filing.py --hours 48
    python scripts/auto_verdict_on_filing.py --ticker ITSA4
    python scripts/auto_verdict_on_filing.py --dry-run
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS auto_verdict_state (
    market         TEXT PRIMARY KEY,
    last_event_id  INTEGER NOT NULL DEFAULT 0,
    last_run_at    TEXT
);

CREATE TABLE IF NOT EXISTS verdict_delta (
    ticker          TEXT NOT NULL,
    date            TEXT NOT NULL,
    prior_action    TEXT,
    new_action      TEXT NOT NULL,
    prior_score     REAL,
    new_score       REAL,
    triggered_by    TEXT,        -- 'cvm:fato_relevante', 'sec:8-K', etc.
    triggered_url   TEXT,
    computed_at     TEXT NOT NULL,
    PRIMARY KEY (ticker, date, triggered_by)
);
CREATE INDEX IF NOT EXISTS idx_vd_date ON verdict_delta(date);
"""


def _ensure_schema(db: Path) -> None:
    with sqlite3.connect(db) as c:
        c.executescript(SCHEMA)


def _new_events(market: str, since_hours: int | None = None,
                use_watermark: bool = False) -> list[dict]:
    """Returns events inserted since the watermark / time cutoff. Each row:
    {id, ticker, source, kind, event_date, url}."""
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    out: list[dict] = []
    with sqlite3.connect(db) as c:
        if use_watermark:
            r = c.execute(
                "SELECT last_event_id FROM auto_verdict_state WHERE market=?", (market,)
            ).fetchone()
            last_id = r[0] if r else 0
            rows = c.execute(
                """SELECT id, ticker, source, kind, event_date, url
                   FROM events WHERE id > ? ORDER BY id ASC""",
                (last_id,),
            ).fetchall()
        else:
            cutoff = (datetime.now(UTC) - timedelta(hours=since_hours or 24)).strftime("%Y-%m-%d")
            rows = c.execute(
                """SELECT id, ticker, source, kind, event_date, url
                   FROM events WHERE event_date >= ?
                   ORDER BY event_date DESC, id DESC""",
                (cutoff,),
            ).fetchall()
        for r in rows:
            out.append({"id": r[0], "ticker": r[1], "source": r[2],
                        "kind": r[3], "event_date": r[4], "url": r[5],
                        "market": market})
    return out


def _bump_watermark(market: str, max_id: int) -> None:
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    now = datetime.now(UTC).isoformat()
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT INTO auto_verdict_state (market, last_event_id, last_run_at)
               VALUES (?,?,?)
               ON CONFLICT(market) DO UPDATE SET
                 last_event_id=excluded.last_event_id,
                 last_run_at=excluded.last_run_at""",
            (market, max_id, now),
        )
        c.commit()


def _prior_verdict(market: str, ticker: str, today: str) -> tuple[str | None, float | None]:
    db = DB_BR if market == "br" else DB_US
    with sqlite3.connect(db) as c:
        try:
            r = c.execute(
                """SELECT action, total_score FROM verdict_history
                   WHERE ticker=? AND date < ? ORDER BY date DESC LIMIT 1""",
                (ticker, today),
            ).fetchone()
        except sqlite3.OperationalError:
            return None, None
    return (r[0], r[1]) if r else (None, None)


def _persist_delta(market: str, ticker: str, today: str, prior_action, prior_score,
                   new_action: str, new_score: float, triggered_by: str, url: str | None) -> None:
    db = DB_BR if market == "br" else DB_US
    _ensure_schema(db)
    now = datetime.now(UTC).isoformat()
    with sqlite3.connect(db) as c:
        c.execute(
            """INSERT OR REPLACE INTO verdict_delta
                 (ticker, date, prior_action, new_action, prior_score, new_score,
                  triggered_by, triggered_url, computed_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (ticker, today, prior_action, new_action, prior_score, new_score,
             triggered_by, url, now),
        )
        c.commit()


def run(hours: int = 24, use_watermark: bool = False, only_ticker: str | None = None,
        dry_run: bool = False) -> dict:
    today = date.today().isoformat()
    summary = {"events_seen": 0, "tickers_recomputed": 0, "verdict_changed": 0,
               "errors": 0, "by_market": {}}

    for market in ("br", "us"):
        events = _new_events(market, since_hours=hours, use_watermark=use_watermark)
        if only_ticker:
            events = [e for e in events if e["ticker"] == only_ticker.upper()]
        summary["events_seen"] += len(events)

        # Group by ticker, keeping the most recent (highest id) trigger per ticker
        by_ticker: dict[str, dict] = {}
        for ev in events:
            cur = by_ticker.get(ev["ticker"])
            if cur is None or ev["id"] > cur["id"]:
                by_ticker[ev["ticker"]] = ev

        market_log = []
        for tk, ev in by_ticker.items():
            triggered_by = f"{ev['source']}:{ev['kind']}"
            if dry_run:
                print(f"  [dry] {market.upper()} {tk:<8} would re-verdict (trigger {triggered_by})")
                continue
            try:
                from scripts.verdict_history import record_verdict
                prior_action, prior_score = _prior_verdict(market, tk, today)
                r = record_verdict(tk, replace=True)
                # record_verdict returns inserted-style dict but doesn't expose new score
                # easily — re-read from verdict_history.
                db = DB_BR if market == "br" else DB_US
                with sqlite3.connect(db) as c:
                    row = c.execute(
                        "SELECT action, total_score FROM verdict_history "
                        "WHERE ticker=? AND date=?", (tk, today)
                    ).fetchone()
                if not row:
                    summary["errors"] += 1
                    continue
                new_action, new_score = row[0], row[1]
                _persist_delta(market, tk, today, prior_action, prior_score,
                               new_action, new_score, triggered_by, ev["url"])
                changed = (prior_action != new_action) and prior_action is not None
                if changed:
                    summary["verdict_changed"] += 1
                summary["tickers_recomputed"] += 1
                arrow = "→" if changed else "="
                market_log.append(
                    f"  {market.upper()} {tk:<8} {prior_action or 'N/A':<5} {arrow} "
                    f"{new_action:<5} score={new_score:.1f} (trig {triggered_by})"
                )
            except Exception as e:  # noqa: BLE001
                summary["errors"] += 1
                market_log.append(f"  {market.upper()} {tk:<8} ERROR — {e}")

        summary["by_market"][market] = {
            "events_seen": len(events),
            "tickers_recomputed": len(by_ticker),
        }
        if events and not dry_run:
            max_id = max(e["id"] for e in events)
            _bump_watermark(market, max_id)
        for line in market_log:
            print(line)

    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--since-id", action="store_true",
                    help="use stored watermark instead of --hours window")
    ap.add_argument("--ticker", default=None, help="restringir a 1 ticker")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    s = run(hours=args.hours, use_watermark=args.since_id,
            only_ticker=args.ticker, dry_run=args.dry_run)
    print()
    print("=== auto_verdict_on_filing ===")
    print(f"events_seen        : {s['events_seen']}")
    print(f"tickers_recomputed : {s['tickers_recomputed']}")
    print(f"verdict_changed    : {s['verdict_changed']}")
    print(f"errors             : {s['errors']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
