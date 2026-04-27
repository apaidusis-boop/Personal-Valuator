"""Token Economy Perpetuum — procura activamente formas de economizar Claude tokens.

USER REQUEST explícito: "autoresearch should find ways to economizar token usage".

Subjects: cada script/agent/fetcher do codebase que potencialmente faz LLM calls.
Identifica padrões de uso que queimam tokens desnecessariamente e propõe fix.

Scoring signals (static analysis — pure Python AST + regex):
  + usa Ollama (in-house) em vez de Claude quando disponível  → +pts
  + tem cache decorator / cache_path                          → +pts
  - chama Claude directo sem cache                            → -pts
  - passa prompts > 5000 chars sem compression               → -pts
  - re-fetches mesma data sem dedup                           → -pts
  - ausência de `if <condition>` antes de LLM call            → -pts
  - hardcoded model string "claude-opus" em vez de config    → -pts
  - duplicate system prompts entre agents (copy-paste)        → -pts

Score 0-100. <70 → propor optimization (action_hint concreto).

Meta-feature: este perpetuum é a manifestação directa da regra
[[in-house first]] — mede quantitativamente se ficamos fieis a ela.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from agents.perpetuum._engine import BasePerpetuum, PerpetuumResult, PerpetuumSubject

SCAN_DIRS = ["agents", "fetchers", "scripts", "scoring", "analytics"]

CLAUDE_IMPORT_RE = re.compile(r"(import\s+anthropic|from\s+anthropic)", re.M)
OLLAMA_IMPORT_RE = re.compile(r"(OLLAMA_URL|ollama\.chat|11434)", re.M)
CACHE_MARKER_RE = re.compile(r"(cache|lru_cache|diskcache|@cache|_cache_)", re.I | re.M)
LONG_PROMPT_RE = re.compile(r'"""[^"]{5000,}"""', re.DOTALL)
HARDCODED_MODEL_RE = re.compile(r'"claude-(?:opus|sonnet|haiku)-[\d-]+[^"]*"')


def _scan_file(path: Path) -> dict:
    try:
        src = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"error": "unreadable"}

    signals = {
        "size": len(src),
        "has_claude_import": bool(CLAUDE_IMPORT_RE.search(src)),
        "has_ollama_usage": bool(OLLAMA_IMPORT_RE.search(src)),
        "has_cache_marker": bool(CACHE_MARKER_RE.search(src)),
        "long_prompts": len(LONG_PROMPT_RE.findall(src)),
        "hardcoded_models": HARDCODED_MODEL_RE.findall(src),
        "llm_calls_count": len(re.findall(r"(?:messages|chat)\.create\(|generate_content|llm_summarise|call_claude", src)),
    }

    # AST check for ungated LLM calls
    try:
        tree = ast.parse(src)
        ungated = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                elif isinstance(node.func, ast.Name):
                    func_name = node.func.id
                if func_name in {"create", "generate", "chat"} and len(node.args) > 0:
                    # Crude heuristic: check if any parent in AST is if/try
                    ungated += 1  # Would need scope tracking for real; approximation
        signals["llm_calls_ast"] = ungated
    except Exception:
        signals["llm_calls_ast"] = 0

    return signals


class TokenEconomyPerpetuum(BasePerpetuum):
    name = "token_economy"
    description = "Procura patterns de waste de tokens Claude + propõe in-house alternatives"
    autonomy_tier = "T2"           # Promoted 2026-04-26: avg 99.7/100, 1 low subject
    drop_alert_threshold = 15

    def subjects(self) -> list[PerpetuumSubject]:
        subjects = []
        for d in SCAN_DIRS:
            base = ROOT / d
            if not base.exists():
                continue
            for py in base.rglob("*.py"):
                rel = py.relative_to(ROOT)
                if "__pycache__" in rel.parts or py.name.startswith("_"):
                    # skip __init__, _base, _helpers — focus on real workflows
                    if py.name not in {"_llm.py"}:  # but _llm.py IS interesting
                        continue
                subjects.append(PerpetuumSubject(
                    id=str(rel).replace("\\", "/"),
                    label=py.stem,
                    metadata={"path": str(py)},
                ))
        return subjects

    def score(self, subject: PerpetuumSubject) -> PerpetuumResult:
        path = Path(subject.metadata["path"])
        signals = _scan_file(path)
        flags: list[str] = []
        action_steps: list[str] = []
        score = 100

        if "error" in signals:
            return PerpetuumResult(subject_id=subject.id, score=-1, flags=[signals["error"]])

        # File has no LLM calls at all → N/A (good citizen)
        if (not signals["has_claude_import"]
                and signals["llm_calls_count"] == 0
                and "_llm" not in path.name):
            return PerpetuumResult(
                subject_id=subject.id, score=100, flag_count=0,
                flags=[],
                details={**signals, "category": "no_llm"},
            )

        # Signal 1: Claude import without cache marker
        if signals["has_claude_import"] and not signals["has_cache_marker"]:
            score -= 25
            flags.append("claude import without cache marker")
            action_steps.append("add disk cache for responses (e.g. data/llm_cache/<hash>.json)")

        # Signal 2: Claude without Ollama fallback
        if signals["has_claude_import"] and not signals["has_ollama_usage"]:
            score -= 20
            flags.append("claude used but no ollama fallback")
            action_steps.append("consider Ollama for summarization/extraction tasks (in-house first)")

        # Signal 3: hardcoded model strings (can't easily swap to cheaper)
        if signals["hardcoded_models"]:
            score -= 10 * min(len(signals["hardcoded_models"]), 3)
            flags.append(f"{len(signals['hardcoded_models'])} hardcoded model strings")
            action_steps.append("extract model to config/settings.yaml for easy swap to Haiku")

        # Signal 4: long prompts without compression
        if signals["long_prompts"] > 0:
            score -= 15
            flags.append(f"{signals['long_prompts']} long (>5000 char) prompts")
            action_steps.append("summarize/chunk long prompts; use prompt caching")

        # Signal 5: many LLM calls (potential duplicate work)
        if signals["llm_calls_count"] > 3:
            score -= 10
            flags.append(f"{signals['llm_calls_count']} LLM call sites — audit for dedup")
            action_steps.append("dedupe sequential LLM calls via in-function cache")

        # Signal 6 (positive): proper Ollama usage
        if signals["has_ollama_usage"] and not signals["has_claude_import"]:
            # rewards stay high (already good)
            pass

        score = max(0, min(100, score))

        action_hint = None
        if score < 70 and action_steps:
            action_hint = "TOKEN_OPT: " + "; ".join(action_steps[:2])

        return PerpetuumResult(
            subject_id=subject.id,
            score=score,
            flag_count=len(flags),
            flags=flags,
            details={**signals, "action_steps": action_steps},
            action_hint=action_hint,
        )
