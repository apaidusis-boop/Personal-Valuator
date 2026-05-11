"""CouncilDossier — factual layer the council reads (no opinions).

Mirrors STORYT_1's Camadas 1-5: pulls structured facts only. Three council
voices receive the *same* dossier text and produce *different* opinions on it.
That isolation is the whole point — same inputs, different lenses.

The dossier is intentionally short (~80-120 lines) so each Ollama call has
room for reasoning rather than re-summarising data.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DBS = {"br": ROOT / "data" / "br_investments.db", "us": ROOT / "data" / "us_investments.db"}


@dataclass
class CouncilDossier:
    ticker: str
    market: str  # "br" | "us"
    name: str = ""
    sector: str = ""
    modo: str = "A"            # A=industrial/consumer, B=banks, C=commodity, D=FII/REIT
    is_holding: bool = False
    quantity: float | None = None
    entry_price: float | None = None
    last_price: float | None = None
    last_price_date: str = ""
    fundamentals: dict = field(default_factory=dict)
    quarterly_trajectory: list[dict] = field(default_factory=list)
    thesis_text: str = ""
    portfolio_context: dict = field(default_factory=dict)
    # Phase Council v1.1 enrichment — scoring engines + qualitative web research
    quality_scores: dict = field(default_factory=dict)  # beneish/altman/piotroski
    web_context: list[dict] = field(default_factory=list)  # Tavily hits (qualitative facts)
    # STORYT_3.0 — research brief (Sprint 1) + peer benchmark (Sprint 2)
    research_brief: object | None = None  # ResearchBrief — typed in Sprint 1
    peer_benchmark: object | None = None  # SectorBenchmark — typed in Sprint 2

    def detect_modo(self) -> str:
        """STORYT_1 Camada 5 detection logic — sector-driven."""
        s = (self.sector or "").lower()
        # Modo D — FIIs (BR) or REITs (US)
        if self.ticker.endswith("11") or "real estate" in s or "fii" in s or "reit" in s:
            return "D"
        # Modo B — financials
        if any(k in s for k in ("bank", "insurance", "finan", "broker")):
            return "B"
        # Modo C — commodities
        if any(k in s for k in (
            "oil", "gas", "min", "steel", "pulp", "paper", "fertilizer", "alumin",
            "metal", "commodit",
        )):
            return "C"
        # Modo A — default
        return "A"

    def render_facts_block(self) -> str:
        """Compact factual block fed to each council member's prompt."""
        f = self.fundamentals
        lines = [
            f"=== TICKER: {self.market.upper()}:{self.ticker} — {self.name} ===",
            f"Sector: {self.sector or '?'}  |  Modo (auto): {self.modo}  |  Held: {self.is_holding}",
        ]
        if self.last_price:
            lines.append(f"Last price: {self.last_price} ({self.last_price_date})")
        if self.is_holding and self.quantity:
            lines.append(f"Position: {self.quantity:.0f} shares @ entry {self.entry_price}")

        if f:
            mp = []
            for k, lbl in [
                ("pe", "P/E"), ("pb", "P/B"), ("dy", "DY"), ("roe", "ROE"),
                ("net_debt_ebitda", "ND/EBITDA"), ("current_ratio", "CR"),
                ("dividend_streak_years", "DivStreak"),
            ]:
                v = f.get(k)
                if v is None:
                    continue
                if k in ("dy", "roe") and isinstance(v, (int, float)) and abs(v) < 5:
                    mp.append(f"{lbl}={v*100:.1f}%")
                elif isinstance(v, (int, float)):
                    mp.append(f"{lbl}={v:.2f}")
                else:
                    mp.append(f"{lbl}={v}")
            if mp:
                lines.append("Fundamentals: " + " | ".join(mp))

        if self.quarterly_trajectory:
            lines.append("\nQuarterly (last 6, R$ M):")
            for r in self.quarterly_trajectory:
                rev = (r.get("revenue") or 0) / 1e6
                ebit = (r.get("ebit") or 0) / 1e6
                ni = (r.get("net_income") or 0) / 1e6
                em = (r.get("ebit_margin") or 0) * 100
                lines.append(
                    f"  {r['period_end']}: rev={rev:7.1f}  ebit={ebit:6.1f}  ni={ni:6.1f}  ebit_margin={em:5.1f}%"
                )

        if self.thesis_text:
            lines.append(f"\nVAULT THESIS (~800 chars):\n{self.thesis_text[:800]}")

        if self.portfolio_context:
            pc = self.portfolio_context
            lines.append("\nPORTFOLIO CONTEXT:")
            if "total_positions" in pc:
                lines.append(f"  Active positions ({self.market.upper()}): {pc['total_positions']}")
            if "weight_pct" in pc and pc["weight_pct"] is not None:
                lines.append(f"  This position weight: {pc['weight_pct']:.1f}%")
            if "sector_weight_pct" in pc and pc["sector_weight_pct"] is not None:
                lines.append(f"  Sector weight: {pc['sector_weight_pct']:.1f}%")

        if self.quality_scores:
            lines.append("\nQUALITY SCORES:")
            qs = self.quality_scores
            if "piotroski" in qs:
                p = qs["piotroski"]
                lines.append(f"  Piotroski F-Score: {p.get('f_score')}/9 ({p.get('period_end','?')})")
            if "altman" in qs:
                a = qs["altman"]
                lines.append(
                    f"  Altman Z-Score: {a.get('z'):.2f}  zone={a.get('zone')}"
                    f"  conf={a.get('confidence')}"
                )
                if a.get("notes"):
                    lines.append(f"    note: {' | '.join(a['notes'][:1])}")
            if "beneish" in qs:
                b = qs["beneish"]
                lines.append(
                    f"  Beneish M-Score: {b.get('m'):.2f}  zone={b.get('zone')}  conf={b.get('confidence')}"
                )

        if self.web_context:
            lines.append("\nWEB CONTEXT (qualitative research, last 30-90d):")
            for hit in self.web_context[:6]:
                pub = f" [{hit.get('published','')[:10]}]" if hit.get("published") else ""
                lines.append(f"  - {hit.get('title','')[:140]}{pub}")
                if hit.get("content"):
                    lines.append(f"    {hit['content'][:240]}")

        # STORYT_3.0 — Research Brief (Ulisses) projection
        if self.research_brief is not None:
            try:
                brief_text = self.research_brief.render_for_council(max_per_section=6)
                lines.append("\n" + "=" * 60)
                lines.append("RESEARCH BRIEFING (Ulisses Navegador puxou da casa):")
                lines.append("=" * 60)
                lines.append(brief_text)
            except Exception as e:
                lines.append(f"\n(Research brief render error: {e})")

        # STORYT_3.0 — Peer benchmark line
        if self.peer_benchmark is not None:
            try:
                pb = self.peer_benchmark
                lines.append(f"\nPEER BENCHMARK ({pb.market.upper()}, sector={pb.sector}, n={pb.n_peers}, source={pb.source}):")
                if pb.median_pe is not None: lines.append(f"  - Mediana P/E: {pb.median_pe:.2f}x")
                if pb.median_pb is not None: lines.append(f"  - Mediana P/B: {pb.median_pb:.2f}x")
                if pb.median_dy is not None: lines.append(f"  - Mediana DY: {pb.median_dy*100:.1f}%")
                if pb.median_roe is not None: lines.append(f"  - Mediana ROE: {pb.median_roe*100:.1f}%")
                if pb.median_nde is not None: lines.append(f"  - Mediana ND/EBITDA: {pb.median_nde:.2f}x")
                if pb.median_fcf_yield is not None: lines.append(f"  - Mediana FCF Yield: {pb.median_fcf_yield*100:.1f}%")
            except Exception as e:
                lines.append(f"(peer benchmark render error: {e})")

        return "\n".join(lines)


