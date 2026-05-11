"""notes — notas por ticker (tese, observações, triggers mentais).

Storage: `memory/notes/<ticker>.md` (mesmo vault que auto-memory).
Schema: YAML frontmatter + markdown body. Apêndice append-only por data.

Integrado em research.py::load_ticker_notes() → secção [8] User Notes.

Uso:
    python scripts/notes_cli.py add ACN "Compra em Mai/24 a $299; tese consulting turnaround"
    python scripts/notes_cli.py show ACN
    python scripts/notes_cli.py list
    python scripts/notes_cli.py list --holdings
    python scripts/notes_cli.py tag ACN turnaround,consulting,buffett
    python scripts/notes_cli.py archive ACN          # remove (preserva ficheiro em _archive/)
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def _memory_dir() -> Path:
    """Resolve memory dir from the harness convention."""
    # Project-level memory dir convention used by Claude Code:
    # C:\Users\<user>\.claude\projects\<slug>\memory\
    home = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or "")
    slug = "C--Users-paidu-investment-intelligence"
    candidate = home / ".claude" / "projects" / slug / "memory"
    if candidate.exists():
        return candidate
    # Fallback: local memory/ next to project
    local = ROOT / "memory"
    local.mkdir(exist_ok=True)
    return local


NOTES_DIR = _memory_dir() / "notes"
NOTES_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR = NOTES_DIR / "_archive"


def _slug(ticker: str) -> str:
    return ticker.strip().upper().replace("/", "_")


def _note_path(ticker: str) -> Path:
    return NOTES_DIR / f"{_slug(ticker)}.md"


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def _parse(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_raw, body = m.group(1), m.group(2)
    fm: dict = {}
    for line in fm_raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm, body


def _serialize(fm: dict, body: str) -> str:
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + body


def read_note(ticker: str) -> tuple[dict, str] | None:
    p = _note_path(ticker)
    if not p.exists():
        return None
    return _parse(p.read_text(encoding="utf-8"))


def _get_ticker_meta(ticker: str) -> dict:
    """Puxa meta básica do DB para frontmatter."""
    meta = {"ticker": ticker, "market": "unknown"}
    from scripts.refresh_ticker import _market_of  # reuse
    meta["market"] = _market_of(ticker)
    db_path = ROOT / "data" / f"{meta['market']}_investments.db"
    if not db_path.exists():
        return meta
    with sqlite3.connect(db_path) as c:
        row = c.execute(
            "SELECT name, sector, is_holding FROM companies WHERE ticker=?", (ticker,)
        ).fetchone()
        if row:
            meta["name"] = row[0]
            meta["sector"] = row[1] or ""
            meta["is_holding"] = str(int(bool(row[2])))
    return meta


def add_note(ticker: str, text: str, tags: list[str] | None = None) -> Path:
    ticker = _slug(ticker)
    existing = read_note(ticker)
    if existing:
        fm, body = existing
    else:
        meta = _get_ticker_meta(ticker)
        fm = {
            "ticker": meta.get("ticker", ticker),
            "name": meta.get("name", ""),
            "market": meta.get("market", ""),
            "sector": meta.get("sector", ""),
            "is_holding": meta.get("is_holding", "0"),
            "created": date.today().isoformat(),
            "updated": date.today().isoformat(),
            "tags": ",".join(tags or []),
        }
        body = "\n"
    # Always update `updated`
    fm["updated"] = date.today().isoformat()
    if tags:
        existing_tags = {t.strip() for t in fm.get("tags", "").split(",") if t.strip()}
        existing_tags.update(tags)
        fm["tags"] = ",".join(sorted(existing_tags))

    body = body.rstrip() + f"\n\n### {date.today().isoformat()}\n{text.strip()}\n"
    p = _note_path(ticker)
    p.write_text(_serialize(fm, body), encoding="utf-8")
    return p


def set_tags(ticker: str, tags: list[str], replace: bool = False) -> Path | None:
    existing = read_note(ticker)
    if not existing:
        return None
    fm, body = existing
    if replace:
        fm["tags"] = ",".join(tags)
    else:
        cur = {t.strip() for t in fm.get("tags", "").split(",") if t.strip()}
        cur.update(tags)
        fm["tags"] = ",".join(sorted(cur))
    fm["updated"] = date.today().isoformat()
    p = _note_path(ticker)
    p.write_text(_serialize(fm, body), encoding="utf-8")
    return p


def show_note(ticker: str) -> None:
    res = read_note(ticker)
    if res is None:
        print(f"(nenhuma nota para {ticker})")
        return
    fm, body = res
    print(f"=== {ticker}  ({fm.get('name','')}) ===")
    for k, v in fm.items():
        print(f"  {k}: {v}")
    print("-" * 60)
    print(body.strip())


def list_notes(holdings_only: bool = False) -> None:
    if not NOTES_DIR.exists():
        print("(sem notas)")
        return
    rows = []
    for p in sorted(NOTES_DIR.glob("*.md")):
        if p.name.startswith("_"):
            continue
        res = _parse(p.read_text(encoding="utf-8"))
        fm, _ = res
        if holdings_only and fm.get("is_holding") != "1":
            continue
        rows.append((p.stem, fm.get("is_holding", "0"), fm.get("tags", ""), fm.get("updated", "")))
    if not rows:
        print("(nenhuma nota match)")
        return
    print(f"{'TICKER':<10} {'H':<3} {'UPDATED':<12} TAGS")
    for r in rows:
        h = "★" if r[1] == "1" else " "
        print(f"  {r[0]:<8} {h:<3} {r[3]:<12} {r[2]}")


def archive_note(ticker: str) -> bool:
    p = _note_path(ticker)
    if not p.exists():
        return False
    ARCHIVE_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.move(str(p), str(ARCHIVE_DIR / f"{_slug(ticker)}_{stamp}.md"))
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="Append note for ticker")
    a.add_argument("ticker")
    a.add_argument("text", nargs="+", help="Note text (quoted or joined)")
    a.add_argument("--tags", help="Comma-separated tags to add")

    s = sub.add_parser("show", help="Show full note for ticker")
    s.add_argument("ticker")

    l = sub.add_parser("list", help="List all notes")
    l.add_argument("--holdings", action="store_true", help="Only holdings")

    t = sub.add_parser("tag", help="Add tags to a ticker's note")
    t.add_argument("ticker")
    t.add_argument("tags", help="Comma-separated tags")
    t.add_argument("--replace", action="store_true", help="Replace existing tags")

    arch = sub.add_parser("archive", help="Move note to _archive/")
    arch.add_argument("ticker")

    args = ap.parse_args()

    from analytics.obsidian_link import print_saved
    if args.cmd == "add":
        text = " ".join(args.text)
        tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
        p = add_note(args.ticker, text, tags)
        print_saved(p, prefix="wrote")
    elif args.cmd == "show":
        show_note(args.ticker)
    elif args.cmd == "list":
        list_notes(holdings_only=args.holdings)
    elif args.cmd == "tag":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        p = set_tags(args.ticker, tags, replace=args.replace)
        if p is None:
            print(f"(nota de {args.ticker} não existe — usa 'add' primeiro)")
            return 1
        print_saved(p, prefix="updated")
    elif args.cmd == "archive":
        ok = archive_note(args.ticker)
        print("archived" if ok else "(nada a arquivar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
