"""
Head-to-head benchmark: gemma4:31b-cloud vs local Ollama models.

Usage:
    python scripts/bench_models.py

Runs the same finance-domain prompt against each model, times tokens/sec,
saves outputs for qualitative comparison.
"""
import subprocess
import time
from pathlib import Path

MODELS = [
    "gemma4:31b-cloud",
    "gemma4:31b",
    "qwen3:30b-a3b",
    "qwen2.5:32b-instruct-q4_K_M",
    "qwen2.5:14b-instruct-q4_K_M",
]

PROMPT = """You are a value-investing analyst. Analyse this thesis in <=180 words:

ITSA4 (Itausa) is a Brazilian holding company. ~93% of its NAV is its 38% stake in Itau Unibanco (ITUB4). Current P/E 6.5x, dividend yield 7.2%, payout ratio ~50%, ROE 14% (look-through). Trades at ~22% discount to NAV.

Tasks:
1. Does this pass a Graham-style screen for Brazilian non-financials? (Note: holding co, not operational.)
2. List 2 specific risks (not generic).
3. List 2 specific catalysts that could close the NAV discount.

Format: numbered, terse, no preamble."""


def run_model(model: str, prompt: str) -> dict:
    out_path = Path(f"data/benchmarks/{model.replace(':', '_').replace('/', '_')}.txt")
    t0 = time.perf_counter()
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=180,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = time.perf_counter() - t0
        output = result.stdout
        # Strip ANSI escapes / spinner chars
        import re
        clean = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", output)
        clean = re.sub(r"[⠀-⣿]", "", clean)  # braille spinners
        out_path.write_text(clean, encoding="utf-8")
        words = len(clean.split())
        return {
            "model": model,
            "elapsed_s": round(elapsed, 1),
            "words": words,
            "wps": round(words / elapsed, 1) if elapsed else 0,
            "ok": result.returncode == 0,
            "path": str(out_path),
        }
    except subprocess.TimeoutExpired:
        return {"model": model, "elapsed_s": 180.0, "ok": False, "error": "timeout"}
    except Exception as e:
        return {"model": model, "ok": False, "error": str(e)}


def main():
    print(f"{'MODEL':<35} {'TIME':>8} {'WORDS':>7} {'W/S':>6}  STATUS")
    print("-" * 70)
    results = []
    for m in MODELS:
        r = run_model(m, PROMPT)
        results.append(r)
        if r.get("ok"):
            print(f"{r['model']:<35} {r['elapsed_s']:>7.1f}s {r['words']:>7} {r['wps']:>6.1f}  ok")
        else:
            print(f"{r['model']:<35} {'-':>7}  {'-':>7} {'-':>6}  {r.get('error','fail')}")
    print()
    print("Outputs saved under data/benchmarks/")
    print("Review side-by-side to judge quality.")


if __name__ == "__main__":
    main()
