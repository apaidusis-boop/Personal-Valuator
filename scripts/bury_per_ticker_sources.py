"""After hubs/<TK>.md absorb per-ticker content, bury the source files.

Categories targeted (all per-ticker):
  - dossiers/<TK>*.md                          -> ABSORBED-dossiers/
  - tickers/<TK>*.md                            -> ABSORBED-tickers/
  - agents/<Persona>/reviews/<TK>_*.md          -> ABSORBED-council-reviews/
  - briefings/drip_scenarios/<TK>_drip.md       -> ABSORBED-drip/
  - briefings/earnings_prep_<TK>_*.md (past)    -> ABSORBED-earnings-prep/
  - wiki/holdings/<TK>.md                       -> ABSORBED-wiki-holdings/
  - Sessions/<TK>_*.md                          -> ABSORBED-sessions-per-ticker/
  - Overnight_<DATE>/<TK>.md                    -> ABSORBED-overnight-per-ticker/
  - Pilot_Deep_Dive_<DATE>/<TK>.md              -> ABSORBED-pilot-per-ticker/

Excluded (keep):
  - Files at vault root (_MASTER, _LEITURA_DA_MANHA, _BOM_DIA, ...)
  - Files starting with `_` (hub-style entry points)
  - Files in `hubs/` (the new home)
  - Files in `cemetery/` (already buried)
  - Files in `Bibliotheca/`, `Glossary/`, `Clippings/`, `videos/` (cross-ref / external)
  - `wiki/` non-holdings subfolders (sectors, macro, methods, playbooks, tax, cycles, history)
  - `agents/personas/*.md` (handled in persona purge phase)
  - `agents/<Persona>/_reviews_index.md` (folder index, not per-ticker)
  - `Sessions/` non-ticker (e.g., `FairValue_Forward_Audit_2026-05-11.md`)
"""
from __future__ import annotations
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import re
import subprocess
import yaml
from pathlib import Path
from datetime import datetime, date

VAULT = Path("obsidian_vault")
CEMETERY = Path("cemetery/2026-05-14")
TODAY = date.today()


def universe_tickers() -> set[str]:
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
    return out


def classify_for_burial(rel: Path, tickers: set[str]) -> tuple[str, str] | None:
    """Decide if this rel-path is a per-ticker source.

    Return (cemetery_subdir, reason) or None to skip.
    """
    s = str(rel).replace("\\", "/")
    name = rel.name
    stem = rel.stem.upper()
    # Skip protected paths
    if s.startswith("Bibliotheca/"): return None
    if s.startswith("Glossary/"): return None
    if s.startswith("Clippings/"): return None
    if s.startswith("videos/"): return None
    if s.startswith("Comercial/"): return None
    if s.startswith("dashboards/"): return None
    if s.startswith("skills/"): return None
    if s.startswith("specs/"): return None
    if s.startswith("workspace/"): return None
    if s.startswith("feedback/"): return None
    if s.startswith("data/"): return None
    if s.startswith("reference/"): return None
    if s.startswith("analysts/"): return None
    if s.startswith("agents/personas/"): return None  # handled separately
    if s.startswith("hubs/"): return None
    if s.startswith("_"): return None
    if name.startswith("_"): return None  # _MASTER, _LEITURA_DA_MANHA, _BOM_DIA, etc.

    # tokenize stem and check if any token is a known ticker
    parts = re.split(r"[_\-\.\s]", stem)
    matched_tk = None
    for p in parts:
        if p in tickers:
            matched_tk = p
            break
    # Also try the prefix-before-first-underscore (handles hyphenated tickers like BRK-B)
    if matched_tk is None:
        prefix = stem.split("_")[0]  # e.g. "BRK-B" from "BRK-B_FILING_2026-05-07"
        if prefix in tickers:
            matched_tk = prefix
    # Watchlist/index tickers not in universe but real (benchmarks/etfs/migrations)
    if matched_tk is None:
        STRAY = {"BRK-B", "BF-B", "BOVA11", "BTLG12", "MCRF11", "SPY", "VOO"}
        prefix = stem.split("_")[0]
        if prefix in STRAY:
            matched_tk = prefix

    # Folder/agent reviews
    if s.startswith("agents/") and "/reviews/" in s and matched_tk:
        return ("ABSORBED-council-reviews", f"per-ticker {matched_tk} review absorbed into hub")
    # Folder/agent root files we leave alone unless per-ticker
    if s.startswith("agents/") and not matched_tk:
        return None

    if matched_tk is None:
        # No ticker token — leave
        return None

    if s.startswith("dossiers/"):
        return ("ABSORBED-dossiers", f"per-ticker dossier for {matched_tk} absorbed into hub")
    if s.startswith("tickers/"):
        return ("ABSORBED-tickers", f"per-ticker view {matched_tk} absorbed into hub")
    if s.startswith("briefings/drip_scenarios/"):
        return ("ABSORBED-drip", f"DRIP scenario {matched_tk} absorbed into hub")
    if s.startswith("briefings/earnings_prep_"):
        # earnings prep — only bury past dates
        m = re.search(r"earnings_prep_[A-Z0-9-]+_(20\d{2}-\d{2}-\d{2})\.md$", name)
        if m:
            try:
                d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
                if d < TODAY:
                    return ("ABSORBED-earnings-prep", f"past earnings prep {matched_tk}")
            except ValueError:
                pass
        return None
    if s.startswith("wiki/holdings/"):
        return ("ABSORBED-wiki-holdings", f"wiki playbook {matched_tk} absorbed into hub")
    if s.startswith("Sessions/"):
        # only bury if it's per-ticker (filename contains ticker as a standalone token)
        return ("ABSORBED-sessions-per-ticker", f"session note {matched_tk} absorbed into hub")
    if s.startswith("Overnight_") and name != "_MASTER.md" and name != "_LEITURA_DA_MANHA.md" and name != "_BOM_DIA.md":
        return ("ABSORBED-overnight-per-ticker", f"overnight per-ticker {matched_tk} absorbed into hub")
    if s.startswith("Pilot_Deep_Dive_"):
        return ("ABSORBED-pilot-per-ticker", f"pilot per-ticker {matched_tk} absorbed into hub")

    return None


