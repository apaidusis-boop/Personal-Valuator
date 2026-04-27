"""_captains_log — data layer para a página Captain's Log do dashboard.

Pure-data: zero rendering, zero Streamlit imports. Funções devolvem dicts/lists
prontos para o dashboard renderizar com `_components`.

Fontes (read-only):
    - data/{br,us}_investments.db (conviction_scores, watchlist_actions,
      perpetuum_health, quarterly_history)
    - obsidian_vault/tickers/*_IC_DEBATE.md (frontmatter + verdict)
    - obsidian_vault/tickers/*_VARIANT.md (frontmatter)

Cache leve via lru_cache nos parsers de ficheiro; o dashboard adiciona
@st.cache_data por cima para TTL.
"""
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_BR = ROOT / "data" / "br_investments.db"
DB_US = ROOT / "data" / "us_investments.db"
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"


# --- Frontmatter parser ---

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def _parse_frontmatter(text: str) -> dict:
    """Tiny YAML-ish frontmatter parser. Strings, ints, floats, lists [a, b]."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            out[key] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
        elif val and val[0].isdigit() and val.replace(".", "", 1).isdigit():
            out[key] = float(val) if "." in val else int(val)
        else:
            out[key] = val
    return out


# --- Conviction ---

@dataclass
class ConvictionRow:
    ticker: str
    market: str
    composite_score: int
    thesis_health: int
    ic_consensus: int
    variant: int
    data_coverage: int
    run_date: str


def top_conviction(n: int = 5) -> list[ConvictionRow]:
    """Top-N holdings por composite_score (latest run, both markets)."""
    if not DB_BR.exists():
        return []
    with sqlite3.connect(DB_BR) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT ticker, market, run_date, composite_score, thesis_health,
                   ic_consensus, variant, data_coverage
            FROM conviction_scores
            WHERE run_date = (SELECT MAX(run_date) FROM conviction_scores)
            ORDER BY composite_score DESC
            LIMIT ?
        """, (n,)).fetchall()
    return [
        ConvictionRow(
            ticker=r["ticker"], market=r["market"], run_date=r["run_date"],
            composite_score=int(r["composite_score"] or 0),
            thesis_health=int(r["thesis_health"] or 0),
            ic_consensus=int(r["ic_consensus"] or 0),
            variant=int(r["variant"] or 0),
            data_coverage=int(r["data_coverage"] or 0),
        ) for r in rows
    ]


# --- Open actions (pending decisions) ---

@dataclass
class OpenAction:
    id: int
    ticker: str
    market: str
    kind: str
    action_hint: str
    opened_at: str


def open_actions(limit: int = 10) -> list[OpenAction]:
    """Open watchlist_actions across both DBs. Most recent first."""
    out: list[OpenAction] = []
    for market, db in (("br", DB_BR), ("us", DB_US)):
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            c.row_factory = sqlite3.Row
            rows = c.execute("""
                SELECT id, ticker, kind, action_hint, opened_at
                FROM watchlist_actions
                WHERE status='open'
                ORDER BY opened_at DESC
            """).fetchall()
        for r in rows:
            out.append(OpenAction(
                id=r["id"], ticker=r["ticker"], market=market,
                kind=r["kind"] or "",
                action_hint=(r["action_hint"] or "")[:140],
                opened_at=r["opened_at"] or "",
            ))
    out.sort(key=lambda a: a.opened_at, reverse=True)
    return out[:limit]


# --- IC debates ---

@dataclass
class ICDebate:
    ticker: str
    market: str
    date: str
    verdict: str
    confidence: str
    consensus_pct: float
    path: Path


@lru_cache(maxsize=128)
def _read_ic_frontmatter(path_str: str) -> dict:
    p = Path(path_str)
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return {}
    return _parse_frontmatter(text)


def recent_ic_debates(n: int = 5) -> list[ICDebate]:
    """Latest IC debates across vault, sorted by date desc."""
    if not TICKERS_DIR.exists():
        return []
    out: list[ICDebate] = []
    for f in TICKERS_DIR.glob("*_IC_DEBATE.md"):
        fm = _read_ic_frontmatter(str(f))
        if not fm or fm.get("type") != "synthetic_ic_debate":
            continue
        out.append(ICDebate(
            ticker=str(fm.get("ticker", f.stem.replace("_IC_DEBATE", ""))),
            market=str(fm.get("market", "")),
            date=str(fm.get("date", "")),
            verdict=str(fm.get("committee_verdict", "UNKNOWN")),
            confidence=str(fm.get("confidence", "")),
            consensus_pct=float(fm.get("consensus_pct", 0) or 0),
            path=f,
        ))
    out.sort(key=lambda d: d.date, reverse=True)
    return out[:n]


# --- Variant perception ---

@dataclass
class VariantView:
    ticker: str
    market: str
    date: str
    variance: str
    magnitude: int
    path: Path


@lru_cache(maxsize=128)
def _read_variant_frontmatter(path_str: str) -> dict:
    return _parse_frontmatter(Path(path_str).read_text(encoding="utf-8")) if Path(path_str).exists() else {}


