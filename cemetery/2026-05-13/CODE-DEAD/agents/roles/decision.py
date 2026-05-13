"""Decision role — resolve N perspectives into one actionable verdict.

Input contract:
    {
        "subject": str,                 # e.g. "VALE3 buy decision"
        "perspectives": [               # list of analyst views
            {"name": "...", "stance": "...", "argument": "..."}, ...
        ],
        "constraints": str (optional),  # hard constraints (budget, mandate, etc.)
        "options": [str, ...] (optional)# allowed verdicts; default BUY/HOLD/SELL/AVOID
    }

Output contract:
    {
        "verdict": str,                 # one of options
        "confidence": 0.0-1.0,
        "reasoning": str,               # 2-4 sentences
        "drivers": [                    # which perspectives drove the call
            {"name": str, "weight": 0.0-1.0, "why": str}
        ]
    }

Modelo: qwen2.5:32b — reasoning é mais robusto.
"""
from __future__ import annotations

import json
from typing import Any

from agents._llm import extract_json

DEFAULT_OPTIONS = ["BUY", "HOLD", "SELL", "AVOID"]


def render_prompt(input: dict[str, Any]) -> str:
    subject = input["subject"]
    perspectives = input["perspectives"]
    constraints = input.get("constraints", "")
    options = input.get("options") or DEFAULT_OPTIONS
    persp_str = json.dumps(perspectives, indent=2, ensure_ascii=False, default=str)
    cons_block = f"\nHard constraints: {constraints}\n" if constraints else ""
    opts_str = " | ".join(options)
    return (
        f"Subject: {subject}\n\n"
        f"Perspectives from {len(perspectives)} analysts:\n{persp_str}\n"
        f"{cons_block}\n"
        f"Allowed verdicts: [{opts_str}]\n\n"
        "Synthesize the perspectives. Be DECISIVE — pick one verdict.\n"
        "Identify which perspectives drove your call (and why).\n"
        "Output STRICT JSON: "
        '{"verdict": "<one of allowed>", "confidence": 0.0-1.0, '
        '"reasoning": "...", '
        '"drivers": [{"name": "...", "weight": 0.0-1.0, "why": "..."}]}'
    )


def parse_output(raw: str, input: dict[str, Any]) -> dict | None:
    obj = extract_json(raw)
    if not isinstance(obj, dict):
        return None
    verdict = obj.get("verdict")
    options = input.get("options") or DEFAULT_OPTIONS
    if verdict not in options:
        return None
    try:
        confidence = float(obj.get("confidence", 0.0))
    except (TypeError, ValueError):
        return None
    if confidence < 0 or confidence > 1:
        return None
    reasoning = obj.get("reasoning", "")
    drivers = obj.get("drivers", [])
    if not isinstance(drivers, list):
        drivers = []
    return {
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": str(reasoning)[:1000],
        "drivers": drivers,
    }
