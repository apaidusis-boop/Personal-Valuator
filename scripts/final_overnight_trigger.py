"""Final trigger after URL discovery completes.

Steps:
  1. Patch yaml with manually-validated URLs (patch_failed_urls.py)
  2. Re-seed BR + US watchlist yamls (catch new ones from discovery)
  3. Run remaining Phase C (US watchlist) — only tickers WITHOUT dossier yet
  4. Run remaining Phase D (BR watchlist) — only tickers WITHOUT dossier yet
  5. Compose final _LEITURA_DA_MANHA.md (orchestrator master)
  6. Compose _BOM_DIA.md (curated)
  7. Re-run code health audit
"""
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PYTHON = str(ROOT / ".venv" / "Scripts" / "python.exe")
TOMORROW = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
OUT_DIR = ROOT / "obsidian_vault" / f"Overnight_{TOMORROW}"
RI_URLS_YAML = ROOT / "config" / "ri_urls.yaml"


def run_step(name: str, cmd: list, env: dict | None = None,
             timeout: int = 1800) -> bool:
    print(f"\n{'='*60}\n[{datetime.now().strftime('%H:%M:%S')}] {name}\n{'='*60}")
    e = os.environ.copy()
    e["PYTHONIOENCODING"] = "utf-8"
    if env:
        e.update(env)
    try:
        r = subprocess.run(cmd, env=e, timeout=timeout)
        ok = r.returncode == 0
        print(f"--> rc={r.returncode} {'✅' if ok else '❌'}")
        return ok
    except Exception as ex:
        print(f"--> EXCEPTION: {ex}")
        return False


def existing_dossiers() -> set[str]:
    if not OUT_DIR.exists():
        return set()
    return {f.stem for f in OUT_DIR.glob("*.md")
            if not f.name.startswith("_")}


def remaining_tickers(yaml_path: Path, market: str,
                       skip_holdings: bool = True) -> list[str]:
    """Return tickers in yaml that are status=ok AND don't have a dossier yet."""
    if not yaml_path.exists():
        return []
    with yaml_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    have = existing_dossiers()
    out = []
    for t, cfg in data.items():
        if cfg.get("status") != "ok":
            continue
        if cfg.get("market") != market:
            continue
        if skip_holdings and cfg.get("is_holding"):
            continue
        if t in have:
            continue
        out.append(t)
    return sorted(out)


def main() -> None:
    print(f"=== FINAL OVERNIGHT TRIGGER @ {datetime.now()}")

    # 1. Patch failed URLs
    run_step("Step 1: Patch failed URLs",
             [PYTHON, str(ROOT / "scripts" / "patch_failed_urls.py")])

    # 2-4. Re-run remaining phases
    if not RI_URLS_YAML.exists():
        print(f"WARNING: {RI_URLS_YAML} not found — discovery may have failed")
        return

    for market, phase in [("us", "watchlist_us"), ("br", "watchlist_br")]:
        tickers = remaining_tickers(RI_URLS_YAML, market)
        print(f"\nRemaining {market} watchlist: {len(tickers)} tickers")
        if not tickers:
            continue
        # Run in batches of 30 to keep subprocess timeouts manageable
        batch_size = 30
        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i + batch_size]
            ok = run_step(
                f"Phase {phase} batch {i // batch_size + 1} ({len(batch)} tickers)",
                [PYTHON, str(ROOT / "scripts" / "pilot_deep_dive.py"),
                 "--from-yaml", "--deep",
                 "--per-ticker-budget", "240",
                 "--tickers"] + batch,
                env={"PILOT_OUT_DIR": str(OUT_DIR),
                     "RI_URLS_YAML": str(RI_URLS_YAML)},
                timeout=int(len(batch) * 360),
            )

    # 5. Final orchestrator master compose
    run_step("Step 5: Final orchestrator master report",
             [PYTHON, str(ROOT / "scripts" / "overnight_orchestrator.py"),
              "--phase", "watchlist_us"],  # any phase will trigger compose
             env={"RI_URLS_YAML": str(RI_URLS_YAML)})

    # 6. Curated _BOM_DIA.md
    run_step("Step 6: Curated _BOM_DIA",
             [PYTHON, str(ROOT / "scripts" / "morning_curated.py")])

    # 7. Code health audit final
    run_step("Step 7: Code health audit",
             [PYTHON, str(ROOT / "scripts" / "overnight_code_health.py")])

    print(f"\n=== FINAL TRIGGER COMPLETE @ {datetime.now()}")


if __name__ == "__main__":
    main()
