"""agent_morning — rotina autónoma matinal (cron 09:30).

Ordem:
  1. Refresh intraday holdings (yfinance)
  2. Snapshot diário MV (portfolio_snapshots)
  3. CVM/SEC monitors (events novos)
  4. earnings_react (detecta novos filings → refetch + quality drift)
  5. daily_update BR + US (scoring + triggers)
  6. Compute verdicts para holdings + write no vault
  7. Gerar morning_briefing → vault + reports
  8. obsidian_bridge --refresh --holdings-only (export full vault)
  9. Push resumo via Telegram (se .env configurado)

Log estruturado em logs/agent_morning_YYYY-MM-DD.log.

Uso:
    python scripts/agent_morning.py           # corre tudo
    python scripts/agent_morning.py --dry-run # não escreve/notifica
    python scripts/agent_morning.py --quick   # skip slow steps (verdicts, reextract)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def _py(*args: str) -> list[str]:
    return [sys.executable, "-X", "utf8", *args]


def _run(label: str, cmd: list[str], timeout: int = 600) -> dict:
    t0 = time.time()
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout,
        )
        dt = time.time() - t0
        return {
            "label": label, "rc": r.returncode, "dt": round(dt, 1),
            "stdout_tail": (r.stdout or "").splitlines()[-10:],
            "stderr_tail": (r.stderr or "").splitlines()[-5:],
        }
    except subprocess.TimeoutExpired:
        return {"label": label, "rc": -1, "dt": timeout, "error": "timeout"}
    except Exception as e:  # noqa: BLE001
        return {"label": label, "rc": -1, "dt": time.time() - t0, "error": str(e)}


def _log(log_path: Path, entry: dict) -> None:
    entry["ts"] = datetime.now(UTC).isoformat()
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")


def _telegram_summary(results: list[dict]) -> str:
    lines = [f"*Morning Briefing — {date.today().isoformat()}*", ""]
    total_dt = sum(r["dt"] for r in results)
    lines.append(f"⏱ Total: {total_dt:.0f}s")
    lines.append("")
    for r in results:
        icon = "✅" if r["rc"] == 0 else "⚠️"
        lines.append(f"{icon} {r['label']}  _{r['dt']:.0f}s_")
    return "\n".join(lines)


def run(dry_run: bool, quick: bool) -> int:
    today = date.today().isoformat()
    log_path = LOG_DIR / f"agent_morning_{today}.log"
    results: list[dict] = []

    def step(label: str, cmd: list[str], timeout: int = 600):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {label} ...", flush=True)
        if dry_run:
            print(f"  [DRY] {' '.join(cmd)}")
            results.append({"label": label, "rc": 0, "dt": 0, "dry": True})
            return
        r = _run(label, cmd, timeout=timeout)
        _log(log_path, r)
        icon = "✓" if r["rc"] == 0 else "✗"
        print(f"  {icon} {label} ({r['dt']:.1f}s)", flush=True)
        if r.get("stdout_tail"):
            for ln in r["stdout_tail"][-3:]:
                print(f"    {ln}")
        results.append(r)

    # 1. Refresh prices
    step("Refresh intraday", _py(str(ROOT / "scripts/refresh_ticker.py"), "--all-holdings", "--quiet"), 180)

    # 2. Snapshot MV
    step("Snapshot portfolio", _py(str(ROOT / "scripts/snapshot_portfolio.py")), 60)

    # 3. CVM/SEC monitors
    step("CVM monitor", _py(str(ROOT / "monitors/cvm_monitor.py")), 300)
    step("SEC monitor", _py(str(ROOT / "monitors/sec_monitor.py")), 300)

    # 4. earnings_react
    step("Earnings react", _py(str(ROOT / "scripts/earnings_react.py")), 600)

    # 5. daily_update (scoring + triggers)
    step("Trigger monitor", _py(str(ROOT / "scripts/trigger_monitor.py")), 180)

    # 6. Verdicts → vault (slow: skip em --quick)
    if not quick:
        step("Verdicts holdings", _py(str(ROOT / "scripts/verdict.py"), "--all-holdings", "--write"), 900)

    # 7. Morning briefing
    step("Morning briefing", _py(str(ROOT / "scripts/morning_briefing.py"), "--no-refresh"), 120)

    # 8. Obsidian bridge export
    step("Obsidian bridge export", _py(str(ROOT / "scripts/obsidian_bridge.py"), "--holdings-only"), 180)

    # 9. Telegram push
    if not dry_run:
        try:
            from notifiers.telegram import send, send_document
            summary = _telegram_summary(results)
            r = send(summary)
            _log(log_path, {"label": "telegram_summary", "result": r})
            briefing = ROOT / "reports" / f"briefing_{today}.md"
            if briefing.exists():
                r2 = send_document(str(briefing), caption=f"Briefing {today}")
                _log(log_path, {"label": "telegram_briefing", "result": r2})
            print(f"\n[telegram] summary sent: {r.get('ok', False)}")
        except Exception as e:  # noqa: BLE001
            print(f"\n[telegram] skip ({e})")

    # Summary
    total_dt = sum(r["dt"] for r in results)
    failed = [r for r in results if r["rc"] != 0]
    print(f"\n=== agent_morning done in {total_dt:.0f}s — {len(results)} steps, {len(failed)} failed ===")
    for r in failed:
        err = r.get("error") or f"rc={r['rc']}"
        print(f"  ✗ {r['label']}: {err}")
    return 0 if not failed else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quick", action="store_true", help="Skip verdicts (poupa ~10min)")
    args = ap.parse_args()
    return run(args.dry_run, args.quick)


if __name__ == "__main__":
    sys.exit(main())
