"""auto_verdict_on_filing — re-compute verdict + write filing dossier for
tickers that just got a new filing.

Pattern: hook called after `cvm_monitor` / `sec_monitor` finishes inserting
events. Determines which tickers have *new* events since the last run (by
`events.id` watermark stored in `auto_verdict_state` table), then for each:

  1. Re-records the verdict via `scripts.verdict_history.record_verdict(replace=True)`
  2. Refreshes data_confidence label (yfinance vs CVM cross-check, BR only)
  3. Re-computes fair_value (consensus + our_fair triplet) and persists with
     trigger="filing:<source>:<kind>:<event_date>" — full history preserved
  4. Computes quarter_delta narrative if quarterly_single has fresh data
  5. Writes `obsidian_vault/dossiers/<TK>_FILING_<event_date>.md` bundling
     prior→new fair value triplet + delta narrative + action emit

Persists:
  - `verdict_history` row (today, replace if exists)
  - `verdict_delta` row (prior_action, new_action, trigger, url)
  - `fair_value` row (append-only history)
  - `data_confidence` row
  - dossier markdown file

Idempotent (watermark-driven for events; dossier overwrites same-day file).
Safe to call from cron.

Uso:
    python scripts/auto_verdict_on_filing.py             # default: last 24h of events
    python scripts/auto_verdict_on_filing.py --since-id  # use watermark
    python scripts/auto_verdict_on_filing.py --hours 48
    python scripts/auto_verdict_on_filing.py --ticker ITSA4
    python scripts/auto_verdict_on_filing.py --dry-run
    python scripts/auto_verdict_on_filing.py --dossier BBDC4   # ad-hoc dossier (no event needed)
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


DOSSIER_DIR = ROOT / "obsidian_vault" / "dossiers"


def _refresh_confidence(market: str, ticker: str) -> dict | None:
    """Idempotent: compute + persist fresh confidence row, return latest."""
    try:
        from analytics.data_confidence import evaluate, persist as persist_conf
        row = evaluate(ticker, market)
        persist_conf(row)
        return row
    except Exception as e:  # noqa: BLE001
        return {"label": "single_source", "score": None,
                "detail": {"reason": f"data_confidence_failed: {e}"}}


def _refresh_fair_value(market: str, ticker: str, trigger: str) -> dict | None:
    """Compute + persist fair_value with the filing trigger context."""
    try:
        from scoring.fair_value import compute as fv_compute, persist as fv_persist
        r = fv_compute(ticker, market)
        if r is None:
            return None
        fv_persist(r, trigger=trigger)
        return r
    except Exception as e:  # noqa: BLE001
        return {"_error": str(e)}


def _fair_value_history(market: str, ticker: str, *, limit: int = 5) -> list[dict]:
    try:
        from scoring.fair_value import history as fv_history
        return fv_history(ticker, market, limit=limit)
    except Exception:
        return []


def _quarter_delta(market: str, ticker: str) -> tuple[dict | None, str]:
    try:
        from analytics.quarter_delta import compute as qd_compute, render_narrative
        d = qd_compute(ticker, market)
        if d is None:
            return None, "_(sem deltas — fonte ausente: BR precisa quarterly_single, US ainda não wired)_"
        return d, render_narrative(d)
    except Exception as e:  # noqa: BLE001
        return None, f"_(quarter_delta error: {e})_"


def write_filing_dossier(*, market: str, ticker: str, event: dict | None,
                         dry_run: bool = False) -> Path | None:
    """Compose + write `obsidian_vault/dossiers/<TK>_FILING_<DATE>.md`.

    `event` may be None for ad-hoc dossier (uses today's date + 'manual' trigger).
    Returns path of written file, or None if dry_run / write failed.
    """
    DOSSIER_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    if event:
        ev_date = event.get("event_date") or today
        ev_kind = f"{event.get('source', '?')}:{event.get('kind', '?')}"
        trigger = f"filing:{ev_kind}:{ev_date}"
        ev_url = event.get("url")
    else:
        ev_date = today
        ev_kind = "manual"
        trigger = "manual:dossier"
        ev_url = None

    # Run all the engines (idempotent, persist anyway)
    confidence = _refresh_confidence(market, ticker)
    fv_now = _refresh_fair_value(market, ticker, trigger=trigger)
    fv_hist = _fair_value_history(market, ticker, limit=8)
    qd, qd_narrative = _quarter_delta(market, ticker)

    # Compose dossier content
    lines: list[str] = []
    lines.append("---")
    lines.append("type: filing_dossier")
    lines.append(f"ticker: {ticker}")
    lines.append(f"market: {market}")
    lines.append(f"event_date: {ev_date}")
    lines.append(f"event_kind: {ev_kind}")
    if fv_now and fv_now.get("action"):
        lines.append(f"action: {fv_now['action']}")
    if confidence and confidence.get("label"):
        lines.append(f"confidence: {confidence['label']}")
    lines.append(f"computed_at: {datetime.now(UTC).isoformat(timespec='seconds')}")
    lines.append(f"tags: [filing, fair_value, dossier]")
    lines.append("---")
    lines.append("")
    lines.append(f"# Filing dossier — [[{ticker}]] · {ev_date}")
    lines.append("")
    lines.append(f"**Trigger**: `{ev_kind}` no dia `{ev_date}`")
    if ev_url:
        lines.append(f"**Filing URL**: <{ev_url}>")
    lines.append("")

    # 1. Action + fair value triplet
    lines.append("## 🎯 Acção sugerida")
    lines.append("")
    if fv_now and "_error" not in fv_now and fv_now.get("action"):
        act = fv_now["action"]
        emoji = {"STRONG_BUY": "🟢🟢", "BUY": "🟢", "HOLD": "🟡",
                 "TRIM": "🟠", "SELL": "🔴", "N/A": "⚪"}.get(act, "·")
        lines.append(f"### {emoji} **{act}** &mdash; preço {fv_now['current_price']:.2f}")
        lines.append("")
        if fv_now.get("our_fair") is not None:
            lines.append("| Banda | Preço |")
            lines.append("|---|---|")
            lines.append(f"| **BUY abaixo de** (our_fair, {fv_now['margin_pct']:.0f}% margem) | "
                         f"`{fv_now['buy_below']:.2f}` |")
            lines.append(f"| HOLD entre | `{fv_now['hold_low']:.2f}` — `{fv_now['hold_high']:.2f}` (consensus) |")
            lines.append(f"| TRIM entre | `{fv_now['hold_high']:.2f}` — `{fv_now['sell_above']:.2f}` |")
            lines.append(f"| **SELL acima de** | `{fv_now['sell_above']:.2f}` |")
            lines.append("")
            lines.append(f"_Método: `{fv_now['method']}`. Consensus fair = "
                         f"R${fv_now['fair_price']:.2f}. Our fair (mais conservador) = "
                         f"R${fv_now['our_fair']:.2f}._")
        else:
            lines.append(f"_Método `{fv_now['method']}`: fair value emitido como N/A "
                         "(sector opt-out via `safety_margins.yaml`)._")
    elif fv_now and "_error" in fv_now:
        lines.append(f"_❌ Fair value engine error: `{fv_now['_error']}`_")
    else:
        lines.append("_Fair value engine devolveu None — fundamentals insuficientes._")
    lines.append("")

    # 2. Confidence label
    lines.append("## 🔍 Confidence")
    lines.append("")
    if confidence:
        label = confidence.get("label", "?")
        score = confidence.get("score")
        score_s = f"score={score:.2f}" if isinstance(score, (int, float)) else "score=—"
        emoji = {"cross_validated": "✅", "single_source": "⚠️",
                 "disputed": "❌"}.get(label, "·")
        lines.append(f"{emoji} **{label}** ({score_s})")
        d = confidence.get("detail") or {}
        if d.get("roe_delta") is not None or d.get("eps_delta") is not None:
            lines.append("")
            lines.append("| Métrica | yfinance | CVM derivada | Δ |")
            lines.append("|---|---|---|---|")
            if d.get("roe_yf") is not None or d.get("roe_cvm") is not None:
                lines.append(f"| ROE | `{d.get('roe_yf')}` | `{d.get('roe_cvm')}` | "
                             f"{(d.get('roe_delta') or 0)*100:+.1f}% |")
            if d.get("eps_yf") is not None or d.get("eps_cvm") is not None:
                lines.append(f"| EPS | `{d.get('eps_yf')}` | `{d.get('eps_cvm')}` | "
                             f"{(d.get('eps_delta') or 0)*100:+.1f}% |")
            lines.append("")
            if label == "disputed":
                lines.append("> ⚠️ **Methodology gap detected** — fair value emitido a partir "
                             "de yfinance pode não bater com CVM oficial. Tipicamente: "
                             "consolidação minority interest (bancos/holdings) ou one-off "
                             "items (cyclicals). Reler antes de mover capital.")
        elif d.get("reason"):
            lines.append(f"_({d['reason']})_")
    lines.append("")

    # 3. Quarter delta
    lines.append("## 📊 Quarter delta")
    lines.append("")
    lines.append(qd_narrative)
    lines.append("")

    # 4. Fair value history
    lines.append("## 📈 Fair value history (últimas runs)")
    lines.append("")
    if fv_hist:
        lines.append("| computed_at | método | consensus | our_fair | preço | acção | confidence | trigger |")
        lines.append("|---|---|---|---|---|---|---|---|")
        # Most recent first
        for h in reversed(fv_hist):
            our = f"{h['our_fair']:.2f}" if h.get('our_fair') is not None else "—"
            lines.append(
                f"| {h['computed_at']} | `{h['method']}` | "
                f"{h['fair_price']:.2f} | {our} | {h['current_price']:.2f} | "
                f"{h.get('action') or '—'} | {h.get('confidence_label') or '—'} | "
                f"`{h.get('trigger') or '—'}` |"
            )
    else:
        lines.append("_(sem histórico — primeira run)_")
    lines.append("")

    # 5. Footer
    lines.append("---")
    lines.append("")
    lines.append("_Auto-gerado por `scripts/auto_verdict_on_filing.py::write_filing_dossier`. "
                 "Engines: `analytics.data_confidence`, `analytics.quarter_delta`, "
                 "`scoring.fair_value` (com `scoring._safety` per-sector margins)._")

    out_path = DOSSIER_DIR / f"{ticker}_FILING_{ev_date}.md"
    if dry_run:
        print(f"  [dry] would write {out_path.relative_to(ROOT).as_posix()}")
        return None
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


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
                # NEW: write the filing dossier (fair value triplet + delta narrative)
                dossier_path = write_filing_dossier(market=market, ticker=tk,
                                                    event=ev, dry_run=False)
                dossier_str = f" dossier={dossier_path.name}" if dossier_path else ""
                market_log.append(
                    f"  {market.upper()} {tk:<8} {prior_action or 'N/A':<5} {arrow} "
                    f"{new_action:<5} score={new_score:.1f} (trig {triggered_by}){dossier_str}"
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


def _market_for(ticker: str) -> str | None:
    for m, db in (("br", DB_BR), ("us", DB_US)):
        with sqlite3.connect(db) as c:
            if c.execute("SELECT 1 FROM companies WHERE ticker=?", (ticker,)).fetchone():
                return m
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--since-id", action="store_true",
                    help="use stored watermark instead of --hours window")
    ap.add_argument("--ticker", default=None, help="restringir a 1 ticker")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dossier", default=None, metavar="TICKER",
                    help="write ad-hoc filing dossier para TICKER e sai (sem watermark / events)")
    args = ap.parse_args()

    if args.dossier:
        tk = args.dossier.upper()
        market = _market_for(tk)
        if not market:
            print(f"{tk}: not found in either DB")
            return 1
        path = write_filing_dossier(market=market, ticker=tk, event=None,
                                    dry_run=args.dry_run)
        if path:
            print(f"[OK] wrote {path.relative_to(ROOT).as_posix()}")
        return 0

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
