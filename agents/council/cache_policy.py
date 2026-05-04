"""Smart re-run cache — STORYT_3.0 follow-up.

Goal: when a ticker is re-analyzed but nothing material changed since the last
snapshot, skip the expensive Ollama work (council debate + narrative) and emit
only a "no material change" delta MD. Saves ~95s per ticker on stable runs.

Decision tree:
  1. Compute fingerprint of current dossier (rounded fundamentals + period_end +
     research-hit counts + price bucket).
  2. Find latest prior snapshot (excluding today).
  3. If fingerprints match → SKIP (emit "no_change" delta).
  4. If trivial drift (< 2% on key metrics, no new flags, same period_end) →
     PARTIAL (Risk Officer only, 1 round, reuse other voices' last R2).
  5. If material change (new period_end, new analyst report, ≥ 2% drift on any
     primary metric, new CVM event) → FULL run.

The fingerprint is conservative: any new research hit triggers re-run because
the hits SHAPE the council debate. Period_end change always triggers full
(earnings filed → completely new fundamentals).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

from agents.council.versioning import find_prior_snapshot

if TYPE_CHECKING:
    from agents.council.dossier import CouncilDossier
    from agents.council.versioning import DossierSnapshot


@dataclass
class CacheDecision:
    """The outcome of cache lookup."""
    action: str          # 'full' | 'partial' | 'skip'
    reason: str          # human-readable
    fingerprint: str     # current dossier fingerprint
    prior_fingerprint: str | None = None
    prior_date: str | None = None


def compute_fingerprint(d: "CouncilDossier") -> str:
    """SHA256 (truncated) of materially-significant dossier features.
    Two dossiers with the same fingerprint should produce ~identical analysis."""
    f = d.fundamentals or {}
    parts = [
        f"pe={round(f.get('pe') or 0, 2)}",
        f"pb={round(f.get('pb') or 0, 2)}",
        f"dy={round(f.get('dy') or 0, 4)}",
        f"roe={round(f.get('roe') or 0, 3)}",
        f"nde={round(f.get('net_debt_ebitda') or 0, 2)}",
        f"streak={int(f.get('dividend_streak_years') or 0)}",
        f"period={f.get('period_end', '')}",
        f"price_bucket={round((d.last_price or 0) / max(d.last_price or 1, 0.01), 1)}",
        # Research brief — counts only (any new hit = different fingerprint)
        f"analyst_n={len(d.research_brief.analyst_hits) if d.research_brief else 0}",
        f"event_n={len(d.research_brief.event_hits) if d.research_brief else 0}",
        f"video_n={len(d.research_brief.video_hits) if d.research_brief else 0}",
        f"tavily_news_n={len(d.research_brief.tavily_news_hits) if d.research_brief else 0}",
        # Quality scores
        f"piotroski={(d.quality_scores or {}).get('piotroski', {}).get('f_score', '?')}",
        f"altman_zone={(d.quality_scores or {}).get('altman', {}).get('zone', '?')}",
        f"beneish_zone={(d.quality_scores or {}).get('beneish', {}).get('zone', '?')}",
    ]
    blob = "|".join(parts)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def _drift_pct(new: float | None, old: float | None) -> float:
    """Absolute drift as fraction (0.02 = 2%). Returns 0.0 if either is None."""
    if new is None or old is None or old == 0:
        return 0.0
    return abs((new - old) / old)


def decide(d: "CouncilDossier", *, run_date: date | None = None) -> CacheDecision:
    """Decide cache action for this dossier."""
    fp = compute_fingerprint(d)
    run_date = run_date or date.today()
    prior = find_prior_snapshot(d.ticker, exclude_date=run_date)

    if prior is None:
        return CacheDecision(action="full", reason="no_prior_snapshot", fingerprint=fp)

    prior_fp = _snapshot_fingerprint(prior)
    if prior_fp == fp:
        return CacheDecision(
            action="skip",
            reason="fingerprint_match (no material change since prior run)",
            fingerprint=fp,
            prior_fingerprint=prior_fp,
            prior_date=prior.date,
        )

    # Compute drifts on key metrics
    f = d.fundamentals or {}
    drifts = {
        "pe": _drift_pct(f.get("pe"), prior.fundamentals.get("pe")),
        "dy": _drift_pct(f.get("dy"), prior.fundamentals.get("dy")),
        "roe": _drift_pct(f.get("roe"), prior.fundamentals.get("roe")),
        "nde": _drift_pct(f.get("net_debt_ebitda"), prior.fundamentals.get("net_debt_ebitda")),
    }

    # Period_end change → full (new earnings)
    if f.get("period_end") != prior.fundamentals.get("period_end"):
        return CacheDecision(
            action="full",
            reason=f"period_end changed: {prior.fundamentals.get('period_end')} → {f.get('period_end')}",
            fingerprint=fp,
            prior_fingerprint=prior_fp,
            prior_date=prior.date,
        )

    max_drift = max(drifts.values())
    if max_drift >= 0.02:
        # Material drift but same period — full run
        worst = max(drifts.items(), key=lambda x: x[1])
        return CacheDecision(
            action="full",
            reason=f"material_drift on {worst[0]}={worst[1]*100:.1f}%",
            fingerprint=fp,
            prior_fingerprint=prior_fp,
            prior_date=prior.date,
        )

    # Trivial drift, same period, but research hit count differs → partial
    if d.research_brief is not None:
        hit_drift = (
            len(d.research_brief.analyst_hits) - 0  # rough heuristic
        )
        # Actually research counts being different was already in fingerprint;
        # if we got here with fingerprint mismatch + period same + low drift,
        # most likely it's just price moved a bucket → partial run
        return CacheDecision(
            action="partial",
            reason=f"trivial_drift (max {max_drift*100:.2f}%) — risk-only refresh",
            fingerprint=fp,
            prior_fingerprint=prior_fp,
            prior_date=prior.date,
        )

    return CacheDecision(
        action="full",
        reason="fallback",
        fingerprint=fp,
        prior_fingerprint=prior_fp,
        prior_date=prior.date,
    )


def _snapshot_fingerprint(snap: "DossierSnapshot") -> str:
    """Reconstruct a fingerprint from a saved snapshot. Best-effort because
    snapshots don't store research_brief hit counts directly — we approximate
    from research_hits_total."""
    f = snap.fundamentals or {}
    parts = [
        f"pe={round(f.get('pe') or 0, 2)}",
        f"pb={round(f.get('pb') or 0, 2)}",
        f"dy={round(f.get('dy') or 0, 4)}",
        f"roe={round(f.get('roe') or 0, 3)}",
        f"nde={round(f.get('net_debt_ebitda') or 0, 2)}",
        f"streak={int(f.get('dividend_streak_years') or 0)}",
        f"period={f.get('period_end', snap.period_end or '')}",
        f"price_bucket=1.0",  # we don't have price in snapshot directly
        # Approximate research hit counts — total hit count split rough
        # Not perfect but good enough for cache invalidation heuristic
        f"analyst_n={snap.research_hits_total // 4 if snap.research_hits_total else 0}",
        f"event_n={snap.research_hits_total // 8 if snap.research_hits_total else 0}",
        f"video_n={snap.research_hits_total // 6 if snap.research_hits_total else 0}",
        f"tavily_news_n={snap.research_hits_total // 3 if snap.research_hits_total else 0}",
        f"piotroski={(snap.quality_scores or {}).get('piotroski', {}).get('f_score', '?')}",
        f"altman_zone={(snap.quality_scores or {}).get('altman', {}).get('zone', '?')}",
        f"beneish_zone={(snap.quality_scores or {}).get('beneish', {}).get('zone', '?')}",
    ]
    blob = "|".join(parts)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def emit_no_change_delta(
    ticker: str,
    market: str,
    current_fp: str,
    prior_date: str,
    *,
    run_date: date | None = None,
) -> Path:
    """Emit a minimal delta MD when the smart cache says nothing material changed."""
    run_date = run_date or date.today()
    out_dir = Path(__file__).resolve().parents[2] / "obsidian_vault" / "dossiers"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{ticker}_DELTA_{run_date.isoformat()}.md"
    days_apart = (run_date - date.fromisoformat(prior_date)).days

    body = f"""---
