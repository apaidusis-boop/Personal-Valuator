#!/usr/bin/env python3
"""
Absorb plugin skills/commands/agents from Claude Code plugin cache into the
project so we no longer depend on marketplace cache being healthy.

Sources scanned: ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/
Files copied:
  skills/<name>/         -> .claude/skills/<plugin>-<name>/        (invocable)
  commands/<name>.md     -> .claude/commands/<plugin>-<name>.md    (slash cmd)
  agents/<name>.md       -> .claude/agents/<plugin>-<name>.md      (subagent)

A pointer doc is also written to obsidian_vault/skills/imported/<plugin>/<name>.md
so absorbed skills are searchable in the vault.

Idempotent: re-run safely after marketplace updates. Manifest of what was
absorbed is written to data/absorbed_plugins.json.

Usage:
  python scripts/absorb_plugins.py            # apply
  python scripts/absorb_plugins.py --dry-run  # report only
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
PLUGIN_CACHE = HOME / ".claude" / "plugins" / "cache"
PROJECT = Path(__file__).resolve().parent.parent

DEST_SKILLS = PROJECT / ".claude" / "skills"
DEST_COMMANDS = PROJECT / ".claude" / "commands"
DEST_AGENTS = PROJECT / ".claude" / "agents"
DEST_VAULT = PROJECT / "obsidian_vault" / "skills" / "imported"
MANIFEST = PROJECT / "data" / "absorbed_plugins.json"

DENY_PLUGINS = {
    "bigdata-com",
}


def find_plugin_versions():
    """Yield (marketplace, plugin, version_dir). Picks most-recent version dir."""
    if not PLUGIN_CACHE.exists():
        return
    for mp in sorted(PLUGIN_CACHE.iterdir()):
        if not mp.is_dir():
            continue
        for plugin in sorted(mp.iterdir()):
            if not plugin.is_dir():
                continue
            versions = [v for v in plugin.iterdir() if v.is_dir()]
            if not versions:
                continue
            versions.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            yield mp.name, plugin.name, versions[0]


def copy_skill_dir(src: Path, dest: Path, dry_run: bool):
    if dry_run:
        return
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def copy_file(src: Path, dest: Path, dry_run: bool):
    if dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def write_vault_pointer(plugin: str, skill_name: str, skill_md: Path, dry_run: bool):
    dest = DEST_VAULT / plugin / f"{skill_name}.md"
    if dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# {plugin}:{skill_name}\n\n"
        f"Skill absorvida do plugin `{plugin}` em "
        f"{datetime.utcnow().date().isoformat()}.\n"
        f"Cópia invocável: `.claude/skills/{plugin}-{skill_name}/SKILL.md`.\n\n"
        f"Re-absorver: `python scripts/absorb_plugins.py`.\n\n"
        f"---\n\n"
    )
    body = skill_md.read_text(encoding="utf-8", errors="replace")
    dest.write_text(header + body, encoding="utf-8")


def absorb_plugin(plugin: str, version_dir: Path, dry_run: bool):
    counts = {"skills": [], "commands": [], "agents": []}

    skills_dir = version_dir / "skills"
    if skills_dir.is_dir():
        for sd in sorted(skills_dir.iterdir()):
            if not sd.is_dir():
                continue
            skill_md = sd / "SKILL.md"
            if not skill_md.is_file():
                continue
            dest = DEST_SKILLS / f"{plugin}-{sd.name}"
            copy_skill_dir(sd, dest, dry_run)
            write_vault_pointer(plugin, sd.name, skill_md, dry_run)
            counts["skills"].append(dest.name)

    cmds_dir = version_dir / "commands"
    if cmds_dir.is_dir():
        for cf in sorted(cmds_dir.iterdir()):
            if cf.suffix.lower() != ".md":
                continue
            dest = DEST_COMMANDS / f"{plugin}-{cf.stem}.md"
            copy_file(cf, dest, dry_run)
            counts["commands"].append(dest.name)

    agents_dir = version_dir / "agents"
    if agents_dir.is_dir():
        for af in sorted(agents_dir.iterdir()):
            if af.suffix.lower() != ".md":
                continue
            dest = DEST_AGENTS / f"{plugin}-{af.stem}.md"
            copy_file(af, dest, dry_run)
            counts["agents"].append(dest.name)

    return counts


def main():
    dry_run = "--dry-run" in sys.argv

    manifest = {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "dry_run": dry_run,
        "plugins": {},
    }
    totals = {"skills": 0, "commands": 0, "agents": 0, "plugins": 0}

    for marketplace, plugin, version_dir in find_plugin_versions():
        if plugin in DENY_PLUGINS:
            continue
        counts = absorb_plugin(plugin, version_dir, dry_run)
        if not any(counts.values()):
            continue
        key = f"{plugin}@{marketplace}"
        manifest["plugins"][key] = {
            "source": str(version_dir),
            "absorbed": {k: len(v) for k, v in counts.items()},
            "items": counts,
        }
        totals["plugins"] += 1
        totals["skills"] += len(counts["skills"])
        totals["commands"] += len(counts["commands"])
        totals["agents"] += len(counts["agents"])

    manifest["totals"] = totals

    if not dry_run:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
