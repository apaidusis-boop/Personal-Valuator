"""Morning helper — re-scrape ITSA4 to catch 1T26 release on 2026-05-11.

Usage:
    .venv\\Scripts\\python.exe scripts/morning_itsa4_check.py

Output: appended to obsidian_vault/Overnight_2026-05-11/ITSA4.md (or new
file if missing). Quick check vs prior scrape.
"""
from __future__ import annotations

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = str(ROOT / ".venv" / "Scripts" / "python.exe")
TODAY = datetime.now().strftime("%Y-%m-%d")
OUT_DIR = ROOT / "obsidian_vault" / f"Overnight_{TODAY}"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[{datetime.now()}] Re-scraping ITSA4 RI for 1T26 release...")
    cmd = [
        PYTHON,
        str(ROOT / "scripts" / "pilot_deep_dive.py"),
        "--tickers", "ITSA4",
        "--force-fresh",
        "--deep",
    ]
    import os
    env = os.environ.copy()
    env["PILOT_OUT_DIR"] = str(OUT_DIR)
    env["PYTHONIOENCODING"] = "utf-8"

    t0 = time.time()
    r = subprocess.run(cmd, env=env, capture_output=True, text=True,
                        timeout=300)
    elapsed = time.time() - t0
    print(f"Elapsed: {elapsed:.1f}s, rc={r.returncode}")

    # Check if 1T26 release found
    dossier = OUT_DIR / "ITSA4.md"
    if dossier.exists():
        text = dossier.read_text(encoding="utf-8", errors="replace")
        for keyword in ("1T26", "Q1 2026", "primeiro trimestre",
                         "Resultados 1T26", "Earnings 1Q26"):
            if keyword.lower() in text.lower():
                print(f"✅ FOUND keyword '{keyword}' in dossier")
                return 0
        print("⏳ ITSA4 1T26 release NOT YET in scraped data")
    else:
        print(f"❌ Dossier not generated at {dossier}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