def git_mv(src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(["git", "mv", str(src), str(dst)], capture_output=True, text=True)
        if r.returncode == 0:
            return True
        # untracked file fallback: plain mv
        if "not under version control" in (r.stderr or "") or "did not match any files" in (r.stderr or "") or "fatal:" in (r.stderr or ""):
            try:
                src.rename(dst)
                return True
            except Exception:
                return False
        return False
    except Exception:
        return False


def main() -> None:
    tickers = universe_tickers()
    print(f"Universe: {len(tickers)} tickers")

    plan: list[tuple[Path, Path, str]] = []
    for p in VAULT.rglob("*.md"):
        if "cemetery" in p.parts:
            continue
        rel = p.relative_to(VAULT)
        cls = classify_for_burial(rel, tickers)
        if cls is None:
            continue
        sub, reason = cls
        dst = CEMETERY / sub / rel
        plan.append((p, dst, reason))

    print(f"Plan: bury {len(plan)} files")
    # Group counts
    from collections import Counter
    groups = Counter(p[1].parts[2] for p in plan)
    for g, n in sorted(groups.items(), key=lambda x: -x[1]):
        print(f"  {g}: {n}")

    # Execute
    ok = fail = 0
    failures: list[str] = []
    manifest_entries: list[str] = []
    for src, dst, reason in plan:
        if git_mv(src, dst):
            ok += 1
            rel = src.relative_to(Path.cwd()) if src.is_absolute() else src
            manifest_entries.append(f"- `{rel}` → `{dst}` — {reason}")
        else:
            fail += 1
            failures.append(str(src))

    print(f"\nResult: {ok} buried, {fail} failed")
    if failures:
        print("Failures:")
        for f in failures[:20]:
            print(f"  {f}")

    # Append to manifest
    manifest = CEMETERY / "manifest.md"
    with manifest.open("a", encoding="utf-8") as f:
        f.write("\n\n### Wave 8 — Per-ticker SOURCE files (merge-total absorbed into hubs)\n")
        f.write(f"Date: {TODAY.isoformat()}\n")
        f.write(f"Total: {ok} files moved across {len(groups)} categories.\n")
        f.write("Each ticker's content was first absorbed into `obsidian_vault/hubs/<TK>.md` (merge-total) before burial here.\n")
        f.write("Restore command pattern: `git mv cemetery/2026-05-14/<SUBDIR>/<ORIGINAL_PATH> <ORIGINAL_PATH>`\n\n")
        for line in manifest_entries[:500]:  # cap detail
            f.write(line + "\n")
        if len(manifest_entries) > 500:
            f.write(f"\n_(+{len(manifest_entries)-500} more — see git history)_\n")


if __name__ == "__main__":
    main()
