"""Evidence Ledger — Sprint 3 of STORYT_3.0.

Every metric, claim, and qualitative fact in the storytelling has a trace:
where it came from, when it was fetched, and (when applicable) a URL the
reader can follow to verify.

The ledger is built incrementally during the dossier construction:
  - Fundamentals → source: "yfinance Ticker.info" + fetched_at
  - Annual evolution → source: "yfinance Ticker.financials cached" + period
  - Quality scores → source: "scoring.beneish/altman/piotroski + period"
  - Peer benchmark → source: "DB fundamentals × N peers"
  - Research hits → source: "<source>" + URL from ResearchHit.url
  - Tavily → source: "Tavily news/guidance" + URL

The narrative engine receives the ledger; each claim it writes references
[N] back to a ledger entry. The ledger is then appended to the storytelling.

Unsourced claims (LLM invented something not in ledger) get caught by the
fact-check pass (Sprint 5) — currently flagged as TODO.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Evidence:
    idx: int                 # 1-based footnote index
    claim: str               # the metric/fact (max ~150 chars)
    value: str = ""          # the actual number or quote (max ~100 chars)
    source: str = ""         # human-readable source name
    url: str = ""            # link if applicable
    fetched_at: str = ""     # ISO timestamp
    confidence: str = "computed"  # 'computed' | 'reported' | 'extracted' | 'inferred' | 'unsourced'
    section: str = ""        # which section of dossier ("fundamentals", "scoring", "research", "peer")


@dataclass
class EvidenceLedger:
    entries: list[Evidence] = field(default_factory=list)
    _next_idx: int = 1

    def add(
        self,
        claim: str,
        value: str = "",
        *,
        source: str = "",
        url: str = "",
        confidence: str = "computed",
        section: str = "",
        fetched_at: str | None = None,
    ) -> int:
        """Add an entry. Returns the footnote index."""
        idx = self._next_idx
        self._next_idx += 1
        self.entries.append(Evidence(
            idx=idx,
            claim=claim[:200],
            value=value[:200],
            source=source[:200],
            url=url[:500],
            fetched_at=fetched_at or datetime.now(timezone.utc).isoformat(timespec="seconds"),
            confidence=confidence,
            section=section,
        ))
        return idx

    def render_md(self) -> str:
        """Markdown table appended to storytelling for audit trail."""
        if not self.entries:
            return "_(Sem evidências registadas — pipeline degraded.)_"
        lines = [
            "| # | Claim | Valor | Fonte | URL | Confiança | Fetched |",
            "|---|---|---|---|---|---|---|",
        ]
        for e in self.entries:
            url_cell = f"[link]({e.url})" if e.url else "—"
            value_cell = e.value[:60].replace("|", "\\|") or "—"
            claim_cell = e.claim[:80].replace("|", "\\|")
            source_cell = e.source[:60].replace("|", "\\|")
            fetched = e.fetched_at[:10] if e.fetched_at else "—"
            lines.append(
                f"| [{e.idx}] | {claim_cell} | {value_cell} | {source_cell} | {url_cell} | `{e.confidence}` | {fetched} |"
            )
        return "\n".join(lines)

    def to_json(self) -> list[dict]:
        return [
            {
                "idx": e.idx,
                "claim": e.claim,
                "value": e.value,
                "source": e.source,
                "url": e.url,
                "fetched_at": e.fetched_at,
                "confidence": e.confidence,
                "section": e.section,
            }
            for e in self.entries
        ]

    def by_section(self) -> dict[str, list[Evidence]]:
        out: dict[str, list[Evidence]] = {}
        for e in self.entries:
            out.setdefault(e.section, []).append(e)
        return out

    def stats(self) -> dict:
        confidence_counts: dict[str, int] = {}
        for e in self.entries:
            confidence_counts[e.confidence] = confidence_counts.get(e.confidence, 0) + 1
        return {
            "total": len(self.entries),
            "by_confidence": confidence_counts,
            "with_url": sum(1 for e in self.entries if e.url),
        }


# ─────────────────────────────────────────────────────────────────────
# Builder — given a dossier + research_brief, populate the ledger
# ─────────────────────────────────────────────────────────────────────


def build_ledger_from_dossier(dossier, research_brief=None, peer_benchmark=None) -> EvidenceLedger:
    """Walk the dossier and emit evidence entries for each metric."""
    L = EvidenceLedger()

    # Fundamentals (yfinance + brapi cached)
    f = dossier.fundamentals or {}
    fetched_at_fund = f.get("fetched_at") or ""
    if f.get("pe") is not None:
        L.add(
            "P/E ratio (TTM)",
            value=f"{f['pe']:.2f}x",
            source="yfinance Ticker.info → fundamentals table",
            url=f"https://finance.yahoo.com/quote/{dossier.ticker}{'.SA' if dossier.market=='br' else ''}",
            confidence="reported",
            section="fundamentals",
            fetched_at=fetched_at_fund or None,
        )
    if f.get("pb") is not None:
        L.add(
            "P/B ratio",
            value=f"{f['pb']:.2f}x",
            source="yfinance Ticker.info",
            url=f"https://finance.yahoo.com/quote/{dossier.ticker}{'.SA' if dossier.market=='br' else ''}",
            confidence="reported",
            section="fundamentals",
        )
    if f.get("dy") is not None:
        L.add(
            "Dividend Yield (reportado, inclui extraordinárias)",
            value=f"{f['dy']*100:.2f}%",
            source="yfinance Ticker.info",
            url=f"https://finance.yahoo.com/quote/{dossier.ticker}{'.SA' if dossier.market=='br' else ''}",
            confidence="reported",
            section="fundamentals",
        )
    if f.get("roe") is not None:
        L.add(
            "ROE (Return on Equity)",
            value=f"{f['roe']*100:.2f}%",
            source="yfinance Ticker.info",
            confidence="reported",
            section="fundamentals",
        )
    if f.get("net_debt_ebitda") is not None:
        L.add(
            "ND/EBITDA reportado",
            value=f"{f['net_debt_ebitda']:.2f}x",
            source="yfinance derived",
            confidence="computed",
            section="fundamentals",
        )
    if f.get("dividend_streak_years"):
        L.add(
            "Dividend streak (anos consecutivos)",
            value=f"{int(f['dividend_streak_years'])} anos",
            source="dividends table aggregation",
            confidence="computed",
            section="fundamentals",
        )

    # Last price
    if dossier.last_price:
        L.add(
            "Preço de fechamento mais recente",
            value=f"R$ {dossier.last_price:.2f}" if dossier.market == "br" else f"$ {dossier.last_price:.2f}",
            source="yfinance daily prices",
            url=f"https://finance.yahoo.com/quote/{dossier.ticker}{'.SA' if dossier.market=='br' else ''}/history",
            confidence="reported",
            section="fundamentals",
            fetched_at=dossier.last_price_date or "",
        )

    # Quality scores
    qs = dossier.quality_scores or {}
    if "piotroski" in qs:
        p = qs["piotroski"]
        L.add(
            "Piotroski F-Score",
            value=f"{p.get('f_score')}/9",
            source="scoring.piotroski (computed from yfinance balance + cashflow)",
            confidence="computed",
            section="scoring",
            fetched_at=p.get("period_end") or "",
        )
    if "altman" in qs:
        a = qs["altman"]
        L.add(
            "Altman Z-Score",
            value=f"{a.get('z'):.2f} ({a.get('zone')})",
            source="scoring.altman (5 ratios)",
            confidence="computed",
            section="scoring",
            fetched_at=a.get("period_end") or "",
        )
    if "beneish" in qs:
        b = qs["beneish"]
        L.add(
            "Beneish M-Score",
            value=f"{b.get('m'):.2f} ({b.get('zone')})",
            source="scoring.beneish (8 indices)",
            confidence="computed",
            section="scoring",
            fetched_at=b.get("period_end") or "",
        )

    # Peer benchmark
    if peer_benchmark and peer_benchmark.n_peers > 0:
        peers_str = ", ".join(peer_benchmark.peers_used[:8])
        if len(peer_benchmark.peers_used) > 8:
            peers_str += f" +{len(peer_benchmark.peers_used)-8} outros"
        L.add(
            f"Peer benchmark — sector={peer_benchmark.sector} ({peer_benchmark.market.upper()})",
            value=f"{peer_benchmark.n_peers} peers · source={peer_benchmark.source}",
            source=f"DB fundamentals: {peers_str}",
            confidence="computed",
            section="peer",
        )

    # Research hits — each becomes evidence entry
    if research_brief:
        for h in research_brief.analyst_hits[:10]:
            L.add(
                f"Analyst insight ({h.stance})",
                value=h.claim[:100],
                source=h.source,
                url=h.url,
                confidence="reported",
                section="research",
                fetched_at=h.date or "",
            )
        for h in research_brief.event_hits[:5]:
            L.add(
                f"CVM/SEC event ({h.kind})",
                value=h.claim[:100],
                source=h.source,
                url=h.url,
                confidence="reported",
                section="research",
                fetched_at=h.date or "",
            )
        for h in research_brief.video_hits[:6]:
            L.add(
                f"YouTube insight ({h.stance})",
                value=h.claim[:100],
                source=h.source,
                url=h.url,
                confidence="extracted",
                section="research",
                fetched_at=h.date or "",
            )
        for h in research_brief.tavily_news_hits[:4]:
            L.add(
                "Tavily news",
                value=h.title[:100],
                source="Tavily web search",
                url=h.url,
                confidence="extracted",
                section="research",
                fetched_at=h.date or "",
            )
        for h in research_brief.tavily_guidance_hits[:3]:
            L.add(
                "Tavily guidance",
                value=h.title[:100],
                source="Tavily web search",
                url=h.url,
                confidence="extracted",
                section="research",
                fetched_at=h.date or "",
            )

    return L
