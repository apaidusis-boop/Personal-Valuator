"""Mega Auditor — Karpathy-driven cruft detector.

T1 Observer (audit-only). NEVER deletes. Output: report markdown.

Inspirado nos princípios Karpathy (CLAUDE.md → "Princípios de coding"):
  - Surgical changes: detecta TODO o que não pertence ao caminho actual
  - Simplicity first: candidato a remoção se 200 linhas podem ser 50

Distinto de `agents/perpetuum/code_health.py`:
  - code_health: anti-patterns INSIDE Python files (CH001-CH007)
  - mega_auditor: file-level / doc-level / folder-level cruft (DELETION candidates)

Categorias:
  CODE-DEAD       : .py files não importados E não no CLAUDE.md catalog
  CODE-ONESHOT    : scripts/<ticker>_*.py / *_<ticker>_scenario.py (anti-pattern)
  CODE-MARK-OLD   : ficheiros com `# DEPRECATED` / `# OLD` / `# legacy` markers
  VAULT-EMPTY     : .md files com body <100 chars after frontmatter
  VAULT-DEPRECATED: .md files com "DEPRECATED" / "PROPOSED" / "HANDOFF_*" markers
  MEM-STALE       : MEMORY.md aponta para .md files que não existem
  FOLDER-EMPTY    : directorias sem ficheiros (recursivo)

Run:
    python -m agents.mega_auditor                 # gera report
    python -m agents.mega_auditor --report-only   # mesmo (defaults)
    python -m agents.mega_auditor --json          # output JSON em vez de markdown
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "obsidian_vault"
MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-paidu-investment-intelligence" / "memory"

CODE_SCAN_DIRS = ["agents", "fetchers", "scripts", "scoring", "analytics",
                  "monitors", "library"]

# Skip these — foundational, test infra, OR already-buried items
SKIP_PATTERNS = [
    "__pycache__", ".git", "venv", "node_modules",
    ".pytest_cache", "tests/", "cemetery/", "cemetery\\",
]

# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def _should_skip(p: Path) -> bool:
    s = _rel(p)
    return any(pat in s for pat in SKIP_PATTERNS)


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            return text[end + 5:]
    return text


def _read_clean(p: Path) -> str:
    """Read with multiple encoding attempts (some .md files are UTF-16)."""
    for enc in ("utf-8", "utf-16", "utf-8-sig", "latin-1"):
        try:
            return p.read_text(encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return ""


# ──────────────────────────────────────────────────────────────────────
# CODE-DEAD: .py files not imported anywhere AND not in CLAUDE.md
# ──────────────────────────────────────────────────────────────────────

def _gather_imports() -> set[str]:
    """Return set of module paths imported anywhere.

    Includes both the module being imported FROM and the names imported AS submodules.
    E.g. `from scripts import _captains_log as cl` → adds {scripts, scripts._captains_log}.
    """
    imported: set[str] = set()
    # `from X import Y, Z [as W]` — capture X plus the names list (single line)
    pat_from = re.compile(
        r"^[ \t]*from\s+([\w.]+)\s+import\s+(.+?)$",
        re.MULTILINE,
    )
    pat_imp = re.compile(r"^\s*import\s+([\w.]+)", re.MULTILINE)
    for d in CODE_SCAN_DIRS + ["tests"]:
        base = ROOT / d
        if not base.exists():
            continue
        for py in base.rglob("*.py"):
            if _should_skip(py):
                continue
            txt = _read_clean(py)
            for parent, names in pat_from.findall(txt):
                imported.add(parent)
                for n in names.split(","):
                    n = n.strip().split(" as ")[0].strip()
                    if n and n != "*":
                        imported.add(f"{parent}.{n}")
                        imported.add(n)  # short name
            for m in pat_imp.findall(txt):
                imported.add(m)
                # Also short-form: import X.Y → also "Y"
                imported.add(m.split(".")[-1])
    return imported


def _claude_md_mentions() -> set[str]:
    """Return set of .py paths mentioned in CLAUDE.md script catalog."""
    md = ROOT / "CLAUDE.md"
    if not md.exists():
        return set()
    txt = _read_clean(md)
    paths: set[str] = set()
    # `python scripts/X.py`, `scripts/X.py` (with or without backticks)
    for m in re.findall(r"([\w/.\-]+\.py)", txt):
        paths.add(m.replace("\\", "/"))
    # `python -m foo.bar` → foo/bar.py
    for m in re.findall(r"python\s+-m\s+([\w.]+)", txt):
        paths.add(m.replace(".", "/") + ".py")
    # backticked module paths: `agents.foo.bar` (used in script catalog)
    for m in re.findall(r"`([\w]+(?:\.[\w]+)+)`", txt):
        if not m.startswith("("):
            paths.add(m.replace(".", "/") + ".py")
    return paths


def _ii_bat_mentions() -> set[str]:
    """Parse ii.bat dispatcher to find all mapped scripts/modules."""
    ii = ROOT / "ii.bat"
    if not ii.exists():
        return set()
    txt = _read_clean(ii)
    paths: set[str] = set()
    # SCRIPT=scripts\foo.py
    for m in re.findall(r"SCRIPT=([\w\\/.\-]+\.py)", txt):
        paths.add(m.replace("\\", "/"))
    # -m analytics.foo
    for m in re.findall(r"-m\s+([\w.]+)", txt):
        paths.add(m.replace(".", "/") + ".py")
    # streamlit run path
    for m in re.findall(r"streamlit\s+run\s+\"[^\"]*?([\w\\/.\-]+\.py)", txt):
        paths.add(m.replace("\\", "/"))
    return paths


def _agents_yaml_classes() -> set[str]:
    """Parse config/agents.yaml + similar configs for `class: foo.bar:Cls` refs.

    Catches agents loaded dynamically via _registry.load_agent(class_path).
    """
    paths: set[str] = set()
    for cfg in (ROOT / "config").rglob("*.yaml"):
        if not cfg.exists():
            continue
        txt = _read_clean(cfg)
        # `class: agents.watchdog:WatchdogAgent` → agents/watchdog.py
        for m in re.findall(r"class:\s*([\w.]+):", txt):
            paths.add(m.replace(".", "/") + ".py")
        # `module: foo.bar` patterns
        for m in re.findall(r"module:\s*([\w.]+)", txt):
            paths.add(m.replace(".", "/") + ".py")
    return paths


def _daily_run_bat_mentions() -> set[str]:
    """Parse scripts/daily_run.bat for `python -m X` and `python scripts/X.py`."""
    paths: set[str] = set()
    bat = ROOT / "scripts" / "daily_run.bat"
    if not bat.exists():
        return paths
    txt = _read_clean(bat)
    for m in re.findall(r"python\s+(?:-X\s+\w+\s+)?-m\s+([\w.]+)", txt):
        paths.add(m.replace(".", "/") + ".py")
    for m in re.findall(r"python\s+(?:-X\s+\w+\s+)?\"?[%\w\\/.\-]*?([\w/.\-]+\.py)", txt):
        paths.add(m.replace("\\", "/"))
    return paths


def _universe_tickers() -> set[str]:
    """Load real tickers from config/universe.yaml. For CODE-ONESHOT precision."""
    yml = ROOT / "config" / "universe.yaml"
    if not yml.exists():
        return set()
    txt = _read_clean(yml)
    # Pattern: `ticker: ABCD3` or `ticker: ABCD11`
    return set(re.findall(r"\bticker:\s*([A-Z]{2,5}\d{1,2})\b", txt))


def detect_code_dead() -> tuple[list[dict], list[dict]]:
    """Return (dead, undocumented_entry_points).

    DEAD = no __main__ + not imported + not in any catalog. High confidence.
    UNDOCUMENTED = has __main__ + not in catalog. Medium signal — add catalog entry.
    """
    imported = _gather_imports()
    catalog = (_claude_md_mentions() | _ii_bat_mentions()
               | _agents_yaml_classes() | _daily_run_bat_mentions())
    dead: list[dict] = []
    undocumented: list[dict] = []
    for d in CODE_SCAN_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for py in base.rglob("*.py"):
            if _should_skip(py):
                continue
            rel = _rel(py)
            name = py.stem
            if name in ("__init__", "__main__"):
                continue
            module_path = rel.replace("/", ".").removesuffix(".py")
            module_short = name
            is_imported = (
                module_path in imported
                or any(m.endswith("." + module_short) or m == module_short
                       for m in imported)
            )
            in_catalog = (
                rel in catalog
                or any(c.endswith("/" + py.name) for c in catalog)
                or module_path in {c.removesuffix(".py").replace("/", ".")
                                    for c in catalog}
            )
            txt = _read_clean(py)
            has_main = "__main__" in txt
            if is_imported or in_catalog:
                continue
            entry = {
                "id": "",  # filled later
                "path": rel,
                "has_main": has_main,
                "lines": len(txt.splitlines()),
            }
            if has_main:
                entry["evidence"] = "has `__main__` but not in CLAUDE.md catalog or ii.bat dispatcher — add catalog entry OR delete"
                undocumented.append(entry)
            else:
                entry["evidence"] = "no `__main__`, not imported anywhere, not in catalog — likely dead"
                dead.append(entry)
    for i, e in enumerate(dead, 1):
        e["id"] = f"MA-CD-{i:03d}"
    for i, e in enumerate(undocumented, 1):
        e["id"] = f"MA-UN-{i:03d}"
    return dead, undocumented


# ──────────────────────────────────────────────────────────────────────
# CODE-ONESHOT: scripts that look ticker-specific (anti-pattern)
# ──────────────────────────────────────────────────────────────────────

def detect_code_oneshot() -> list[dict]:
    """Match scripts where filename contains an actual ticker from universe.yaml.

    Anti-pattern (CLAUDE.md): one-shot ticker-specific scripts like
    `itsa4_drip_scenario.py` should be generalised to `--ticker X`.
    """
    out: list[dict] = []
    tickers = _universe_tickers()
    if not tickers:
        return out
    scripts = ROOT / "scripts"
    if not scripts.exists():
        return out
    for py in scripts.glob("*.py"):
        if _should_skip(py):
            continue
        stem = py.stem.upper()
        # Look for ticker as token (delimited by _ or boundary)
        tokens = re.split(r"[_\-]", stem)
        for tk in tokens:
            if tk in tickers:
                out.append({
                    "id": f"MA-CO-{len(out) + 1:03d}",
                    "path": _rel(py),
                    "evidence": f"filename contains ticker '{tk}' from universe.yaml; "
                                "CLAUDE.md flags one-shot ticker scripts as anti-pattern",
                })
                break
    return out


# ──────────────────────────────────────────────────────────────────────
# CODE-MARK-OLD: files with deprecation markers
# ──────────────────────────────────────────────────────────────────────

OLD_MARKERS = [
    # Tighter: marker must be the WHOLE comment OR follow boundary (no descriptive text after :)
    re.compile(r"#\s*DEPRECATED\b(?!:)", re.IGNORECASE),
    re.compile(r"#\s*LEGACY\b(?!:)(?!\s+[a-z])", re.IGNORECASE),
    re.compile(r"#\s*TODO[:\s]+REMOVE\b", re.IGNORECASE),
    re.compile(r"#\s*XXX[:\s]+remove\b", re.IGNORECASE),
]


# Self-skip: this auditor mentions the markers as text, don't flag itself
SELF_SKIP_PATHS = {"agents/mega_auditor.py", "agents/perpetuum/code_health.py"}


def detect_code_marked_old() -> list[dict]:
    out: list[dict] = []
    for d in CODE_SCAN_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for py in base.rglob("*.py"):
            if _should_skip(py):
                continue
            if _rel(py) in SELF_SKIP_PATHS:
                continue
            txt = _read_clean(py)
            # Skip docstring-only mentions: only count if marker is at start of line
            for marker in OLD_MARKERS:
                # Look at non-docstring lines: simplest heuristic = first 3 chars
                # of the line are not whitespace+quote
                hit = False
                for line in txt.splitlines():
                    if marker.search(line):
                        # Skip if line is inside a docstring (starts with whitespace then quote)
                        if line.lstrip().startswith(('"', "'", "#  ")):
                            # Only count if it's at very start of line OR very intentional
                            stripped = line.lstrip()
                            if stripped.startswith("# ") and "DEPRECATED" in stripped.upper():
                                hit = True
                                break
                            continue
                        hit = True
                        break
                if hit:
                    out.append({
                        "id": f"MA-CM-{len(out) + 1:03d}",
                        "path": _rel(py),
                        "evidence": f"contains marker matching {marker.pattern!r}",
                    })
                    break
    return out


# ──────────────────────────────────────────────────────────────────────
# VAULT-EMPTY: markdown files with negligible body
# ──────────────────────────────────────────────────────────────────────

# Vault marker filenames that are intentionally short (Phase U.0 layer markers etc.)
VAULT_PROTECTED = {"_LAYER.md", "_MOC.md", "_Index.md", "_INDEX.md"}


def detect_vault_empty() -> list[dict]:
    out: list[dict] = []
    if not VAULT.exists():
        return out
    for md in VAULT.rglob("*.md"):
        if _should_skip(md):
            continue
        if md.name in VAULT_PROTECTED:
            continue
        txt = _read_clean(md)
        body = _strip_frontmatter(txt).strip()
        # Strip headings, links, count meaningful chars
        meaningful = re.sub(r"[#\-*\[\]()|]+", "", body).strip()
        if len(meaningful) < 100:
            out.append({
                "id": f"MA-VE-{len(out) + 1:03d}",
                "path": _rel(md),
                "body_chars": len(body),
                "evidence": f"body has {len(meaningful)} meaningful chars (threshold 100)",
            })
    return out


# ──────────────────────────────────────────────────────────────────────
# VAULT-DEPRECATED: handoff/proposed docs from past phases
# ──────────────────────────────────────────────────────────────────────

VAULT_STALE_PATTERNS = [
    re.compile(r"HANDOFF_PHASE_[A-Z]+", re.IGNORECASE),
    re.compile(r"_DEPRECATED\.md$", re.IGNORECASE),
    re.compile(r"^PROPOSED_", re.IGNORECASE),
    re.compile(r"^DRAFT_", re.IGNORECASE),
]


def detect_vault_deprecated() -> list[dict]:
    out: list[dict] = []
    seen_paths: set[str] = set()
    # Search both vault and project root for HANDOFF_*
    for base in [VAULT, ROOT]:
        if not base.exists():
            continue
        for md in base.rglob("*.md"):
            if _should_skip(md):
                continue
            rel = _rel(md)
            if rel in seen_paths:
                continue
            seen_paths.add(rel)
            for pat in VAULT_STALE_PATTERNS:
                if pat.search(md.name):
                    out.append({
                        "id": f"MA-VD-{len(out) + 1:03d}",
                        "path": rel,
                        "evidence": f"filename matches stale pattern {pat.pattern!r}",
                    })
                    break
    return out


# ──────────────────────────────────────────────────────────────────────
# MEM-STALE: MEMORY.md links to non-existent .md files
# ──────────────────────────────────────────────────────────────────────

def detect_mem_stale() -> list[dict]:
    out: list[dict] = []
    mem = MEMORY_DIR / "MEMORY.md"
    if not mem.exists():
        return out
    txt = _read_clean(mem)
    # Pattern: `[label](file.md)` or `[label](path/file.md)`
    pat = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")
    for label, link in pat.findall(txt):
        target = MEMORY_DIR / link
        if not target.exists():
            out.append({
                "id": f"MA-MS-{len(out) + 1:03d}",
                "path": link,
                "label": label,
                "evidence": f"MEMORY.md links to {link!r} which does not exist in {MEMORY_DIR}",
            })
    return out


# ──────────────────────────────────────────────────────────────────────
# FOLDER-EMPTY: directories without any files (recursively)
# ──────────────────────────────────────────────────────────────────────

def detect_folder_empty() -> list[dict]:
    out: list[dict] = []
    for base in [ROOT / "agents", ROOT / "scripts", VAULT,
                 ROOT / "library", ROOT / "fetchers", ROOT / "data",
                 ROOT / "reports"]:
        if not base.exists():
            continue
        for sub in base.rglob("*"):
            if not sub.is_dir():
                continue
            if _should_skip(sub):
                continue
            # Has any file (recursively)?
            has_file = any(p.is_file() for p in sub.rglob("*"))
            if not has_file:
                out.append({
                    "id": f"MA-FE-{len(out) + 1:03d}",
                    "path": _rel(sub),
                    "evidence": "directory contains no files (recursively)",
                })
    return out


# ──────────────────────────────────────────────────────────────────────
# Report assembly
# ──────────────────────────────────────────────────────────────────────

def run_audit() -> dict:
    dead, undocumented = detect_code_dead()
    cats = {
        "CODE-DEAD": dead,
        "CODE-UNDOCUMENTED": undocumented,
        "CODE-ONESHOT": detect_code_oneshot(),
        "CODE-MARK-OLD": detect_code_marked_old(),
        "VAULT-EMPTY": detect_vault_empty(),
        "VAULT-DEPRECATED": detect_vault_deprecated(),
        "MEM-STALE": detect_mem_stale(),
        "FOLDER-EMPTY": detect_folder_empty(),
    }
    # Annotate each item with its category for lookup during burial
    for cat, items in cats.items():
        for item in items:
            item["category"] = cat
    return {"run_date": date.today().isoformat(), "categories": cats}


# ──────────────────────────────────────────────────────────────────────
# Cemetery — quarantine before delete
# ──────────────────────────────────────────────────────────────────────

CEMETERY = ROOT / "cemetery"
CEMETERY_README = """# 🪦 Cemetery — Quarantine Area

