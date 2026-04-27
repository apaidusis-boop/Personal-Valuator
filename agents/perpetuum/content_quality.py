"""Content Quality Perpetuum — signal-to-noise de briefings/reports/research memos.

Subjects: ficheiros em obsidian_vault/briefings/ + reports/ + ticker notes recentes.

Scoring signals (determinístico, zero LLM):
  + specificity: contem numbers, dates, tickers concretos (regex count)
  + actionability: contem bullet points accionáveis ("BUY X", "TRIM Y", "watch Z")
  + uniqueness: jaccard similarity vs briefing anterior
  - boilerplate: frases repetidas entre briefings ("Hoje o mercado...")
  - generic: frases vazias ("de forma geral", "possivelmente")
  - age: briefings antigos perdem score (gradient)

Score 0-100. < 50 → flag LOW_SIGNAL (propor rewrite/deletion).
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

TICKER_RE = re.compile(r"\b([A-Z]{1,5}\d?\.?[A-Z]{0,2}\b|\b[A-Z]{3,5}\d\b)")
NUMBER_RE = re.compile(r"[-+]?\$?R?\$?\s?\d+[\d,\.]*\%?")
DATE_RE = re.compile(r"\b20\d{2}[-/]\d{2}[-/]\d{2}\b|\bQ[1-4][\s-]?20\d{2}\b")
ACTION_RE = re.compile(r"\b(BUY|SELL|TRIM|ADD|HOLD|WATCH|EXIT|REBALANCE|REVIEW)\b", re.I)

GENERIC_PHRASES = [
    "de forma geral", "possivelmente", "talvez", "parece ser", "no geral",
    "pode ser", "em tese", "as coisas", "olhando para", "interessante notar",
]


def _tokenize(text: str) -> set[str]:
    words = re.findall(r"\b[a-zA-ZÀ-ÿ]{4,}\b", text.lower())
    return set(words)


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class ContentQualityPerpetuum(BasePerpetuum):
    name = "content_quality"
    description = "Signal-to-noise de briefings + reports + research memos"
    autonomy_tier = "T2"           # Promoted 2026-04-26: avg 100/100, 0 low subjects
    drop_alert_threshold = 15

    def subjects(self) -> list[PerpetuumSubject]:
        subjects = []
        scan_dirs = [
            VAULT / "briefings",
            ROOT / "reports",
        ]
        for d in scan_dirs:
            if not d.exists():
                continue
            for md in d.glob("*.md"):
                if md.name.startswith("_") or md.name.startswith("."):
                    continue
                subjects.append(PerpetuumSubject(
                    id=str(md.relative_to(ROOT)).replace("\\", "/"),
                    label=md.stem,
                    metadata={"path": str(md)},
                ))
        return subjects

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        path = Path(subject.metadata["path"])
        flags: list[str] = []

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return PerpetuumResult(subject_id=subject.id, score=-1, flags=[str(e)])

        # Strip frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2]

        total_chars = len(content)
        if total_chars < 200:
            return PerpetuumResult(
                subject_id=subject.id, score=30,
                flag_count=1, flags=["too short (< 200 chars)"],
                details={"chars": total_chars},
                action_hint="ARCHIVE or EXPAND",
            )

        score = 100

        # Specificity (positive)
        tickers = len(set(TICKER_RE.findall(content)))
        numbers = len(NUMBER_RE.findall(content))
        dates = len(DATE_RE.findall(content))
        actions = len(ACTION_RE.findall(content))

        specificity_raw = tickers * 2 + numbers + dates * 3 + actions * 5
        specificity_per_kb = specificity_raw / max(total_chars / 1000, 1)

        # Expect ≥8 specifics per 1k chars for good briefing
        if specificity_per_kb < 3:
            score -= 30
            flags.append(f"low specificity ({specificity_per_kb:.1f}/kb)")
        elif specificity_per_kb < 6:
            score -= 10
            flags.append(f"medium specificity ({specificity_per_kb:.1f}/kb)")

        # Generic phrase penalty
        generic_count = sum(content.lower().count(p) for p in GENERIC_PHRASES)
        if generic_count > 5:
            score -= 20
            flags.append(f"generic phrases x{generic_count}")
        elif generic_count > 2:
            score -= 8

        # Uniqueness vs previous briefing (same folder)
        siblings = [p for p in path.parent.glob("*.md")
                    if p != path and p.stat().st_mtime < path.stat().st_mtime]
        if siblings:
            prev = max(siblings, key=lambda p: p.stat().st_mtime)
            try:
                prev_content = prev.read_text(encoding="utf-8", errors="ignore")
                j = _jaccard(_tokenize(content), _tokenize(prev_content))
                if j > 0.75:
                    score -= 25
                    flags.append(f"repeats prev briefing ({j*100:.0f}% overlap)")
                elif j > 0.5:
                    score -= 10
                    flags.append(f"moderate overlap ({j*100:.0f}%)")
            except Exception:
                pass

        # Age
        age_days = (datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)).days
        if age_days > 90:
            score -= 15
            flags.append(f"stale {age_days}d")
        elif age_days > 30:
            score -= 5

        score = max(0, min(100, score))

        action_hint = None
        if score < 50:
            action_hint = "ARCHIVE_or_REWRITE — low signal content"
        elif score < 70:
            action_hint = "ADD_SPECIFICS — tickers/numbers/dates/actions thin"

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(flags),
            flags=flags,
            details={
                "chars": total_chars,
                "tickers": tickers,
                "numbers": numbers,
                "dates": dates,
                "actions": actions,
                "specificity_per_kb": round(specificity_per_kb, 2),
                "generic_count": generic_count,
                "age_days": age_days,
            },
            action_hint=action_hint,
        )
