"""Persona purge:
  1. Bury all 23 persona .md descriptions in obsidian_vault/agents/personas/
  2. Rename the 10 persona folders to their canonical handles.

After this, "Charlie Compounder" / "Helena Linha" etc. disappear from Obsidian.
Reversible via cemetery for the .md files; folder renames reversible via git mv.
"""
from __future__ import annotations
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import subprocess
from pathlib import Path

VAULT = Path("obsidian_vault")
CEMETERY = Path("cemetery/2026-05-14/PURGED-personas")
CEMETERY.mkdir(parents=True, exist_ok=True)

# Persona folder -> canonical handle (from AGENTS_REGISTRY.md)
FOLDER_RENAMES = {
    "Aderbaldo Cíclico": "council.commodities-br",
    "Charlie Compounder": "council.industrials-us",
    "Diego Bancário": "council.banks-br",
    "Hank Tier-One": "council.banks-us",
    "Lourdes Aluguel": "council.fiis-br",
    "Mariana Macro": "council.macro",
    "Pedro Alocação": "council.allocation",
    "Tião Galpão": "council.industrials-br",
    "Valentina Prudente": "risk.drift-audit",
    "Walter Triple-Net": "council.reits-us",
}


def git_mv(src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(["git", "mv", str(src), str(dst)], capture_output=True, text=True)
        if r.returncode == 0:
            return True
        if "not under version control" in (r.stderr or "") or "did not match any files" in (r.stderr or ""):
            try:
                src.rename(dst)
                return True
            except Exception as e:
                print(f"  WARN: plain rename failed for {src}: {e}")
                return False
        print(f"  WARN: {r.stderr.strip()[:200]}")
        return False
    except Exception as e:
        print(f"  WARN: {e}")
        return False


def main() -> None:
    # ─── 1. Bury all persona .md descriptions ───
    personas_dir = VAULT / "agents" / "personas"
    if personas_dir.exists():
        files = sorted(personas_dir.glob("*.md"))
        print(f"Step 1: bury {len(files)} persona description files")
        ok = 0
        for p in files:
            rel = p.relative_to(VAULT)
            dst = CEMETERY / "personas_md" / rel
            if git_mv(p, dst):
                ok += 1
                print(f"  buried: {p.name}")
        print(f"  total buried: {ok}/{len(files)}")
        # Try removing now-empty dir
        try:
            personas_dir.rmdir()
            print(f"  removed empty dir: {personas_dir}")
        except OSError:
            pass
    else:
        print("Step 1: no agents/personas/ folder")

    # ─── 2. Rename persona folders to handles ───
    print(f"\nStep 2: rename {len(FOLDER_RENAMES)} persona folders to handles")
    agents_dir = VAULT / "agents"
    renamed = 0
    for old, new in FOLDER_RENAMES.items():
        old_path = agents_dir / old
        new_path = agents_dir / new
        if not old_path.exists():
            print(f"  SKIP {old} (folder doesn't exist)")
            continue
        if new_path.exists():
            print(f"  SKIP {old} → {new} (destination already exists)")
            continue
        if git_mv(old_path, new_path):
            print(f"  renamed: {old} → {new}")
            renamed += 1
        else:
            print(f"  FAILED: {old} → {new}")
    print(f"  total renamed: {renamed}/{len(FOLDER_RENAMES)}")


if __name__ == "__main__":
    main()
