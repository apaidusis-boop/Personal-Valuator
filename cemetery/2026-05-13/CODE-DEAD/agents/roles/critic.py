"""Critic role — audit another agent's output for issues.

Input contract:
    {
        "output_to_review": str | dict,  # text/JSON to audit
        "context": str (optional),       # ground truth / source data
        "criteria": [str, ...] (optional) # what to check; defaults to standard list
    }

Output contract:
    {
        "issues": [{"severity": "high|medium|low",
                    "category": "factual|logical|context|overconfidence|other",
                    "description": str,
                    "suggested_fix": str (optional)}],
        "overall": "pass" | "concerns" | "reject"
    }

Default criteria: factual_accuracy, logical_soundness, missing_context,
overconfidence.
"""
from __future__ import annotations

import json
from typing import Any

from agents._llm import extract_json

DEFAULT_CRITERIA = [
    "factual_accuracy: every claim must trace to evidence",
    "logical_soundness: conclusions must follow from premises",
    "missing_context: important caveats not omitted",
    "overconfidence: numerical certainty without source is a red flag",
]


def render_prompt(input: dict[str, Any]) -> str:
    out = input["output_to_review"]
    if not isinstance(out, str):
        out = json.dumps(out, indent=2, ensure_ascii=False, default=str)
    context = input.get("context", "")
    criteria = input.get("criteria") or DEFAULT_CRITERIA
    crit_str = "\n".join(f"  - {c}" for c in criteria)
    ctx_block = f"\nContext / ground truth:\n---\n{context}\n---\n" if context else ""
    return (
        f"Output to review:\n---\n{out}\n---\n"
        f"{ctx_block}\n"
        f"Audit the output against:\n{crit_str}\n\n"
        "Be brutal. If the output passes, return issues=[].\n"
        "Output STRICT JSON: "
        '{"issues": [{"severity": "high|medium|low", '
        '"category": "factual|logical|context|overconfidence|other", '
        '"description": "...", "suggested_fix": "..."}], '
        '"overall": "pass|concerns|reject"}'
    )


def parse_output(raw: str, input: dict[str, Any]) -> dict | None:
    obj = extract_json(raw)
    if not isinstance(obj, dict):
        return None
    issues = obj.get("issues")
    overall = obj.get("overall")
    if not isinstance(issues, list):
        return None
    if overall not in ("pass", "concerns", "reject", None):
        return None
    return {
        "issues": issues,
        "overall": overall or ("pass" if not issues else "concerns"),
    }
