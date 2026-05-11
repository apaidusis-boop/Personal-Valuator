"""Method Discovery Perpetuum — autoresearch sobre nossos critérios de investimento.

Subjects: critérios codificados (CLAUDE.md thresholds, scoring rules).
Para cada um, mede "evidência staleness" — quando foi actualizado / validado
contra literatura recente.

Actions propostas (T2+ futuro):
  - "autoresearch_query: 'is DY >6% still valid with Selic 11%?'"
  - "autoresearch_query: 'Piotroski F-score updates 2024-2026'"
  - "refresh_threshold: ROE >=15% → test alternatives"

Scoring signals (determinístico por agora; autoresearch wires em X.3 deep):
  - last_validated_days (desde última nota de validation)
  - evidence_citations (links para papers/blogs na método's description)
  - backtest_age (se temos backtest, quando foi última run)
  - regime_covered (aplicou-se só em regime X ou múltiplos?)

Score 0-100. < 60 → propor autoresearch refresh.

Stub mode: quando GPT Researcher não instalado, gera as QUERIES que seriam
corridas e persiste. User pode manual-run via `python scripts/research.py`.
"""
from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject


METHODS_CATALOG = [
    {
        "id": "br_graham_threshold",
        "label": "BR non-bank: Graham Number + DY≥6% + ROE≥15% + NetDebt/EBITDA<3 + 5y streak",
        "source": "CLAUDE.md",
        "last_validated": "2026-01-15",
        "evidence_refs": [],
        "queries": [
            "Is dividend yield >=6% still appropriate threshold for Brazilian equities with Selic at 11.5%?",
            "Graham Number formula validity in emerging markets 2024-2026",
            "Alternative to ROE>=15% for capital-intensive Brazilian sectors",
        ],
    },
    {
        "id": "br_banks_threshold",
        "label": "BR banks: P/E≤10, P/B≤1.5, DY≥6%, ROE≥12%, 5y streak",
        "source": "CLAUDE.md",
        "last_validated": "2026-01-15",
        "evidence_refs": [],
        "queries": [
            "Brazilian bank valuation metrics — P/B thresholds 2025-2026",
            "ROE 12% vs 15% for Brazilian banks in Selic >11% regime",
        ],
    },
    {
        "id": "us_buffett_threshold",
        "label": "US: P/E≤20, P/B≤3, DY≥2.5%, ROE≥15%, aristocrat or 10y streak",
        "source": "CLAUDE.md",
        "last_validated": "2026-01-15",
        "evidence_refs": [],
        "queries": [
            "Buffett-style quality thresholds in 2025-2026 US market",
            "Dividend aristocrat outperformance 2020-2025 empirical evidence",
        ],
    },
    {
        "id": "drip_damper",
        "label": "DRIP projection damper (when hist CAGR >> Gordon equilibrium)",
        "source": "scripts/drip_projection.py",
        "last_validated": "2025-11-01",
        "evidence_refs": [],
        "queries": [
            "Realistic long-term dividend growth rate assumptions 2026",
            "Gordon growth model assumptions under high inflation regimes",
        ],
    },
    {
        "id": "piotroski_f",
        "label": "Piotroski F-score (veto F≤3)",
        "source": "scoring/piotroski.py",
        "last_validated": "2025-09-10",
        "evidence_refs": [],
        "queries": [
            "Piotroski F-score predictive power 2020-2025 academic",
            "F-score alternatives for cash-rich tech companies",
        ],
    },
    {
        "id": "altman_z",
        "label": "Altman Z-Score (distress, veto R5)",
        "source": "scoring/altman.py",
        "last_validated": "2025-09-10",
        "evidence_refs": [],
        "queries": [
            "Altman Z-Score industry-specific adjustments 2024",
            "Z-score applicability to asset-light business models",
        ],
    },
    {
        "id": "dividend_safety",
        "label": "Dividend Safety Score (forward-looking 0-100)",
        "source": "scoring/dividend_safety.py",
        "last_validated": "2025-11-01",
        "evidence_refs": [],
        "queries": [
            "Forward dividend safety scoring — best practices Simply Safe Dividends",
            "Payout ratio thresholds by sector 2024",
        ],
    },
    {
        "id": "regime_classifier",
        "label": "Rule-based regime classifier (expansion/late_cycle/recession/recovery)",
        "source": "analytics/regime.py",
        "last_validated": "2026-04-01",
        "evidence_refs": [],
        "queries": [
            "Dalio Big Debt Cycles 2024-2026 regime classification",
            "Yield curve inversion false positives 2022-2024",
        ],
    },
]


class MethodDiscoveryPerpetuum(BasePerpetuum):
    name = "method_discovery"
    description = "Avalia staleness dos métodos + propõe autoresearch queries"
    autonomy_tier = "T1"
    drop_alert_threshold = 20

    def subjects(self) -> list[PerpetuumSubject]:
        return [
            PerpetuumSubject(
                id=f"method:{m['id']}",
                label=m["label"],
                metadata=m,
            )
            for m in METHODS_CATALOG
        ]

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        m = subject.metadata
        flags: list[str] = []
        score = 100

        # Age of last validation
        try:
            last_v = datetime.fromisoformat(m["last_validated"])
            age = (datetime.now() - last_v).days
        except Exception:
            age = 9999
            flags.append("unknown last_validated date")

        if age > 365:
            score -= 40
            flags.append(f"stale {age}d (>1yr)")
        elif age > 180:
            score -= 25
            flags.append(f"stale {age}d (>6mo)")
        elif age > 90:
            score -= 10
            flags.append(f"aging {age}d (>3mo)")

        # Evidence citations
        if not m.get("evidence_refs"):
            score -= 25
            flags.append("no citation links in method definition")

        # Backtest coverage check (placeholder)
        has_backtest = m["id"] in {"br_graham_threshold", "us_buffett_threshold", "regime_classifier"}
        if not has_backtest:
            score -= 15
            flags.append("no backtest on file")

        score = max(0, min(100, score))

        # Build action hint with concrete queries (stub for GPT Researcher)
        action_hint = None
        if score < 70:
            q = m.get("queries", [])[:2]
            if q:
                qstr = " | ".join(q)
                action_hint = f"autoresearch: {qstr}"[:300]

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(flags),
            flags=flags,
            details={
                "label": m["label"],
                "source": m["source"],
                "last_validated": m["last_validated"],
                "age_days": age,
                "queries_to_run": m.get("queries", []),
                "evidence_refs_count": len(m.get("evidence_refs", [])),
            },
            action_hint=action_hint,
        )
