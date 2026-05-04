"""agent_call — canonical wrapper for role-based LLM dispatch.

ARQUITECTURA: Agentes decidem, modelos executam.

`agent_call(role, input, ...)` faz:
  1. Resolve role config from config/agents_governance.yaml
  2. Look up dedup cache via _memory.last_for_input(hash)
  3. If cache miss → render prompt template → call ollama_call
  4. Parse output through role's expected schema
  5. Retry on parse/schema failure (up to N times)
  6. Escalate to bigger model on repeated failure
  7. Record outcome in _memory.record(...)

Each role provides a render_prompt() and a parse_output() function in
agents/roles/<role>.py. Roles are loaded lazily on first use.

Uso típico (caller):

    from agents._agent import agent_call

    out = agent_call(
        role="classification",
        input={"text": "Analyst raised target",
               "labels": ["bullish", "neutral", "bearish"]},
        ticker="AAPL",
        market="us",
        run_id="overnight_2026-05-04",
    )
    print(out["label"], out["confidence"])
"""
from __future__ import annotations

import importlib
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

import yaml

from agents import _memory
from agents._llm import ollama_call

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "agents_governance.yaml"


# ============================================================
# Config loader (cached)
# ============================================================
@lru_cache(maxsize=1)
def _config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing {CONFIG_PATH}")
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}


def role_config(role: str) -> dict:
    cfg = _config()
    roles = cfg.get("roles") or {}
    if role not in roles:
        raise ValueError(f"Unknown role: {role}. Available: {list(roles)}")
    return roles[role]


def defaults_config() -> dict:
    return _config().get("defaults") or {}


def escalation_config() -> dict:
    return _config().get("escalation") or {}


# ============================================================
# Role module loader — agents.roles.<role>.render_prompt + parse_output
# ============================================================
@lru_cache(maxsize=16)
def _role_module(role: str):
    return importlib.import_module(f"agents.roles.{role}")


# ============================================================
# Public API
# ============================================================
class AgentCallError(RuntimeError):
    """Raised when a role call exhausts retries + escalation."""


def agent_call(
    role: str,
    input: dict[str, Any],
    *,
    ticker: str | None = None,
    market: str | None = None,
    run_id: str | None = None,
    use_cache: bool = True,
    max_retries: int | None = None,
    force_model: str | None = None,
    raise_on_failure: bool = False,
) -> dict[str, Any]:
    """Dispatch a task to a role specialist.

    Args:
        role: 'research' | 'synthesis' | 'critic' | 'decision' |
              'extraction' | 'classification'
        input: role-specific input dict (each role validates internally)
        ticker / market: metadata for memory + audit
        run_id: optional batch correlator
        use_cache: if True, hit _memory.last_for_input first
        max_retries: override config default
        force_model: override role's default model
        raise_on_failure: if True, raises AgentCallError on exhausted retries

    Returns:
        dict with role-specific output, plus meta:
          {"_meta": {"role", "model", "attempts", "cached", "escalated",
                     "latency_ms", "input_hash", "decision_id"}, ...}
        On final failure (raise_on_failure=False): {"_meta": {...,
          "success": False, "error": "..."}, ...}
    """
    cfg = role_config(role)
    defaults = defaults_config()
    role_module = _role_module(role)

    input_hash = _memory.hash_input({"role": role, "input": input})
    primary_model = force_model or cfg["model"]
    fallback_model = cfg.get("fallback_model")
    retries = max_retries if max_retries is not None else int(defaults.get("retries", 2))

    # 1. Cache lookup
    if use_cache and defaults.get("log_to_memory", True):
        cached = _memory.last_for_input(input_hash, max_age_hours=1)
        if cached and cached["output"] is not None:
            return _attach_meta(
                cached["output"],
                role=role, model=cached["model"],
                attempts=cached["attempts"], cached=True,
                escalated=False, latency_ms=0,
                input_hash=input_hash, decision_id=cached["id"],
                success=True,
            )

    # 2. Live call with retry + escalation
    attempts = 0
    escalated = False
    last_error = ""
    output: dict | None = None

    model_chain = [primary_model]
    if fallback_model and fallback_model != primary_model:
        model_chain.append(fallback_model)

    for model in model_chain:
        for _ in range(retries + 1):
            attempts += 1
            t0 = time.time()
            try:
                prompt = role_module.render_prompt(input)
            except Exception as e:  # noqa: BLE001
                last_error = f"render_prompt failed: {e}"
                break
            raw = ollama_call(
                prompt,
                system=cfg.get("system_prompt"),
                max_tokens=cfg.get("max_tokens", 800),
                model=model,
                temperature=cfg.get("temperature", 0.3),
                seed=cfg.get("seed"),
                json_mode=cfg.get("json_mode", False),
            )
            latency_ms = int((time.time() - t0) * 1000)
            if raw.startswith("[LLM FAILED"):
                last_error = raw
                continue
            try:
                output = role_module.parse_output(raw, input)
            except Exception as e:  # noqa: BLE001
                last_error = f"parse_output failed: {type(e).__name__}: {e}"
                continue
            if output is not None:
                # success — record + return
                meta_decision = {
                    "role": role,
                    "task": input.get("task") or role,
                    "ticker": ticker,
                    "market": market,
                    "model": model,
                    "input_hash": input_hash,
                    "output_summary": str(output)[:200],
                    "output": output,
                    "success": True,
                    "attempts": attempts,
                    "latency_ms": latency_ms,
                    "escalated": escalated,
                    "run_id": run_id,
                }
                decision_id = _memory.record(meta_decision)
                return _attach_meta(
                    output, role=role, model=model, attempts=attempts,
                    cached=False, escalated=escalated, latency_ms=latency_ms,
                    input_hash=input_hash, decision_id=decision_id,
                    success=True,
                )
        # All retries on this model failed — escalate to next in chain
        if model != model_chain[-1]:
            escalated = True

    # 3. Fully failed — record + return error
    meta_decision = {
        "role": role,
        "task": input.get("task") or role,
        "ticker": ticker,
        "market": market,
        "model": model_chain[-1],
        "input_hash": input_hash,
        "output_summary": f"FAILED: {last_error}"[:200],
        "output": None,
        "success": False,
        "attempts": attempts,
        "latency_ms": 0,
        "escalated": escalated,
        "run_id": run_id,
        "notes": last_error,
    }
    decision_id = _memory.record(meta_decision)
    if raise_on_failure:
        raise AgentCallError(
            f"agent_call({role}) failed after {attempts} attempts: {last_error}"
        )
    return _attach_meta(
        {}, role=role, model=model_chain[-1], attempts=attempts,
        cached=False, escalated=escalated, latency_ms=0,
        input_hash=input_hash, decision_id=decision_id,
        success=False, error=last_error,
    )


def _attach_meta(output: dict, **meta) -> dict:
    """Wrap output with _meta dict — non-destructive."""
    out = dict(output) if output else {}
    out["_meta"] = meta
    return out


# ============================================================
# Smoke test CLI
# ============================================================
if __name__ == "__main__":
    import argparse
    import json

    ap = argparse.ArgumentParser(description="agent_call smoke test")
    ap.add_argument("role")
    ap.add_argument("--input", required=True, help="JSON input dict")
    ap.add_argument("--ticker")
    ap.add_argument("--market")
    args = ap.parse_args()

    inp = json.loads(args.input)
    out = agent_call(args.role, inp, ticker=args.ticker, market=args.market)
    print(json.dumps(out, indent=2, default=str))
