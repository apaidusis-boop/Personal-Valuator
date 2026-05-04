"""ResearchBrief — Camada 1 of STORYT_3.0.

Ulisses Navegador (Head of Research) convoca tudo o que existe sobre o ticker
ANTES do council debater. Sources:

  1. analyst_insights / analyst_reports — Suno, BTG, XP, Fool, WSJ etc.
  2. events — CVM fatos relevantes / SEC filings
  3. obsidian_vault/videos/ — YouTube transcripts já ingeridos com insights
  4. library/chunks_index — Bibliotheca RAG (text search por nome/ticker)
  5. Tavily — news + guidance + insider/scandal (Phase K wire)
  6. Aristóteles Backtest — accuracy histórica de cada source (se disponível)

Each source is wrapped in try/except so missing data doesn't block the brief.
The brief is a STRUCTURED dataclass; renderers project it for council prompt
consumption AND for evidence ledger entries.
"""
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}
ALIASES_PATH = ROOT / "config" / "aliases.yaml"
VIDEOS_DIR = ROOT / "obsidian_vault" / "videos"
LIBRARY_DB = ROOT / "library" / "chunks_index.db"


@dataclass
class ResearchHit:
    """One piece of evidence — analyst insight, filing, video, or chunk."""
    kind: str               # 'analyst_insight' | 'event' | 'video_insight' | 'bibliotheca_chunk' | 'tavily_news' | 'tavily_guidance' | 'tavily_insider'
    source: str             # human-readable: "BTG Equity Brazil", "CVM", "Virtual Asset YouTube", "Tavily news"
    title: str              # short headline
    claim: str              # the actual content (max ~400 chars)
    date: str               # ISO date if available
    url: str                # link if available
    confidence: float       # 0-1 if extracted; 1.0 if primary source
    stance: str             # 'bull' | 'bear' | 'neutral' | 'risk' | 'guidance' | 'rating' | 'fact'
    extra: dict = field(default_factory=dict)


@dataclass
class ResearchBrief:
    ticker: str
    market: str
    aliases: list[str] = field(default_factory=list)
    analyst_hits: list[ResearchHit] = field(default_factory=list)
    event_hits: list[ResearchHit] = field(default_factory=list)
    video_hits: list[ResearchHit] = field(default_factory=list)
    bibliotheca_hits: list[ResearchHit] = field(default_factory=list)
    tavily_news_hits: list[ResearchHit] = field(default_factory=list)
    tavily_guidance_hits: list[ResearchHit] = field(default_factory=list)
    tavily_insider_hits: list[ResearchHit] = field(default_factory=list)
    source_accuracy: dict[str, float] = field(default_factory=dict)
    fetched_at: str = ""
    notes: list[str] = field(default_factory=list)

    @property
    def all_hits(self) -> list[ResearchHit]:
        return (
            self.analyst_hits + self.event_hits + self.video_hits
            + self.bibliotheca_hits + self.tavily_news_hits
            + self.tavily_guidance_hits + self.tavily_insider_hits
        )

    @property
    def total_hits(self) -> int:
        return len(self.all_hits)

    def render_for_council(self, max_per_section: int = 5) -> str:
        """Compact projection for the council prompt. Each hit gets [N] index
        so council voices can cite (e.g. "[3] BTG diz X")."""
        lines = []
        idx = 0

        def section(name: str, hits: list[ResearchHit]) -> None:
            nonlocal idx
            if not hits:
                return
            lines.append(f"\n## {name} ({len(hits)} hits)")
            for h in hits[:max_per_section]:
                idx += 1
                date = f" [{h.date[:10]}]" if h.date else ""
                stance = f" ({h.stance})" if h.stance and h.stance != "fact" else ""
                lines.append(f"[{idx}] {h.source}{date}{stance}: {h.claim[:300]}")
                if h.url:
                    lines.append(f"     URL: {h.url}")

        section("ANALYST INSIGHTS (subscriptions BTG/XP/Suno)", self.analyst_hits)
        section("CVM/SEC EVENTS (fatos relevantes/filings)", self.event_hits)
        section("YOUTUBE INSIGHTS (transcripts ingeridos)", self.video_hits)
        section("BIBLIOTHECA (livros/clippings RAG)", self.bibliotheca_hits)
        section("TAVILY NEWS (≤30d)", self.tavily_news_hits)
        section("TAVILY GUIDANCE (≤90d)", self.tavily_guidance_hits)
        section("TAVILY INSIDER/SHORT/SCANDAL", self.tavily_insider_hits)

        if self.source_accuracy:
            lines.append("\n## SOURCE ACCURACY (Aristóteles Backtest)")
            for src, acc in sorted(self.source_accuracy.items(), key=lambda x: -x[1]):
                lines.append(f"  - {src}: {acc*100:.0f}% accuracy historical")

        if self.notes:
            lines.append("\n## RESEARCH NOTES")
            for n in self.notes:
                lines.append(f"  - {n}")

        if not lines:
            return "_(Research department não encontrou material sobre este ticker.)_"
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Aliases — ticker → list of name variants (for fuzzy text search)
# ─────────────────────────────────────────────────────────────────────


