"""Global wikilink rewriter — kills ghost graph nodes in Obsidian.

After Wave 3 (deep merge), per-ticker source files were buried. But notes
across the vault still contain wikilinks like [[JNJ_DOSSIE]] / [[JNJ_STORY]] /
[[Charlie Compounder]] / [[JNJ_2026-05-01]]. Obsidian renders each as an
"unresolved" graph node — exactly the scatter the user keeps seeing.

This script rewrites those wikilinks to canonical targets:
  - [[<TK>_<SUFFIX>]]    -> [[<TK>]]              (ticker hub)
  - [[<TK>_<DATE>]]      -> [[<TK>]]              (dated council review)
  - [[<TK>_<SUFFIX>|x]]  -> [[<TK>|x]]            (preserve display text)
  - [[<Persona>]]        -> [[<handle>]]          (23 mappings)

SUFFIX is one of:
  DOSSIE · STORY · COUNCIL · IC_DEBATE · VARIANT · RI · drip · FILING_<DATE> ·
  MIGRATION · CONTENT_TRIGGER_<DATE> · PATRIA_TRANSITION · <YYYY-MM-DD>

Idempotent: re-run is a no-op once everything is rewritten.
"""
from __future__ import annotations
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import re
import yaml
from pathlib import Path
from collections import defaultdict

VAULT = Path("obsidian_vault")

PERSONA_MAP = {
    "Aderbaldo Cíclico": "council.commodities-br",
    "Aristóteles Backtest": "perf.backtest-analysts",
    "Aurora Matina": "ops.briefing",
    "Charlie Compounder": "council.industrials-us",
    "Clara Fit": "perf.portfolio-matcher",
    "Diabo Silva": "risk.devils-advocate",
    "Diego Bancário": "council.banks-br",
    "Hank Tier-One": "council.banks-us",
    "Helena Linha": "design.lint",
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
    "Vitória Vitrine": "design.product",
    "Walter Triple-Net": "council.reits-us",
    "Wilson Vigil": "ops.watchdog",
    "Zé Mensageiro": "ops.telegram-bridge",
}

# Known stray tickers (not in universe but tracked)
STRAY_TICKERS = {"SPY", "VOO", "BOVA11", "BTLG12", "MCRF11", "BF-B"}

# Suffix patterns: anything after <TK>_ that maps back to the ticker hub
SUFFIX_PATTERN = re.compile(
    r"^("
    r"DOSSIE"
    r"|STORY"
    r"|COUNCIL"
    r"|IC[_ ]DEBATE"
    r"|VARIANT"
    r"|RI"
    r"|drip"
    r"|FILING(?:_\d{4}-\d{2}-\d{2})?"
    r"|MIGRATION"
    r"|CONTENT_TRIGGER(?:_\d{4}-\d{2}-\d{2})?"
    r"|PATRIA_TRANSITION"
    r"|\d{4}-\d{2}-\d{2}"  # dated review
    r")$",
    re.IGNORECASE,
)


def load_universe() -> set[str]:
    out: set[str] = set()
    with open("config/universe.yaml", "r", encoding="utf-8") as f:
        u = yaml.safe_load(f)
    for market in ("br", "us"):
        m = u.get(market, {})
        for bucket in ("holdings", "watchlist", "research_pool"):
            stack = [m.get(bucket, {})]
            while stack:
                cur = stack.pop()
                if isinstance(cur, dict):
                    stack.extend(cur.values())
                elif isinstance(cur, list):
                    for item in cur:
                        if isinstance(item, dict) and "ticker" in item:
                            out.add(item["ticker"])
                        else:
                            stack.append(item)
    if Path("config/kings_aristocrats.yaml").exists():
        with open("config/kings_aristocrats.yaml", "r", encoding="utf-8") as f:
            k = yaml.safe_load(f)
        for item in k.get("tickers", []):
            out.add(item["ticker"])
    out |= STRAY_TICKERS
    return out


