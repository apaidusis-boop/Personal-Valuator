"""Classification role — text → label from fixed enum.

Input contract:
    {
        "text": str,                # short text to classify
        "labels": [str, str, ...],  # allowed labels
        "context": str (optional),  # extra context
    }

Output contract:
    {
        "label": str | None,        # one of input.labels, or None if uncertain
        "confidence": float,        # 0.0-1.0
        "rationale": str (optional),
    }

Default model: qwen2.5:3b-instruct-q4_K_M (10× faster than 14B for this task).
Fallback model: qwen2.5:14b-instruct-q4_K_M (set in agents_governance.yaml).
"""
from __future__ import annotations

import json
from typing import Any

from agents._llm import extract_json


def render_prompt(input: dict[str, Any]) -> str:
    text = input["text"]
    labels = input["labels"]
    context = input.get("context", "")
    labels_str = " | ".join(f'"{lbl}"' for lbl in labels)
    ctx_block = f"\n\nContext: {context}" if context else ""
    return (
        f"Text to classify: {text!r}\n"
        f"Allowed labels: [{labels_str}]"
        f"{ctx_block}\n\n"
        "Return STRICT JSON: {\"label\": \"<one of allowed or null>\", "
        "\"confidence\": 0.0-1.0, \"rationale\": \"<brief>\"}."
    )


def parse_output(raw: str, input: dict[str, Any]) -> dict | None:
    obj = extract_json(raw)
    if not isinstance(obj, dict):
        return None
    label = obj.get("label")
    confidence = obj.get("confidence")
    if label is not None and label not in input["labels"]:
        return None
    try:
        confidence_f = float(confidence) if confidence is not None else 0.0
    except (TypeError, ValueError):
        return None
    if confidence_f < 0 or confidence_f > 1:
        return None
    return {
        "label": label,
        "confidence": confidence_f,
        "rationale": obj.get("rationale", ""),
    }
