"""Foundation — StrategyOutput dataclass + StrategyEngine Protocol.

Each strategy engine evaluates a ticker (or universe) and emits a uniform
StrategyOutput. PortfolioEngine then combines outputs across engines into
an AllocationProposal.

Conventions:
- score is 0.0-1.0 (NOT 0-100). Engines normalize internally.
- verdict is one of: BUY / HOLD / AVOID / N/A. Encoded as Verdict literal.
- weight_suggestion is a fraction (0.0-1.0) of the engine's notional bucket.
  Portfolio engine multiplies by the engine's bucket weight.
- rationale is engine-specific dict; same shape as scoring details_json.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Literal, Protocol, runtime_checkable

Verdict = Literal["BUY", "HOLD", "AVOID", "N/A"]
"""3-state decision + 'no opinion' fallback."""


@dataclass
class StrategyOutput:
    """Per-(ticker, engine) result. Same shape across all engines."""
    ticker: str
    market: str                  # 'br' | 'us'
    engine: str                  # 'graham' | 'buffett' | 'drip' | 'macro' | 'hedge'
    score: float                 # 0.0-1.0
    verdict: Verdict
    weight_suggestion: float = 0.0  # 0.0-1.0; engine's vote within its bucket
    rationale: dict[str, Any] = field(default_factory=dict)
    rank: int | None = None      # rank within universe if applicable
    message: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AllocationProposal:
    """Portfolio Engine output: combined ranking + weights across engines."""
    target_weights: dict[str, float]   # ticker -> 0.0-1.0
    per_engine: dict[str, list[StrategyOutput]]  # engine -> ranked list
    bucket_weights: dict[str, float]   # engine -> bucket fraction
    conflicts: list[dict[str, Any]] = field(default_factory=list)
    macro_overlay: dict[str, Any] = field(default_factory=dict)
    hedge_overlay: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "target_weights": self.target_weights,
            "per_engine": {
                k: [o.as_dict() for o in v] for k, v in self.per_engine.items()
            },
            "bucket_weights": self.bucket_weights,
            "conflicts": self.conflicts,
            "macro_overlay": self.macro_overlay,
            "hedge_overlay": self.hedge_overlay,
            "notes": self.notes,
        }


@runtime_checkable
class StrategyEngine(Protocol):
    """Contract every engine must satisfy."""
    name: str

    def evaluate(self, ticker: str, market: str = "br") -> StrategyOutput: ...

    def rank_universe(self, market: str = "br",
                      tickers: list[str] | None = None) -> list[StrategyOutput]: ...


# ============================================================
# Helpers — verdict from criteria pass count
# ============================================================
def verdict_from_pass_ratio(passes: int, applicable: int,
                            buy_threshold: float = 0.85,
                            hold_threshold: float = 0.60) -> Verdict:
    """Default mapping ratio → verdict. Engines override if needed.
    Applicable=0 ⇒ 'N/A'. Otherwise ratio = passes/applicable."""
    if applicable == 0:
        return "N/A"
    ratio = passes / applicable
    if ratio >= buy_threshold:
        return "BUY"
    if ratio >= hold_threshold:
        return "HOLD"
    return "AVOID"


def details_to_pass_count(details: dict) -> tuple[int, int]:
    """Extract (passes, applicable) from a `scoring.engine`-style details dict.
    Each criterion has a 'verdict' in {'pass', 'fail', 'n/a'}."""
    passes = 0
    applicable = 0
    for crit in details.values():
        if not isinstance(crit, dict):
            continue
        v = crit.get("verdict")
        if v == "pass":
            passes += 1
            applicable += 1
        elif v == "fail":
            applicable += 1
    return passes, applicable
