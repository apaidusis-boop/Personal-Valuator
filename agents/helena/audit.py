"""audit — Helena design system linter.

Scans Streamlit + Plotly code for violations of obsidian_vault/skills/Design_System.md.

Rules (each has ID + severity):
    DS001 error  — Rainbow / sequential cmap in pandas styler (RdYlGn, viridis, …)
    DS002 error  — Raw `st.metric(` (must use `kpi_tile()`)
    DS003 error  — Emoji-prefix in `st.title/header/subheader/markdown("# …")`
    DS004 error  — `px.pie(` (anti-padrão #6, use bar/treemap)
    DS005 warn   — `template="plotly_white"` / `"plotly_dark"` cru (use `ii_dark`)
    DS006 warn   — Hex color literal fora dos 5 tokens da paleta
    DS007 warn   — `color="black"|"red"|"green"|"blue"|…` (cor por nome)
    DS008 warn   — `section_caption()` ou `st.caption()` com >8 palavras
    DS009 info   — Page sem `inject_css()` (não aplica design tokens)
    DS010 warn   — Skill file >500 body lines (progressive disclosure)

Excluded files (são fonte do sistema, não alvo): `scripts/_theme.py`, `scripts/_components.py`.

Run:
    python -m agents.helena.audit             # writes 01_Audit.md
    python -m agents.helena.audit --print     # stdout only
    python -m agents.helena.audit --paths X   # custom path scope
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from . import VAULT_OUT, ROOT

# ────────────────── palette canon ──────────────────

PALETTE_HEX = {
    "#0f1115", "#161a22", "#1d2330", "#222833",        # neutrals
    "#e6e8eb", "#7a8290",                              # text
    "#4f8df9", "#4ade80", "#f87171", "#fbbf24", "#a78bfa",  # 5 categorical/semantic
}
RAINBOW_CMAPS = {
    "RdYlGn", "RdYlBu", "Spectral", "viridis", "plasma",
    "inferno", "magma", "cividis", "rainbow", "jet", "turbo",
    "Set1", "Set2", "Set3", "Dark2", "Paired", "tab10", "tab20",
}
NAMED_COLORS = {
    "black", "white", "red", "green", "blue", "yellow", "orange",
    "purple", "pink", "brown", "grey", "gray", "cyan", "magenta",
}
EXCLUDED = {"scripts/_theme.py", "scripts/_components.py"}

# ────────────────── data classes ──────────────────


@dataclass
class Violation:
    file: str
    line: int
    rule: str
    severity: str
    text: str
    fix: str = ""


# ────────────────── rule scanners ──────────────────

_RULES_DOC = {
    "DS001": ("error", "Rainbow/sequential cmap em styler",
              "Cor é binária (pass/fail) ou axial. Substituir por threshold numérico ou status_pill()."),
    "DS002": ("error", "st.metric() cru",
              "Usar kpi_tile(label, value, delta=..., tone=...) de scripts._components."),
    "DS003": ("error", "Emoji-prefix em heading",
              "Heading sem emoji; estado vai em status_pill() ao lado."),
    "DS004": ("error", "px.pie() banido (anti-padrão #6 ornamental)",
              "Substituir por bar horizontal ordenada ou treemap se hierarquia."),
    "DS005": ("warn", "Plotly template cru (plotly_white/plotly_dark)",
              "Não passar template= ou usar template='ii_dark' explicitamente."),
    "DS006": ("warn", "Hex literal fora dos 5 tokens",
              "Usar COLORS['accent'|'positive'|'negative'|'warning'|'amethyst']."),
    "DS007": ("warn", "Cor por nome (black/red/blue/…)",
              "Refactor para token COLORS[...]."),
    "DS008": ("warn", "Caption >8 palavras",
              "Captions ≤8 palavras factuais. Cortar adjectivos."),
    "DS009": ("info", "Página sem inject_css()",
              "Adicionar `from scripts._theme import inject_css; inject_css()` após set_page_config."),
    "DS010": ("warn", "Skill file >500 body lines",
              "Anthropic best practice: <500 lines per skill file. "
              "Split into reference files via progressive disclosure."),
}


def _scan_line(file_rel: str, lineno: int, line: str) -> list[Violation]:
    out: list[Violation] = []
    stripped = line.strip()

    # DS001 — rainbow cmaps
    for cmap in RAINBOW_CMAPS:
        if re.search(rf'cmap\s*=\s*["\']{re.escape(cmap)}["\']', line):
            out.append(Violation(file_rel, lineno, "DS001", "error",
                                 stripped, _RULES_DOC["DS001"][2]))

    # DS002 — st.metric raw
    if re.search(r'\bst\.metric\s*\(', line):
        out.append(Violation(file_rel, lineno, "DS002", "error",
                             stripped, _RULES_DOC["DS002"][2]))

    # DS003 — emoji-prefix headings (only check call sites with literal string)
    heading_re = re.compile(
        r'\b(st\.title|st\.header|st\.subheader)\s*\(\s*(["\'])([^\2]+?)\2'
    )
    m = heading_re.search(line)
    if m:
        title_text = m.group(3)
        # presence of any non-ASCII char OR known semantic emoji at start
        first = title_text.lstrip()
        if first and ord(first[0]) > 127:
            # exception: pure language markers are also banned in headings per DS
            out.append(Violation(file_rel, lineno, "DS003", "error",
                                 stripped, _RULES_DOC["DS003"][2]))

    # markdown headers via st.markdown("# ...")
    md_h = re.search(r'st\.markdown\s*\(\s*[fr]?["\']\s*#{1,3}\s+([^"\']+)', line)
    if md_h:
        first = md_h.group(1).lstrip()
        if first and ord(first[0]) > 127:
            out.append(Violation(file_rel, lineno, "DS003", "error",
                                 stripped, _RULES_DOC["DS003"][2]))

    # DS004 — px.pie
    if re.search(r'\bpx\.pie\s*\(', line):
        out.append(Violation(file_rel, lineno, "DS004", "error",
                             stripped, _RULES_DOC["DS004"][2]))

    # DS005 — plotly default templates
    if re.search(r'template\s*=\s*["\'](plotly_white|plotly_dark|ggplot2|seaborn|simple_white)["\']', line):
        out.append(Violation(file_rel, lineno, "DS005", "warn",
                             stripped, _RULES_DOC["DS005"][2]))

    # DS006 — hex literal outside palette
    for hx in re.findall(r'["\'](#[0-9a-fA-F]{6})["\']', line):
        if hx.lower() not in {h.lower() for h in PALETTE_HEX}:
            # exclude alpha-suffixed values used in components
            out.append(Violation(file_rel, lineno, "DS006", "warn",
                                 f"{stripped[:140]}  ← {hx}", _RULES_DOC["DS006"][2]))
            break  # one per line is enough

    # DS007 — named colors in color= or line color
    for m2 in re.finditer(r'(?:color|line_color|fillcolor)\s*=\s*["\']([a-zA-Z]+)["\']', line):
        name = m2.group(1).lower()
        if name in NAMED_COLORS:
            out.append(Violation(file_rel, lineno, "DS007", "warn",
                                 stripped, _RULES_DOC["DS007"][2]))
            break

    # DS008 — caption >8 words (literal arg)
    cap = re.search(r'(section_caption|st\.caption)\s*\(\s*["\']([^"\']{4,400})["\']', line)
    if cap:
        text = cap.group(2)
        if len(text.split()) > 8:
            out.append(Violation(file_rel, lineno, "DS008", "warn",
                                 stripped[:160], _RULES_DOC["DS008"][2]))

    return out


def _scan_file(path: Path) -> tuple[list[Violation], dict]:
    """Return (violations, file_meta). file_meta has has_inject_css, has_kpi_tile_import."""
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    has_inject = "inject_css(" in text
    has_kpi_import = "kpi_tile" in text
    has_set_page = "st.set_page_config" in text
    is_streamlit_page = "import streamlit" in text and has_set_page

    violations: list[Violation] = []
    for i, line in enumerate(text.splitlines(), start=1):
        # skip comment-only lines
        if line.strip().startswith("#"):
            continue
        violations.extend(_scan_line(rel, i, line))

    # DS009 — page-level rule (file scope)
    if is_streamlit_page and not has_inject:
        violations.append(Violation(rel, 1, "DS009", "info",
                                    "set_page_config presente mas inject_css() ausente",
                                    _RULES_DOC["DS009"][2]))

    return violations, {
        "has_inject_css": has_inject,
        "has_kpi_tile_import": has_kpi_import,
        "is_streamlit_page": is_streamlit_page,
        "lines": text.count("\n") + 1,
    }


# ────────────────── DS010 — skill file length ──────────────────

_SKILLS_ROOT = ROOT / "obsidian_vault" / "skills"
_DS010_SKIP_DIR = _SKILLS_ROOT / "Helena_Mega"
_DS010_SKIP_TYPES = {"roadmap", "master_plan"}
_DS010_BODY_LIMIT = 500


def _count_body_lines(text: str) -> int:
    """Count non-blank lines, excluding YAML frontmatter (first --- ... --- block)."""
    lines = text.splitlines()
    in_front = False
    front_done = False
    body: list[str] = []
    for i, ln in enumerate(lines):
        if i == 0 and ln.strip() == "---":
            in_front = True
            continue
        if in_front and ln.strip() == "---":
            in_front = False
            front_done = True
            continue
        if in_front:
            continue
        body.append(ln)
    # if no closing --- found, treat whole file as body
    if in_front:
        body = lines
    return sum(1 for ln in body if ln.strip())


def _get_frontmatter_type(text: str) -> str | None:
    """Extract 'type' field from YAML frontmatter, or None."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        m = re.match(r"^type\s*:\s*(.+)$", ln.strip())
        if m:
            return m.group(1).strip().strip('"\'')
    return None


