"""Confirm whether gemma4:31b actually produces degenerate output, or whether
the postmortem repetition collapse was a transient/prompt-specific issue.

Tests three regimes:
  1. temp=0.0 generic prompt (baseline)
  2. temp=0.3 synthetic_ic-style JSON-mode persona prompt
  3. format=json synthetic_ic exact wrapper
"""
from __future__ import annotations
import json
import urllib.request
import time

URL = "http://localhost:11434/api/generate"


def call(model: str, prompt: str, options: dict | None = None, fmt: str | None = None) -> dict:
    payload = {"model": model, "prompt": prompt, "stream": False,
               "options": options or {"temperature": 0.0, "num_predict": 400}}
    if fmt:
        payload["format"] = fmt
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    return {"wall": round(time.time() - t0, 2),
            "tokens": data.get("eval_count", 0),
            "response": data.get("response", "")}


def has_repetition_collapse(text: str) -> tuple[bool, str | None]:
    """Detect 'ownable ownable ownable...' style collapse.

    Heuristic: any 1-2-word phrase repeated >= 5 times consecutively.
    """
    words = text.split()
    for win in (1, 2):
        for i in range(len(words) - win * 6):
            phrase = " ".join(words[i:i + win])
            count = 1
            j = i + win
            while j + win <= len(words) and " ".join(words[j:j + win]) == phrase:
                count += 1
                j += win
                if count >= 5:
                    return True, phrase
    return False, None


SYNTHETIC_IC_PROMPT = """You are Nassim Nicholas Taleb. Apply your antifragile lens
to this stock. Required JSON output:
{"verdict": "BUY|HOLD|AVOID", "conviction": 1-10, "rationale": ["bullet 1","bullet 2"]}

TICKER: ACN  (Accenture)
SECTOR: IT Services
P/E: 24, P/B: 8.1, ROE: 28%, DivYield: 1.7%
Net cash positive. FCF growing 12%/y.
What is your verdict?"""


if __name__ == "__main__":
    model = "gemma4:31b"
    print(f"\n=== Test 1: generic prompt, temp=0.0 ===")
    r1 = call(model, "Explain in one paragraph why a moat matters in investing.",
              {"temperature": 0.0, "num_predict": 250})
    bad, phr = has_repetition_collapse(r1["response"])
    flag = "DEGENERATE" if bad else "OK"
    print(f"  {flag}  ({r1['tokens']} tok in {r1['wall']}s)")
    if bad:
        print(f"  collapse phrase: '{phr}'")
    print(f"  raw[:300] = {r1['response'][:300]!r}")

    print(f"\n=== Test 2: synthetic_ic prompt, temp=0.3 ===")
    r2 = call(model, SYNTHETIC_IC_PROMPT,
              {"temperature": 0.3, "num_predict": 400})
    bad, phr = has_repetition_collapse(r2["response"])
    flag = "DEGENERATE" if bad else "OK"
    print(f"  {flag}  ({r2['tokens']} tok in {r2['wall']}s)")
    if bad:
        print(f"  collapse phrase: '{phr}'")
    print(f"  raw[:300] = {r2['response'][:300]!r}")

    print(f"\n=== Test 3: synthetic_ic prompt, format=json, temp=0.3 ===")
    r3 = call(model, SYNTHETIC_IC_PROMPT,
              {"temperature": 0.3, "num_predict": 400}, fmt="json")
    bad, phr = has_repetition_collapse(r3["response"])
    flag = "DEGENERATE" if bad else "OK"
    print(f"  {flag}  ({r3['tokens']} tok in {r3['wall']}s)")
    if bad:
        print(f"  collapse phrase: '{phr}'")
    print(f"  raw[:500] = {r3['response'][:500]!r}")
    try:
        parsed = json.loads(r3["response"])
        print(f"  JSON parse: OK  verdict={parsed.get('verdict')} conviction={parsed.get('conviction')}")
    except Exception as e:
        print(f"  JSON parse: FAIL ({e})")