def rewrite_target(target: str, tickers: set[str]) -> str | None:
    """Return rewritten target, or None if no rewrite applies."""
    # Strip optional path prefix like "../agents/personas/Helena Linha" or "hubs/JNJ"
    raw = target.split("/")[-1] if "/" in target else target
    # Persona names → handles (check both full target and stripped basename)
    if target in PERSONA_MAP:
        return PERSONA_MAP[target]
    if raw in PERSONA_MAP:
        return PERSONA_MAP[raw]
    # Ticker_SUFFIX → ticker
    # Match against both case-sensitive and prefix-of-token strategies
    # Strategy: longest-matching ticker prefix that has _<SUFFIX> after
    for tk in sorted(tickers, key=len, reverse=True):
        if raw == tk:
            # Plain [[JNJ]] — already canonical (return canonical to handle path-prefixed form)
            return tk if "/" in target else None
        prefix = f"{tk}_"
        if raw.startswith(prefix):
            suffix = raw[len(prefix):]
            if SUFFIX_PATTERN.match(suffix):
                return tk
    # Hyphenated tickers (BRK-B, BF-B) need explicit handling
    for tk in sorted(tickers, key=len, reverse=True):
        if "-" in tk and raw.startswith(tk + "_"):
            suffix = raw[len(tk) + 1:]
            if SUFFIX_PATTERN.match(suffix):
                return tk
    return None


WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(\|([^\]]+))?\]\]")


def rewrite_text(text: str, tickers: set[str], stats: dict) -> tuple[str, int]:
    """Rewrite all wikilinks in `text`. Return (new_text, n_changed)."""
    n_changed = 0

    def _repl(m: re.Match) -> str:
        nonlocal n_changed
        target = m.group(1).strip()
        anchor = m.group(2) or ""
        display = m.group(4)
        new = rewrite_target(target, tickers)
        if new is None or new == target:
            return m.group(0)
        n_changed += 1
        stats[(target, new)] += 1
        if display:
            return f"[[{new}{anchor}|{display}]]"
        return f"[[{new}{anchor}]]"

    new_text = WIKILINK_RE.sub(_repl, text)
    return new_text, n_changed


SKIP_DIRS = {"cemetery", ".obsidian", ".git"}
SKIP_PREFIXES = {"skills/imported"}  # absorbed plugin docs — leave alone
# Cleanup reports document the rewrite operation itself; if rewriter touches them
# they become self-referential (e.g. "[[council.industrials-us]] -> [[council.industrials-us]]").
SKIP_FILE_PATTERNS = ("Cleanup_2026-05-", "Cleanup_Overnight_")


def should_skip(rel: Path) -> bool:
    parts = rel.parts
    if any(p in SKIP_DIRS for p in parts):
        return True
    s = str(rel).replace("\\", "/")
    if any(s.startswith(p) for p in SKIP_PREFIXES):
        return True
    return any(rel.name.startswith(p) for p in SKIP_FILE_PATTERNS)


def main() -> None:
    tickers = load_universe()
    print(f"Universe: {len(tickers)} tickers (+{len(PERSONA_MAP)} persona mappings)")

    files_changed = 0
    total_links_changed = 0
    stats: dict[tuple[str, str], int] = defaultdict(int)

    for p in VAULT.rglob("*.md"):
        rel = p.relative_to(VAULT)
        if should_skip(rel):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        new_text, n = rewrite_text(text, tickers, stats)
        if n > 0:
            p.write_text(new_text, encoding="utf-8")
            files_changed += 1
            total_links_changed += n

    print(f"Files changed: {files_changed}")
    print(f"Wikilinks rewritten: {total_links_changed}")

    # Top rewrites by frequency
    print("\nTop 30 rewrites:")
    top = sorted(stats.items(), key=lambda x: -x[1])[:30]
    for (old, new), cnt in top:
        print(f"  {cnt:5d}  [[{old}]] → [[{new}]]")


if __name__ == "__main__":
    main()
