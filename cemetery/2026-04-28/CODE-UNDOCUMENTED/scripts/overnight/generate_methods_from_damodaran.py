"""Overnight job 1: Generate 10 new YAML methods from top Damodaran extracted methods.

Input:  library/insights/investment_valuation_3rd_edition.json (910 methods)
Output: library/methods/damodaran_auto_*.yaml (10 new)

Strategy:
  - Filter methods with non-empty rules_or_formula
  - Score them by "actionability" (has numbers, formulas, ratios)
  - Pick top 10 distinct
  - For each: prompt Ollama to convert into our YAML rule format
  - Save to library/methods/damodaran_auto_<slug>.yaml

Zero Claude tokens. Qwen 14B local.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
INSIGHTS = ROOT / "library" / "insights" / "investment_valuation_3rd_edition.json"
METHODS_DIR = ROOT / "library" / "methods"
LOG = ROOT / "data" / "overnight" / "methods_generation.log"

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:14b-instruct-q4_K_M"

CONVERT_PROMPT = """Convert an investment method into an executable YAML rule for a screening system.

AVAILABLE VARIABLES (all stored as decimals: 0.08 = 8%):
  pe, pb, dy, roe, eps, bvps, net_debt_ebitda, lpa, vpa
  shares_outstanding, market_cap_usd, current_ratio, ltd, working_capital
  beta_levered, peg_ratio, price

INPUT METHOD:
  name: {name}
  description: {description}
  formula: {formula}

OUTPUT: ONLY pure YAML (no markdown fence), matching this template:

id: damodaran_auto_<short_slug>
name: "<same name>"
book: Investment Valuation 3rd ed (Damodaran)
horizon: long
direction: LONG
derived_from: ollama_auto_2026-04-24
rules:
  - id: <rule_id>
    description: "<what it checks>"
    check: "<python-like expression using vars above>"
  # 2-4 rules total; use AND/OR/comparison operators only
caveats:
  - "<1 honest limitation>"

CRITICAL:
- id slug lowercase, no spaces, use underscores
- check expressions MUST use decimal scale (dy<0.06, roe>=0.15)
- NEVER invent variables not in the list
- if a method can't be expressed in rules, return: {{"skip": "reason"}}
"""


def load_top_methods(n: int = 25) -> list[dict]:
    d = json.loads(INSIGHTS.read_text(encoding="utf-8"))
    methods = d["methods_unique"]
    # Score by "actionability"
    scored = []
    for m in methods:
        name = m.get("name", "").strip()
        formula = (m.get("rules_or_formula", "") or "").strip()
        desc = (m.get("description", "") or "").strip()
        if not formula or len(formula) < 25:
            continue
        # Skip overly academic concepts
        if any(x in name.lower() for x in ["survival bias", "january effect", "standard error", "data mining"]):
            continue
        # Prefer methods with numbers/operators in formula
        actionable = sum(1 for c in formula if c in "=+-*/<>()%") + len(re.findall(r"\d", formula))
        if actionable < 5:
            continue
        scored.append((actionable, m))
    scored.sort(key=lambda x: -x[0])
    return [m for _, m in scored[:n]]


def convert_method(m: dict) -> dict | None:
    prompt = (CONVERT_PROMPT
              .replace("{name}", m.get("name", "")[:120])
              .replace("{description}", (m.get("description", "") or "")[:240])
              .replace("{formula}", (m.get("rules_or_formula", "") or "")[:300]))
    try:
        r = requests.post(
            OLLAMA,
            json={"model": MODEL, "prompt": prompt, "stream": False,
                  "options": {"temperature": 0.2, "num_predict": 600}},
            timeout=120,
        )
        r.raise_for_status()
        raw = r.json().get("response", "").strip()
        # Strip markdown fence if present
        raw = re.sub(r"^```(?:yaml)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        return yaml.safe_load(raw)
    except Exception as e:
        return {"_error": str(e)}


def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9_]", "", re.sub(r"\s+", "_", s.lower()))[:40]


def main(target: int = 10) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log_lines = [f"=== Methods generation from Damodaran — 2026-04-24 overnight ===\n"]

    candidates = load_top_methods(n=25)
    log_lines.append(f"Candidates (top actionable): {len(candidates)}\n")

    generated = 0
    existing_ids = {p.stem for p in METHODS_DIR.glob("*.yaml")}

    for cand in candidates:
        if generated >= target:
            break
        name = cand.get("name", "unknown")
        log_lines.append(f"\n--- Processing: {name[:80]}")
        result = convert_method(cand)
        if not result or "_error" in result or "skip" in result:
            log_lines.append(f"  skipped: {result}")
            continue
        method_id = result.get("id") or f"damodaran_auto_{_slugify(name)}"
        if method_id in existing_ids:
            log_lines.append(f"  skipped: id exists ({method_id})")
            continue
        if "rules" not in result or not result["rules"]:
            log_lines.append(f"  skipped: no rules")
            continue
        # Save YAML
        out_path = METHODS_DIR / f"{method_id}.yaml"
        try:
            # Ensure proper YAML header
            yaml_text = "---\n" + yaml.dump(result, sort_keys=False, allow_unicode=True, default_flow_style=False)
            out_path.write_text(yaml_text, encoding="utf-8")
            log_lines.append(f"  OK -> {out_path.name}  ({len(result['rules'])} rules)")
            generated += 1
            existing_ids.add(method_id)
        except Exception as e:
            log_lines.append(f"  save error: {e}")

    log_lines.append(f"\n=== Done. Generated {generated} new methods.\n")
    LOG.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"Generated {generated} methods. Log: {LOG}")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    main(target=n)
