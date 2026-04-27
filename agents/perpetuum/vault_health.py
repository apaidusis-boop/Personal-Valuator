"""Vault Health Perpetuum — valida saúde de cada nota do Obsidian vault.

Scoring signals:
  - orphan: 0 inbound OR outbound links  → -40 pts
  - stale: not modified in N days        → -X pts (gradient)
  - short: < 30 chars of substance       → -25 pts
  - no_thesis: ticker sem ## Thesis      → -20 pts (only for ticker notes)
  - broken_links: [[X]] que não existe   → -5 pts per broken

Subjects: every .md file in obsidian_vault/, EXCEPT generated dashboards
and skills/ (meta notes don't need health scoring).

Action hints:
  < 50 → "Archive or rewrite"
  50-69 → "Review + add context"
  70-89 → "Light refresh"
  90+ → "Healthy, no action"

Zero LLM calls. Pure filesystem + regex.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

VAULT = ROOT / "obsidian_vault"
SKIP_DIRS = {"skills", "Clippings", ".obsidian"}   # skip meta
SKIP_FILES = {"_MOC.md", "Home.md"}                 # hubs, naturally high link density

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]*)?(?:#[^\]]*)?\]\]")


def _all_notes() -> list[Path]:
    notes = []
    for md in VAULT.rglob("*.md"):
        rel = md.relative_to(VAULT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if md.name in SKIP_FILES:
            continue
        notes.append(md)
    return notes


def _all_note_names() -> set[str]:
    """Set of valid wikilink targets (just the filename stem)."""
    return {p.stem for p in VAULT.rglob("*.md")}


def _extract_outbound_links(content: str) -> set[str]:
    return {m.group(1).strip() for m in WIKILINK_RE.finditer(content)}


def _build_inbound_index(all_notes: list[Path]) -> dict[str, set[str]]:
    """For each note stem, set of other notes that link to it."""
    inbound: dict[str, set[str]] = {}
    for note in all_notes:
        try:
            content = note.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for target in _extract_outbound_links(content):
            inbound.setdefault(target, set()).add(note.stem)
    return inbound


class VaultHealthPerpetuum(BasePerpetuum):
    name = "vault"
    description = "Saúde de cada nota: orphan, stale, short, broken links"
    autonomy_tier = "T2"           # Promoted 2026-04-24: proposes MANUAL_REVIEW actions
    drop_alert_threshold = 15
    action_score_threshold = 30    # 2026-04-26: raised 50→30 após bulk-ignore de 80 generic
                                   # vault drift actions; só notas REALMENTE doentes
                                   # (orphan + stale + thin + missing thesis combinados)
                                   # emitem agora. Reduz noise ~80% sem perder sinal alto.

    def __init__(self):
        super().__init__()
        self._all_notes_cache = None
        self._inbound_index = None
        self._valid_names = None

    def _load_caches(self):
        if self._all_notes_cache is not None:
            return
        self._all_notes_cache = _all_notes()
        self._valid_names = _all_note_names()
        self._inbound_index = _build_inbound_index(self._all_notes_cache)

    def subjects(self) -> list[PerpetuumSubject]:
        self._load_caches()
        return [
            PerpetuumSubject(
                id=str(p.relative_to(VAULT)).replace("\\", "/"),
                label=p.stem,
                metadata={"path": str(p), "stem": p.stem},
            )
            for p in self._all_notes_cache
        ]

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        self._load_caches()
        path = Path(subject.metadata["path"])
        stem = subject.metadata["stem"]
        flags: list[str] = []

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return PerpetuumResult(
                subject_id=subject.id, score=-1, flags=[f"unreadable: {e}"],
                details={"error": str(e)},
            )

        score = 100
        outbound = _extract_outbound_links(content)
        inbound = self._inbound_index.get(stem, set())
        age_days = (datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)).days
        substantive_chars = len(re.sub(r"[\s\W_]+", "", content))

        # Signal 1: orphan
        if not inbound and not outbound:
            score -= 40
            flags.append("orphan (0 in, 0 out)")
        elif not inbound:
            score -= 15
            flags.append(f"no inbound links (has {len(outbound)} outbound)")
        elif not outbound:
            score -= 10
            flags.append(f"no outbound links (has {len(inbound)} inbound)")

        # Signal 2: stale (gradient)
        if age_days > 365:
            score -= 25
            flags.append(f"stale {age_days}d (>1yr)")
        elif age_days > 180:
            score -= 12
            flags.append(f"stale {age_days}d (>6mo)")
        elif age_days > 90:
            score -= 5
            flags.append(f"stale {age_days}d (>3mo)")

        # Signal 3: short/thin
        if substantive_chars < 300:
            score -= 25
            flags.append(f"thin content ({substantive_chars} chars)")
        elif substantive_chars < 800:
            score -= 10
            flags.append(f"lightweight ({substantive_chars} chars)")

        # Signal 4: ticker-specific — no ## Thesis
        if "tickers/" in subject.id and "## Thesis" not in content:
            score -= 20
            flags.append("ticker note missing ## Thesis section")

        # Signal 5: broken wikilinks
        broken = [link for link in outbound if link not in self._valid_names]
        if broken:
            penalty = min(len(broken) * 5, 30)
            score -= penalty
            flags.append(f"{len(broken)} broken wikilink(s)")

        score = max(0, min(100, score))

        action_hint = None
        if score < 30:
            action_hint = "ARCHIVE or REWRITE — note is dead weight"
        elif score < 50:
            action_hint = "REVIEW + add context / backlinks"
        elif score < 70:
            action_hint = "LIGHT_REFRESH"

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(flags),
            flags=flags,
            details={
                "inbound": len(inbound),
                "outbound": len(outbound),
                "age_days": age_days,
                "chars": substantive_chars,
                "broken_links": broken[:10],
                "flags": flags,
            },
            action_hint=action_hint,
        )
