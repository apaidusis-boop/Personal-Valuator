"""Tests for agents/_agent.py + roles/* — contract conformance with mocked LLM.

Mocks ollama_call to return canned strings so tests are 100% offline.
Tests focus on:
  - agent_call dispatches to right role module
  - parse_output rejects malformed JSON / wrong labels / out-of-range conf
  - retry kicks in on parse fail
  - escalation chain (primary → fallback model)
  - memory cache hit prevents re-call
  - meta dict shape
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents import _agent, _memory


@pytest.fixture(autouse=True)
def isolate_memory(tmp_path, monkeypatch):
    """Redirect agent decisions DB to tmp."""
    monkeypatch.setattr(_memory, "DB_PATH", tmp_path / "test_decisions.db")
    yield


# ============================================================
# Helpers
# ============================================================
def _mock_ollama(responses: list[str]):
    """Returns a side_effect that yields each response once. Cycles indefinitely
    if exhausted (so retry tests don't crash on extra calls)."""
    state = {"i": 0}
    def f(prompt, **kw):
        i = min(state["i"], len(responses) - 1)
        state["i"] += 1
        return responses[i]
    return f


# ============================================================
# Classification role
# ============================================================
def test_classification_happy_path():
    canned = json.dumps({"label": "bullish", "confidence": 0.9, "rationale": "..."})
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned])):
        out = _agent.agent_call(
            "classification",
            {"text": "Goldman raised target", "labels": ["bullish", "neutral", "bearish"]},
            use_cache=False,
        )
    assert out["label"] == "bullish"
    assert out["confidence"] == 0.9
    assert out["_meta"]["success"] is True
    assert out["_meta"]["attempts"] == 1
    assert out["_meta"]["cached"] is False


def test_classification_rejects_unknown_label():
    canned_bad = json.dumps({"label": "EXPLODE", "confidence": 0.5})
    canned_ok = json.dumps({"label": "neutral", "confidence": 0.6})
    with patch("agents._agent.ollama_call",
               side_effect=_mock_ollama([canned_bad, canned_ok])):
        out = _agent.agent_call(
            "classification",
            {"text": "x", "labels": ["bullish", "neutral", "bearish"]},
            use_cache=False,
        )
    # First raw output failed (label not in allowed); retry succeeded.
    assert out["label"] == "neutral"
    assert out["_meta"]["attempts"] >= 2


def test_classification_rejects_invalid_confidence():
    canned = json.dumps({"label": "bullish", "confidence": "not a number"})
    canned_ok = json.dumps({"label": "bullish", "confidence": 0.7})
    with patch("agents._agent.ollama_call",
               side_effect=_mock_ollama([canned, canned_ok])):
        out = _agent.agent_call(
            "classification",
            {"text": "x", "labels": ["bullish", "neutral", "bearish"]},
            use_cache=False,
        )
    assert out["confidence"] == 0.7


def test_classification_full_failure_returns_meta_with_error():
    with patch("agents._agent.ollama_call",
               side_effect=_mock_ollama(["[LLM FAILED: timeout]"])):
        out = _agent.agent_call(
            "classification",
            {"text": "x", "labels": ["a", "b"]},
            use_cache=False,
        )
    assert out["_meta"]["success"] is False
    assert "error" in out["_meta"]


# ============================================================
# Extraction role
# ============================================================
def test_extraction_returns_only_requested_fields():
    canned = json.dumps({
        "ceo": "Tim Cook",
        "revenue": 94.9,
        "extra_unrequested": "should be dropped",
    })
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned])):
        out = _agent.agent_call(
            "extraction",
            {"text": "Apple Q3 ...",
             "fields": {"ceo": "name of CEO", "revenue": "USD billions"}},
            use_cache=False,
        )
    assert out["ceo"] == "Tim Cook"
    assert out["revenue"] == 94.9
    assert "extra_unrequested" not in out


def test_extraction_missing_field_becomes_null():
    canned = json.dumps({"ceo": "Tim Cook"})  # 'revenue' omitted
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned])):
        out = _agent.agent_call(
            "extraction",
            {"text": "x", "fields": {"ceo": "x", "revenue": "y"}},
            use_cache=False,
        )
    assert out["ceo"] == "Tim Cook"
    assert out["revenue"] is None


# ============================================================
# Decision role
# ============================================================
def test_decision_rejects_unknown_verdict():
    canned_bad = json.dumps({"verdict": "MAYBE", "confidence": 0.5,
                              "reasoning": "x", "drivers": []})
    canned_ok = json.dumps({"verdict": "HOLD", "confidence": 0.6,
                             "reasoning": "x", "drivers": []})
    with patch("agents._agent.ollama_call",
               side_effect=_mock_ollama([canned_bad, canned_ok])):
        out = _agent.agent_call(
            "decision",
            {"subject": "AAPL",
             "perspectives": [{"name": "X", "stance": "BUY", "argument": "..."}]},
            use_cache=False,
        )
    assert out["verdict"] == "HOLD"


