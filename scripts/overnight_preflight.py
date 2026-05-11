"""Pre-flight check before overnight orchestrator runs.

Validates all dependencies, cleans stale state, prints go/no-go.
"""
from __future__ import annotations

import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = str(ROOT / ".venv" / "Scripts" / "python.exe")


def check(name: str, ok: bool, detail: str = "") -> bool:
    icon = "✅" if ok else "❌"
    msg = f"{icon} {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return ok


def main() -> int:
    print("=" * 60)
    print("OVERNIGHT PRE-FLIGHT CHECK")
    print("=" * 60)
    all_ok = True

    # 1. Required scripts exist
    for path in [
        "scripts/ri_url_resolver.py",
        "scripts/pilot_deep_dive.py",
        "scripts/overnight_orchestrator.py",
        "scripts/overnight_code_health.py",
        "fetchers/portal_playwright.py",
        "library/_md_extract.py",
    ]:
        all_ok &= check(f"file: {path}", (ROOT / path).exists())

    # 2. .venv has required libs
    libs = ["playwright", "markitdown", "pdfplumber", "yaml", "requests"]
    for lib in libs:
        try:
            r = subprocess.run([PYTHON, "-c", f"import {lib}"],
                                capture_output=True, timeout=10)
            all_ok &= check(f"lib: {lib}", r.returncode == 0)
        except Exception as e:
            all_ok &= check(f"lib: {lib}", False, str(e)[:60])

    # 3. ri_urls.yaml exists & has content
    yaml_path = ROOT / "config" / "ri_urls.yaml"
    if yaml_path.exists():
        size = yaml_path.stat().st_size
        all_ok &= check("config/ri_urls.yaml", size > 100,
                         f"{size} bytes")
    else:
        all_ok &= check("config/ri_urls.yaml", False, "missing")

    # 4. DB readable
    for db in ["data/br_investments.db", "data/us_investments.db"]:
        try:
            c = sqlite3.connect(ROOT / db)
            n = c.execute(
                "SELECT COUNT(*) FROM companies WHERE is_holding=1"
            ).fetchone()[0]
            c.close()
            all_ok &= check(f"db: {db}", True, f"{n} holdings")
        except Exception as e:
            all_ok &= check(f"db: {db}", False, str(e)[:60])

    # 5. Output dir writable
    out_dir = ROOT / "obsidian_vault" / "Overnight_2026-05-11"
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        test = out_dir / ".write_test"
        test.write_text("ok")
        test.unlink()
        all_ok &= check(f"out dir: {out_dir.relative_to(ROOT)}", True,
                         "writable")
    except Exception as e:
        all_ok &= check(f"out dir", False, str(e)[:60])

    # 6. Playwright chromium installed
    try:
        r = subprocess.run([
            PYTHON, "-c",
            "from playwright.sync_api import sync_playwright; "
            "p=sync_playwright().start(); "
            "b=p.chromium.launch(); b.close(); p.stop(); print('ok')"
        ], capture_output=True, timeout=30, text=True)
        ok = r.returncode == 0 and "ok" in (r.stdout or "")
        all_ok &= check("playwright chromium", ok,
                         (r.stderr or "")[:80] if not ok else "launches")
    except Exception as e:
        all_ok &= check("playwright chromium", False, str(e)[:60])

    print("=" * 60)
    print(f"OVERALL: {'✅ READY' if all_ok else '❌ NOT READY'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
