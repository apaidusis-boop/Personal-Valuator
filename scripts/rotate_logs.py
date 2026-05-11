"""Arquiva logs antigos em logs/archive/YYYY-MM/.

Política:
  - daily_run_YYYY-MM-DD.log com mais de N dias -> archive/YYYY-MM/<file>.gz
  - outros .log (fetchers, monitors) -> rotate ao tamanho (>5MB) para .log.1.gz

Idempotente. Corre ao final do daily_run.bat.

Uso:
    python scripts/rotate_logs.py             # default: archive daily_run >30 dias
    python scripts/rotate_logs.py --days 7    # janela personalizada
"""
from __future__ import annotations

import argparse
import gzip
import re
import shutil
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
ARCHIVE_DIR = LOG_DIR / "archive"
SIZE_ROTATE_MB = 5

DAILY_RE = re.compile(r"^daily_run_(\d{4}-\d{2}-\d{2})\.log$")


def archive_daily_logs(cutoff: date) -> tuple[int, int]:
    ok = 0
    skipped = 0
    for f in LOG_DIR.glob("daily_run_*.log"):
        m = DAILY_RE.match(f.name)
        if not m:
            continue
        try:
            d = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if d > cutoff:
            skipped += 1
            continue
        month_dir = ARCHIVE_DIR / f"{d.year:04d}-{d.month:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)
        target = month_dir / f"{f.name}.gz"
        with f.open("rb") as src, gzip.open(target, "wb") as dst:
            shutil.copyfileobj(src, dst)
        f.unlink()
        ok += 1
    return ok, skipped


def rotate_large_logs() -> int:
    """Logs de fetchers/monitors que crescem indefinidamente. Se > 5MB,
    gzip e recomeça vazio."""
    n = 0
    threshold = SIZE_ROTATE_MB * 1024 * 1024
    skip = set(DAILY_RE.match(f.name).string for f in LOG_DIR.glob("daily_run_*.log") if DAILY_RE.match(f.name))
    for f in LOG_DIR.glob("*.log"):
        if f.name in skip:
            continue
        if f.stat().st_size < threshold:
            continue
        target = f.with_suffix(f.suffix + ".1.gz")
        # se já existir, sobreescreve (política simples)
        with f.open("rb") as src, gzip.open(target, "wb") as dst:
            shutil.copyfileobj(src, dst)
        f.write_text("", encoding="utf-8")  # trunca
        n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30,
                    help="arquivar daily_run logs com mais de N dias (default 30)")
    args = ap.parse_args()
    cutoff = date.today() - timedelta(days=args.days)
    archived, kept = archive_daily_logs(cutoff)
    rotated = rotate_large_logs()
    print(f"[rotate_logs] archived: {archived}  kept_recent: {kept}  large_rotated: {rotated}")


if __name__ == "__main__":
    main()
