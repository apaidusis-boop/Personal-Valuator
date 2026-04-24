"""vault_clean_video_names — rename videos/<id>.md → <date>_<channel>_<slug>.md.

Lê frontmatter YAML + primeira heading dos ficheiros em `obsidian_vault/videos/`,
computa nome legível, adiciona `video_id` como alias do Obsidian (preserva links
antigos), e renomeia. Idempotente — se já está no formato novo, skip.

Uso:
    python scripts/vault_clean_video_names.py                 # dry-run
    python scripts/vault_clean_video_names.py --apply         # executar
    python scripts/vault_clean_video_names.py --vault <path>  # override

Naming convention:
    <YYYY-MM-DD>_<ChannelSlug>_<TitleSlugTruncated>.md
    Ex: 2026-04-19_StockPickers_aegea-aegp23-aegpa3-oportunidade.md
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def _vault_path(override: str | None = None) -> Path:
    if override:
        return Path(override).expanduser().resolve()
    envp = os.environ.get("OBSIDIAN_VAULT_PATH")
    if envp:
        return Path(envp).expanduser().resolve()
    return ROOT / "obsidian_vault"


def _slugify(s: str, maxlen: int = 60) -> str:
    """ASCII-safe slug, lowercase, hyphens, truncated."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:maxlen].rstrip("-")


def _parse_video_md(path: Path) -> dict | None:
    """Parse frontmatter + first heading. Returns None if not recognizable."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    if not text.startswith("---"):
        return None
    # split frontmatter
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm_block, body = parts[1], parts[2]
    meta: dict = {"_raw": text, "_fm_block": fm_block, "_body": body}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip("\"'")
    # first heading
    m = re.search(r"^#\s+(?:🎬\s*)?(.+?)\s*$", body, re.MULTILINE)
    if m:
        meta["_title"] = m.group(1).strip()
    return meta


def _compute_new_name(meta: dict) -> str | None:
    vid = meta.get("video_id")
    if not vid:
        return None
    date = meta.get("published_at", "")
    channel = _slugify(meta.get("channel", ""), maxlen=25)
    title_src = meta.get("_title") or meta.get("title") or vid
    title = _slugify(title_src, maxlen=70)
    pieces = [p for p in (date, channel, title) if p]
    return "_".join(pieces) + ".md"


def _update_frontmatter_with_alias(fm_block: str, video_id: str) -> str:
    """Ensure `aliases: [<video_id>]` is present. Preserve everything else."""
    lines = fm_block.strip().splitlines()
    has_aliases = any(re.match(r"^\s*aliases\s*:", ln) for ln in lines)
    if has_aliases:
        # Ensure video_id is in the list
        out = []
        for ln in lines:
            m = re.match(r"^(\s*aliases\s*:\s*)\[(.*)\]\s*$", ln)
            if m:
                prefix, items = m.group(1), m.group(2)
                existing = {x.strip().strip("\"'") for x in items.split(",") if x.strip()}
                if video_id not in existing:
                    existing.add(video_id)
                items = ", ".join(sorted(existing))
                out.append(f"{prefix}[{items}]")
            else:
                out.append(ln)
        return "\n".join(out)
    # no aliases key yet — add after first line (which is 'type:' typically)
    insert_idx = 1 if lines else 0
    lines.insert(insert_idx, f"aliases: [{video_id}]")
    return "\n".join(lines)


def clean_videos(vault: Path, apply: bool = False) -> list[tuple[str, str, str]]:
    videos_dir = vault / "videos"
    if not videos_dir.is_dir():
        print(f"[!] no videos dir at {videos_dir}")
        return []
    changes: list[tuple[str, str, str]] = []  # (old, new, status)
    for p in sorted(videos_dir.glob("*.md")):
        meta = _parse_video_md(p)
        if not meta:
            continue
        new_name = _compute_new_name(meta)
        if not new_name:
            continue
        if new_name == p.name:
            continue  # already clean
        vid = meta["video_id"]
        new_fm = _update_frontmatter_with_alias(meta["_fm_block"], vid)
        new_text = f"---\n{new_fm}\n---{meta['_body']}"
        new_path = videos_dir / new_name
        if new_path.exists() and new_path != p:
            changes.append((p.name, new_name, "CONFLICT — target exists"))
            continue
        if apply:
            new_path.write_text(new_text, encoding="utf-8")
            p.unlink()
            changes.append((p.name, new_name, "renamed"))
        else:
            changes.append((p.name, new_name, "would rename"))
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--vault", help="override vault path")
    ap.add_argument("--apply", action="store_true", help="execute renames (default dry-run)")
    args = ap.parse_args()
    vault = _vault_path(args.vault)
    print(f"vault: {vault}")
    changes = clean_videos(vault, apply=args.apply)
    if not changes:
        print("✓ nothing to do — all videos already clean or empty folder")
        return
    for old, new, status in changes:
        print(f"  [{status}] {old}")
        print(f"    → {new}")
    print(f"\n{len(changes)} file(s) affected. Apply: {args.apply}")
    if not args.apply:
        print("Re-run with --apply to execute.")


if __name__ == "__main__":
    main()
