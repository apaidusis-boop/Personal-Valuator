"""LLM abstraction — Ollama default, Claude escalation with budget cap.

Agents chamam `llm_summarise(prompt, prefer='ollama')`. Budget está em
data/agents/_llm_budget.json — registo de tokens gastos em Claude por dia.

Default model: qwen2.5:14b-instruct-q4_K_M local.
"""
from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_OLLAMA_MODEL = "qwen2.5:14b-instruct-q4_K_M"

ROOT = Path(__file__).resolve().parents[1]
BUDGET_PATH = ROOT / "data" / "agents" / "_llm_budget.json"


class LLMBudget:
    """Tracks daily Claude token usage; blocks if over daily cap."""

    def __init__(self, daily_cap_tokens: int = 50_000):
        self.daily_cap = daily_cap_tokens
        BUDGET_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self):
        if BUDGET_PATH.exists():
            try:
                self._data = json.loads(BUDGET_PATH.read_text(encoding="utf-8"))
            except Exception:
                self._data = {}
        else:
            self._data = {}
        today = date.today().isoformat()
        if self._data.get("date") != today:
            self._data = {"date": today, "tokens_used": 0}

    def can_spend(self, estimated_tokens: int) -> bool:
        self._load()
        return (self._data["tokens_used"] + estimated_tokens) <= self.daily_cap

    def record(self, tokens_used: int) -> None:
        self._load()
        self._data["tokens_used"] = self._data.get("tokens_used", 0) + tokens_used
        BUDGET_PATH.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def remaining(self) -> int:
        self._load()
        return max(0, self.daily_cap - self._data.get("tokens_used", 0))


def llm_summarise(
    prompt: str,
    *,
    prefer: str = "ollama",
    system: str | None = None,
    max_tokens: int = 800,
    model: str | None = None,
    temperature: float = 0.3,
) -> str:
    """Synthesize text. Ollama first (0 tokens Claude); can escalate if prefer='claude'.

    Return: text response string. Never raises; returns "[LLM FAILED]" on error.
    """
    if prefer == "ollama":
        return _ollama_call(prompt, system=system, max_tokens=max_tokens, model=model, temperature=temperature)
    elif prefer == "claude":
        # Future: anthropic API call with budget check
        return _claude_escalation(prompt, system=system, max_tokens=max_tokens)
    return "[LLM FAILED: unknown prefer]"


def _ollama_call(
    prompt: str,
    system: str | None = None,
    max_tokens: int = 800,
    model: str | None = None,
    temperature: float = 0.3,
) -> str:
    model = model or DEFAULT_OLLAMA_MODEL
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {"temperature": temperature, "num_predict": max_tokens},
            },
            timeout=180,
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"[LLM FAILED: {type(e).__name__}: {e}]"


def _claude_escalation(prompt: str, system: str | None = None, max_tokens: int = 800) -> str:
    """Escalation path — only if budget allows. Placeholder."""
    budget = LLMBudget()
    est_tokens = max_tokens + len(prompt.split()) * 2
    if not budget.can_spend(est_tokens):
        return "[CLAUDE BUDGET EXCEEDED — falling back to Ollama]"
    # Placeholder — real impl would call anthropic SDK:
    # from anthropic import Anthropic
    # msg = Anthropic().messages.create(model="claude-sonnet-4-6", ...)
    # budget.record(msg.usage.input_tokens + msg.usage.output_tokens)
    # return msg.content[0].text
    # For now, fallback:
    return _ollama_call(prompt, system=system, max_tokens=max_tokens)


def extract_json(text: str) -> dict | list | None:
    """Try to extract JSON object/array from LLM text output."""
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            return None
    return None
