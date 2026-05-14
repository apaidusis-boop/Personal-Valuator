"""Inject `handle:` front-matter into each obsidian_vault/agents/personas/<Name>.md
file so Obsidian search by canonical handle (area.funcao) lands the persona note.

Aligns with feedback rule `feedback_agent_function_names`: use handle, not persona.
Non-destructive: only adds `handle:` line if missing. Pasta names kept (would break links).
"""
from __future__ import annotations
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from pathlib import Path

PERSONAS = Path("obsidian_vault/agents/personas")

# persona file stem -> canonical handle (from AGENTS_REGISTRY.md)
MAPPING = {
    "Aderbaldo Cíclico": "council.commodities-br",
    "Aristóteles Backtest": "perf.backtest-analysts",
    "Aurora Matina": "ops.briefing",
    "Charlie Compounder": "council.industrials-us",
    "Clara Fit": "perf.portfolio-matcher",
    "Diabo Silva": "risk.devils-advocate",
    "Diego Bancário": "council.banks-br",
    "Hank Tier-One": "council.banks-us",
    "Helena Linha": "design.lint",  # primary handle (also design.scout, design.curate, design.spike)
    "Lourdes Aluguel": "council.fiis-br",
    "Mariana Macro": "council.macro",
    "Noé Arquivista": "ops.janitor",
    "Pedro Alocação": "council.allocation",
    "Regina Ordem": "risk.compliance",
    "Sofia Clippings": "research.subscriptions",
    "Teresa Tese": "research.thesis-refresh",
    "Tião Galpão": "council.industrials-br",
    "Ulisses Navegador": "research.scout",
    "Valentina Prudente": "risk.drift-audit",
    "Vitória Vitrine": "design.product",  # aspirational, not in registry
    "Walter Triple-Net": "council.reits-us",
    "Wilson Vigil": "ops.watchdog",
    "Zé Mensageiro": "ops.telegram-bridge",
}


def inject_handle(path: Path, handle: str) -> bool:
    """Add `handle: <handle>` to front-matter if missing. Returns True if edited."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "handle:" in text.splitlines()[:25]:
        return False
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        # No front-matter — wrap one
        new = f"---\nhandle: {handle}\ntype: persona\ntags: [persona, legacy_name_alias]\n---\n\n" + text
        path.write_text(new, encoding="utf-8")
        return True
    # find closing ---
    end = next((i for i, ln in enumerate(lines[1:], start=1) if ln == "---"), None)
    if end is None:
        return False
    # insert `handle:` right after opening ---
    lines.insert(1, f"handle: {handle}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def main() -> None:
    edited = 0
    skipped = 0
    missing = 0
    for stem, handle in MAPPING.items():
        p = PERSONAS / f"{stem}.md"
        if not p.exists():
            print(f"MISS  {stem}")
            missing += 1
            continue
        if inject_handle(p, handle):
            print(f"OK    {stem}  ->  handle: {handle}")
            edited += 1
        else:
            print(f"skip  {stem}  (already has handle)")
            skipped += 1
    print(f"\n{edited} edited · {skipped} skipped · {missing} missing")


if __name__ == "__main__":
    main()
