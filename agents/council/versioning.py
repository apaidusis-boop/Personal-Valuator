"""Versioning + Delta Engine — Sprint 4 of STORYT_3.0.

Solves: "Próxima vez que correr essa análise, no próximo earnings call,
como saberei o que mudou?"

Mechanism:
  1. Every council run saves a SNAPSHOT JSON in data/dossier_snapshots/<TICKER>/<DATE>.json
     containing every metric, score, philosophy, council outcome, evidence ledger.
  2. Storytelling MD is written to TWO locations:
        a) dossiers/<TICKER>_STORY.md            (latest — overwritten)
        b) dossiers/archive/<TICKER>_STORY_<DATE>.md (versioned — never overwritten)
  3. If a prior snapshot exists, a DELTA MD is generated comparing key metrics,
     stance flips, philosophy changes, new pre-pub flags:
        dossiers/<TICKER>_DELTA_<DATE>.md

This makes earnings-call refresh trivial: re-run pipeline, get delta MD that
says "Receita +5% vs último, ROE -2pp, Council mudou de BUY→HOLD, Risk Officer
flagou novo trigger" — all citable, all replicable.
"""
from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = ROOT / "data" / "dossier_snapshots"
DOSSIERS_DIR = ROOT / "obsidian_vault" / "dossiers"
ARCHIVE_DIR = DOSSIERS_DIR / "archive"


@dataclass
class DossierSnapshot:
    """Programmatic snapshot — diff target for next run."""
    ticker: str
    market: str
    date: str            # YYYY-MM-DD
    period_end: str      # period_end of latest fundamentals
    fundamentals: dict = field(default_factory=dict)
    quality_scores: dict = field(default_factory=dict)
    philosophy: dict = field(default_factory=dict)
    dcf: dict = field(default_factory=dict)
    council_stance: str = ""
    council_confidence: str = ""
    council_seats: list[str] = field(default_factory=list)
    pre_publication_flags: list[str] = field(default_factory=list)
    consensus_points: list[str] = field(default_factory=list)
    dissent_points: list[str] = field(default_factory=list)
    evidence_count: int = 0
    research_hits_total: int = 0


def _snapshot_path(ticker: str, run_date: date) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    p = SNAPSHOT_DIR / ticker
    p.mkdir(exist_ok=True)
    return p / f"{run_date.isoformat()}.json"


