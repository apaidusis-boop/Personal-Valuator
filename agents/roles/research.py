"""Research role — gather facts from RAG/DB context.

Input contract:
    {
        "question": str,            # what to research
        "context": str | list[str], # passages already retrieved
        "fields": [str, ...]        # facts to populate (optional)
    }

Output contract:
    {
        "facts": [{"claim": str, "source": str, "confidence": 0.0-1.0}, ...],
        "open_questions": [str, ...],
        "context_quality": "high" | "medium" | "low" | "insufficient"
    }
"""
from __future__ import annotations

from typing import Any

from agents._llm import extract_json


def render_prompt(input: dict[str, Any]) -> str:
    question = input["question"]
    ctx = input.get("context", "")
    if isinstance(ctx, list):
        ctx = "\n\n".join(f"[chunk {i+1}]\n{c}" for i, c in enumerate(ctx))
    fields = input.get("fields") or []
    field_block = (
        "\nSpecifically populate these fields if present in the context:\n"
        + "\n".join(f"  - {f}" for f in fields)
        if fields else ""
    )
    return (
        f"Research question: {question}\n\n"
        f"Available context:\n---\n{ctx}\n---\n"
        f"{field_block}\n\n"
        "Extract FACTS ONLY (no opinions, no extrapolation). "
        "For each fact: cite the source chunk and assign a confidence 0-1. "
        "List open_questions where the context didn't answer.\n\n"
        "Output STRICT JSON:\n"
        '{"facts": [{"claim": "...", "source": "chunk N or url", "confidence": 0.0-1.0}], '
        '"open_questions": [...], "context_quality": "high|medium|low|insufficient"}'
    )


def parse_output(raw: str, input: dict[str, Any]) -> dict | None:
    obj = extract_json(raw)
    if not isinstance(obj, dict):
        return None
    facts = obj.get("facts")
    if not isinstance(facts, list):
        return None
    quality = obj.get("context_quality")
    if quality not in ("high", "medium", "low", "insufficient", None):
        return None
    return {
        "facts": facts,
        "open_questions": obj.get("open_questions", []) or [],
        "context_quality": quality or "medium",
    }