Files and folders enterrados pelo `agents/mega_auditor.py --bury` aguardam aqui antes
de delete definitivo. Princípio: **reversível por default**.

## Estrutura

```
cemetery/
├── README.md             # este ficheiro
├── <DATE>/               # data do enterro (run_date do audit)
│   ├── manifest.md       # o que foi enterrado, porquê, como restaurar
│   └── <CATEGORY>/       # CODE-DEAD, VAULT-EMPTY, etc.
│       └── <orig_path>   # estrutura original preservada
```

## Restaurar

Cada entrada no `manifest.md` tem comando `git mv` para restaurar para localização
original. Ou usa `python -m agents.mega_auditor --exhume <ID>` (futuro).

## Truly delete

Após N dias (recomendado 30+) sem regressão observada, podes apagar a pasta de
data inteira: `rm -rf cemetery/<DATE>`. Se algo dependia daquele código, já saberias
neste ponto.

## Política

- Burial é registado em git (move, não delete)
- Cada burial tem manifest com reason
- FOLDER-EMPTY são apenas registadas (não há content para mover)
- VAULT-EMPTY e VAULT-DEPRECATED preservam path completo dentro de `vault/`
"""


def _ensure_cemetery() -> Path:
    """Create cemetery/ root + README if missing."""
    CEMETERY.mkdir(exist_ok=True)
    readme = CEMETERY / "README.md"
    if not readme.exists():
        readme.write_text(CEMETERY_README, encoding="utf-8")
    return CEMETERY


def bury(audit: dict, ids: list[str], dry_run: bool = False) -> dict:
    """Move audit-flagged items to cemetery/<DATE>/<CATEGORY>/<orig_path>.

    Preserves folder structure for git-friendly restore. Writes manifest.md
    with restore commands. Idempotent — safe to re-run with same IDs (skips
    already-buried items).
    """
    _ensure_cemetery()
    grave = CEMETERY / audit["run_date"]
    grave.mkdir(exist_ok=True)

    # Flat lookup by ID
    by_id: dict[str, dict] = {}
    for cat_items in audit["categories"].values():
        for item in cat_items:
            by_id[item["id"]] = item

    results: list[dict] = []
    manifest_entries: list[str] = []

    for id_ in ids:
        if id_ not in by_id:
            results.append({"id": id_, "status": "not_found",
                            "error": f"ID {id_} not in audit"})
            continue
        item = by_id[id_]
        src = ROOT / item["path"]
        cat = item["category"]
        dest = grave / cat / item["path"]

        if not src.exists():
            results.append({"id": id_, "status": "source_missing",
                            "src": _rel(src)})
            continue

        if dest.exists():
            results.append({"id": id_, "status": "already_buried",
                            "dest": _rel(dest)})
            continue

        if dry_run:
            results.append({"id": id_, "status": "dry_run",
                            "src": _rel(src), "dest": _rel(dest)})
            continue

        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            # FOLDER-EMPTY: just rmdir source (no content to preserve)
            if cat == "FOLDER-EMPTY":
                src.rmdir()
                manifest_entries.append(
                    f"- **{id_}** `{item['path']}` (FOLDER-EMPTY) — directory was empty, removed.\n"
                    f"  - Restore: `mkdir -p \"{item['path']}\"` (if needed)"
                )
                results.append({"id": id_, "status": "removed_empty_dir",
                                "src": _rel(src)})
            else:
                shutil.move(str(src), str(dest))
                rel_dest = _rel(dest)
                manifest_entries.append(
                    f"- **{id_}** `{item['path']}` → `{rel_dest}`\n"
                    f"  - Category: {cat}\n"
                    f"  - Reason: {item.get('evidence', '?')}\n"
                    f"  - Restore: `git mv \"{rel_dest}\" \"{item['path']}\"` "
                    f"(or `mv` if not staged)"
                )
                results.append({"id": id_, "status": "buried",
                                "src": _rel(src), "dest": rel_dest})
        except Exception as e:
            results.append({"id": id_, "status": "error",
                            "error": f"{type(e).__name__}: {e}"})

    # Append to manifest (or create)
    manifest = grave / "manifest.md"
    header = f"# 🪦 Cemetery {audit['run_date']} — manifest"
    burial_block = "\n".join([
        f"\n## Burial @ {datetime.now().isoformat(timespec='seconds')}",
        f"_Audit IDs: {', '.join(ids)}_\n",
        *manifest_entries,
    ])
    if manifest.exists():
        manifest.write_text(
            manifest.read_text(encoding="utf-8") + "\n" + burial_block,
            encoding="utf-8",
        )
    else:
        manifest.write_text(header + burial_block, encoding="utf-8")

    return {
        "grave": _rel(grave),
        "manifest": _rel(manifest),
        "buried_count": sum(1 for r in results
                            if r["status"] in ("buried", "removed_empty_dir")),
        "results": results,
    }


# Shortcut presets — for batch burial
SAFE_CATEGORIES = {"FOLDER-EMPTY", "VAULT-EMPTY", "VAULT-DEPRECATED", "MEM-STALE"}
VERIFIED_DEAD_CATEGORIES = {"CODE-DEAD"}  # Only after manual verification


def select_ids(audit: dict, preset: str) -> list[str]:
    """Return IDs matching preset: 'safe', 'verified-dead', 'all'."""
    out: list[str] = []
    for cat, items in audit["categories"].items():
        if preset == "safe" and cat in SAFE_CATEGORIES:
            out.extend(i["id"] for i in items)
        elif preset == "verified-dead" and cat in VERIFIED_DEAD_CATEGORIES:
            out.extend(i["id"] for i in items)
        elif preset == "safe-and-dead" and cat in (SAFE_CATEGORIES | VERIFIED_DEAD_CATEGORIES):
            out.extend(i["id"] for i in items)
        elif preset == "all":
            out.extend(i["id"] for i in items)
    return out


CATEGORY_DESCRIPTIONS = {
    "CODE-DEAD": "Python files com **NO `__main__`**, NÃO importados por nada, NÃO no catalog. Alta confiança — provavelmente seguros para apagar.",
    "CODE-UNDOCUMENTED": "Python files **com `__main__`** (entry points runnable) mas NÃO mencionados em `CLAUDE.md` catalog ou `ii.bat` dispatcher. Acção: ou adicionar ao catalog, ou apagar se obsoleto.",
    "CODE-ONESHOT": "Scripts com nome contendo ticker real do `universe.yaml` (anti-pattern CLAUDE.md). Generalizar para `--ticker X` e apagar one-shot.",
    "CODE-MARK-OLD": "Files com markers `# DEPRECATED` / `# LEGACY` / `# TODO REMOVE` em código. Hint deixado pelo autor.",
    "VAULT-EMPTY": "Markdown files com <100 meaningful chars no body. Provavelmente stub esquecido ou rascunho abandonado.",
    "VAULT-DEPRECATED": "Markdown com filename pattern `HANDOFF_*` / `_DEPRECATED.md` / `PROPOSED_*`. Phase docs antigos.",
    "MEM-STALE": "MEMORY.md aponta para .md file inexistente. Clean-up trivial.",
    "FOLDER-EMPTY": "Directorias sem ficheiros (recursivo). Apagar é seguro.",
}


def render_markdown(audit: dict) -> str:
    out = [
        f"# 🧹 Mega Audit — {audit['run_date']}",
        "",
        "> **T1 Observer**. Audit-only — zero ficheiros tocados. User aprova batch-a-batch.",
        "> Princípios Karpathy: Surgical changes + Simplicity first → candidatos a remoção/unificação.",
        "",
        "## Resumo",
        "",
        "| Categoria | Count | Severidade |",
        "|---|---|---|",
    ]
    severity = {
        "MEM-STALE": "🟢 low (clean-up trivial)",
        "FOLDER-EMPTY": "🟢 low (apagar safe)",
        "VAULT-EMPTY": "🟡 medium (verificar caso-a-caso)",
        "VAULT-DEPRECATED": "🟡 medium (provavelmente safe)",
        "CODE-MARK-OLD": "🟡 medium (autor marcou)",
        "CODE-ONESHOT": "🟠 medium-high (anti-pattern explícito)",
        "CODE-UNDOCUMENTED": "🟠 medium (catalog gap OR obsoleto)",
        "CODE-DEAD": "🔴 high confidence (no main + no import + no catalog)",
    }
    for cat, items in audit["categories"].items():
        out.append(f"| {cat} | {len(items)} | {severity.get(cat, '?')} |")
    out.append("")
    out.append(f"**Total candidatos**: {sum(len(v) for v in audit['categories'].values())}")
    out.append("")
    out.append("---")
    out.append("")

    for cat, items in audit["categories"].items():
        out.append(f"## {cat}")
        out.append("")
        out.append(f"_{CATEGORY_DESCRIPTIONS.get(cat, '')}_")
        out.append("")
        if not items:
            out.append("✅ Nenhum candidato.")
            out.append("")
            continue
        for item in items:
            line = f"- **{item['id']}** `{item['path']}`"
            extras = []
            if "lines" in item:
                extras.append(f"{item['lines']} LoC")
            if "has_main" in item and item["has_main"]:
                extras.append("has `__main__`")
            if "body_chars" in item:
                extras.append(f"body={item['body_chars']}c")
            if "label" in item:
                extras.append(f"label={item['label']!r}")
            if extras:
                line += f" — {', '.join(extras)}"
            out.append(line)
            out.append(f"  - _{item['evidence']}_")
        out.append("")

    out.append("---")
    out.append("")
    out.append("## Workflow para apagar")
    out.append("")
    out.append("1. Reviewer escolhe IDs específicos (ex: `MA-FE-001`, `MA-FE-003`)")
    out.append("2. Comanda: \"apaga MA-FE-001..003 + MA-MS-001..005\"")
    out.append("3. Execução manual ou via futuro `mega_auditor.py --apply --ids ...`")
    out.append("4. Commit em git ANTES de cada batch (rollback seguro)")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Mega Auditor — T1 Observer")
    ap.add_argument("--json", action="store_true",
                    help="Output JSON in vez de markdown")
    ap.add_argument("--out", type=str, default=None,
                    help="Report path (default: obsidian_vault/Mega_Audit_<DATE>.md)")
    ap.add_argument("--bury", nargs="+", metavar="ID",
                    help="Move flagged items to cemetery/<DATE>/. Specific IDs (MA-CD-001 ...)")
    ap.add_argument("--bury-preset", choices=["safe", "verified-dead", "safe-and-dead", "all"],
                    help="Bulk bury a preset: safe (FOLDER-EMPTY+VAULT-*+MEM-STALE), "
                         "verified-dead (CODE-DEAD), safe-and-dead, all")
    ap.add_argument("--dry-run", action="store_true",
                    help="With --bury: show what would move, don't touch files")
    args = ap.parse_args()

    audit = run_audit()

    # Bury mode
    if args.bury or args.bury_preset:
        ids = list(args.bury) if args.bury else []
        if args.bury_preset:
            ids.extend(select_ids(audit, args.bury_preset))
        ids = list(dict.fromkeys(ids))  # dedup, preserve order
        if not ids:
            print("No IDs selected for burial. Pass --bury <ID...> or --bury-preset safe.")
            sys.exit(1)
        result = bury(audit, ids, dry_run=args.dry_run)
        action = "Would bury" if args.dry_run else "Buried"
        print(f"{action} {result['buried_count']}/{len(ids)} items.")
        print(f"Grave: {result['grave']}")
        print(f"Manifest: {result['manifest']}")
        skipped = [r for r in result["results"]
                   if r["status"] not in ("buried", "removed_empty_dir", "dry_run")]
        if skipped:
            print(f"\nSkipped/errors ({len(skipped)}):")
            for r in skipped[:10]:
                print(f"  {r['id']}: {r['status']}"
                      + (f" — {r.get('error', '')}" if r.get("error") else ""))
        return

    # Audit mode (default)
    if args.json:
        print(json.dumps(audit, indent=2, ensure_ascii=False))
        return

    md = render_markdown(audit)
    out_path = Path(args.out) if args.out else (
        VAULT / f"Mega_Audit_{audit['run_date']}.md"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")

    total = sum(len(v) for v in audit["categories"].values())
    print(f"Mega Audit complete — {total} candidates across {len(audit['categories'])} categories.")
    print(f"Report: {_rel(out_path)}")
    for cat, items in audit["categories"].items():
        print(f"  {cat}: {len(items)}")


if __name__ == "__main__":
    main()