# ============================================================
# Memory cache
# ============================================================
def test_memory_cache_hit_skips_llm():
    canned = json.dumps({"label": "neutral", "confidence": 0.5})
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned])) as mock:
        _agent.agent_call(
            "classification",
            {"text": "same input", "labels": ["bullish", "neutral", "bearish"]},
            ticker="AAPL",
        )
        # Second call: same input → should hit cache
        out2 = _agent.agent_call(
            "classification",
            {"text": "same input", "labels": ["bullish", "neutral", "bearish"]},
            ticker="AAPL",
        )
    assert mock.call_count == 1                      # only 1 LLM call total
    assert out2["_meta"]["cached"] is True


def test_memory_cache_disabled_with_use_cache_false():
    canned = json.dumps({"label": "neutral", "confidence": 0.5})
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned, canned])) as mock:
        _agent.agent_call(
            "classification",
            {"text": "x", "labels": ["bullish", "neutral", "bearish"]},
            use_cache=False,
        )
        _agent.agent_call(
            "classification",
            {"text": "x", "labels": ["bullish", "neutral", "bearish"]},
            use_cache=False,
        )
    assert mock.call_count == 2                       # both went through


# ============================================================
# Escalation
# ============================================================
def test_escalation_to_fallback_model():
    """3B fallback config: classification fallback to 14B."""
    bad = "garbage non-json"
    canned_ok = json.dumps({"label": "bullish", "confidence": 0.8})
    # bad x retries on primary, then OK on fallback
    with patch("agents._agent.ollama_call",
               side_effect=_mock_ollama([bad, bad, bad, canned_ok])) as mock:
        out = _agent.agent_call(
            "classification",
            {"text": "x", "labels": ["bullish", "neutral", "bearish"]},
            use_cache=False,
        )
    assert out["label"] == "bullish"
    assert out["_meta"]["escalated"] is True
    assert out["_meta"]["attempts"] >= 4


# ============================================================
# Memory stats
# ============================================================
# ============================================================
# LLM routing enforcement (P3)
# ============================================================
def test_force_model_rejects_unknown_model():
    """force_model must be in role's allowed set; rogue models raise."""
    with pytest.raises(_agent.ModelRoutingError) as exc:
        _agent.agent_call(
            "classification",
            {"text": "hi", "labels": ["a", "b"]},
            force_model="claude-3-opus-rogue",
            use_cache=False,
        )
    assert "claude-3-opus-rogue" in str(exc.value)
    assert "classification" in str(exc.value)


def test_force_model_accepts_role_primary():
    """Forcing the role's own primary model is always allowed."""
    cfg = _agent.role_config("classification")
    canned = json.dumps({"label": "a", "confidence": 0.9})
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned])):
        out = _agent.agent_call(
            "classification",
            {"text": "hi", "labels": ["a", "b"]},
            force_model=cfg["model"],
            use_cache=False,
        )
    assert out["_meta"]["success"] is True
    assert out["_meta"]["model"] == cfg["model"]


def test_force_model_accepts_fallback_model():
    """Forcing the role's declared fallback_model is allowed."""
    cfg = _agent.role_config("classification")
    fb = cfg.get("fallback_model")
    if not fb:
        pytest.skip("no fallback_model declared for classification")
    canned = json.dumps({"label": "a", "confidence": 0.9})
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned])):
        out = _agent.agent_call(
            "classification",
            {"text": "hi", "labels": ["a", "b"]},
            force_model=fb,
            use_cache=False,
        )
    assert out["_meta"]["model"] == fb


def test_force_model_accepts_escalation_target():
    """The escalation target_model is allowed for any role (chain may upgrade)."""
    esc = _agent.escalation_config().get("target_model")
    if not esc:
        pytest.skip("no escalation target_model configured")
    canned = json.dumps({"label": "a", "confidence": 0.9})
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned])):
        out = _agent.agent_call(
            "classification",
            {"text": "hi", "labels": ["a", "b"]},
            force_model=esc,
            use_cache=False,
        )
    assert out["_meta"]["model"] == esc


def test_memory_stats_aggregates():
    canned = json.dumps({"label": "neutral", "confidence": 0.5})
    with patch("agents._agent.ollama_call", side_effect=_mock_ollama([canned, canned, canned])):
        _agent.agent_call("classification",
                          {"text": "a", "labels": ["bullish", "neutral", "bearish"]},
                          use_cache=False)
        _agent.agent_call("classification",
                          {"text": "b", "labels": ["bullish", "neutral", "bearish"]},
                          use_cache=False)
        _agent.agent_call("classification",
                          {"text": "c", "labels": ["bullish", "neutral", "bearish"]},
                          use_cache=False)
    s = _memory.stats(days=1)
    assert s["total"] == 3
    assert s["ok"] == 3
    by_role = {r["role"]: r for r in s["by_role"]}
    assert by_role["classification"]["count"] == 3
