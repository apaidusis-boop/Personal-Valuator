"""Synthesis role — facts + context → coherent narrative.

Input contract:
    {
        "facts": [str, ...] | dict,  # bullet list or structured dict
        "topic": str,                # subject (e.g. "VALE3 Q3 thesis")
        "audience": str (optional),  # e.g. "founder, technical-fluent PT"
        "length": "short" | "medium" | "long" (optional, default medium),
        "language": "pt" | "en" (optional, default pt)
    }

Output contract:
    Markdown text. NOT JSON (json_mode=False).
    Wrapped as {"narrative": "<markdown>"}.

Constraint: every claim must trace to a fact. If a fact is missing,
say so — never fabricate.
"""
from __future__ import annotations

import json
from typing import Any


def render_prompt(input: dict[str, Any]) -> str:
    facts = input["facts"]
    topic = input["topic"]
    audience = input.get("audience", "founder, technical-fluent PT")
    length = input.get("length", "medium")
    language = input.get("language", "pt")

    facts_str = json.dumps(facts, indent=2, ensure_ascii=False, default=str) \
        if not isinstance(facts, str) else facts
    length_hint = {
        "short": "1 short paragraph (~80 words)",
        "medium": "2-3 paragraphs (~250 words)",
        "long": "4-6 paragraphs (~600 words)",
    }.get(length, "2-3 paragraphs")
    return (
        f"Topic: {topic}\n"
        f"Audience: {audience}\n"
        f"Language: {language}\n"
        f"Length: {length_hint}\n\n"
        f"Facts to weave (cite all that matter):\n{facts_str}\n\n"
        "Write a coherent narrative. Use Markdown. "
        "Every claim must come from the facts above. "
        "If a logical gap exists, name it explicitly ('falta dado X'). "
        "No bullet lists unless absolutely necessary."
    )


def parse_output(raw: str, input: dict[str, Any]) -> dict | None:
    """Synthesis is free-form Markdown; we just verify non-empty."""
    if not raw or not raw.strip():
        return None
    return {"narrative": raw.strip()}