def _load_aliases(ticker: str) -> list[str]:
    """Load name variants for the ticker from config/aliases.yaml.
    Returns a list of strings to search for in free text."""
    try:
        import yaml
    except ImportError:
        return [ticker]
    if not ALIASES_PATH.exists():
        return [ticker]
    try:
        data = yaml.safe_load(ALIASES_PATH.read_text(encoding="utf-8")) or {}
        entry = (data.get("tickers") or {}).get(ticker) or {}
        names = entry.get("names") or [ticker]
        # Always include the bare ticker
        if ticker not in names:
            names = [ticker] + list(names)
        # Also include sibling tickers (POMO3 ↔ POMO4) by checking same-prefix entries
        sibling_tickers = []
        prefix = ticker[:-1] if ticker[-1].isdigit() else ticker
        for other_ticker in (data.get("tickers") or {}).keys():
            if other_ticker != ticker and other_ticker.startswith(prefix):
                sibling_tickers.append(other_ticker)
        return list({n for n in names if n}) + sibling_tickers
    except Exception:
        return [ticker]


def _aliases_with_ticker_variants(ticker: str) -> list[str]:
    """Returns aliases + ticker + sibling shares (POMO3 ↔ POMO4)."""
    bases = _load_aliases(ticker)
    out = set(bases)
    # Add sibling shares (same letters, different number)
    m = re.match(r"^([A-Z]+)(\d+)$", ticker)
    if m:
        prefix = m.group(1)
        for n in (3, 4, 5, 6, 11):
            out.add(f"{prefix}{n}")
    return [a for a in out if a]


# ─────────────────────────────────────────────────────────────────────
# Source pullers
# ─────────────────────────────────────────────────────────────────────


def _pull_analyst_insights(ticker: str, market: str, aliases: list[str]) -> list[ResearchHit]:
    db = DBS[market]
    if not db.exists():
        return []
    out: list[ResearchHit] = []
    seen_ids: set[int] = set()
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        # Direct ticker match
        for tk in aliases:
            try:
                rows = c.execute("""
                    SELECT i.id, i.stance, i.kind, i.claim, i.confidence, i.price_target,
                           r.source, r.title, r.published_at, r.url, r.author
                    FROM analyst_insights i
                    JOIN analyst_reports r ON r.id = i.report_id
                    WHERE i.ticker = ?
                    ORDER BY r.published_at DESC LIMIT 30
                """, (tk,)).fetchall()
            except sqlite3.OperationalError:
                continue
            for r in rows:
                if r["id"] in seen_ids:
                    continue
                seen_ids.add(r["id"])
                out.append(ResearchHit(
                    kind="analyst_insight",
                    source=f"{r['source']}",
                    title=(r["title"] or "")[:200],
                    claim=r["claim"] or "",
                    date=r["published_at"] or "",
                    url=r["url"] or "",
                    confidence=float(r["confidence"] or 0.5),
                    stance=r["stance"] or "neutral",
                    extra={
                        "kind_finegrained": r["kind"],
                        "price_target": r["price_target"],
                        "author": r["author"],
                        "report_id": r["id"],
                    },
                ))
    # Sort by recency
    out.sort(key=lambda h: h.date, reverse=True)
    return out[:15]


