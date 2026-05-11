"""Quick t/s probe per model. Used to verify GPU offload after Postmortem 2026-05-09.

Usage: python scripts/_ollama_probe.py [model1] [model2] ...
Defaults: qwen2.5:14b-instruct-q4_K_M, qwen2.5:32b-instruct-q4_K_M
"""
from __future__ import annotations
import json
import sys
import time
import urllib.request

DEFAULT_MODELS = [
    "qwen2.5:14b-instruct-q4_K_M",
    "qwen2.5:32b-instruct-q4_K_M",
]

PROMPT = (
    "Write a single paragraph (about 200 words) explaining what makes a "
    "company a 'compounder' in the Buffett sense. Be specific and concrete."
)


def probe(model: str) -> dict:
    payload = {
        "model": model,
        "prompt": PROMPT,
        "stream": False,
        "options": {"num_predict": 250, "temperature": 0.0},
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    wall = time.time() - t0
    eval_count = data.get("eval_count", 0)
    eval_dur_ns = data.get("eval_duration", 0)
    tps = (eval_count / (eval_dur_ns / 1e9)) if eval_dur_ns else 0.0
    return {
        "model": model,
        "wall_s": round(wall, 2),
        "tokens": eval_count,
        "tokens_per_sec": round(tps, 1),
        "load_s": round(data.get("load_duration", 0) / 1e9, 2),
    }


if __name__ == "__main__":
    models = sys.argv[1:] or DEFAULT_MODELS
    for m in models:
        try:
            r = probe(m)
            print(f"{r['model']:40s}  {r['tokens_per_sec']:6.1f} t/s  "
                  f"({r['tokens']} tok in {r['wall_s']}s, load {r['load_s']}s)")
        except Exception as e:
            print(f"{m:40s}  ERROR: {type(e).__name__}: {e}")
