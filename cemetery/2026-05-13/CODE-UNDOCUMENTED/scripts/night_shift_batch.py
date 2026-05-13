"""Night shift batch — STORYT_3.0 across all holdings.

Runs `agents.council.story` on each active position. Smart cache means
subsequent runs are fast; first run for each ticker is full pipeline (~100s).

Logs to logs/night_shift_YYYY-MM-DD.log with structured per-ticker entries.
Output: night shift report at obsidian_vault/Bibliotheca/Night_Shift_<DATE>.md
"""
from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def list_holdings(market: str) -> list[tuple[str, str, str]]:
    """Returns [(ticker, sector, name), ...] for active positions."""
    db = ROOT / "data" / f"{market}_investments.db"
    if not db.exists():
        return []
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT p.ticker, c.sector, c.name
            FROM portfolio_positions p
            LEFT JOIN companies c ON c.ticker = p.ticker
            WHERE p.active = 1
            ORDER BY p.ticker
        """).fetchall()
    return [(r["ticker"], r["sector"] or "?", r["name"] or "?") for r in rows]


def run_single(ticker: str, market: str, *, timeout: int = 600) -> dict:
    """Run agents.council.story on one ticker. Returns metadata dict."""
    t0 = time.time()
    log_path = LOG_DIR / f"night_shift_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}_{ticker}.log"
    try:
        r = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "agents.council.story", ticker, "--market", market, "--quiet"],
            capture_output=True, text=True, timeout=timeout, cwd=str(ROOT),
            encoding="utf-8", errors="replace",
        )
        elapsed = time.time() - t0
        log_path.write_text(
            f"# {ticker} ({market}) — {datetime.now(timezone.utc).isoformat()}\n"
            f"# Exit code: {r.returncode}\n"
            f"# Elapsed: {elapsed:.1f}s\n\n"
            f"## stdout\n{r.stdout}\n\n## stderr\n{r.stderr}",
            encoding="utf-8",
        )
        # Parse the JSON snapshot to get key results
        snapshot_path = ROOT / "data" / "dossier_snapshots" / ticker
        latest_json = None
        if snapshot_path.exists():
            jsons = sorted(snapshot_path.glob("*.json"), reverse=True)
            if jsons:
                try:
                    latest_json = json.loads(jsons[0].read_text(encoding="utf-8"))
                except Exception:
                    pass
        return {
            "ticker": ticker,
            "market": market,
            "exit_code": r.returncode,
            "elapsed_sec": elapsed,
            "snapshot": latest_json,
            "stderr_preview": r.stderr[-500:] if r.stderr else "",
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        log_path.write_text(f"# {ticker} TIMEOUT after {elapsed:.0f}s", encoding="utf-8")
        return {
            "ticker": ticker, "market": market, "exit_code": -1,
            "elapsed_sec": elapsed, "error": "timeout",
        }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "ticker": ticker, "market": market, "exit_code": -2,
            "elapsed_sec": elapsed, "error": f"{type(e).__name__}: {e}",
        }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

    # Skip configuration
    SKIP_TICKERS = {
        # ETFs/RF — council fit is poor for these
        "LFTB11", "IVVB11", "GREK",
    }

    holdings: list[tuple[str, str, str]] = []
    for market in ("br", "us"):
        for ticker, sector, name in list_holdings(market):
            if ticker in SKIP_TICKERS:
                print(f"  [skip] {ticker} (in SKIP_TICKERS)")
                continue
            holdings.append((market, ticker, sector, name))

    print(f"\n=== Night Shift Batch — {len(holdings)} tickers ===")
    print(f"Estimated time: ~{len(holdings) * 100 // 60} minutes (full runs)")
    print(f"Smart cache will skip unchanged after first night.")
    print()

    results: list[dict] = []
    overall_t0 = time.time()
    progress_path = ROOT / "logs" / f"night_shift_progress_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"

    for i, (market, ticker, sector, name) in enumerate(holdings, 1):
        elapsed_total = time.time() - overall_t0
        eta_min = (len(holdings) - i + 1) * 100 / 60
        print(f"[{i}/{len(holdings)}] {market.upper()}:{ticker} ({sector}) — total {elapsed_total/60:.1f}min, ETA ~{eta_min:.1f}min...")
        result = run_single(ticker, market, timeout=600)
        results.append(result)

        # Append progress file (resilient to crash)
        with progress_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False, default=str) + "\n")

        # Inline summary
        ec = result.get("exit_code")
        elapsed = result.get("elapsed_sec", 0)
        snap = result.get("snapshot") or {}
        stance = snap.get("council_stance", "?")
        conf = snap.get("council_confidence", "?")
        flags = len(snap.get("pre_publication_flags") or [])
        seats = len(snap.get("council_seats") or [])
        print(f"   → exit={ec} {elapsed:.0f}s  stance={stance}({conf})  seats={seats}  flags={flags}")

    overall_elapsed = time.time() - overall_t0
    print(f"\n=== Done. Total {overall_elapsed/60:.1f} minutes for {len(holdings)} tickers ===")

    # Write final results JSON
    final_path = ROOT / "logs" / f"night_shift_final_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.json"
    final_path.write_text(
        json.dumps({
            "run_at": datetime.now(timezone.utc).isoformat(),
            "total_tickers": len(holdings),
            "elapsed_total_sec": overall_elapsed,
            "results": results,
        }, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(f"Final results: {final_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