def _pull_events(ticker: str, market: str, aliases: list[str]) -> list[ResearchHit]:
    db = DBS[market]
    if not db.exists():
        return []
    out: list[ResearchHit] = []
    seen_ids: set[int] = set()
    with sqlite3.connect(db) as c:
        c.row_factory = sqlite3.Row
        for tk in aliases:
            try:
                rows = c.execute("""
                    SELECT id, event_date, source, kind, summary, url, full_text
                    FROM events
                    WHERE ticker = ?
                    ORDER BY event_date DESC LIMIT 15
                """, (tk,)).fetchall()
            except sqlite3.OperationalError:
                continue
            for r in rows:
                if r["id"] in seen_ids:
                    continue
                seen_ids.add(r["id"])
                summary = r["summary"] or ""
                if not summary and r["full_text"]:
                    summary = r["full_text"][:400]
                out.append(ResearchHit(
                    kind="event",
                    source=f"{r['source']} ({r['kind']})",
                    title=(r["summary"] or r["kind"] or "")[:200],
                    claim=summary[:500],
                    date=r["event_date"] or "",
                    url=r["url"] or "",
                    confidence=1.0,  # primary source
                    stance="fact",
                ))
    out.sort(key=lambda h: h.date, reverse=True)
    return out[:10]


def _pull_videos(ticker: str, aliases: list[str]) -> list[ResearchHit]:
    """Search obsidian_vault/videos/*.md for files mentioning the ticker.
    Each video has structured insights per ticker — extract those."""
    if not VIDEOS_DIR.exists():
        return []
    out: list[ResearchHit] = []

    # Build search regex (match any alias as whole word, case-insensitive)
    pattern_parts = [re.escape(a) for a in aliases if len(a) >= 3]
    if not pattern_parts:
        return []
    pattern = re.compile(r"\b(" + "|".join(pattern_parts) + r")\b", re.IGNORECASE)

    for md_path in sorted(VIDEOS_DIR.glob("*.md"), reverse=True):
        try:
            text = md_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if not pattern.search(text):
            continue

        # Parse frontmatter for channel, date, video_id
        channel = ""
        published = ""
        video_id = ""
        url = ""
        if text.startswith("---"):
            try:
                front_end = text.index("---", 3)
                front = text[3:front_end]
                for line in front.split("\n"):
                    if line.startswith("channel:"):
                        channel = line.split(":", 1)[1].strip()
                    elif line.startswith("published_at:"):
                        published = line.split(":", 1)[1].strip()
                    elif line.startswith("video_id:"):
                        video_id = line.split(":", 1)[1].strip()
            except ValueError:
                pass
        if video_id:
            url = f"https://www.youtube.com/watch?v={video_id}"

        # Extract per-ticker insights — look for `### [[TICKER]]` blocks
        for tk in aliases:
            block_pattern = re.compile(
                r"###\s+\[\[" + re.escape(tk) + r"\]\]\s*\n(.*?)(?=\n###|\n##|\Z)",
                re.DOTALL,
            )
            m = block_pattern.search(text)
            if not m:
                continue
            block = m.group(1)
            # Each insight: `- [0.80 kind] claim text`
            insight_pattern = re.compile(r"-\s+\[([\d.]+)\s+(\w+)\]\s+(.+?)(?=\n-|\Z)", re.DOTALL)
            for im in insight_pattern.finditer(block):
                conf = float(im.group(1))
                kind = im.group(2)
                claim = im.group(3).strip().replace("\n", " ")
                out.append(ResearchHit(
                    kind="video_insight",
                    source=f"YouTube {channel}" if channel else "YouTube",
                    title=md_path.stem,
                    claim=claim,
                    date=published,
                    url=url,
                    confidence=conf,
                    stance=kind,
                    extra={"video_id": video_id, "ticker_in_video": tk},
                ))
    out.sort(key=lambda h: h.date, reverse=True)
    return out[:15]


