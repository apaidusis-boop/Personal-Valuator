"""Pydantic schemas for LLM-structured outputs across agents.

Phase W.6 — Sprint 1: structured outputs.

Pattern: every agent that previously did `json.loads(raw_llm_text)` should now
return one of these Pydantic models via `agents._llm.ollama_call_typed`.
Validation moves from "hope the LLM gave good JSON" to compile-time enforced
shape.

These schemas are deliberately permissive (Field defaults, str fallbacks for
list-shaped fields, no Field(max_length=) on free text) so a slightly malformed
LLM response still parses — strictness is in the literal-typed enum fields and
conviction range.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, conint, field_validator


# ──────────────────────────────────────────────────────────────────────
# synthetic_ic.py — single-persona verdict
# ──────────────────────────────────────────────────────────────────────

Verdict = Literal["BUY", "HOLD", "AVOID"]
Sizing = Literal["small", "medium", "large", "none"]


class PersonaVerdict(BaseModel):
    """Single Investment Committee persona verdict on a ticker.

    Mirrors the JSON shape the prompt asks Qwen 14B for in
    `agents/synthetic_ic.py::ask_persona`.
    """

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    verdict: Verdict
    conviction: conint(ge=1, le=10) = Field(default=5)
    rationale: list[str] = Field(default_factory=list)
    key_risk: str = ""
    would_size: Sizing = "none"

    @field_validator("verdict", mode="before")
    @classmethod
    def _upper_verdict(cls, v):
        if isinstance(v, str):
            return v.strip().upper()
        return v

    @field_validator("would_size", mode="before")
    @classmethod
    def _lower_size(cls, v):
        # Tolerate verbose outputs like "medium — proporção típica do meu book"
        # by extracting the first sizing token.
        if isinstance(v, str):
            s = v.strip().lower()
            for kw in ("small", "medium", "large", "none"):
                if kw in s:
                    return kw
            return s
        return v

    @field_validator("rationale", mode="before")
    @classmethod
    def _coerce_rationale(cls, v):
        # Tolerate single-string responses from chatty models.
        if isinstance(v, str):
            return [v]
        return v


# ──────────────────────────────────────────────────────────────────────
# thesis_synthesizer.py — Buffett/Graham thesis output
# ──────────────────────────────────────────────────────────────────────


class ThesisDraft(BaseModel):
    """Structured thesis written by `agents/thesis_synthesizer.py`."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    core_thesis: str = ""
    key_assumptions: list[str] = Field(default_factory=list)
    disconfirmation_triggers: list[str] = Field(default_factory=list)
    intent: str = ""

    @field_validator("key_assumptions", "disconfirmation_triggers", mode="before")
    @classmethod
    def _coerce_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v or []


# ──────────────────────────────────────────────────────────────────────
# holding_wiki_synthesizer.py — wiki holdings stub
# ──────────────────────────────────────────────────────────────────────


class HoldingWikiStub(BaseModel):
    """Wiki holdings stub — output of `agents/holding_wiki_synthesizer.py`."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    intent_one_liner: str = ""
    business_snapshot: str = ""
    why_we_hold: list[str] = Field(default_factory=list)
    moat: str = ""
    current_state: str = ""
    invalidation_triggers: list[str] = Field(default_factory=list)
    sizing_drip_intent: str = ""

    @field_validator(
        "why_we_hold", "invalidation_triggers", mode="before"
    )
    @classmethod
    def _coerce_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v or []


# ──────────────────────────────────────────────────────────────────────
# council/ — STORYT_2.0 pre-publication debate (Modo A-BR prototype)
# ──────────────────────────────────────────────────────────────────────

CouncilStance = Literal["BUY", "HOLD", "AVOID", "NEEDS_DATA"]


class CouncilOpening(BaseModel):
    """Round 1 — each council member's opening statement, blind to peers."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    headline: str = ""
    stance: CouncilStance = "HOLD"
    main_argument: str = ""
    supporting_metrics: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    veto_signals: list[str] = Field(default_factory=list)

    @field_validator("stance", mode="before")
    @classmethod
    def _upper(cls, v):
        if isinstance(v, str):
            return v.strip().upper()
        return v

    @field_validator("supporting_metrics", "concerns", "veto_signals", mode="before")
    @classmethod
    def _coerce_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v or []


class CouncilResponse(BaseModel):
    """Round 2 — each council member responds to peers' Round 1 statements."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    agree_with: list[str] = Field(default_factory=list)
    challenge: list[str] = Field(default_factory=list)
    new_evidence: str = ""
    revised_stance: CouncilStance = "HOLD"

    @field_validator("revised_stance", mode="before")
    @classmethod
    def _upper(cls, v):
        if isinstance(v, str):
            return v.strip().upper()
        return v

    @field_validator("agree_with", "challenge", mode="before")
    @classmethod
    def _coerce_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v or []


class CouncilSynthesis(BaseModel):
    """Coordinator output — preserves dissent, surfaces pre-publication flags."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    consensus_points: list[str] = Field(default_factory=list)
    dissent_points: list[str] = Field(default_factory=list)
    final_stance: CouncilStance = "HOLD"
    confidence: Literal["high", "medium", "low"] = "low"
    pre_publication_flags: list[str] = Field(default_factory=list)
    sizing_recommendation: str = ""

    @field_validator("final_stance", mode="before")
    @classmethod
    def _upper(cls, v):
        if isinstance(v, str):
            return v.strip().upper()
        return v

    @field_validator("confidence", mode="before")
    @classmethod
    def _lower(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator(
        "consensus_points", "dissent_points", "pre_publication_flags", mode="before"
    )
    @classmethod
    def _coerce_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v or []