def high_variance_views(n: int = 5, min_magnitude: int = 1) -> list[VariantView]:
    """Variant views ordered by magnitude desc, magnitude >= min_magnitude."""
    if not TICKERS_DIR.exists():
        return []
    out: list[VariantView] = []
    for f in TICKERS_DIR.glob("*_VARIANT.md"):
        fm = _read_variant_frontmatter(str(f))
        if not fm or fm.get("type") != "variant_perception":
            continue
        magnitude = int(fm.get("magnitude", 0) or 0)
        if magnitude < min_magnitude:
            continue
        out.append(VariantView(
            ticker=str(fm.get("ticker", f.stem.replace("_VARIANT", ""))),
            market=str(fm.get("market", "")),
            date=str(fm.get("date", "")),
            variance=str(fm.get("variance", "unknown")),
            magnitude=magnitude,
            path=f,
        ))
    out.sort(key=lambda v: (v.magnitude, v.date), reverse=True)
    return out[:n]


# --- Perpetuum alerts (drop_alerts from latest run) ---

@dataclass
class PerpetuumAlert:
    perpetuum_name: str
    subject_id: str
    score: int
    prev_score: int
    drop: int
    run_date: str


def recent_alerts(n: int = 5) -> list[PerpetuumAlert]:
    """Perpetuum drop_alerts from latest run."""
    if not DB_BR.exists():
        return []
    with sqlite3.connect(DB_BR) as c:
        c.row_factory = sqlite3.Row
        try:
            rows = c.execute("""
                SELECT perpetuum_name, subject_id, score, run_date, details_json
                FROM perpetuum_health
                WHERE run_date = (SELECT MAX(run_date) FROM perpetuum_health)
                  AND details_json LIKE '%alert_drop%'
                ORDER BY score ASC
                LIMIT ?
            """, (n * 3,)).fetchall()
        except sqlite3.OperationalError:
            return []
    out: list[PerpetuumAlert] = []
    for r in rows:
        try:
            details = json.loads(r["details_json"] or "{}")
        except json.JSONDecodeError:
            continue
        if "alert_drop" not in details:
            continue
        out.append(PerpetuumAlert(
            perpetuum_name=r["perpetuum_name"],
            subject_id=r["subject_id"],
            score=int(r["score"] or 0),
            prev_score=int(details.get("prev_score", 0) or 0),
            drop=int(details.get("alert_drop", 0) or 0),
            run_date=r["run_date"],
        ))
    out.sort(key=lambda a: a.drop, reverse=True)
    return out[:n]


# --- RI material changes (last quarter YoY deltas) ---

@dataclass
class RIChange:
    ticker: str
    period_end: str
    metric: str
    yoy_pct: float
    direction: str  # "up" | "down"


def recent_ri_changes(n: int = 5, threshold_pct: float = 15.0) -> list[RIChange]:
    """For each holding stock, compute YoY change on latest quarter.
    Surface anything with |YoY| >= threshold_pct on revenue/ebit/net_income.
    """
    if not DB_BR.exists():
        return []
    out: list[RIChange] = []
    with sqlite3.connect(DB_BR) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT ticker, period_end, revenue, ebit, net_income
            FROM quarterly_history
            WHERE source='ITR' OR source='DFP'
            ORDER BY ticker, period_end
        """).fetchall()
    by_ticker: dict[str, list[dict]] = {}
    for r in rows:
        by_ticker.setdefault(r["ticker"], []).append(dict(r))

    for ticker, qs in by_ticker.items():
        qs.sort(key=lambda q: q["period_end"])
        if len(qs) < 5:
            continue
        latest = qs[-1]
        # Find same period -1y
        latest_period = latest["period_end"]
        try:
            y, m, d = latest_period.split("-")
            prior_period = f"{int(y)-1}-{m}-{d}"
        except Exception:
            continue
        prior = next((q for q in qs if q["period_end"] == prior_period), None)
        if not prior:
            continue
        for metric in ("revenue", "ebit", "net_income"):
            curr = latest.get(metric) or 0
            prev = prior.get(metric) or 0
            if not prev or prev == 0:
                continue
            yoy = (curr - prev) / abs(prev) * 100
            if abs(yoy) >= threshold_pct:
                out.append(RIChange(
                    ticker=ticker, period_end=latest_period,
                    metric=metric, yoy_pct=yoy,
                    direction="up" if yoy > 0 else "down",
                ))
    out.sort(key=lambda c: abs(c.yoy_pct), reverse=True)
    return out[:n]


# --- Pulse summary (single-row dashboard header) ---

@dataclass
class Pulse:
    holdings_count: int
    open_actions_count: int
    perpetuum_alerts_count: int
    high_variance_count: int
    last_perpetuum_run: str | None


def pulse() -> Pulse:
    holdings = 0
    actions = 0
    for db in (DB_BR, DB_US):
        if not db.exists():
            continue
        with sqlite3.connect(db) as c:
            holdings += c.execute(
                "SELECT COUNT(*) FROM portfolio_positions WHERE active=1"
            ).fetchone()[0]
            try:
                actions += c.execute(
                    "SELECT COUNT(*) FROM watchlist_actions WHERE status='open'"
                ).fetchone()[0]
            except sqlite3.OperationalError:
                pass

    alerts = len(recent_alerts(n=50))
    variance = len(high_variance_views(n=50, min_magnitude=2))

    last_run = None
    if DB_BR.exists():
        with sqlite3.connect(DB_BR) as c:
            try:
                r = c.execute(
                    "SELECT MAX(run_date) FROM perpetuum_health"
                ).fetchone()
                last_run = r[0] if r else None
            except sqlite3.OperationalError:
                pass

    return Pulse(
        holdings_count=holdings,
        open_actions_count=actions,
        perpetuum_alerts_count=alerts,
        high_variance_count=variance,
        last_perpetuum_run=last_run,
    )