def scan_skills_files() -> list[Violation]:
    """DS010 — scan obsidian_vault/skills/**/*.md for files exceeding body line limit."""
    violations: list[Violation] = []
    if not _SKILLS_ROOT.is_dir():
        return violations
    for path in sorted(_SKILLS_ROOT.rglob("*.md")):
        # skip Helena_Mega auto-generated reports
        try:
            path.relative_to(_DS010_SKIP_DIR)
            continue
        except ValueError:
            pass
        text = path.read_text(encoding="utf-8", errors="replace")
        fm_type = _get_frontmatter_type(text)
        if fm_type in _DS010_SKIP_TYPES:
            continue
        n = _count_body_lines(text)
        if n > _DS010_BODY_LIMIT:
            rel = path.relative_to(ROOT).as_posix()
            violations.append(Violation(
                file=rel,
                line=1,
                rule="DS010",
                severity="warn",
                text=(
                    f"Skill file {rel} has {n} body lines — "
                    "Anthropic best practice recommends <500. "
                    "Consider progressive disclosure (split into reference files)."
                ),
                fix=_RULES_DOC["DS010"][2],
            ))
    return violations


# ────────────────── targets ──────────────────


def collect_targets(paths: list[str] | None = None) -> list[Path]:
    """Return list of .py files to scan, filtering EXCLUDED."""
    if not paths:
        paths = ["scripts"]
    targets: list[Path] = []
    for p in paths:
        base = ROOT / p
        if base.is_file() and base.suffix == ".py":
            targets.append(base)
        elif base.is_dir():
            targets.extend(base.rglob("*.py"))
    out = []
    for t in targets:
        rel = t.relative_to(ROOT).as_posix()
        if rel in EXCLUDED:
            continue
        if "__pycache__" in rel or "/.venv/" in rel:
            continue
        out.append(t)
    return sorted(out)


