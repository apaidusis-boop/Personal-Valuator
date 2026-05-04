"""Extraction role — text/document → structured JSON fields.

Input contract:
    {
        "text": str,                    # source text
        "fields": {                     # field name → field description
            "revenue": "annual revenue in USD millions",
            "ceo": "name of CEO",
            ...
        },
        "context": str (optional),
    }

Output contract:
    {
        "<field_name>": <value or null>,
        ...
    }
    + "_extraction_notes": str (optional, brief)

Determinism: temperature=0.0. Empty extraction is OK; invention is not.
"""
from __future__ import annotations

from typing import Any

from agents._llm import extract_json


def render_prompt(input: dict[str, Any]) -> str:
    text = input["text"]
    fields = input["fields"]
    context = input.get("context", "")
    field_desc = "\n".join(f"  - {k}: {v}" for k, v in fields.items())
    ctx_block = f"\nContext: {context}\n" if context else ""
    return (
        f"Source text:\n---\n{text}\n---\n"
        f"{ctx_block}\n"
        f"Extract these fields:\n{field_desc}\n\n"
        "Output STRICT JSON with the field names as keys. "
        "Use null when a field is not present in the source. "
        "Do NOT invent values."
    )


def parse_output(raw: str, input: dict[str, Any]) -> dict | None:
    obj = extract_json(raw)
    if not isinstance(obj, dict):
        return None
    expected = set(input["fields"].keys())
    # Coerce missing fields to null; ignore extra keys (drop them).
    out = {k: obj.get(k) for k in expected}
    notes = obj.get("_extraction_notes") or obj.get("notes")
    if notes:
        out["_extraction_notes"] = str(notes)[:500]
    return out
