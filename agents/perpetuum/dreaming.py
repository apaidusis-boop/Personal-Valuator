"""Dreaming perpetuum — background memory consolidation (OpenClaw pattern).

Three-phase model from docs/concepts/dreaming.md (cooperative, not exclusive):
  Light  — sort + stage recent material from daily_logs/. Never writes MEMORY.md.
  Deep   — score + promote durable candidates → MEMORY.md (via DREAMS.md surface).
  REM    — extract themes + reflections. Never writes MEMORY.md.

OpenClaw uses:  short-term store (memory/.dreams/) → ranked promotion → MEMORY.md
We use:        obsidian_vault/daily_logs/<agent>/<date>.md  →  DREAMS.md
                 → optional manual promotion to ~/.claude/.../memory/MEMORY.md

This is **opt-in** (enabled=False by default) and runs read+write only on the vault.
Promotion to user-level MEMORY.md is left as a manual review step (DREAMS.md is
the surface; user decides what graduates).

Subjects: each daily_log file from the last N days = one subject.
Score: composite of recency, frequency (lines), error_count, ok_ratio.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

from agents._llm import ollama_call

from ._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

ROOT = Path(__file__).resolve().parents[2]
DAILY_LOGS_DIR = ROOT / "obsidian_vault" / "daily_logs"
DREAMS_PATH = ROOT / "obsidian_vault" / "workspace" / "DREAMS.md"
LOOKBACK_DAYS = 7
MAX_PROMPT_CHARS = 6000


class DreamingPerpetuum(BasePerpetuum):
    """Consolidate daily_logs/ into DREAMS.md surface for human review."""

    name = "dreaming"
    description = "Light/Deep/REM memory consolidation: daily_logs → DREAMS.md"
    autonomy_tier = "T1"   # observer — surfaces candidates, never auto-promotes to MEMORY.md
    enabled = True         # activated 2026-04-30; runs alongside daily_run.bat cron 23:30
    drop_alert_threshold = 25  # signal-noise drop

    def subjects(self) -> list[PerpetuumSubject]:
        if not DAILY_LOGS_DIR.exists():
            return []
        cutoff = date.today() - timedelta(days=LOOKBACK_DAYS)
        out: list[PerpetuumSubject] = []
        for agent_dir in sorted(DAILY_LOGS_DIR.iterdir()):
            if not agent_dir.is_dir():
                continue
            for f in sorted(agent_dir.glob("*.md")):
                day_str = f.stem
                try:
                    day = date.fromisoformat(day_str)
                except ValueError:
                    continue
                if day < cutoff:
                    continue
                out.append(PerpetuumSubject(
                    id=f"{agent_dir.name}/{day_str}",
                    label=f"{agent_dir.name} {day_str}",
                    metadata={"path": str(f), "agent": agent_dir.name, "day": day_str},
                ))
        return out

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        path = Path(subject.metadata["path"])
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            return PerpetuumResult(subject_id=subject.id, score=-1,
                                   flags=[f"read_error:{e}"])

        line_count = text.count("\n")
        ok_count = text.count("✅")
        fail_count = text.count("❌")
        err_section = "**Errors:**" in text
        run_count = text.count("##") - 1  # minus the title heading

        # Composite signal score:
        #   - bigger files = more material to consolidate (good signal)
        #   - high fail_count = noise; reduce score
        #   - err_section = needs attention; reduce score
        score = 50
        if run_count >= 1:
            score += min(20, run_count * 2)
        if line_count >= 50:
            score += 15
        if line_count >= 200:
            score += 10
        if fail_count > 0:
            score -= min(30, fail_count * 5)
        if err_section:
            score -= 10
        if ok_count > 0:
            score += min(10, ok_count)
        score = max(0, min(100, score))

        details = {
            "path": str(path.relative_to(ROOT)),
            "lines": line_count,
            "runs": max(0, run_count),
            "ok": ok_count,
            "failures": fail_count,
        }
        flags: list[str] = []
        if fail_count > 5:
            flags.append("high_failure_rate")
        if line_count > 500:
            flags.append("verbose_log")
        return PerpetuumResult(
            subject_id=subject.id, score=score,
            flag_count=len(flags), flags=flags, details=details,
        )

    def run(self, run_date: str | None = None, dry_run: bool = False) -> dict:
        """Override to also write DREAMS.md surface after standard score persistence."""
        result = super().run(run_date=run_date, dry_run=dry_run)
        if not dry_run and result["scored"] > 0:
            try:
                self._write_dreams_surface(result, run_date or date.today().isoformat())
            except Exception as e:
                result["errors"].append(f"dreams_surface: {type(e).__name__}: {e}")
        return result

    def _write_dreams_surface(self, run_summary: dict, run_date: str) -> None:
        """Append a Light/Deep/REM block to DREAMS.md.

        Light: list of (agent/date, score, flags) — staged candidates.
        Deep:  Ollama-summarised top-3 themes worth promoting (suggestions only).
        REM:   patterns/recurring topics across days.
        """
        DREAMS_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Aggregate corpus for Ollama (cap at MAX_PROMPT_CHARS)
        corpus_parts: list[str] = []
        total_chars = 0
        for r in run_summary["results"]:
            if r["score"] < 0:
                continue
            subject_id = r["subject"]
            agent, day = subject_id.split("/", 1) if "/" in subject_id else (subject_id, "")
            f = DAILY_LOGS_DIR / agent / f"{day}.md"
            if f.exists():
                try:
                    snippet = f.read_text(encoding="utf-8")[:1000]
                    corpus_parts.append(f"### {subject_id}\n{snippet}")
                    total_chars += len(snippet)
                    if total_chars > MAX_PROMPT_CHARS:
                        break
                except Exception:
                    continue

        corpus = "\n\n".join(corpus_parts)[:MAX_PROMPT_CHARS]

        # Deep + REM via Ollama (Qwen 14B local, zero Claude tokens)
        deep_summary = "(corpus vazio — sem material para consolidar)"
        rem_themes = "(sem temas)"
        if corpus:
            try:
                deep_prompt = (
                    "Resume em 3-5 bullets PT-BR os factos/decisões mais importantes destes "
                    "logs de agents para promoção potencial a MEMORY.md (long-term). "
                    "Apenas factos não-óbvios, surpreendentes ou validados. "
                    "Skip routine/successful runs.\n\n" + corpus
                )
                deep_summary = ollama_call(deep_prompt, max_tokens=400, temperature=0.2)
            except Exception as e:
                deep_summary = f"[deep failed: {e}]"

            try:
                rem_prompt = (
                    "Identifica 2-3 padrões recorrentes ou temas atravessando estes logs "
                    "(em 1 frase cada, PT-BR). Foco em behavioural patterns ou friction "
                    "points, não factos individuais.\n\n" + corpus
                )
                rem_themes = ollama_call(rem_prompt, max_tokens=200, temperature=0.4)
            except Exception as e:
                rem_themes = f"[rem failed: {e}]"

        # Light: scored list, sorted desc
        scored = [r for r in run_summary["results"] if r["score"] >= 0]
        scored.sort(key=lambda r: -r["score"])
        light_lines = []
        for r in scored[:20]:
            light_lines.append(f"- `{r['subject']}` score={r['score']} flags={r['flags']}")

        # Compose block
        block = [
            f"## Sweep {run_date}",
            "",
            "### 🌙 Light Sleep — staged candidates",
            "",
            f"_Scanned {run_summary['scored']} daily-log files (last {LOOKBACK_DAYS} days)._",
            "",
            *light_lines,
            "",
            "### 💤 Deep Sleep — promotion candidates (Ollama Qwen 14B)",
            "",
            deep_summary.strip(),
            "",
            "### 🌀 REM — themes & patterns",
            "",
            rem_themes.strip(),
            "",
            "---",
            "",
        ]

        if not DREAMS_PATH.exists():
            header = [
                "---",
                "title: DREAMS",
                "purpose: Dream Diary — surface human-readable de memory consolidation. Generated by dreaming perpetuum.",
                "edit: read-only generated; humano promove items para ~/.claude/.../memory/MEMORY.md manualmente.",
                "---",
                "",
                "# DREAMS — Memory Consolidation Diary",
                "",
                "_Light/Deep/REM phases, append-only. Most recent first via reverse scroll._",
                "",
            ]
            DREAMS_PATH.write_text("\n".join(header) + "\n", encoding="utf-8")

        with DREAMS_PATH.open("a", encoding="utf-8") as f:
            f.write("\n".join(block) + "\n")