# ────────────────── render ──────────────────


def render_md(violations: list[Violation], file_meta: dict[str, dict],
              targets: list[Path]) -> str:
    by_rule: dict[str, list[Violation]] = {}
    by_file: dict[str, list[Violation]] = {}
    for v in violations:
        by_rule.setdefault(v.rule, []).append(v)
        by_file.setdefault(v.file, []).append(v)

    severities = {"error": 0, "warn": 0, "info": 0}
    for v in violations:
        severities[v.severity] = severities.get(v.severity, 0) + 1

    from datetime import date
    today = date.today().isoformat()

    out = [
        "---",
        "type: design_audit",
        f"updated: {today}",
        "owner: helena_linha",
        "tags: [design, audit, helena, mega]",
        "---",
        "",
        "# 01 — Design audit",
        "",
        f"> Helena Mega · run **{today}** · {len(targets)} ficheiros · "
        f"**{len(violations)}** violações "
        f"({severities['error']} errors / {severities['warn']} warns / {severities['info']} info)",
        "",
        "## Resumo executivo",
        "",
    ]

    if not violations:
        out.append("**Zero violações.** Design system aplicado em 100% do scope. 🟢")
    else:
        out.append("Distribuição por regra:")
        out.append("")
        out.append("| Regra | Severidade | Descrição | Hits |")
        out.append("|---|---|---|---:|")
        for rid, _spec in _RULES_DOC.items():
            sev, desc, _fix = _spec
            n = len(by_rule.get(rid, []))
            mark = "🔴" if sev == "error" and n else ("🟡" if sev == "warn" and n else
                                                      ("⚪" if sev == "info" else "🟢"))
            out.append(f"| `{rid}` | {sev} {mark} | {desc} | {n} |")

        out.append("")
        out.append("Top 10 ficheiros com mais violações:")
        out.append("")
        ranked = sorted(by_file.items(), key=lambda kv: -len(kv[1]))[:10]
        out.append("| Ficheiro | Violações | Linhas |")
        out.append("|---|---:|---:|")
        for f, vs in ranked:
            lines = file_meta.get(f, {}).get("lines", 0)
            out.append(f"| `{f}` | {len(vs)} | {lines} |")

    out += ["", "## Detalhe por regra", ""]
    for rid in _RULES_DOC.keys():
        rows = by_rule.get(rid, [])
        if not rows:
            continue
        sev, desc, fix = _RULES_DOC[rid]
        out += [
            f"### `{rid}` — {desc}  _({sev}, {len(rows)} hits)_",
            "",
            f"**Fix sugerido**: {fix}",
            "",
            "| Ficheiro | Linha | Trecho |",
            "|---|---:|---|",
        ]
        for v in rows[:50]:
            txt = v.text.replace("|", "\\|")[:140]
            out.append(f"| `{v.file}` | {v.line} | `{txt}` |")
        if len(rows) > 50:
            out.append(f"| _(+{len(rows)-50} mais)_ | | |")
        out.append("")

    out += [
        "## Cobertura de design system por ficheiro",
        "",
        "| Ficheiro | inject_css? | kpi_tile import? | Streamlit page? | LoC |",
        "|---|---|---|---|---:|",
    ]
    for t in targets:
        rel = t.relative_to(ROOT).as_posix()
        meta = file_meta.get(rel, {})
        if not meta.get("is_streamlit_page"):
            continue
        ic = "✅" if meta.get("has_inject_css") else "❌"
        kp = "✅" if meta.get("has_kpi_tile_import") else "·"
        out.append(f"| `{rel}` | {ic} | {kp} | ✅ | {meta.get('lines', 0)} |")

    out += [
        "",
        "## Cross-links",
        "",
        "- [[Design_System]] — fonte das regras",
        "- [[../scripts/_theme.py]] — tokens canónicos",
        "- [[../scripts/_components.py]] — helpers `kpi_tile`, `status_pill`, …",
        "- [[Helena Linha]] — owner",
        "",
    ]

    return "\n".join(out)


