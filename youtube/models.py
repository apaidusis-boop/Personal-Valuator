"""Pydantic models for the YouTube ingestion pipeline.

`ExtractorOutput` é o JSON schema que o LLM local tem de devolver.
Validators garantem: evidence_quote ≤300 chars, confidence em [0,1],
kind/theme num vocabulário fechado.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

InsightKind = Literal[
    "guidance",
    "capex",
    "dividend",
    "balance_sheet",
    "thesis_bull",
    "thesis_bear",
    "catalyst",
    "risk",
    "operational",
    "management",
    "valuation",
]

Stance = Literal["bullish", "bearish", "neutral"]


class VideoMetadata(BaseModel):
    video_id: str
    url: str
    title: str | None = None
    channel: str | None = None
    channel_id: str | None = None
    published_at: str | None = None   # ISO 8601
    duration_sec: int | None = None


class TranscriptChunk(BaseModel):
    text: str
    ts_start: float   # seconds
    ts_end: float


class Insight(BaseModel):
    ticker: str
    kind: InsightKind
    claim: str = Field(..., max_length=500)
    evidence_quote: str = Field(..., max_length=400)
    ts_seconds: int | None = None
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, v: str) -> str:
        return v.strip().upper()


class Theme(BaseModel):
    theme: str = Field(..., max_length=64)
    stance: Stance | None = None
    summary: str = Field(..., max_length=500)
    evidence_quote: str = Field(..., max_length=400)
    ts_seconds: int | None = None
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("theme")
    @classmethod
    def norm_theme(cls, v: str) -> str:
        return v.strip().lower().replace(" ", "_")


class ExtractorOutput(BaseModel):
    """Schema que o LLM devolve. Pode estar vazio (nenhum facto confiável)."""

    insights: list[Insight] = Field(default_factory=list)
    themes: list[Theme] = Field(default_factory=list)
