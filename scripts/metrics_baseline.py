"""Metrics baseline — freeze state 'before Phase W Gold'.

Run once: `python scripts/metrics_baseline.py --freeze`
Output: data/metrics_baseline_YYYY-MM-DD.json

Fields captured: data sources, MCP integrations, agents, tests, vault stats,
deliverables, cost tracking readiness.

Run without --freeze to just preview numbers without writing baseline.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def count_files(pattern: str, base: Path | None = None) -> int:
    base = base or ROOT
    return sum(1 for _ in base.glob(pattern))


def count_grep(pattern: str, glob: str) -> int:
    hits = 0
    for f in ROOT.glob(glob):
        if f.is_file():
            try:
                if pattern in f.read_text(encoding="utf-8", errors="ignore"):
                    hits += 1
            except Exception:
                pass
    return hits


def count_db_rows(db: Path, table: str, where: str = "1=1") -> int:
    if not db.exists():
        return 0
    try:
        with sqlite3.connect(db) as conn:
            return conn.execute(f"SELECT COUNT(*) FROM {table} WHERE {where}").fetchone()[0]
    except Exception:
        return 0


def collect() -> dict:
    br = ROOT / "data" / "br_investments.db"
    us = ROOT / "data" / "us_investments.db"

    return {
        "baseline_date": date.today().isoformat(),
        "baseline_label": "before_phase_w_gold",
        # Data sources
        "fetchers": count_files("fetchers/*.py") - 2,  # minus _base, __init__
        "subscriptions": count_files("fetchers/subscriptions/*.py") - 3,  # minus helpers
        # Agents
        "agents_count": count_files("agents/*.py") - 9,  # exclude _underscore helpers
        "agents_with_tests": 0,  # target: all
        # Vault
        "vault_wiki_notes": count_files("obsidian_vault/wiki/**/*.md"),
        "vault_ticker_notes": count_files("obsidian_vault/tickers/*.md"),
        "vault_skills_notes": count_files("obsidian_vault/skills/*.md"),
        "vault_tickers_with_thesis": count_grep("## Thesis", "obsidian_vault/tickers/*.md"),
        # Scripts
        "scripts_count": count_files("scripts/*.py"),
        # Portfolio
        "br_holdings": count_db_rows(br, "portfolio_positions", "active=1"),
        "us_holdings": count_db_rows(us, "portfolio_positions", "active=1"),
        # Thesis health (should be 0 pre-perpetuum)
        "br_thesis_health_rows": count_db_rows(br, "thesis_health"),
        "us_thesis_health_rows": count_db_rows(us, "thesis_health"),
        # Deliverables
        "reports_md_count": count_files("reports/*.md"),
        "reports_pptx_count": count_files("reports/*.pptx"),
        "reports_videos_count": count_files("reports/videos/*.mp4"),
        # Skills (Phase W)
        "user_skills_installed": count_files("*/SKILL.md", base=Path.home() / ".claude" / "skills") if (Path.home() / ".claude" / "skills").exists() else 0,
        "project_skills_installed": count_files(".claude/skills/*/SKILL.md"),
        # Observability
        "langfuse_configured": (ROOT / ".langfuse").exists(),
        "promptfoo_configured": (ROOT / "promptfooconfig.yaml").exists(),
        # MCPs
        "mcp_json_exists": (ROOT / ".claude" / "mcp.json").exists(),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--freeze", action="store_true", help="Write baseline JSON to disk.")
    args = ap.parse_args()

    data = collect()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    if args.freeze:
        out = ROOT / "data" / f"metrics_baseline_{data['baseline_date']}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nBaseline frozen: {out}")
    else:
        print("\n(preview only -- pass --freeze to persist)")


if __name__ == "__main__":
    main()
