"""A/B test qwen2.5:14b vs qwen3:30b-a3b for thesis synthesis quality.

Para 5 tickers: gera nova thesis com qwen3 e compara lado-a-lado
com a thesis actual no vault (escrita pelo 14b).

Output: obsidian_vault/skills/AB_qwen3_vs_14b_2026-04-26.md
NÃO sobrescreve thesis no vault — só compara.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
TICKERS_DIR = ROOT / "obsidian_vault" / "tickers"
SKILLS_DIR = ROOT / "obsidian_vault" / "skills"

OLLAMA = "http://localhost:11434/api/generate"
DEFAULT_TICKERS = ["TSLA", "AAPL", "ITSA4", "BBDC4", "ABBV"]


def vault_thesis(ticker: str) -> str | None:
    p = TICKERS_DIR / f"{ticker}.md"
    if not p.exists():
        return None
    content = p.read_text(encoding="utf-8", errors="ignore")
    if "## Thesis" not in content:
        return None
    after = content.split("## Thesis", 1)[1]
    end = after.find("\n## ")
    return after[:end].strip() if end > 0 else after.strip()


def vault_context(ticker: str) -> str:
    """Pull metadata + holdings/sector/etc lines from the ticker file."""
    p = TICKERS_DIR / f"{ticker}.md"
    if not p.exists():
        return ""
    content = p.read_text(encoding="utf-8", errors="ignore")
    # Take frontmatter + first 1.2k chars
    return content[:1500]


PROMPT_TMPL = """Sintetiza uma thesis de investimento concisa para o ticker {ticker}.

CONTEXTO disponível:
{context}

ESTRUTURA exigida (markdown):

**Intent**: DRIP / Compounder / Growth / Value / Tactical
**Core thesis**: 2-3 frases sobre porquê é hold/buy. Foca em moat, fundamentais, posicionamento.
**Disconfirmation triggers**: 2-3 sinais que invalidam a thesis (ex: dividend cut, ROE < 12%, debt/EBITDA > 4x).
**Time horizon**: 5y / 10y / indefinite

Reply em PORTUGUÊS DE PORTUGAL. Sem disclaimers genéricos. Nada de listas de bullets fora do template."""


def synth(model: str, ticker: str, context: str, timeout: int = 240) -> tuple[str, float]:
    prompt = PROMPT_TMPL.format(ticker=ticker, context=context)
    t0 = time.monotonic()
    payload: dict = {"model": model, "prompt": prompt, "stream": False,
                     "options": {"temperature": 0.3, "num_predict": 800}}
    # qwen3 family uses thinking mode by default — disable to get usable output.
    if "qwen3" in model:
        payload["think"] = False
    r = requests.post(OLLAMA, json=payload, timeout=timeout)
    r.raise_for_status()
    elapsed = time.monotonic() - t0
    return r.json().get("response", "").strip(), elapsed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", nargs="*", default=DEFAULT_TICKERS)
    ap.add_argument("--model-a", default="qwen2.5:14b-instruct-q4_K_M")
    ap.add_argument("--model-b", default="qwen3:30b-a3b")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    out_path = Path(args.out) if args.out else SKILLS_DIR / f"AB_qwen3_vs_14b_{date.today().isoformat()}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "---",
        f"type: ab_test",
        f"date: {date.today().isoformat()}",
        f"model_a: {args.model_a}",
        f"model_b: {args.model_b}",
        f"tickers: {args.tickers}",
        "tags: [ab_test, model_eval]",
        "---",
        "",
        f"# 🧪 A/B Test — {args.model_a} vs {args.model_b}",
        "",
        f"**Date**: {date.today().isoformat()}",
        f"**Model A** (current): `{args.model_a}`",
        f"**Model B** (candidate): `{args.model_b}`",
        f"**Tickers**: {', '.join(args.tickers)}",
        "",
        "## Methodology",
        "",
        "Para cada ticker:",
        "1. Vault thesis actual (escrita pelo Model A) → coluna 'Current'",
        "2. Re-synth com Model A → 'Model A new'",
        "3. Re-synth com Model B → 'Model B new'",
        "4. Comparação lado-a-lado",
        "",
        "Métricas: tempo de inferência (s), comprimento (chars), aderência ao template.",
        "",
    ]

    timings_a, timings_b = [], []
    for ticker in args.tickers:
        ctx = vault_context(ticker)
        current = vault_thesis(ticker) or "_(no thesis)_"
        print(f"[{ticker}] Model A...")
        try:
            new_a, t_a = synth(args.model_a, ticker, ctx)
            timings_a.append(t_a)
        except Exception as e:
            new_a, t_a = f"(error: {e})", 0
        print(f"  {t_a:.1f}s")
        print(f"[{ticker}] Model B...")
        try:
            new_b, t_b = synth(args.model_b, ticker, ctx)
            timings_b.append(t_b)
        except Exception as e:
            new_b, t_b = f"(error: {e})", 0
        print(f"  {t_b:.1f}s")

        lines += [
            "---",
            "",
            f"## {ticker}",
            "",
            f"### Current (vault)",
            "",
            current[:1500],
            "",
            f"### {args.model_a} (re-synth, t={t_a:.1f}s, {len(new_a)} chars)",
            "",
            new_a[:1500],
            "",
            f"### {args.model_b} (t={t_b:.1f}s, {len(new_b)} chars)",
            "",
            new_b[:1500],
            "",
        ]

    lines += [
        "---",
        "",
        "## Summary",
        "",
        f"- Avg time {args.model_a}: {sum(timings_a)/max(len(timings_a),1):.1f}s",
        f"- Avg time {args.model_b}: {sum(timings_b)/max(len(timings_b),1):.1f}s",
        f"- Speed ratio (B/A): {sum(timings_b)/max(sum(timings_a),0.1):.2f}×",
        "",
        "## Decision",
        "",
        "_Manual review by user. Compare outputs, decide if Model B quality justifies any speed delta._",
        "",
    ]

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n✓ Written: {out_path}")
    print(f"  A avg: {sum(timings_a)/max(len(timings_a),1):.1f}s")
    print(f"  B avg: {sum(timings_b)/max(len(timings_b),1):.1f}s")


if __name__ == "__main__":
    main()
