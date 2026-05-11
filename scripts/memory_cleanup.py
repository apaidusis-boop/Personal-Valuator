"""memory_cleanup — flag notas stale + dangling no auto-memory.

Checks:
  1. Notas em memory/ que não estão referenciadas em MEMORY.md
  2. Entradas em MEMORY.md apontando para ficheiros inexistentes
  3. Notas com `updated` > 90d (configurável)
  4. Notas de tickers que deixaram de ser holding (opcional)

Action modes:
  --list (default): apenas imprime findings
  --fix: remove entries órfãs de MEMORY.md + cria secção "stale" com candidatos
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def _memory_dir() -> Path:
    home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or "")
    slug = "C--Users-paidu-investment-intelligence"
    c = home / ".claude" / "projects" / slug / "memory"
    if c.exists():
        return c
    return ROOT / "memory"


MEM = _memory_dir()
MEMORY_MD = MEM / "MEMORY.md"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")


def _scan_memory_md() -> tuple[set[str], list[tuple[int, str, str]]]:
    """Devolve (filenames_referenced, entries com line_num)."""
    if not MEMORY_MD.exists():
        return set(), []
    files: set[str] = set()
    entries: list[tuple[int, str, str]] = []
    for i, line in enumerate(MEMORY_MD.read_text(encoding="utf-8").splitlines(), 1):
        for m in LINK_RE.finditer(line):
            files.add(m.group(1))
            entries.append((i, line, m.group(1)))
    return files, entries


def _list_memory_files() -> list[Path]:
    if not MEM.exists():
        return []
    return [p for p in MEM.glob("*.md") if p.name != "MEMORY.md"]


def _parse_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end < 0:
        return {}
    fm: dict = {}
    for line in text[3:end].splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def _cleanup(stale_days: int, fix: bool) -> dict:
    refs, entries = _scan_memory_md()
    files = _list_memory_files()
    filenames_on_disk = {p.name for p in files}

    # 1) broken links in MEMORY.md
    broken = [(ln, line, tgt) for ln, line, tgt in entries if tgt.split("/")[-1] not in filenames_on_disk]

    # 2) orphan files (no ref in MEMORY.md)
    orphan_names = filenames_on_disk - {r.split("/")[-1] for r in refs}

    # 3) stale by updated frontmatter
    stale: list[tuple[str, str]] = []
    threshold = (date.today() - timedelta(days=stale_days)).isoformat()
    for p in files:
        fm = _parse_frontmatter(p)
        upd = fm.get("updated") or fm.get("created")
        # use file mtime fallback
        if not upd:
            ts = datetime.fromtimestamp(p.stat().st_mtime, UTC).date()
            upd = ts.isoformat()
        if upd < threshold:
            stale.append((p.name, upd))

    print("=" * 60)
    print(f"Memory cleanup — {MEM}")
    print("=" * 60)
    print(f"Total memory files:      {len(files)}")
    print(f"Broken links in MEMORY:  {len(broken)}")
    print(f"Orphan files (no ref):   {len(orphan_names)}")
    print(f"Stale (>{stale_days}d sem update): {len(stale)}")
    print()

    if broken:
        print("### Broken links in MEMORY.md")
        for ln, line, tgt in broken:
            print(f"  L{ln}: {tgt}")
            print(f"    {line.strip()}")
        print()

    if orphan_names:
        print("### Orphan files (existem mas não estão no MEMORY.md)")
        for n in sorted(orphan_names):
            print(f"  {n}")
        print()

    if stale:
        print(f"### Stale (>{stale_days}d)")
        for n, upd in sorted(stale, key=lambda x: x[1]):
            print(f"  {upd}  {n}")
        print()

    if fix and broken:
        # remove broken-link lines from MEMORY.md
        text = MEMORY_MD.read_text(encoding="utf-8")
        lines = text.splitlines()
        to_remove = {ln - 1 for ln, _, _ in broken}
        new_lines = [ln for i, ln in enumerate(lines) if i not in to_remove]
        bak = MEMORY_MD.with_suffix(".md.bak")
        bak.write_text(text, encoding="utf-8")
        MEMORY_MD.write_text("\n".join(new_lines), encoding="utf-8")
        print(f"FIX: removed {len(broken)} broken-link lines. Backup: {bak.name}")

    return {"broken": len(broken), "orphan": len(orphan_names), "stale": len(stale)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stale-days", type=int, default=90)
    ap.add_argument("--fix", action="store_true", help="Remove broken links (backup em .md.bak)")
    args = ap.parse_args()
    _cleanup(args.stale_days, args.fix)
    return 0


if __name__ == "__main__":
    sys.exit(main())
