"""strategies — multi-philosophy investment engines.

Each engine implements StrategyEngine Protocol and emits StrategyOutput.
A PortfolioEngine combines multiple engines into an AllocationProposal.

Usage:
    from strategies import graham, buffett, drip, macro, hedge, portfolio_engine

    g_out = graham.evaluate("PETR4", market="br")
    portfolio_engine.combine(["graham", "buffett", "drip", "macro", "hedge"])
"""
from strategies._base import (
    AllocationProposal,
    StrategyEngine,
    StrategyOutput,
    Verdict,
)

__all__ = ["AllocationProposal", "StrategyEngine", "StrategyOutput", "Verdict"]
