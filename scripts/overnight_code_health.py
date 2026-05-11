"""Code health audit for the overnight session.

Runs:
  1. ruff (lint + style)
  2. pyflakes (unused imports / vars)
  3. ast parse check (syntax)
  4. TODO/FIXME scan
  5. code_health perpetuum if available

Targets the files touched in this session + supporting modules.
Output: obsidian_vault/Overnight_<TOMORROW>/_CODE_HEALTH.md
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOMORROW = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
OUT_DIR = ROOT / "obsidian_vault" / f"Overnight_{TOMORROW}"
PYTHON = str(ROOT / ".venv" / "Scripts" / "python.exe")

# Files touched / created in this session (manual list)
TARGETS = [
    "scripts/pilot_deep_dive.py",
    "scripts/ri_url_resolver.py",
    "scripts/overnight_orchestrator.py",
    "scripts/overnight_code_health.py",
    "library/_md_extract.py",
    "fetchers/portal_playwright.py",
    "monitors/cvm_pdf_extractor.py",
]


def run_cmd(cmd: list, timeout: int = 120) -> tuple[int, str, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8",
                           errors="replace")
        return r.returncode, r.stdout or "", r.stderr or ""
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except FileNotFoundError as e:
        return -2, "", f"NOT FOUND: {e}"


def check_syntax(path: Path) -> dict:
    """ast.parse syntax check."""
    try:
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        return {"ok": True, "lines": text.count("\n") + 1}
    except SyntaxError as e:
        return {"ok": False, "error": f"line {e.lineno}: {e.msg}"}


def find_todos(path: Path) -> list:
    """Find TODO/FIXME/XXX/HACK markers."""
    found = []
    pattern = re.compile(r"#\s*(TODO|FIXME|XXX|HACK|BUG)\s*:?\s*(.+)$",
                         re.IGNORECASE)
    try:
        for i, ln in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            m = pattern.search(ln)
            if m:
                found.append({"line": i, "kind": m.group(1).upper(),
                              "msg": m.group(2).strip()[:100]})
    except Exception:
        pass
    return found


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    L = []
    L.append("# Code Health Audit — Overnight 2026-05-11")
    L.append("")
    L.append("Audit dos ficheiros tocados ou criados durante esta sessão.")
    L.append("")

    # Existence + syntax
    L.append("## Sintaxe + linha-count")
    L.append("")
    L.append("| Ficheiro | Existe | Sintaxe | Linhas | TODOs |")
    L.append("|---|---|---|---|---|")
    for rel in TARGETS:
        p = ROOT / rel
        if not p.exists():
            L.append(f"| `{rel}` | ❌ | - | - | - |")
            continue
        syn = check_syntax(p)
        todos = find_todos(p)
        L.append(f"| `{rel}` | ✅ | "
                 f"{'✅' if syn.get('ok') else '❌ ' + syn.get('error', '')} | "
                 f"{syn.get('lines', '-')} | {len(todos)} |")
    L.append("")

    # ruff
    L.append("## ruff (lint)")
    L.append("")
    rc, stdout, stderr = run_cmd(
        [PYTHON, "-m", "ruff", "check"] + [str(ROOT / t) for t in TARGETS
                                             if (ROOT / t).exists()],
        timeout=60,
    )
    if rc == -2:
        L.append("_ruff não instalado_")
    elif rc < 0:
        L.append(f"_timeout/erro: {stderr[:200]}_")
    else:
        if stdout:
            issues = stdout.strip().splitlines()
            L.append(f"**{len(issues)} issues**:")
            L.append("")
            L.append("```")
            for ln in issues[:30]:
                L.append(ln)
            if len(issues) > 30:
                L.append(f"... e mais {len(issues) - 30}")
            L.append("```")
        else:
            L.append("_(zero issues)_ ✅")
    L.append("")

    # pyflakes
    L.append("## pyflakes (unused imports / vars)")
    L.append("")
    rc, stdout, stderr = run_cmd(
        [PYTHON, "-m", "pyflakes"] + [str(ROOT / t) for t in TARGETS
                                        if (ROOT / t).exists()],
        timeout=60,
    )
    if rc == -2:
        L.append("_pyflakes não instalado_")
    elif rc < 0:
        L.append(f"_timeout/erro: {stderr[:200]}_")
    else:
        if stdout:
            issues = stdout.strip().splitlines()
            L.append(f"**{len(issues)} warnings**:")
            L.append("")
            L.append("```")
            for ln in issues[:20]:
                L.append(ln)
            L.append("```")
        else:
            L.append("_(clean)_ ✅")
    L.append("")

    # TODO/FIXME details
    L.append("## TODO / FIXME / HACK")
    L.append("")
    any_todos = False
    for rel in TARGETS:
        p = ROOT / rel
        if not p.exists():
            continue
        todos = find_todos(p)
        if todos:
            any_todos = True
            L.append(f"### `{rel}`")
            L.append("")
            for t in todos:
                L.append(f"- L{t['line']} **{t['kind']}**: {t['msg']}")
            L.append("")
    if not any_todos:
        L.append("_(nenhum TODO/FIXME no código novo)_")
        L.append("")

    # code_health perpetuum (if exists)
    L.append("## code_health perpetuum (CH001-CH007)")
    L.append("")
    perp = ROOT / "agents" / "perpetuum_master.py"
    if perp.exists():
        rc, stdout, stderr = run_cmd(
            [PYTHON, str(perp), "--only", "code_health", "--dry-run"],
            timeout=180,
        )
        if rc == 0 and stdout:
            L.append("```")
            tail = stdout.strip().splitlines()[-30:]
            L.extend(tail)
            L.append("```")
        else:
            L.append(f"_skipped (rc={rc})_")
    else:
        L.append("_perpetuum_master não disponível_")
    L.append("")

    # Final summary
    L.append("---")
    L.append(f"_Generated by `scripts/overnight_code_health.py` at "
             f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")

    out_path = OUT_DIR / "_CODE_HEALTH.md"
    out_path.write_text("\n".join(L), encoding="utf-8")
    print(f"Code health saved: {out_path}")


if __name__ == "__main__":
    main()