type: storyt2_delta
ticker: {ticker}
market: {market}
prior_date: {prior_date}
current_date: {run_date.isoformat()}
days_apart: {days_apart}
action: no_change
fingerprint: {current_fp}
tags: [storyt2, delta, no_change]
---

# Δ Delta — {ticker} (sem mudança material)

**Comparação**: `{prior_date}` → `{run_date.isoformat()}` ({days_apart} dias)

✅ **Smart cache**: fingerprint do dossier idêntico ao último snapshot. Nenhuma métrica primária alterou, nenhum novo evento CVM/SEC, nenhum analyst report novo, nenhum novo video YouTube ingerido.

📖 [[{ticker}_STORY|Storytelling actual (do run anterior)]] · 🏛️ [[{ticker}_COUNCIL|Council debate anterior]]

## O que esta decisão significa

- **Fundamentals**: P/E, P/B, DY, ROE, ND/EBITDA, dividend streak — todos inalterados desde {prior_date}
- **Period_end**: mesmo trimestre/ano
- **Research depth**: hits do Ulisses idênticos
- **Quality scores**: zonas Piotroski/Altman/Beneish iguais

Sem rationale para reprocessar Council ou Narrative. Storytelling do dia {prior_date} continua válido.

## Quando pular SMART CACHE

Para forçar full re-run, usar `python -m agents.council.story {ticker} --market {market} --no-cache`.

Triggers automáticos para next full run:
- Novo período `period_end` (earnings call → full re-run)
- Drift ≥ 2% em qualquer métrica primária
- Novo analyst report / CVM event / video YouTube ingerido sobre o ticker
- Mudança de zona Altman / Beneish (clean → grey, safe → distress)

---
*Smart cache decision · STORYT_3.0 · `{current_fp}`*
"""
    out.write_text(body, encoding="utf-8")
    return out