def _row(con: sqlite3.Connection, sql: str, args=()) -> dict:
    con.row_factory = sqlite3.Row
    r = con.execute(sql, args).fetchone()
    return dict(r) if r else {}


def _rows(con: sqlite3.Connection, sql: str, args=()) -> list[dict]:
    con.row_factory = sqlite3.Row
    return [dict(r) for r in con.execute(sql, args).fetchall()]


def _read_vault_thesis(ticker: str) -> str:
    """Reuse the canonical vault reader — same as synthetic_ic.py."""
    try:
        from agents._common import read_vault_thesis
        return read_vault_thesis(ticker, max_chars=1500) or ""
    except Exception:
        return ""


def _portfolio_context(con: sqlite3.Connection, ticker: str, sector: str) -> dict:
    """Total positions + weight estimates. Light — Portfolio Officer can deepen."""
    out: dict = {}
    try:
        n = con.execute(
            "SELECT COUNT(*) FROM portfolio_positions WHERE active=1"
        ).fetchone()[0]
        out["total_positions"] = n
    except sqlite3.OperationalError:
        return out

    # Approximate weight: quantity * latest close / sum(quantity * latest close)
    try:
        rows = con.execute("""
            SELECT p.ticker, p.quantity,
                   (SELECT close FROM prices pr WHERE pr.ticker = p.ticker
                    ORDER BY date DESC LIMIT 1) AS last_close,
                   c.sector
            FROM portfolio_positions p
            LEFT JOIN companies c ON c.ticker = p.ticker
            WHERE p.active=1
        """).fetchall()
        values = []
        target_value = None
        sector_value = 0.0
        for r in rows:
            q = r[1] or 0
            px = r[2] or 0
            v = float(q) * float(px)
            values.append(v)
            if r[0] == ticker:
                target_value = v
            if sector and (r[3] or "") == sector:
                sector_value += v
        total = sum(values) or 1.0
        if target_value is not None:
            out["weight_pct"] = target_value / total * 100
        if sector:
            out["sector_weight_pct"] = sector_value / total * 100
    except Exception:
        pass
    return out


