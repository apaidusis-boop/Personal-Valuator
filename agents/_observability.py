"""Phase W.6.3 — Observability infrastructure.

Lightweight trace decorator for LLM calls. Two writers:

1. **Local JSONL** (always on, zero deps): one file per day at
   ``data/traces/llm_traces_YYYY-MM-DD.jsonl``. Inspect with grep/jq.
   Used to answer "what was the prompt that produced answer X?" months later.

2. **LangFuse** (optional, opt-in via env var): when ``LANGFUSE_HOST`` +
   ``LANGFUSE_PUBLIC_KEY`` + ``LANGFUSE_SECRET_KEY`` are set, traces also
   forward to LangFuse for visual exploration. Self-host via Docker
   compose at ``config/langfuse/docker-compose.yml`` (NOT auto-deployed —
   user runs ``docker compose up -d`` manually).

Usage:
    from agents._observability import trace_llm_call

    @trace_llm_call(name="ollama_call")
    def ollama_call(...): ...

The decorator captures: input prompt (truncated), output (truncated),
model, latency, error class. NEVER captures secrets / API keys.
"""
from __future__ import annotations

import functools
import json
import os
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, TypeVar

ROOT = Path(__file__).resolve().parent.parent
TRACES_DIR = ROOT / "data" / "traces"
TRACES_DIR.mkdir(parents=True, exist_ok=True)

PROMPT_TRUNCATE = 2000  # chars
OUTPUT_TRUNCATE = 2000

F = TypeVar("F", bound=Callable[..., Any])


def _trace_path() -> Path:
    return TRACES_DIR / f"llm_traces_{date.today().isoformat()}.jsonl"


def _truncate(text: Any, limit: int) -> str:
    if text is None:
        return ""
    s = str(text)
    if len(s) <= limit:
        return s
    return s[:limit] + f"... [truncated {len(s) - limit} chars]"


def _write_local(record: dict) -> None:
    try:
        with _trace_path().open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except OSError:
        pass  # tracing must never break the actual call


def _langfuse_forward(record: dict) -> None:
    """Optional: forward to LangFuse if configured. No-op otherwise."""
    if not os.getenv("LANGFUSE_HOST"):
        return
    try:
        # lazy import — langfuse SDK is optional
        from langfuse import Langfuse  # type: ignore
        client = Langfuse(
            host=os.getenv("LANGFUSE_HOST"),
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        )
        client.generation(
            name=record.get("name"),
            model=record.get("model"),
            input=record.get("input"),
            output=record.get("output"),
            metadata={"latency_ms": record.get("latency_ms"),
                      "error": record.get("error")},
            start_time=datetime.fromisoformat(record["ts"]),
        )
    except Exception:
        pass  # silent — local trace is the source of truth


def trace_llm_call(name: str) -> Callable[[F], F]:
    """Decorator. Wraps an LLM-call function so each invocation is recorded.

    Captures:
      - timestamp (ISO UTC)
      - name (decorator argument; stable across versions)
      - model (kwarg or first positional that looks like a model id)
      - input (first arg, truncated)
      - output (return value, truncated; or error class if exception)
      - latency_ms

    Decorated function's behaviour is unchanged. Failures in tracing
    NEVER affect the wrapped function's return value or exceptions.
    """
    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            t0 = time.time()
            ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
            input_capture = _truncate(args[0] if args else kwargs.get("prompt"), PROMPT_TRUNCATE)
            model = kwargs.get("model") or "(default)"
            error: str | None = None
            output_capture = ""
            try:
                result = fn(*args, **kwargs)
                output_capture = _truncate(result, OUTPUT_TRUNCATE)
                return result
            except Exception as e:
                error = f"{type(e).__name__}: {e}"
                raise
            finally:
                record = {
                    "ts": ts,
                    "name": name,
                    "model": model,
                    "input": input_capture,
                    "output": output_capture,
                    "latency_ms": int((time.time() - t0) * 1000),
                    "error": error,
                }
                _write_local(record)
                _langfuse_forward(record)
        return wrapper  # type: ignore[return-value]
    return decorator


def get_today_stats() -> dict:
    """Quick aggregate over today's traces — useful for /api/health endpoint."""
    p = _trace_path()
    if not p.exists():
        return {"calls": 0, "errors": 0, "avg_latency_ms": 0}
    total = 0
    errors = 0
    latency_sum = 0
    by_name: dict[str, int] = {}
    try:
        with p.open(encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                total += 1
                if rec.get("error"):
                    errors += 1
                latency_sum += rec.get("latency_ms", 0) or 0
                n = rec.get("name") or "?"
                by_name[n] = by_name.get(n, 0) + 1
    except OSError:
        pass
    return {
        "calls": total,
        "errors": errors,
        "avg_latency_ms": int(latency_sum / total) if total else 0,
        "by_name": by_name,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        print(json.dumps(get_today_stats(), indent=2))
    else:
        print("Usage: python -m agents._observability stats")
