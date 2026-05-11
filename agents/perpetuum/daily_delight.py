"""Daily delight perpetuum — proactive build (OpenClaw "wake-up gift" pattern).

Tina Huang's pattern from the OpenClaw video: every morning the agent picks
ONE topic from the watchlist that crossed a threshold and produces something
delightful for the founder to wake up to.

Our adaptation:
  Subjects: top topics from data/topic_scores.json (tier='make_now' or score≥80).
  Score: composite of topic.score + holdings_hit_count + recency.
  Action: pick top 1, emit a "delight" markdown to obsidian_vault/Bibliotheca/Daily_Delight_<DATE>.md
          containing: 3-bullet rundown + 1 chart suggestion + 1 paper-trade idea (if applicable)
          + links to relevant dossiers/wiki notes.
  Push: optional Telegram + Discord (#captains-log) heads-up "I built X for you".

Stays T1 Observer — zero risk: just generates a vault markdown. Founder reads
in the morning and decides whether to act on it.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

from agents._llm import ollama_call

from ._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

ROOT = Path(__file__).resolve().parents[2]
TOPIC_SCORES_PATH = ROOT / "data" / "topic_scores.json"
DELIGHT_DIR = ROOT / "obsidian_vault" / "Bibliotheca"
MIN_SCORE = 80


class DailyDelightPerpetuum(BasePerpetuum):
    """Pick top topic of the day, build a delight markdown, push heads-up."""

    name = "daily_delight"
    description = "Proactive morning build: top topic → delight markdown + push"
    autonomy_tier = "T1"
    enabled = False  # opt-in until founder confirms cadence
    drop_alert_threshold = 30

    def subjects(self) -> list[PerpetuumSubject]:
        if not TOPIC_SCORES_PATH.exists():
            return []
        try:
            data = json.loads(TOPIC_SCORES_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
        topics = data.get("topics", [])
        # Only above-threshold candidates
        eligible = [t for t in topics if t.get("score", 0) >= MIN_SCORE]
        return [
            PerpetuumSubject(
                id=t["id"],
                label=t.get("name", t["id"]),
                metadata=t,
            )
            for t in eligible
        ]

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        meta = subject.metadata
        topic_score = int(meta.get("score", 0))
        holdings_hit = len(meta.get("holdings_hit") or [])
        weeks_tracked = int(meta.get("weeks_tracked", 0))

        # Composite: prefer high-score topics that hit current holdings + are fresh
        score = min(100, topic_score)
        if holdings_hit >= 3:
            score = min(100, score + 5)
        if weeks_tracked == 1:
            score = min(100, score + 3)  # newer = surface first

        flags: list[str] = []
        if holdings_hit >= 5:
            flags.append("portfolio_heavy")
        if topic_score >= 95:
            flags.append("urgent_topic")

        return PerpetuumResult(
            subject_id=subject.id, score=score,
            flag_count=len(flags), flags=flags,
            details={
                "topic_score": topic_score,
                "holdings_hit": meta.get("holdings_hit", []),
                "weeks_tracked": weeks_tracked,
                "tier": meta.get("tier"),
            },
        )

    def run(self, run_date: str | None = None, dry_run: bool = False) -> dict:
        result = super().run(run_date=run_date, dry_run=dry_run)
        if dry_run or result["scored"] == 0:
            return result

        # Pick top-scored subject of the day; bail if none
        scored = [r for r in result["results"] if r["score"] >= 0]
        if not scored:
            return result
        scored.sort(key=lambda r: -r["score"])
        winner = scored[0]
        topic_id = winner["subject"]
        # Re-fetch metadata for the winner
        topics = json.loads(TOPIC_SCORES_PATH.read_text(encoding="utf-8")).get("topics", [])
        meta = next((t for t in topics if t["id"] == topic_id), None)
        if not meta:
            return result

        try:
            self._build_delight(meta, run_date or date.today().isoformat())
            result["delight_topic"] = topic_id
        except Exception as e:
            result["errors"].append(f"delight_build: {type(e).__name__}: {e}")

        return result

    def _build_delight(self, topic: dict, run_date: str) -> None:
        DELIGHT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = DELIGHT_DIR / f"Daily_Delight_{run_date}.md"

        # Compose Ollama prompt for the rundown
        prompt = f"""És o agent matinal do founder. Constrói um rundown de 3 bullets PT-BR
sobre este topic do watchlist, optimizado para leitura mobile/Telegram:

TOPIC: {topic.get('name')}
RESUMO: {topic.get('summary', '')}
HOLDINGS AFECTADAS: {', '.join(topic.get('holdings_hit', []))}
SCORE: {topic.get('score')} (tier {topic.get('tier')})

Formato:
- 3 bullets max, 1 frase cada.
- Cada bullet ≤ 25 palavras.
- 1º bullet: estado actual / o que mudou esta semana.
- 2º bullet: implicação para a carteira (qual holding mais afectada).
- 3º bullet: 1 acção concreta a considerar (não obrigatória — só sugestão).

NÃO uses preâmbulos, NÃO uses "vou explicar". Vai direto aos 3 bullets.
"""
        rundown = "(Ollama indisponível)"
        try:
            rundown = ollama_call(prompt, max_tokens=300, temperature=0.4)
        except Exception:
            pass

        lines = [
            "---",
            f"type: daily_delight",
            f"date: {run_date}",
            f"topic_id: {topic['id']}",
            f"topic_score: {topic.get('score')}",
            f"holdings_hit: {topic.get('holdings_hit', [])}",
            "---",
            "",
            f"# 🌅 Daily Delight — {run_date}",
            "",
            f"## Topic of the day: {topic.get('name')}",
            "",
            "_Score:_ "
            f"**{topic.get('score')}/100** ({topic.get('tier')}) · "
            f"_Holdings hit:_ {', '.join(topic.get('holdings_hit', [])) or '(none)'}",
            "",
            "## Morning rundown",
            "",
            rundown.strip(),
            "",
            "## Suggested actions",
            "",
            "- Verificar peers + macro regime para o sector afectado: `ii panorama <TICKER>`",
            "- Se quiser deep dive: `ii deepdive <TICKER>` (V10 Personal Equity Valuator)",
            "- Synthetic IC para sanity check: `python -m agents.synthetic_ic <TICKER> --majority 3`",
            "",
            "## References",
            "",
            f"- Topic config: `config/topic_watchlist.yaml::{topic['id']}`",
            f"- Score detail: `data/topic_scores.json` (computed_at = today)",
            "- Recent research: `obsidian_vault/Bibliotheca/Research_Digest_<recent>.md`",
            "",
            "---",
            "",
            "_Built by daily_delight perpetuum. Zero auto-actions; this is a heads-up. "
            "Ignore se irrelevante hoje._",
        ]
        out_path.write_text("\n".join(lines), encoding="utf-8")

        # Optional pushes — both gracefully no-op if not configured
        msg = (f"🌅 *Daily Delight* `{run_date}`\n\n"
               f"*{topic.get('name')}* — score {topic.get('score')}\n\n"
               f"Holdings hit: {', '.join(topic.get('holdings_hit', [])) or '(none)'}\n\n"
               f"Vault: `Bibliotheca/Daily_Delight_{run_date}.md`")
        try:
            from notifiers.telegram import send as tg_send
            tg_send(msg, silent=True)
        except Exception:
            pass
        try:
            from notifiers.discord import send as dc_send
            dc_send("captains-log", msg.replace("*", "**"))
        except Exception:
            pass