def save_snapshot(snapshot: DossierSnapshot) -> Path:
    p = _snapshot_path(snapshot.ticker, date.fromisoformat(snapshot.date))
    p.write_text(json.dumps(asdict(snapshot), indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def find_prior_snapshot(ticker: str, exclude_date: date | None = None) -> DossierSnapshot | None:
    """Find the most recent snapshot for this ticker, optionally excluding today's run."""
    p = SNAPSHOT_DIR / ticker
    if not p.exists():
        return None
    snaps = sorted(p.glob("*.json"), reverse=True)
    for snap_file in snaps:
        snap_date_str = snap_file.stem
        if exclude_date and snap_date_str == exclude_date.isoformat():
            continue
        try:
            data = json.loads(snap_file.read_text(encoding="utf-8"))
            return DossierSnapshot(**data)
        except Exception:
            continue
    return None


def archive_storytelling(latest_path: Path, run_date: date) -> Path:
    """Copy <TICKER>_STORY.md to archive/<TICKER>_STORY_<DATE>.md (versioned)."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    if not latest_path.exists():
        return latest_path
    archive_path = ARCHIVE_DIR / f"{latest_path.stem}_{run_date.isoformat()}.md"
    shutil.copy2(latest_path, archive_path)
    return archive_path


def _pct_change(new: float | None, old: float | None) -> str:
    if new is None or old is None:
        return "—"
    if old == 0:
        return "—"
    delta = (new - old) / abs(old) * 100
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.1f}%"


def _abs_change(new: float | None, old: float | None) -> str:
    if new is None or old is None:
        return "—"
    delta = new - old
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.2f}"


def render_delta_md(prior: DossierSnapshot, current: DossierSnapshot) -> str:
    """Build the DELTA markdown comparing two snapshots."""
    days_apart = (date.fromisoformat(current.date) - date.fromisoformat(prior.date)).days

    lines = [
        "---",
        "type: storyt2_delta",
        f"ticker: {current.ticker}",
        f"market: {current.market}",
        f"prior_date: {prior.date}",
        f"current_date: {current.date}",
        f"days_apart: {days_apart}",
        "tags: [storyt2, delta, audit]",
        "---",
        "",
        f"# Δ Delta — {current.ticker}",
        "",
        f"**Comparação**: `{prior.date}` → `{current.date}` ({days_apart} dias)",
        "",
        f"📖 [[{current.ticker}_STORY|Storytelling actual]] · 🏛️ [[{current.ticker}_COUNCIL|Council debate actual]]",
        "",
    ]

    # Council outcome flip
    lines.append("## Council outcome")
    lines.append("")
    if prior.council_stance != current.council_stance:
        flip = f"{prior.council_stance} → **{current.council_stance}**"
        lines.append(f"⚠️ **STANCE FLIP**: {flip}  ({prior.council_confidence} → {current.council_confidence})")
    else:
        lines.append(f"Stance mantido: **{current.council_stance}** (confiança: {prior.council_confidence} → {current.council_confidence})")
    lines.append("")

    # Fundamentals delta
    lines.append("## Métricas — variação")
    lines.append("")
    lines.append("| Métrica | Anterior | Actual | Δ % | Δ abs |")
    lines.append("|---|---|---|---|---|")
    for key, label, fmt in [
        ("pe", "P/E", "x"),
        ("pb", "P/B", "x"),
        ("dy", "DY", "%"),
        ("roe", "ROE", "%"),
        ("net_debt_ebitda", "ND/EBITDA", "x"),
    ]:
        old = prior.fundamentals.get(key)
        new = current.fundamentals.get(key)
        if old is None and new is None:
            continue
        if fmt == "%":
            old_str = f"{old*100:.2f}%" if old is not None else "—"
            new_str = f"{new*100:.2f}%" if new is not None else "—"
        else:
            old_str = f"{old:.2f}{fmt}" if old is not None else "—"
            new_str = f"{new:.2f}{fmt}" if new is not None else "—"
        lines.append(f"| {label} | {old_str} | {new_str} | {_pct_change(new, old)} | {_abs_change(new, old)} |")
    lines.append("")

    # Quality scores delta
    if prior.quality_scores or current.quality_scores:
        lines.append("## Quality scores — variação")
        lines.append("")
        for key, label in [("piotroski", "Piotroski"), ("altman", "Altman Z"), ("beneish", "Beneish M")]:
            old_d = prior.quality_scores.get(key) or {}
            new_d = current.quality_scores.get(key) or {}
            if not old_d and not new_d:
                continue
            old_v = old_d.get("f_score") or old_d.get("z") or old_d.get("m")
            new_v = new_d.get("f_score") or new_d.get("z") or new_d.get("m")
            old_zone = old_d.get("zone") or ("safe" if (old_v or 0) >= 7 else "?")
            new_zone = new_d.get("zone") or ("safe" if (new_v or 0) >= 7 else "?")
            change = ""
            if old_zone != new_zone and old_zone != "?" and new_zone != "?":
                change = f"  ⚠️ zona: {old_zone} → {new_zone}"
            lines.append(f"- **{label}**: {old_v} → {new_v}{change}")
        lines.append("")

    # DCF delta
    if prior.dcf and current.dcf:
        lines.append("## DCF base value")
        lines.append("")
        old_dcf = prior.dcf.get("base_value")
        new_dcf = current.dcf.get("base_value")
        old_mos = prior.dcf.get("margin_of_safety_pct")
        new_mos = current.dcf.get("margin_of_safety_pct")
        if old_dcf and new_dcf:
            lines.append(f"- **Valor base**: R$ {old_dcf:.2f} → R$ {new_dcf:.2f} ({_pct_change(new_dcf, old_dcf)})")
        if old_mos is not None and new_mos is not None:
            lines.append(f"- **Margem segurança**: {old_mos*100:+.0f}% → {new_mos*100:+.0f}%")
        lines.append("")

    # Philosophy
    if prior.philosophy != current.philosophy:
        lines.append("## Perfil filosófico")
        lines.append("")
        old_pri = prior.philosophy.get("primary", "?")
        new_pri = current.philosophy.get("primary", "?")
        if old_pri != new_pri:
            lines.append(f"- Primário: **{old_pri}** → **{new_pri}**")
        old_sec = prior.philosophy.get("secondary", "")
        new_sec = current.philosophy.get("secondary", "")
        if old_sec != new_sec:
            lines.append(f"- Secundário: {old_sec or '—'} → {new_sec or '—'}")
        lines.append("")

    # Pre-publication flags — added/resolved
    old_flags = set(prior.pre_publication_flags or [])
    new_flags = set(current.pre_publication_flags or [])
    added = new_flags - old_flags
    resolved = old_flags - new_flags
    if added or resolved:
        lines.append("## Pre-publication flags — diff")
        lines.append("")
        if added:
            lines.append("**Novas (este run)**:")
            for f in sorted(added):
                lines.append(f"- 🆕 {f}")
            lines.append("")
        if resolved:
            lines.append("**Resolvidas (presentes no anterior, ausentes agora)**:")
            for f in sorted(resolved):
                lines.append(f"- ✅ {f}")
            lines.append("")

    # Council seats delta
    old_seats = set(prior.council_seats or [])
    new_seats = set(current.council_seats or [])
    if old_seats != new_seats:
        lines.append("## Especialistas convocados — diff")
        lines.append("")
        added_seats = new_seats - old_seats
        removed_seats = old_seats - new_seats
        if added_seats:
            lines.append("**Novos**: " + ", ".join(f"[[{s}]]" for s in sorted(added_seats)))
        if removed_seats:
            lines.append("**Removidos**: " + ", ".join(f"[[{s}]]" for s in sorted(removed_seats)))
        lines.append("")

    # Research depth
    lines.append("## Profundidade de research")
    lines.append("")
    lines.append(f"- Hits anterior: {prior.research_hits_total}  ·  Hits actual: {current.research_hits_total}  ·  Δ: {current.research_hits_total - prior.research_hits_total:+d}")
    lines.append(f"- Evidence ledger: {prior.evidence_count} → {current.evidence_count} ({current.evidence_count - prior.evidence_count:+d} entries)")
    lines.append("")

    lines.append("---")
    lines.append("*Delta gerado automaticamente. Ler com o storytelling actual lado a lado para contexto.*")
    return "\n".join(lines)


def emit_delta_if_prior(
    current: DossierSnapshot,
    *,
    run_date: date | None = None,
) -> Path | None:
    run_date = run_date or date.fromisoformat(current.date)
    prior = find_prior_snapshot(current.ticker, exclude_date=run_date)
    if prior is None:
        return None
    delta_md = render_delta_md(prior, current)
    DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DOSSIERS_DIR / f"{current.ticker}_DELTA_{run_date.isoformat()}.md"
    out_path.write_text(delta_md, encoding="utf-8")
    return out_path