def _quality_scores(ticker: str, market: str) -> dict:
    """Compute Piotroski/Altman/Beneish on demand. Each is wrapped in a try
    block — any failure leaves that key absent rather than blowing up the
    dossier build. The council/narrative read these as 'available or not'."""
    out: dict = {}
    try:
        from scoring.piotroski import compute as pt_compute
        s = pt_compute(ticker, market=market)
        if s and s.applicable:
            out["piotroski"] = {
                "f_score": s.f_score,
                "period_end": getattr(s, "period_t", None),
            }
    except Exception:
        pass
    try:
        from scoring.altman import compute as al_compute
        s = al_compute(ticker, market=market)
        if s and s.applicable:
            out["altman"] = {
                "z": s.z,
                "zone": s.zone,
                "confidence": s.confidence,
                "period_end": s.period_end,
                "notes": list(getattr(s, "notes", []) or []),
            }
    except Exception:
        pass
    try:
        from scoring.beneish import compute as bn_compute
        s = bn_compute(ticker, market=market)
        if s and s.applicable:
            out["beneish"] = {
                "m": s.m,
                "zone": s.zone,
                "confidence": s.confidence,
                "period_end": s.period_end,
            }
    except Exception:
        pass
    return out


def _web_context(ticker: str, market: str, *, days_back: int = 60) -> list[dict]:
    """Pull qualitative context via Tavily (Phase K wire). Two queries:
    'news' and 'guidance'. Cache 7d so re-runs are free. Disabled by setting
    env COUNCIL_NO_TAVILY=1."""
    import os
    if os.environ.get("COUNCIL_NO_TAVILY"):
        return []
    try:
        from agents.autoresearch import search_ticker
    except Exception:
        return []
    hits: list[dict] = []
    for topic in ("news", "guidance"):
        try:
            r = search_ticker(ticker, topic=topic, market=market, days_back=days_back)
        except Exception:
            continue
        if r.error or not r.results:
            continue
        for h in r.results[:3]:
            hits.append({
                "title": h.title,
                "score": h.score,
                "published": h.published_date,
                "content": h.content,
                "topic": topic,
            })
    # dedup by title (rough)
    seen: set[str] = set()
    deduped: list[dict] = []
    for h in hits:
        k = (h.get("title") or "")[:80]
        if k in seen:
            continue
        seen.add(k)
        deduped.append(h)
    return deduped[:6]


