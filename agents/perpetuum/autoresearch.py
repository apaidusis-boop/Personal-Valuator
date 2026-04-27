"""Autoresearch Perpetuum — descobre material news não-coberto no vault.

Phase K (2026-04-26). Wraps `agents/autoresearch.py` (Tavily client) num
perpetuum scoring framework.

Design:
  - Subjects: top conviction holdings (composite_score >= 60) — limita
    quota Tavily aos tickers que importam mais.
  - Cadence: queries só corre se ticker last_query > 6 dias. Persistido em
    perpetuum_health details_json.score field. Cache 7d natural do client
    + esta lógica protegem quota mensal.
  - Score: 100 - (penalty per material news item found NÃO coverage no vault).
    Score baixo = "há news novas que tu não viste". Score alto = "all clear".
  - T1 Observer: emite alert via drop_alert quando score cai (= news novas
    apareceram). User vai ler no Captain's Log + Telegram brief.

Material thresholds:
  - Tavily score >= 0.5 (relevância)
  - published_date dentro últimos 14 dias
  - Title NOT já em vault tickers/<TICKER>.md (substring match básico)

Rate budget protection:
  - Max ~30 calls/run × 1 run/dia = 30/dia (dentro 100/dia limit)
  - Cache 7d efectivo: queries iguais não recontactam
  - Skip se last_query < 6d em details_json
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject
from agents.autoresearch import search_ticker

DBS = {"br": ROOT / "data" / "br_investments.db",
       "us": ROOT / "data" / "us_investments.db"}
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"

CONVICTION_THRESHOLD = 70      # só corre Tavily para tickers acima disto
QUERY_COOLDOWN_DAYS = 6        # não re-query mesmo ticker dentro deste prazo
MATERIAL_DAYS = 14             # news must be within last N days
MIN_TAVILY_SCORE = 0.5         # relevância
MAX_SUBJECTS_PER_RUN = 30      # protege quota mensal (~5/dia steady com cooldown 6d)


class AutoresearchPerpetuum(BasePerpetuum):
    name = "autoresearch"
    description = "Tavily web research para top-conviction tickers; flag material news não-coberto"
    autonomy_tier = "T1"            # Observer — não acciona auto, só alerta
    drop_alert_threshold = 25
    action_score_threshold = 60

    def subjects(self) -> list[PerpetuumSubject]:
        """Top conviction holdings + watchlist com composite >= threshold.
        Cap em MAX_SUBJECTS_PER_RUN (~5/dia steady com cooldown 6d)."""
        out = []
        with sqlite3.connect(DBS["br"]) as c:
            c.row_factory = sqlite3.Row
            rows = c.execute("""
                SELECT ticker, market, composite_score
                FROM conviction_scores
                WHERE composite_score >= ?
                  AND run_date = (SELECT MAX(run_date) FROM conviction_scores)
                ORDER BY composite_score DESC
                LIMIT ?
            """, (CONVICTION_THRESHOLD, MAX_SUBJECTS_PER_RUN)).fetchall()
        for r in rows:
            out.append(PerpetuumSubject(
                id=f"{r['market']}:{r['ticker']}",
                label=r["ticker"],
                metadata={"market": r["market"], "ticker": r["ticker"],
                          "conviction": r["composite_score"]},
            ))
        return out

    def _last_query_date(self, subject_id: str) -> str | None:
        """Lê details_json.last_query da run anterior."""
        try:
            with sqlite3.connect(self._db) as c:
                row = c.execute(
                    "SELECT details_json FROM perpetuum_health "
                    "WHERE perpetuum_name=? AND subject_id=? "
                    "ORDER BY run_date DESC LIMIT 1",
                    (self.name, subject_id),
                ).fetchone()
                if row and row[0]:
                    d = json.loads(row[0])
                    return d.get("last_query")
        except Exception:
            pass
        return None

    def _vault_text(self, ticker: str) -> str:
        """Concatena ticker note + IC_DEBATE + VARIANT para coverage check."""
        chunks = []
        for suffix in ("", "_IC_DEBATE", "_VARIANT", "_RI"):
            p = TICKERS_DIR / f"{ticker}{suffix}.md"
            if p.exists():
                try:
                    chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
                except Exception:
                    pass
        return " ".join(chunks).lower()

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        ticker = subject.metadata["ticker"]
        market = subject.metadata["market"]
        today = date.today()
        details: dict = {"conviction": subject.metadata.get("conviction")}

        # Cooldown — não re-query se feito há < 6 dias
        last_q = self._last_query_date(subject.id)
        if last_q:
            try:
                last_dt = date.fromisoformat(last_q)
                if (today - last_dt).days < QUERY_COOLDOWN_DAYS:
                    details["skipped"] = "cooldown"
                    details["last_query"] = last_q
                    # Mantém score anterior (não emite alert)
                    return PerpetuumResult(
                        subject_id=subject.id, score=100, flag_count=0,
                        flags=["cooldown"], details=details,
                    )
            except Exception:
                pass

        # Tavily news search
        result = search_ticker(ticker, topic="news", market=market, days_back=MATERIAL_DAYS)
        details["last_query"] = today.isoformat()
        details["query"] = result.query
        details["cached"] = result.cached
        if result.error:
            return PerpetuumResult(
                subject_id=subject.id, score=-1,
                flags=[f"tavily_error: {result.error}"],
                details={**details, "error": result.error},
            )

        # Filter to material hits not covered in vault
        vault_text = self._vault_text(ticker)
        cutoff = today - timedelta(days=MATERIAL_DAYS)
        novel: list[dict] = []
        for h in result.results:
            if h.score < MIN_TAVILY_SCORE:
                continue
            if h.published_date:
                # Tavily returns RFC2822-ish; tentar parse simples
                try:
                    d = datetime.strptime(h.published_date[:25],
                                           "%a, %d %b %Y %H:%M:%S").date()
                    if d < cutoff:
                        continue
                except Exception:
                    pass
            # Coverage check: title token in vault?
            title_tokens = [t for t in h.title.lower().split() if len(t) > 5]
            if title_tokens:
                covered = sum(1 for t in title_tokens[:5] if t in vault_text)
                if covered >= 3:
                    continue   # 3+ keywords match = likely covered
            novel.append({
                "title": h.title[:120],
                "url": h.url,
                "score": h.score,
                "published_date": h.published_date,
            })

        details["hits_total"] = len(result.results)
        details["hits_novel"] = len(novel)
        details["novel"] = novel[:5]

        # Scoring: 100 - 15 * novel_count, floor 0
        score = max(0, 100 - 15 * len(novel))
        flags = []
        action_hint = None
        if novel:
            flags.append(f"{len(novel)} novel material news")
            top_titles = "; ".join(n["title"][:60] for n in novel[:3])
            action_hint = f"REVIEW autoresearch: {len(novel)} news não-cobertas — {top_titles}"

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(novel),
            flags=flags,
            details=details,
            action_hint=action_hint,
        )
