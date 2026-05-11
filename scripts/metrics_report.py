"""Daily metrics report — Phase W tracking.

Run daily (cron) após daily_update + perpetuum_validator. Captura snapshot
e escreve em data/metrics_history table + markdown diff no vault.

Uso:
    python scripts/metrics_report.py             # run + persist
    python scripts/metrics_report.py --compare   # show diff vs baseline
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metrics_baseline import collect  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BR_DB = ROOT / "data" / "br_investments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS metrics_history (
    run_date TEXT PRIMARY KEY,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def _load_baseline() -> dict | None:
    candidates = sorted(ROOT.glob("data/metrics_baseline_*.json"))
    if not candidates:
        return None
    return json.loads(candidates[0].read_text(encoding="utf-8"))


def _ensure_table() -> None:
    with sqlite3.connect(BR_DB) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def _persist(snapshot: dict) -> None:
    _ensure_table()
    with sqlite3.connect(BR_DB) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO metrics_history (run_date, payload_json, created_at) VALUES (?, ?, ?)",
            (snapshot["baseline_date"], json.dumps(snapshot, ensure_ascii=False), datetime.utcnow().isoformat()),
        )
        conn.commit()


def _diff(baseline: dict, current: dict) -> list[tuple[str, object, object]]:
    rows = []
    for key in sorted(set(baseline) | set(current)):
        if key in ("baseline_date", "baseline_label"):
            continue
        b = baseline.get(key, "-")
        c = current.get(key, "-")
        if b != c:
            rows.append((key, b, c))
    return rows


def _write_markdown_report(baseline: dict, current: dict) -> Path:
    diff = _diff(baseline, current)
    out = ROOT / "obsidian_vault" / "briefings" / f"metrics_{current['baseline_date']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "type: metrics_daily",
        f"date: {current['baseline_date']}",
        "tags: [metrics, phase_w, daily]",
        "---",
        "",
        f"# Phase W Metrics — {current['baseline_date']}",
        "",
        f"Baseline: {baseline['baseline_date']} ({baseline['baseline_label']})",
        "",
        "## Deltas vs baseline",
        "",
        "| Metric | Baseline | Now | Delta |",
        "|---|---|---|---|",
    ]
    for key, b, c in diff:
        try:
            delta = c - b if isinstance(b, (int, float)) and isinstance(c, (int, float)) else "—"
            dstr = f"+{delta}" if isinstance(delta, (int, float)) and delta > 0 else str(delta)
        except TypeError:
            dstr = "—"
        lines.append(f"| `{key}` | {b} | {c} | {dstr} |")
    if not diff:
        lines.append("| _(no changes)_ | — | — | — |")
    lines.append("")
    lines.append(f"## Current snapshot")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(current, indent=2, ensure_ascii=False))
    lines.append("```")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--compare", action="store_true", help="Print delta table vs baseline.")
    ap.add_argument("--no-persist", action="store_true", help="Skip DB write.")
    args = ap.parse_args()

    current = collect()
    baseline = _load_baseline()
    if not baseline:
        print("ERROR: no baseline file found. Run: python scripts/metrics_baseline.py --freeze")
        return

    if not args.no_persist:
        _persist(current)
    report_path = _write_markdown_report(baseline, current)

    if args.compare:
        diff = _diff(baseline, current)
        print(f"Deltas vs baseline ({baseline['baseline_date']}):")
        for key, b, c in diff:
            print(f"  {key:<35} {b} -> {c}")
        if not diff:
            print("  (no changes yet)")

    print(f"\nReport written: {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