def _pull_bibliotheca(ticker: str, aliases: list[str], top_k: int = 5) -> list[ResearchHit]:
    """Text search in library/chunks_index for ticker mentions. Falls back to
    plain text LIKE queries (no embedding lookup needed for direct mentions)."""
    if not LIBRARY_DB.exists():
        return []
    out: list[ResearchHit] = []
    seen_chunks: set[tuple[str, str]] = set()
    with sqlite3.connect(LIBRARY_DB) as c:
        c.row_factory = sqlite3.Row
        for alias in aliases:
            if len(alias) < 4:
                continue  # avoid noise from short tokens
            try:
                rows = c.execute(
                    "SELECT book_slug, chunk_file, text FROM chunk_index "
                    "WHERE text LIKE ? LIMIT 10",
                    (f"%{alias}%",),
                ).fetchall()
            except Exception:
                continue
            for r in rows:
                key = (r["book_slug"], r["chunk_file"])
                if key in seen_chunks:
                    continue
                seen_chunks.add(key)
                txt = (r["text"] or "")[:500]
                out.append(ResearchHit(
                    kind="bibliotheca_chunk",
                    source=f"Bibliotheca: {r['book_slug']}",
                    title=r["chunk_file"],
                    claim=txt,
                    date="",
                    url="",
                    confidence=0.7,
                    stance="fact",
                    extra={"book": r["book_slug"]},
                ))
                if len(out) >= top_k:
                    break
            if len(out) >= top_k:
                break
    return out[:top_k]


def _pull_tavily(ticker: str, market: str, topic: str, days_back: int) -> list[ResearchHit]:
    """Pull Tavily hits for a specific topic. Cached 7d via autoresearch."""
    import os
    if os.environ.get("COUNCIL_NO_TAVILY"):
        return []
    try:
        from agents.autoresearch import search_ticker
    except Exception:
        return []
    try:
        r = search_ticker(ticker, topic=topic, market=market, days_back=days_back)
    except Exception:
        return []
    if r.error or not r.results:
        return []
    out: list[ResearchHit] = []
    for h in r.results[:5]:
        out.append(ResearchHit(
            kind=f"tavily_{topic}",
            source="Tavily",
            title=(h.title or "")[:200],
            claim=(h.content or "")[:500],
            date=h.published_date or "",
            url=h.url or "",
            confidence=float(h.score or 0.5),
            stance="fact",
            extra={"topic": topic},
        ))
    return out


def _source_accuracy(market: str, aliases: list[str]) -> dict[str, float]:
    """Pull historical accuracy per source from analyst_backtest output if available.
    Returns {source: accuracy_0_to_1}. Empty if no backtest data."""
    db = DBS[market]
    if not db.exists():
        return {}
    out: dict[str, float] = {}
    with sqlite3.connect(db) as c:
        try:
            for tk in aliases:
                rows = c.execute("""
                    SELECT source, AVG(CASE WHEN correct = 1 THEN 1.0 ELSE 0.0 END) AS acc, COUNT(*) AS n
                    FROM analyst_backtest_results
                    WHERE ticker = ? AND correct IS NOT NULL
                    GROUP BY source
                    HAVING n >= 3
                """, (tk,)).fetchall()
                for r in rows:
                    out[r[0]] = float(r[1])
        except sqlite3.OperationalError:
            pass
    return out


# ─────────────────────────────────────────────────────────────────────
# Main builder
# ─────────────────────────────────────────────────────────────────────


def build_research_brief(
    ticker: str,
    market: str = "br",
    *,
    enable_tavily: bool = True,
) -> ResearchBrief:
    aliases = _aliases_with_ticker_variants(ticker)
    brief = ResearchBrief(
        ticker=ticker,
        market=market,
        aliases=aliases,
        fetched_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )

    brief.analyst_hits = _pull_analyst_insights(ticker, market, aliases)
    brief.event_hits = _pull_events(ticker, market, aliases)
    brief.video_hits = _pull_videos(ticker, aliases)
    brief.bibliotheca_hits = _pull_bibliotheca(ticker, aliases)

    if enable_tavily:
        brief.tavily_news_hits = _pull_tavily(ticker, market, "news", days_back=30)
        brief.tavily_guidance_hits = _pull_tavily(ticker, market, "guidance", days_back=90)
        brief.tavily_insider_hits = _pull_tavily(ticker, market, "scandal", days_back=180)

    brief.source_accuracy = _source_accuracy(market, aliases)

    # Notes
    if not brief.analyst_hits:
        brief.notes.append(f"Sem analyst_insights na DB para {ticker} (ou aliases). Considerar fetch de subscriptions.")
    if not brief.event_hits:
        brief.notes.append(f"Sem CVM/SEC events para {ticker}. Considerar correr cvm_monitor / sec_monitor.")

    return brief