def build_dossier(
    ticker: str,
    market: str = "br",
    *,
    enrich_scores: bool = True,
    enrich_web: bool = True,
    enrich_research_brief: bool = True,
    enrich_peer_benchmark: bool = True,
) -> CouncilDossier:
    """Pull a CouncilDossier from the market's DB. Degrades gracefully on missing data.

    Args:
      enrich_scores: run Piotroski/Altman/Beneish on demand. Adds ~5-10s.
      enrich_web: pull Tavily news+guidance. Adds ~2-5s, costs 1-2 API calls
                  (cached 7d). Set COUNCIL_NO_TAVILY=1 to skip globally.
      enrich_research_brief: Ulisses pulls analyst_insights, events, videos,
                             Bibliotheca chunks, Tavily news+guidance+insider.
                             Adds ~3-8s. STORYT_3.0 Sprint 1.
      enrich_peer_benchmark: compute sector medians from DB (P/E, P/B, DY, ROE,
                             ND/EBITDA, FCF Yield). STORYT_3.0 Sprint 2.
    """
    db = DBS[market]
    if not db.exists():
        return CouncilDossier(ticker=ticker, market=market)

    with sqlite3.connect(db) as con:
        co = _row(con, "SELECT name, sector, is_holding FROM companies WHERE ticker=?", (ticker,))
        f = _row(
            con,
            "SELECT * FROM fundamentals WHERE ticker=? ORDER BY period_end DESC LIMIT 1",
            (ticker,),
        )
        try:
            qh = _rows(
                con,
                "SELECT period_end, revenue, ebit, net_income, ebit_margin "
                "FROM quarterly_single WHERE ticker=? ORDER BY period_end DESC LIMIT 6",
                (ticker,),
            )
        except sqlite3.OperationalError:
            qh = []
        price = _row(
            con,
            "SELECT date, close FROM prices WHERE ticker=? ORDER BY date DESC LIMIT 1",
            (ticker,),
        )
        try:
            pos = _row(
                con,
                "SELECT quantity, entry_price FROM portfolio_positions "
                "WHERE ticker=? AND active=1",
                (ticker,),
            )
        except sqlite3.OperationalError:
            pos = {}
        portfolio = _portfolio_context(con, ticker, co.get("sector") or "")

    d = CouncilDossier(
        ticker=ticker,
        market=market,
        name=co.get("name") or "",
        sector=co.get("sector") or "",
        is_holding=bool(co.get("is_holding") or pos),
        quantity=pos.get("quantity"),
        entry_price=pos.get("entry_price"),
        last_price=price.get("close"),
        last_price_date=price.get("date") or "",
        fundamentals=f,
        quarterly_trajectory=qh,
        thesis_text=_read_vault_thesis(ticker),
        portfolio_context=portfolio,
        quality_scores=(_quality_scores(ticker, market) if enrich_scores else {}),
        web_context=(_web_context(ticker, market) if enrich_web else []),
    )
    d.modo = d.detect_modo()

    # STORYT_3.0 enrichment — research brief + peer benchmark
    if enrich_research_brief:
        try:
            from agents.council.research_brief import build_research_brief
            d.research_brief = build_research_brief(ticker, market, enable_tavily=enrich_web)
        except Exception as e:
            d.research_brief = None

    if enrich_peer_benchmark:
        try:
            from agents.council.peer_engine import compute_sector_benchmark
            d.peer_benchmark = compute_sector_benchmark(ticker, market, d.sector or "")
        except Exception:
            d.peer_benchmark = None

    return d