# ────────────────── main ──────────────────


def run(paths: list[str] | None = None) -> tuple[list[Violation], dict, list[Path]]:
    targets = collect_targets(paths)
    all_v: list[Violation] = []
    file_meta: dict[str, dict] = {}
    for t in targets:
        v, meta = _scan_file(t)
        all_v.extend(v)
        file_meta[t.relative_to(ROOT).as_posix()] = meta
    # DS010 — skill file length (separate scope: obsidian_vault/skills/)
    all_v.extend(scan_skills_files())
    return all_v, file_meta, targets


def main() -> int:
    import sys
    ap = argparse.ArgumentParser(description="Helena design audit")
    ap.add_argument("--print", action="store_true", help="stdout only, no write")
    ap.add_argument("--paths", nargs="*", default=["scripts"])
    args = ap.parse_args()

    violations, file_meta, targets = run(args.paths)
    md = render_md(violations, file_meta, targets)

    if args.print:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        sys.stdout.write(md + "\n")
        return 0

    out_path = VAULT_OUT / "01_Audit.md"
    out_path.write_text(md, encoding="utf-8")
    sev = sum(1 for v in violations if v.severity == "error")
    print(f"wrote {out_path.relative_to(ROOT)} · {len(violations)} violations ({sev} errors) "
          f"in {len(targets)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
